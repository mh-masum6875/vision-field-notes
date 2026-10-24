"""Figures for read-rtsp-streams-with-opencv."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, save

SLUG = "read-rtsp-streams-with-opencv"


def box(ax, x, y, w, h, title, sub, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=color + "1f", ec=color, lw=1.6))
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=13, weight="bold", color=INK)
    ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=11, color=INK2, linespacing=1.3)


def arrow(ax, x1, y1, x2, y2, color=INK2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16))


# 1. Where each part of the stream is handled
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.set_xlim(0, 100); ax.set_ylim(10, 46); ax.axis("off")
w, h, y = 18.6, 15, 22
xs = [i * 20.35 for i in range(5)]
items = [("IP camera", "encodes\nH.264 / H.265", C[0]),
         ("Network", "RTSP control,\nRTP via UDP/TCP", C[1]),
         ("FFmpeg", "receive, buffer,\ndecode", C[2]),
         ("VideoCapture", "cap.read()\nreturns a frame", C[3]),
         ("Your loop", "inference,\nrules, display", C[6])]
for x, (t, s, c) in zip(xs, items):
    box(ax, x, y, w, h, t, s, c)
for a, b in zip(xs[:-1], xs[1:]):
    arrow(ax, a + w + 0.3, y + h / 2, b - 0.3, y + h / 2)
# bracket over the parts OpenCV delegates
ax.plot([xs[1], xs[1], xs[2] + w, xs[2] + w], [y + h + 2, y + h + 4, y + h + 4, y + h + 2], color=ACCENT, lw=1.6)
ax.text((xs[1] + xs[2] + w) / 2, y + h + 5.5, "Transport, buffering and timeouts live here",
        ha="center", va="bottom", fontsize=12, color=ACCENT, weight="bold")
notes = ["Main stream or\nsub stream", "TCP: reliable\nUDP: can smear", "Queues frames if\nyou read slowly",
         "Check the ok flag\nevery time", "Must keep up with\nthe frame rate"]
for x, n in zip(xs, notes):
    ax.text(x + w / 2, y - 3, n, ha="center", va="top", fontsize=11, color=INK2, linespacing=1.3)
save(fig, f"{SLUG}-pipeline.png")


# 2. Latency growth: camera at 25 fps, loop at 10 fps (the article's example)
t = np.linspace(0, 60, 301)
cam_fps, proc_fps = 25.0, 10.0
naive = t * (1 - proc_fps / cam_fps)               # frame processed at time t was captured at t*10/25
latest = np.full_like(t, 1 / proc_fps + 0.5 / cam_fps)  # one processing step plus half a frame interval
fig, ax = plt.subplots(figsize=(9.5, 4.6))
ax.plot(t, naive, color=C[1], lw=2, label="Plain read() loop: every frame queued")
ax.plot(t, latest, color=C[0], lw=2, label="Latest-frame reader: stale frames dropped")
ax.set_xlabel("Seconds since the stream was opened")
ax.set_ylabel("Delay behind real time (s)")
ax.set_xlim(0, 60); ax.set_ylim(0, 40)
ax.set_title("A loop slower than the camera falls further behind every second", loc="left")
ax.text(38, 27, "+0.6 s of delay\nper second", ha="right", va="bottom", fontsize=12, color=INK2)
ax.text(60, latest[-1] + 1.2, "stays bounded", ha="right", va="bottom", fontsize=12, color=INK2)
ax.legend(loc="upper left", fontsize=12)
save(fig, f"{SLUG}-latency.png")
