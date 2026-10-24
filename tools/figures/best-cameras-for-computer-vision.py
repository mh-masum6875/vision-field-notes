"""Figures for best-cameras-for-computer-vision."""
import cv2
import numpy as np

import style  # noqa: F401  (sets output folder)
import detect

SLUG = "best-cameras-for-computer-vision"
IDX = 75  # frame index in the safety clip where the worker is fully in view


def label(im, text, scale=0.8):
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)
    cv2.rectangle(im, (0, 0), (tw + 16, th + 18), (255, 255, 255), -1)
    cv2.putText(im, text, (8, th + 9), cv2.FONT_HERSHEY_SIMPLEX, scale, (11, 11, 11), 2, cv2.LINE_AA)
    return im


img = detect.frame("safety", IDX / 360)

# 1. Motion blur vs detection (blur applied synthetically, detections are real model output)
tiles = []
for k, name in [(1, "Sharp frame"), (17, "Blur 17 px"), (25, "Blur 25 px"), (41, "Blur 41 px")]:
    if k > 1:
        ker = np.zeros((k, k), np.float32)
        ker[k // 2, :] = 1.0 / k
        im = cv2.filter2D(img, -1, ker)
    else:
        im = img.copy()
    dets = detect.detect(im)
    out = detect.draw(im, dets)
    txt = f"{name}: " + (", ".join(f"{n} {s:.2f}" for *_, s, n in dets) if dets else "no detection")
    tiles.append(label(out, txt, 0.7))
pad_v = np.full((360, 8, 3), 255, np.uint8)
row1 = np.hstack([tiles[0], pad_v, tiles[1]])
row2 = np.hstack([tiles[2], pad_v, tiles[3]])
grid = np.vstack([row1, np.full((8, row1.shape[1], 3), 255, np.uint8), row2])
detect.save_jpg(grid, f"{SLUG}-motion-blur.jpg", width=1200)

# 2. Pixels on target: the same worker resampled to fewer pixels
dets = [d for d in detect.detect(img) if d[5] == "person"]
x1, y1, x2, y2 = [int(v) for v in dets[0][:4]]
m = 6
crop = img[max(0, y1 - m):y2 + m, max(0, x1 - m):x2 + m]
H = 300
cols = []
for px in [None, 60, 30, 15]:
    if px is None:
        c = crop
        txt = f"{crop.shape[0]} px tall"
    else:
        w = max(1, int(round(crop.shape[1] * px / crop.shape[0])))
        c = cv2.resize(crop, (w, px), interpolation=cv2.INTER_AREA)
        txt = f"{px} px tall"
    disp = cv2.resize(c, (int(crop.shape[1] * H / crop.shape[0]), H), interpolation=cv2.INTER_NEAREST)
    panel = np.full((H + 50, disp.shape[1] + 60, 3), 255, np.uint8)
    ox = 30
    panel[0:H, ox:ox + disp.shape[1]] = disp
    (tw, _), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    cv2.putText(panel, txt, ((panel.shape[1] - tw) // 2, H + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (11, 11, 11), 2, cv2.LINE_AA)
    cols.append(panel)
strip = np.hstack(cols)
strip = np.vstack([np.full((20, strip.shape[1], 3), 255, np.uint8), strip])
detect.save_jpg(strip, f"{SLUG}-pixels-on-target.jpg", width=1000)
