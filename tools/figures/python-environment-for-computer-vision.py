"""Figures for python-environment-for-computer-vision.md"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, CRIT, save

SLUG = "python-environment-for-computer-vision"


def box(ax, x, y, w, h, color, fill=0.12, lw=1.6, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw, ls=ls))


def arrow(ax, p1, p2, color=INK2):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=15))


# 1. The GPU stack and where torch.cuda.is_available() == False comes from
fig, ax = plt.subplots(figsize=(10, 5.8))
ax.set_xlim(0, 12.1); ax.set_ylim(0, 7); ax.axis("off")
ax.text(0.05, 6.85, "torch.cuda.is_available() needs every layer to line up", fontsize=14, weight="bold", va="top")
layers = [  # bottom to top: (title, check)
    ("NVIDIA GPU", "the hardware"),
    ("NVIDIA driver", "check: nvidia-smi (driver + max CUDA)"),
    ("PyTorch wheel (bundles its CUDA runtime)", "check: torch.cuda.is_available()"),
    ("Your libraries: ultralytics, opencv, ...", "install after PyTorch"),
]
colors = [MUTED, C[0], C[1], C[2]]
y = 0.35
for (title, check), col in zip(layers, colors):
    box(ax, 0.1, y, 7.0, 1.2, col)
    ax.text(0.35, y + 0.78, title, fontsize=12.5, weight="bold", va="center")
    ax.text(0.35, y + 0.36, check, fontsize=12, color=INK2, va="center")
    y += 1.45
causes = [  # (text, layer index it points at)
    ("Container started without\nGPU passthrough", 0),
    ("Driver missing, or too old\nfor the wheel's CUDA version", 1),
    ("CPU-only build installed,\nor replaced by a later install", 2),
]
ax.text(7.95, 6.15, "Usual reasons it prints False", fontsize=12.5, weight="bold", va="center")
for i, (t, li) in enumerate(causes):
    cy = 0.35 + li * 1.45 + 0.6
    box(ax, 7.75, cy - 0.5, 4.2, 1.0, CRIT, fill=0.06)
    ax.text(7.95, cy, t, fontsize=12, va="center")
    arrow(ax, (7.75, cy), (7.15, cy), color=CRIT)
save(fig, f"{SLUG}-gpu-stack.png")

# 2. Training vs runtime requirements
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.set_xlim(0, 12); ax.set_ylim(0, 6.3); ax.axis("off")
ax.text(0.05, 6.2, "Ship only what the deployed app needs", fontsize=14, weight="bold", va="top")
train = ["torch (CUDA build)", "ultralytics", "experiment tracking", "plotting, notebooks",
         "+ everything in runtime"]
runtime = ["opencv-python-headless", "onnxruntime", "numpy", "your app code"]
box(ax, 0.1, 0.4, 5.0, 4.9, C[1])
ax.text(2.6, 4.85, "requirements-train.txt", ha="center", fontsize=13, weight="bold", family="DejaVu Sans Mono")
ax.text(2.6, 4.4, "GPU workstation or cloud", ha="center", fontsize=12, color=INK2)
for i, t in enumerate(train):
    ax.text(0.45, 3.75 - i * 0.6, "•  " + t, fontsize=12.5, va="center",
            color=INK2 if t.startswith("+") else INK)
box(ax, 6.9, 1.3, 5.0, 4.0, C[2])
ax.text(9.4, 4.85, "requirements-runtime.txt", ha="center", fontsize=13, weight="bold", family="DejaVu Sans Mono")
ax.text(9.4, 4.4, "edge device, server, container", ha="center", fontsize=12, color=INK2)
for i, t in enumerate(runtime):
    ax.text(7.25, 3.75 - i * 0.6, "•  " + t, fontsize=12.5, va="center")
arrow(ax, (5.15, 2.85), (6.85, 2.85))
ax.text(6.0, 3.0, "model.onnx", ha="center", va="bottom", fontsize=12, color=INK)
ax.text(9.4, 0.75, "Smaller install, fewer things to break,\nsmaller container image", ha="center",
        va="center", fontsize=12, color=INK2)
save(fig, f"{SLUG}-train-vs-runtime.png")
