"""Figures for opencv-essentials-for-cv-engineers.md"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, OUT, save
import detect

SLUG = "opencv-essentials-for-cv-engineers"


def save_photo_fig(fig, name):
    fig.savefig(OUT / name, dpi=130, bbox_inches="tight", pad_inches=0.1, pil_kwargs={"quality": 85})
    plt.close(fig)


def draw(img, dets, scale=1.0, highlight=None, fs=0.55):
    """Like detect.draw, but keeps labels inside the image and can upscale first."""
    im = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC) if scale != 1 else img.copy()
    H, W = im.shape[:2]
    for x1, y1, x2, y2, s, n in dets:
        x1, y1, x2, y2 = [int(round(v * scale)) for v in (x1, y1, x2, y2)]
        col = (72, 59, 208) if highlight and n in highlight else (92, 107, 11)
        cv2.rectangle(im, (x1, y1), (x2, y2), col, 2)
        t = f"{n} {s:.2f}"
        (tw, th), _ = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, fs, 1)
        lx = min(max(x1, 0), W - tw - 6)
        ly = y1 if y1 - th - 8 >= 0 else y1 + th + 8
        cv2.rectangle(im, (lx, ly - th - 8), (lx + tw + 6, ly), col, -1)
        cv2.putText(im, t, (lx + 3, ly - 5), cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 255), 1, cv2.LINE_AA)
    return im


def show(ax, bgr, title):
    ax.imshow(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    ax.set_title(title, fontsize=13, loc="left", color=INK, weight="bold")
    ax.axis("off")


# 1. Coordinates: (x, y) points, (h, w, c) shape, (w, h) sizes, [y1:y2, x1:x2] crops
fig, ax = plt.subplots(figsize=(10, 6.2))
W, H = 16, 9
ax.set_xlim(-1.2, W + 9.5); ax.set_ylim(H + 1.6, -1.6); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((0, 0), W, H, fc="#f4f3ef", ec=INK2, lw=1.5))
for x in range(1, W):
    ax.plot([x, x], [0, H], color=GRID, lw=0.8)
for y in range(1, H):
    ax.plot([0, W], [y, y], color=GRID, lw=0.8)
ax.annotate("", xy=(W + 0.8, -0.6), xytext=(-0.2, -0.6), arrowprops=dict(arrowstyle="-|>", color=C[0], lw=2))
ax.text(W / 2, -0.95, "x  (columns, width w)", ha="center", fontsize=12.5, color=INK)
ax.annotate("", xy=(-0.6, H + 0.8), xytext=(-0.6, -0.2), arrowprops=dict(arrowstyle="-|>", color=C[1], lw=2))
ax.text(-0.95, H / 2, "y  (rows, height h)", rotation=90, ha="center", va="center", fontsize=12.5, color=INK)
ax.plot(0, 0, "o", color=INK, ms=6)
ax.text(0.2, 0.55, "(0, 0)", fontsize=12, color=INK)
x1, y1, x2, y2 = 5, 3, 11, 7
ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fc=ACCENT + "33", ec=ACCENT, lw=2.2))
ax.plot([x1, x2], [y1, y2], "o", color=ACCENT, ms=7)
ax.text(x1 - 0.15, y1 - 0.25, "(x1, y1)", ha="right", fontsize=12, color=INK)
ax.text(x2 + 0.15, y2 + 0.55, "(x2, y2)", ha="left", fontsize=12, color=INK)
lines = [
    ("img.shape", "(h, w, c)   rows first"),
    ("cv2.resize(img, size)", "size = (w, h)"),
    ("cv2.VideoWriter(..., size)", "size = (w, h)"),
    ("crop = img[y1:y2, x1:x2]", "rows (y) first"),
    ("cv2.rectangle(img, p1, p2, ...)", "points are (x, y),\nintegers"),
]
ty = 0.2
for code, note in lines:
    ax.text(W + 1.0, ty, code, fontsize=12, family="DejaVu Sans Mono", color=INK, va="top")
    ax.text(W + 1.3, ty + 0.75, note, fontsize=12, color=INK2, va="top")
    ty += 2.0 if "\n" not in note else 2.4
ax.set_title("Two orders to keep straight: arrays are (row, col), OpenCV sizes and points are (x, y)",
             loc="left", fontsize=13.5)
save(fig, f"{SLUG}-coordinates.png")

# 2. BGR vs RGB fed to the model (real detections)
img = detect.frame("retail", 0.5)
swapped = img[:, :, ::-1].copy()  # what a model sees when the channel order is wrong
d_ok = detect.detect(img)
d_sw = detect.detect(swapped)
fig, axes = plt.subplots(1, 2, figsize=(12, 3.7))
plt.subplots_adjust(wspace=0.03)
show(axes[0], draw(img, d_ok, scale=1.5), "Correct channel order")
show(axes[1], draw(swapped, d_sw, scale=1.5, highlight={"boat"}), "Channels swapped (BGR/RGB mix-up)")
save_photo_fig(fig, f"{SLUG}-bgr-rgb.jpg")
print("ok:", [(n, round(s, 2)) for *_, s, n in d_ok])
print("swapped:", [(n, round(s, 2)) for *_, s, n in d_sw])

# 3. Stretch vs letterbox to a square model input (real detections)
img = detect.frame("retail", 0.8)
S = 416
h, w = img.shape[:2]
r = S / max(h, w)
nh, nw = int(round(h * r)), int(round(w * r))
lb = np.full((S, S, 3), 114, np.uint8)
lb[:nh, :nw] = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)
d_lb = [(x1 * r, y1 * r, x2 * r, y2 * r, s, n) for x1, y1, x2, y2, s, n in detect.detect(img)]
st = cv2.resize(img, (S, S), interpolation=cv2.INTER_AREA)
d_st = detect.detect(st)
fig, axes = plt.subplots(1, 2, figsize=(11, 5.8))
plt.subplots_adjust(wspace=0.04)
show(axes[0], draw(lb, d_lb, scale=2, fs=0.75), "Letterbox: resize + pad")
show(axes[1], draw(st, d_st, scale=2, fs=0.75), "Stretch: resize to 416 x 416")
save_photo_fig(fig, f"{SLUG}-letterbox.jpg")
print("letterbox:", [(n, round(s, 2)) for *_, s, n in d_lb])
print("stretch:", [(n, round(s, 2)) for *_, s, n in d_st])
