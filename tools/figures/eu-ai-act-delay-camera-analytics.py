"""Figure for eu-ai-act-delay-camera-analytics.

Real dates from the AI Act and from Regulation (EU) 2026/1744, as described in
the post. Nothing here is simulated. The point is which obligations moved and
which did not.
"""
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyArrowPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "eu-ai-act-delay-camera-analytics"
D = dt.date

# (date, label, row, depth, colour, moved-from)
EVENTS = [
    (D(2025, 2, 2),  "Article 5 prohibitions apply\nscraped face databases, emotion\nrecognition at work, live biometric ID",
     1, 0.50, CRIT, None),
    (D(2026, 12, 2), "New prohibitions apply\nnon-consensual intimate\nimagery, CSAM",
     1, 1.35, CRIT, None),
    (D(2027, 12, 2), "Annex III high-risk duties\nbiometrics, critical infrastructure,\neducation, employment",
     -1, 1.35, WARN, D(2026, 8, 2)),
    (D(2028, 8, 2),  "Annex I high-risk duties\nsafety components of\nregulated products",
     -1, 0.50, WARN, None),
]

fig, ax = plt.subplots(figsize=(13.2, 5.8))
x0, x1 = D(2024, 10, 1), D(2029, 2, 1)
ax.set_xlim(x0, x1)
ax.set_ylim(-2.35, 2.35)
ax.axhline(0, color=INK2, lw=2.4, zorder=2)

today = D(2026, 11, 13)
ax.axvline(today, color=C[0], lw=1.8, ls="--", zorder=3)
ax.text(today, -2.22, "  today", color=C[0], fontsize=11.5, weight="bold", va="bottom")

for date, label, row, depth, col, moved in EVENTS:
    y = depth * row
    ax.plot([date, date], [0, y], color=col, lw=2.0, zorder=4)
    ax.plot([date], [0], marker="o", ms=11, mfc=col, mec="white", mew=2, zorder=5)
    va = "bottom" if row > 0 else "top"
    ax.text(date, y + (0.14 if row > 0 else -0.14), label, ha="center", va=va,
            fontsize=10.8, color=INK, linespacing=1.4, zorder=6,
            bbox=dict(fc="white", ec=col, lw=1.4, boxstyle="round,pad=0.42"))
    ax.text(date, 0.14 * -row, date.strftime("%-d %b %Y"), ha="center",
            va="top" if row > 0 else "bottom", fontsize=10, color=INK2, zorder=6)

    if moved:
        ax.plot([moved], [0], marker="o", ms=9, mfc="white", mec=MUTED, mew=2, zorder=5)
        ax.text(moved, -0.12, "was\n2 Aug 2026", ha="center", va="top", fontsize=10,
                color=MUTED, linespacing=1.3, zorder=6)
        ax.add_patch(FancyArrowPatch((moved, 0.04), (date, 0.04),
                                     arrowstyle="-|>", mutation_scale=18,
                                     color=WARN, lw=2.0, ls=(0, (4, 2)),
                                     connectionstyle="arc3,rad=-0.22", zorder=4))
        mid = moved + (date - moved) / 2
        ax.text(mid, 0.72, "delayed 16 months", ha="center", fontsize=11.5,
                color=WARN, weight="bold", zorder=6)

ax.text(0.004, 0.96, "NOT delayed", transform=ax.transAxes, fontsize=12.5,
        weight="bold", color=CRIT, va="top")
ax.text(0.004, 0.045, "delayed by the omnibus", transform=ax.transAxes, fontsize=12.5,
        weight="bold", color=WARN, va="bottom")

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_yticks([])
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color=GRID, lw=0.9)
for sp in ("left", "right", "top"):
    ax.spines[sp].set_visible(False)

fig.suptitle("The AI Act delay moved the high-risk duties, not the prohibitions",
             x=0.01, ha="left", fontsize=15, weight="bold")
fig.text(0.01, 0.925,
         "Dates from the AI Act and from Regulation (EU) 2026/1744, in force 27 July 2026. "
         "Not legal advice.",
         ha="left", va="top", fontsize=11.5, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-timeline.png")

gap = (D(2027, 12, 2).year - D(2026, 8, 2).year) * 12 + (12 - 8)
print("delay in months:", gap)
