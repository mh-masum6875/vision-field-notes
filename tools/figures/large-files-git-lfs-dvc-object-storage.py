"""Figure for large-files-git-lfs-dvc-object-storage.

A decision tree, not data. The three options in the post, with the questions
that actually separate them, and the combination the post recommends.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "large-files-git-lfs-dvc-object-storage"

fig, ax = plt.subplots(figsize=(13.0, 7.2))
ax.set_xlim(0, 13)
ax.set_ylim(0, 7.6)
ax.axis("off")


def node(cx, cy, w, h, text, fc, ec, size=11.6, weight="normal", tc=INK):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.05,rounding_size=0.14",
                                fc=fc, ec=ec, lw=1.8, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, color=tc,
            weight=weight, linespacing=1.35, zorder=4)


def link(p0, p1, label=None, color=INK2, rad=0.0, dx=0.0, dy=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=16,
                                 color=color, lw=1.8, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}"))
    if label:
        ax.text((p0[0] + p1[0]) / 2 + dx, (p0[1] + p1[1]) / 2 + dy, label,
                ha="center", va="center", fontsize=11, color=color, weight="bold",
                zorder=5,
                bbox=dict(fc="white", ec="none", alpha=0.9, boxstyle="round,pad=0.18"))


Q = "#fff8e8"
node(6.5, 6.95, 7.4, 0.95, "What is the file?", Q, WARN, size=12.6, weight="bold")

node(2.3, 5.25, 4.0, 1.15,
     "A few files that belong\nwith the code\nweights, golden outputs", "#eef3fb", C[0])
node(10.7, 5.25, 4.4, 1.15,
     "A dataset: thousands of\nimages, versioned,\nwith splits", "#eef3fb", C[0])
link((5.0, 6.48), (2.6, 5.85), rad=0.12)
link((8.0, 6.48), (10.4, 5.85), rad=-0.12)

node(2.3, 3.35, 4.0, 1.0, "Git LFS", "#eaf6ee", GOOD, size=13.2, weight="bold")
ax.text(2.3, 2.45, "versions files with the commit\nwatch the provider's quota",
        ha="center", va="top", fontsize=10.8, color=INK2, linespacing=1.35)
link((2.3, 4.67), (2.3, 3.88))

node(10.7, 3.70, 4.4, 1.0, "Do you need pipelines\nand reproducible stages?",
     Q, WARN, size=11.6, weight="bold")
link((10.7, 4.67), (10.7, 4.23))

node(8.0, 2.05, 3.4, 1.0, "DVC", "#eaf6ee", GOOD, size=13.2, weight="bold")
ax.text(8.0, 1.30, "dataset versions, splits,\nstage graph", ha="center", va="top",
        fontsize=10.8, color=INK2, linespacing=1.35)
link((9.9, 3.20), (8.4, 2.58), label="yes", rad=0.1, dx=-0.30)

node(11.4, 2.05, 3.0, 1.0, "Object storage\n+ manifest", "#eaf6ee", GOOD,
     size=12.2, weight="bold")
ax.text(11.4, 1.30, "cheapest at scale,\nyou write the glue", ha="center", va="top",
        fontsize=10.8, color=INK2, linespacing=1.35)
link((11.5, 3.20), (11.4, 2.58), label="no", rad=-0.1, dx=0.46)

ax.text(6.5, 0.26, "Most teams end up with Git LFS for weights and one of the other two "
                   "for footage, not a single choice for everything.",
        ha="center", fontsize=11.8, color=INK, weight="bold")

fig.suptitle("These are not competitors; they answer different questions",
             x=0.008, ha="left", fontsize=15.5, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.955])
save(fig, f"{SLUG}-decision-tree.png")
print("rendered large files decision tree")
