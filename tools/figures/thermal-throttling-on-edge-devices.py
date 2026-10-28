"""Figures for thermal-throttling-on-edge-devices. Schematic shapes only, no measured values or units."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, WARN, CRIT, save

SLUG = "thermal-throttling-on-edge-devices"
t = np.linspace(0, 60, 600)
temp = 1 - np.exp(-t / 9)
limit = 0.82
thr = temp >= limit
lat = np.where(thr, 1.0 + 0.6 * (temp - limit) / (1 - limit) + 0.25, 1.0)
t_hit = t[thr][0]

fig, axes = plt.subplots(2, 1, figsize=(10, 5.6), sharex=True)
ax = axes[0]
ax.plot(t, temp, color=C[1])
ax.axhline(limit, color=CRIT, ls="--", lw=1.2)
ax.text(59, limit + 0.03, "throttle threshold", ha="right", fontsize=11.5, color=CRIT)
ax.set_yticks([]); ax.set_ylabel("SoC temperature")
ax.set_ylim(0, 1.12)
ax.axvspan(0, 2, color=WARN, alpha=0.25, lw=0)
ax.text(2.6, 0.25, "a 2-minute benchmark\nends here", fontsize=11.5, color=INK2)
ax = axes[1]
ax.plot(t, lat, color=C[0])
ax.axvline(t_hit, color=MUTED, lw=1)
ax.text(t_hit + 0.8, 1.55, "clocks drop,\nlatency rises", fontsize=11.5, color=INK2)
ax.set_yticks([]); ax.set_ylabel("latency per frame")
ax.set_ylim(0.8, 1.95)
ax.set_xlabel("time under sustained load (minutes)")
axes[0].set_title("A short test finishes before the board heats up (schematic shape, not a measurement)",
                  loc="left")
fig.tight_layout()
save(fig, f"{SLUG}-schematic.png")
