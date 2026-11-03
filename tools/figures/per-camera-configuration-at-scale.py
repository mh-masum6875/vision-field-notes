"""Figures for per-camera-configuration-at-scale. A diagram with example values, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, save

SLUG = "per-camera-configuration-at-scale"


def box(ax, x, y, w, h, color, title, body):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "22", ec=color, lw=1.6))
    ax.text(x + 0.2, y + h - 0.33, title, fontsize=12.5, weight="bold", va="center")
    ax.text(x + 0.2, y + h - 0.7, body, fontsize=10.5, color=INK2, va="top", family="DejaVu Sans Mono",
            linespacing=1.45)


fig, ax = plt.subplots(figsize=(12, 4.8))
ax.set_xlim(0, 12.3); ax.set_ylim(0, 4.9); ax.axis("off")
ax.text(0.1, 4.7, "Layered settings: each level overrides only what it must", fontsize=14, weight="bold", va="center")
box(ax, 0.1, 0.3, 2.8, 3.8, C[0], "Global defaults", "model: ppe-1.8.0\nfps: 5\nperson.conf: 0.45\nhelmet.conf: 0.50\ncooldown_s: 120\ntz: from site")
box(ax, 3.2, 0.3, 2.8, 3.8, C[6], "Site", "site: warehouse-2\ntz: Asia/Singapore\nschedule:\n  22:00-06:00")
box(ax, 6.3, 0.3, 2.8, 3.8, C[3], "Camera", "camera: cam07\nstream: sub\nzones: [...]\nperson.conf: 0.55\n# glare at dusk")
box(ax, 9.4, 0.3, 2.8, 3.8, C[2], "Effective (computed)", "model: ppe-1.8.0\nfps: 5\nperson.conf: 0.55\nhelmet.conf: 0.50\ncooldown_s: 120\ntz: Asia/Singapore")
for x in (2.9, 6.0, 9.1):
    ax.annotate("", xy=(x + 0.3, 2.2), xytext=(x, 2.2), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4))
save(fig, f"{SLUG}-layers.png")
