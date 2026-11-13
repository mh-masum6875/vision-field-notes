"""Figure for microchip-completes-hailo-acquisition.

A diagram of where vendor lock-in actually sits in an edge vision stack, and
which artefacts have to survive a vendor changing direction. No measurements.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "microchip-completes-hailo-acquisition"

# (label, note, lock)  lock: "yours" | "vendor"
STAGES = [
    ("Training data\nand labels",        "dataset version,\nlabel guide",       "yours"),
    ("Training recipe",                  "code, seeds,\nhyper-parameters",      "yours"),
    ("Framework-neutral\nmodel (ONNX)",  "the handover point",                 "yours"),
    ("Vendor compiler",                  "pinned version,\narchived installer", "vendor"),
    ("Compiled binary\n(.hef)",          "rebuilt, never\nthe only copy",       "vendor"),
    ("Vendor runtime\non the device",    "pinned version",                     "vendor"),
]

fig, ax = plt.subplots(figsize=(12.8, 6.4))
ax.set_xlim(0, 12.8)
ax.set_ylim(0, 6.4)
ax.axis("off")

BW, BH, GAP = 1.86, 1.70, 0.22
x = 0.35
Y = 3.55

for i, (label, note, lock) in enumerate(STAGES):
    yours = lock == "yours"
    fc = "#eaf6ee" if yours else "#fdf0e6"
    ec = GOOD if yours else WARN
    ax.add_patch(FancyBboxPatch((x, Y - BH / 2), BW, BH,
                                boxstyle="round,pad=0.05,rounding_size=0.14",
                                fc=fc, ec=ec, lw=1.9, zorder=3))
    ax.text(x + BW / 2, Y + 0.30, label, ha="center", va="center", fontsize=11.4,
            color=INK, weight="bold", linespacing=1.3, zorder=4)
    ax.text(x + BW / 2, Y - 0.50, note, ha="center", va="center", fontsize=9.6,
            color=INK2, linespacing=1.3, zorder=4)
    if i < len(STAGES) - 1:
        ax.add_patch(FancyArrowPatch((x + BW, Y), (x + BW + GAP, Y),
                                     arrowstyle="-|>", mutation_scale=15,
                                     color=INK2, lw=1.8, zorder=2))
    x += BW + GAP

split = 0.35 + 3 * (BW + GAP) - GAP / 2
ax.plot([split, split], [1.25, 5.55], color=CRIT, lw=2.4, ls="--", zorder=5)
ax.text(split - 0.14, 5.62, "yours, whatever the vendor does", ha="right", fontsize=12.5,
        color=GOOD, weight="bold")
ax.text(split + 0.14, 5.62, "replaceable, if you kept the left half", ha="left",
        fontsize=12.5, color=WARN, weight="bold")

ax.add_patch(FancyArrowPatch((split - 0.9, 2.25), (split + 3.4, 2.25),
                             arrowstyle="-|>", mutation_scale=17, color=C[0], lw=2.2,
                             connectionstyle="arc3,rad=0.26", zorder=4))
ax.text(split + 1.2, 0.78, "Changing accelerator means recompiling from the ONNX,\n"
                           "not retraining from scratch",
        ha="center", fontsize=12, color=C[0], weight="bold", linespacing=1.4)

fig.suptitle("Only the right-hand half is tied to a vendor",
             x=0.012, ha="left", fontsize=15.5, weight="bold")
fig.text(0.012, 0.925,
         "Hailo is now part of Microchip. The same picture applies to any accelerator vendor.",
         ha="left", va="top", fontsize=11.5, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-what-is-portable.png")
print("rendered portability figure")
