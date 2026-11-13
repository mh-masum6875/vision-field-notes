"""Figures for multi-camera-handover-and-reid.

Both panels use simulated similarity scores, not a benchmark. The overlap
between the two distributions is the point; the exact numbers are illustrative.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "multi-camera-handover-and-reid"

rng = np.random.default_rng(5)
N = 60000

# cosine similarity: same person across cameras, and different people
same = np.clip(rng.beta(7.0, 3.1, N), 0, 1)
diff = np.clip(rng.beta(3.4, 6.2, N), 0, 1)

THRESH = 0.62
bins = np.linspace(0, 1, 90)

fig, axs = plt.subplots(1, 2, figsize=(12.2, 5.0))

# ---- panel 1: the two distributions overlap, and the threshold has to sit in it
ax = axs[0]
ax.hist(diff, bins=bins, color=C[1], alpha=0.72, label="different people")
ax.hist(same, bins=bins, color=C[0], alpha=0.72, label="same person, two cameras")
ax.axvline(THRESH, color=INK, lw=2, ls="--")
ax.text(THRESH + 0.012, ax.get_ylim()[1] * 0.97, f"threshold {THRESH}", rotation=90,
        va="top", fontsize=11, color=INK)

missed = (same < THRESH).mean() * 100
false_m = (diff >= THRESH).mean() * 100
top = ax.get_ylim()[1]

# label each distribution on itself rather than in a legend
ax.text(0.30, top * 0.88, "different people", color=C[1], fontsize=12, weight="bold", ha="center")
ax.text(0.80, top * 0.72, "same person,\ntwo cameras", color=C[0], fontsize=12, weight="bold",
        ha="center", linespacing=1.3)

ax.annotate(f"{missed:.0f}% of true pairs\nfall below the line",
            xy=(0.50, top * 0.17), xytext=(0.015, top * 0.46), fontsize=11.5,
            color=C[0], weight="bold", linespacing=1.3,
            arrowprops=dict(arrowstyle="->", color=C[0], lw=1.6,
                            connectionstyle="arc3,rad=-0.2"))
ax.annotate(f"{false_m:.0f}% of wrong pairs\nsit above it",
            xy=(0.70, top * 0.06), xytext=(0.69, top * 0.32), fontsize=11.5,
            color=C[1], weight="bold", linespacing=1.3,
            arrowprops=dict(arrowstyle="->", color=C[1], lw=1.6,
                            connectionstyle="arc3,rad=0.2"))
ax.set_xlabel("appearance similarity (cosine)")
ax.set_ylabel("pairs")
ax.set_yticks([])
ax.set_ylim(0, top * 1.12)
ax.set_title("Appearance alone: the distributions overlap", fontsize=12.5, loc="left")

# ---- panel 2: shrinking the candidate pool is worth more than a better model
ax = axs[1]
pools = np.array([200, 60, 12])
labels = ["every person\nseen today\n(200)", "+ time window\n(60)", "+ time and\ntopology (12)"]
p_same_pass = (same >= THRESH).mean()
# expected wrong candidates above threshold, and the resulting precision
wrong_above = pools * (diff >= THRESH).mean()
precision = p_same_pass / (p_same_pass + wrong_above) * 100

bars = ax.bar(np.arange(3), precision, 0.58, color=[CRIT, WARN, GOOD])
for b, v, w in zip(bars, precision, wrong_above):
    cx = b.get_x() + b.get_width() / 2
    ax.text(cx, v + 3.0, f"{v:.0f}%", ha="center", fontsize=14, weight="bold", color=INK)
    ax.text(cx, v + 12.0, f"{w:.1f} wrong candidates\nabove {THRESH}", ha="center",
            fontsize=10.5, color=INK2, linespacing=1.3)
ax.set_xticks(np.arange(3), labels, fontsize=10.5)
ax.set_ylabel("matches that are correct (%)")
ax.set_ylim(0, 86)
ax.set_title("Same model, same threshold, smaller candidate pool", fontsize=12.5, loc="left")

fig.suptitle("Re-ID accuracy is mostly decided before the model runs",
             x=0.01, ha="left", fontsize=14.5, weight="bold")
fig.tight_layout()
save(fig, f"{SLUG}-overlap-and-gating.png")

print(f"missed={missed:.1f}%  false={false_m:.1f}%  precision={precision.round(1)}")
