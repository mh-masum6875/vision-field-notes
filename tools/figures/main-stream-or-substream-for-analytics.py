"""Figures for main-stream-or-substream-for-analytics.

Pure arithmetic: a person 5% of the frame height tall, letterboxed into a 640 and a 1280 model input, from
streams of different resolution; and the pixels per second each stream costs to decode at 15 fps.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, WARN, save

SLUG = "main-stream-or-substream-for-analytics"
streams = [("640 x 360", 640, 360), ("1280 x 720", 1280, 720), ("1920 x 1080", 1920, 1080), ("3840 x 2160", 3840, 2160)]
FRAC = 0.05


def at_input(w, h, s):
    r = min(s / w, s / h)
    r = min(r, 1.0)  # never upscale a small stream
    return h * FRAC * r


fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
ax = axes[0]
y = np.arange(len(streams))
v640 = [at_input(w, h, 640) for _, w, h in streams]
v1280 = [at_input(w, h, 1280) for _, w, h in streams]
ax.barh(y - 0.19, v640, height=0.36, color=C[0], label="model input 640")
ax.barh(y + 0.19, v1280, height=0.36, color=C[1], label="model input 1280")
for i, (a, b) in enumerate(zip(v640, v1280)):
    ax.text(a + 0.4, i - 0.19, f"{a:.0f} px", va="center", fontsize=10.5)
    ax.text(b + 0.4, i + 0.19, f"{b:.0f} px", va="center", fontsize=10.5)
ax.set_yticks(y); ax.set_yticklabels([s[0] for s in streams]); ax.invert_yaxis()
ax.set_xlabel("height of the person at the model input (px)")
ax.set_xlim(0, 42)
ax.grid(axis="y", visible=False)
ax.legend(loc="lower right", fontsize=10.5)
ax.set_title("Person 5% of frame height", loc="left", fontsize=13)

ax = axes[1]
mpx = [w * h * 15 / 1e6 for _, w, h in streams]
ax.barh(y, mpx, height=0.55, color=C[6], alpha=0.85)
for i, v in enumerate(mpx):
    ax.text(v + 2, i, f"{v:.0f}", va="center", fontsize=10.5)
ax.set_yticks(y); ax.set_yticklabels([s[0] for s in streams]); ax.invert_yaxis()
ax.set_xlabel("megapixels per second to decode at 15 fps")
ax.set_xlim(0, 145)
ax.grid(axis="y", visible=False)
ax.set_title("Decode cost per camera", loc="left", fontsize=13)
fig.suptitle("Above the model's input size, extra stream resolution costs decode work and adds no pixels (arithmetic)",
             x=0.01, ha="left", fontsize=13, weight="bold", y=1.03)
fig.tight_layout()
save(fig, f"{SLUG}-resolution.png")
