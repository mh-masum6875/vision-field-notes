"""Figures for fine-tuning-yolo-transfer-learning."""
import io
import cv2
import numpy as np
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT, CRIT
from matplotlib.patches import FancyBboxPatch, Rectangle
import detect

SLUG = "fine-tuning-yolo-transfer-learning"
B_FC, N_FC = "#eef3fb", "#fdf0ea"


def fig_to_jpg(fig, name, width=1300):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    return detect.save_jpg(img, name, width=width)


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, fs=12, bold=False, color=INK, lw=1.5, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=fc, ec=ec, lw=lw, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, color=INK2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16))


# ---- Figure 1: what is reused and what is new ----
def architecture():
    fig, ax = plt.subplots(figsize=(10, 4.3))
    ax.set_xlim(0, 10); ax.set_ylim(0.45, 5.0); ax.axis("off")
    y, h = 1.6, 1.6
    box(ax, 0.1, y, 1.4, h, "Your\nimage", fc="#ffffff")
    box(ax, 2.0, y, 3.0, h, "Backbone\nedges, textures,\nobject parts", fc=B_FC, ec=C[0])
    box(ax, 5.5, y, 1.8, h, "Neck\ncombines\nscales", fc=B_FC, ec=C[0])
    box(ax, 7.8, y, 2.1, h, "Head\nboxes + your\nclass names", fc=N_FC, ec=C[1])
    arrow(ax, 1.5, y + h / 2, 2.0, y + h / 2)
    arrow(ax, 5.0, y + h / 2, 5.5, y + h / 2)
    arrow(ax, 7.3, y + h / 2, 7.8, y + h / 2)
    # reused / new brackets
    ax.plot([2.0, 7.3], [3.55, 3.55], color=C[0], lw=2)
    ax.text(4.65, 3.7, "reused from the COCO checkpoint (yolo11n.pt)", ha="center", va="bottom",
            fontsize=12.5, color=INK)
    ax.plot([7.8, 9.9], [3.55, 3.55], color=C[1], lw=2)
    ax.text(8.85, 3.7, "re-created for\nyour class count", ha="center", va="bottom", fontsize=12.5, color=INK)
    # freeze bracket
    ax.add_patch(FancyBboxPatch((1.9, 1.35), 3.2, 2.1, boxstyle="round,pad=0,rounding_size=0.15",
                                fc="none", ec=INK2, lw=1.4, ls="--"))
    ax.text(3.5, 1.15, "freeze: keep these early layers fixed\n(worth testing on small datasets)",
            ha="center", va="top", fontsize=12, color=INK2)
    ax.text(5.0, 4.85, "Fine-tuning keeps the general features and relearns the output",
            ha="center", va="center", fontsize=14, fontweight="bold")
    style.save(fig, f"{SLUG}-what-is-reused.png")


# ---- Figure 2: what the pretrained model already knows (real detections) ----
def out_of_box():
    img = detect.frame("safety", 0.70)
    dets = detect.detect(img)
    print("dets:", [(d[5], round(d[4], 2)) for d in dets])
    H, W = img.shape[:2]
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    ax.imshow(img[:, :, ::-1])
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    for x1, y1, x2, y2, s, n in dets:
        ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, ec=ACCENT, lw=2.5))
        ax.text(x1, y1 - 3, f"{n} {s:.2f}", fontsize=12, color="white", va="bottom", ha="left",
                bbox=dict(fc=ACCENT, ec="none", pad=2))
    p = max(dets, key=lambda d: d[4])
    px1, py1, px2, py2 = p[:4]
    pw, ph = px2 - px1, py2 - py1
    helmet = (px1 + pw * 0.5, py1 + ph * 0.07)
    vest = (px1 + pw * 0.55, py1 + ph * 0.35)
    style_kw = dict(fontsize=12.5, color="white", bbox=dict(fc=INK, ec="none", pad=3, alpha=0.85),
                    arrowprops=dict(arrowstyle="->", color="white", lw=1.6))
    ax.annotate("hard hat: not a COCO class", xy=helmet, xytext=(px2 + 90, py1 + 15), **style_kw)
    ax.annotate("safety vest: not a COCO class", xy=vest, xytext=(px2 + 90, py1 + 95), **style_kw)
    ax.set_title("Out of the box, the COCO model finds the person but has no hard hat or vest class",
                 fontsize=13.5)
    fig_to_jpg(fig, f"{SLUG}-coco-out-of-box.jpg")


if __name__ == "__main__":
    architecture()
    out_of_box()
