"""Figures for raspberry-pi-ai-kit-hailo (pure diagrams)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT, save

SLUG = "raspberry-pi-ai-kit-hailo"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, size=11.5, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight,
            linespacing=1.3)


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=16, shrinkA=0, shrinkB=0))


# 1. Toolchain: the accelerator path adds a compile + quantize step
fig, ax = plt.subplots(figsize=(10.5, 5.1))
ax.set_xlim(0, 10.5)
ax.set_ylim(-0.15, 5.0)
ax.axis("off")
ax.text(0.1, 4.55, "CPU only", fontsize=13, weight="bold", color=C[0])
ax.text(0.1, 2.35, "With accelerator", fontsize=13, weight="bold", color=C[1])
# CPU lane
for i, t in enumerate(["Train and\nvalidate", "Export\nto ONNX", "ONNX Runtime\non the Pi CPU"]):
    x = 0.1 + i * 3.6 if i < 2 else 7.3
    box(ax, x, 3.3, 3.0 if i < 2 else 3.1, 1.0, t, fc="#eaf2fb", ec=C[0])
arrow(ax, 3.1, 3.8, 3.7, 3.8)
arrow(ax, 6.7, 3.8, 7.3, 3.8)
# Accelerator lane
box(ax, 0.1, 1.1, 1.9, 1.0, "Train and\nvalidate", fc="#fdf0e9", ec=C[1])
arrow(ax, 2.0, 1.6, 2.35, 1.6)
box(ax, 2.35, 1.1, 1.6, 1.0, "Export\nto ONNX", fc="#fdf0e9", ec=C[1])
arrow(ax, 3.95, 1.6, 4.3, 1.6)
box(ax, 4.3, 0.85, 2.7, 1.5, "Vendor compiler:\nparse, optimise,\nquantize to INT8,\ncompile", fc="#fff6dc", ec=C[3],
    weight="bold")
arrow(ax, 7.0, 1.6, 7.3, 1.6)
box(ax, 7.3, 1.1, 3.1, 1.0, "Vendor runtime\non the accelerator", fc="#fdf0e9", ec=C[1])
box(ax, 4.3, 0.0, 2.7, 0.55, "+ calibration images", fc="#ffffff", ec=MUTED, size=10.5)
arrow(ax, 5.65, 0.55, 5.65, 0.85)
ax.text(5.65, 2.55, "new step: supported layers only,\naccuracy must be re-checked", ha="center",
        fontsize=10.5, color=INK2)
ax.set_title("The accelerator adds a compile-and-quantize step to the toolchain", loc="left")
save(fig, f"{SLUG}-toolchain.png")

# 2. Which stages move to the accelerator
stages = ["Video\ndecode", "Pre-\nprocess", "Inference", "Post-process\n(NMS)", "Tracking,\nrules", "Alerts,\nstorage"]
fig, ax = plt.subplots(figsize=(10.5, 3.9))
ax.set_xlim(0, 10.5)
ax.set_ylim(-0.1, 3.8)
ax.axis("off")
w, gap = 1.5, 0.22
for row, (y, label) in enumerate([(2.2, "Pi CPU only"), (0.5, "Pi + accelerator")]):
    ax.text(0.1, y + 1.15, label, fontsize=12.5, weight="bold", color=INK)
    for i, s in enumerate(stages):
        x = 0.1 + i * (w + gap)
        on_acc = row == 1 and s == "Inference"
        box(ax, x, y, w, 0.85, s, fc="#fff6dc" if on_acc else "#eaf2fb", ec=C[3] if on_acc else C[0],
            size=11, weight="bold" if on_acc else "normal")
        if i < len(stages) - 1:
            arrow(ax, x + w, y + 0.425, x + w + gap, y + 0.425)
ax.text(0.1, 0.05, "blue = runs on the Pi CPU    yellow = runs on the accelerator", ha="left", fontsize=11, color=INK2)
ax.set_title("The accelerator takes over one stage; the CPU still does the rest", loc="left")
save(fig, f"{SLUG}-pipeline-split.png")
