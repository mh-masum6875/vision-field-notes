"""Figure for turning-down-a-computer-vision-project.

Pure geometry, not measurements. Horizontal pixels across a target are

    px = object_width / (2 * distance * tan(hfov / 2)) * image_width

so the answer to "can the camera see it?" is arithmetic you can do in the
first meeting, before anyone writes code.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "turning-down-a-computer-vision-project"

IMG_W = 1920          # a 1080p camera
PLATE_W = 0.52        # metres, a European number plate

LENSES = [(90, "wide overview, 90°"), (50, "medium, 50°"), (20, "zoomed in, 20°")]
dist = np.linspace(3, 70, 400)


def px_across(width_m, distance_m, hfov_deg, image_w=IMG_W):
    scene_w = 2 * distance_m * np.tan(np.radians(hfov_deg) / 2)
    return width_m / scene_w * image_w


fig, ax = plt.subplots(figsize=(12.2, 6.4))

# what each task needs across the plate, as commonly quoted for ANPR
BANDS = [
    (0, 25, "#fdecec", CRIT, "nothing usable"),
    (25, 70, "#fdf4e6", WARN, "a box, but no characters"),
    (70, 400, "#eaf6ee", GOOD, "characters readable"),
]
for lo, hi, fc, ec, label in BANDS:
    ax.axhspan(lo, hi, color=fc, zorder=0)
    ax.text(69.4, lo + (min(hi, 185) - lo) / 2, label, ha="right", va="center",
            fontsize=11.5, color=ec, weight="bold", zorder=4,
            bbox=dict(fc="white", ec="none", alpha=0.82, boxstyle="round,pad=0.22"))

for (hfov, name), col in zip(LENSES, [C[0], C[2], C[3]]):
    ax.plot(dist, px_across(PLATE_W, dist, hfov), lw=2.4, color=col, label=name, zorder=3)

# the example from the post: 60 m on a wide overview camera
d_ex, hf_ex = 60, 90
px_ex = px_across(PLATE_W, d_ex, hf_ex)
ax.plot([d_ex], [px_ex], marker="o", ms=11, mfc=CRIT, mec="white", mew=2, zorder=5)
ax.annotate(f"a plate at {d_ex} m on the wide camera\nis {px_ex:.0f} pixels across",
            xy=(d_ex, px_ex), xytext=(44, 92), fontsize=12, color=CRIT, weight="bold",
            linespacing=1.4, zorder=6,
            arrowprops=dict(arrowstyle="->", color=CRIT, lw=1.9,
                            connectionstyle="arc3,rad=0.22"))

# where the wide camera stops being able to read
reach = PLATE_W / (70 / IMG_W) / (2 * np.tan(np.radians(90) / 2))
ax.plot([reach, reach], [0, 70], color=C[0], lw=1.6, ls=":", zorder=3)
ax.text(reach + 0.7, 150, f"the wide camera can only read\na plate closer than {reach:.1f} m",
        fontsize=11.5, color=C[0], weight="bold", linespacing=1.4, zorder=6)

ax.set_xlim(3, 70)
ax.set_ylim(0, 185)
ax.set_xlabel("distance from camera (metres)")
ax.set_ylabel("pixels across a 52 cm number plate")
ax.legend(title="1080p camera, horizontal field of view", title_fontsize=11,
          fontsize=11, loc="upper right")

fig.suptitle("No model recovers detail the lens never captured",
             x=0.01, ha="left", fontsize=15.5, weight="bold")
fig.text(0.01, 0.925,
         "Geometry only: pixels across = object width / scene width at that distance × 1920. "
         "The bands are the usual rules of thumb for plate reading.",
         ha="left", va="top", fontsize=11.3, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.885])
save(fig, f"{SLUG}-pixels-on-target.png")

for d in (10, 20, 40, 60):
    print(f"{d:3} m  90°: {px_across(PLATE_W, d, 90):5.1f} px   "
          f"50°: {px_across(PLATE_W, d, 50):5.1f} px   20°: {px_across(PLATE_W, d, 20):5.1f} px")
print(f"wide camera reaches 70 px at {reach:.1f} m")
