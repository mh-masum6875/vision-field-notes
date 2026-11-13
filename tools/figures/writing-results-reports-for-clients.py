"""Figure for writing-results-reports-for-clients.

Two report structures, and the line most readers stop at. Not data: it is the
argument of the post drawn so the cost of ordering is visible at a glance.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "writing-results-reports-for-clients"

PAPER = [
    ("Method", "how the system works"),
    ("Dataset", "sources, splits, label process"),
    ("Metrics", "mAP50-95, precision-recall curve"),
    ("Error analysis", "confusion matrix, per-class table"),
    ("Conclusion", "whether it met the target"),
]
REPORT = [
    ("The answer", "41 of 44 entries caught, 1.5 false\nalerts per camera per day, target met"),
    ("What was tested", "48 hours, cameras 3 and 7, day and night"),
    ("Results in their units", "misses and false alerts, not mAP"),
    ("What we recommend", "start the pilot, add a light at the far end"),
    ("Appendix", "curves, matrices, everything else"),
]

fig, axs = plt.subplots(1, 2, figsize=(13.4, 7.6))
BH, GAP = 1.0, 0.26


def column(ax, rows, title, title_col, answer_row, verdict, verdict_col):
    ax.set_xlim(0, 10); ax.set_ylim(0, 8.5)
    ax.axis("off")
    ax.text(0.1, 8.32, title, fontsize=13.8, weight="bold", color=title_col, va="top")
    y = 7.55
    for i, (head, note) in enumerate(rows):
        is_answer = i == answer_row
        ax.add_patch(FancyBboxPatch((0.1, y - BH), 9.0, BH,
                                    boxstyle="round,pad=0.04,rounding_size=0.1",
                                    fc="#eaf6ee" if is_answer else "#ffffff",
                                    ec=GOOD if is_answer else GRID,
                                    lw=2.0 if is_answer else 1.5, zorder=3))
        ax.text(0.42, y - 0.33, head, fontsize=12.2, weight="bold",
                color=INK, va="center", zorder=4)
        ax.text(0.42, y - 0.72, note, fontsize=10.2, color=INK2, va="center",
                linespacing=1.3, zorder=4)
        if i == 0:
            stop = y - BH - GAP / 2
            ax.plot([-0.25, 9.6], [stop, stop], color=CRIT, lw=2.2, ls="--", zorder=5)
            ax.text(9.55, stop - 0.17, "most readers stop here", ha="right", va="top",
                    fontsize=11.2, color=CRIT, weight="bold", zorder=6)
        y -= BH + GAP
    ax.text(5.0, 0.45, verdict, ha="center", fontsize=12.4, weight="bold",
            color=verdict_col, linespacing=1.4)


column(axs[0], PAPER, "Written like a paper", CRIT, answer_row=4,
       verdict="They read how it works,\nand still ask “so, does it work?”", verdict_col=CRIT)
column(axs[1], REPORT, "Written for a decision", "#0b5c22", answer_row=0,
       verdict="They can stop after one paragraph\nand still decide correctly", verdict_col="#0b5c22")

fig.suptitle("Same findings, same numbers, opposite order",
             x=0.01, ha="left", fontsize=15.5, weight="bold")
fig.text(0.01, 0.925,
         "The green block is the conclusion. Only its position changes between the two.",
         ha="left", va="top", fontsize=11.5, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.895])
save(fig, f"{SLUG}-answer-first.png")
print("rendered report structure figure")
