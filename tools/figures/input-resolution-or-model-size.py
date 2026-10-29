"""Figures for input-resolution-or-model-size. Pure arithmetic: how compute and object size scale with input size."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "input-resolution-or-model-size"
s = np.array([320, 416, 512, 640, 800, 960, 1280])
compute = (s / 640) ** 2
obj = 24 * s / 640  # an object that is 24 px tall at 640 input

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(s, compute, color=C[1], marker="o", label="convolution compute, relative to 640  (∝ size²)")
ax.plot(s, obj / 24, color=C[0], marker="o", label="object height in pixels, relative to 640  (∝ size)")
for x, y in zip(s, compute):
    if x in (320, 1280):
        ax.text(x, y + 0.2, f"{y:.2g}x", ha="center", fontsize=11.5, color=C[1])
ax.text(1280, 2 - 0.35, "2x", ha="center", fontsize=11.5, color=C[0])
ax.set_xticks(s)
ax.set_xlabel("square input size (px)")
ax.set_ylabel("relative to 640 input")
ax.set_ylim(0, 4.5)
ax.legend(loc="upper left", fontsize=11.5)
ax.set_title("Doubling input size doubles object pixels and roughly quadruples compute (arithmetic)", loc="left")
save(fig, f"{SLUG}-scaling.png")
