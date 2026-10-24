"""Figures for train-val-test-split-video-frames."""
import io
import cv2
import numpy as np
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT
from matplotlib.patches import Rectangle, Patch
import detect

SLUG = "train-val-test-split-video-frames"
TRAIN, VAL, GAP = C[0], C[1], "#d9d8d3"


def fig_to_jpg(fig, name, width=1300):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    return detect.save_jpg(img, name, width=width)


# ---- Figure 1: three ways to split, as frame strips ----
def split_diagram():
    rng = np.random.default_rng(11)
    n = 20  # frames per video in the drawing
    fig, ax = plt.subplots(figsize=(10, 6.6))
    ax.set_xlim(-2.6, 3 * n + 4); ax.set_ylim(-0.6, 11.5)
    ax.axis("off")
    sq = 0.85

    def strip(x0, y, colors):
        for i, c in enumerate(colors):
            ax.add_patch(Rectangle((x0 + i, y), sq, sq * 1.4, fc=c, ec="none"))

    rows = [
        (8.4, "Random frame split", "neighbouring frames land on both sides: leaks"),
        (4.6, "Split by video", "each video entirely on one side"),
        (0.8, "One long recording", "time blocks with an unused gap between them"),
    ]
    for y, title, sub in rows:
        ax.text(0, y + 2.05, title, fontsize=13, fontweight="bold", color=INK, va="bottom")
        ax.text(0, y + 1.4, sub, fontsize=12, color=INK2, va="bottom")
    # row 1
    for v in range(3):
        cols = [VAL if rng.random() < 0.2 else TRAIN for _ in range(n)]
        x0 = v * (n + 1.5)
        strip(x0, 8.4, cols)
        ax.text(x0 + n / 2, 8.05, f"video {'ABC'[v]}", ha="center", va="top", fontsize=11.5, color=INK2)
    # row 2
    for v, c in enumerate([TRAIN, TRAIN, VAL]):
        x0 = v * (n + 1.5)
        strip(x0, 4.6, [c] * n)
        ax.text(x0 + n / 2, 4.25, f"video {'ABC'[v]}", ha="center", va="top", fontsize=11.5, color=INK2)
    # row 3: one recording, continuous
    total = 3 * n + 3
    cols = [TRAIN] * 46 + [GAP] * 5 + [VAL] * (total - 51)
    strip(0, 0.8, cols)
    ax.text(23, 0.45, "earlier weeks", ha="center", va="top", fontsize=11.5, color=INK2)
    ax.text(48.5, 0.45, "gap", ha="center", va="top", fontsize=11.5, color=INK2)
    ax.text(57, 0.45, "later weeks", ha="center", va="top", fontsize=11.5, color=INK2)
    ax.legend(handles=[Patch(fc=TRAIN, label="training frame"), Patch(fc=VAL, label="validation frame"),
                       Patch(fc=GAP, label="unused")], loc="upper center", bbox_to_anchor=(0.5, 0.02),
              ncol=3, fontsize=12)
    ax.set_title("Split by the unit that groups similar frames, never by single frame", loc="left")
    style.save(fig, f"{SLUG}-split-strategies.png")


# ---- Figure 2: two frames one second apart are near copies (real footage) ----
def near_copy():
    s = "people"
    cap = cv2.VideoCapture(f"{detect.BENCH}/samples/{s}.mp4")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps = cap.get(cv2.CAP_PROP_FPS)
    i0 = int(n * 0.70)
    frames = []
    for i in (i0, i0 + int(fps)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, im = cap.read()
        frames.append(im)
    cap.release()
    a, b = frames
    da, db = detect.detect(a), detect.detect(b)
    diff = cv2.absdiff(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY))
    changed = float((diff > 25).mean() * 100)
    print(f"pixels changed by >25 levels: {changed:.1f}%  dets {len(da)} {len(db)}")
    fig, axes = plt.subplots(1, 3, figsize=(10, 2.9))
    panels = [(detect.draw(a, da, thick=3, label=False)[:, :, ::-1], f"Training frame, t = {i0 / fps:.1f} s"),
              (detect.draw(b, db, thick=3, label=False)[:, :, ::-1], f"Validation frame, t = {(i0 + int(fps)) / fps:.1f} s"),
              (255 - np.minimum(255, diff.astype(np.int32) * 3).astype(np.uint8), "What changed (darker = more)")]
    for ax, (im, title) in zip(axes, panels):
        ax.imshow(im, cmap="gray" if im.ndim == 2 else None, vmin=0, vmax=255)
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_title(title, fontsize=12, color=INK)
    fig.suptitle(f"One second apart: same people, same room; only {changed:.0f}% of pixels changed noticeably",
                 fontsize=13.5, fontweight="bold", y=1.04)
    fig.tight_layout()
    fig_to_jpg(fig, f"{SLUG}-near-copies.jpg")


if __name__ == "__main__":
    split_diagram()
    near_copy()
