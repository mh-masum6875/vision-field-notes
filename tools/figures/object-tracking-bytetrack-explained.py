"""Figures for object-tracking-bytetrack-explained."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, OUT, save
import detect

SLUG = "object-tracking-bytetrack-explained"


# ---------------------------------------------------------------- 1. the loop
def box(ax, x, y, w, h, title, sub, color):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=1.5",
                                fc=color + "1f", ec=color, lw=1.6))
    ax.text(x, y + h * (0.27 if "\n" in sub and sub.count("\n") > 1 else 0.17), title, ha="center", va="center", fontsize=13, weight="bold", color=INK)
    ax.text(x, y - h * (0.13 if sub.count("\n") > 1 else 0.2), sub, ha="center", va="center", fontsize=11.5, color=INK2, linespacing=1.3)


def arrow(ax, p, q, rad=0.0):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.6, mutation_scale=16,
                                                    connectionstyle=f"arc3,rad={rad}"))


fig, ax = plt.subplots(figsize=(10, 4.6))
ax.set_xlim(0, 100); ax.set_ylim(1, 48); ax.axis("off")
W, H = 24, 13
pos = {"det": (15, 36), "pred": (50, 36), "assoc": (85, 36), "upd": (50, 10)}
box(ax, *pos["det"], W, H, "1. Detect", "detector runs on\nthe new frame", C[0])
box(ax, *pos["pred"], W, H, "2. Predict", "Kalman filter moves\neach track forward", C[1])
box(ax, *pos["assoc"], W, H, "3. Associate", "IoU cost, then\none-to-one matching", C[2])
box(ax, *pos["upd"], 38, 16, "4. Update", "matched: correct the track\nunmatched det: new track\nunmatched track: age, then drop", C[6])
arrow(ax, (27.5, 36), (37.5, 36))
arrow(ax, (62.5, 36), (72.5, 36))
arrow(ax, (85, 29), (70, 12), rad=-0.25)
arrow(ax, (30, 12), (15, 29), rad=-0.25)
ax.text(85, 20, "matches", ha="left", va="center", fontsize=12, color=INK2)
ax.text(10, 20, "next frame", ha="right", va="center", fontsize=12, color=INK2)
ax.text(50, 47, "The detector does the visual work; the tracker is bookkeeping and geometry",
        ha="center", va="top", fontsize=12.5, color=ACCENT, weight="bold")
save(fig, f"{SLUG}-loop.png")


# ---------------------------------------------------------------- 2. real occlusion example
def iou(a, b):
    x1, y1, x2, y2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    return inter / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter + 1e-9)


def greedy(tracks, dets, tids, thr=0.3):
    """Greedy one-to-one IoU matching. Returns list of (tid, det_index)."""
    pairs = sorted(((iou(tracks[t]["box"], d[:4]), t, j) for t in tids for j, d in enumerate(dets)), reverse=True)
    used_t, used_d, out = set(), set(), []
    for v, t, j in pairs:
        if v < thr:
            break
        if t in used_t or j in used_d:
            continue
        used_t.add(t); used_d.add(j); out.append((t, j))
    return out


def run_tracker(all_dets, two_round, high=0.5, low=0.1, max_age=8):
    """Minimal tracker for the figure. two_round=True follows the ByteTrack idea."""
    tracks, nid, out = {}, 1, []
    for dets in all_dets:
        dets = [d for d in dets if d[5] == "person"]
        hi = [d for d in dets if d[4] >= high]
        lo = [d for d in dets if low <= d[4] < high]
        assigned = {}
        m1 = greedy(tracks, hi, list(tracks))
        for t, j in m1:
            assigned[t] = hi[j]
        if two_round:
            rest = [t for t in tracks if t not in assigned]
            for t, j in greedy(tracks, lo, rest):
                assigned[t] = lo[j]
        used_hi = {j for _, j in m1}
        for j, d in enumerate(hi):
            if j not in used_hi:
                tracks[nid] = {"box": d[:4], "age": 0}
                assigned[nid] = d
                nid += 1
        for t in list(tracks):
            if t in assigned:
                tracks[t] = {"box": assigned[t][:4], "age": 0}
            else:
                tracks[t]["age"] += 1
                if tracks[t]["age"] > max_age:
                    del tracks[t]
        out.append(dict(assigned))
    return out


cap = cv2.VideoCapture(f"{detect.BENCH}/samples/retail.mp4")
frames, dets = [], []
while True:
    ok, im = cap.read()
    if not ok:
        break
    frames.append(im)
    dets.append(detect.detect(im, conf=0.1))

res = {m: run_tracker(dets, m) for m in (False, True)}
SHOW = [254, 261, 270]           # before, during and after the occlusion
TARGET_X = 490                    # the shopper partly hidden behind the man in front
BGR = {"hi": (214, 120, 42), "lo": (52, 104, 235)}   # C[0] blue, C[1] orange in BGR
CROP = (300, 640)                 # x range of the crop


def find_target(assigned):
    best = None
    for t, d in assigned.items():
        cx = (d[0] + d[2]) / 2
        if abs(cx - TARGET_X) < 40 and d[1] < 130:
            best = (t, d)
    return best


def panel(fi, two_round):
    im = frames[fi].copy()
    found = find_target(res[two_round][fi])
    raw = [d for d in dets[fi] if d[5] == "person" and abs((d[0] + d[2]) / 2 - TARGET_X) < 40 and d[1] < 130]
    raw = max(raw, key=lambda d: d[4]) if raw else None
    if raw is not None:
        x1, y1, x2, y2, s, _ = raw
        col = BGR["hi"] if s >= 0.5 else BGR["lo"]
        cv2.rectangle(im, (int(x1), int(y1)), (int(x2), int(y2)), col, 2)
        tag = f"ID {found[0]}" if found else "no track"
        txt = f"{tag}  conf {s:.2f}"
        (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        tx = int(min(x1, CROP[1] - tw - 8))
        cv2.rectangle(im, (tx, int(y1) - th - 10), (tx + tw + 8, int(y1)), col, -1)
        cv2.putText(im, txt, (tx + 4, int(y1) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    im = im[60:, CROP[0]:CROP[1]].copy()
    cv2.rectangle(im, (0, 0), (100, 28), (30, 30, 30), -1)
    cv2.putText(im, f"frame {fi}", (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


fig, axes = plt.subplots(2, 3, figsize=(10, 6.4))
for r, (mode, label) in enumerate([(False, "High-confidence boxes only"),
                                   (True, "Second round with low-confidence boxes")]):
    for c, fi in enumerate(SHOW):
        ax = axes[r, c]
        ax.imshow(panel(fi, mode)); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(False)
    axes[r, 0].set_title(label, loc="left", fontsize=13, x=0.0)
# legend for box colours
from matplotlib.lines import Line2D
fig.legend([Line2D([], [], color=C[0], lw=3), Line2D([], [], color=C[1], lw=3)],
           ["confidence 0.5 or above", "confidence below 0.5"], loc="upper center", ncol=2,
           fontsize=12, bbox_to_anchor=(0.5, 0.06))
fig.subplots_adjust(wspace=0.03, hspace=0.16)
fig.savefig(OUT / f"{SLUG}-occlusion-ids.jpg", dpi=130, bbox_inches="tight", pad_inches=0.15,
            pil_kwargs={"quality": 85})
plt.close(fig)

for m in (False, True):
    print("two_round" if m else "high_only", [find_target(res[m][f])[0] if find_target(res[m][f]) else None for f in range(250, 272)])
