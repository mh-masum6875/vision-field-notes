"""Figures for export-yolo-to-onnx."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT, save
import detect

SLUG = "export-yolo-to-onnx"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, size=12, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight,
            linespacing=1.3)


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=16))


# 1. Letterbox vs stretch on a real frame
img = detect.frame("retail", 0.7)
h, w = img.shape[:2]
S = 640
stretched = cv2.resize(img, (S, S))
scale = min(S / h, S / w)
nh, nw = int(round(h * scale)), int(round(w * scale))
top, left = (S - nh) // 2, (S - nw) // 2
lb = np.full((S, S, 3), 114, np.uint8)
lb[top:top + nh, left:left + nw] = cv2.resize(img, (nw, nh))

fig, axs = plt.subplots(1, 3, figsize=(12, 4.6), gridspec_kw=dict(width_ratios=[1.45, 1, 1]))
for ax, im, title, col in [(axs[0], img, f"Original frame\n{w} x {h}", INK),
                           (axs[1], stretched, "Stretched to 640 x 640\n(wrong: shapes distorted)", CRIT),
                           (axs[2], lb, "Letterboxed to 640 x 640\n(right: aspect kept, grey pad)", GOOD)]:
    ax.imshow(im[:, :, ::-1])
    ax.set_title(title, fontsize=12, color=col, weight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color(GRID)
ax = axs[2]
ax.annotate("", xy=(S + 25, 0), xytext=(S + 25, top), annotation_clip=False,
            arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.4))
ax.text(S + 45, top / 2, f"top = {top}", va="center", fontsize=11, color=INK2)
ax.text(S / 2, top + nh + (S - top - nh) / 2, f"scale = {scale:.2f}, left = {left}",
        ha="center", va="center", fontsize=11, color=INK)
fig.suptitle("Letterboxing keeps the aspect ratio; remember scale, left and top to map boxes back",
             fontsize=14, weight="bold", x=0.02, ha="left", y=0.97)
fig.tight_layout(rect=(0, 0, 1, 0.93))
save(fig, f"{SLUG}-letterbox.jpg")

# 2. Output tensor layout
fig, ax = plt.subplots(figsize=(10.5, 5.6))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.6)
ax.axis("off")
x0, y0, W, H = 1.3, 1.5, 8.4, 3.2
segs = [(6400, "80 x 80 grid\n6400 columns", C[0]), (1600, "40 x 40\n1600", C[1]), (400, "20 x 20\n400", C[2])]
box_h = H * 4 / 84 * 3  # visually enlarged box rows so they stay readable
cls_h = H - box_h
x = x0
for n, txt, col in segs:
    ww = W * n / 8400
    ax.add_patch(Rectangle((x, y0), ww, cls_h, fc=col, alpha=0.18, ec=col, lw=1.5))
    ax.add_patch(Rectangle((x, y0 + cls_h), ww, box_h, fc=col, alpha=0.45, ec=col, lw=1.5))
    if n > 500:
        ax.text(x + ww / 2, y0 + cls_h / 2, txt, ha="center", va="center", fontsize=11)
    else:
        ax.annotate(txt.replace("\n", " = "), xy=(x + ww / 2, y0), xytext=(x + ww / 2 - 0.2, y0 - 0.35),
                    ha="center", va="top", fontsize=11,
                    arrowprops=dict(arrowstyle="-", color=INK2, lw=1))
    x += ww
ax.text(x0 - 0.1, y0 + cls_h + box_h / 2, "4 box rows\ncx, cy, w, h", ha="right", va="center", fontsize=11)
ax.text(x0 - 0.1, y0 + cls_h / 2, "80 class\nscore rows", ha="right", va="center", fontsize=11)
ax.annotate("", xy=(x0 + W, y0 + H + 0.3), xytext=(x0, y0 + H + 0.3),
            arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.4))
ax.text(x0 + W / 2, y0 + H + 0.5, "8400 candidate predictions (one column each)", ha="center",
        fontsize=12, color=INK)
ax.text(x0, 0.45, "One column = one candidate: its box plus a score for every class.\n"
        "Transpose to [8400, 84], take the best class per row, threshold, NMS, undo the letterbox.",
        fontsize=11.5, color=INK2, va="center")
ax.set_title("Output [1, 84, 8400] of a 640-input, 80-class YOLOv8 detection model", loc="left")
save(fig, f"{SLUG}-output-layout.png")

# 3. Wrong colour order: real detections on the same frame
img = detect.frame("retail", 0.7)
rgb_ok = detect.detect(img)                                   # correct: detect() converts BGR->RGB
bgr_bad = detect.detect(np.ascontiguousarray(img[:, :, ::-1]))  # channels swapped before the model


ok_classes = {d[5] for d in rgb_ok}


def panel(dets, title):
    T = 46
    im = cv2.copyMakeBorder(img, T, 0, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    sh = [(x1, y1 + T, x2, y2 + T, sc, n) for x1, y1, x2, y2, sc, n in dets]
    im = detect.draw(im, [d for d in sh if d[5] in ok_classes])
    im = detect.draw(im, [d for d in sh if d[5] not in ok_classes], color=(59, 59, 208), thick=3)
    cv2.putText(im, title, (8, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (11, 11, 11), 2, cv2.LINE_AA)
    return im


a = panel(rgb_ok, "RGB input (correct)")
b = panel(bgr_bad, "BGR input (colour order bug)")
out = np.hstack([a, np.full((a.shape[0], 10, 3), 255, np.uint8), b])
detect.save_jpg(out, f"{SLUG}-bgr-vs-rgb.jpg", width=1200)
print("RGB:", [(n, round(s, 2)) for *_, s, n in rgb_ok])
print("BGR:", [(n, round(s, 2)) for *_, s, n in bgr_bad])
