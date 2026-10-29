"""Figures for building-a-replay-set. A schematic coverage grid; the ticks are an example plan, not data."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from style import C, INK, INK2, MUTED, GRID, GOOD, CRIT, WARN, save

SLUG = "building-a-replay-set"
rows = ["day, normal traffic", "day, busy", "night (IR)", "dawn / dusk switch", "rain or glare",
        "known false-alarm source", "rare real event", "camera fault (frozen, blurred)"]
cols = ["cam 1\nentrance", "cam 2\ncorridor", "cam 3\nloading bay", "cam 4\nyard"]
plan = np.array([[2, 2, 2, 2], [2, 1, 2, 0], [2, 2, 2, 2], [1, 0, 2, 2],
                 [0, 0, 1, 2], [2, 0, 2, 1], [1, 0, 2, 0], [1, 1, 0, 0]])
colors = {2: GOOD, 1: WARN, 0: CRIT}
labels = {2: "covered", 1: "one short clip", 0: "missing"}
fig, ax = plt.subplots(figsize=(10.5, 5.6))
ax.set_xlim(-3.6, len(cols)); ax.set_ylim(len(rows), -1.1); ax.axis("off")
for i, rlab in enumerate(rows):
    ax.text(-0.15, i + 0.5, rlab, ha="right", va="center", fontsize=11.5, color=INK2)
    for j in range(len(cols)):
        v = plan[i, j]
        ax.add_patch(Rectangle((j + 0.05, i + 0.08), 0.9, 0.84, fc=colors[v], alpha=0.28 if v else 0.18,
                               ec=colors[v], lw=1.2))
        ax.text(j + 0.5, i + 0.5, labels[v], ha="center", va="center", fontsize=9.5, color=INK)
for j, c in enumerate(cols):
    ax.text(j + 0.5, -0.1, c, ha="center", va="bottom", fontsize=11, color=INK)
ax.text(-3.6, -1.0, "Plan the replay set as a grid, then fill the gaps (example plan)", fontsize=14,
        weight="bold", va="center")
save(fig, f"{SLUG}-coverage-grid.png")
