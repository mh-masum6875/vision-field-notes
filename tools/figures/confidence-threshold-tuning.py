"""Figures for confidence-threshold-tuning: one real frame at three thresholds, and illustrative P/R/F1 vs confidence."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, OUT
import detect

SLUG = "confidence-threshold-tuning"


def annot(img, dets, k=2, color=(92, 107, 11), fs=1.0, thick=3):
    im = cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC)
    for x1, y1, x2, y2, s, n in sorted(dets, key=lambda d: d[4]):
        p1, p2 = (int(x1 * k), int(y1 * k)), (int(x2 * k), int(y2 * k))
        cv2.rectangle(im, p1, p2, color, thick)
    for x1, y1, x2, y2, s, n in sorted(dets, key=lambda d: d[4]):
        p1 = (int(x1 * k), int(y1 * k))
        t = f"{n} {s:.2f}"
        (tw, th), _ = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, fs, 2)
        y0 = max(p1[1], th + 12)
        x0 = max(0, min(p1[0], im.shape[1] - tw - 10))
        cv2.rectangle(im, (x0, y0 - th - 12), (x0 + tw + 10, y0), color, -1)
        cv2.putText(im, t, (x0 + 5, y0 - 7), cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 255), 2, cv2.LINE_AA)
    return im[:, :, ::-1]


def save_jpg_fig(fig, name, width_px=1400):
    w = fig.get_size_inches()[0]
    fig.savefig(OUT / name, dpi=width_px / w, bbox_inches="tight", pad_inches=0.12, pil_kwargs={"quality": 85})
    plt.close(fig)


def fig_real_thresholds():
    img = detect.frame("retail", 0.4)
    alld = detect.detect(img, 0.10)
    print([(n, round(s, 2)) for *_, s, n in alld])
    # crop to the right half where all the detections are
    x0 = 300
    crop = img[:, x0:]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.0))
    for ax, t in zip(axes, [0.10, 0.30, 0.50]):
        d = [(a - x0, b, c - x0, e, s, n) for a, b, c, e, s, n in alld if s >= t]
        ax.imshow(annot(crop, d, fs=1.05))
        ax.set_title(f"Threshold {t:.2f}: {len(d)} box{'es' if len(d) != 1 else ''}", loc="left", fontsize=13)
        ax.axis("off")
    fig.tight_layout(w_pad=1.0)
    save_jpg_fig(fig, f"{SLUG}-three-thresholds.jpg")


def fig_curves():
    t = np.linspace(0.02, 0.95, 300)
    # illustrative shapes, not measurements
    precision = 0.45 + 0.53 / (1 + np.exp(-(t - 0.32) / 0.07))
    recall = 0.97 / (1 + np.exp((t - 0.62) / 0.08))
    f1 = 2 * precision * recall / (precision + recall)
    need_p, need_r = 0.85, 0.75
    ok = (precision >= need_p) & (recall >= need_r)
    lo, hi = t[ok].min(), t[ok].max()
    fig, ax = plt.subplots(figsize=(9.5, 5.3))
    ax.axvspan(lo, hi, color=ACCENT, alpha=0.12, lw=0)
    ax.plot(t, precision, color=C[0], label="Precision")
    ax.plot(t, recall, color=C[1], label="Recall")
    ax.plot(t, f1, color=C[2], ls="--", label="F1")
    ax.axhline(need_p, color=C[0], lw=1, ls=":")
    ax.axhline(need_r, color=C[1], lw=1, ls=":")
    ax.text(0.94, need_p - 0.015, f"precision you need: {need_p}", fontsize=11, color=INK2, va="top", ha="right")
    ax.text(0.94, need_r - 0.015, f"recall you need: {need_r}", fontsize=11, color=INK2, va="top", ha="right")
    ax.text((lo + hi) / 2, 0.06, f"acceptable\n{lo:.2f} to {hi:.2f}", ha="center", va="bottom", fontsize=11.5, color=INK, weight="bold")
    i = int(np.argmax(f1))
    ax.plot([t[i]], [f1[i]], "o", color=C[2], ms=7)
    ax.annotate(f"F1 peak at {t[i]:.2f}", xy=(t[i], f1[i]), xytext=(0.06, 0.3), fontsize=11.5, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2))
    ax.set_xlim(0, 0.95); ax.set_ylim(0, 1.05)
    ax.set_xlabel("Confidence threshold")
    ax.set_ylabel("Score")
    ax.set_title("Pick the threshold where both needs are met (illustrative)", loc="left")
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.5), fontsize=11.5)
    print("acceptable", round(lo, 2), round(hi, 2), "f1 peak", round(t[i], 2))
    style.save(fig, f"{SLUG}-pr-vs-threshold.png")


if __name__ == "__main__":
    fig_real_thresholds()
    fig_curves()
