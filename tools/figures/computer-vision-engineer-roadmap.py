"""Figures for computer-vision-engineer-roadmap.md"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from style import C, ACCENT, INK, INK2, MUTED, GRID, save

SLUG = "computer-vision-engineer-roadmap"


def box(ax, x, y, w, h, color, fill=0.12, lw=1.6, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw, ls=ls))


def arrow(ax, p1, p2, color=INK2, rad=0.0):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.7, mutation_scale=15,
                                                      connectionstyle=f"arc3,rad={rad}"))


# 1. Eight stages, each ending in something built
stages = [
    ("Python + data basics", "resize a folder of images"),
    ("Classic OpenCV", "label frames, write a video"),
    ("Core machine learning ideas", "classifier + train/val curves"),
    ("A deep learning framework", "fine-tune a pretrained model"),
    ("Object detection, end to end", "detector on your own data"),
    ("Deployment + edge hardware", "time it on a small device"),
    ("Video analytics", "people counter or zone alert"),
    ("Engineering habits", "tests, logging, licences"),
]
fig, ax = plt.subplots(figsize=(10, 6.4))
ax.set_xlim(0, 12.4); ax.set_ylim(0, 7.9); ax.axis("off")
ax.text(0.05, 7.85, "Eight stages, each finished with something you built", fontsize=14, weight="bold", va="top")
w, h = 5.8, 1.3
xs = [0.1, 6.5]
ys = [5.75, 3.95, 2.15, 0.35]
pos = [(xs[0], y) for y in ys] + [(xs[1], y) for y in ys]
cols = [C[0]] * 2 + [C[6]] * 2 + [C[1]] * 2 + [C[2]] * 2
for i, ((title, build), (x, y), col) in enumerate(zip(stages, pos, cols)):
    box(ax, x, y, w, h, col)
    ax.add_patch(Circle((x + 0.4, y + h / 2), 0.26, fc=col, ec="none"))
    ax.text(x + 0.4, y + h / 2, str(i + 1), ha="center", va="center", color="white", fontsize=12.5, weight="bold")
    ax.text(x + 0.85, y + h - 0.36, title, va="center", fontsize=12.5, weight="bold")
    ax.text(x + 0.85, y + 0.38, "Build: " + build.replace("\n", " "), va="center", fontsize=12, color=INK2)
for i in range(3):
    for x in xs:
        arrow(ax, (x + 0.4, ys[i] - 0.03), (x + 0.4, ys[i + 1] + h + 0.03))
mx = (xs[0] + w + xs[1]) / 2
ax.plot([xs[0] + w + 0.03, mx, mx], [ys[3] + h / 2, ys[3] + h / 2, ys[0] + h / 2], color=INK2, lw=1.7)
arrow(ax, (mx, ys[0] + h / 2), (xs[1] - 0.03, ys[0] + h / 2))
save(fig, f"{SLUG}-stages.png")

# 2. Where each stage shows up in a production video system
fig, ax = plt.subplots(figsize=(10, 4.3))
ax.set_xlim(0, 12.4); ax.set_ylim(0, 4.7); ax.axis("off")
ax.text(0.05, 4.65, "The stages map onto the parts of a real camera system", fontsize=14, weight="bold", va="top")
parts = [("Camera\nstream", "7"), ("Decode,\nresize", "2"), ("Detector\nmodel", "4, 5, 6"),
         ("Tracking", "7"), ("Events:\ncounts,\nzones", "7"), ("Alerts +\nmonitoring", "7, 8")]
w, gap, x = 1.78, 0.3, 0.1
centers = []
for i, (t, st) in enumerate(parts):
    col = C[1] if "5" in st else C[0]
    box(ax, x, 2.3, w, 1.6, col)
    ax.text(x + w / 2, 3.1, t, ha="center", va="center", fontsize=12, linespacing=1.3)
    ax.text(x + w / 2, 1.95, f"stage {st}", ha="center", va="center", fontsize=12, color=INK2)
    if i < len(parts) - 1:
        arrow(ax, (x + w + 0.02, 3.1), (x + w + gap - 0.02, 3.1))
    centers.append(x + w / 2)
    x += w + gap
# data loop feeding the model
box(ax, centers[2] - 3.0, 0.15, 6.0, 1.15, C[6], fill=0.08)
ax.text(centers[2], 0.72, "Data loop (stages 3-5):\ncollect, label, split, train, evaluate",
        ha="center", va="center", fontsize=12)
arrow(ax, (centers[2], 1.32), (centers[2], 1.75))
save(fig, f"{SLUG}-pipeline.png")
