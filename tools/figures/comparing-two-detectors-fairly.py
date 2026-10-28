"""Figures for comparing-two-detectors-fairly. Pure arithmetic (binomial standard error), no measured data."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "comparing-two-detectors-fairly"
n = np.arange(20, 3001)
fig, ax = plt.subplots(figsize=(10, 4.8))
for p, c in [(0.5, C[1]), (0.8, C[0]), (0.95, C[2])]:
    half = 1.96 * np.sqrt(p * (1 - p) / n) * 100
    ax.plot(n, half, color=c, label=f"true recall {p:.2f}")
for v in (100, 500, 2000):
    h = 1.96 * np.sqrt(0.8 * 0.2 / v) * 100
    ax.plot([v], [h], "o", color=C[0], ms=6)
    ax.text(v * 1.08, h + 0.6, f"{v} objects: ± {h:.1f} points", fontsize=11.5, color=INK)
ax.set_xscale("log")
ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000])
ax.get_xaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
ax.set_xlim(20, 3000); ax.set_ylim(0, 23)
ax.set_xlabel("number of objects in the test set (log scale)")
ax.set_ylabel("95% interval, ± percentage points")
ax.legend(loc="upper right", fontsize=11.5)
ax.set_title("How much a recall figure can move by chance alone (normal approximation)", loc="left")
save(fig, f"{SLUG}-sampling-noise.png")
