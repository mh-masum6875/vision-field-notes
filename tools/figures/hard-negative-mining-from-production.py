"""Figures for hard-negative-mining-from-production. A diagram, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, WARN, save

SLUG = "hard-negative-mining-from-production"


def box(ax, x, y, w, h, color, title, sub, fill=0.14):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=1.6))
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="center", fontsize=12.5, weight="bold")
    ax.text(x + w / 2, y + (h - 0.5) / 2, sub, ha="center", va="center", fontsize=11, color=INK2, linespacing=1.3)


def arrow(ax, a, b, text=None):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4))
    if text:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.15, text, ha="center", fontsize=10.5, color=INK2)


fig, ax = plt.subplots(figsize=(11.5, 5.6))
ax.set_xlim(0, 12); ax.set_ylim(0, 6.2); ax.axis("off")
W, H = 3.0, 1.5
box(ax, 0.2, 4.3, W, H, C[1], "Alerts in production", "frame, box, score,\ncamera, time")
box(ax, 4.5, 4.3, W, H, C[3], "Operator feedback", "one click:\ntrue or false alert")
box(ax, 8.8, 4.3, W, H, C[6], "Review and dedupe", "confirm the label,\ndrop near-duplicates")
box(ax, 8.8, 1.0, W, H, C[0], "Training set", "add as background\nor with correct labels")
box(ax, 4.5, 1.0, W, H, C[2], "Retrain and evaluate", "fixed test set:\nfalse alarms AND recall")
box(ax, 0.2, 1.0, W, H, C[5], "Deploy, per camera", "staged rollout,\nwatch alert rates")
arrow(ax, (3.2, 5.05), (4.5, 5.05))
arrow(ax, (7.5, 5.05), (8.8, 5.05))
arrow(ax, (10.3, 4.3), (10.3, 2.5))
ax.text(10.45, 3.4, "most go here", fontsize=10.5, color=INK2)
arrow(ax, (8.8, 1.75), (7.5, 1.75))
arrow(ax, (4.5, 1.75), (3.2, 1.75))
arrow(ax, (1.7, 2.5), (1.7, 4.3))
ax.annotate("", xy=(6.0, 2.5), xytext=(9.4, 4.3),
            arrowprops=dict(arrowstyle="-|>", color=WARN, lw=1.6, ls="--"))
ax.text(6.55, 3.45, "some held out\nas a test set", fontsize=10.5, color=INK2, ha="center")
ax.text(0.2, 6.15, "Hard negatives: a loop, not a one-off clean-up", fontsize=14, weight="bold", va="top")
save(fig, f"{SLUG}-loop.png")
