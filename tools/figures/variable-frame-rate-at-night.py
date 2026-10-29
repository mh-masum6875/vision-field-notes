"""Figures for variable-frame-rate-at-night. Arithmetic and a constructed timeline, no measured data."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, WARN, save

SLUG = "variable-frame-rate-at-night"

fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})

# 1. Frame arrival: day at 25 fps, night at 12.5 fps (a camera lengthening exposure)
ax = axes[0]
day = np.arange(0, 2, 1 / 25)
night = np.arange(0, 2, 1 / 12.5)
ax.vlines(day, 1.1, 1.7, color=C[0], lw=1.2)
ax.vlines(night, 0.1, 0.7, color=C[1], lw=1.2)
ax.set_yticks([0.4, 1.4]); ax.set_yticklabels(["night\n12.5 fps", "day\n25 fps"])
ax.set_ylim(-0.1, 2.1); ax.set_xlim(0, 2)
ax.grid(axis="y", visible=False)
ax.set_xlabel("seconds")
ax.set_title("The same two seconds, as frames", loc="left")

# 2. A rule written in frames changes meaning with the frame rate
ax = axes[1]
fps = np.array([25, 15, 12.5, 8, 5])
secs = 50 / fps
ax.barh([f"{f:g} fps" for f in fps], secs, color=[C[0], C[3], C[1], C[1], C[1]], alpha=0.85, height=0.6)
for i, s in enumerate(secs):
    ax.text(s + 0.15, i, f"{s:.1f} s", va="center", fontsize=11.5, color=INK)
ax.invert_yaxis()
ax.set_xlim(0, 12)
ax.set_xlabel("real time covered by '50 frames'")
ax.grid(axis="y", visible=False)
ax.set_title("A 50-frame dwell rule", loc="left")
fig.suptitle("When the camera halves its frame rate at night, frame-based rules double in length (arithmetic)",
             x=0.01, ha="left", fontsize=13.5, weight="bold", y=1.02)
fig.tight_layout()
save(fig, f"{SLUG}-frames-vs-time.png")
