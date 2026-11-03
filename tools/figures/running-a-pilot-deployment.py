"""Figures for running-a-pilot-deployment. A diagram; durations are examples, not a rule."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, WARN, save

SLUG = "running-a-pilot-deployment"
fig, ax = plt.subplots(figsize=(12, 4.4))
ax.set_xlim(0, 12.2); ax.set_ylim(0, 4.4); ax.axis("off")
ax.text(0.1, 4.2, "A pilot in four stages, each ending in a decision (example durations)", fontsize=14,
        weight="bold", va="center")
stages = [("Install and check", "1 week", "streams, health,\ntime, settings", C[0], 1.8),
          ("Shadow mode", "1-2 weeks", "alerts logged, not sent;\nreview daily", C[6], 3.0),
          ("Live, small group", "2-4 weeks", "alerts to trained users;\nfeedback on each", C[2], 3.8),
          ("Decide", "", "against the agreed\nexit criteria", C[1], 1.8)]
x = 0.1
for name, dur, sub, c, w in stages:
    ax.add_patch(FancyBboxPatch((x, 1.2), w, 2.2, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=c + "22", ec=c, lw=1.6))
    ax.text(x + w / 2, 3.05, name, ha="center", fontsize=12.5, weight="bold")
    if dur:
        ax.text(x + w / 2, 2.65, dur, ha="center", fontsize=11, color=c)
    ax.text(x + w / 2, 1.9, sub, ha="center", va="center", fontsize=10.8, color=INK2, linespacing=1.35)
    x += w + 0.25
ax.text(0.1, 0.6, "Go: roll out.   Fix: change and repeat the last stage.   Stop: the pilot did its job by "
        "answering the question cheaply.", fontsize=11, color=INK2)
save(fig, f"{SLUG}-stages.png")
