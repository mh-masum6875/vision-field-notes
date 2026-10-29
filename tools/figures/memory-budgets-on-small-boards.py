"""Figures for memory-budgets-on-small-boards. Pure arithmetic: bytes of decoded BGR frames held in queues."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "memory-budgets-on-small-boards"
streams = np.arange(1, 17)
res = [("640 x 360", 640, 360, C[2]), ("1280 x 720", 1280, 720, C[0]),
       ("1920 x 1080", 1920, 1080, C[1]), ("3840 x 2160", 3840, 2160, C[6])]
DEPTH = 30
fig, ax = plt.subplots(figsize=(10, 4.8))
for name, w, h, c in res:
    gb = streams * DEPTH * w * h * 3 / 1e9
    ax.plot(streams, gb, color=c, marker="o", ms=3.5, label=f"{name}  ({w * h * 3 / 1e6:.1f} MB per frame)")
for g in (1, 2, 4, 8):
    ax.axhline(g, color=GRID, lw=1.2, zorder=0)
    ax.text(16.4, g, f"{g} GB", va="center", fontsize=11, color=INK2)
ax.set_yscale("log")
ax.set_yticks([0.1, 0.3, 1, 3, 10, 30])
ax.get_yaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(plt.matplotlib.ticker.NullFormatter())
ax.set_xlim(1, 17.5)
ax.set_xlabel("camera streams")
ax.set_ylabel("memory for queued frames (GB, log)")
ax.legend(loc="upper left", fontsize=11)
ax.set_title(f"A queue of {DEPTH} decoded BGR frames per stream, by resolution (arithmetic)", loc="left")
save(fig, f"{SLUG}-frame-queues.png")
