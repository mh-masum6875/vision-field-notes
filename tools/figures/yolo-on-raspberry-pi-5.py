"""Figures for yolo-on-raspberry-pi-5 (pure diagrams, no speed numbers)."""
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT, CRIT
from matplotlib.patches import FancyBboxPatch, Rectangle

SLUG = "yolo-on-raspberry-pi-5"
B_FC, O_FC = "#eef3fb", "#e8f3ef"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, fs=12, bold=False, color=INK, lw=1.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, color=INK2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16))


def bracket(ax, x1, x2, y, text, color):
    ax.plot([x1, x1, x2, x2], [y + 0.18, y, y, y + 0.18], color=color, lw=2)
    ax.text((x1 + x2) / 2, y - 0.12, text, ha="center", va="top", fontsize=12, color=INK)


# ---- Figure 1: capture and inference in separate threads, and what to time ----
def pipeline():
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off")
    y, h = 2.2, 1.3
    items = [(0.05, 1.45, "Camera\nUSB / CSI /\nRTSP", "#ffffff", INK2),
             (1.85, 1.7, "Capture\nthread\nreads every\nframe", B_FC, C[0]),
             (3.95, 1.5, "Latest\nframe only\n(old ones\ndropped)", B_FC, C[0]),
             (5.85, 1.75, "Inference\nthread\nevery Nth\nframe", O_FC, ACCENT),
             (8.0, 1.95, "Post-process\nNMS, tracking,\nalerts", O_FC, ACCENT)]
    for x, w, t, fc, ec in items:
        box(ax, x, y, w, h, t, fc=fc, ec=ec)
    for (x, w, *_), (nx, *_) in zip(items[:-1], items[1:]):
        arrow(ax, x + w, y + h / 2, nx, y + h / 2)
    ax.text(5.6, 3.75, "separate threads keep latency low: the model always gets a recent frame",
            ha="center", va="center", fontsize=12, color=INK2)
    bracket(ax, 5.85, 7.6, 1.85, "model call alone", C[1])
    bracket(ax, 1.85, 9.95, 0.95, "full loop: capture, resize, model, post-process\n(what your users experience)", C[0])
    ax.text(5.0, 4.4, "Run capture and inference apart, and time the whole loop",
            ha="center", va="center", fontsize=14, fontweight="bold")
    style.save(fig, f"{SLUG}-pipeline.png")


# ---- Figure 2: frame skipping timeline ----
def frame_skipping():
    n, N = 24, 3
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.set_xlim(-6.2, n + 0.5); ax.set_ylim(-0.5, 3.1); ax.axis("off")
    for i in range(n):
        ax.add_patch(Rectangle((i, 2.0), 0.8, 0.8, fc=C[0], ec="none"))
        if i % N == 0:
            ax.add_patch(Rectangle((i, 0.6), 0.8, 0.8, fc=ACCENT, ec="none"))
            ax.annotate("", xy=(i + 0.4, 1.42), xytext=(i + 0.4, 1.98),
                        arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2, mutation_scale=10))
        else:
            ax.add_patch(Rectangle((i, 0.6), 0.8, 0.8, fc="none", ec=GRID, lw=1.2))
    ax.text(-0.4, 2.4, "Frames read\nfrom the camera", ha="right", va="center", fontsize=12, color=INK)
    ax.text(-0.4, 1.0, "Frames sent to\nthe model (N = 3)", ha="right", va="center", fontsize=12, color=INK)
    ax.annotate("", xy=(n, 0.15), xytext=(0, 0.15), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
    ax.text(n / 2, -0.05, "time", ha="center", va="top", fontsize=12, color=INK2)
    ax.set_title("Read every frame to keep the buffer fresh; run the model on every Nth", fontsize=14)
    style.save(fig, f"{SLUG}-frame-skipping.png")


if __name__ == "__main__":
    pipeline()
    frame_skipping()
