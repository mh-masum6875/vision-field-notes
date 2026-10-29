"""Figures for day-night-switching-ir-cut-filter.

A constructed light curve at dusk with hysteresis switching, to show why a camera can flip between
modes several times. Light values and thresholds are made up; no camera was measured.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, WARN, save

SLUG = "day-night-switching-ir-cut-filter"
rng = np.random.default_rng(4)
t = np.linspace(0, 60, 1200)                       # minutes around dusk
light = (10 * np.exp(-t / 14) + 0.9 * np.sin(t / 0.9) * np.exp(-((t - 22) / 12) ** 2)
         + rng.normal(0, 0.2, len(t)))  # passing clouds and headlights near the threshold
light = np.clip(light, 0.05, None)


def modes(lo, hi):
    m, out = "day", []
    for v in light:
        if m == "day" and v < lo:
            m = "night"
        elif m == "night" and v > hi:
            m = "day"
        out.append(m)
    return np.array(out)


fig, axes = plt.subplots(2, 1, figsize=(10.5, 5.6), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
ax = axes[0]
ax.plot(t, light, color=C[3])
ax.axhline(2.0, color=C[1], ls="--", lw=1.2); ax.text(59, 2.15, "switch to night below", ha="right", fontsize=11, color=C[1])
ax.axhline(2.6, color=C[0], ls="--", lw=1.2); ax.text(59, 2.75, "switch back to day above (narrow gap)", ha="right", fontsize=11, color=C[0])
ax.set_yticks([]); ax.set_ylabel("scene light")
ax.set_ylim(0, 6)
ax.set_title("At dusk, light hovers near the threshold; a narrow gap makes the camera flap (constructed)", loc="left")
ax = axes[1]
for row, (lo, hi, name) in enumerate([(2.0, 2.6, "narrow gap"), (2.0, 4.5, "wide gap")]):
    m = modes(lo, hi)
    ax.fill_between(t, row + 0.1, row + 0.9, where=m == "night", color=INK2, alpha=0.75, step="mid", lw=0)
    ax.fill_between(t, row + 0.1, row + 0.9, where=m == "day", color=C[3], alpha=0.35, step="mid", lw=0)
    print(name, "switches:", int((m[1:] != m[:-1]).sum()))
ax.set_yticks([0.5, 1.5]); ax.set_yticklabels(["narrow gap", "wide gap"])
ax.grid(False)
ax.set_xlabel("minutes")
axes[1].text(60, 2.05, "yellow = colour day mode   grey = IR night mode", ha="right", fontsize=10.5, color=INK2)
fig.tight_layout()
save(fig, f"{SLUG}-hysteresis.png")
