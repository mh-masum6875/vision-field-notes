"""Figures for int8-quantization-explained.

Figure 1 uses synthetic (illustrative) activation values, not measurements.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "int8-quantization-explained"

# 1. Outlier stretches the range (illustrative synthetic activations)
rng = np.random.default_rng(7)
acts = rng.laplace(0, 0.6, 50000)
acts = np.concatenate([acts, [38.0, -31.0, 35.5]])  # a few rare outliers


def quant(x, scale):
    q = np.clip(np.round(x / scale), -127, 127)
    return q


s_max = np.abs(acts).max() / 127
clip = np.percentile(np.abs(acts), 99.99)
s_clip = clip / 127
fig, axs = plt.subplots(2, 1, figsize=(10, 6.6), sharex=True)
for ax, s, title in [(axs[0], s_max, f"Scale set by the largest value ({np.abs(acts).max():.0f}): step = {s_max:.2f}"),
                     (axs[1], s_clip, f"Scale set by calibration (clip at {clip:.1f}): step = {s_clip:.3f}")]:
    q = quant(acts, s)
    used = len(np.unique(q[np.abs(acts) < 4]))
    ax.hist(acts, bins=np.linspace(-4, 4, 161), color=C[0], alpha=0.85)
    levels = np.arange(-127, 128) * s
    for l in levels[(levels > -4) & (levels < 4)]:
        ax.axvline(l, color=C[1], lw=0.8, alpha=0.8)
    ax.set_title(title, fontsize=12.5, loc="left")
    ax.text(0.99, 0.92, f"{used} integer levels cover\nthe bulk of the values (|x| < 4)", transform=ax.transAxes,
            ha="right", va="top", fontsize=11.5, color=INK,
            bbox=dict(fc="white", ec=GRID, boxstyle="round,pad=0.3"))
    ax.set_ylabel("count")
    ax.set_yticks([])
axs[1].set_xlabel("activation value (zoomed to -4 .. 4; orange lines = INT8 levels)")
fig.suptitle("One outlier can waste most of the 256 INT8 levels (illustrative data)", x=0.01, ha="left",
             fontsize=14, weight="bold")
fig.tight_layout()
save(fig, f"{SLUG}-outlier-range.png")


# 2. Decision flow from FP32 to INT8
def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, size=11.5, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight,
            linespacing=1.3)


def arrow(ax, x1, y1, x2, y2, label=None, lx=0, ly=0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=16, shrinkA=0, shrinkB=0))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=11, weight="bold", color=INK2,
                ha="center", va="center")


fig, ax = plt.subplots(figsize=(10.5, 5.6))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.6)
ax.axis("off")
box(ax, 0.1, 4.1, 2.2, 1.0, "FP32 model\n(keep it!)", fc="#f4f3ef")
arrow(ax, 2.3, 4.6, 2.75, 4.6)
box(ax, 2.75, 4.1, 2.6, 1.0, "FP16 or a smaller\nmodel meets\nthe target?", ec=ACCENT, weight="bold", size=11)
arrow(ax, 5.35, 4.6, 5.9, 4.6, "yes", ly=0.22)
box(ax, 5.9, 4.1, 2.2, 1.0, "Stop here:\nno INT8 needed", fc="#e7f5e7", ec=GOOD)
arrow(ax, 4.05, 4.1, 4.05, 3.45, "no", lx=0.3)
box(ax, 2.75, 2.45, 2.6, 1.0, "PTQ: calibrate on\nrepresentative images", fc="#ffffff")
arrow(ax, 5.35, 2.95, 5.9, 2.95)
box(ax, 5.9, 2.25, 2.4, 1.4, "Validate vs FP32:\nmAP50-95, per class,\nsmall objects,\nfalse alarms", fc="#ffffff")
arrow(ax, 8.3, 2.95, 8.75, 2.95)
box(ax, 8.75, 2.45, 1.65, 1.0, "Passes your\nrule?", ec=ACCENT, weight="bold")
arrow(ax, 9.575, 3.45, 9.575, 4.1, "yes", lx=0.35)
box(ax, 8.75, 4.1, 1.65, 1.0, "Ship INT8,\nre-tune\nthresholds", fc="#e7f5e7", ec=GOOD, size=11)
arrow(ax, 9.575, 2.45, 9.575, 1.4, "no", lx=0.3)
box(ax, 5.9, 0.4, 4.5, 1.0, "Mixed precision for sensitive layers,\nor quantization-aware training (QAT)",
    fc="#fdf0e9", ec=C[1])
arrow(ax, 7.1, 1.4, 7.1, 2.25)
ax.text(6.95, 1.82, "re-validate", fontsize=10.5, color=MUTED, ha="right")
ax.set_title("Try the low-risk options first and validate every INT8 model like a new model", loc="left")
save(fig, f"{SLUG}-decision-flow.png")
