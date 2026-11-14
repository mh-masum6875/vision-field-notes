"""Animation for people-counting-line-crossing.

Schematic, not footage. One person walks up to the line and hesitates on it.
The detector flickers while they are stationary, the tracker issues new IDs,
and a naive rule counts every one of them. A rule with a margin and a cooldown
counts the single crossing that actually happened.

Writes content/videos/line-crossing-loitering.mp4 and its poster.
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save, OUT

SLUG = "people-counting-line-crossing"
VID = OUT.parent / "videos"

W, H = 640, 360
FPS = 20
DUR = 9.0
N = int(DUR * FPS)

LINE_X = 50.0            # the counting line, in scene units (0..100)
MARGIN = 6.0             # hysteresis band for the better rule
COOLDOWN = 1.2           # seconds one ID must wait before it can count again

rng = np.random.default_rng(4)


def walk(t):
    """Approach, hesitate right on the line, then carry on through."""
    if t < 0.30:
        return 14 + (t / 0.30) * 34                      # 14 -> 48
    if t < 0.68:
        u = (t - 0.30) / 0.38
        return 48 + 4.0 * np.sin(u * 3 * np.pi)          # sways across the line
    return 48 + ((t - 0.68) / 0.32) * 40                 # 48 -> 88


# detections flicker while the person is stationary on the line
t_norm = np.arange(N) / (N - 1)
xs = np.array([walk(t) for t in t_norm])
detected = np.ones(N, dtype=bool)
for a, b in [(0.38, 0.41), (0.49, 0.52), (0.60, 0.63)]:
    detected[(t_norm >= a) & (t_norm <= b)] = False

# a new ID every time the track comes back
track_id = np.zeros(N, dtype=int)
tid = 1
for i in range(N):
    if not detected[i]:
        track_id[i] = 0
        if i + 1 < N and detected[i + 1]:
            tid += 1
    else:
        track_id[i] = tid

# ---- run both counting rules over the same data
naive, guarded = 0, 0
naive_events, guarded_events = [], []
prev_side = {}
last_count_t = {}
for i in range(N):
    if not detected[i]:
        continue
    k, x = track_id[i], xs[i]
    side = 1 if x > LINE_X else -1
    if k in prev_side and prev_side[k] != side and side == 1:
        naive += 1
        naive_events.append(i)
    prev_side[k] = side

# The better rule re-links a fragment: a track that appears close in space and
# time to one that just vanished is treated as the same person, so the zone it
# started in is not forgotten every time the detector blinks.
RELINK_S, RELINK_DIST = 0.8, 10.0
logical = {}            # tracker id -> logical id
state = {}              # logical id -> {"zone", "last_t", "last_x", "counted_t"}
next_logical = 1
for i in range(N):
    if not detected[i]:
        continue
    k, x, t = track_id[i], xs[i], i / FPS
    if k not in logical:
        reuse = None
        for lid, st in state.items():
            if t - st["last_t"] <= RELINK_S and abs(x - st["last_x"]) <= RELINK_DIST:
                reuse = lid
                break
        if reuse is None:
            reuse = next_logical
            next_logical += 1
            state[reuse] = {"zone": 0, "last_t": t, "last_x": x, "counted_t": -99}
        logical[k] = reuse
    lid = logical[k]
    st = state[lid]
    st["last_t"], st["last_x"] = t, x
    zone = 1 if x > LINE_X + MARGIN else (-1 if x < LINE_X - MARGIN else 0)
    if zone != 0:
        if st["zone"] == -1 and zone == 1 and t - st["counted_t"] > COOLDOWN:
            guarded += 1
            guarded_events.append(i)
            st["counted_t"] = t
        st["zone"] = zone

print(f"naive rule counts {naive}; with a {MARGIN:g}-unit margin and a "
      f"{COOLDOWN:g}s cooldown it counts {guarded}")

# ---- draw
frames_dir = Path(tempfile.mkdtemp())
n_count, g_count = 0, 0

for i in range(N):
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100); ax.set_ylim(0, 56)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

    ax.add_patch(Rectangle((0, 0), 100, 56, fc="#eceae4", ec="none"))
    ax.add_patch(Rectangle((0, 6), 100, 26, fc="#ded8cd", ec="none"))       # corridor
    ax.axvspan(LINE_X - MARGIN, LINE_X + MARGIN, color=GOOD, alpha=0.14, lw=0)
    ax.plot([LINE_X, LINE_X], [4, 34], color=INK, lw=3, zorder=4)
    ax.text(LINE_X, 36, "counting line", ha="center", fontsize=10.5, color=INK,
            weight="bold")
    ax.text(LINE_X + MARGIN + 0.6, 8.5, "margin", fontsize=9.5, color="#0b5c22")

    if i in naive_events:
        n_count += 1
    if i in guarded_events:
        g_count += 1

    x = xs[i]
    if detected[i]:
        ax.add_patch(Rectangle((x - 4.4, 9), 8.8, 17, fill=False, ec=C[0], lw=2.4,
                               zorder=6))
        ax.text(x, 27.6, f"ID {track_id[i]}", ha="center", fontsize=10.5, color=C[0],
                weight="bold", zorder=7)
    ax.add_patch(Rectangle((x - 1.8, 11), 3.6, 11, fc=C[3], ec=INK2, lw=1.1, zorder=5))
    ax.add_patch(Circle((x, 24), 2.1, fc="#f4c7a1", ec=INK2, lw=1.1, zorder=5))
    if not detected[i]:
        ax.text(x, 30.5, "no detection", ha="center", fontsize=10, color=CRIT,
                weight="bold", zorder=7)

    ax.text(4, 50, f"naive rule:  {n_count}", fontsize=13, color=CRIT, weight="bold",
            va="center")
    ax.text(4, 43, f"margin + cooldown:  {g_count}", fontsize=13, color="#0b5c22",
            weight="bold", va="center")
    ax.text(96, 50, "one person walks through, once", ha="right", fontsize=11,
            color=INK2, va="center")

    fig.savefig(frames_dir / f"f{i:04d}.png", dpi=100)
    plt.close(fig)

shutil.copyfile(frames_dir / f"f{int(N * 0.75):04d}.png",
                OUT / "line-crossing-loitering-poster.png")

VID.mkdir(parents=True, exist_ok=True)
mp4 = VID / "line-crossing-loitering.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                "-i", str(frames_dir / "f%04d.png"), "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "26", "-movflags", "+faststart",
                "-an", str(mp4)], check=True)
print(f"mp4 {mp4}  {mp4.stat().st_size/1024:.0f} KB   final counts: "
      f"naive {n_count}, guarded {g_count}")
