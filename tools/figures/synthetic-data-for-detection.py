"""Figure for synthetic-data-for-detection.

A map of the three approaches against the two things that decide whether they
work, plus the gap each one fills. Positions are judgements from the post, not
measurements, and the figure says so.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "synthetic-data-for-detection"

#        name            pixels real  label control  colour  what it is for
METHODS = [
    ("Compositing", 0.88, 0.62, C[0],
     "real objects on real\nbackgrounds; blending\nseams are the risk"),
    ("Rendering", 0.34, 0.88, C[2],
     "perfect labels, unlimited\nvolume, expensive to\nset up"),
    ("Generative", 0.62, 0.18, C[1],
     "cheap per image, hard\nto control, labels are\nthe problem"),
]

fig, ax = plt.subplots(figsize=(11.6, 7.4))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

ax.axhspan(0.5, 1, xmin=0.5, color=GOOD, alpha=0.07, zorder=0)
ax.text(0.985, 0.525, "real pixels and trustworthy labels", ha="right", va="bottom",
        fontsize=11.5, color="#0b5c22", weight="bold", zorder=1)
ax.text(0.015, 0.025, "neither: you are generating\nconfident nonsense", ha="left",
        va="bottom", fontsize=11.5, color=CRIT, weight="bold", linespacing=1.35,
        zorder=1)

for name, px, lab, col, blurb in METHODS:
    ax.scatter([lab], [px], s=460, color=col, zorder=6, edgecolors="white", linewidths=2.4)
    ax.text(lab, px, name[0], ha="center", va="center", fontsize=14, color="white",
            weight="bold", zorder=7)
    dx, dy = (0.045, 0.085) if name != "Rendering" else (-0.045, 0.085)
    ha = "left" if dx > 0 else "right"
    ax.text(lab + dx, px + dy, name, ha=ha, va="bottom", fontsize=13.5, color=col,
            weight="bold", zorder=7)
    ax.text(lab + dx, px + dy - 0.035, blurb, ha=ha, va="top", fontsize=10.6,
            color=INK2, linespacing=1.35, zorder=7)

ax.set_xlabel("control over what the labels actually say  →", fontsize=12.5)
ax.set_ylabel("how real the pixels are  →", fontsize=12.5)
ax.set_xticks([0.1, 0.5, 0.9], ["you are guessing", "partly", "exact by construction"],
              fontsize=11)
ax.set_yticks([0.1, 0.5, 0.9], ["rendered look", "close", "genuine photographs"],
              fontsize=11)
ax.axhline(0.5, color=GRID, lw=1.2)
ax.axvline(0.5, color=GRID, lw=1.2)
ax.grid(False)

fig.suptitle("The three things people mean by synthetic fail in different directions",
             x=0.01, ha="left", fontsize=15, weight="bold")
fig.text(0.01, 0.928,
         "Positions are judgements from the post, not measurements. "
         "Use them to pick which failure you can live with.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-three-kinds.png")
print("rendered synthetic data map")
