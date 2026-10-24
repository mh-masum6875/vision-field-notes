"""Figures for class-imbalance-and-small-objects."""
import io
import cv2
import numpy as np
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT
from matplotlib.patches import Rectangle
import detect

SLUG = "class-imbalance-and-small-objects"


def fig_to_jpg(fig, name, width=1300):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    return detect.save_jpg(img, name, width=width)


# ---- Figure 1: instance counts per class (illustrative) ----
def imbalance():
    classes = ["person", "hard hat", "safety vest", "forklift", "no hard hat"]
    counts = [4200, 3100, 2700, 900, 140]
    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    colors = [MUTED] * 4 + [C[1]]
    y = np.arange(len(classes))[::-1]
    ax.barh(y, counts, color=colors, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(classes, fontsize=13, color=INK)
    for yi, c in zip(y, counts):
        ax.text(c + 60, yi, f"{c:,}", va="center", fontsize=12, color=INK2)
    ax.set_xlabel("Labelled boxes in the training set (illustrative)")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 4900)
    ax.text(900, y[-1], "the class the alert depends on:\nunder 2% of all boxes", va="center",
            fontsize=12, color=INK)
    ax.set_title("The class that matters is often the one with the fewest boxes")
    style.save(fig, f"{SLUG}-class-counts.png")


# ---- Figure 2: whole frame vs overlapping tiles (real detections) ----
TW, TH = 352, 224


def tiles_for(W, H):
    return [(x, y) for y in (0, H - TH) for x in (0, W - TW)]


def tiled_detect(img, conf=0.25, iou=0.45):
    H, W = img.shape[:2]
    out = []
    for x, y in tiles_for(W, H):
        for d in detect.detect(img[y:y + TH, x:x + TW], conf=conf, iou=iou):
            out.append((d[0] + x, d[1] + y, d[2] + x, d[3] + y, d[4], d[5]))
    if not out:
        return out
    idx = cv2.dnn.NMSBoxes([[o[0], o[1], o[2] - o[0], o[3] - o[1]] for o in out], [o[4] for o in out], conf, iou)
    return [out[i] for i in np.array(idx).reshape(-1)]


def tiling():
    img = detect.frame("retail", 0.10)
    H, W = img.shape[:2]
    full = detect.detect(img)
    tiled = tiled_detect(img)
    print("full:", sorted(d[5] for d in full))
    print("tiled:", sorted(d[5] for d in tiled))
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for ax, dets, title in [(axes[0], full, f"Whole frame resized once: {len(full)} boxes"),
                            (axes[1], tiled, f"Four overlapping tiles + NMS: {len(tiled)} boxes")]:
        ax.imshow(img[:, :, ::-1])
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
        for x1, y1, x2, y2, s, n in dets:
            ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, ec=ACCENT, lw=1.8))
            ax.text(x1 + 1, y2 - 1, n, fontsize=8.5, color="white", va="bottom", ha="left",
                    bbox=dict(fc=ACCENT, ec="none", pad=1))
        ax.set_title(title, fontsize=12.5)
    for i, (x, y) in enumerate(tiles_for(W, H)):
        axes[1].add_patch(Rectangle((x + 2, y + 2), TW - 4, TH - 4, fill=False, ec=C[i], lw=1.6, ls="--"))
    fig.suptitle("Tiling keeps more pixels per object: more small items found, and new mistakes to check",
                 fontsize=13.5, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig_to_jpg(fig, f"{SLUG}-tiling.jpg")


if __name__ == "__main__":
    imbalance()
    tiling()
