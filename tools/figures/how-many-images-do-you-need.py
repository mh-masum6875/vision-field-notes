"""Figures for how-many-images-do-you-need."""
import io
import cv2
import numpy as np
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT
import detect

SLUG = "how-many-images-do-you-need"


def fig_to_jpg(fig, name, width=1400):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    return detect.save_jpg(img, name, width=width)


def read_frame_index(sample, idx):
    cap = cv2.VideoCapture(f"{detect.BENCH}/samples/{sample}.mp4")
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ok, img = cap.read()
    cap.release()
    return img


def nframes(sample):
    cap = cv2.VideoCapture(f"{detect.BENCH}/samples/{sample}.mp4")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return n


# ---- Figure 1: consecutive frames vs frames sampled at intervals (real footage) ----
def near_duplicates():
    s = "retail"
    n = nframes(s)
    base = int(n * 0.70)
    top = [base, base + 1, base + 2]
    bottom = [int(n * 0.05), int(n * 0.45), int(n * 0.80)]
    fig, axes = plt.subplots(2, 3, figsize=(10, 5.0))
    for row, idxs, label in [(0, top, "Consecutive\nframes"), (1, bottom, "Spaced\nseconds apart")]:
        for col, i in enumerate(idxs):
            img = read_frame_index(s, i)
            dets = detect.detect(img)
            ax = axes[row, col]
            ax.imshow(detect.draw(img, dets, thick=3, label=False)[:, :, ::-1])
            ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
            for sp in ax.spines.values():
                sp.set_visible(False)
            ax.set_title(f"t = {i / 15:.1f} s,  {len(dets)} boxes", fontsize=12, fontweight="normal", color=INK2)
        axes[row, 0].set_ylabel(label, fontsize=13, color=INK, fontweight="bold")
    fig.suptitle("Three consecutive frames add almost nothing; spaced frames add variety",
                 fontsize=14, fontweight="bold", y=1.0)
    fig.tight_layout()
    fig_to_jpg(fig, f"{SLUG}-frame-sampling.jpg")


# ---- Figure 2: learning curve by data size (illustrative) ----
def learning_curve():
    x = np.array([25, 50, 75, 100])
    rising = np.array([0.30, 0.45, 0.56, 0.66])
    flat = np.array([0.48, 0.58, 0.61, 0.62])
    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.plot(x, rising, "-o", color=C[0], label="Project A: still rising", ms=7)
    ax.plot(x, flat, "-o", color=C[1], label="Project B: flattening", ms=7)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{v}%" for v in x])
    ax.set_xlabel("Share of training images used (same validation set every time)")
    ax.set_ylabel("Validation metric (illustrative)")
    ax.set_yticklabels([])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(18, 132)
    ax.set_ylim(0.2, 0.75)
    ax.annotate("Collect more data:\nthe model is limited\nby examples", xy=(100, 0.66), xytext=(104, 0.67),
                color=INK, fontsize=12, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.annotate("Flattening: more of\nthe same helps little,\nstudy the errors", xy=(100, 0.62), xytext=(104, 0.53),
                color=INK, fontsize=12, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.legend(loc="upper left", fontsize=12)
    ax.set_title("Train on 25, 50, 75 and 100 percent, then read the slope")
    style.save(fig, f"{SLUG}-learning-curve.png")


if __name__ == "__main__":
    near_duplicates()
    learning_curve()
