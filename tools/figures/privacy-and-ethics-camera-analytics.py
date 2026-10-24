"""Figures for privacy-and-ethics-camera-analytics."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, OUT, save
import detect

SLUG = "privacy-and-ethics-camera-analytics"

# ---------------------------------------------------------------- 1. the same frame, minimised before storage
FT = 290 / 360
img = detect.frame("retail", FT)
dets = [d for d in detect.detect(img) if d[5] == "person"]
print("people detected:", len(dets))

live = detect.draw(img, dets)

stored = img.copy()
# mask: the left part of the frame is treated as an area that must never be stored (illustration)
MASK_X = 150
stored[:, :MASK_X] = (60, 60, 60)
cv2.putText(stored, "masked", (28, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (220, 220, 220), 2, cv2.LINE_AA)
# pixelate every detected person before the frame is written anywhere
for x1, y1, x2, y2, s, n in dets:
    x1, y1, x2, y2 = max(0, int(x1)), max(0, int(y1)), min(img.shape[1], int(x2)), min(img.shape[0], int(y2))
    roi = stored[y1:y2, x1:x2]
    small = cv2.resize(roi, (max(1, (x2 - x1) // 14), max(1, (y2 - y1) // 14)), interpolation=cv2.INTER_AREA)
    stored[y1:y2, x1:x2] = cv2.resize(small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)

fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
for ax, im, title in [(axes[0], live, "Live: analysed in memory, not kept"),
                      (axes[1], stored, "Stored snapshot: masked, pixelated")]:
    ax.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, loc="left", fontsize=12)
fig.text(0.5, 0.1, f"What the counting purpose needs long-term:   people in aisle = {len(dets)},  time stamp,  camera id",
         ha="center", va="top", fontsize=12, color=ACCENT, weight="bold")
fig.subplots_adjust(wspace=0.03)
fig.savefig(OUT / f"{SLUG}-minimise.jpg", dpi=150, bbox_inches="tight", pad_inches=0.15,
            pil_kwargs={"quality": 85})
plt.close(fig)


# ---------------------------------------------------------------- 2. data flow with retention, no specific periods
def box(ax, x, y, w, h, title, sub, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=color + "1f", ec=color, lw=1.6))
    ax.text(x + w / 2, y + h - 2.6, title, ha="center", va="top", fontsize=12.5, weight="bold", color=INK)
    ax.text(x + w / 2, y + 2.4, sub, ha="center", va="bottom", fontsize=10.5, color=INK2, linespacing=1.3)


def arrow(ax, p, q, label=None):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.5, mutation_scale=14))
    if label:
        ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 1.0, label, ha="center", va="bottom", fontsize=10.5, color=INK2)


fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis("off")
box(ax, 0, 20, 21, 16, "Camera", "angle and resolution\nchosen to avoid\nneedless detail", C[0])
box(ax, 25, 20, 22, 16, "Edge analytics", "live video handled\nin memory only,\nmasks applied first", C[2])
box(ax, 54, 31, 24, 14, "Alert snapshots", "blurred, role-based\naccess, short period", C[1])
box(ax, 54, 9, 24, 14, "Aggregates", "counts and statistics,\nkept longer", C[6])
box(ax, 83, 20, 17, 16, "Deleted", "on a schedule,\nincl. backups\nand dev copies", MUTED)
arrow(ax, (21.3, 28), (24.7, 28))
arrow(ax, (47.3, 30), (53.7, 37))
arrow(ax, (47.3, 26), (53.7, 17))
arrow(ax, (78.3, 37), (82.7, 31))
arrow(ax, (78.3, 17), (82.7, 24))
ax.text(36, 17.5, "raw video:\nnot stored", ha="center", va="top", fontsize=11, color=INK2)
ax.text(0, 49.5, "Keep less, keep it shorter, and let a schedule do the deleting",
        ha="left", va="top", fontsize=13, weight="bold", color=ACCENT)
ax.text(0, 2, "Retention periods depend on purpose and local rules; set them with the site owner and advisers.",
        ha="left", va="bottom", fontsize=11, color=INK2, style="italic")
save(fig, f"{SLUG}-data-flow.png")
