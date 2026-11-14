"""Figure for reproducible-training-runs.

Simulated runs, not measurements. The spread is set to something typical for a
detector fine-tune; the point is the comparison, which is why one run against
one run cannot answer the question whatever the real spread turns out to be.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "reproducible-training-runs"

rng = np.random.default_rng(180)   # a draw where one run each is misleading
BASE, SPREAD = 54.0, 0.62          # mAP50-95, and run-to-run standard deviation
N = 8

a = rng.normal(BASE, SPREAD, N)
b = rng.normal(BASE - 0.45, SPREAD, N)      # genuinely a touch worse
single_a, single_b = a[0], b[0]

fig, axs = plt.subplots(1, 2, figsize=(12.8, 5.6))

# ---- one run each: the usual comparison
ax = axs[0]
ax.scatter([0], [single_a], s=190, color=C[0], zorder=5, label="old config")
ax.scatter([1], [single_b], s=190, color=C[1], zorder=5, label="new config")
ax.plot([0, 1], [single_a, single_b], color=INK2, lw=1.6, ls="--", zorder=3)
gap = single_a - single_b
ax.annotate(f"{gap:+.1f} points\n“the new one is worse”",
            xy=(0.5, (single_a + single_b) / 2), xytext=(0.5, BASE + 1.45),
            ha="center", fontsize=12.5, color=CRIT, weight="bold", linespacing=1.4,
            arrowprops=dict(arrowstyle="->", color=CRIT, lw=1.8))
ax.set_xticks([0, 1], ["old config\n1 run", "new config\n1 run"], fontsize=11.5)
ax.set_xlim(-0.55, 1.55)
ax.set_ylim(BASE - 2.4, BASE + 2.4)
ax.set_ylabel("mAP50-95")
ax.set_title("What the comparison usually looks like", fontsize=12.5, loc="left")

# ---- the same configs, run eight times each
ax = axs[1]
for i, (vals, col, name) in enumerate([(a, C[0], "old config"), (b, C[1], "new config")]):
    jitter = rng.uniform(-0.13, 0.13, N)
    ax.scatter(np.full(N, i) + jitter, vals, s=95, color=col, alpha=0.85, zorder=5)
    ax.hlines(vals.mean(), i - 0.30, i + 0.30, color=col, lw=3, zorder=6)
    ax.add_patch(plt.Rectangle((i - 0.30, vals.mean() - vals.std()), 0.60,
                               2 * vals.std(), fc=col, alpha=0.14, zorder=2))
    ax.text(i + 0.37, vals.mean(), f"mean {vals.mean():.2f}\nsd {vals.std():.2f}",
            va="center", fontsize=11, color=col, weight="bold", linespacing=1.35)

ax.scatter([0], [single_a], s=190, facecolors="none", edgecolors=INK, linewidths=2.4,
           zorder=7)
ax.scatter([1], [single_b], s=190, facecolors="none", edgecolors=INK, linewidths=2.4,
           zorder=7)
ax.text(0.5, BASE + 1.9, "the two circled runs are the pair from the left",
        ha="center", fontsize=11.3, color=INK2, style="italic")

ax.set_xticks([0, 1], ["old config\n8 runs", "new config\n8 runs"], fontsize=11.5)
ax.set_xlim(-0.55, 1.75)
ax.set_ylim(BASE - 2.4, BASE + 2.4)
ax.set_title("The same two configs, retrained", fontsize=12.5, loc="left")

real = a.mean() - b.mean()
fig.suptitle(f"Run-to-run spread is {SPREAD:.1f} points, so a {gap:.1f}-point gap "
             f"tells you nothing",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.925,
         "Simulated runs with a typical fine-tuning spread. Measure yours before "
         "trusting any single comparison.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-run-to-run-spread.png")

print(f"single-run gap: {gap:+.2f}   true difference of means: {real:+.2f}")
print(f"old: mean {a.mean():.2f} sd {a.std():.2f}   new: mean {b.mean():.2f} sd {b.std():.2f}")
print(f"old range {a.min():.2f}..{a.max():.2f}   new range {b.min():.2f}..{b.max():.2f}")
