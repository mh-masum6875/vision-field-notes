"""Figure for detecting-model-drift-in-production.

Simulated confidence distributions, not production data. The two are built so
their means almost coincide while their shapes differ, because that is the
situation the post is warning about: the summary statistic does not move.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "detecting-model-drift-in-production"

rng = np.random.default_rng(31)
N = 60000
THRESH = 0.80


def baseline(n=N):
    """A confident cluster near the top, plus a tail down near the threshold."""
    k = rng.random(n) < 0.62
    confident = rng.beta(11.0, 2.0, n)          # piles up high
    marginal = rng.beta(2.1, 3.4, n) * 0.72     # sits low, below the threshold
    return np.where(k, confident, marginal)


base = baseline()

# The drifted month is deliberately given the SAME mean as the baseline: the
# confident cluster spreads downward and the tail fills in, which is the case
# the post warns about, where the summary statistic reports nothing.
m = base.mean()
a_drift = 4.4
b_drift = a_drift * (1 - m) / m                 # Beta mean a/(a+b) == m
drift = rng.beta(a_drift, b_drift, N)

bins = np.linspace(0, 1, 70)
fig, axs = plt.subplots(1, 2, figsize=(12.8, 5.6),
                        gridspec_kw={"width_ratios": [1.35, 1.0]})

ax = axs[0]
ax.hist(base, bins=bins, color=C[0], alpha=0.62, label="baseline month")
ax.hist(drift, bins=bins, color=C[1], alpha=0.62, label="six months later")
for vals, col in [(base, C[0]), (drift, C[1])]:
    ax.axvline(vals.mean(), color=col, lw=2.6, ls="--")
ax.axvline(THRESH, color=INK, lw=2.0)
ax.text(THRESH + 0.012, ax.get_ylim()[1] * 0.97, "0.80", rotation=90, va="top",
        fontsize=11, color=INK)
ax.annotate(f"the two means: {base.mean():.3f} and {drift.mean():.3f}",
            xy=(base.mean(), ax.get_ylim()[1] * 0.52),
            xytext=(0.045, ax.get_ylim()[1] * 0.80), fontsize=12, color=INK,
            weight="bold",
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.7,
                            connectionstyle="arc3,rad=-0.2"))
ax.set_xlabel("detection confidence")
ax.set_ylabel("detections")
ax.set_yticks([])
ax.set_xlim(0, 1)
ax.set_title("The shape moves; the mean does not", fontsize=12.5, loc="left")
ax.legend(fontsize=10.8, loc="upper left")

# ---- the two numbers you could have watched
ax = axs[1]
hi_base = (base >= THRESH).mean() * 100
hi_drift = (drift >= THRESH).mean() * 100
mean_move = abs(base.mean() - drift.mean()) / base.mean() * 100
hi_move = (hi_base - hi_drift) / hi_base * 100

bars = ax.bar([0, 1], [mean_move, hi_move], 0.58, color=[MUTED, CRIT])
for x, v, lab in [(0, mean_move, "mean\nconfidence"),
                  (1, hi_move, f"fraction above {THRESH:.2f}")]:
    ax.text(x, v + 2.2, f"{v:.0f}%", ha="center", fontsize=15, weight="bold", color=INK)
ax.set_xticks([0, 1], ["mean confidence", f"fraction above {THRESH:.2f}"], fontsize=11.5)
ax.set_ylabel("how far the number moved (%)")
ax.set_ylim(0, max(hi_move) * 1.25 if hasattr(hi_move, "__len__") else hi_move * 1.25)
ax.set_title("Same drift, two ways of watching for it", fontsize=12.5, loc="left")
ax.grid(axis="x", visible=False)
ax.text(0, 8.5, "invisible", ha="center", fontsize=12, color=MUTED, weight="bold")
ax.text(1, hi_move * 0.45, "obvious", ha="center", fontsize=12, color="white",
        weight="bold")

fig.suptitle("A mean that barely moves can hide half your confident detections",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.925,
         "Simulated. The drifted month is constructed to have the same mean as the baseline, "
         "so the only thing that changes is the shape.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-confidence-shape.png")

print(f"mean: {base.mean():.4f} -> {drift.mean():.4f}  ({mean_move:.1f}% move)")
print(f"fraction >= {THRESH}: {hi_base:.1f}% -> {hi_drift:.1f}%  ({hi_move:.1f}% move)")
