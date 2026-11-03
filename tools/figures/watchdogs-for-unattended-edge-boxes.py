"""Figures for watchdogs-for-unattended-edge-boxes. A diagram, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, save

SLUG = "watchdogs-for-unattended-edge-boxes"


def box(ax, x, y, w, h, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "22", ec=color, lw=1.6))


layers = [
    ("Remote monitoring", "device stopped reporting, or keeps restarting", "a person: remote fix or site visit", C[1]),
    ("Application health check", "frames flowing, inference running, queues short", "restart the pipeline", C[6]),
    ("Service manager (systemd)", "process exited or stopped sending heartbeats", "restart the service, with limits", C[0]),
    ("Hardware watchdog", "operating system hung, nothing else can run", "reboot the board", C[2]),
]
fig, ax = plt.subplots(figsize=(11.5, 5.4))
ax.set_xlim(0, 11.5); ax.set_ylim(0, 5.5); ax.axis("off")
ax.text(0.1, 5.3, "Each layer catches what the layer below cannot", fontsize=14, weight="bold", va="center")
ax.text(4.3, 4.75, "detects", fontsize=11, color=INK2, weight="bold")
ax.text(8.2, 4.75, "action", fontsize=11, color=INK2, weight="bold")
for i, (name, det, act, c) in enumerate(layers):
    y = 3.55 - i * 1.1
    box(ax, 0.1, y, 11.3, 0.9, c)
    ax.text(0.3, y + 0.45, name, fontsize=12.5, weight="bold", va="center")
    ax.text(4.3, y + 0.45, det, fontsize=10.8, color=INK2, va="center")
    ax.text(8.2, y + 0.45, act, fontsize=10.8, color=INK2, va="center")
save(fig, f"{SLUG}-layers.png")
