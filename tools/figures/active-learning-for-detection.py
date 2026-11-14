"""Figure for active-learning-for-detection.

Simulated uncertainty scores over two minutes of video. The selection rule is
real: take the top N by score, with and without a minimum time gap. The counts
printed and drawn are computed from the simulation, not asserted.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "active-learning-for-detection"

FPS = 25
SECONDS = 120
N = FPS * SECONDS
BUDGET = 30
MIN_GAP = FPS * 2          # at least two seconds between chosen frames

rng = np.random.default_rng(7)
t = np.arange(N) / FPS

# a handful of genuinely hard moments, each lasting a second or two
score = rng.normal(0.22, 0.05, N)
MOMENTS = [(14, 2.2, 0.62), (31, 1.4, 0.50), (58, 2.6, 0.70),
           (77, 1.1, 0.44), (96, 2.0, 0.58), (109, 1.5, 0.47)]
for centre, width, height in MOMENTS:
    score += height * np.exp(-0.5 * ((t - centre) / (width / 2)) ** 2)
score = np.clip(score + rng.normal(0, 0.012, N), 0, None)


def pick_top(scores, budget):
    return np.sort(np.argsort(scores)[::-1][:budget])


def pick_spaced(scores, budget, gap):
    chosen = []
    for i in np.argsort(scores)[::-1]:
        if all(abs(i - j) >= gap for j in chosen):
            chosen.append(i)
            if len(chosen) == budget:
                break
    return np.sort(np.array(chosen))


def moments_covered(idx, gap=FPS * 2):
    """How many separate events the chosen frames come from."""
    if len(idx) == 0:
        return 0
    return 1 + int((np.diff(idx) > gap).sum())


naive = pick_top(score, BUDGET)
spaced = pick_spaced(score, BUDGET, MIN_GAP)

fig, axs = plt.subplots(2, 1, figsize=(12.6, 6.8), sharex=True, sharey=True)

for ax, idx, title, col in [
        (axs[0], naive, f"Top {BUDGET} by uncertainty", CRIT),
        (axs[1], spaced, f"Top {BUDGET}, with a {MIN_GAP // FPS}-second minimum gap", GOOD)]:
    ax.plot(t, score, color=MUTED, lw=1.0, zorder=2)
    ax.vlines(t[idx], 0, score[idx], color=col, lw=1.6, alpha=0.9, zorder=3)
    ax.scatter(t[idx], score[idx], s=26, color=col, zorder=4)
    m = moments_covered(idx)
    ax.set_title(f"{title}    →  {m} distinct moment{'s' if m != 1 else ''}, "
                 f"{len(np.unique(idx)):d} frames",
                 fontsize=12.6, loc="left", color=col)
    ax.set_ylabel("uncertainty")
    ax.set_ylim(0, score.max() * 1.12)

axs[1].set_xlabel("time in the clip (seconds)")
axs[1].set_xlim(0, SECONDS)

fig.suptitle("The same budget, spent on six moments or on two",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.932,
         f"Simulated uncertainty over {SECONDS} seconds at {FPS} fps. Both rows label "
         f"{BUDGET} frames; only the spacing rule differs.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.895])
save(fig, f"{SLUG}-near-duplicates.png")

print(f"naive : {moments_covered(naive)} moments, "
      f"spans {(naive.max()-naive.min())/FPS:.1f}s of the clip")
print(f"spaced: {moments_covered(spaced)} moments, "
      f"spans {(spaced.max()-spaced.min())/FPS:.1f}s of the clip")
print(f"hard moments actually present: {len(MOMENTS)}")
