"""Figure for estimating-a-computer-vision-project.

Illustrative, not measured. The shape is the point: effort and calendar
duration are different quantities, and the gap between them is waiting.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "estimating-a-computer-vision-project"

#            phase                 start  duration  effort   who waits
PHASES = [
    ("Discovery",                   0.0,   1.5,     1.2,  ""),
    ("Data access",                 0.5,   5.0,     0.8,  "client IT, security, legal"),
    ("Labelling",                   4.0,   3.5,     3.0,  ""),
    ("Model work",                  6.0,   1.5,     1.3,  ""),
    ("Pipeline",                    6.5,   2.5,     2.2,  ""),
    ("Integration",                 7.0,   4.0,     1.5,  "credentials, test environment"),
    ("Deployment",                 10.0,   2.5,     1.0,  "hardware, network changes"),
    ("Testing on site",            11.0,   3.5,     1.5,  "nights, weather, escorts"),
    ("Revisions",                  13.5,   2.5,     1.5,  "client review"),
    ("Handover",                   15.5,   1.5,     1.0,  ""),
]

fig, ax = plt.subplots(figsize=(12.2, 6.2))
ys = np.arange(len(PHASES))[::-1]

for y, (name, start, dur, eff, waits) in zip(ys, PHASES):
    highlight = name == "Model work"
    ax.barh(y, dur, left=start, height=0.62, color=GRID, ec="#d8d6d0", zorder=2)
    ax.barh(y, eff, left=start, height=0.62, zorder=3,
            color=C[1] if highlight else C[0])
    if dur - eff > 1.0:
        ax.text(start + eff + (dur - eff) / 2, y, "waiting", ha="center", va="center",
                fontsize=10, color=INK2, style="italic", zorder=4)
    ax.text(start + dur + 0.18, y, f"{eff:g}w effort / {dur:g}w elapsed",
            va="center", fontsize=10.5, color=INK if highlight else INK2,
            weight="bold" if highlight else "normal", zorder=4)

ax.set_yticks(ys, [p[0] for p in PHASES], fontsize=11.5)
ax.set_xlabel("calendar weeks from kick-off")
ax.set_xlim(0, 24.5)
ax.set_xticks(np.arange(0, 18, 2))
ax.grid(axis="y", visible=False)

total_eff = sum(p[3] for p in PHASES)
model_eff = dict((p[0], p[3]) for p in PHASES)["Model work"]
end = max(p[1] + p[2] for p in PHASES)

ax.annotate(f"Model work is {model_eff:g} of {total_eff:g} weeks of effort, "
            f"{model_eff / total_eff * 100:.0f}% of the project",
            xy=(7.5, ys[3]), xytext=(11.2, ys[3] + 2.5), fontsize=12, color=C[1],
            weight="bold",
            arrowprops=dict(arrowstyle="->", color=C[1], lw=1.8,
                            connectionstyle="arc3,rad=0.25"))

ax.legend(handles=[Patch(fc=C[0], label="effort: someone is working"),
                   Patch(fc=C[1], label="effort: model work"),
                   Patch(fc=GRID, ec="#d8d6d0", label="elapsed: waiting on someone else")],
          loc="lower left", bbox_to_anchor=(0, 1.005), ncol=3, fontsize=11)

fig.suptitle(f"{total_eff:g} weeks of work spread over {end:g} weeks of calendar",
             x=0.01, ha="left", fontsize=15, weight="bold")
fig.text(0.01, 0.935, "Illustrative shape for a mid-sized deployment, not measured from one project.",
         ha="left", va="top", fontsize=11.5, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-effort-vs-duration.png")

print(f"effort {total_eff:g}w   calendar {end:g}w   model share {model_eff/total_eff*100:.0f}%")
