"""Figures for measuring-fps-and-latency-correctly.

All timing data here is simulated (illustrative), not measured on any hardware.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "measuring-fps-and-latency-correctly"
rng = np.random.default_rng(11)

# 1. Warm-up: first iterations are slow
n = 120
base = 20 + rng.gamma(4, 0.35, n)
warm = 160 * np.exp(-np.arange(n) / 2.2)
lat = base + warm
lat[0] = 420  # first call includes setup
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.axvspan(-0.5, 19.5, color=WARN, alpha=0.12, lw=0)
ax.plot(np.arange(n), lat, color=C[0], marker="o", ms=3, lw=1.5)
ax.set_yscale("log")
ax.set_yticks([20, 30, 50, 100, 200, 400])
ax.get_yaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(plt.matplotlib.ticker.NullFormatter())
ax.set_xlim(-1, n)
ax.set_xlabel("iteration")
ax.set_ylabel("latency (ms, log scale)")
ax.text(21.5, 250, "<- warm-up: discard these\n    (first 20 runs here)", ha="left", fontsize=11.5, color=INK)
ax.text(70, 45, "steady state: start timing here", ha="center", fontsize=11.5, color=INK)
ax.set_title("The first runs measure start-up, not steady state (simulated data)", loc="left")
save(fig, f"{SLUG}-warmup.png")

# 2. Distribution: the mean hides the tail
lat = np.concatenate([rng.normal(25, 1.5, 1900), rng.normal(48, 6, 90), rng.uniform(70, 110, 10)])
mean, med, p95, p99, mx = lat.mean(), np.median(lat), np.percentile(lat, 95), np.percentile(lat, 99), lat.max()
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.hist(lat, bins=np.arange(15, 115, 1), color=C[0], alpha=0.85)
ax.set_yscale("log")
ax.set_yticks([1, 10, 100])
ax.get_yaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(plt.matplotlib.ticker.NullFormatter())
for v, name, y, ha in [(med, "median", 300, "right"), (p95, "p95", 60, "left"), (p99, "p99", 60, "left"),
                       (mx, "max", 60, "right")]:
    ax.axvline(v, color=INK2, lw=1.2, ls="--")
    off = 0.8 if ha == "left" else -0.8
    ax.text(v + off, y, f"{name}\n{v:.0f} ms", fontsize=11.5, color=INK, va="top", ha=ha)
ax.text(0.98, 0.95, f"mean {mean:.0f} ms   median {med:.0f} ms\np95 {p95:.0f} ms   p99 {p99:.0f} ms   max {mx:.0f} ms",
        transform=ax.transAxes, ha="right", va="top", fontsize=11.5,
        bbox=dict(fc="white", ec=GRID, boxstyle="round,pad=0.35"))
ax.set_xlabel("latency per frame (ms)")
ax.set_ylabel("frames (log scale)")
ax.set_title("Mean and median look fine; the slow tail is what users notice (simulated)", loc="left")
save(fig, f"{SLUG}-latency-distribution.png")

# 3. Batching: more throughput, but frames wait for the batch to fill
fig, ax = plt.subplots(figsize=(10.5, 4.8))
ax.set_xlim(-0.3, 12.3)
ax.set_ylim(-0.4, 3.9)
ax.set_yticks([])
ax.grid(False)
for s in ["left"]:
    ax.spines[s].set_visible(False)
ax.set_xlabel("time (in frame intervals)")
# Batch 1: each frame processed as it arrives (takes 0.6 interval)
y1, y4 = 2.6, 0.7
ax.text(-0.3, y1 + 0.85, "Batch 1", fontsize=12.5, weight="bold", color=INK)
ax.text(-0.3, y4 + 0.85, "Batch 4", fontsize=12.5, weight="bold", color=INK)
for f in range(12):
    ax.plot([f, f], [y1 - 0.15, y1 + 0.55], color=MUTED, lw=1)
    ax.plot([f, f], [y4 - 0.15, y4 + 0.55], color=MUTED, lw=1)
    ax.add_patch(Rectangle((f, y1), 0.6, 0.4, fc=C[0], ec="none", alpha=0.85))
# Batch 4: frames 0-3 wait, then one batch run of 1.5 intervals
for b in range(3):
    start = b * 4 + 3
    ax.add_patch(Rectangle((b * 4, y4 + 0.05), 3, 0.3, fc=C[3], ec="none", alpha=0.45))
    ax.add_patch(Rectangle((start, y4), 1.0, 0.4, fc=C[1], ec="none", alpha=0.85))
ax.annotate("", xy=(4.0, y4 - 0.25), xytext=(0, y4 - 0.25),
            arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.3))
ax.text(2.0, y4 - 0.32, "first frame waits for 3 more, then the batch runs", ha="center", va="top", fontsize=11, color=INK2)
ax.annotate("", xy=(0.6, y1 - 0.25), xytext=(0, y1 - 0.25),
            arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.3))
ax.text(0.8, y1 - 0.32, "result right away", ha="left", va="top", fontsize=11, color=INK2)
ax.text(12.3, 3.75, "grey ticks = frames arriving   blue/orange = inference   yellow = waiting",
        ha="right", fontsize=10.5, color=INK2)
ax.set_title("Batching raises throughput but adds waiting time to every frame (schematic)", loc="left")
save(fig, f"{SLUG}-batching.png")
