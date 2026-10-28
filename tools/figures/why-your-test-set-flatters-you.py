"""Figures for why-your-test-set-flatters-you. Schematic only: no measurements."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "why-your-test-set-flatters-you"
rng = np.random.default_rng(5)

fig, axes = plt.subplots(2, 1, figsize=(11, 5.2))
cams = ["camera 1", "camera 2", "camera 3", "camera 4"]
weeks = 8
for ax, mode in zip(axes, ["random", "held-out"]):
    ax.set_xlim(-1.7, weeks); ax.set_ylim(-0.6, len(cams) - 0.2); ax.axis("off")
    for i, cam in enumerate(cams):
        ax.text(-0.15, i, cam, ha="right", va="center", fontsize=11.5, color=INK2)
        for wk in range(weeks):
            for d in range(7):
                x = wk + d / 7
                if mode == "random":
                    test = rng.random() < 0.2
                else:
                    test = cam == "camera 4" or wk == weeks - 1
                ax.add_patch(Rectangle((x, i - 0.32), 1 / 7 - 0.02, 0.64,
                                       fc=C[1] if test else C[0], alpha=0.9 if test else 0.35, lw=0))
    ax.text(-1.7, len(cams) - 0.35, "Random split by day" if mode == "random" else
            "Split by camera and by time", fontsize=13, weight="bold", va="bottom")
axes[1].text(weeks / 2, -0.85, "weeks of footage  →   (each cell is one day of frames)", ha="center",
             fontsize=11.5, color=INK2)
h = [Rectangle((0, 0), 1, 1, fc=C[0], alpha=0.35), Rectangle((0, 0), 1, 1, fc=C[1], alpha=0.9)]
fig.legend(h, ["train", "test"], loc="upper right", ncol=2, fontsize=11.5, bbox_to_anchor=(0.98, 1.0))
fig.suptitle("Random splits put close neighbours of training data in the test set (schematic)",
             x=0.02, ha="left", fontsize=14, weight="bold", y=1.04)
fig.tight_layout()
save(fig, f"{SLUG}-split-schematic.png")
