"""Figure for gstreamer-ffmpeg-or-opencv.

Arithmetic, not a benchmark. If frames arrive faster than you consume them and
nothing drops, the backlog grows by the difference every second, and the age of
the frame you are looking at grows with it.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "gstreamer-ffmpeg-or-opencv"

CAM_FPS = 25
PROC_FPS = 18          # a detector that cannot quite keep up
MINUTES = 5
t = np.linspace(0, MINUTES * 60, 800)

backlog = (CAM_FPS - PROC_FPS) * t          # frames waiting, if nothing is dropped
age_queued = backlog / CAM_FPS              # seconds behind live
age_latest = np.full_like(t, 1 / PROC_FPS)  # keep only the newest frame

fig, axs = plt.subplots(1, 2, figsize=(12.8, 5.4),
                        gridspec_kw={"width_ratios": [1.3, 1.0]})

ax = axs[0]
ax.plot(t / 60, age_queued, lw=2.8, color=CRIT, label="read every frame in order")
ax.plot(t / 60, age_latest, lw=2.8, color=GOOD, label="keep only the latest frame")
for mins in (1, 3, 5):
    v = (CAM_FPS - PROC_FPS) * mins * 60 / CAM_FPS
    ax.plot([mins], [v], marker="o", ms=9, mfc=CRIT, mec="white", mew=1.8, zorder=6)
    ax.annotate(f"{v:.0f} s behind", (mins, v), xytext=(-8, 12),
                textcoords="offset points", ha="right", fontsize=11.4, color=CRIT,
                weight="bold")
ax.set_xlabel("minutes since the stream started")
ax.set_ylabel("how old the frame you are processing is (s)")
ax.set_title(f"Camera sends {CAM_FPS} fps, the pipeline handles {PROC_FPS}",
             fontsize=12.5, loc="left")
ax.set_xlim(0, MINUTES)
ax.legend(fontsize=11, loc="upper left")

# ---- what that means for an alert
ax = axs[1]
mins = np.array([0.5, 1, 2, 5])
delay = (CAM_FPS - PROC_FPS) * mins * 60 / CAM_FPS
bars = ax.bar(np.arange(len(mins)), delay, 0.6,
              color=[GOOD if d < 10 else (WARN if d < 60 else CRIT) for d in delay])
for i, d in enumerate(delay):
    ax.text(i, d + 2.5, f"{d:.0f} s", ha="center", fontsize=12.5, weight="bold",
            color=INK)
ax.axhline(10, color=INK2, lw=1.6, ls="--")
ax.text(1.5, 24, "10 s: an alert nobody\ncan act on", ha="center", fontsize=11,
        color=INK2, linespacing=1.3)
ax.set_xticks(np.arange(len(mins)), [f"{m:g} min" for m in mins], fontsize=11.5)
ax.set_xlabel("time since the stream started")
ax.set_ylabel("alert delay (s)")
ax.set_title("The alert is late by the whole backlog", fontsize=12.5, loc="left")
ax.grid(axis="x", visible=False)

fig.suptitle(f"A {CAM_FPS - PROC_FPS}-frame-per-second shortfall is "
             f"{(CAM_FPS - PROC_FPS) * 60 / CAM_FPS:.0f} seconds of lag per minute",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.925,
         "Arithmetic, not a benchmark. The backlog grows whenever frames are queued "
         "rather than dropped, whichever library queues them.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-backlog.png")

for m in (1, 2, 5, 10):
    print(f"after {m:2} min: {(CAM_FPS-PROC_FPS)*m*60/CAM_FPS:6.0f} s behind live "
          f"({(CAM_FPS-PROC_FPS)*m*60:.0f} frames queued)")
