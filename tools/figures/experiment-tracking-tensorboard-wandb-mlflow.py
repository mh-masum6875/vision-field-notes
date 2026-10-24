"""Figures for experiment-tracking-tensorboard-wandb-mlflow.md"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, save

SLUG = "experiment-tracking-tensorboard-wandb-mlflow"


def box(ax, x, y, w, h, color, fill=0.10, lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.15",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw))


def arrow(ax, p1, p2):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.8, mutation_scale=16))


# 1. One run = inputs + outputs, linked
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.set_xlim(0, 12.4); ax.set_ylim(0, 6.7); ax.axis("off")
ax.text(0.1, 6.55, "A run is only reproducible if its inputs are recorded with its outputs",
        fontsize=14, weight="bold", va="top")
inputs = ["model + starting weights", "dataset version or hash", "imgsz, epochs, batch, LR",
          "augmentation settings", "random seed", "git commit", "library versions"]
outputs = ["train / val loss per epoch", "P, R and mAP per epoch", "per-class metrics at the end",
           "weights file + its location", "sample predictions (images)", "training time + hardware"]
box(ax, 0.1, 0.5, 4.6, 5.2, C[0])
ax.text(2.4, 5.35, "Inputs: what you changed", ha="center", fontsize=13, weight="bold")
for i, t in enumerate(inputs):
    ax.text(0.4, 4.75 - i * 0.6, "•  " + t, fontsize=12, va="center")
box(ax, 7.7, 0.5, 4.6, 5.2, C[1])
ax.text(10.0, 5.35, "Outputs: what happened", ha="center", fontsize=13, weight="bold")
for i, t in enumerate(outputs):
    ax.text(7.95, 4.75 - i * 0.6, "•  " + t, fontsize=12, va="center")
box(ax, 5.05, 2.45, 2.3, 1.3, ACCENT, fill=0.14)
ax.text(6.2, 3.25, "run", ha="center", fontsize=12, color=INK2)
ax.text(6.2, 2.85, "n-640-relabel", ha="center", fontsize=12, weight="bold")
arrow(ax, (4.7, 3.1), (5.05, 3.1))
arrow(ax, (7.35, 3.1), (7.7, 3.1))
ax.text(6.2, 1.75, "Settings are\nthe part people\nforget", ha="center", va="top", fontsize=11.5, color=INK2)
save(fig, f"{SLUG}-what-to-log.png")

# 2. Why keep the full curve (illustrative)
ep = np.arange(1, 101)
rng = np.random.default_rng(3)
a = 0.62 * (1 - np.exp(-ep / 12)) - 0.0022 * np.clip(ep - 35, 0, None) + rng.normal(0, 0.006, ep.size)
b = 0.60 * (1 - np.exp(-ep / 25)) + rng.normal(0, 0.006, ep.size)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ep, a, color=C[0], label="Run A")
ax.plot(ep, b, color=C[1], label="Run B")
for y, col, name in [(a, C[0], "A"), (b, C[1], "B")]:
    i = int(np.argmax(y))
    ax.plot(ep[i], y[i], "o", color=col, ms=7)
    ax.annotate(f"best epoch of run {name}", (ep[i], y[i]), xytext=(ep[i] + (4 if name == "A" else -32), y[i] + 0.06),
                fontsize=12, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=1))
ax.annotate("A falls after its peak:\noverfitting", (85, a[84]), xytext=(70, 0.22), fontsize=12, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=1))
ax.set_xlabel("Epoch")
ax.set_ylabel("Validation mAP50 (illustrative)")
ax.set_ylim(0, 0.8)
ax.set_xlim(0, 101)
ax.legend(loc="lower right")
ax.set_title("Two runs with similar best scores can behave very differently", loc="left")
save(fig, f"{SLUG}-full-curve.png")
