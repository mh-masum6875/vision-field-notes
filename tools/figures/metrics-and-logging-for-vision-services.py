"""Figure for metrics-and-logging-for-vision-services.

Simulated detection counts, not a real camera. It shows why a fixed threshold
cannot separate "quiet night" from "blind camera", and why comparing against
the same hour on previous days can.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "metrics-and-logging-for-vision-services"

rng = np.random.default_rng(19)
DAYS, H = 4, 24
hours = np.arange(DAYS * H)

# a shop doorway: busy in the day, near-dead overnight
shape = 8 + 46 * np.exp(-0.5 * ((np.arange(H) - 13.5) / 3.6) ** 2)
shape[:6] = 0.6
shape[22:] = 1.4
base = np.tile(shape, DAYS) * rng.uniform(0.82, 1.18, DAYS * H)
counts = np.round(base).astype(float)

FAIL = 3 * H + 9          # camera goes blind on day 4 at 09:00
counts[FAIL:] = 0

# the baseline: same hour, previous days, so the night is allowed to be quiet
hist = counts.reshape(DAYS, H)
expected = np.full(DAYS * H, np.nan)
for d in range(1, DAYS):
    prev = hist[max(0, d - 3):d]
    expected[d * H:(d + 1) * H] = prev.mean(axis=0)
floor = expected * 0.25   # alert when well under what this hour normally gives

FIXED = 5

fig, ax = plt.subplots(figsize=(12.4, 5.4))
ax.plot(hours, counts, color=C[0], lw=1.9, label="detections per hour")
ax.plot(hours, expected, color=C[2], lw=1.6, ls="--",
        label="same hour, previous 3 days")
ax.fill_between(hours, 0, floor, color=C[2], alpha=0.14,
                label="below this = something is wrong")
ax.axhline(FIXED, color=CRIT, lw=1.8, ls=":", label=f"fixed threshold of {FIXED}")

ax.axvline(FAIL, color=INK, lw=1.6)
ax.annotate("camera goes blind", xy=(FAIL, 30), xytext=(FAIL - 31, 46),
            fontsize=12, weight="bold", color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))

# every night the fixed threshold would fire with nothing wrong
nights = [(d * H + 0, d * H + 6) for d in range(DAYS)]
for i, (a, b) in enumerate(nights):
    ax.axvspan(a, b, color=MUTED, alpha=0.11, lw=0)
ax.text(3.0, 33, "nights:\nquiet, but fine", fontsize=10.5, color=INK2, ha="center",
        linespacing=1.35)

false_fires = int(((counts < FIXED) & (np.arange(DAYS * H) < FAIL)).sum())
caught = int(np.nanargmax((counts < floor) & (hours > FAIL)))
ax.annotate(f"the baseline catches it\n{caught - FAIL} hour{'s' if caught - FAIL != 1 else ''} later",
            xy=(caught, 1.5), xytext=(caught + 7, 26), fontsize=11.5,
            color=C[2], weight="bold", linespacing=1.35,
            arrowprops=dict(arrowstyle="->", color=C[2], lw=1.7,
                            connectionstyle="arc3,rad=-0.25"))

ax.set_xticks(np.arange(0, DAYS * H + 1, 12))
ax.set_xticklabels([f"d{t // H + 1}\n{t % H:02d}:00" for t in np.arange(0, DAYS * H + 1, 12)],
                   fontsize=10)
ax.set_xlim(0, DAYS * H)
ax.set_ylim(0, 72)
ax.set_ylabel("detections per hour, one camera")
ax.set_xlabel("")
ax.legend(fontsize=10.5, loc="lower left", bbox_to_anchor=(0, 1.005), ncol=4)

fig.suptitle(f"A fixed threshold fires {false_fires} times on ordinary quiet hours, "
             f"and still misses the real failure",
             x=0.01, ha="left", fontsize=14.5, weight="bold")
fig.text(0.01, 0.925, "Simulated counts for a shop doorway, not a real camera.",
         ha="left", va="top", fontsize=11.5, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.865])
save(fig, f"{SLUG}-alert-on-absence.png")

print(f"fixed-threshold false fires before the failure: {false_fires}")
print(f"baseline catches the blind camera {caught - FAIL} hours after it starts")
