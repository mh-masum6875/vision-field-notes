"""Figures for classification-vs-detection-vs-segmentation: four task outputs on one schematic scene, and a decision flow."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID

SLUG = "classification-vs-detection-vs-segmentation"
H, W = 120, 160
# three fruits on a belt: two touching, one apart (centre x, centre y, radius)
FRUIT = [(48, 62, 22), (86, 66, 20), (128, 58, 17)]


def scene():
    S = 4
    yy, xx = np.mgrid[0:H * S, 0:W * S] / S
    img = np.ones((H * S, W * S, 3)) * np.array([0.93, 0.925, 0.9])
    img[(yy > 40) & (yy < 92)] = [0.84, 0.83, 0.8]  # belt
    labels = np.zeros((H * S, W * S), int)
    for i, (cx, cy, r) in enumerate(FRUIT, 1):
        m = (xx - cx) ** 2 + ((yy - cy) * 1.05) ** 2 <= r * r
        labels[m & (labels == 0)] = i
        shade = 0.55 + 0.25 * np.clip(1 - ((xx - cx + r / 3) ** 2 + (yy - cy + r / 3) ** 2) / (r * r), 0, 1)
        for c, base in enumerate([0.85, 0.45, 0.25]):
            img[..., c] = np.where(m, base * shade + 0.05, img[..., c])
    return img, labels


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])


def fig_tasks():
    img, labels = scene()
    fig, axes = plt.subplots(1, 4, figsize=(12.5, 3.9))
    titles = ["Classification", "Detection", "Semantic segmentation", "Instance segmentation"]
    subs = ["one label for the image", "a box per object", "a class per pixel", "a mask per object"]
    for ax, t, s in zip(axes, titles, subs):
        ax.set_title(t, fontsize=13.5)
        ax.text(W / 2, H + 6, s, ha="center", va="top", fontsize=12, color=INK2)
        ax.set_xlim(0, W); ax.set_ylim(H + 22, 0); ax.axis("off")
    # classification
    axes[0].imshow(img, extent=(0, W, H, 0))
    axes[0].text(6, 10, "fruit: 0.97", fontsize=12.5, color="white", va="top", weight="bold",
                 bbox=dict(fc=ACCENT, ec="none", pad=3))
    # detection
    axes[1].imshow(img, extent=(0, W, H, 0))
    for cx, cy, r in FRUIT:
        axes[1].add_patch(Rectangle((cx - r - 1, cy - r - 1), 2 * r + 2, 2 * r + 2, fill=False, ec=ACCENT, lw=2))
    # semantic: every fruit pixel the same colour, touching fruits merge into one region
    sem = img * 0.35 + 0.65
    sem[labels > 0] = hexrgb(C[1])
    axes[2].imshow(sem, extent=(0, W, H, 0))
    axes[2].text(67, 100, "touching fruits\nmerge into one region", ha="center", va="top", fontsize=10.5, color=INK)
    # instance: each fruit its own colour
    ins = img * 0.35 + 0.65
    for i, c in zip(range(1, 4), [C[0], C[2], C[4]]):
        ins[labels == i] = hexrgb(c)
    axes[3].imshow(ins, extent=(0, W, H, 0))
    axes[3].text(80, 100, "each fruit separate,\nwith its outline", ha="center", va="top", fontsize=10.5, color=INK)
    for ax in axes:
        ax.add_patch(Rectangle((0, 0), W, H, fill=False, ec=GRID, lw=1))
    fig.suptitle("The same scene, four tasks: each step right adds detail and labelling cost", fontsize=14, weight="bold", y=0.97)
    fig.tight_layout(w_pad=1.2)
    style.save(fig, f"{SLUG}-four-tasks.png")


def rbox(ax, x, y, w, h, text, color, fs=12.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=color + "1f", ec=color, lw=1.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK, linespacing=1.25)


def arrow(ax, p1, p2):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=15))


def fig_decide():
    fig, ax = plt.subplots(figsize=(10, 5.9))
    ax.axis("off")
    rows = [
        ("Is the decision about the\nwhole image (one thing per image)?", "Classification", C[0]),
        ("Do you need where objects are,\nor how many?", "Detection", C[1]),
        ("Do you need area, outline\nor shape?", "Segmentation", C[2]),
        ("Must touching objects of the\nsame type be told apart?", "Instance\nsegmentation", C[4]),
    ]
    qw, h, ax0, aw = 50, 9, 66, 30
    ys = [46, 33, 20, 7]
    for i, ((q, a, c), y) in enumerate(zip(rows, ys)):
        rbox(ax, 0, y, qw, h, q, MUTED)
        rbox(ax, ax0, y, aw, h, a, c, fs=13.5)
        arrow(ax, (qw + 0.4, y + h / 2), (ax0 - 0.4, y + h / 2))
        ax.text((qw + ax0) / 2, y + h / 2 + 1.3, "yes", ha="center", va="bottom", fontsize=11.5, weight="bold", color=INK)
        if i < 3:
            arrow(ax, (qw / 2, y - 0.3), (qw / 2, ys[i + 1] + h + 0.3))
            ax.text(qw / 2 + 1.2, y - 2, "no" if i < 2 else "if yes, then", ha="left", va="center", fontsize=11.5, color=INK2)
    ax.text(48, 60.5, "Ask in order; the first yes is usually the simplest task that works", ha="center",
            fontsize=14, weight="bold", color=INK)
    ax.text(0, 3.5, "If segmentation is needed and touching objects do not matter, semantic segmentation is enough.",
            ha="left", va="center", fontsize=11, color=INK2, style="italic")
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(1.5, 63)
    style.save(fig, f"{SLUG}-decision-flow.png")


if __name__ == "__main__":
    fig_tasks()
    fig_decide()
