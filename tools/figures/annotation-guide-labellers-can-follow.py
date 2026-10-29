"""Figures for annotation-guide-labellers-can-follow. A schematic of box rules, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, FancyBboxPatch
from style import C, INK, INK2, MUTED, GRID, GOOD, CRIT, save

SLUG = "annotation-guide-labellers-can-follow"


def person(ax, x, y, s=1.0, color=MUTED):
    ax.add_patch(Ellipse((x, y + 3.4 * s), 0.8 * s, 0.9 * s, fc=color, ec="none"))
    ax.add_patch(FancyBboxPatch((x - 0.6 * s, y + 1.4 * s), 1.2 * s, 1.6 * s,
                                boxstyle="round,pad=0,rounding_size=0.2", fc=color, ec="none"))
    ax.add_patch(Rectangle((x - 0.5 * s, y), 0.4 * s, 1.5 * s, fc=color, ec="none"))
    ax.add_patch(Rectangle((x + 0.1 * s, y), 0.4 * s, 1.5 * s, fc=color, ec="none"))


fig, axes = plt.subplots(1, 3, figsize=(12, 4.6))
titles = ["Tight box, whole person", "Occluded: box the visible part", "Do not: pad or crop"]
for ax, t in zip(axes, titles):
    ax.set_xlim(0, 6); ax.set_ylim(-0.6, 5.4); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(t, fontsize=12.5, loc="left")
person(axes[0], 3, 0.3)
axes[0].add_patch(Rectangle((2.4, 0.3), 1.2, 3.55, fill=False, ec=GOOD, lw=2.4))
person(axes[1], 3, 0.3)
axes[1].add_patch(Rectangle((1.2, -0.3), 3.6, 2.1, fc="#c9c3b6", ec="none"))
axes[1].text(3, 0.6, "counter", ha="center", fontsize=11, color=INK2)
axes[1].add_patch(Rectangle((2.4, 1.8), 1.2, 2.05, fill=False, ec=GOOD, lw=2.4))
person(axes[2], 2.0, 0.3, 0.9)
axes[2].add_patch(Rectangle((1.1, -0.1), 1.8, 4.1, fill=False, ec=CRIT, lw=2.2, ls="--"))
person(axes[2], 4.4, 0.3, 0.9)
axes[2].add_patch(Rectangle((3.9, 1.0), 1.0, 2.3, fill=False, ec=CRIT, lw=2.2, ls="--"))
axes[2].text(2.0, -0.55, "loose", ha="center", fontsize=11, color=CRIT)
axes[2].text(4.4, -0.55, "cuts off head, feet", ha="center", fontsize=11, color=CRIT)
fig.suptitle("Write the box rule down, with a picture for each case (schematic)", x=0.01, ha="left",
             fontsize=14, weight="bold", y=1.02)
fig.tight_layout()
save(fig, f"{SLUG}-box-rules.png")
