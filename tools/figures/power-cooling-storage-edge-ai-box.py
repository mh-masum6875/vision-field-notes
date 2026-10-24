"""Figures for power-cooling-storage-edge-ai-box.

Figure 1 is simulated (illustrative) data, not a measurement of any device.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "power-cooling-storage-edge-ai-box"

# 1. Illustrative thermal throttling: log temperature next to frame rate
t = np.linspace(0, 30, 150)  # minutes
limit = 80.0
rng = np.random.default_rng(3)
bare_T = np.minimum(35 + 50 * (1 - np.exp(-t / 5)), limit + 0.6 * np.sin(t * 3))
cool_T = 35 + 25 * (1 - np.exp(-t / 6))
throttled = np.clip((35 + 50 * (1 - np.exp(-t / 5)) - limit) / 5.0, 0, 1)
bare_fps = 100 - 38 * throttled + rng.normal(0, 0.8, t.size)
cool_fps = 100 + rng.normal(0, 0.8, t.size)

fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 6.6), sharex=True)
a1.plot(t, bare_T, color=C[1], label="bare board")
a1.plot(t, cool_T, color=C[0], label="with heatsink and fan")
a1.axhline(limit, color=MUTED, lw=1, ls="--")
a1.text(30, limit + 1.5, "throttle point", ha="right", fontsize=11, color=INK2)
a1.set_ylabel("temperature (°C)")
a1.set_ylim(30, 92)
a1.legend(loc="lower right")
a1.set_title("Temperature", loc="left", fontsize=12.5)
a2.plot(t, bare_fps, color=C[1], label="bare board")
a2.plot(t, cool_fps, color=C[0], label="with heatsink and fan")
a2.set_ylabel("frame rate (% of start)")
a2.set_ylim(50, 110)
a2.set_xlabel("minutes under sustained load")
a2.set_title("Frame rate", loc="left", fontsize=12.5)
a2.annotate("a 1-minute test\nlooks fine", xy=(1, 100), xytext=(3.5, 66), fontsize=11, color=INK2,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=1))
a2.annotate("throttling starts:\nframe rate drops, no error", xy=(12.5, 94), xytext=(16.5, 53), fontsize=11, color=INK2,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=1))
fig.suptitle("Without cooling, frame rate falls once the board reaches its throttle point (simulated)",
             x=0.01, ha="left", fontsize=14, weight="bold")
fig.tight_layout()
save(fig, f"{SLUG}-throttling.png")


# 2. Recovery layers: what fails and what brings it back
def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, size=11.5, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight,
            linespacing=1.25)


rows = [
    ("App crashes", "Process supervisor restarts it\n(systemd, Docker restart policy)"),
    ("Main loop hangs,\nprocess still alive", "App heartbeat check\nrestarts the loop or process"),
    ("Whole device hangs", "Hardware watchdog\nreboots the board"),
    ("Power cut", "UPS, few writes, read-only root;\napp starts again on boot"),
    ("Silent for any reason", "Remote monitoring alerts\nwhen data stops arriving"),
]
fig, ax = plt.subplots(figsize=(10, 6.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")
ax.text(1.85, 5.75, "What goes wrong", ha="center", fontsize=12.5, weight="bold", color=CRIT)
ax.text(6.9, 5.75, "What recovers it without a site visit", ha="center", fontsize=12.5, weight="bold", color=ACCENT)
for i, (fail, fix) in enumerate(rows):
    y = 4.6 - i * 1.1
    box(ax, 0.1, y, 3.5, 0.85, fail, fc="#fbeaea", ec=CRIT)
    ax.annotate("", xy=(4.3, y + 0.425), xytext=(3.6, y + 0.425),
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=16, shrinkA=0, shrinkB=0))
    box(ax, 4.3, y, 5.2, 0.85, fix, fc="#e6f2ef", ec=ACCENT)
ax.set_title("Layer the recovery: each layer catches what the one above misses", loc="left")
save(fig, f"{SLUG}-recovery-layers.png")
