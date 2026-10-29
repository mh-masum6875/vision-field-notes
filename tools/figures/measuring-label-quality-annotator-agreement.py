"""Figures for measuring-label-quality-annotator-agreement.

Pure geometry: IoU between two square boxes when the second annotator places every edge d pixels
outward (a slightly looser box). No annotation data.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "measuring-label-quality-annotator-agreement"
d = np.linspace(0, 6, 61)
fig, ax = plt.subplots(figsize=(10, 4.8))
for size, c in [(12, C[1]), (24, C[3]), (48, C[0]), (128, C[2])]:
    iou = size ** 2 / (size + 2 * d) ** 2
    ax.plot(d, iou, color=c, label=f"{size} px object")
    v = size ** 2 / (size + 4) ** 2
    ax.plot([2], [v], "o", color=c, ms=6)
    ax.text(2.12, v - 0.035, f"{v:.2f}", fontsize=11, color=c)
ax.axhline(0.5, color=INK2, ls="--", lw=1.1)
ax.text(6, 0.515, "IoU 0.5", ha="right", fontsize=11, color=INK2)
ax.set_xlim(0, 6); ax.set_ylim(0, 1.03)
ax.set_xlabel("each edge placed this many pixels further out by the second annotator")
ax.set_ylabel("IoU between the two boxes")
ax.legend(loc="lower left", fontsize=11.5)
ax.set_title("The same few pixels of disagreement cost small objects far more IoU (geometry)", loc="left")
save(fig, f"{SLUG}-iou-vs-size.png")
