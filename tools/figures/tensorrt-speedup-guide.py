"""Figures for tensorrt-speedup-guide (pure diagrams)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT, save

SLUG = "tensorrt-speedup-guide"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, size=12, weight="normal", color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight,
            linespacing=1.3, color=color)


def arrow(ax, x1, y1, x2, y2, color=INK2, style_="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style_, color=color, lw=1.6, mutation_scale=16,
                                shrinkA=0, shrinkB=0))


# 1. ONNX is the portable source; engines are per-target build artefacts
fig, ax = plt.subplots(figsize=(10.5, 5.8))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.8)
ax.axis("off")
box(ax, 0.1, 2.2, 1.7, 1.0, "PyTorch\nbest.pt", fc="#f4f3ef")
arrow(ax, 1.8, 2.7, 2.15, 2.7)
box(ax, 2.15, 2.0, 2.3, 1.4, "best.onnx\nportable source\nof truth", fc="#e6f2ef", ec=ACCENT, weight="bold")
targets = ["Jetson device\nits GPU + TensorRT", "Desktop RTX GPU\nits GPU + TensorRT", "Cloud GPU\nits GPU + TensorRT"]
ys = [4.0, 2.2, 0.4]
for t, y in zip(targets, ys):
    arrow(ax, 4.45, 2.7, 5.0, y + 0.5)
    box(ax, 5.0, y, 2.3, 1.0, "build on target\n" + t.split("\n")[0], fc="#ffffff", size=11)
    arrow(ax, 7.3, y + 0.5, 7.7, y + 0.5)
    box(ax, 7.7, y, 2.7, 1.0, ".engine\nvalidate accuracy,\nthen benchmark", fc="#fdf0e9", ec=C[1], size=11)
ax.text(6.15, 5.3, "rebuild per GPU type\nand TensorRT version", fontsize=11, color=INK2, ha="center", va="center")
ax.text(9.05, 5.3, "not portable", fontsize=11, color=C[1], ha="center", weight="bold")
ax.set_title("Keep the ONNX file; build a separate engine on each target", loc="left")
save(fig, f"{SLUG}-onnx-to-engines.png")

# 2. Layer fusion: three kernels with memory round-trips become one kernel
fig, ax = plt.subplots(figsize=(10.5, 4.6))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 4.6)
ax.axis("off")
ax.text(0.1, 4.2, "Before: three kernels", fontsize=13, weight="bold", color=INK)
ops = ["Convolution", "Bias add", "Activation"]
x = 0.1
for i, op in enumerate(ops):
    box(ax, x, 2.75, 1.9, 0.95, op + "\nkernel", fc="#ffffff")
    if i < 2:
        box(ax, x + 2.1, 2.8, 1.2, 0.85, "write,\nthen read\nmemory", fc="#f4f3ef", ec=MUTED, size=10.5, color=INK2)
        arrow(ax, x + 1.9, 3.22, x + 2.1, 3.22)
        arrow(ax, x + 3.3, 3.22, x + 3.5, 3.22)
    x += 3.5
ax.text(0.1, 1.75, "After TensorRT fusion: one kernel", fontsize=13, weight="bold", color=INK)
box(ax, 0.1, 0.35, 6.4, 0.95, "Convolution + bias + activation\nin a single kernel", fc="#e6f2ef",
    ec=ACCENT, weight="bold")
ax.text(6.8, 0.82, "intermediate results stay\non-chip: fewer launches,\nless memory traffic",
        fontsize=11.5, color=INK2, va="center")
ax.set_title("Layer fusion removes memory round-trips between small operations", loc="left")
save(fig, f"{SLUG}-layer-fusion.png")
