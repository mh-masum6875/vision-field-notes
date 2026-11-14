"""Figure for night-and-bad-weather-test-set.

Exact arithmetic, not measurements. If night images are a tenth of the test
set, the overall number is 0.9 * day + 0.1 * night, so it can only move a
tenth as far as the night number does.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "night-and-bad-weather-test-set"

DAY = 0.92                      # day recall, held fixed
night = np.linspace(0.92, 0.30, 300)
SHARES = [(0.10, C[0], "night is 10% of the test set"),
          (0.25, C[2], "night is 25%"),
          (0.50, C[3], "night is 50%")]

fig, axs = plt.subplots(1, 2, figsize=(12.6, 5.6),
                        gridspec_kw={"width_ratios": [1.15, 1.0]})

ax = axs[0]
ax.plot(night, night, color=INK, lw=2.6, ls="--", label="the night set itself")
for share, col, lab in SHARES:
    ax.plot(night, (1 - share) * DAY + share * night, lw=2.4, color=col, label=lab)

NIGHT_BAD = 0.45
overall = (1 - 0.10) * DAY + 0.10 * NIGHT_BAD
ax.plot([NIGHT_BAD], [overall], marker="o", ms=11, mfc=CRIT, mec="white", mew=2, zorder=5)
ax.plot([NIGHT_BAD], [NIGHT_BAD], marker="o", ms=11, mfc=INK, mec="white", mew=2, zorder=5)
ax.annotate(f"night recall {NIGHT_BAD:.0%}\nreads as {overall:.0%} overall",
            xy=(NIGHT_BAD, overall), xytext=(0.53, 0.70), fontsize=12, color=CRIT,
            weight="bold", linespacing=1.4,
            arrowprops=dict(arrowstyle="->", color=CRIT, lw=1.8,
                            connectionstyle="arc3,rad=-0.25"))

ax.set_xlabel("recall on night images")
ax.set_ylabel("the number you report")
ax.set_xlim(0.92, 0.30)
ax.set_ylim(0.28, 0.97)
ax.set_xticks([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3])
ax.set_xticklabels([f"{v:.0%}" for v in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]])
ax.set_yticks([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
ax.set_yticklabels([f"{v:.0%}" for v in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]])
ax.set_title("Night gets worse to the right", fontsize=12.5, loc="left")
ax.legend(fontsize=10.6, loc="lower left")

# ---- how far the headline moves for a 47-point collapse at night
ax = axs[1]
drop_night = DAY - NIGHT_BAD
drops = [(share, DAY - ((1 - share) * DAY + share * NIGHT_BAD)) for share, _, _ in SHARES]
labels = [f"{int(s*100)}%" for s, _ in drops]
cols = [C[0], C[2], C[3]]
bars = ax.bar(np.arange(len(drops)) + 1, [d * 100 for _, d in drops], 0.6, color=cols)
ax.bar([0], [drop_night * 100], 0.6, color=INK)
for x, v in zip([0] + list(np.arange(len(drops)) + 1),
                [drop_night * 100] + [d * 100 for _, d in drops]):
    ax.text(x, v + 1.1, f"{v:.1f} pts", ha="center", fontsize=11.6, weight="bold", color=INK)
ax.set_xticks(range(4), ["the night\nset itself"] + [f"overall,\nnight = {l}" for l in labels],
              fontsize=10.8)
ax.set_ylabel("points the reported number falls")
ax.set_ylim(0, 56)
ax.set_title("The same failure, four ways of reporting it", fontsize=12.5, loc="left")
ax.grid(axis="x", visible=False)

fig.suptitle("A tenth of the test set can only move the headline by a tenth",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.925,
         f"Arithmetic, with day recall held at {DAY:.0%}. Overall = (1 − share) × day + share × night.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-dilution.png")

for share, _, _ in SHARES:
    o = (1 - share) * DAY + share * NIGHT_BAD
    print(f"night {NIGHT_BAD:.0%} at {share:.0%} of the set -> overall {o:.1%} "
          f"(falls {(DAY-o)*100:.1f} pts, night itself falls {drop_night*100:.1f})")
