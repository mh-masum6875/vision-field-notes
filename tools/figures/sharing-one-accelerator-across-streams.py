"""Figures for sharing-one-accelerator-across-streams.

Arithmetic with an example capacity: an accelerator that sustains 200 inferences per second for the chosen model
(an example number, not a benchmark of any device), loaded to 70%.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "sharing-one-accelerator-across-streams"
CAP, LOAD = 200, 0.7
fps = np.array([1, 2, 3, 5, 8, 10, 15, 25])
cams = np.floor(CAP * LOAD / fps)
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.bar([f"{f:g}" for f in fps], cams, color=C[0], alpha=0.85, width=0.6)
for i, c in enumerate(cams):
    ax.text(i, c + 2, f"{c:.0f}", ha="center", fontsize=11)
ax.set_xlabel("analysis frames per second per camera")
ax.set_ylabel("cameras on one accelerator")
ax.grid(axis="x", visible=False)
ax.set_title(f"Example: {CAP} inferences/s capacity, planned at {LOAD:.0%} load (arithmetic)", loc="left")
save(fig, f"{SLUG}-cameras-vs-fps.png")
