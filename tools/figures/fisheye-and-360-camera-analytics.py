"""Figure for fisheye-and-360-camera-analytics.

A schematic ceiling fisheye view, not a real frame. People are drawn
radially, the way a ceiling fisheye renders them, so the cost of an
axis-aligned box at the edge is visible rather than described.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Ellipse, Wedge

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "fisheye-and-360-camera-analytics"

fig, axs = plt.subplots(1, 2, figsize=(13.0, 6.6),
                        gridspec_kw={"width_ratios": [1.0, 1.05]})

R = 1.0


def person(ax, r, theta, length, width, col):
    """A person lying along the radius, as a ceiling fisheye renders them.

    Directly under the camera you see the top of a head, so the shape is round.
    Towards the rim the body stretches outwards along the radius.
    """
    cx, cy = r * np.cos(theta), r * np.sin(theta)
    ang = np.degrees(theta)
    ax.add_patch(Ellipse((cx, cy), length, width, angle=ang, fc=col, ec=INK2,
                         lw=1.3, zorder=5))
    if r > 0.12:                       # a head is only visible away from the centre
        hx = (r + length * 0.30) * np.cos(theta)
        hy = (r + length * 0.30) * np.sin(theta)
        ax.add_patch(Circle((hx, hy), width * 0.40, fc="#f4c7a1", ec=INK2, lw=1.2,
                            zorder=6))
    else:
        ax.add_patch(Circle((cx, cy), width * 0.42, fc="#f4c7a1", ec=INK2, lw=1.2,
                            zorder=6))
    return cx, cy, ang, length, width


def frame(ax, title):
    ax.set_xlim(-1.62, 1.62); ax.set_ylim(-1.52, 1.52)
    ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Circle((0, 0), R, fc="#eceae4", ec=INK2, lw=2.0, zorder=1))
    for rr in (0.33, 0.66):
        ax.add_patch(Circle((0, 0), rr, fc="none", ec=GRID, lw=1.1, ls=":", zorder=2))
    ax.set_title(title, fontsize=13, loc="left", pad=10)


PEOPLE = [(0.0, 1.57, 0.17, 0.17), (0.50, 3.49, 0.30, 0.15), (0.82, 5.76, 0.40, 0.13)]

# ---- left: axis-aligned boxes
frame(axs[0], "Axis-aligned boxes on the raw fisheye")
for r, th, ln, wd in PEOPLE:
    cx, cy, ang, L, W = person(axs[0], r, th, ln, wd, C[0])
    # the axis-aligned box that must contain the rotated ellipse
    a, b = L / 2, W / 2
    t = th
    hw = np.sqrt((a * np.cos(t)) ** 2 + (b * np.sin(t)) ** 2)
    hh = np.sqrt((a * np.sin(t)) ** 2 + (b * np.cos(t)) ** 2)
    fill = (np.pi * a * b) / (4 * hw * hh) * 100
    col = GOOD if fill > 60 else CRIT
    axs[0].add_patch(Rectangle((cx - hw, cy - hh), 2 * hw, 2 * hh, fill=False,
                               ec=col, lw=2.2, ls="--", zorder=7))
    # park the label outside the disc, on the same bearing as the person
    lab_th = np.radians(90) if r == 0 else th
    lx, ly = 1.34 * np.cos(lab_th), 1.34 * np.sin(lab_th)
    axs[0].annotate(f"{fill:.0f}% of the box\nis the person", xy=(cx, cy),
                    xytext=(lx, ly), ha="center", va="center", fontsize=10.5,
                    color=col, weight="bold", linespacing=1.3, zorder=8,
                    bbox=dict(fc="white", ec=col, lw=1.1, boxstyle="round,pad=0.24"),
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.4))

# ---- right: the three ways out
frame(axs[1], "Three ways to deal with it")
for r, th, ln, wd in PEOPLE:
    person(axs[1], r, th, ln, wd, MUTED)

for k, (a0, a1, lab, col) in enumerate([
        (35, 145, "dewarp into\nvirtual views", C[0]),
        (155, 265, "train on the\nwarped frames", C[2]),
        (275, 385, "detect warped,\nreason in world\ncoordinates", C[3])]):
    axs[1].add_patch(Wedge((0, 0), R, a0, a1, width=0.30, fc=col, alpha=0.30,
                           ec=col, lw=1.8, zorder=4))
    mid = np.radians((a0 + a1) / 2)
    axs[1].text(1.19 * np.cos(mid), 1.19 * np.sin(mid), lab, ha="center", va="center",
                fontsize=11, color=col, weight="bold", linespacing=1.3, zorder=8,
                bbox=dict(fc="white", ec=col, lw=1.3, boxstyle="round,pad=0.26"))



fig.suptitle("At the rim a person is sideways, and the box around them is mostly floor",
             x=0.008, ha="left", fontsize=15, weight="bold")
fig.text(0.008, 0.925,
         "Schematic ceiling fisheye, not a real frame. The percentage is the ellipse's area "
         "as a share of its axis-aligned box.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-radial-distortion.png")

for r, th, ln, wd in PEOPLE:
    a, b, t = ln / 2, wd / 2, th
    hw = np.sqrt((a * np.cos(t)) ** 2 + (b * np.sin(t)) ** 2)
    hh = np.sqrt((a * np.sin(t)) ** 2 + (b * np.cos(t)) ** 2)
    print(f"r={r:.2f}  box fill {(np.pi*a*b)/(4*hw*hh)*100:.0f}%")
