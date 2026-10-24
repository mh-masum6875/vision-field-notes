"""Figures for choosing-yolo-model-size: real detections as objects lose pixels, and the six-step method."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, OUT
import detect

SLUG = "choosing-yolo-model-size"


def annot(img, dets, k=2, color=(92, 107, 11), fs=1.1, thick=3):
    im = cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_NEAREST)
    for x1, y1, x2, y2, s, n in dets:
        p1, p2 = (int(x1 * k), int(y1 * k)), (int(x2 * k), int(y2 * k))
        cv2.rectangle(im, p1, p2, color, thick)
        t = f"{n} {s:.2f}"
        (tw, th), _ = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, fs, 2)
        y0 = max(p1[1], th + 12)
        x0 = max(0, min(p1[0], im.shape[1] - tw - 10))
        cv2.rectangle(im, (x0, y0 - th - 12), (x0 + tw + 10, y0), color, -1)
        cv2.putText(im, t, (x0 + 5, y0 - 7), cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 255), 2, cv2.LINE_AA)
    return im[:, :, ::-1]


def save_jpg_fig(fig, name, width_px=1400):
    w = fig.get_size_inches()[0]
    fig.savefig(OUT / name, dpi=width_px / w, bbox_inches="tight", pad_inches=0.12, pil_kwargs={"quality": 85})
    plt.close(fig)


def fig_shrink():
    img = detect.frame("retail", 0.92)
    h, w = img.shape[:2]
    ref = [d for d in detect.detect(img, 0.25) if d[5] == "person"]
    ref_h = np.median([d[3] - d[1] for d in ref])  # typical person height in the original frame
    fig, axes = plt.subplots(2, 2, figsize=(11, 6.9))
    for ax, f in zip(axes.flat, [1, 3, 4, 6]):
        small = cv2.resize(img, (w // f, h // f), interpolation=cv2.INTER_AREA)
        back = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)  # same frame, 1/f of the detail
        d = detect.detect(back, 0.25)
        npers = sum(1 for x in d if x[5] == "person")
        print(f, [(n, round(s, 2)) for *_, s, n in d])
        ax.imshow(annot(back, d))
        ax.set_title(f"{'Original' if f == 1 else f'Shrunk {f}x'}: people about {ref_h / f:.0f} px tall, {npers} of 3 found",
                     loc="left", fontsize=12.5)
        ax.axis("off")
    fig.tight_layout(h_pad=1.0, w_pad=1.0)
    save_jpg_fig(fig, f"{SLUG}-object-pixels.jpg", width_px=1250)


def rbox(ax, x, y, w, h, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=color + "1f", ec=color, lw=1.8))


def arrow(ax, p1, p2, conn=None):
    props = dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=15)
    if conn:
        props["connectionstyle"] = conn
    ax.annotate("", xy=p2, xytext=p1, arrowprops=props)


def fig_method():
    steps = [
        ("1  Set the budget", "frame rate, streams,\nhardware, power, memory"),
        ("2  Accuracy target", "e.g. recall needed at a\nprecision you can accept"),
        ("3  Shortlist 2 or 3", "smallest plausible size\nand one size up"),
        ("4  Train identically", "same split, input size,\nepochs, augmentation"),
        ("5  Measure on device", "exported model, timed\nend to end on real input"),
        ("6  Pick the cheapest", "that meets accuracy and\ntime, with headroom"),
    ]
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    ax.axis("off")
    bw, bh = 30, 15
    pos = [(0, 33), (35, 33), (70, 33), (0, 8), (35, 8), (70, 8)]
    for i, ((t, s), (x, y)) in enumerate(zip(steps, pos)):
        c = ACCENT if i == 5 else C[0]
        rbox(ax, x, y, bw, bh, c)
        ax.text(x + 1.8, y + bh - 3.6, t, ha="left", va="center", fontsize=12.5, weight="bold", color=INK)
        ax.text(x + 1.8, y + 5, s, ha="left", va="center", fontsize=11.5, color=INK2, linespacing=1.3)
    arrow(ax, (30.3, 40.5), (34.7, 40.5))
    arrow(ax, (65.3, 40.5), (69.7, 40.5))
    ax.plot([85, 85, 15], [32.7, 28.2, 28.2], color=INK2, lw=1.6, solid_capstyle="butt")
    arrow(ax, (15, 28.2), (15, 23.3))
    arrow(ax, (30.3, 15.5), (34.7, 15.5))
    arrow(ax, (65.3, 15.5), (69.7, 15.5))
    # fallback loop
    ax.text(50, 3.5, "None passes? Lower the frame rate, crop the region, improve the data or change the hardware.",
            ha="center", va="top", fontsize=11, color=INK2, style="italic")
    ax.text(50, 54, "Pick the model size from a budget and a test, not a leaderboard", ha="center", fontsize=14,
            weight="bold", color=INK)
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(-3.5, 57)
    style.save(fig, f"{SLUG}-method.png")


if __name__ == "__main__":
    fig_shrink()
    fig_method()
