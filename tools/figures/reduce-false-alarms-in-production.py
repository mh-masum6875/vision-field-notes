"""Figures for reduce-false-alarms-in-production."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from style import C, ACCENT, INK, INK2, MUTED, GRID, CRIT, OUT, save
import detect

SLUG = "reduce-false-alarms-in-production"


def hex2bgr(h):
    h = h.lstrip("#")
    return (int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16))


def draw_big(img, dets, color):
    im = img.copy()
    for x1, y1, x2, y2, s, n in dets:
        p1, p2 = (int(x1), int(y1)), (int(x2), int(y2))
        cv2.rectangle(im, p1, p2, color, 2)
        t = f"{n} {s:.2f}"
        (tw, th), _ = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        y0 = max(p1[1], th + 10)
        x0 = min(p1[0], im.shape[1] - tw - 8)
        cv2.rectangle(im, (x0, y0 - th - 10), (x0 + tw + 8, y0), color, -1)
        cv2.putText(im, t, (x0 + 4, y0 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    return im


def read_all(sample):
    cap = cv2.VideoCapture(f"{detect.BENCH}/samples/{sample}.mp4")
    out = []
    while True:
        ok, im = cap.read()
        if not ok:
            break
        out.append(im)
    return out


# ---------------------------------------------------------------- 1. wrong-object detections, real model output
people = read_all("people")
traffic = read_all("traffic")
pa = draw_big(people[70], detect.detect(people[70]), hex2bgr(CRIT))
pb = draw_big(traffic[95], detect.detect(traffic[95]), hex2bgr(CRIT))
fig, axes = plt.subplots(1, 2, figsize=(10, 3.2))
for ax, im, title in [(axes[0], pa, "Person scored as 'dog', window as 'tv'"),
                      (axes[1], pb, "Car seen from above scored as 'cell phone'")]:
    ax.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, loc="left", fontsize=12)
fig.subplots_adjust(wspace=0.03)
fig.savefig(OUT / f"{SLUG}-wrong-object.jpg", dpi=150, bbox_inches="tight", pad_inches=0.12,
            pil_kwargs={"quality": 85})
plt.close(fig)


# ---------------------------------------------------------------- 2. the arithmetic of per-frame errors
rate = np.logspace(-5, -2, 200)          # share of analysed frames with a false detection
fig, ax = plt.subplots(figsize=(9.5, 4.6))
for fps, col in [(15, C[0]), (5, C[1]), (1, C[2])]:
    ax.plot(rate * 100, rate * fps * 86400, color=col, lw=2, label=f"{fps} analysed frame{'s' if fps > 1 else ''} per second")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(rate[0] * 100, rate[-1] * 100)
ax.set_ylim(0.5, 2e4)
ax.set_xticks([0.001, 0.01, 0.1, 1]); ax.set_xticklabels(["0.001%", "0.01%", "0.1%", "1%"])
ax.set_yticks([1, 10, 100, 1000, 10000]); ax.set_yticklabels(["1", "10", "100", "1,000", "10,000"])
ax.grid(which="minor", visible=False)
ax.set_xlabel("Share of frames with a false detection")
ax.set_ylabel("False events per camera per day")
ax.set_title("Rare per-frame errors still add up to many events a day", loc="left")
ax.legend(loc="upper left", fontsize=12)
ax.text(0.97, 0.05, "No temporal filter: each false frame\ncounts as one event. 24 h per day.",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=11.5, color=INK2)
save(fig, f"{SLUG}-per-frame-arithmetic.png")


# ---------------------------------------------------------------- 3. N-of-M filter on real detections
fps = 15.0
classes = ["person", "dog", "cat", "tv", "handbag"]
dets = [detect.detect(im) for im in people]
raw = {c: np.array([any(d[5] == c for d in f) for f in dets]) for c in classes}
N, M = 5, 8


def n_of_m(x):
    return np.array([x[max(0, i - M + 1):i + 1].sum() >= N for i in range(len(x))])


def events(x):
    return int(x[0] + np.sum(x[1:] & ~x[:-1]))


filt = {c: n_of_m(raw[c]) for c in classes}
t = np.arange(len(people)) / fps
fig, axes = plt.subplots(2, 1, figsize=(10, 5.4), sharex=True)
for ax, data, title in [(axes[0], raw, "Every frame with a detection (confidence 0.25 or more)"),
                        (axes[1], filt, f"Kept only when seen in {N} of the last {M} frames")]:
    for k, c in enumerate(classes):
        y = len(classes) - 1 - k
        on = t[data[c]]
        ax.scatter(on, np.full(on.size, y), marker="|", s=110, lw=1.6, color=C[0] if c == "person" else C[1])
        ax.text(t[-1] + 0.3, y, f"{events(data[c])} event{'s' if events(data[c]) != 1 else ''}",
                va="center", ha="left", fontsize=11.5, color=INK2)
    ax.set_yticks(range(len(classes))); ax.set_yticklabels(classes[::-1])
    ax.set_ylim(-0.7, len(classes) - 0.3)
    ax.grid(axis="y", visible=False)
    ax.set_title(title, loc="left", fontsize=13)
axes[1].set_xlabel("Seconds into the clip")
axes[1].set_xlim(0, t[-1])
fig.tight_layout()
save(fig, f"{SLUG}-n-of-m.png")
for c in classes:
    print(c, raw[c].sum(), events(raw[c]), filt[c].sum(), events(filt[c]))
