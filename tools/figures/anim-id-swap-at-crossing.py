"""Animation for tracker-id-switches-and-double-counting.

Schematic, not footage. Two people walk towards each other and pass. While
they overlap the tracker has one blob and two claims on it, and when they
separate it attaches the IDs the wrong way round. Nothing errors; the dwell
timers simply swap people.

Writes content/videos/tracker-id-swap.mp4 and its poster.
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

SLUG = "tracker-id-switches-and-double-counting"
VID = OUT.parent / "videos"

W, H = 640, 360
FPS = 20
DUR = 8.0
N = int(DUR * FPS)
MEET = 0.50                 # when they overlap

frames_dir = Path(tempfile.mkdtemp())

# the two people keep their own colours; the tracker colours boxes by ID
A_COL, B_COL = "#1baf7a", "#6250d6"
ID_COL = {"1": C[0], "2": C[1]}


def positions(u):
    """A walks left to right, B right to left, crossing in the middle."""
    a = 10 + u * 80
    b = 90 - u * 80
    return a, b


for i in range(N):
    u = i / (N - 1)
    ax_, bx = positions(u)
    overlapping = abs(ax_ - bx) < 9

    # after they separate, the IDs have exchanged people
    swapped = u > MEET
    a_id, b_id = ("2", "1") if swapped else ("1", "2")

    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100); ax.set_ylim(0, 56)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

    ax.add_patch(Rectangle((0, 0), 100, 56, fc="#eceae4", ec="none"))
    ax.add_patch(Rectangle((0, 6), 100, 26, fc="#ded8cd", ec="none"))

    # the two people, drawn in their own colours throughout: the person never changes
    for x, col in [(ax_, A_COL), (bx, B_COL)]:
        ax.add_patch(Rectangle((x - 1.8, 11), 3.6, 11, fc=col, ec=INK2, lw=1.1, zorder=5))
        ax.add_patch(Circle((x, 24), 2.1, fc="#f4c7a1", ec=INK2, lw=1.1, zorder=5))

    if overlapping:
        mid = (ax_ + bx) / 2
        ax.add_patch(Rectangle((mid - 7.5, 9), 15, 17, fill=False, ec=WARN, lw=2.6,
                               ls="--", zorder=6))
        ax.text(mid, 28.2, "one blob, two claims", ha="center", fontsize=11,
                color="#8a6d00", weight="bold", zorder=7)
    else:
        for x, tid in [(ax_, a_id), (bx, b_id)]:
            col = ID_COL[tid]
            ax.add_patch(Rectangle((x - 4.4, 9), 8.8, 17, fill=False, ec=col, lw=2.4,
                                   zorder=6))
            ax.text(x, 28.2, f"ID {tid}", ha="center", fontsize=11.5, color=col,
                    weight="bold", zorder=7)

    ax.text(50, 2.6, "green and purple are the people; blue and orange are the IDs",
            ha="center", fontsize=11, color=INK2, va="center")
    if swapped and not overlapping:
        ax.text(50, 50, "the IDs have changed places", ha="center", fontsize=13,
                color=CRIT, weight="bold", va="center")
        ax.text(50, 43.5, "every per-ID timer now belongs to the other person",
                ha="center", fontsize=11, color=CRIT, va="center")
    elif not swapped and not overlapping:
        ax.text(50, 50, "IDs correct", ha="center", fontsize=13, color=GOOD,
                weight="bold", va="center")

    fig.savefig(frames_dir / f"f{i:04d}.png", dpi=100)
    plt.close(fig)

shutil.copyfile(frames_dir / f"f{int(N * 0.86):04d}.png",
                OUT / "tracker-id-swap-poster.png")

VID.mkdir(parents=True, exist_ok=True)
mp4 = VID / "tracker-id-swap.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                "-i", str(frames_dir / "f%04d.png"), "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "26", "-movflags", "+faststart",
                "-an", str(mp4)], check=True)
print(f"mp4 {mp4}  {mp4.stat().st_size/1024:.0f} KB  frames {N}")
