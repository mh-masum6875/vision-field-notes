"""Animation for variable-frame-rate-at-night.

Schematic, not footage. The same person walks the same path at the same speed.
On the left the camera delivers 25 fps, on the right it has dropped to 6 fps
for a longer exposure. The detections are identical; only how many of them
arrive changes, and the gap between them is what breaks the association.

Writes content/videos/frame-rate-and-tracking.mp4 and its poster.
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

SLUG = "variable-frame-rate-at-night"
VID = OUT.parent / "videos"

W, H = 760, 380
FPS = 20
DUR = 3.2          # seconds of scene time; a brisk walk through a doorway view
N = int(DUR * FPS)

DAY_FPS, NIGHT_FPS = 25, 5
BOX_W = 9.0        # the detection box, in the same units as the corridor
IOU_MIN = 0.30     # SORT-style association: boxes must overlap at least this much


def iou_1d(gap, w=BOX_W):
    """Overlap of two equal boxes offset horizontally. A 1-D stand-in for IoU."""
    inter = max(0.0, w - abs(gap))
    return inter / (2 * w - inter) if (2 * w - inter) > 0 else 0.0

frames_dir = Path(tempfile.mkdtemp())


def walked(u):
    """Position along the corridor, 0..100, at constant speed."""
    return 6 + u * 88


for i in range(N):
    u = i / (N - 1)
    x_true = walked(u)
    t_s = u * DUR

    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100); ax.set_ylim(-1, 60)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.add_patch(Rectangle((0, 0), 100, 60, fc="#eceae4", ec="none"))

    for row, (cam_fps, label, col) in enumerate(
            [(DAY_FPS, f"{DAY_FPS} fps, daytime", GOOD),
             (NIGHT_FPS, f"{NIGHT_FPS} fps, slow shutter at night", CRIT)]):
        y0 = 33 - row * 26
        ax.add_patch(Rectangle((0, y0), 100, 20, fc="#ded8cd", ec="none"))
        ax.text(2, y0 + 17.2, label, fontsize=11.6, color=col, weight="bold")

        # the frames this camera has actually delivered by now
        step_u = (1 / cam_fps) / DUR
        ticks = np.arange(0, u + 1e-9, step_u)
        if len(ticks) == 0:
            ticks = np.array([0.0])
        xs = walked(ticks)

        # ghosts of recent detections, so the sampling is visible
        for xg in xs[-6:-1]:
            ax.add_patch(Rectangle((xg - 2.6, y0 + 3), 5.2, 11, fc=col, alpha=0.16,
                                   ec="none", zorder=3))

        x_last = xs[-1]
        jump = x_last - xs[-2] if len(xs) > 1 else 0.0

        ax.add_patch(Rectangle((x_last - 2.0, y0 + 3.5), 4.0, 10,
                               fc=C[3], ec=INK2, lw=1.0, zorder=5))
        ax.add_patch(Circle((x_last, y0 + 15), 2.0, fc="#f4c7a1", ec=INK2, lw=1.0,
                            zorder=5))

        overlap = iou_1d(jump)
        lost = len(xs) > 1 and overlap < IOU_MIN
        box_col = CRIT if lost else col
        ax.add_patch(Rectangle((x_last - 4.6, y0 + 2), 9.2, 15, fill=False,
                               ec=box_col, lw=2.3, ls="--" if lost else "-", zorder=6))

        if len(xs) > 1:
            ax.annotate("", xy=(x_last - 4.6, y0 + 9), xytext=(xs[-2] + 4.6, y0 + 9),
                        arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.4))
            note = f"moved {jump:.1f},  overlap {overlap:.2f}"
            if lost:
                note += f"  \u2192  below {IOU_MIN:.2f}, new ID"
            ax.text(50, y0 - 3.0, note, ha="center", fontsize=10.6,
                    color=CRIT if lost else INK2, zorder=7,
                    weight="bold" if lost else "normal")

        ax.text(97, y0 + 17.2, f"{len(ticks)} frames so far", ha="right", fontsize=10.8,
                color=INK2)


    ax.text(50, 57, f"same person, same speed, {t_s:.1f} s in", ha="center",
            fontsize=12.4, color=INK, weight="bold")
    

    fig.savefig(frames_dir / f"f{i:04d}.png", dpi=100)
    plt.close(fig)

shutil.copyfile(frames_dir / f"f{int(N * 0.6):04d}.png",
                OUT / "frame-rate-and-tracking-poster.png")

VID.mkdir(parents=True, exist_ok=True)
mp4 = VID / "frame-rate-and-tracking.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                "-i", str(frames_dir / "f%04d.png"), "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "26", "-movflags", "+faststart",
                "-an", str(mp4)], check=True)

for f in (DAY_FPS, NIGHT_FPS):
    step = 88 / DUR / f
    print(f"{f:2} fps: {step:5.2f} units between frames, overlap {iou_1d(step):.2f} "
          f"-> {'associates' if iou_1d(step) >= IOU_MIN else 'NEW ID'}")
print(f"mp4 {mp4}  {mp4.stat().st_size/1024:.0f} KB")
