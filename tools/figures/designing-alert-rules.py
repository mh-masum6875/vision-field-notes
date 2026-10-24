"""Figures for designing-alert-rules."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, CRIT, WARN, save

SLUG = "designing-alert-rules"


def box(ax, x, y, w, h, title, sub, color, title_size=13):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=color + "1f", ec=color, lw=1.6))
    if sub:
        ax.text(x + w / 2, y + h - 3.2, title, ha="center", va="center", fontsize=title_size, weight="bold", color=INK)
        ax.text(x + w / 2, y + (h - 5) / 2, sub, ha="center", va="center", fontsize=11.5, color=INK2, linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=title_size, weight="bold", color=INK)


def arrow(ax, p, q, text=None, color=INK2):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16))
    if text:
        ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 1.2, text, ha="center", va="bottom", fontsize=11, color=INK2)


# ---------------------------------------------------------------- 1. the rule layer
fig, ax = plt.subplots(figsize=(10, 5.0))
ax.set_xlim(0, 100); ax.set_ylim(0, 54); ax.axis("off")
box(ax, 0, 27, 16.5, 14, "Detections", "per frame,\nnoisy", C[0])
box(ax, 20, 27, 19, 14, "Confirm", "N of M frames or\na min. duration", C[1])
box(ax, 42.5, 27, 15, 14, "Events", "facts, all\nstored", C[2])
box(ax, 61, 21, 18, 26, "Rule", "scope\nschedule\nstream health\ncooldown\nseverity", C[6])
box(ax, 82.5, 27, 17.5, 14, "Alert", "with snapshot\nand context", CRIT)
arrow(ax, (16.8, 34), (19.7, 34))
arrow(ax, (39.3, 34), (42.2, 34))
arrow(ax, (57.8, 34), (60.7, 34))
arrow(ax, (79.3, 34), (82.2, 34))
# lower row: storage and delivery
box(ax, 38, 3, 23, 12, "Event store", "audit trail, tuning,\nreplay new rules", C[2])
arrow(ax, (50, 26.7), (50, 15.3))
box(ax, 67, 3, 33, 12, "Delivery", "queue, retry, rate limit\nescalate if not acknowledged", C[3])
arrow(ax, (91.25, 26.7), (88, 15.3))
ax.text(0, 53.5, "Store every event; interrupt people only when a rule says so",
        ha="left", va="top", fontsize=13, weight="bold", color=ACCENT)
save(fig, f"{SLUG}-rule-layer.png")


# ---------------------------------------------------------------- 2. cooldown and reminder on one evening (illustrative)
# presence intervals in a zone, minutes after 22:00; IDs change during long stays, so events repeat
presence = [(4, 9), (21, 58), (75, 79)]
events = [4, 21, 23.5, 27, 33, 34.5, 41, 47, 52, 75]
COOLDOWN, REMIND = 15, 30


def with_cooldown(evts, pres):
    alerts, reminders, last = [], [], -1e9
    for e in evts:
        if e - last >= COOLDOWN:
            alerts.append(e); last = e
    for a, b in pres:                     # reminder if a condition persists past REMIND minutes
        if b - a > REMIND:
            reminders.append(a + REMIND)
    return alerts, reminders


cd_alerts, reminders = with_cooldown(events, presence)
rows = ["Person in zone", "Events", "Alerts, no cooldown", f"Alerts, {COOLDOWN} min cooldown"]
fig, ax = plt.subplots(figsize=(10, 4.2))
Y = {r: len(rows) - 1 - i for i, r in enumerate(rows)}
for a, b in presence:
    ax.add_patch(plt.Rectangle((a, Y[rows[0]] - 0.22), b - a, 0.44, color=C[0], alpha=0.85, lw=0))
ax.scatter(events, [Y[rows[1]]] * len(events), s=55, color=C[2], zorder=3)
ax.scatter(events, [Y[rows[2]]] * len(events), s=70, marker="v", color=C[1], zorder=3)
ax.scatter(cd_alerts, [Y[rows[3]]] * len(cd_alerts), s=70, marker="v", color=C[1], zorder=3, label="alert")
ax.scatter(reminders, [Y[rows[3]]] * len(reminders), s=80, marker="D", color=C[3], zorder=3,
           label=f"reminder: still present after {REMIND} min")
for i, a in enumerate(cd_alerts):
    ax.add_patch(plt.Rectangle((a, Y[rows[3]] - 0.12), COOLDOWN, 0.24, color=GRID, lw=0, zorder=1,
                               label="cooldown window" if i == 0 else None))
ax.text(91, Y[rows[2]], f"{len(events)} messages", va="center", fontsize=12, color=INK2)
ax.text(91, Y[rows[3]], f"{len(cd_alerts) + len(reminders)} messages", va="center", fontsize=12, color=INK2)
ax.set_yticks(list(Y.values())); ax.set_yticklabels(list(Y.keys()))
ax.set_ylim(-0.7, len(rows) - 0.3)
ax.set_xlim(0, 100)
ax.set_xticks(range(0, 91, 15)); ax.set_xticklabels([f"22:{m:02d}" if m < 60 else f"23:{m - 60:02d}" for m in range(0, 91, 15)])
ax.grid(axis="y", visible=False)
ax.set_xlabel("Local time")
ax.set_title("A cooldown turns a stream of repeat events into a few useful messages", loc="left")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=12)
save(fig, f"{SLUG}-cooldown-timeline.png")
print("alerts with cooldown:", cd_alerts, "reminders:", reminders)
