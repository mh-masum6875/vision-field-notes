"""Figures for map-precision-recall-explained: TP/FP/FN, an illustrative PR curve with AP, and mAP50 vs mAP50-95."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT

SLUG = "map-precision-recall-explained"
GT_C, PR_C = INK2, C[0]


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua


def rect(ax, b, color, dashed=False, lw=2.4):
    ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fill=False, ec=color, lw=lw,
                           ls=(0, (4, 3)) if dashed else "-"))


def obj(ax, b):
    """A simple stand-in object: a soft grey blob inside the true box."""
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    ax.add_patch(plt.matplotlib.patches.FancyBboxPatch((b[0] + 1.2, b[1] + 1.2), b[2] - b[0] - 2.4, b[3] - b[1] - 2.4,
                 boxstyle="round,pad=0,rounding_size=3", fc="#d9d7d0", ec="none"))


def fig_outcomes():
    fig, axes = plt.subplots(1, 4, figsize=(12, 4.0))
    gt = (20, 15, 60, 85)
    cases = [
        ("True positive", "box matches the object", [gt], [((24, 18, 64, 82), 0.91)], GOOD),
        ("False positive", "box on background", [], [((22, 28, 70, 72), 0.48)], CRIT),
        ("False positive", "duplicate box", [gt], [((22, 16, 61, 84), 0.88), ((30, 30, 72, 92), 0.41)], CRIT),
        ("False negative", "object missed", [gt], [], CRIT),
    ]
    for ax, (t, sub, gts, preds, col) in zip(axes, cases):
        ax.set_xlim(0, 90); ax.set_ylim(100, 0); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((0, 0), 90, 100, fc="#f6f5f1", ec=GRID, lw=1))
        for g in gts:
            obj(ax, g)
            rect(ax, g, GT_C, dashed=True)
        for k, (p, s) in enumerate(preds):
            rect(ax, p, PR_C)
            ax.text(p[2] - 1, p[3] - 2, f"{s:.2f}", ha="right", va="bottom", fontsize=11, color="white",
                    bbox=dict(fc=PR_C, ec="none", pad=1.5))
        if t == "True positive":
            ax.text(45, 96, f"IoU {iou(gts[0], preds[0][0]):.2f}", ha="center", va="bottom", fontsize=11.5, color=INK2)
        if sub == "duplicate box":
            ax.text(45, 98.5, "second box counts as FP", ha="center", va="bottom", fontsize=11, color=INK2)
        ax.set_title(f"{t}\n", fontsize=13.5, color=INK, loc="center")
        ax.text(45, -4, sub, ha="center", va="bottom", fontsize=11.5, color=INK2)
    # legend
    h1 = plt.Line2D([], [], color=GT_C, ls=(0, (4, 3)), lw=2.4, label="true box (label)")
    h2 = plt.Line2D([], [], color=PR_C, lw=2.4, label="predicted box with score")
    fig.legend(handles=[h1, h2], loc="lower center", ncol=2, fontsize=12, bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout(rect=(0, 0.06, 1, 1), w_pad=1.5)
    style.save(fig, f"{SLUG}-tp-fp-fn.png")


def fig_pr_curve():
    r = np.linspace(0, 1, 300)
    # illustrative shapes, not measurements
    pa = np.clip(0.97 - 0.10 * r ** 2 - 0.75 * np.clip((r - 0.78) / 0.22, 0, 1) ** 2.2, 0, 1)
    pb = np.clip(0.95 - 0.55 * r ** 1.4, 0, 1)
    ra, rb = 0.96, 0.88
    pa[r > ra] = np.nan
    pb[r > rb] = np.nan
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.fill_between(r, 0, np.nan_to_num(pa), color=C[0], alpha=0.12, lw=0)
    ax.plot(r, pa, color=C[0], label="Model A: precision holds as recall rises")
    ax.plot(r, pb, color=C[1], label="Model B: precision drops early")
    apa = np.trapezoid(np.nan_to_num(pa), r)
    apb = np.trapezoid(np.nan_to_num(pb), r)
    ax.text(0.35, 0.45, f"shaded area = AP\nfor model A (about {apa:.2f})", fontsize=12, color=INK, ha="center")
    ax.annotate("high threshold:\nfew boxes, mostly right", xy=(0.06, 0.965), xytext=(0.1, 0.62), fontsize=11.5, color=INK2,
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2))
    ax.annotate("low threshold:\nmore found, more junk", xy=(0.94, 0.50), xytext=(0.6, 0.12), fontsize=11.5, color=INK2,
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2))
    ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.04)
    ax.set_xlabel("Recall (share of real objects found)")
    ax.set_ylabel("Precision (share of boxes that are right)")
    ax.set_title("Bigger area under the curve means higher AP (illustrative)", loc="left")
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 0.22), fontsize=11.5)
    print("illustrative AP", round(apa, 2), round(apb, 2))
    style.save(fig, f"{SLUG}-pr-curve.png")


def fig_iou_thresholds():
    gt = (20, 12, 70, 88)
    pred = (27, 18, 76, 96)
    v = iou(gt, pred)
    ths = np.round(np.arange(0.5, 0.951, 0.05), 2)
    fig = plt.figure(figsize=(11, 4.4))
    ax0 = fig.add_axes([0.0, 0.05, 0.25, 0.8])
    ax0.set_xlim(0, 95); ax0.set_ylim(105, 0); ax0.set_aspect("equal"); ax0.axis("off")
    ax0.add_patch(Rectangle((0, 0), 95, 105, fc="#f6f5f1", ec=GRID, lw=1))
    obj(ax0, gt)
    rect(ax0, gt, GT_C, dashed=True)
    rect(ax0, pred, PR_C)
    ax0.set_title(f"One prediction, IoU {v:.2f}", fontsize=13.5)
    ax = fig.add_axes([0.32, 0.12, 0.66, 0.72])
    passed = ths <= v + 1e-9
    for i, (t, ok) in enumerate(zip(ths, passed)):
        ax.add_patch(Rectangle((i + 0.06, 0), 0.88, 1, fc=(ACCENT if ok else "#f0efea"), ec=(ACCENT if ok else GRID), lw=1.2))
        ax.text(i + 0.5, 0.5, "match" if ok else "miss", ha="center", va="center", fontsize=11.5,
                color=("white" if ok else INK2), weight="bold" if ok else "normal")
        ax.text(i + 0.5, -0.18, f"{t:.2f}", ha="center", va="top", fontsize=11.5, color=INK2)
    ax.set_xlim(0, 10); ax.set_ylim(-0.55, 1.45); ax.axis("off")
    ax.text(0, -0.42, "IoU threshold used to decide a match", ha="left", va="top", fontsize=12, color=INK2)
    ax.text(0, 1.3, f"mAP50 checks only the first cell. mAP50-95 averages all ten: this box\npasses {passed.sum()} of 10, so it earns full credit at 0.50 but only partial credit overall.",
            ha="left", va="center", fontsize=12.5, color=INK)
    print("iou", round(v, 3), "passes", passed.sum())
    style.save(fig, f"{SLUG}-map50-vs-map50-95.png")


if __name__ == "__main__":
    fig_outcomes()
    fig_pr_curve()
    fig_iou_thresholds()
