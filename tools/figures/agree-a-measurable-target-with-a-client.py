"""Figures for agree-a-measurable-target-with-a-client. Pure arithmetic, no measured data."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "agree-a-measurable-target-with-a-client"

# Rule of three: with zero misses in n events, the 95% upper bound on the miss rate is about 3/n.
# Exact one-sided bound for zero failures: 1 - 0.05 ** (1 / n).
n = np.arange(5, 301)
exact = 1 - 0.05 ** (1 / n)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(n, exact * 100, color=C[0], label="exact bound, zero misses observed")
ax.plot(n, 3 / n * 100, color=C[1], ls="--", label="rule of three, 3 / n")
for v in (20, 50, 100, 200):
    b = (1 - 0.05 ** (1 / v)) * 100
    ax.plot([v], [b], "o", color=C[0], ms=6)
    ax.text(v + 4, b + 1.2, f"{v} events: up to {b:.1f}%", fontsize=11.5, color=INK)
ax.set_xlim(0, 300); ax.set_ylim(0, 45)
ax.set_xlabel("number of real events in the acceptance test")
ax.set_ylabel("miss rate you cannot rule out (%)")
ax.legend(loc="upper right", fontsize=11.5)
ax.set_title("Even a perfect test result only bounds the miss rate (95% confidence)", loc="left")
save(fig, f"{SLUG}-rule-of-three.png")
