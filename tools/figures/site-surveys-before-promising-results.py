"""Figure for site-surveys-before-promising-results.

A schematic yard with one camera, annotated with the things the survey has to
produce a number for. Not a real site; it is the checklist drawn in place, so
each item is attached to the thing it is about.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "site-surveys-before-promising-results"

fig, ax = plt.subplots(figsize=(12.8, 7.4))
ax.set_xlim(0, 100)
ax.set_ylim(0, 58)
ax.axis("off")

# ground and building
ax.add_patch(Rectangle((2, 4), 96, 44, fc="#f2efe9", ec=GRID, lw=1.4))
ax.add_patch(Rectangle((2, 34), 30, 14, fc="#ded8cd", ec=INK2, lw=1.5))
ax.text(17, 41, "building", ha="center", fontsize=11.5, color=INK2, weight="bold")

CAM = (12, 30)
ax.add_patch(Circle(CAM, 1.5, fc=INK, ec="white", lw=1.6, zorder=6))
ax.text(CAM[0] + 2.4, CAM[1] - 0.2, "camera, 4.5 m up", fontsize=11.4, color=INK,
        weight="bold", va="center")

# field of view
# the cone is kept inside the site so the drawing stays readable
fov = Polygon([CAM, (74, 6.5), (94, 33)],
              closed=True, fc=C[0], alpha=0.13, ec=C[0], lw=1.6, zorder=2)
ax.add_patch(fov)

# the area of interest
ax.add_patch(Rectangle((40, 12), 30, 16, fc=GOOD, alpha=0.16, ec=GOOD, lw=2.0, ls="--",
                       zorder=3))
ax.text(55, 20, "area of interest", ha="center", fontsize=12, color="#0b5c22",
        weight="bold", zorder=4)

# near and far points, with the pixel counts that decide the job
for (px, py), dist, pix, col in [((42, 26), 18, 74, GOOD), ((68, 14), 44, 30, CRIT)]:
    ax.plot([CAM[0], px], [CAM[1], py], color=col, lw=1.8, ls=":", zorder=4)
    ax.add_patch(Circle((px, py), 1.1, fc=col, ec="white", lw=1.4, zorder=6))
    ax.text(px + 1.8, py - 0.3, f"{dist} m\na person is {pix} px tall",
            fontsize=11, color=col, weight="bold", linespacing=1.35, zorder=6,
            bbox=dict(fc="white", ec=col, lw=1.2, boxstyle="round,pad=0.3"))

# obstructions and conditions, each pinned to where it bites
ax.add_patch(Rectangle((33, 20), 3, 18, fc="#9a958c", ec=INK2, lw=1.3, zorder=5))
ax.text(34.5, 39.5, "pillar:\noccludes", ha="center", fontsize=10.6, color=INK2,
        weight="bold", linespacing=1.3)

ax.add_patch(Rectangle((70, 29), 16, 7.5, fc=C[0], alpha=0.5, ec=INK2, lw=1.3, zorder=5))
ax.text(78, 32.7, "parked vehicles\nmove", ha="center", fontsize=10.6, color=INK2,
        weight="bold", linespacing=1.3, zorder=6)

ax.add_patch(Circle((90, 44.5), 2.6, fc="#ffd400", ec="#d8a800", lw=1.4, zorder=5))
ax.text(90, 40.6, "low sun into\nthe lens at dusk", ha="center", va="top", fontsize=10.6,
        color="#8a6d00", weight="bold", linespacing=1.3)

ax.add_patch(Rectangle((2, 4), 22, 8, fc="#e8e4dc", ec=INK2, lw=1.3, zorder=5))
ax.text(13, 8, "comms cabinet\npower, PoE, uplink", ha="center", fontsize=10.6,
        color=INK2, weight="bold", linespacing=1.3, zorder=6)

ax.add_patch(FancyArrowPatch((24, 8), (40, 8), arrowstyle="-|>", mutation_scale=15,
                             color=INK2, lw=1.6, zorder=5))
ax.text(42, 8, "how do the streams get out, and at what bitrate?",
        fontsize=11, color=INK2, va="center")

ax.text(2, 53.5, "Every label here is a number the survey has to come back with",
        fontsize=12.6, color=INK, weight="bold")
ax.text(2, 50.6, "Distances, pixel heights, what blocks the view, where the light comes "
                 "from, and how the stream reaches the compute.",
        fontsize=11.3, color=INK2)

fig.suptitle("The survey decides the project; the model only reflects it",
             x=0.008, ha="left", fontsize=15.5, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.955])
save(fig, f"{SLUG}-what-to-measure.png")
print("rendered site survey figure")
