"""Figures for cvat-vs-label-studio-vs-roboflow (pure diagrams)."""
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT, SURFACE
from matplotlib.patches import FancyBboxPatch

SLUG = "cvat-vs-label-studio-vs-roboflow"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, fs=12, bold=False, color=INK, lw=1.5, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=fc, ec=ec, lw=lw, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, label=None, lx=0, ly=0, color=INK2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=12, color=INK2,
                ha="center", va="center", fontweight="bold")


def canvas(w, h, figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, w); ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


Q_FC = "#eef3fb"
O_FC = "#e8f3ef"


def decision_flow():
    fig, ax = canvas(10, 9.4, (10, 9.2))
    qx, qw, qh = 0.2, 4.6, 1.15
    ox, ow = 6.3, 3.5
    qs = [
        (8.0, "1. Can the images leave\nyour network?", "No", "Self-host CVAT or\nLabel Studio"),
        (6.0, "2. Is the data mostly video?", "Yes", "Pilot CVAT first\n(keyframe interpolation)"),
        (4.0, "3. Do you need more than\nboxes on images?", "Yes", "Look at Label Studio\n(custom interfaces)"),
        (2.0, "4. Is there no one to\nrun servers?", "Yes", "A hosted tool such as\nRoboflow saves that work"),
    ]
    for y, q, side, out in qs:
        box(ax, qx, y, qw, qh, q, fc=Q_FC, ec=C[0])
        box(ax, ox, y, ow, qh, out, fc=O_FC, ec=ACCENT)
        arrow(ax, qx + qw, y + qh / 2, ox, y + qh / 2, side, ly=0.25)
    for (y1, *_), (y2, *_) in zip(qs[:-1], qs[1:]):
        lab = "Yes" if y1 == 8.0 else "No"
        arrow(ax, qx + qw / 2, y1, qx + qw / 2, y2 + qh, lab, lx=0.4)
    # final
    box(ax, qx, 0.0, qw, qh, "Any of the three can work:\npilot two on 100 images", fc="#ffffff", ec=ACCENT)
    arrow(ax, qx + qw / 2, 2.0, qx + qw / 2, qh, "No", lx=0.4)
    ax.text(5.0, 9.35, "Ask the questions in order; the first decisive answer narrows the field",
            ha="center", va="center", fontsize=14, fontweight="bold")
    style.save(fig, f"{SLUG}-decision-flow.png")


def data_location():
    fig, ax = canvas(10, 5.9, (10, 5.6))
    # private network boundary
    ax.add_patch(FancyBboxPatch((0.2, 0.3), 6.2, 4.6, boxstyle="round,pad=0,rounding_size=0.2",
                                fc="#f6f6f3", ec=INK2, lw=1.6, ls="--"))
    ax.text(6.2, 0.55, "Your network", fontsize=13, fontweight="bold", color=INK2, va="center", ha="right")
    box(ax, 0.5, 2.6, 2.3, 1.3, "Cameras and\nimage storage", fc="#ffffff")
    box(ax, 3.7, 3.15, 2.4, 1.0, "CVAT\n(self-hosted)", fc=O_FC, ec=ACCENT)
    box(ax, 3.7, 1.85, 2.4, 1.0, "Label Studio\n(self-hosted)", fc=O_FC, ec=ACCENT)
    box(ax, 0.5, 0.65, 2.3, 1.2, "Training\nmachine", fc="#ffffff")
    arrow(ax, 2.8, 3.4, 3.7, 3.6)
    arrow(ax, 2.8, 3.1, 3.7, 2.4)
    arrow(ax, 3.7, 1.95, 2.8, 1.35)
    ax.text(3.35, 1.25, "labels", fontsize=12, color=INK2, ha="left", va="center", fontweight="bold")
    # hosted
    box(ax, 7.3, 2.4, 2.5, 1.5, "Roboflow\n(hosted service)", fc="#fdf0ea", ec=C[1])
    ax.plot([1.65, 1.65, 8.55], [3.9, 4.45, 4.45], color=C[1], lw=1.8, solid_capstyle="round")
    ax.annotate("", xy=(8.55, 3.9), xytext=(8.55, 4.47),
                arrowprops=dict(arrowstyle="-|>", color=C[1], lw=1.8, mutation_scale=16))
    ax.text(8.55, 5.0, "images are uploaded\nto a third party", fontsize=12, color=INK, ha="center", va="center")
    ax.text(8.55, 1.95, "Check plan terms:\nfree plans may make\ndatasets public", fontsize=12, color=INK2,
            ha="center", va="top")
    ax.text(5.0, 5.7, "Self-hosting keeps footage inside; a hosted tool means uploading it",
            ha="center", va="center", fontsize=14, fontweight="bold")
    style.save(fig, f"{SLUG}-data-location.png")


if __name__ == "__main__":
    decision_flow()
    data_location()
