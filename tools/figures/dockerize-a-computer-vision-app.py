"""Figures for dockerize-a-computer-vision-app (pure diagrams)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT, save

SLUG = "dockerize-a-computer-vision-app"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, size=11.5, weight="normal", family=None, color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight,
            linespacing=1.25, family=family, color=color)


CACHED = ("#eaf2fb", C[0])
REBUILT = ("#fdf0e9", C[1])

# 1. Layer order and the build cache
good = [("FROM python:3.11-slim", CACHED), ("COPY requirements.txt .", CACHED),
        ("RUN pip install -r requirements.txt", CACHED), ("COPY src/ ./src/", REBUILT),
        ("COPY models/best.onnx ...", REBUILT)]
bad = [("FROM python:3.11-slim", CACHED), ("COPY . .", REBUILT),
       ("RUN pip install -r requirements.txt", REBUILT), ("", None), ("", None)]
fig, ax = plt.subplots(figsize=(10.5, 5.6))
ax.set_xlim(0, 10.5)
ax.set_ylim(-0.9, 5.6)
ax.axis("off")
for x0, layers, title, col in [(0.1, good, "Dependencies first (good)", GOOD),
                               (5.4, bad, "Code copied first (slow)", CRIT)]:
    ax.text(x0, 4.95, title, fontsize=13, weight="bold", color=col)
    for i, (txt, st) in enumerate(layers):
        if st is None:
            continue
        box(ax, x0, 0.3 + i * 0.85, 5.0, 0.7, txt, fc=st[0], ec=st[1], family="DejaVu Sans Mono", size=11)
ax.text(0.1, -0.35, "After a one-line code change:\nonly the top layers rebuild.", fontsize=11.5, color=INK2)
ax.text(5.4, -0.35, "After a one-line code change:\npip install runs again.", fontsize=11.5, color=INK2)
ax.legend(handles=[Patch(fc=CACHED[0], ec=CACHED[1], label="reused from cache"),
                   Patch(fc=REBUILT[0], ec=REBUILT[1], label="rebuilt after a code change")],
          loc="upper right", bbox_to_anchor=(1.0, 0.72), fontsize=11.5)
ax.set_title("Install dependencies before copying code so edits do not trigger a reinstall", loc="left")
save(fig, f"{SLUG}-layer-cache.png")

# 2. What is in the image vs on the host for GPU use
fig, ax = plt.subplots(figsize=(10.5, 5.6))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.6)
ax.axis("off")
ax.add_patch(FancyBboxPatch((0.1, 2.35), 6.6, 2.75, boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc="#f3f8fd", ec=C[0], lw=1.8))
ax.text(0.3, 4.75, "Container image (you build and version this)", fontsize=12.5, weight="bold", color=C[0])
box(ax, 0.4, 3.75, 6.0, 0.7, "Your app: OpenCV (headless), NumPy, model file")
box(ax, 0.4, 2.95, 2.9, 0.65, "onnxruntime-gpu")
box(ax, 3.5, 2.95, 2.9, 0.65, "CUDA + cuDNN libraries")
ax.add_patch(FancyBboxPatch((0.1, 0.2), 6.6, 1.85, boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc="#f7f6f2", ec=INK2, lw=1.8))
ax.text(0.3, 1.7, "Host (installed on the machine)", fontsize=12.5, weight="bold", color=INK2)
box(ax, 0.4, 0.45, 1.9, 0.95, "Linux kernel")
box(ax, 2.45, 0.45, 1.9, 0.95, "NVIDIA\ndriver")
box(ax, 4.5, 0.45, 1.9, 0.95, "NVIDIA Container\nToolkit", size=10.5)
# compatibility brackets
ax.annotate("", xy=(6.95, 3.27), xytext=(6.95, 0.92),
            arrowprops=dict(arrowstyle="<->", color=CRIT, lw=1.6))
ax.text(7.15, 2.1, "Versions must be compatible:\nhost driver  ↔  CUDA in image\n↔  onnxruntime-gpu build.\n"
        "Check the ONNX Runtime\ncompatibility table.", fontsize=11.5, color=INK, va="center")
ax.text(7.15, 0.75, "docker run --gpus all ...\npasses the GPU in", fontsize=11, color=INK2, va="center",
        family="DejaVu Sans Mono")
ax.set_title("The image carries CUDA libraries; the GPU driver stays on the host", loc="left")
save(fig, f"{SLUG}-gpu-stack.png")
