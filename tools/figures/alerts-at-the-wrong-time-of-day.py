"""Figures for alerts-at-the-wrong-time-of-day. A diagram with example values, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, CRIT, GOOD, save

SLUG = "alerts-at-the-wrong-time-of-day"


def box(ax, x, y, w, h, color, title, lines):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "22", ec=color, lw=1.6))
    ax.text(x + 0.18, y + h - 0.32, title, fontsize=12.5, weight="bold", va="center")
    ax.text(x + 0.18, y + h - 0.68, lines, fontsize=10.8, color=INK2, va="top", linespacing=1.4)


fig, ax = plt.subplots(figsize=(12, 5.4))
ax.set_xlim(0, 12.2); ax.set_ylim(0, 5.6); ax.axis("off")
ax.text(0.1, 5.4, "One event, four clocks: decide which one the pipeline trusts", fontsize=14, weight="bold", va="center")
box(ax, 0.1, 2.3, 2.7, 2.6, C[1], "Camera clock", "overlay: 18:07:12\nno NTP, drifted\n+7 min since install")
box(ax, 3.1, 2.3, 2.7, 2.6, C[3], "Stream timestamps", "RTP / PTS:\ngood for intervals,\nnot for time of day")
box(ax, 6.1, 2.3, 2.7, 2.6, C[0], "Server clock", "NTP synchronised\nreceive time, stored\nin UTC: 10:00:05Z")
box(ax, 9.1, 2.3, 3.0, 2.6, C[2], "Display", "converted with the\nsite's time zone:\n18:00:05 (UTC+8)")
for x in (2.8, 5.8, 8.8):
    ax.annotate("", xy=(x + 0.3, 3.6), xytext=(x, 3.6), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4))
ax.text(1.45, 1.9, "do not use for logic", ha="center", fontsize=11.5, color=CRIT)
ax.text(4.45, 1.9, "use for durations", ha="center", fontsize=11.5, color=INK2)
ax.text(7.45, 1.9, "use as the event time", ha="center", fontsize=11.5, color=GOOD)
ax.text(10.6, 1.9, "only at the edges", ha="center", fontsize=11.5, color=INK2)
ax.text(0.1, 0.8, "Example values. Schedules ('restricted 22:00-06:00') are written in the site's local time "
        "and evaluated after converting UTC with a named time zone.", fontsize=11, color=INK2)
save(fig, f"{SLUG}-four-clocks.png")
