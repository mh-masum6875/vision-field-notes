"""Figures for scaling-to-hundreds-of-camera-streams."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, CRIT, save

SLUG = "scaling-to-hundreds-of-camera-streams"


def box(ax, x, y, w, h, title, sub, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=color + "1f", ec=color, lw=1.6))
    ax.text(x + w / 2, y + h - 1.8, title, ha="center", va="top", fontsize=12.5, weight="bold", color=INK,
            linespacing=1.2)
    if sub:
        ax.text(x + w / 2, y + (h - 8) / 2, sub, ha="center", va="center", fontsize=11, color=INK2, linespacing=1.3)


def queue(ax, x, y, label):
    """Draw a small queue symbol (row of slots) centred at x, y."""
    for i in range(4):
        ax.add_patch(plt.Rectangle((x - 3 + i * 1.5, y - 1.6), 1.3, 3.2, fc=GRID, ec=INK2, lw=0.8))
    ax.text(x, y - 3.2, label, ha="center", va="top", fontsize=10.5, color=INK2)


def arrow(ax, p, q):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.5, mutation_scale=14))


# ---------------------------------------------------------------- 1. architecture
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 44); ax.axis("off")
# cameras
for i, y in enumerate([33, 27, 21, 15]):
    ax.add_patch(FancyBboxPatch((0, y), 6, 3.6, boxstyle="round,pad=0,rounding_size=0.6", fc=C[0] + "33", ec=C[0], lw=1.2))
ax.text(3, 11.5, "cameras", ha="center", va="top", fontsize=11, color=INK2)
box(ax, 10, 13, 15, 26, "Ingest\nworkers", "RTSP, decode,\nresize,\nreconnect,\nhealth", C[0])
for y in [35, 29, 23, 17]:
    arrow(ax, (6.2, y + 1.8), (9.8, y + 1.8))
queue(ax, 30, 26, "frame\nqueue")
box(ax, 36, 13, 17, 26, "Inference\nservice", "batches frames\nfrom many\ncameras on\nthe GPU", C[2])
queue(ax, 58, 26, "results\nqueue")
box(ax, 64, 13, 16, 26, "Tracking\nand rules", "per camera,\nin frame order,\nkeyed by\ncamera id", C[6])
box(ax, 85, 21, 15, 10, "Alerts and\nstorage", None, C[1])
ax.text(92.5, 19.5, "compact events,\nnot frames", ha="center", va="top", fontsize=10.5, color=INK2)
arrow(ax, (25.3, 26), (26.6, 26)); arrow(ax, (33.4, 26), (35.7, 26))
arrow(ax, (53.3, 26), (54.6, 26)); arrow(ax, (61.4, 26), (63.7, 26))
arrow(ax, (80.3, 26), (84.7, 26))
# metrics strip
ax.add_patch(FancyBboxPatch((0, 1.5), 100, 6, boxstyle="round,pad=0,rounding_size=1", fc="white", ec=MUTED, lw=1, ls="--"))
ax.text(50, 4.5, "Metrics at every stage: frames in, processed and dropped; queue depth; latency; GPU and decoder load",
        ha="center", va="center", fontsize=10.5, color=INK2)
ax.text(0, 43.5, "Each stage scales and restarts on its own; bounded queues connect them",
        ha="left", va="top", fontsize=13, weight="bold", color=ACCENT)
save(fig, f"{SLUG}-architecture.png")


# ---------------------------------------------------------------- 2. bounded vs unbounded queue under overload (illustrative)
dt = 0.1
t = np.arange(0, 300, dt)
arrive = 100.0                                            # frames per second offered
capacity = np.where((t >= 60) & (t < 150), 80.0, 120.0)   # a slowdown between 60 s and 150 s
MAXQ = 40


def simulate(bounded):
    q, lat, dropped = 0.0, [], 0.0
    for c in capacity:
        q += (arrive - c) * dt
        q = max(q, 0.0)
        if bounded and q > MAXQ:
            dropped += q - MAXQ
            q = MAXQ
        lat.append(q / c)                                  # waiting time for the newest frame
    return np.array(lat), dropped


lat_u, _ = simulate(False)
lat_b, dropped = simulate(True)
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.axvspan(60, 150, color=GRID, alpha=0.6, lw=0)
ax.text(105, 29, "inference slower than\nthe incoming frames", ha="center", va="top", fontsize=12, color=INK2)
ax.plot(t, lat_u, color=C[1], lw=2, label="Unbounded queue: every frame waits its turn")
ax.plot(t, lat_b, color=C[0], lw=2, label=f"Bounded queue ({MAXQ} frames), oldest dropped")
ax.set_xlim(0, 300); ax.set_ylim(0, 31)
ax.text(152, 23, "overload ends;\nlag drains for 90 s", fontsize=12, color=INK2, va="top")
ax.set_xlabel("Seconds")
ax.set_ylabel("Queue wait for a new frame (s)")
ax.set_title("An unbounded queue keeps the lag long after the overload ends", loc="left")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=11.5)
save(fig, f"{SLUG}-queue-overload.png")
print("max lag unbounded %.1f s, bounded %.2f s, dropped %.0f frames" % (lat_u.max(), lat_b.max(), dropped))
