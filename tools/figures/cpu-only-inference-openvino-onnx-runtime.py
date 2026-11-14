"""Figure for cpu-only-inference-openvino-onnx-runtime.

Arithmetic, not a benchmark. Convolution work scales with the pixel count, so
halving each side quarters the work. Real throughput depends on the CPU, the
runtime and the memory system, which is why the post says to measure.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "cpu-only-inference-openvino-onnx-runtime"

SIZES = np.array([320, 416, 480, 544, 640, 768, 960, 1280])
REF = 640
rel = (SIZES / REF) ** 2

fig, axs = plt.subplots(1, 2, figsize=(12.6, 5.4),
                        gridspec_kw={"width_ratios": [1.25, 1.0]})

# ---- relative work against input size
ax = axs[0]
cols = [GOOD if r < 1 else (INK2 if r == 1 else CRIT) for r in rel]
bars = ax.bar(np.arange(len(SIZES)), rel, 0.64, color=cols)
for i, (b, r, s) in enumerate(zip(bars, rel, SIZES)):
    ax.text(b.get_x() + b.get_width() / 2, r + 0.055, f"{r:.2f}×", ha="center",
            fontsize=11.4, weight="bold" if s in (320, 480, 640) else "normal",
            color=INK)
ax.axhline(1.0, color=INK2, lw=1.4, ls="--")
ax.set_xticks(np.arange(len(SIZES)), [str(s) for s in SIZES], fontsize=10.5)
ax.set_xlabel("input size (square, pixels)")
ax.set_ylabel("work, relative to 640")
ax.set_ylim(0, 5.0)
ax.set_title("Halve each side, quarter the work", fontsize=12.5, loc="left")
ax.annotate("480 is 56% of the work at 640", xy=(2, rel[2]), xytext=(0.15, 2.05),
            fontsize=11.3, color=GOOD, weight="bold",
            arrowprops=dict(arrowstyle="->", color=GOOD, lw=1.7,
                            connectionstyle="arc3,rad=0.22"))
ax.annotate("1280 is 4× the work", xy=(7, rel[7]), xytext=(2.9, 4.55),
            fontsize=11.3, color=CRIT, weight="bold",
            arrowprops=dict(arrowstyle="->", color=CRIT, lw=1.7,
                            connectionstyle="arc3,rad=0.2"))

# ---- what that buys at a fixed CPU budget
ax = axs[1]
BUDGET = 1.0            # one unit of CPU, spent on 640 at 10 fps
cams = BUDGET / rel * 1.0
keep = [0, 2, 4, 6]
ax.barh(np.arange(len(keep)), [cams[i] for i in keep], 0.6,
        color=[GOOD, GOOD, INK2, CRIT])
for y, i in enumerate(keep):
    ax.text(cams[i] + 0.06, y, f"{cams[i]:.2f}× the cameras", va="center",
            fontsize=11.4, color=INK, weight="bold")
ax.set_yticks(np.arange(len(keep)), [f"{SIZES[i]} px" for i in keep], fontsize=11.5)
ax.set_xlim(0, 5.6)
ax.set_xlabel("cameras per box, relative to 640")
ax.set_title("The same CPU, different input size", fontsize=12.5, loc="left")
ax.grid(axis="y", visible=False)

fig.suptitle("On a CPU, input size is the cheapest lever you have",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.925,
         "Arithmetic from pixel count alone. Real throughput depends on the CPU, the runtime "
         "and threading, so measure on the machine you will deploy on.",
         ha="left", va="top", fontsize=11.2, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.875])
save(fig, f"{SLUG}-input-size-cost.png")

for s, r in zip(SIZES, rel):
    print(f"{s:5} px  {r:.3f}× the work of 640   -> {1/r:.2f}× the cameras")
