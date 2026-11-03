"""Figures for tracker-id-switches-and-double-counting. A constructed scenario, no tracker was run."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from style import C, INK, INK2, MUTED, GRID, CRIT, GOOD, WARN, save

SLUG = "tracker-id-switches-and-double-counting"
LINE = 3.6
fig, axes = plt.subplots(2, 1, figsize=(11, 5.4), sharex=True)
xs = np.linspace(0.6, 11.4, 25)
hidden = (xs > 5.9) & (xs < 7.9)
cases = [
    (axes[0], "Rule 'count every new ID seen past the line': the ID changes behind the pillar, counted twice",
     ["7" if x < 6 else "12" for x in xs], [("7", LINE, CRIT), ("12", 8.0, CRIT)]),
    (axes[1], "Rule 'count a track when it crosses the line', plus a short re-link window: counted once",
     ["7"] * len(xs), [("7", LINE, GOOD)]),
]
for ax, title, ids, counts in cases:
    ax.set_xlim(0, 12); ax.set_ylim(0, 2.3); ax.set_yticks([]); ax.grid(False)
    ax.add_patch(Rectangle((6.0, 0.15), 1.8, 1.9, fc=MUTED, alpha=0.5, lw=0))
    ax.text(6.9, 1.1, "pillar", ha="center", va="center", fontsize=10.5, color="white")
    ax.axvline(LINE, color=WARN, lw=2.2)
    for x, i, h in zip(xs, ids, hidden):
        if h:
            continue
        c = C[0] if i == "7" else C[1]
        ax.add_patch(Rectangle((x - 0.17, 0.55), 0.34, 0.9, fill=False, ec=c, lw=1.6))
        ax.text(x, 1.55, i, ha="center", fontsize=9.5, color=c)
    for i, x, col in counts:
        ax.text(x + 0.12, 2.2, f"count +1 (ID {i})", fontsize=10.5, color=col, va="top")
    ax.set_title(title, loc="left", fontsize=12)
axes[1].set_xlabel("position along a corridor (yellow: counting line; the person walks left to right)")
fig.tight_layout()
save(fig, f"{SLUG}-double-count.png")
