"""Figures for iou-and-nms-explained: IoU examples, real NMS before/after, NMS threshold effect on real footage."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, OUT
import detect

SLUG = "iou-and-nms-explained"
FOOT = (52, 104, 235)  # BGR orange for raw candidates


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    return inter / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter)


def annot(img, dets, k=2, color=(92, 107, 11), label=True, fs=1.0, thick=3, short=False):
    im = cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC)
    for x1, y1, x2, y2, s, n in dets:
        p1, p2 = (int(x1 * k), int(y1 * k)), (int(x2 * k), int(y2 * k))
        cv2.rectangle(im, p1, p2, color, thick)
        if label:
            t = f"{s:.2f}" if short else f"{n} {s:.2f}"
            (tw, th), _ = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, fs, 2)
            y0 = max(p1[1], th + 12)
            x0 = max(0, min(p1[0], im.shape[1] - tw - 10))
            cv2.rectangle(im, (x0, y0 - th - 12), (x0 + tw + 10, y0), color, -1)
            cv2.putText(im, t, (x0 + 5, y0 - 7), cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 255), 2, cv2.LINE_AA)
    return im[:, :, ::-1]


def save_jpg_fig(fig, name, width_px=1400):
    w = fig.get_size_inches()[0]
    fig.savefig(OUT / name, dpi=width_px / w, bbox_inches="tight", pad_inches=0.12, pil_kwargs={"quality": 85})
    plt.close(fig)


def fig_iou_examples():
    pairs = [
        ((0, 0, 10, 10), (5, 5, 15, 15), "The worked example"),
        ((0, 0, 10, 10), (2.5, 0, 12.5, 10), "Shifted a quarter"),
        ((0, 0, 10, 10), (1, 0, 11, 10), "Shifted by a tenth"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.3))
    for ax, (a, b, t) in zip(axes, pairs):
        v = iou(a, b)
        ix1, iy1, ix2, iy2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
        for bx, c in [(a, C[0]), (b, C[1])]:
            ax.add_patch(Rectangle((bx[0], bx[1]), bx[2] - bx[0], bx[3] - bx[1], fc=c + "22", ec=c, lw=2.2))
        ax.add_patch(Rectangle((ix1, iy1), ix2 - ix1, iy2 - iy1, fc=INK2 + "55", ec="none", hatch="///"))
        ax.set_xlim(-1.5, 16.5); ax.set_ylim(16.5, -1.5); ax.set_aspect("equal"); ax.axis("off")
        inter = (ix2 - ix1) * (iy2 - iy1)
        union = 200 - inter
        ax.set_title(f"{t}\nIoU = {inter:g} / {union:g} = {v:.2f}", fontsize=13)
    axes[0].text(0.6, 1.4, "A", fontsize=13, weight="bold", color=C[0])
    axes[0].text(13.6, 14.2, "B", fontsize=13, weight="bold", color=C[1])
    h = [Rectangle((0, 0), 1, 1, fc=INK2 + "55", ec="none", hatch="///", label="overlap (intersection)")]
    fig.legend(handles=h, loc="lower center", fontsize=12, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Same-size boxes: even a small shift costs a lot of IoU", fontsize=14,
                 weight="bold", y=1.03)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    style.save(fig, f"{SLUG}-iou-examples.png")


def fig_nms_real():
    img = detect.frame("retail", 0.92)
    raw = detect.detect(img, 0.25, nms=False)
    kept = detect.detect(img, 0.25, iou=0.45)
    print("raw", len(raw), "kept", len(kept))
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.9))
    axes[0].imshow(annot(img, raw, color=FOOT, label=False, thick=2))
    axes[0].set_title(f"Before NMS: {len(raw)} boxes, many stacked", loc="left", fontsize=13)
    axes[1].imshow(annot(img, kept, fs=1.1))
    axes[1].set_title(f"After NMS (IoU 0.45): {len(kept)} boxes", loc="left", fontsize=13)
    for ax in axes:
        ax.axis("off")
    fig.tight_layout(w_pad=1.2)
    save_jpg_fig(fig, f"{SLUG}-nms-before-after.jpg")


def fig_nms_threshold():
    img = detect.frame("people", 0.8)
    x0, y0, x1, y1 = 0, 40, 240, 250  # crop around the two walkers
    out = []
    for t in (0.45, 0.9):
        d = detect.detect(img, 0.25, iou=t)
        print("iou", t, [(round(s, 2), [round(v) for v in b]) for *b, s, n in d])
        dd = [(a - x0, b - y0, c - x0, e - y0, s, n) for a, b, c, e, s, n in d]
        out.append((t, d, annot(img[y0:y1, x0:x1], dd, k=3, fs=1.0, short=True)))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.9))
    for ax, (t, d, im) in zip(axes, out):
        ax.imshow(im)
        ax.set_title(f"NMS IoU threshold {t}: {len(d)} person boxes", loc="left", fontsize=13)
        ax.axis("off")
    fig.tight_layout(w_pad=1.5)
    save_jpg_fig(fig, f"{SLUG}-nms-threshold.jpg", width_px=1300)


if __name__ == "__main__":
    fig_iou_examples()
    fig_nms_real()
    fig_nms_threshold()
