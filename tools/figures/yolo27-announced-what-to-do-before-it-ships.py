"""Figure for yolo27-announced-what-to-do-before-it-ships.

A decision flow, not data. It is the plan from the post drawn as the gates it
actually is: two of them end the evaluation, and both are cheap to reach.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "yolo27-announced-what-to-do-before-it-ships"

fig, ax = plt.subplots(figsize=(10.6, 9.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 15.2)
ax.axis("off")

BW, BH = 5.0, 1.02
CX = 3.5


def box(y, text, fc="#ffffff", ec=INK2, tc=INK, w=BW, cx=CX, size=11.6, weight="normal"):
    ax.add_patch(FancyBboxPatch((cx - w / 2, y - BH / 2), w, BH,
                                boxstyle="round,pad=0.06,rounding_size=0.16",
                                fc=fc, ec=ec, lw=1.7, zorder=3))
    ax.text(cx, y, text, ha="center", va="center", fontsize=size, color=tc,
            weight=weight, linespacing=1.35, zorder=4)


def arrow(y0, y1, cx=CX, label=None, color=INK2):
    ax.add_patch(FancyArrowPatch((cx, y0), (cx, y1), arrowstyle="-|>",
                                 mutation_scale=17, color=color, lw=1.9, zorder=2))
    if label:
        ax.text(cx + 0.16, (y0 + y1) / 2, label, ha="left", va="center",
                fontsize=10.8, color=color, weight="bold", zorder=4)


def stop(y, text):
    ax.add_patch(FancyBboxPatch((7.05, y - BH / 2), 2.75, BH,
                                boxstyle="round,pad=0.06,rounding_size=0.16",
                                fc="#fdecec", ec=CRIT, lw=1.8, zorder=3))
    ax.text(8.42, y, text, ha="center", va="center", fontsize=11.4, color=CRIT,
            weight="bold", linespacing=1.3, zorder=4)
    ax.add_patch(FancyArrowPatch((CX + BW / 2, y), (7.05, y), arrowstyle="-|>",
                                 mutation_scale=16, color=CRIT, lw=1.8, zorder=2))


ys = [14.4, 12.9, 11.4, 9.9, 8.4, 6.9, 5.4, 3.9, 2.4, 0.95]

box(ys[0], "YOLO27 announced", fc="#eef3fb", ec=C[0], size=12.4, weight="bold")
arrow(ys[0] - BH / 2, ys[1] + BH / 2)

box(ys[1], "Change nothing in production", fc="#eaf6ee", ec=GOOD, tc="#0b5c22",
    size=12.2, weight="bold")
arrow(ys[1] - BH / 2, ys[2] + BH / 2, label="wait for release")

box(ys[2], "Does the licence fit your product?", fc="#fff8e8", ec=WARN, weight="bold")
stop(ys[2], "no\nstop here")
arrow(ys[2] - BH / 2, ys[3] + BH / 2, label="yes")

box(ys[3], "Fine-tune on your data\nsame dataset version, budget, image size")
arrow(ys[3] - BH / 2, ys[4] + BH / 2)

box(ys[4], "Compare on your test set\nyour operating threshold, per class, by size")
arrow(ys[4] - BH / 2, ys[5] + BH / 2)

box(ys[5], "Is the gain bigger than\nrun-to-run noise?", fc="#fff8e8", ec=WARN,
    weight="bold")
stop(ys[5], "no\nstay put")
arrow(ys[5] - BH / 2, ys[6] + BH / 2, label="yes")

box(ys[6], "Export and time it on the target device")
arrow(ys[6] - BH / 2, ys[7] + BH / 2)

box(ys[7], "Run the replay set at the event level")
arrow(ys[7] - BH / 2, ys[8] + BH / 2)

box(ys[8], "Roll out in stages", fc="#eef3fb", ec=C[0], size=12.2, weight="bold")

ax.text(CX, ys[9] + 0.30,
        "The licence gate costs nothing to check and ends it outright.\n"
        "Staying on a model that works is a result, not a failure.",
        ha="center", va="center", fontsize=11.6, color=INK2, linespacing=1.5)

fig.suptitle("Two gates decide this, and neither is the mAP number",
             x=0.015, ha="left", fontsize=15, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.962])
save(fig, f"{SLUG}-decision-flow.png")
print("rendered decision flow")
