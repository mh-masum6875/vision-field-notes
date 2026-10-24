"""Figures for annotation-mistakes-that-hurt-models."""
import io
import cv2
import numpy as np
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT, CRIT, GOOD
from matplotlib.patches import Rectangle
import detect

SLUG = "annotation-mistakes-that-hurt-models"


def fig_to_jpg(fig, name, width=1400):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    return detect.save_jpg(img, name, width=width)


# ---- Figure 1: simulated label mistakes on a real frame ----
def label_mistakes():
    img = detect.frame("retail", 0.80)
    people = [d for d in detect.detect(img) if d[5] == "person"]
    people.sort(key=lambda d: d[0])
    print("person boxes:", [(round(d[0]), round(d[1]), round(d[2]), round(d[3]), round(d[4], 2)) for d in people])
    x0 = max(0, int(min(d[0] for d in people)) - 90)
    x1 = min(img.shape[1], int(max(d[2] for d in people)) + 40)
    crop = img[:, x0:x1, ::-1]

    def rect(ax, d, color, ls="-", lw=2.4):
        ax.add_patch(Rectangle((d[0] - x0, d[1]), d[2] - d[0], d[3] - d[1], fill=False, ec=color, lw=lw, ls=ls))

    def tag(ax, d, text, color, dy=-6):
        ax.text(d[0] - x0, d[1] + dy, text, color="white", fontsize=11, va="bottom", ha="left",
                bbox=dict(fc=color, ec="none", pad=2))

    target = people[0]  # the mistake is always made on this person
    panels = [
        ("Consistent labels", "ok"),
        ("Missing label: taught to ignore a person", "missing"),
        ("Loose box: edge rule unclear", "loose"),
        ("Duplicate box: one person, two labels", "dup"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(10, 7.6))
    for ax, (title, kind) in zip(axes.flat, panels):
        ax.imshow(crop)
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_title(title, fontsize=13, fontweight="bold",
                     color=INK)
        for d in people:
            if d is target and kind != "ok":
                continue
            rect(ax, d, ACCENT)
        t = target
        if kind == "ok":
            rect(ax, t, ACCENT)
        elif kind == "missing":
            rect(ax, t, CRIT, ls="--", lw=2)
            tag(ax, t, "no label", CRIT)
        elif kind == "loose":
            loose = (t[0] - 28, t[1] - 22, t[2] + 30, min(img.shape[0] - 2, t[3] + 15))
            rect(ax, loose, CRIT)
            tag(ax, loose, "loose", CRIT)
        elif kind == "dup":
            rect(ax, t, ACCENT)
            dup = (t[0] + 8, t[1] + 10, t[2] + 6, t[3] - 4)
            rect(ax, dup, CRIT)
            tag(ax, t, "2 boxes", CRIT, dy=-28)
    fig.suptitle("Each mistake teaches the model something false about the same scene",
                 fontsize=14, fontweight="bold", y=0.995)
    fig.tight_layout()
    fig_to_jpg(fig, f"{SLUG}-label-mistakes.jpg", width=1200)


# ---- Figure 2: box size scatter with red flags (illustrative) ----
def box_stats():
    rng = np.random.default_rng(7)
    n = 900
    w = np.clip(rng.lognormal(np.log(0.07), 0.45, n), 0.01, 0.5)
    h = np.clip(w * rng.lognormal(np.log(2.4), 0.18, n), 0.02, 0.95)
    tiny = np.array([[0.002, 0.003], [0.004, 0.002], [0.003, 0.006], [0.001, 0.002]])
    huge = np.array([[0.97, 0.99], [1.0, 0.98], [0.99, 1.0]])
    swapped = np.c_[h[:6] * 1.0, w[:6] * 1.0][[0, 2, 3, 5]] + [0.05, 0]
    fig, ax = plt.subplots(figsize=(9.5, 6))
    ax.scatter(w, h, s=12, color=C[0], alpha=0.35, lw=0, label="Typical person boxes")
    flags = np.vstack([tiny, huge, swapped])
    ax.scatter(flags[:, 0], flags[:, 1], s=60, facecolor="none", edgecolor=CRIT, lw=1.8,
               label="Boxes to inspect")
    ax.set_xlabel("Box width (fraction of image width)")
    ax.set_ylabel("Box height (fraction of image height)")
    ax.set_xlim(-0.02, 1.05); ax.set_ylim(-0.02, 1.08)
    ax.annotate("Near-zero size:\nslip of the mouse", xy=(0.008, 0.004), xytext=(0.36, 0.0),
                fontsize=12, color=INK, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.annotate("Whole-image boxes:\nconversion bug or\naccidental drag", xy=(0.97, 0.98), xytext=(0.62, 0.80),
                fontsize=12, color=INK, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.annotate("Wide, short boxes for an\nupright class: width and\nheight swapped?", xy=(0.25, 0.08),
                xytext=(0.42, 0.25), fontsize=12, color=INK, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.legend(loc="upper left", fontsize=12)
    ax.set_title("Plot box sizes: the errors sit apart from the crowd")
    style.save(fig, f"{SLUG}-box-sizes.png")
    print("swapped pts:", swapped.round(3).tolist())


if __name__ == "__main__":
    label_mistakes()
    box_stats()
