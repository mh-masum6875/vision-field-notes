"""Figures for what-map-hides.

Both precision-recall curves are constructed from formulas, not measured. They are shaped so that their
areas (AP) match, to show that equal AP can mean very different behaviour at one operating threshold.
"""
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "what-map-hides"
r = np.linspace(0, 1, 1001)


def ap(p):
    # 101-point interpolated AP, the COCO-style definition
    pi = np.maximum.accumulate(p[::-1])[::-1]
    pts = np.linspace(0, 1, 101)
    return float(np.mean(np.interp(pts, r, pi)))


# A: holds precision high, then collapses. B: lower precision early, but keeps going further.
pa = np.where(r < 0.62, 0.97, np.clip(0.97 - (r - 0.62) * 4.2, 0, 1))
k = 0.0
for _ in range(60):  # pick B's slope so both curves have the same AP
    pb = np.clip(0.86 - k * r ** 3, 0, 1)
    k += (ap(pb) - ap(pa)) * 4
print("AP A", round(ap(pa), 3), "AP B", round(ap(pb), 3), "k", round(k, 3))

target = 0.85
ra = r[pa >= target].max()
rb = r[pb >= target].max()
print("recall at precision >= 0.85: A", round(ra, 2), "B", round(rb, 2))

fig, ax = plt.subplots(figsize=(9.5, 5.4))
ax.plot(r, pa, color=C[0], label=f"Model A  (AP {ap(pa):.2f})")
ax.plot(r, pb, color=C[1], label=f"Model B  (AP {ap(pb):.2f})")
ax.axhline(target, color=INK2, ls="--", lw=1.2)
ax.text(0.01, target + 0.015, "requirement: precision at least 0.85", fontsize=11.5, color=INK2)
for rv, c in [(ra, C[0]), (rb, C[1])]:
    ax.plot([rv], [target], "o", color=c, ms=8, zorder=4)
    ax.annotate(f"recall {rv:.2f}", xy=(rv, target), xytext=(rv - 0.02, target - 0.17), ha="center",
                fontsize=11.5, color=c, arrowprops=dict(arrowstyle="->", color=c))
ax.set_xlim(0, 1); ax.set_ylim(0, 1.03)
ax.set_xlabel("recall"); ax.set_ylabel("precision")
ax.legend(loc="lower left", fontsize=11.5)
ax.set_title("Same AP, different answer at the threshold you will deploy (constructed curves)", loc="left")
save(fig, f"{SLUG}-same-ap.png")
