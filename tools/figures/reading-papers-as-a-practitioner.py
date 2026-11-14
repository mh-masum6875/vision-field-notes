"""Figure for reading-papers-as-a-practitioner.

Arithmetic on a reading budget, not a study. The survival rates are a working
assumption, stated on the figure; the time totals follow from them.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "reading-papers-as-a-practitioner"

ARRIVE = 30            # papers worth a glance in a week
#        label                    minutes each   fraction kept
PASSES = [("Pass 1\ntitle, abstract,\nmain figure, results", 5, 0.17),
          ("Pass 2\nmethod, baselines,\nablations, cost", 30, 0.40),
          ("Pass 3\nreproduce it on\nyour own data", 180, 0.50)]

counts = [ARRIVE]
for _, _, keep in PASSES:
    counts.append(max(1, round(counts[-1] * keep)))

fig, axs = plt.subplots(1, 2, figsize=(12.8, 5.8),
                        gridspec_kw={"width_ratios": [1.45, 1.0]})

# ---- the funnel
ax = axs[0]
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
cols = [C[0], C[2], C[3]]
y = 8.9
ax.add_patch(FancyBboxPatch((0.6, y - 0.75), 8.8, 0.95,
                            boxstyle="round,pad=0.05,rounding_size=0.14",
                            fc="#eef3fb", ec=INK2, lw=1.6))
ax.text(5.0, y - 0.28, f"{ARRIVE} papers arrive this week", ha="center", va="center",
        fontsize=13, weight="bold", color=INK)

for i, ((label, mins, keep), col) in enumerate(zip(PASSES, cols)):
    top = y - 1.25 - i * 2.45
    width = 8.8 * (counts[i] / ARRIVE) ** 0.38
    ax.add_patch(FancyArrowPatch((5.0, top + 0.42), (5.0, top), arrowstyle="-|>",
                                 mutation_scale=16, color=INK2, lw=1.7))
    ax.add_patch(FancyBboxPatch((5.0 - width / 2, top - 1.55), width, 1.55,
                                boxstyle="round,pad=0.05,rounding_size=0.14",
                                fc=col, alpha=0.22, ec=col, lw=1.8))
    ax.text(5.0, top - 0.78, label, ha="center", va="center", fontsize=11.2,
            color=INK, linespacing=1.3)
    spent = counts[i] * mins
    ax.text(5.0 + width / 2 + 0.25, top - 0.78,
            f"{counts[i]} × {mins} min\n= {spent / 60:.1f} h",
            ha="left", va="center", fontsize=11.2, color=col, weight="bold",
            linespacing=1.35)

ax.text(5.0, 0.55, f"{counts[-1]} paper actually tried", ha="center", fontsize=12.6,
        weight="bold", color=GOOD)

# ---- the time budget, against reading everything properly
ax = axs[1]
triage = sum(c * m for c, (_, m, _) in zip(counts[:2], PASSES[:2])) / 60
everything = ARRIVE * 45 / 60
bars = ax.bar([0, 1], [triage, everything], 0.58, color=[GOOD, CRIT])
for x, v in zip([0, 1], [triage, everything]):
    ax.text(x, v + 0.7, f"{v:.1f} h", ha="center", fontsize=15, weight="bold", color=INK)
ax.set_xticks([0, 1], ["passes 1 and 2", f"read all {ARRIVE}\nproperly"], fontsize=11.8)
ax.set_ylabel("hours a week")
ax.set_ylim(0, everything * 1.22)
ax.set_title("Same reading list, two budgets", fontsize=12.5, loc="left")
ax.grid(axis="x", visible=False)

fig.suptitle("The three passes are a filter, and the filter is the point",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.925,
         f"Assumes {int(PASSES[0][2]*100)}% survive pass 1, {int(PASSES[1][2]*100)}% of "
         f"those survive pass 2, and half of those are worth reproducing. "
         f"Swap your own rates in.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.text(0.52, 0.015, "Pass 3 is occasional rather than weekly, so it is left out of "
         "the budget on the right.", ha="left", fontsize=10.8, color=INK2)
fig.tight_layout(rect=[0, 0.045, 1, 0.885])
save(fig, f"{SLUG}-three-passes.png")

print("counts through the funnel:", counts)
print(f"triage total {triage:.1f} h   reading everything {everything:.1f} h")
