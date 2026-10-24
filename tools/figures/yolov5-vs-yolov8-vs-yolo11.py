"""Figures for yolov5-vs-yolov8-vs-yolo11: what changes between generations, and a decision flow."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID

SLUG = "yolov5-vs-yolov8-vs-yolo11"


def rbox(ax, x, y, w, h, color, fill=True, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=(color + "1f") if fill else "white", ec=color, lw=lw))


def arrow(ax, p1, p2, color=INK2, text=None, tx=None, ty=None, ha="center"):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16))
    if text:
        ax.text(tx, ty, text, ha=ha, va="center", fontsize=11, color=INK2)


def fig_generations():
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.axis("off")
    cards = [
        ("YOLOv5", "released 2020", ["Anchor-based head", "Repo scripts", "train.py, detect.py", "Many older", "tutorials online"], C[0]),
        ("YOLOv8", "released 2023", ["Anchor-free head", "ultralytics package", "One YOLO class for", "train, val, predict", "and export"], C[1]),
        ("YOLO11", "released 2024", ["Anchor-free head", "Same package", "Same API", "as YOLOv8", ""], C[2]),
    ]
    xs = [0, 39, 78]
    for x, (name, sub, lines, c) in zip(xs, cards):
        rbox(ax, x, 0, 22, 40, c)
        ax.text(x + 11, 35.5, name, ha="center", va="center", fontsize=16, weight="bold", color=INK)
        ax.text(x + 11, 31.5, sub, ha="center", va="center", fontsize=11, color=INK2)
        for i, l in enumerate(lines):
            ax.text(x + 11, 25 - i * 4.6, l, ha="center", va="center", fontsize=11.5, color=INK)
    # transitions
    arrow(ax, (23, 26), (38, 26))
    ax.text(30.5, 21, "Big switch", ha="center", va="center", fontsize=12, weight="bold", color=INK)
    ax.text(30.5, 13.5, "new API\nnew output\nlayout\nretrain", ha="center", va="center", fontsize=11, color=INK2, linespacing=1.3)
    arrow(ax, (62, 26), (77, 26))
    ax.text(69.5, 21, "Small switch", ha="center", va="center", fontsize=12, weight="bold", color=INK)
    ax.text(69.5, 13.5, "same code,\nnew weights\nfile name,\nretrain", ha="center", va="center", fontsize=11, color=INK2, linespacing=1.3)
    ax.text(50, 46, "Moving v5 to v8 changes your code; v8 to 11 mostly changes a file name",
            ha="center", va="center", fontsize=14, weight="bold", color=INK)
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(-0.5, 49)
    style.save(fig, f"{SLUG}-generations.png")


def fig_decide():
    fig, ax = plt.subplots(figsize=(10, 6.6))
    ax.axis("off")
    qx, qw, h = 0, 44, 8.5
    ax_, aw = 58, 42
    rows = [  # question, yes action, y
        ("Working YOLOv5 pipeline\nin production?", "Keep it. Plan a migration\nfor the next retrain.", 54),
        ("New project?", "Newest Ultralytics generation\nyou trust, small size.", 41),
        ("Need pose, oriented boxes\nor segmentation?", "Use the ultralytics package,\none API for all of these.", 28),
        ("Unusual target hardware?", "Test export and runtime on\nthat device before training.", 15),
        ("Two versions score\nabout the same?", "Pick better docs and fewer\ndeployment problems.", 2),
    ]
    for i, (q, a, y) in enumerate(rows):
        rbox(ax, qx, y, qw, h, C[0])
        ax.text(qx + qw / 2, y + h / 2, q, ha="center", va="center", fontsize=12.5, color=INK, linespacing=1.25)
        rbox(ax, ax_, y, aw, h, ACCENT)
        ax.text(ax_ + aw / 2, y + h / 2, a, ha="center", va="center", fontsize=12.5, color=INK, linespacing=1.25)
        arrow(ax, (qx + qw + 0.4, y + h / 2), (ax_ - 0.4, y + h / 2))
        ax.text((qx + qw + ax_) / 2, y + h / 2 + 1.6, "yes", ha="center", va="bottom", fontsize=11.5, weight="bold", color=ACCENT)
        if i < len(rows) - 1:
            ny = rows[i + 1][2] + h
            arrow(ax, (qx + qw / 2, y - 0.3), (qx + qw / 2, ny + 0.3))
            ax.text(qx + qw / 2 + 1.2, (y + ny) / 2, "no" if i == 0 else "then", ha="left", va="center", fontsize=11.5, color=INK2)
    ax.text(50, 67, "Questions to ask, in order", ha="center", fontsize=14, weight="bold", color=INK)
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(1, 70)
    style.save(fig, f"{SLUG}-decision-flow.png")


if __name__ == "__main__":
    fig_generations()
    fig_decide()
