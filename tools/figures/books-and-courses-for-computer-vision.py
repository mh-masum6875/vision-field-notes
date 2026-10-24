"""Figures for books-and-courses-for-computer-vision.md"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, save

SLUG = "books-and-courses-for-computer-vision"


def box(ax, x, y, w, h, color, fill=0.12, lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw))


# 1. Levels as a staircase: where you are, what to look for next
levels = [
    ("Beginner", "write basic Python", "NumPy, image basics, OpenCV,\nsimple machine learning"),
    ("Early", "train a classifier\nfrom a tutorial", "why it works; a detector\non your own data"),
    ("Intermediate", "train and evaluate\ndetectors", "deployment, video, edge\nhardware, debugging data"),
    ("Advanced", "ship a system", "specialised topics, papers,\nscaling, monitoring"),
]
fig, ax = plt.subplots(figsize=(10, 5.4))
ax.set_xlim(0, 12.4); ax.set_ylim(0, 6.9); ax.axis("off")
ax.text(0.05, 6.85, "Pick resources for the step you are on, not the one you want to be on",
        fontsize=14, weight="bold", va="top")
rw, rh, shift = 10.4, 1.15, 0.6
for i, (name, can, need) in enumerate(levels):
    x = 0.1 + i * shift
    y = 0.15 + i * (rh + 0.2)
    col = [C[0], C[6], C[1], C[2]][i]
    box(ax, x, y, rw, rh, col)
    ax.text(x + 0.25, y + rh / 2, name, fontsize=13, weight="bold", va="center")
    ax.text(x + 2.6, y + rh / 2, can, fontsize=12, va="center", linespacing=1.2)
    ax.text(x + 6.0, y + rh / 2, need, fontsize=12, va="center", linespacing=1.2)
hy = 0.15 + 4 * (rh + 0.2) + 0.05
hx = 0.1 + 3 * shift
ax.text(hx + 2.6, hy, "You can already", fontsize=12, color=INK2, style="italic", va="bottom")
ax.text(hx + 6.0, hy, "Look for resources on", fontsize=12, color=INK2, style="italic", va="bottom")
save(fig, f"{SLUG}-levels.png")

# 2. The weekly study loop
fig, ax = plt.subplots(figsize=(10, 6.2))
ax.set_xlim(-6.2, 6.2); ax.set_ylim(-3.9, 3.9); ax.set_aspect("equal"); ax.axis("off")
ax.text(-6.1, 3.85, "Alternate learning with building, every week", fontsize=14, weight="bold", va="top")
steps = [("1  Learn", "one small topic from\na chapter or lesson", 90),
         ("2  Apply", "code it that week\non your own data", 0),
         ("3  Write", "a short note in your\nown words", -90),
         ("4  Revisit", "a week later, test\nwithout looking", 180)]
R = 2.35
for i, (title, sub, ang) in enumerate(steps):
    a = np.deg2rad(ang)
    cx, cy = R * 1.45 * np.cos(a), R * 0.95 * np.sin(a) - 0.2
    bw, bh = 3.6, 1.35
    col = [C[0], C[1], C[6], C[2]][i]
    box(ax, cx - bw / 2, cy - bh / 2, bw, bh, col)
    ax.text(cx, cy + 0.32, title, ha="center", va="center", fontsize=13, weight="bold")
    ax.text(cx, cy - 0.25, sub, ha="center", va="center", fontsize=12, color=INK2, linespacing=1.2)
# curved arrows between boxes (clockwise)
pairs = [((1.75, 2.05), (3.4, 0.75)), ((3.4, -1.15), (1.75, -2.45)),
         ((-1.75, -2.45), (-3.4, -1.15)), ((-3.4, 0.75), (-1.75, 2.05))]
for p1, p2 in pairs:
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.8, mutation_scale=16,
                                                      connectionstyle="arc3,rad=-0.3"))
ax.text(0, -0.05, "Every few topics:\na small project that\ncombines them\n↓\na portfolio item", ha="center",
        va="center", fontsize=12, color=INK, linespacing=1.3)
save(fig, f"{SLUG}-study-loop.png")
