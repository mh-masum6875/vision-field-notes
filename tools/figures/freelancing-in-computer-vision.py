"""Figures for freelancing-in-computer-vision.md"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
from style import C, ACCENT, INK, INK2, MUTED, GRID, WARN, save

SLUG = "freelancing-in-computer-vision"


def box(ax, x, y, w, h, color, fill=0.12, lw=1.6, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw, ls=ls))


# 1. Phases: commitment grows only after evidence
fig, ax = plt.subplots(figsize=(10, 5.4))
ax.set_xlim(0, 12.4); ax.set_ylim(-1.5, 5.6); ax.axis("off")
ax.text(0.05, 5.5, "Spend grows only after each phase produces evidence", fontsize=14, weight="bold", va="top")
phases = [("Discovery", "look at data,\ndefine success", 1.1),
          ("Prototype", "first model,\nhonest metrics", 2.0),
          ("Build", "full pipeline,\nalerts, testing", 3.6),
          ("Handover /\nsupport", "docs, deploy,\nmonitoring", 2.4)]
w, gap = 2.3, 0.9
x = 0.1
xs = []
for i, (name, sub, hgt) in enumerate(phases):
    col = [C[0], C[6], C[1], C[2]][i]
    box(ax, x, 0, w, hgt, col, fill=0.22)
    ax.text(x + w / 2, hgt + 0.15, name, ha="center", va="bottom", fontsize=13, weight="bold", linespacing=1.15)
    ax.text(x + w / 2, -0.25, sub, ha="center", va="top", fontsize=12, color=INK2, linespacing=1.3)
    xs.append(x)
    x += w + gap
for i in range(2):
    gx = xs[i] + w + gap / 2
    ax.add_patch(Polygon([[gx, 0.95], [gx + 0.28, 0.6], [gx, 0.25], [gx - 0.28, 0.6]], closed=True,
                         fc=WARN, ec=INK2, lw=1))
    ax.text(gx, 1.15, "go /\nno-go", ha="center", va="bottom", fontsize=11.5, color=INK, linespacing=1.1)
ax.text(12.3, 4.6, "box height = relative\nclient spend (schematic)", ha="right", va="top", fontsize=11.5,
        color=INK2)
ax.plot([0, 12.3], [0, 0], color=INK2, lw=1)
save(fig, f"{SLUG}-phases.png")

# 2. Choosing a pricing model (conceptual map)
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.grid(False)
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
ax.spines["left"].set_color(INK2); ax.spines["bottom"].set_color(INK2)
ax.set_xticks([]); ax.set_yticks([])
ax.annotate("", xy=(10, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.3), annotation_clip=False)
ax.annotate("", xy=(0, 10), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.3), annotation_clip=False)
ax.set_xlabel("How clear is the scope?   unclear  →  clear", fontsize=12.5, color=INK, labelpad=8)
ax.set_ylabel("How long is the work?   one project  →  ongoing", fontsize=12.5, color=INK, labelpad=8)
items = [
    (0.5, 1.2, 4.0, 2.6, C[0], "Hourly or daily rate", "safer while unknowns remain;\nsend estimates and updates"),
    (5.5, 1.2, 4.2, 2.6, C[1], "Fixed price per phase", "only with written scope,\nexclusions and change process"),
    (2.6, 6.6, 4.4, 2.6, C[2], "Retainer", "ongoing monitoring\nand improvement"),
    (5.5, 4.0, 4.2, 2.3, C[6], "Value-based", "needs clear, measurable\nsavings and trust"),
]
for x, y, w, h, col, title, sub in items:
    box(ax, x, y, w, h, col)
    ax.text(x + w / 2, y + h - 0.55, title, ha="center", va="center", fontsize=13, weight="bold")
    ax.text(x + w / 2, y + (h - 0.6) / 2, sub, ha="center", va="center", fontsize=12, color=INK2, linespacing=1.3)
ax.set_title("Match the pricing model to how well the work is understood", loc="left")
save(fig, f"{SLUG}-pricing-map.png")
