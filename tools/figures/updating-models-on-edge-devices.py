"""Figures for updating-models-on-edge-devices. A diagram, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, CRIT, GOOD, WARN, save

SLUG = "updating-models-on-edge-devices"


def box(ax, x, y, w, h, color, title, sub):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "22", ec=color, lw=1.6))
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="center", fontsize=12.5, weight="bold")
    ax.text(x + w / 2, y + (h - 0.5) / 2, sub, ha="center", va="center", fontsize=10.8, color=INK2, linespacing=1.35)


fig, ax = plt.subplots(figsize=(12, 5.2))
ax.set_xlim(0, 12.4); ax.set_ylim(0, 5.4); ax.axis("off")
ax.text(0.1, 5.2, "Roll out in stages; every stage can roll back on its own", fontsize=14, weight="bold", va="center")
steps = [("Download", "to a new folder;\ncheck hash and\nsignature", C[0]),
         ("Self-test", "load, run test\nimages, compare\nwith expected", C[6]),
         ("Switch", "atomic: change\na pointer, restart\nthe service", C[3]),
         ("Watch", "health, FPS,\nalert rates vs\nprevious days", C[2]),
         ("Widen", "1 device, then\na few, then\nthe rest", C[1])]
for i, (t, s, c) in enumerate(steps):
    x = 0.1 + i * 2.48
    box(ax, x, 2.2, 2.1, 2.3, c, t, s)
    if i < len(steps) - 1:
        ax.annotate("", xy=(x + 2.43, 3.35), xytext=(x + 2.1, 3.35),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4))
ax.annotate("", xy=(5.6, 1.3), xytext=(9.6, 2.2), arrowprops=dict(arrowstyle="-|>", color=CRIT, lw=1.6, ls="--",
                                                                connectionstyle="arc3,rad=-0.25"))
ax.annotate("", xy=(4.0, 1.3), xytext=(3.6, 2.2), arrowprops=dict(arrowstyle="-|>", color=CRIT, lw=1.6, ls="--"))
ax.text(4.8, 0.9, "on failure: keep or restore the previous model and config", ha="center", fontsize=11.5, color=CRIT)
save(fig, f"{SLUG}-staged-rollout.png")
