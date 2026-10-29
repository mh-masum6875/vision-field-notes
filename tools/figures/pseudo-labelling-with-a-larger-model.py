"""Figures for pseudo-labelling-with-a-larger-model. A diagram of confidence bands; thresholds are examples."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from style import C, INK, INK2, MUTED, GOOD, WARN, CRIT, save

SLUG = "pseudo-labelling-with-a-larger-model"
fig, ax = plt.subplots(figsize=(11, 3.8))
ax.set_xlim(0, 1); ax.set_ylim(-1.4, 1.6); ax.axis("off")
bands = [(0.0, 0.3, CRIT, "discard", "mostly noise;\nbut review a sample\nfor missed objects"),
         (0.3, 0.75, WARN, "human review", "accept, fix or delete\neach box; this is\nwhere time goes"),
         (0.75, 1.0, GOOD, "accept, spot-check", "check a random\nsample per class\nand per camera")]
for a, b, c, t, s in bands:
    ax.add_patch(Rectangle((a, 0), b - a, 0.7, fc=c, alpha=0.3, ec=c, lw=1.4))
    ax.text((a + b) / 2, 0.35, t, ha="center", va="center", fontsize=12.5, weight="bold")
    ax.text((a + b) / 2, -0.15, s, ha="center", va="top", fontsize=10.8, color=INK2, linespacing=1.3)
for v in (0, 0.3, 0.75, 1.0):
    ax.text(v, 0.85, f"{v:g}", ha="center", fontsize=11, color=INK2)
ax.text(0.5, 1.25, "teacher model's confidence for each proposed box (example thresholds, set per class)",
        ha="center", fontsize=12, color=INK)
save(fig, f"{SLUG}-bands.png")
