"""Figures for anchor-free-vs-anchor-based-detectors: how each predicts a box, and anchor fit to label shapes."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID

SLUG = "anchor-free-vs-anchor-based-detectors"


def grid(ax, n=6, size=60):
    s = size / n
    for i in range(n + 1):
        ax.plot([i * s, i * s], [0, size], color=GRID, lw=1, zorder=0)
        ax.plot([0, size], [i * s, i * s], color=GRID, lw=1, zorder=0)
    ax.set_xlim(-1, size + 1); ax.set_ylim(size + 1, -1); ax.set_aspect("equal"); ax.axis("off")


def person(ax, b):
    ax.add_patch(FancyBboxPatch((b[0] + 1, b[1] + 1), b[2] - b[0] - 2, b[3] - b[1] - 2,
                                boxstyle="round,pad=0,rounding_size=2.5", fc="#dcdad3", ec="none", zorder=1))


def fig_compare():
    obj = (21, 12, 37, 52)  # true object box
    cx, cy = 25, 35         # grid cell centre used for prediction (cell size 10)
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.6))
    # anchor-based
    ax = axes[0]
    grid(ax)
    person(ax, obj)
    ax.add_patch(Rectangle((20, 30), 10, 10, fc=C[0] + "22", ec=C[0], lw=1.5, zorder=2))
    anchors = [(14, 34, MUTED, "wide anchor"), (12, 12, MUTED, "square anchor"), (14, 36, C[1], "tall anchor")]
    shapes = [(28, 14), (16, 16), (14, 36)]
    for (w, h), col in zip(shapes, [MUTED, MUTED, C[1]]):
        ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fill=False, ec=col, lw=2, ls=(0, (4, 3)), zorder=3))
    ax.add_patch(Rectangle((obj[0], obj[1]), obj[2] - obj[0], obj[3] - obj[1], fill=False, ec=ACCENT, lw=2.6, zorder=4))
    ax.annotate("best-matching anchor\nis shifted and stretched", xy=(cx + 7, cy - 18), xytext=(40, 6),
                fontsize=11.5, color=INK, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2))
    ax.text(30, 63, "Several preset shapes per cell;\nthe model adjusts one of them", ha="center", va="top", fontsize=12, color=INK2)
    ax.set_title("Anchor-based (e.g. YOLOv5)", fontsize=14)
    # anchor-free
    ax = axes[1]
    grid(ax)
    person(ax, obj)
    ax.add_patch(Rectangle((20, 30), 10, 10, fc=C[0] + "22", ec=C[0], lw=1.5, zorder=2))
    ax.add_patch(Rectangle((obj[0], obj[1]), obj[2] - obj[0], obj[3] - obj[1], fill=False, ec=ACCENT, lw=2.6, zorder=4))
    ax.plot([cx], [cy], "o", color=C[1], ms=8, zorder=6)
    for (x2, y2), lab, (tx, ty) in [((obj[0], cy), "left", (13, cy - 3)), ((obj[2], cy), "right", (38, cy - 3)),
                                    ((cx, obj[1]), "top", (cx + 1, 20)), ((cx, obj[3]), "bottom", (cx + 1, 47))]:
        ax.annotate("", xy=(x2, y2), xytext=(cx, cy), arrowprops=dict(arrowstyle="-|>", color=C[1], lw=2, mutation_scale=14), zorder=5)
        ax.text(tx, ty, lab, fontsize=11.5, color=INK, ha="left", va="center", zorder=7,
                bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.85))
    ax.text(30, 63, "No preset shapes; a location predicts\ndistances to the four sides", ha="center", va="top", fontsize=12, color=INK2)
    ax.set_title("Anchor-free (e.g. YOLOv8, YOLO11)", fontsize=14)
    for a in axes:
        a.set_ylim(70, -1)
    h = [plt.Line2D([], [], color=ACCENT, lw=2.6, label="predicted box"),
         plt.Line2D([], [], color=MUTED, lw=2, ls=(0, (4, 3)), label="anchors (preset shapes)"),
         Rectangle((0, 0), 1, 1, fc=C[0] + "22", ec=C[0], label="grid cell making the prediction")]
    fig.legend(handles=h, loc="lower center", ncol=3, fontsize=11.5, bbox_to_anchor=(0.5, -0.03))
    fig.tight_layout(rect=(0, 0.05, 1, 1), w_pad=3)
    style.save(fig, f"{SLUG}-how-boxes-are-predicted.png")


def fig_shapes():
    rng = np.random.default_rng(3)
    # illustrative label shapes (pixels at model input), not a real dataset
    groups = [
        ("people (tall)", 40, 100, 0.25, C[0]),
        ("vehicles (wide)", 120, 70, 0.25, C[1]),
        ("signs (square)", 45, 45, 0.25, C[2]),
        ("poles (very thin)", 9, 160, 0.2, C[4]),
    ]
    anchors = np.array([[10, 13], [16, 30], [33, 23], [30, 61], [62, 45], [59, 119], [116, 90], [156, 198], [373, 326]])
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    for name, w, h, sd, c in groups:
        ws = np.exp(rng.normal(np.log(w), sd, 70))
        hs = np.exp(rng.normal(np.log(h), sd, 70))
        ax.scatter(ws, hs, s=16, color=c, alpha=0.6, label=name, lw=0)
    ax.scatter(anchors[:, 0], anchors[:, 1], marker="X", s=120, color=INK, label="anchor shapes", zorder=5)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(4, 500); ax.set_ylim(8, 500)
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
    for axis, t in [(ax.xaxis, [5, 10, 20, 50, 100, 200, 400]), (ax.yaxis, [10, 20, 50, 100, 200, 400])]:
        axis.set_major_locator(FixedLocator(t)); axis.set_major_formatter(FixedFormatter([str(v) for v in t]))
        axis.set_minor_locator(NullLocator())
    ax.set_xlabel("Box width (pixels, log scale)")
    ax.set_ylabel("Box height (pixels, log scale)")
    ax.annotate("no anchor is close to\nthese thin shapes", xy=(9, 150), xytext=(14, 330), fontsize=11.5, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2))
    ax.set_title("Anchors only help shapes they resemble (illustrative)", loc="left")
    ax.legend(loc="lower right", fontsize=11.5, markerscale=1.4)
    style.save(fig, f"{SLUG}-anchor-fit.png")


if __name__ == "__main__":
    fig_compare()
    fig_shapes()
