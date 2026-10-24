"""Figures for host-cv-demos-free-on-github-pages.md"""
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, OUT, save
import detect

SLUG = "host-cv-demos-free-on-github-pages"


def box(ax, x, y, w, h, color, fill=0.12, lw=1.6, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw, ls=ls))


def arrow(ax, p1, p2, color=INK2):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.7, mutation_scale=15))


def draw(img, dets, scale=1.0, fs=0.6):
    im = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC) if scale != 1 else img.copy()
    H, W = im.shape[:2]
    col = (92, 107, 11)
    for x1, y1, x2, y2, s, n in dets:
        x1, y1, x2, y2 = [int(round(v * scale)) for v in (x1, y1, x2, y2)]
        cv2.rectangle(im, (x1, y1), (x2, y2), col, 2)
        t = f"{n} {s:.2f}"
        (tw, th), _ = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, fs, 1)
        lx = min(max(x1, 0), W - tw - 6)
        ly = y1 if y1 - th - 8 >= 0 else y1 + th + 8
        cv2.rectangle(im, (lx, ly - th - 8), (lx + tw + 6, ly), col, -1)
        cv2.putText(im, t, (lx + 3, ly - 5), cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 255), 1, cv2.LINE_AA)
    return im


# 1. Static hosting, inference in the browser
fig, ax = plt.subplots(figsize=(10, 6.0))
ax.set_xlim(0, 12); ax.set_ylim(0, 7.2); ax.axis("off")
ax.text(0.05, 7.1, "GitHub Pages only serves files; the model runs in the visitor's browser",
        fontsize=14, weight="bold", va="top")
box(ax, 0.1, 4.0, 3.7, 2.4, MUTED)
ax.text(1.95, 6.0, "GitHub repository", ha="center", fontsize=13, weight="bold")
for i, f in enumerate(["index.html", "app.js", "style.css", "model/best.onnx"]):
    ax.text(0.45, 5.45 - i * 0.4, f, fontsize=12, family="DejaVu Sans Mono", va="center")
box(ax, 4.6, 4.5, 2.9, 1.4, C[0])
ax.text(6.05, 5.45, "GitHub Pages", ha="center", fontsize=13, weight="bold")
ax.text(6.05, 4.9, "static files only,\nno Python", ha="center", va="center", fontsize=12, color=INK2)
arrow(ax, (3.8, 5.2), (4.6, 5.2))
ax.text(6.25, 4.05, "files downloaded once (use relative paths)", ha="left", va="center", fontsize=12, color=INK2)
arrow(ax, (6.05, 4.5), (6.05, 3.6))
# browser
box(ax, 0.1, 0.25, 11.8, 3.3, C[2], fill=0.06)
ax.text(0.35, 3.15, "Visitor's browser", fontsize=13, weight="bold", va="center")
ax.text(11.65, 3.15, "the image never leaves the device", fontsize=12, color="#087a08", ha="right", va="center")
steps = [("Image or\nwebcam\nframe", C[1]), ("Preprocess:\nresize, RGB,\nscale 0-1", C[1]), ("ONNX\nRuntime Web\n(WASM or\nWebGPU)", C[0]),
         ("Decode,\nthreshold,\nNMS", C[1]), ("Draw boxes\non canvas", C[1])]
w, gap, x = 2.0, 0.36, 0.35
for i, (t, col) in enumerate(steps):
    box(ax, x, 0.55, w, 2.0, col)
    ax.text(x + w / 2, 1.55, t, ha="center", va="center", fontsize=12, linespacing=1.3)
    if i < len(steps) - 1:
        arrow(ax, (x + w + 0.02, 1.55), (x + w + gap - 0.02, 1.55))
    x += w + gap
save(fig, f"{SLUG}-architecture.png")

# 2. What a confidence slider shows (real detections)
img = detect.frame("retail", 0.8)
fig, axes = plt.subplots(1, 2, figsize=(12, 3.75))
plt.subplots_adjust(wspace=0.03)
for ax, conf in zip(axes, (0.25, 0.60)):
    d = detect.detect(img, conf=conf)
    print(conf, [(n, round(s, 2)) for *_, s, n in d])
    ax.imshow(cv2.cvtColor(draw(img, d, scale=1.5, fs=0.8), cv2.COLOR_BGR2RGB))
    ax.axis("off")
    ax.set_title(f"Confidence slider at {conf:.2f}: {len(d)} boxes", loc="left", fontsize=13, weight="bold")
fig.savefig(OUT / f"{SLUG}-confidence-slider.jpg", dpi=130, bbox_inches="tight", pad_inches=0.1,
            pil_kwargs={"quality": 85})
plt.close(fig)
