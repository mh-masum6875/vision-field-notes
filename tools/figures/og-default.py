"""Default share image (1200 x 630) for pages and posts without their own figure."""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import style
from style import ACCENT, OUT

fig = plt.figure(figsize=(12, 6.3), dpi=100)
fig.patch.set_facecolor("#fbfbf9")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 12); ax.set_ylim(0, 6.3); ax.axis("off")
ax.add_patch(Circle((1.6, 3.15), 0.75, fill=False, ec=ACCENT, lw=10))
ax.add_patch(Circle((1.6, 3.15), 0.26, fc=ACCENT, ec="none"))
ax.text(2.9, 3.55, "Vision Field Notes", fontsize=54, weight="bold", color="#1c1f23", va="center")
ax.text(2.95, 2.55, "Practical computer vision and edge AI,\nfrom someone who runs it in production.",
        fontsize=24, color="#5b6470", va="center", linespacing=1.35)
ax.text(2.95, 0.8, "Maidul Hasan Masum", fontsize=20, color=ACCENT, va="center")
fig.savefig(OUT / "og-default.png", dpi=100, facecolor=fig.get_facecolor())
