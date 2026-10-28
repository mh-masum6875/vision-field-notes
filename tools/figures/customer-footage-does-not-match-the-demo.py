"""Figures for customer-footage-does-not-match-the-demo.

Pure geometry: pixels on a 1.7 m tall person for a 1080p camera, before and after resizing to a 640 model input.
Assumes a simple pinhole camera with the person upright and roughly facing the camera; no measured data.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, WARN, save

SLUG = "customer-footage-does-not-match-the-demo"
d = np.linspace(3, 60, 400)
H_PX, PERSON = 1080, 1.7
fig, ax = plt.subplots(figsize=(10, 5))
for vfov, c in [(60, C[1]), (30, C[0]), (12, C[2])]:
    cover = 2 * d * np.tan(np.radians(vfov / 2))
    px = H_PX * PERSON / cover
    ax.plot(d, px / 3, color=c, label=f"vertical field of view {vfov}°")
ax.axhspan(0, 16, color=WARN, alpha=0.18, lw=0)
ax.text(59, 9, "very small at the model input", ha="right", fontsize=11.5, color=INK2)
ax.set_yscale("log")
ax.set_yticks([5, 10, 20, 50, 100, 200, 400])
ax.get_yaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(plt.matplotlib.ticker.NullFormatter())
ax.set_xlim(3, 60)
ax.set_xlabel("distance from camera (m)")
ax.set_ylabel("person height at 640 input (px, log)")
ax.legend(loc="upper right", fontsize=11.5)
ax.set_title("Same person, same 1080p camera: lens and distance decide the pixels (geometry only)", loc="left")
save(fig, f"{SLUG}-pixels-on-target.png")
