"""Figure for pose-estimation-for-behaviour.

Simulated keypoints, not a real pose model. The rule is real: raise an alert
when the wrist is above the shoulder. Counting how often it fires, with and
without the two guards the post recommends, is arithmetic over the simulation.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "pose-estimation-for-behaviour"

FPS = 25
SECONDS = 24
N = FPS * SECONDS
t = np.arange(N) / FPS
rng = np.random.default_rng(13)

# the true wrist height relative to the shoulder: normally below, raised once
true_h = np.full(N, -0.22)
RAISE = (14.0, 16.5)
true_h[(t >= RAISE[0]) & (t <= RAISE[1])] = 0.20

# keypoint confidence: two stretches where the arm is occluded
conf = np.clip(rng.normal(0.86, 0.05, N), 0, 1)
for a, b in [(5.0, 7.5), (19.0, 21.0)]:
    m = (t >= a) & (t <= b)
    conf[m] = np.clip(rng.normal(0.30, 0.08, m.sum()), 0, 1)

# jitter, much larger where the model is guessing
noise = rng.normal(0, 0.09, N) + (conf < 0.5) * rng.normal(0, 0.30, N)
obs_h = true_h + noise

above = obs_h > 0


def runs(mask):
    """Start indices and lengths of each run of True."""
    d = np.diff(np.concatenate([[0], mask.view(np.int8), [0]]))
    starts, ends = np.where(d == 1)[0], np.where(d == -1)[0]
    return starts, ends - starts


HOLD = int(0.4 * FPS)          # must stay true for 0.4 s
gated = above & (conf >= 0.5)
s_g, l_g = runs(gated)
sustained = np.zeros(N, dtype=bool)
for s, l in zip(s_g, l_g):
    if l >= HOLD:
        sustained[s:s + l] = True

naive_alerts = len(runs(above)[0])
guarded_alerts = len(runs(sustained)[0])

fig, axs = plt.subplots(2, 1, figsize=(12.6, 6.8), sharex=True,
                        gridspec_kw={"height_ratios": [2.0, 1.0]})

ax = axs[0]
ax.axhline(0, color=INK, lw=1.8)
ax.plot(t, obs_h, color=MUTED, lw=1.1, zorder=2, label="observed wrist height")
ax.plot(t, true_h, color=INK2, lw=2.2, ls="--", zorder=3, label="what is really happening")
for s, l in zip(*runs(above)):
    ax.axvspan(t[s], t[min(s + l, N - 1)], color=CRIT, alpha=0.30, lw=0, zorder=1)
for s, l in zip(*runs(sustained)):
    ax.axvspan(t[s], t[min(s + l, N - 1)], color=GOOD, alpha=0.45, lw=0, zorder=4)
ax.set_ylabel("wrist height above shoulder")
ax.set_ylim(-0.95, 0.75)
ax.set_title(f"“alert when the wrist is above the shoulder”  →  "
             f"{naive_alerts} alerts, of which 1 is real",
             fontsize=13, loc="left", color=CRIT)
ax.legend(fontsize=10.8, loc="lower left", ncol=2)

ax = axs[1]
ax.plot(t, conf, color=C[0], lw=1.8)
ax.axhline(0.5, color=CRIT, lw=1.6, ls="--")
ax.fill_between(t, 0, 1, where=conf < 0.5, color=CRIT, alpha=0.13, lw=0)
ax.text(6.2, 0.70, "arm occluded:\nthe model is guessing", ha="center", fontsize=10.8,
        color=CRIT, weight="bold", linespacing=1.3)
ax.set_ylabel("keypoint\nconfidence")
ax.set_xlabel("time (seconds)")
ax.set_ylim(0, 1.02)
ax.set_xlim(0, SECONDS)
ax.set_title(f"Discard below 0.5 and require {HOLD / FPS:.1f} s  →  "
             f"{guarded_alerts} alert{'s' if guarded_alerts != 1 else ''}",
             fontsize=13, loc="left", color=GOOD)

fig.suptitle(f"The same rule, {naive_alerts} alerts or {guarded_alerts}",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.932,
         "Simulated keypoints. The red bands are every moment the raw rule fires; "
         "the green band is what survives the two guards.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.895])
save(fig, f"{SLUG}-jitter-and-confidence.png")

print(f"naive rule fires {naive_alerts} times; guarded fires {guarded_alerts}")
print(f"frames below confidence 0.5: {(conf < 0.5).sum()} of {N}")
