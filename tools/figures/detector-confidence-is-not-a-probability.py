"""Figures for detector-confidence-is-not-a-probability.

A constructed reliability diagram: the 'observed precision' curves are formulas chosen to show over- and
under-confidence, not measurements of any model.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "detector-confidence-is-not-a-probability"
s = np.linspace(0.05, 0.95, 10)
over = s ** 1.8
under = 1 - (1 - s) ** 1.8
fig, ax = plt.subplots(figsize=(7.6, 6))
ax.plot([0, 1], [0, 1], color=MUTED, ls="--", lw=1.3, label="perfectly calibrated")
ax.plot(s, over, color=C[1], marker="o", label="over-confident (scores too high)")
ax.plot(s, under, color=C[0], marker="o", label="under-confident (scores too low)")
ax.annotate("boxes scored 0.7 are right\nonly about half the time", xy=(0.65, 0.65 ** 1.8), xytext=(0.5, 0.12),
            fontsize=11, color=C[1], arrowprops=dict(arrowstyle="->", color=C[1]))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
ax.set_xlabel("confidence score (binned)")
ax.set_ylabel("share of boxes in the bin that are correct")
ax.legend(loc="upper left", fontsize=11)
ax.set_title("Reliability diagram (constructed curves)", loc="left")
save(fig, f"{SLUG}-reliability.png")
