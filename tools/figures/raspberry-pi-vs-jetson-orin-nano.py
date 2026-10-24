"""Figures for raspberry-pi-vs-jetson-orin-nano."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT, save
import detect

SLUG = "raspberry-pi-vs-jetson-orin-nano"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, color=INK, size=12, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=color, fontsize=size,
            weight=weight, linespacing=1.3)


def arrow(ax, x1, y1, x2, y2, label=None, lx=0, ly=0, color=INK2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, ha="center", va="center",
                fontsize=11, color=INK2, weight="bold")


# 1. Decision flow: test the cheap board first
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.axis("off")
steps = [
    "1. Write down the\nrequirement: cameras,\nresolution, rate, latency",
    "2. Smallest model that\nmeets accuracy\non your own data",
    "3. Run it on the Pi\nmeasure end-to-end\nthroughput",
]
for i, s in enumerate(steps):
    box(ax, 0.1 + i * 3.35, 3.7, 3.0, 1.5, s, fc="#f4f3ef")
    if i < 2:
        arrow(ax, 3.1 + i * 3.35, 4.45, 3.45 + i * 3.35, 4.45)
# question
box(ax, 6.8, 1.85, 3.0, 1.1, "Meets the\nrequirement?", fc="#ffffff", ec=ACCENT, weight="bold")
arrow(ax, 8.3, 3.7, 8.3, 2.95)
box(ax, 6.8, 0.15, 3.0, 1.0, "Ship the Pi", fc="#e7f5e7", ec=GOOD, weight="bold")
arrow(ax, 8.3, 1.85, 8.3, 1.15, "yes", lx=0.35)
box(ax, 3.5, 1.65, 2.6, 1.5, "Try first:\nsmaller input,\nframe skipping", fc="#ffffff")
arrow(ax, 6.8, 2.4, 6.1, 2.4, "no", ly=0.25)
box(ax, 0.1, 1.65, 2.75, 1.5, "Still short?\nAdd an accelerator\nor move to Jetson", fc="#fdf0e9", ec=C[1])
arrow(ax, 3.5, 2.4, 2.85, 2.4)
arrow(ax, 4.8, 3.15, 4.8, 3.7, color=MUTED)
ax.text(5.0, 3.42, "re-measure", fontsize=10, color=MUTED, va="center")
ax.set_title("Start on the cheaper board and move up only when a measurement fails", loc="left")
save(fig, f"{SLUG}-decision-flow.png")

# 2. Real footage: a person stays in view for many frames
fps = 15
idxs = [45, 60, 75, 90, 105, 120]
tiles = []
for i in idxs:
    img = detect.frame("safety", i / 360)
    dets = [d for d in detect.detect(img) if d[5] == "person"]
    im = detect.draw(img, dets)
    t = f"t = {(i - idxs[0]) / fps:.0f} s"
    cv2.rectangle(im, (0, 0), (110, 34), (255, 255, 255), -1)
    cv2.putText(im, t, (8, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (11, 11, 11), 2, cv2.LINE_AA)
    tiles.append(im)
pad = np.full((360, 8, 3), 255, np.uint8)
row1 = np.hstack([tiles[0], pad, tiles[1], pad, tiles[2]])
row2 = np.hstack([tiles[3], pad, tiles[4], pad, tiles[5]])
grid = np.vstack([row1, np.full((8, row1.shape[1], 3), 255, np.uint8), row2])
detect.save_jpg(grid, f"{SLUG}-one-frame-per-second.jpg", width=1200)
