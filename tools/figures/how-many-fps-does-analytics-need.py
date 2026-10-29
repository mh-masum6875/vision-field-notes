"""Figures for how-many-fps-does-analytics-need. Pure arithmetic: frames in which a moving object is visible."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, WARN, save

SLUG = "how-many-fps-does-analytics-need"
fps = np.array([1, 2, 3, 5, 8, 10, 15, 25])
cases = [("person walking 1.4 m/s across a 10 m view", 10 / 1.4, C[0]),
         ("person running 4 m/s across a 10 m view", 10 / 4, C[1]),
         ("car at 50 km/h across a 30 m view", 30 / (50 / 3.6), C[6]),
         ("car at 50 km/h across a 10 m view", 10 / (50 / 3.6), C[3])]
fig, ax = plt.subplots(figsize=(10, 5))
for name, secs, c in cases:
    ax.plot(fps, fps * secs, color=c, marker="o", label=f"{name}  ({secs:.1f} s)")
ax.axhspan(0, 8, color=WARN, alpha=0.18, lw=0)
ax.text(24.5, 5.5, "too few frames for a\n5-of-8 filter and a tracker", ha="right", fontsize=11, color=INK2)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xticks(fps); ax.get_xaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
ax.set_yticks([1, 2, 5, 10, 20, 50, 100, 200])
ax.get_yaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(plt.matplotlib.ticker.NullFormatter())
ax.set_xlim(0.9, 28); ax.set_ylim(0.5, 250)
ax.set_xlabel("frames analysed per second (log)")
ax.set_ylabel("frames showing the object (log)")
ax.legend(loc="upper left", fontsize=10.5)
ax.set_title("How many frames you get of an object passing through the view (arithmetic)", loc="left")
save(fig, f"{SLUG}-frames-per-pass.png")
