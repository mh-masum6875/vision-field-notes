"""Figure for research-code-to-production-code.

Illustrative proportions, not a line count from a real repository. The method
block is deliberately the same size in both columns, because that is the
claim: the research code survives the move, it just stops being most of it.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "research-code-to-production-code"

#  part                              research  production
PARTS = [
    ("the method itself",                 100, 100, C[1]),
    ("handling bad input",                  4,  70, C[0]),
    ("running unattended\nand recovering",  0,  85, C[2]),
    ("configuration",                       6,  45, C[3]),
    ("tests",                               8,  80, C[5]),
    ("logging and metrics",                 5,  60, C[6]),
]

fig, axs = plt.subplots(1, 2, figsize=(12.4, 6.4),
                        gridspec_kw={"width_ratios": [1.25, 1.0]})

# ---- stacked columns
ax = axs[0]
for col_i, key in enumerate([1, 2]):
    bottom = 0
    for name, r, p, colr in PARTS:
        v = (r, p)[key - 1]
        if v == 0:
            continue
        ax.bar(col_i, v, 0.56, bottom=bottom, color=colr,
               ec="white", lw=1.4)
        if v >= 40:
            ax.text(col_i, bottom + v / 2, name.split("\n")[0], ha="center",
                    va="center", fontsize=10.2, color="white", weight="bold")
        bottom += v

totals = [sum(r for _, r, _, _ in PARTS), sum(p for _, _, p, _ in PARTS)]
for i, t in enumerate(totals):
    ax.text(i, t + 12, f"{t}", ha="center", fontsize=14, weight="bold", color=INK)

ax.set_xticks([0, 1], ["research code", "production code"], fontsize=12.5)
ax.set_ylabel("relative size of the codebase")
ax.set_ylim(0, max(totals) * 1.15)
ax.set_yticks([])
ax.set_title("The method is the same size in both", fontsize=12.6, loc="left")
ax.grid(axis="x", visible=False)

# ---- the share the method occupies
ax = axs[1]
shares = [100 / totals[0] * 100, 100 / totals[1] * 100]
bars = ax.bar([0, 1], shares, 0.56, color=[C[1], C[1]], alpha=0.9)
for i, v in enumerate(shares):
    ax.text(i, v + 2.2, f"{v:.0f}%", ha="center", fontsize=16, weight="bold", color=INK)
ax.set_xticks([0, 1], ["research code", "production code"], fontsize=12.5)
ax.set_ylabel("share of the codebase that is the method")
ax.set_ylim(0, 100)
ax.set_title("The share it occupies is not", fontsize=12.6, loc="left")
ax.grid(axis="x", visible=False)
ax.annotate("", xy=(1, shares[1] + 1), xytext=(0, shares[0] - 1),
            arrowprops=dict(arrowstyle="->", color=INK2, lw=2.0,
                            connectionstyle="arc3,rad=0.22"))
ax.text(0.5, (shares[0] + shares[1]) / 2 + 12, "same code,\nsmaller fraction",
        ha="center", fontsize=12, color=INK2, weight="bold", linespacing=1.35)

fig.legend(handles=[Patch(fc=c, label=n.replace("\n", " ")) for n, _, _, c in PARTS],
           loc="lower center", bbox_to_anchor=(0.5, -0.005), ncol=3, fontsize=10.6,
           frameon=False)

fig.suptitle("Moving to production does not replace the research code; it surrounds it",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.928,
         "Illustrative proportions, not a line count. The point is the ratio, not the numbers.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0.11, 1, 0.885])
save(fig, f"{SLUG}-what-surrounds-it.png")

print(f"research total {totals[0]}, production total {totals[1]}")
print(f"method share: {shares[0]:.0f}% -> {shares[1]:.0f}%")
