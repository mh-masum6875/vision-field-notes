"""Figures for computer-vision-portfolio-that-gets-clients.md"""
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT, OUT, save
import detect

SLUG = "computer-vision-portfolio-that-gets-clients"


def box(ax, x, y, w, h, color, fill=0.12, lw=1.5, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw, ls=ls))


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


# 1. Project page layout: top for the business reader, below for the technical reader
fig, ax = plt.subplots(figsize=(10, 6.3))
ax.set_xlim(0, 12); ax.set_ylim(1.7, 11.2); ax.axis("off")
ax.text(0.05, 11.1, "One project page, written for two readers", fontsize=14, weight="bold", va="top")
sections = [  # (label, height)
    ("1  Problem, in one or two plain sentences", 0.7),
    ("2  Visual: short video or GIF on real footage", 1.9),
    ("3  Your role and the scope", 0.7),
    ("4  Data: source, size, labelling, split", 0.7),
    ("5  Method: model, key settings, why", 0.7),
    ("6  Results on held-out data, per class", 0.7),
    ("7  Failures and what you learned", 0.7),
    ("8  Deployment: hardware, measured speed", 0.7),
    ("9  Links: code, live demo, write-up", 0.7),
]
px, pw = 0.2, 7.3
box(ax, px - 0.1, 1.85, pw + 0.2, 8.55, MUTED, fill=0.04, lw=1.2)
y = 10.2
spans = []
for i, (label, h) in enumerate(sections):
    y -= h
    col = C[0] if i < 3 else C[1]
    box(ax, px + 0.1, y + 0.06, pw - 0.2, h - 0.12, col, fill=0.14 if i == 1 else 0.08)
    if i == 1:
        ax.text(px + 0.35, y + h - 0.4, label, fontsize=12, va="center")
        box(ax, px + 2.2, y + 0.25, 3.0, 1.0, INK2, fill=0.10, lw=1)
        ax.text(px + 3.7, y + 0.75, "output on real footage", ha="center", va="center", fontsize=11.5, color=INK2)
    else:
        ax.text(px + 0.35, y + h / 2, label, fontsize=12, va="center")
    spans.append((y, y + h))
    y -= 0.08


def bracket(y0, y1, title, sub, col):
    x = px + pw + 0.25
    ax.plot([x, x + 0.2, x + 0.2, x], [y1 - 0.08, y1 - 0.08, y0 + 0.08, y0 + 0.08], color=col, lw=2)
    ax.text(x + 0.45, (y0 + y1) / 2 + 0.75, title, fontsize=12.5, weight="bold", va="center")
    ax.text(x + 0.45, (y0 + y1) / 2 + 0.4, sub, fontsize=12, color=INK2, va="top", linespacing=1.3)


bracket(spans[2][0], spans[0][1], "Business reader", "understands the problem\nand sees it working\nin seconds", C[0])
bracket(spans[8][0], spans[3][1], "Technical reader", "checks the split, the\nmetrics, the failures\nand the hardware", C[1])
save(fig, f"{SLUG}-project-page.png")

# 2. Show a success and a failure (real detections)
cases = [("safety", 0.2, "Works: worker found at 0.89"), ("people", 0.18, "Fails: person labelled \"dog\"")]
fig, axes = plt.subplots(1, 2, figsize=(12, 3.75))
plt.subplots_adjust(wspace=0.03)
for ax, (sample, t, title) in zip(axes, cases):
    img = detect.frame(sample, t)
    d = detect.detect(img)
    print(sample, t, [(n, round(s, 2)) for *_, s, n in d])
    ax.imshow(cv2.cvtColor(draw(img, d, scale=1.5, fs=0.85), cv2.COLOR_BGR2RGB))
    ax.axis("off")
    ax.set_title(title, loc="left", fontsize=13, weight="bold")
fig.savefig(OUT / f"{SLUG}-success-and-failure.jpg", dpi=130, bbox_inches="tight", pad_inches=0.1,
            pil_kwargs={"quality": 85})
plt.close(fig)
