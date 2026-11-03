"""Figures for debug-overlays-that-help.

An overlay design drawn with OpenCV on a synthetic frame. Boxes, IDs, scores and states are made up to show
the layout; no model was run.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from style import save, OUT

SLUG = "debug-overlays-that-help"
W, H = 1280, 720
img = np.full((H, W, 3), (200, 205, 198), np.uint8)
cv2.rectangle(img, (0, 520), (W, H), (150, 150, 150), -1)
for x in (150, 420, 980):
    cv2.rectangle(img, (x, 180), (x + 120, 520), (120, 125, 130), -1)          # shelving

zone = np.array([[600, 400], [1180, 400], [1240, 700], [560, 700]], np.int32)
over = img.copy()
cv2.fillPoly(over, [zone], (60, 60, 220))
img = cv2.addWeighted(over, 0.18, img, 0.82, 0)
cv2.polylines(img, [zone], True, (60, 60, 220), 2, cv2.LINE_AA)
cv2.putText(img, "ZONE loading-bay  active 22:00-06:00", (610, 392), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (60, 60, 220), 2, cv2.LINE_AA)


def person(x, y, h, col):
    w = int(h * 0.38)
    cv2.ellipse(img, (x + w // 2, y + h // 8), (w // 4, h // 9), 0, 0, 360, col, -1)
    cv2.rectangle(img, (x + w // 6, y + h // 5), (x + w - w // 6, y + h), col, -1)
    return (x, y, x + w, y + h)


def box(b, col, label, sub=None, dashed=False):
    x1, y1, x2, y2 = b
    if dashed:
        for xx in range(x1, x2, 14):
            cv2.line(img, (xx, y1), (min(xx + 7, x2), y1), col, 2); cv2.line(img, (xx, y2), (min(xx + 7, x2), y2), col, 2)
        for yy in range(y1, y2, 14):
            cv2.line(img, (x1, yy), (x1, min(yy + 7, y2)), col, 2); cv2.line(img, (x2, yy), (x2, min(yy + 7, y2)), col, 2)
    else:
        cv2.rectangle(img, (x1, y1), (x2, y2), col, 2)
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    cv2.rectangle(img, (x1, y1 - th - 10), (x1 + tw + 8, y1), col, -1)
    cv2.putText(img, label, (x1 + 4, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)
    if sub:
        cv2.putText(img, sub, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 2, cv2.LINE_AA)


b1 = person(820, 430, 230, (70, 70, 80))
box(b1, (40, 40, 210), "#7 person 0.81", "in zone 12.4 s / 10 s  ALERT sent")
b2 = person(300, 300, 170, (90, 90, 100))
box(b2, (40, 150, 40), "#3 person 0.66", "outside zone")
cv2.rectangle(img, (470, 260), (530, 330), (180, 180, 180), -1)
box((462, 252, 538, 338), (0, 160, 230), "person 0.31", "below threshold 0.45", dashed=True)

cv2.rectangle(img, (0, 0), (W, 34), (30, 30, 30), -1)
hud = "cam07  2026-11-19 22:41:07 +08  |  model ppe-1.8.0  thr v6  |  in 5.0 fps  proc 5.0 fps  |  lat 46 ms  |  night"
cv2.putText(img, hud, (10, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)

fig, ax = plt.subplots(figsize=(11, 6.4))
ax.imshow(img[:, :, ::-1]); ax.axis("off")
ax.set_title("A debug overlay that answers 'why did it alert?' (synthetic frame, made-up values)", loc="left")
save(fig, f"{SLUG}-overlay.png")
