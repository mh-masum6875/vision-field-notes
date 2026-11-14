"""Figure for video-compression-and-detection-accuracy.

Simulated curves, not a benchmark. The shape is the claim the post makes: a
cliff rather than a slope, arriving at different bitrates for different object
sizes, and flat above it so extra bits buy nothing.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "video-compression-and-detection-accuracy"

bitrate = np.linspace(0.3, 12, 500)


def curve(ceiling, knee, sharpness):
    """Flat at the top, falling away below the knee."""
    return ceiling / (1 + np.exp(-sharpness * (np.log(bitrate) - np.log(knee))))


SIZES = [
    ("large objects (vehicles up close)", 0.94, 0.55, 3.4, C[2]),
    ("medium objects (people at 15 m)",   0.89, 0.90, 3.2, C[0]),
    ("small objects (people at 40 m)",    0.78, 1.90, 2.8, C[1]),
]

fig, axs = plt.subplots(1, 2, figsize=(12.8, 5.6),
                        gridspec_kw={"width_ratios": [1.35, 1.0]})

ax = axs[0]
for name, ceil, knee, sharp, col in SIZES:
    y = curve(ceil, knee, sharp) * 100
    ax.plot(bitrate, y, lw=2.6, color=col, label=name)
    # mark where it has lost a tenth of its ceiling
    target = ceil * 0.9 * 100
    i = int(np.argmin(np.abs(y - target)))
    ax.plot([bitrate[i]], [y[i]], marker="o", ms=9, mfc=col, mec="white", mew=1.8,
            zorder=6)

INSTALLED = 2.0
ax.axvline(INSTALLED, color=INK, lw=2.0, ls="--")
ax.text(INSTALLED * 1.06, 12, "what the installer\nleft configured", fontsize=11.4,
        color=INK, weight="bold", linespacing=1.35)

small_at = curve(0.78, 1.90, 2.8)[np.argmin(np.abs(bitrate - INSTALLED))] * 100
large_at = curve(0.94, 0.55, 3.4)[np.argmin(np.abs(bitrate - INSTALLED))] * 100
ax.annotate(f"at {INSTALLED:g} Mbps the large objects are fine ({large_at:.0f}%)\n"
            f"and the small ones are not ({small_at:.0f}%)",
            xy=(INSTALLED, small_at), xytext=(4.3, 46), fontsize=11.8, color=CRIT,
            weight="bold", linespacing=1.4,
            arrowprops=dict(arrowstyle="->", color=CRIT, lw=1.8,
                            connectionstyle="arc3,rad=0.22"))

ax.set_xscale("log")
ax.set_xticks([0.5, 1, 2, 4, 8, 12])
ax.set_xticklabels(["0.5", "1", "2", "4", "8", "12"])
ax.set_xlabel("stream bitrate (Mbps, 1080p)")
ax.set_ylabel("recall (%)")
ax.set_ylim(0, 100)
ax.set_title("The cliff is in a different place for each object size",
             fontsize=12.5, loc="left")
ax.legend(fontsize=10.6, loc="upper left")

# ---- what you lose, per object size, at the installed bitrate
ax = axs[1]
names, losses, cols = [], [], []
for name, ceil, knee, sharp, col in SIZES:
    at = curve(ceil, knee, sharp)[np.argmin(np.abs(bitrate - INSTALLED))] * 100
    names.append(name.split(" (")[0])
    losses.append(ceil * 100 - at)
    cols.append(col)
bars = ax.barh(np.arange(3)[::-1], losses, 0.6, color=cols)
for y, (v, n) in enumerate(zip(losses, names)):
    ax.text(v + 0.8, 2 - y, f"{v:.0f} point{'s' if round(v) != 1 else ''} lost", va="center", fontsize=12,
            weight="bold", color=INK)
ax.set_yticks(np.arange(3)[::-1], names, fontsize=11.5)
ax.set_xlabel(f"recall lost at {INSTALLED:g} Mbps, against the same model at 12 Mbps")
ax.set_xlim(0, max(losses) * 1.42)
ax.set_title("The frame still looks fine", fontsize=12.5, loc="left")
ax.grid(axis="y", visible=False)

fig.suptitle("Compression takes the small objects first, and nothing reports it",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.925,
         "Simulated curves with the shape the post describes. Measure your own cliff; "
         "it moves with resolution, scene motion and object size.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-bitrate-cliff.png")

for (name, ceil, knee, sharp, _), loss in zip(SIZES, losses):
    at = ceil * 100 - loss
    print(f"{name:38} ceiling {ceil*100:.0f}%  at {INSTALLED:g} Mbps {at:.0f}%  "
          f"lost {loss:.0f} pts")
