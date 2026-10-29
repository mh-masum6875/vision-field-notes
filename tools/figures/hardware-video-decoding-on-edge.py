"""Figures for hardware-video-decoding-on-edge. Pure arithmetic: pixels per second the decoder must produce."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "hardware-video-decoding-on-edge"
cases = [("8 x 720p @ 15", 8 * 1280 * 720 * 15), ("4 x 1080p @ 25", 4 * 1920 * 1080 * 25),
         ("8 x 1080p @ 15", 8 * 1920 * 1080 * 15), ("8 x 1080p @ 25", 8 * 1920 * 1080 * 25),
         ("2 x 4K @ 25", 2 * 3840 * 2160 * 25), ("16 x 1080p @ 25", 16 * 1920 * 1080 * 25)]
names = [c[0] for c in cases]
mpx = np.array([c[1] for c in cases]) / 1e6
model = np.array([8 * 15, 4 * 25, 8 * 15, 8 * 25, 2 * 25, 16 * 25]) * 640 * 640 / 1e6

fig, ax = plt.subplots(figsize=(10.5, 4.8))
y = np.arange(len(cases))
ax.barh(y - 0.19, mpx, height=0.36, color=C[1], label="decoded by the video decoder")
ax.barh(y + 0.19, model, height=0.36, color=C[0], label="seen by a 640 x 640 model")
for i, (a, b) in enumerate(zip(mpx, model)):
    ax.text(a + 8, i - 0.19, f"{a:.0f}", va="center", fontsize=10.5, color=INK)
    ax.text(b + 8, i + 0.19, f"{b:.0f}", va="center", fontsize=10.5, color=INK)
ax.set_yticks(y); ax.set_yticklabels(names)
ax.invert_yaxis()
ax.set_xlabel("megapixels per second")
ax.grid(axis="y", visible=False)
ax.legend(loc="lower right", fontsize=11)
ax.set_title("Every stream is decoded at full resolution before it is shrunk for the model (arithmetic)",
             loc="left")
save(fig, f"{SLUG}-pixel-rates.png")
