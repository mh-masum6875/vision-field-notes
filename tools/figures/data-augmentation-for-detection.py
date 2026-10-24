"""Figures for data-augmentation-for-detection.

Boxes are YOLOv8n detections on the original frame, transformed with the same
geometry as the image (as a training pipeline would do with labels).
"""
import io
import cv2
import numpy as np
import style
from style import plt, C, INK, INK2, MUTED, ACCENT, GOOD, CRIT
from matplotlib.patches import Rectangle, Polygon
import detect

SLUG = "data-augmentation-for-detection"


def fig_to_jpg(fig, name, width=1300):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    return detect.save_jpg(img, name, width=width)


def clean(ax):
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def affine_boxes(boxes, M, W, H):
    out = []
    for x1, y1, x2, y2 in boxes:
        pts = np.array([[x1, y1, 1], [x2, y1, 1], [x2, y2, 1], [x1, y2, 1]]) @ M.T
        bx1, by1 = pts[:, 0].min(), pts[:, 1].min()
        bx2, by2 = pts[:, 0].max(), pts[:, 1].max()
        out.append((max(0, bx1), max(0, by1), min(W, bx2), min(H, by2), pts))
    return out


# ---- Figure 1: plausible vs implausible transforms ----
def transforms():
    img = detect.frame("bottles", 0.15)
    H, W = img.shape[:2]
    dets = [d for d in detect.detect(img) if d[5] == "bottle"]
    print("bottles:", len(dets))
    boxes = [d[:4] for d in dets]
    panels = []
    I = np.array([[1, 0, 0], [0, 1, 0]], float)
    panels.append(("Original", img, affine_boxes(boxes, I, W, H), None))
    M = np.array([[-1, 0, W], [0, 1, 0]], float)
    panels.append(("Horizontal flip", cv2.warpAffine(img, M, (W, H)), affine_boxes(boxes, M, W, H), True))
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, 0.65)
    M[0, 2] += 70; M[1, 2] += 20
    panels.append(("Scale down and shift", cv2.warpAffine(img, M, (W, H), borderValue=(114, 114, 114)),
                   affine_boxes(boxes, M, W, H), True))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 2] *= 0.55; hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
    dark = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    panels.append(("Darker, more saturated", dark, affine_boxes(boxes, I, W, H), True))
    M = np.array([[1, 0, 0], [0, -1, H]], float)
    panels.append(("Vertical flip", cv2.warpAffine(img, M, (W, H)), affine_boxes(boxes, M, W, H), False))
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 35, 1.0)
    panels.append(("35 degree rotation", cv2.warpAffine(img, M, (W, H), borderValue=(114, 114, 114)),
                   affine_boxes(boxes, M, W, H), False))

    fig, axes = plt.subplots(2, 3, figsize=(10, 4.9))
    for ax, (title, im, bxs, ok) in zip(axes.flat, panels):
        ax.imshow(im[:, :, ::-1])
        clean(ax)
        for x1, y1, x2, y2, pts in bxs:
            if title.startswith("35"):
                ax.add_patch(Polygon(pts[:, :2], closed=True, fill=False, ec="white", lw=1.2, ls="--"))
            ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, ec=ACCENT, lw=2.2))
        ax.set_title(title, fontsize=12.5, color=INK)
        if ok is not None:
            ax.text(8, 10, "plausible" if ok else "unrealistic for this camera", fontsize=11, color="white",
                    va="top", ha="left", bbox=dict(fc=GOOD if ok else CRIT, ec="none", pad=2.5))
    fig.suptitle("Keep transforms your camera could produce; drop the ones it never would",
                 fontsize=14, fontweight="bold", y=1.0)
    fig.tight_layout()
    fig_to_jpg(fig, f"{SLUG}-transforms.jpg")


# ---- Figure 2: mosaic of four real frames ----
def crop_around(img, dets, cw, ch):
    H, W = img.shape[:2]
    if dets:
        cx = (min(d[0] for d in dets) + max(d[2] for d in dets)) / 2
        cy = (min(d[1] for d in dets) + max(d[3] for d in dets)) / 2
    else:
        cx, cy = W / 2, H / 2
    ox = int(np.clip(cx - cw / 2, 0, W - cw))
    oy = int(np.clip(cy - ch / 2, 0, H - ch))
    return ox, oy


def mosaic():
    S = 640
    cx, cy = 340, 300
    sources = [("retail", 0.80), ("bottles", 0.15), ("people", 0.70), ("safety", 0.60)]
    quads = [(0, 0, cx, cy), (cx, 0, S, cy), (0, cy, cx, S), (cx, cy, S, S)]
    canvas = np.full((S, S, 3), 114, np.uint8)
    out_boxes = []
    for (name, t), (qx1, qy1, qx2, qy2) in zip(sources, quads):
        img = detect.frame(name, t)
        dets = [d for d in detect.detect(img) if d[5] in ("person", "bottle")]
        cw, ch = qx2 - qx1, qy2 - qy1
        ox, oy = crop_around(img, dets, cw, ch)
        canvas[qy1:qy2, qx1:qx2] = img[oy:oy + ch, ox:ox + cw]
        for x1, y1, x2, y2, s, n in dets:
            a = (x2 - x1) * (y2 - y1)
            nx1, ny1 = max(qx1, x1 - ox + qx1), max(qy1, y1 - oy + qy1)
            nx2, ny2 = min(qx2, x2 - ox + qx1), min(qy2, y2 - oy + qy1)
            if nx2 > nx1 and ny2 > ny1 and (nx2 - nx1) * (ny2 - ny1) >= 0.4 * a:
                out_boxes.append((nx1, ny1, nx2, ny2, n))
    print("mosaic boxes:", len(out_boxes))
    fig, ax = plt.subplots(figsize=(7.2, 7.4))
    ax.imshow(canvas[:, :, ::-1])
    clean(ax)
    ax.axvline(cx, color="white", lw=1.5, ls="--")
    ax.axhline(cy, color="white", lw=1.5, ls="--")
    for x1, y1, x2, y2, n in out_boxes:
        ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, ec=ACCENT, lw=2.2))
        ax.text(x1 + 2, y1 + 2, n, fontsize=10, color="white", va="top", ha="left",
                bbox=dict(fc=ACCENT, ec="none", pad=1.5))
    ax.set_title("Mosaic: four frames, one training image,\nboxes cropped with the image", fontsize=14)
    fig_to_jpg(fig, f"{SLUG}-mosaic.jpg", width=1000)


if __name__ == "__main__":
    transforms()
    mosaic()
