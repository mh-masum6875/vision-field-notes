"""Figures for thermal-cameras-for-detection.

The scene is synthetic: a temperature field built from simple shapes, not a
capture from a real thermal camera. The point is that one field renders to
four completely different sets of pixel values, which is true regardless.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import style
from style import INK, INK2, GRID, save

SLUG = "thermal-cameras-for-detection"

H, W = 150, 230
yy, xx = np.mgrid[0:H, 0:W]
rng = np.random.default_rng(3)


def blob(cx, cy, rx, ry, amp):
    return amp * np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2))


# scene temperature in degrees C: cool ground, cooler sky, a person, a warm engine
scene = np.full((H, W), 11.0)
scene += (H - yy) / H * 3.0                      # sky a little cooler up top
scene += blob(70, 95, 11, 30, 20.0)              # person: torso and legs
scene += blob(70, 55, 7.5, 8.5, 22.5)            # head
scene += blob(170, 108, 26, 13, 15.0)            # vehicle body
scene += blob(170, 100, 11, 6, 30.0)             # engine bay, hottest thing here
scene += rng.normal(0, 0.28, (H, W))             # sensor noise

# ironbow, as thermal cameras usually render it
ironbow = LinearSegmentedColormap.from_list(
    "ironbow",
    ["#00000a", "#1b0a52", "#5c0f8b", "#9c1f6b", "#d2452f", "#f08c00", "#ffd400", "#ffffff"])

palettes = [("White-hot", "gray"), ("Black-hot", "gray_r"),
            ("Ironbow", ironbow), ("Rainbow", "turbo")]

fig, axs = plt.subplots(2, 4, figsize=(13.6, 5.1),
                        gridspec_kw={"height_ratios": [2.5, 1]})

sample_y, sample_x = 55, 70        # the person's head, the same pixel in every panel

for i, (label, cmap) in enumerate(palettes):
    ax = axs[0, i]
    im = ax.imshow(scene, cmap=cmap, vmin=scene.min(), vmax=scene.max())
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(label, fontsize=13, weight="bold", pad=8)
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color(GRID); sp.set_linewidth(1.2)

    # read back the RGB this palette gives the sampled pixel
    norm = (scene[sample_y, sample_x] - scene.min()) / (scene.max() - scene.min())
    rgb = plt.get_cmap(cmap)(norm)[:3]
    r, g, b = (np.array(rgb) * 255).round().astype(int)

    ax.plot(sample_x, sample_y, marker="o", ms=9, mfc="none", mec="#00ff6a", mew=2.2)

    ax2 = axs[1, i]
    ax2.set_xticks([]); ax2.set_yticks([]); ax2.grid(False)
    for sp in ax2.spines.values():
        sp.set_visible(False)
    ax2.add_patch(plt.Rectangle((0.12, 0.42), 0.76, 0.40, fc=rgb, ec=GRID, lw=1.2,
                                transform=ax2.transAxes))
    ax2.text(0.5, 0.26, f"RGB {r}, {g}, {b}", ha="center", va="center", fontsize=12,
             color=INK, weight="bold", transform=ax2.transAxes)
    ax2.text(0.5, 0.06, "same pixel, same temperature", ha="center", va="center",
             fontsize=10, color=INK2, transform=ax2.transAxes)

fig.suptitle("One sensor reading, four sets of pixels: the palette is a display setting",
             x=0.01, y=0.985, ha="left", va="top", fontsize=15, weight="bold")
fig.text(0.01, 0.925,
         f"The circled pixel is the same point on the same synthetic scene in all four panels, "
         f"at {scene[sample_y, sample_x]:.1f} °C.",
         ha="left", va="top", fontsize=11.5, color=INK2)
fig.tight_layout(rect=[0, 0, 1, 0.92])
save(fig, f"{SLUG}-palette-trap.png")

for label, cmap in palettes:
    norm = (scene[sample_y, sample_x] - scene.min()) / (scene.max() - scene.min())
    print(label, (np.array(plt.get_cmap(cmap)(norm)[:3]) * 255).round().astype(int))
