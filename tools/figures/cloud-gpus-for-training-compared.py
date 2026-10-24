"""Figures for cloud-gpus-for-training-compared. All numbers are illustrative units, not real prices."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, ACCENT, INK, INK2, MUTED, GRID, save

SLUG = "cloud-gpus-for-training-compared"

# ---------------------------------------------------------------- 1. cost per run = rate x time
runs = [  # label, rate (units per hour), hours for the same training job
    ("Smaller GPU", 1.0, 10.0, C[0]),
    ("Larger GPU", 2.5, 3.6, C[1]),
    ("Oversized, under-used GPU", 4.0, 3.2, C[6]),
]
fig, axes = plt.subplots(1, 3, figsize=(10, 4.2), sharey=True)
for ax, (label, rate, hours, col) in zip(axes, runs):
    ax.add_patch(plt.Rectangle((0, 0), hours, rate, fc=col + "33", ec=col, lw=2))
    ax.text(hours / 2, rate / 2, f"{rate * hours:.1f}\nunits", ha="center", va="center", fontsize=13,
            weight="bold", color=INK)
    ax.set_title(label, fontsize=12.5, loc="left", weight="bold")
    ax.text(0.2, 4.35, f"{rate:g} per hour x {hours:g} h", fontsize=11.5, color=INK2, va="top")
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 4.5); ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_axisbelow(True)
axes[0].set_ylabel("Hourly rate (illustrative units)")
axes[1].set_xlabel("Hours to finish the same training job")
fig.suptitle("Cost per run is the area, rate times time: the pricier GPU can be cheapest",
             x=0.06, ha="left", fontsize=14, weight="bold")
fig.tight_layout()
save(fig, f"{SLUG}-cost-per-run.png")


# ---------------------------------------------------------------- 2. where the bill goes (illustrative)
parts = ["Useful training", "Failed or buggy runs", "Idle instance", "Storage while stopped", "Data egress"]
careless = [40, 25, 30, 10, 8]
careful = [40, 4, 2, 3, 2]
fig, ax = plt.subplots(figsize=(10, 3.8))
labels = ["Careless month", "Same work, good habits"]
for row, vals in enumerate([careless, careful]):
    left = 0
    for i, v in enumerate(vals):
        ax.barh(row, v, left=left, color=C[i], height=0.55, edgecolor="white", lw=1.2,
                label=parts[i] if row == 0 else None)
        left += v
    ax.text(left + 1.5, row, f"{left} units", va="center", fontsize=12, color=INK2)
ax.set_yticks([0, 1]); ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlim(0, 128)
ax.set_xlabel("Monthly bill (illustrative units)")
ax.grid(axis="y", visible=False)
ax.set_axisbelow(True)
ax.set_title("Same useful training; the difference is idle time, failed runs and storage", loc="left")
ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.22), ncol=3, fontsize=11.5)
save(fig, f"{SLUG}-bill-breakdown.png")
