"""Animation for ptz-cameras-and-analytics.

A schematic yard, not footage. The zone is drawn in image coordinates, the way
analytics software stores it, so it stays where it is on screen while the
camera pans and the scene slides underneath it.

Writes content/videos/ptz-zone-drift.mp4 and a matching poster PNG.
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
from matplotlib.path import Path as MplPath

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save, OUT

SLUG = "ptz-cameras-and-analytics"
VID = OUT.parent / "videos"

W, H = 640, 360          # the camera's view, in pixels
FPS = 20
WORLD_W = 1500

# the zone, in IMAGE coordinates: fractions of the frame, fixed to the screen
ZONE = np.array([[0.46, 0.22], [0.76, 0.22], [0.78, 0.62], [0.44, 0.62]])
zone_path = MplPath(ZONE)


def camera_x(t):
    """Pan: hold on the preset, swing right, hold again.

    The swing is small enough that the gate stays in shot afterwards, so you
    can see the zone sitting somewhere else while the gate is still visible.
    """
    if t < 0.34:
        return 150.0
    if t < 0.50:
        u = (t - 0.34) / 0.16
        u = u * u * (3 - 2 * u)                  # ease in and out
        return 150.0 + u * 150.0
    return 300.0


def person_x(t):
    """Walks past the gate twice, once before the pan and once after."""
    if t < 0.34:
        return 180 + (t / 0.34) * 300            # reaches the gate at 423
    if t < 0.50:
        return None                              # off frame during the move
    return 320 + ((t - 0.50) / 0.50) * 360       # gate at 423, then on to the zone


def draw_world(ax):
    ax.add_patch(Rectangle((-50, 0), WORLD_W + 100, 150, fc="#dcd8cf", ec="none"))      # ground
    ax.add_patch(Rectangle((-50, 150), WORLD_W + 100, 300, fc="#cfe0ef", ec="none"))    # sky
    # building with a gate opening
    ax.add_patch(Rectangle((300, 140), 240, 170, fc="#b9b4aa", ec=INK2, lw=1.4))
    ax.add_patch(Rectangle((392, 140), 62, 104, fc="#4a4640", ec=INK2, lw=1.4))
    ax.text(423, 320, "gate", ha="center", fontsize=11, color=INK2, weight="bold")
    # fence
    for fx in range(560, 1180, 44):
        ax.plot([fx, fx], [140, 215], color="#9a958c", lw=2.2, zorder=2)
    ax.plot([560, 1180], [212, 212], color="#9a958c", lw=2.2, zorder=2)
    # empty tarmac to the right, which is where the zone ends up
    ax.add_patch(Rectangle((700, 60), 320, 78, fc="#c9c4ba", ec="none"))
    ax.text(860, 100, "empty tarmac", ha="center", fontsize=11, color=MUTED)
    # a parked van, so the pan is legible
    ax.add_patch(Rectangle((1080, 95), 150, 72, fc=C[0], ec=INK2, lw=1.4))
    ax.add_patch(Circle((1115, 92), 15, fc="#2b2b2b", ec="none"))
    ax.add_patch(Circle((1196, 92), 15, fc="#2b2b2b", ec="none"))
    ax.plot([-50, WORLD_W + 100], [140, 140], color="#a7a299", lw=1.6)


frames_dir = Path(tempfile.mkdtemp())
N = int(7.5 * FPS)

for i in range(N):
    t = i / (N - 1)
    cx = camera_x(t)
    px = person_x(t)

    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(cx, cx + 520)
    ax.set_ylim(0, 300)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

    draw_world(ax)

    inside = False
    if px is not None:
        # feet position, converted to the image fractions the zone is stored in
        fx = (px - cx) / 520.0
        fy = 92 / 300.0
        inside = bool(zone_path.contains_point((fx, fy))) and 0 <= fx <= 1
        if -0.08 <= fx <= 1.08:
            ax.add_patch(Circle((px, 112), 11, fc="#f4c7a1", ec=INK2, lw=1.2, zorder=6))
            ax.add_patch(Rectangle((px - 10, 60), 20, 44, fc=C[3], ec=INK2, lw=1.2, zorder=6))
            ax.plot([px - 5, px - 5], [36, 60], color=INK2, lw=3, zorder=6)
            ax.plot([px + 5, px + 5], [36, 60], color=INK2, lw=3, zorder=6)

    zcol = CRIT if inside else C[2]
    ax.add_patch(Polygon(ZONE, closed=True, transform=ax.transAxes, zorder=8,
                         fc=zcol, ec=zcol, alpha=0.20, lw=0))
    ax.add_patch(Polygon(ZONE, closed=True, transform=ax.transAxes, zorder=9,
                         fill=False, ec=zcol, lw=2.6, ls="--"))
    ax.text(0.61, 0.655, "intrusion zone", transform=ax.transAxes, ha="center",
            fontsize=11, color=zcol, weight="bold", zorder=10)

    panning = 0.34 <= t < 0.50
    label = "camera panning" if panning else ("preset 1" if t < 0.34 else "preset 2")
    ax.text(0.018, 0.955, label, transform=ax.transAxes, va="top", fontsize=12,
            color="white", weight="bold", zorder=11,
            bbox=dict(fc=INK2 if not panning else WARN, ec="none",
                      boxstyle="round,pad=0.34"))

    if inside:
        ax.text(0.982, 0.955, "ALERT", transform=ax.transAxes, ha="right", va="top",
                fontsize=13, color="white", weight="bold", zorder=11,
                bbox=dict(fc=CRIT, ec="none", boxstyle="round,pad=0.34"))
    elif t >= 0.50 and px is not None and 385 <= px <= 470:
        # standing in the gateway, which is what the zone was drawn around
        ax.text(0.982, 0.955, "no alert", transform=ax.transAxes, ha="right", va="top",
                fontsize=13, color=INK, weight="bold", zorder=11,
                bbox=dict(fc="white", ec=GRID, boxstyle="round,pad=0.34"))

    fig.savefig(frames_dir / f"f{i:04d}.png", dpi=100)
    plt.close(fig)
POSTER_FRAME = 12
shutil.copyfile(frames_dir / f"f{POSTER_FRAME:04d}.png", OUT / "ptz-zone-drift-poster.png")

VID.mkdir(parents=True, exist_ok=True)
mp4 = VID / "ptz-zone-drift.mp4"
subprocess.run(
    ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
     "-i", str(frames_dir / "f%04d.png"),
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26",
     "-movflags", "+faststart", "-an", str(mp4)],
    check=True)

print("frames:", N, " mp4:", mp4, f"{mp4.stat().st_size/1024:.0f} KB")
print("poster:", OUT / "ptz-zone-drift-poster.png")
