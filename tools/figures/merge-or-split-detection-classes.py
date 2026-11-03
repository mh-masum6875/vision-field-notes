"""Figures for merge-or-split-detection-classes. A diagram, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, GOOD, save

SLUG = "merge-or-split-detection-classes"


def box(ax, x, y, w, h, color, text, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.1",
                                fc=color + "22", ec=color, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=11.5,
            weight="bold" if bold else "normal", linespacing=1.3)


fig, ax = plt.subplots(figsize=(11.5, 5))
ax.set_xlim(0, 11.5); ax.set_ylim(0, 5.2); ax.axis("off")
ax.text(0.1, 5.0, "Detect broad classes; split them in a second step only where the decision needs it",
        fontsize=13.5, weight="bold", va="center")
box(ax, 0.3, 2.0, 2.4, 1.0, C[0], "detector:\nvehicle", True)
box(ax, 0.3, 0.4, 2.4, 1.0, C[0], "detector:\nperson", True)
for i, (t, c) in enumerate([("car", C[2]), ("van", C[2]), ("truck", C[2])]):
    box(ax, 4.2, 3.3 - i * 0.9, 1.8, 0.7, c, t)
    ax.annotate("", xy=(4.2, 3.65 - i * 0.9), xytext=(2.7, 2.5), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2))
box(ax, 4.2, 0.55, 1.8, 0.7, C[6], "helmet: yes / no")
ax.annotate("", xy=(4.2, 0.9), xytext=(2.7, 0.9), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2))
ax.text(3.45, 2.95, "classifier on crops,\nor attribute head", ha="center", fontsize=10, color=INK2)
notes = ["Merge when classes look alike, are rare,", "or lead to the same action.",
         "", "Split when the action differs and the", "difference is visible at your resolution.",
         "", "A second stage can be trained, tested", "and changed without touching the detector."]
for i, n in enumerate(notes):
    ax.text(6.8, 3.6 - i * 0.38, n, fontsize=11, color=INK)
save(fig, f"{SLUG}-two-stage.png")
