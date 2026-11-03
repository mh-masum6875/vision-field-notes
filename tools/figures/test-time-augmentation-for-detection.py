"""Figures for test-time-augmentation-for-detection.

Arithmetic: relative convolution compute (proportional to input pixels) of a single pass and of TTA variants.
The Ultralytics variant uses the scales and flips found in its source at the time of writing: 1.0, 0.83 (flipped)
and 0.67.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "test-time-augmentation-for-detection"
variants = [
    ("single pass", [1.0]),
    ("+ horizontal flip", [1.0, 1.0]),
    ("Ultralytics augment=True\n(1.0, 0.83 flipped, 0.67)", [1.0, 0.83, 0.67]),
    ("scales 1.0, 1.25, 1.5", [1.0, 1.25, 1.5]),
    ("scales 1.0, 1.5, with flips", [1.0, 1.0, 1.5, 1.5]),
]
vals = [sum(s ** 2 for s in sc) for _, sc in variants]
fig, ax = plt.subplots(figsize=(10, 4.6))
y = np.arange(len(variants))
ax.barh(y, vals, color=[C[2]] + [C[0]] * 2 + [C[1]] * 2, alpha=0.85, height=0.6)
for i, v in enumerate(vals):
    ax.text(v + 0.05, i, f"{v:.2f}x", va="center", fontsize=11)
ax.set_yticks(y); ax.set_yticklabels([v[0] for v in variants]); ax.invert_yaxis()
ax.set_xlabel("relative inference compute (sum of scale squared over passes)")
ax.set_xlim(0, 7.2)
ax.grid(axis="y", visible=False)
ax.set_title("What test-time augmentation costs per frame (arithmetic, excluding merge and NMS)", loc="left")
save(fig, f"{SLUG}-cost.png")
