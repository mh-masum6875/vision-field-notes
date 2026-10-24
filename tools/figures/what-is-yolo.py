"""Figures for what-is-yolo: single-pass pipeline with real frames, and what the output means."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import style
from style import C, ACCENT, INK, INK2, MUTED, OUT
import detect

SLUG = "what-is-yolo"


def annot(img, dets, k=2, color=(92, 107, 11), label=True, fs=0.9, thick=3):
    """Upscale by k and draw boxes with readable labels. Returns RGB."""
    im = cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC)
    for x1, y1, x2, y2, s, n in dets:
        p1, p2 = (int(x1 * k), int(y1 * k)), (int(x2 * k), int(y2 * k))
        cv2.rectangle(im, p1, p2, color, thick)
        if label:
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


def box(ax, x, y, w, h, title, sub, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=color + "1f", ec=color, lw=1.8))
    ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", fontsize=13, weight="bold", color=INK)
    ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=11, color=INK2)


def arrow(ax, p1, p2):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=16))


def fig_pipeline():
    img = detect.frame("retail", 0.92)
    raw = detect.detect(img, 0.25, nms=False)
    final = detect.detect(img, 0.25)
    fig, ax = plt.subplots(figsize=(10, 5.05))
    ax.axis("off")
    # row 1: image -> resize -> backbone -> neck -> head
    ax.imshow(img[:, :, ::-1], extent=(0, 20, 31.4, 31.4 + 20 * 9 / 16))
    ax.text(10, 30.2, "Input frame", ha="center", va="top", fontsize=12, color=INK2)
    xs = [24, 43.3, 62.6, 81.9]
    steps = [("Resize", "fixed size,\nwith padding"), ("Backbone", "edges, then\nshapes"),
             ("Neck", "mixes detail\nand context"), ("Head", "predicts at\nseveral scales")]
    for x, (t, sub) in zip(xs, steps):
        box(ax, x, 31, 17, 12, t, sub, C[0])
    arrow(ax, (20.4, 37), (23.7, 37))
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, (a + 17.3, 37), (b - 0.3, 37))
    ax.text(50, 47.5, "One pass through one network, then a clean-up step", ha="center", fontsize=14, weight="bold", color=INK)
    # row 2: candidates -> NMS -> final
    iw = 32
    ih = iw * 9 / 16
    ax.imshow(annot(img, raw, color=(52, 104, 235), label=False, thick=2), extent=(0, iw, 4, 4 + ih))
    ax.text(iw / 2, 2.8, f"{len(raw)} overlapping candidates", ha="center", va="top", fontsize=12, color=INK2)
    box(ax, 38.5, 7, 23, 12, "NMS", "drop duplicates,\nkeep best box", C[1])
    ax.imshow(annot(img, final, fs=1.1), extent=(68, 68 + iw, 4, 4 + ih))
    ax.text(68 + iw / 2, 2.8, f"{len(final)} final detections", ha="center", va="top", fontsize=12, color=INK2)
    ax.annotate("", xy=(iw / 2, 4 + ih + 0.5), xytext=(90.4, 30.7),
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=16,
                                connectionstyle="angle,angleA=-90,angleB=0,rad=0"))
    arrow(ax, (iw + 0.4, 13), (38.2, 13))
    arrow(ax, (61.8, 13), (67.6, 13))
    ax.set_xlim(0, 100); ax.set_ylim(0, 50.5)
    save_jpg_fig(fig, f"{SLUG}-single-pass.jpg")


def fig_output():
    a = detect.frame("retail", 0.92)
    b = detect.frame("people", 0.15)
    da, db = detect.detect(a, 0.25), detect.detect(b, 0.25)
    print("retail", [(n, round(s, 2)) for *_, s, n in da])
    print("people", [(n, round(s, 2)) for *_, s, n in db])
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.9))
    for ax, im, d, t in [(axes[0], a, da, "Store aisle: people found, plus low-score bowls"),
                         (axes[1], b, db, "Hallway: a person labelled dog, score 0.35")]:
        ax.imshow(annot(im, d, fs=1.1))
        ax.set_title(t, fontsize=13, loc="left")
        ax.axis("off")
    fig.tight_layout(w_pad=1.2)
    save_jpg_fig(fig, f"{SLUG}-real-output.jpg")


if __name__ == "__main__":
    fig_pipeline()
    fig_output()
