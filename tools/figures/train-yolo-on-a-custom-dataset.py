"""Figures for train-yolo-on-a-custom-dataset."""
import io
import cv2
import numpy as np
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT, CRIT
from matplotlib.patches import FancyBboxPatch, Rectangle
import detect

SLUG = "train-yolo-on-a-custom-dataset"
Q_FC, O_FC = "#eef3fb", "#e8f3ef"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, fs=12, bold=False, color=INK, lw=1.5, family=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal", family=family)


def arrow(ax, x1, y1, x2, y2, color=INK2, rad=0.0, lw=1.6):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=16,
                                connectionstyle=f"arc3,rad={rad}"))


def fig_to_jpg(fig, name, width=1300):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    return detect.save_jpg(img, name, width=width)


def canvas(w, h, figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, w); ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


# ---- Figure 1: the workflow with its improvement loop ----
def workflow():
    fig, ax = canvas(10, 5.2, (10, 5.0))
    w, h = 2.05, 1.2
    xs = [0.15, 2.65, 5.15, 7.65]
    top = [("1. Environment", "venv, GPU check"), ("2-3. Images\n+ labels", "YOLO txt files"),
           ("4. Split", "by video, camera\nor time"), ("5. data.yaml", "paths + class names")]
    bot = [("9. Improve", "data first,\nsettings later"), ("8. Validate\n+ predict", "fresh footage"),
           ("7. Read results", "per class,\nlook at images"), ("6. Train", "pretrained .pt,\nsmall model")]
    ty, by = 3.3, 0.7
    for x, (t, sub) in zip(xs, top):
        box(ax, x, ty, w, h, t, fc=Q_FC, ec=C[0], bold=True)
        ax.text(x + w / 2, ty - 0.12, sub, ha="center", va="top", fontsize=11.5, color=INK2)
    for x, (t, sub) in zip(xs, bot):
        fc, ec = (O_FC, ACCENT)
        box(ax, x, by, w, h, t, fc=fc, ec=ec, bold=True)
        ax.text(x + w / 2, by - 0.12, sub, ha="center", va="top", fontsize=11.5, color=INK2)
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, a + w, ty + h / 2, b, ty + h / 2)
        arrow(ax, b, by + h / 2, a + w, by + h / 2)
    # down from data.yaml to train
    arrow(ax, xs[3] + w / 2, ty - 0.75, xs[3] + w / 2, by + h + 0.05)
    # loop back from improve to images+labels
    arrow(ax, 1.9, by + h, 2.75, ty - 0.02, color=CRIT, lw=2)
    ax.text(2.5, 2.4, "loop back to\nthe data", color=CRIT, fontsize=12, ha="left",
            va="center", fontweight="bold")
    ax.text(5, 5.05, "Most of the loop is data work; training is one box of nine",
            ha="center", va="center", fontsize=14, fontweight="bold")
    style.save(fig, f"{SLUG}-workflow.png")


# ---- Figure 2: one label line explained on a real frame ----
def label_format():
    img = detect.frame("safety", 0.70)
    H, W = img.shape[:2]
    d = max(detect.detect(img), key=lambda d: d[4])
    x1, y1, x2, y2 = [v for v in d[:4]]
    xc, yc, bw, bh = (x1 + x2) / 2 / W, (y1 + y2) / 2 / H, (x2 - x1) / W, (y2 - y1) / H
    nx1, ny1, nx2, ny2 = x1 / W, y1 / H, x2 / W, y2 / H
    line = f"0 {xc:.3f} {yc:.3f} {bw:.3f} {bh:.3f}"
    print(d, line)
    fig = plt.figure(figsize=(10, 6.9))
    ax = fig.add_axes([0.06, 0.25, 0.9, 0.68])
    ax.imshow(img[:, :, ::-1], extent=[0, 1, 1, 0], aspect=H / W)
    ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1])
    ax.grid(False)
    ax.tick_params(labelsize=12)
    ax.add_patch(Rectangle((nx1, ny1), bw, bh, fill=False, ec=ACCENT, lw=2.5))
    ax.plot([xc], [yc], "o", ms=8, mfc="white", mec=INK, mew=1.5)
    ax.annotate(f"centre ({xc:.3f}, {yc:.3f})", xy=(xc, yc), xytext=(nx2 + 0.08, yc - 0.12),
                fontsize=12, color="white", arrowprops=dict(arrowstyle="->", color="white", lw=1.5),
                bbox=dict(fc=INK, ec="none", pad=3, alpha=0.8))
    # width arrow below the box
    yb = ny2 + 0.03
    ax.annotate("", xy=(nx1, yb), xytext=(nx2, yb), arrowprops=dict(arrowstyle="<->", color="white", lw=2))
    ax.text(xc, yb + 0.012, f"width {bw:.3f}", ha="center", va="top", fontsize=12, color="white",
            bbox=dict(fc=INK, ec="none", pad=2, alpha=0.8))
    xr = nx1 - 0.03
    ax.annotate("", xy=(xr, ny1), xytext=(xr, ny2), arrowprops=dict(arrowstyle="<->", color="white", lw=2))
    ax.text(xr - 0.01, yc, f"height\n{bh:.3f}", ha="right", va="center", fontsize=12, color="white",
            bbox=dict(fc=INK, ec="none", pad=2, alpha=0.8))
    ax.set_title("A YOLO label is one line per object, in fractions of the image size", pad=10)
    # the text line with field names
    fields = line.split()
    names = ["class_id", "x_center", "y_center", "width", "height"]
    fig.text(0.06, 0.135, "img001.txt", fontsize=12, color=INK2, family="monospace")
    xs = [0.06, 0.2, 0.38, 0.56, 0.74]
    for x, f, n in zip(xs, fields, names):
        fig.text(x, 0.075, f, fontsize=17, family="monospace", color=INK, fontweight="bold")
        fig.text(x, 0.025, n, fontsize=12, color=INK2)
    fig_to_jpg(fig, f"{SLUG}-label-format.jpg")


# ---- Figure 3: how images and labels pair up ----
def folder_pairing():
    fig, ax = canvas(10, 5.6, (10, 5.2))
    rows = [("img001", 3.3), ("img002", 2.0), ("img003", 0.7)]
    ax.text(1.9, 4.55, "dataset/images/train/", ha="center", fontsize=13, family="monospace", fontweight="bold")
    ax.text(8.1, 4.55, "dataset/labels/train/", ha="center", fontsize=13, family="monospace", fontweight="bold")
    ax.text(5.0, 4.6, "same base name,\n'images' becomes 'labels'", ha="center", va="center", fontsize=12, color=INK2)
    contents = ["0 0.257 0.491 0.136 0.591", "two lines = two objects", "empty file = background image"]
    for (name, y), cont in zip(rows, contents):
        box(ax, 0.6, y, 2.6, 0.7, f"{name}.jpg", fc=Q_FC, ec=C[0], family="monospace")
        box(ax, 6.8, y, 2.6, 0.7, f"{name}.txt", fc=O_FC, ec=ACCENT, family="monospace")
        arrow(ax, 3.25, y + 0.35, 6.75, y + 0.35)
        ax.text(8.1, y - 0.1, cont, ha="center", va="top", fontsize=11.5, color=INK2,
                family="monospace" if cont[0].isdigit() else None)
    ax.set_ylim(-0.5, 5.6)
    ax.text(5.0, -0.3, "A missing or misnamed .txt file silently means 'no objects in this image'",
            ha="center", va="center", fontsize=12, color=CRIT)
    ax.text(5.0, 5.35, "Ultralytics finds each label by swapping the folder name and extension",
            ha="center", va="center", fontsize=14, fontweight="bold")
    style.save(fig, f"{SLUG}-folder-pairing.png")


if __name__ == "__main__":
    workflow()
    label_format()
    folder_pairing()
