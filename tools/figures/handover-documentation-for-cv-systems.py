"""Figure for handover-documentation-for-cv-systems.

Two folder listings, and the four questions the post says a successor arrives
with. Nothing measured; it is the shape of a handover, drawn.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "handover-documentation-for-cv-systems"

BAD = [
    ("final/", 0, "dir"),
    ("best.pt", 1, "bad"),
    ("best_v2.pt", 1, "bad"),
    ("best_v2_FINAL.pt", 1, "bad"),
    ("config.yaml", 1, "plain"),
    ("notes.txt", 1, "bad"),
]

GOOD_TREE = [
    ("handover/", 0, "dir"),
    ("01-system-overview.pdf", 1, "plain"),
    ("02-runbook.md", 1, "good"),
    ("03-camera-and-zone-guide.md", 1, "plain"),
    ("04-retraining.md", 1, "plain"),
    ("models/", 1, "dir"),
    ("prod-2026-09-14.onnx", 2, "good"),
    ("prod-2026-09-14.md", 2, "good"),
    ("config/", 1, "dir"),
    ("cameras.yaml", 2, "plain"),
    ("thresholds.yaml", 2, "plain"),
    ("data/", 1, "dir"),
    ("dataset-v7.md", 2, "plain"),
]

QUESTIONS = [
    ("Is it running?", "02-runbook.md"),
    ("This alert looks wrong.\nWhere do I look?", "02-runbook.md"),
    ("A camera was replaced.\nWhat do I change?", "03-camera-and-zone-guide.md"),
    ("Which model is live,\nand how was it trained?", "prod-2026-09-14.md"),
]

fig, axs = plt.subplots(1, 3, figsize=(15.2, 6.6),
                        gridspec_kw={"width_ratios": [1.0, 1.25, 1.25]})

# ---- the four questions a successor arrives with
ax = axs[0]
ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.text(0.02, 0.965, "What they arrive with", fontsize=13.5, weight="bold", color=INK,
        va="top")
for i, (q, _) in enumerate(QUESTIONS):
    y = 0.80 - i * 0.205
    ax.add_patch(FancyBboxPatch((0.02, y - 0.115), 0.94, 0.155,
                                boxstyle="round,pad=0.012,rounding_size=0.03",
                                fc="#eef3fb", ec=C[0], lw=1.5))
    ax.text(0.5, y - 0.038, q, ha="center", va="center", fontsize=11.8, color=INK,
            linespacing=1.35)


def tree(ax, rows, title, subtitle, sub_col):
    ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.0, 0.965, title, fontsize=13.5, weight="bold", color=INK, va="top")
    ax.text(0.0, 0.905, subtitle, fontsize=11.6, color=sub_col, va="top", weight="bold")
    for i, (name, depth, kind) in enumerate(rows):
        y = 0.825 - i * 0.0605
        col = {"dir": INK, "good": "#0b5c22", "bad": CRIT, "plain": INK2}[kind]
        wgt = "bold" if kind in ("dir", "good") else "normal"
        mark = {"dir": "", "good": "", "bad": "", "plain": ""}[kind]
        ax.text(0.03 + depth * 0.075, y, name, fontsize=12.2, color=col,
                family="DejaVu Sans Mono", weight=wgt, va="center")
        if kind == "bad":
            ax.text(0.80, y, "?", fontsize=13, color=CRIT, weight="bold", va="center")


tree(axs[1], BAD, "What they usually get",
     "nothing here answers any of the four", CRIT)
tree(axs[2], GOOD_TREE, "What to leave instead",
     "every question has one file", "#0b5c22")

fig.suptitle("A handover is finished when someone else can answer these without you",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.945])
save(fig, f"{SLUG}-what-to-leave.png")
print("rendered handover figure")
