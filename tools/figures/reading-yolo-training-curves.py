"""Figures for reading-yolo-training-curves.

Constructed curves that show common shapes (healthy, overfitting, still improving). Not from a training run.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "reading-yolo-training-curves"
rng = np.random.default_rng(8)
e = np.arange(1, 201)
n = lambda s: rng.normal(0, s, len(e))

fig, axes = plt.subplots(1, 3, figsize=(13, 4.3), sharey=False)
cases = [
    ("Healthy: both fall, then flatten",
     1.6 * np.exp(-e / 35) + 0.55 + n(0.01), 1.6 * np.exp(-e / 35) + 0.68 + n(0.015), None),
    ("Overfitting: validation turns up",
     1.6 * np.exp(-e / 30) + 0.35 - 0.0008 * e + n(0.01),
     1.4 * np.exp(-e / 30) + 0.75 + 0.000015 * np.clip(e - 60, 0, None) ** 2 + n(0.015), 60),
    ("Not finished: still falling at the end",
     1.6 * np.exp(-e / 120) + 0.45 + n(0.01), 1.6 * np.exp(-e / 120) + 0.58 + n(0.015), None),
]
for ax, (title, tr, va, best) in zip(axes, cases):
    ax.plot(e, tr, color=C[0], label="train loss")
    ax.plot(e, va, color=C[1], label="validation loss")
    if best:
        best = int(e[np.argmin(np.convolve(va, np.ones(15) / 15, mode="same")[10:-10]) + 10])
        ax.axvline(best, color=INK2, ls="--", lw=1.1)
        ax.text(best + 4, va.max() * 0.97, "best validation\naround here", fontsize=10.5, color=INK2, va="top")
    ax.set_title(title, loc="left", fontsize=12.5)
    ax.set_xlabel("epoch"); ax.set_yticks([])
axes[0].set_ylabel("loss")
axes[0].legend(loc="upper right", fontsize=10.5)
fig.suptitle("Three loss-curve shapes worth recognising (constructed curves)", x=0.01, ha="left",
             fontsize=14, weight="bold", y=1.03)
fig.tight_layout()
save(fig, f"{SLUG}-shapes.png")
