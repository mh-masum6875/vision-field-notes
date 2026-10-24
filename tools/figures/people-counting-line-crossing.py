"""Figures for people-counting-line-crossing."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT, save
import detect

SLUG = "people-counting-line-crossing"


def hex2bgr(h):
    h = h.lstrip("#")
    return (int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16))


# ---------------------------------------------------------------- minimal tracker (ByteTrack-style two rounds)
def iou(a, b):
    x1, y1, x2, y2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    return inter / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter + 1e-9)


def greedy(tracks, dets, tids, thr=0.3):
    pairs = sorted(((iou(tracks[t]["box"], d[:4]), t, j) for t in tids for j, d in enumerate(dets)), reverse=True)
    ut, ud, out = set(), set(), []
    for v, t, j in pairs:
        if v < thr:
            break
        if t in ut or j in ud:
            continue
        ut.add(t); ud.add(j); out.append((t, j))
    return out


def run_tracker(all_dets, high=0.5, low=0.1, max_age=8):
    tracks, nid, out = {}, 1, []
    for dets in all_dets:
        dets = [d for d in dets if d[5] == "person"]
        hi = [d for d in dets if d[4] >= high]
        lo = [d for d in dets if low <= d[4] < high]
        assigned = {}
        m1 = greedy(tracks, hi, list(tracks))
        for t, j in m1:
            assigned[t] = hi[j]
        for t, j in greedy(tracks, lo, [t for t in tracks if t not in assigned]):
            assigned[t] = lo[j]
        used = {j for _, j in m1}
        for j, d in enumerate(hi):
            if j not in used:
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


def side(a, b, p):
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def within_segment(a, b, p):
    a, b, p = map(np.asarray, (a, b, p))
    t = np.dot(p - a, b - a) / np.dot(b - a, b - a)
    return 0 <= t <= 1


# ---------------------------------------------------------------- 1. real counting run
cap = cv2.VideoCapture(f"{detect.BENCH}/samples/people.mp4")
frames, dets = [], []
while True:
    ok, im = cap.read()
    if not ok:
        break
    frames.append(im)
    dets.append(detect.detect(im, conf=0.1))
tracked = run_tracker(dets)

A, B = (70, 290), (500, 290)          # counting line; moving up the image = "in"
paths, last_side, counted, crossings = {}, {}, {}, []
count_in = count_out = 0
for fi, assigned in enumerate(tracked):
    for tid, d in assigned.items():
        p = ((d[0] + d[2]) / 2, d[3])  # bottom centre
        paths.setdefault(tid, []).append(p)
        s = side(A, B, p)
        prev = last_side.get(tid)
        last_side[tid] = s
        if prev is None or prev == 0 or s == 0 or (prev > 0) == (s > 0):
            continue
        if not within_segment(A, B, p) or fi - counted.get(tid, -10**9) < 30:
            continue
        counted[tid] = fi
        crossings.append((tid, p))
        if prev > 0:          # below the line -> above the line
            count_in += 1
        else:
            count_out += 1
print("tracks:", {t: len(v) for t, v in paths.items()}, "in", count_in, "out", count_out)

im = frames[150].copy()                # empty room as background
cv2.line(im, A, B, hex2bgr(ACCENT), 3, cv2.LINE_AA)
cv2.arrowedLine(im, (520, 315), (520, 265), hex2bgr(ACCENT), 2, cv2.LINE_AA, tipLength=0.3)
cv2.putText(im, "in", (530, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.6, hex2bgr(ACCENT), 2, cv2.LINE_AA)
ci = 0
for tid, pts in paths.items():
    if len(pts) < 8:
        continue
    col = hex2bgr(C[ci % len(C)]); ci += 1
    arr = np.array(pts, np.int32)
    cv2.polylines(im, [arr], False, col, 2, cv2.LINE_AA)
    for q in arr[::3]:
        cv2.circle(im, tuple(int(v) for v in q), 3, col, -1, cv2.LINE_AA)
    cross = [p for t_, p in crossings if t_ == tid]
    if cross:   # label next to the crossing point, on the side away from the other tracks
        cx, cy = int(cross[0][0]), int(cross[0][1])
        org = (cx + 12, cy - 16) if cx >= 300 else (cx - 62, cy + 28) if cx >= 250 else (cx - 62, cy - 16)
    else:
        end = arr[-1]
        org = (int(end[0]) - 70, int(end[1]) - 10)
    (tw, th), _ = cv2.getTextSize(f"ID {tid}", cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
    cv2.rectangle(im, (org[0] - 3, org[1] - th - 4), (org[0] + tw + 3, org[1] + 4), (30, 30, 30), -1)
    cv2.putText(im, f"ID {tid}", org, cv2.FONT_HERSHEY_SIMPLEX, 0.55, col, 1, cv2.LINE_AA)
for tid, p in crossings:
    cv2.circle(im, (int(p[0]), int(p[1])), 9, (255, 255, 255), 2, cv2.LINE_AA)
cv2.rectangle(im, (8, 8), (175, 62), (30, 30, 30), -1)
cv2.putText(im, f"in:  {count_in}", (18, 31), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 1, cv2.LINE_AA)
cv2.putText(im, f"out: {count_out}", (18, 54), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 1, cv2.LINE_AA)
im = cv2.resize(im, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
detect.save_jpg(im, f"{SLUG}-real-tracks.jpg")


# ---------------------------------------------------------------- 2. jitter on the line (illustrative)
rng = np.random.default_rng(3)
t = np.linspace(0, 12, 181)            # 15 frames per second
pos = np.interp(t, [0, 3, 9, 12], [-60, 0, 2, 60]) + rng.normal(0, 3.5, t.size)   # px from line, +: past it
naive_n, hyst_n, state, n_naive, n_h = [], [], -1, 0, 0
M = 15                                                    # margin in px either side of the line
naive_t = []
for i, v in enumerate(pos):
    if i and np.sign(v) != np.sign(pos[i - 1]):
        n_naive += 1
        naive_t.append(t[i])
    if state < 0 and v > M:
        state, n_h = 1, n_h + 1
    elif state > 0 and v < -M:
        state, n_h = -1, n_h + 1
    naive_n.append(n_naive); hyst_n.append(n_h)

fig, ax = plt.subplots(figsize=(10, 4.4))
ax.axhspan(-M, M, color=GRID, alpha=0.7, lw=0)
ax.axhline(0, color=ACCENT, lw=1.5)
ax.plot(t, pos, color=C[0], lw=1.6, label="Foot point, signed distance to the line")
ax.scatter(naive_t, np.zeros(len(naive_t)), marker="|", s=160, color=C[1], lw=2, zorder=3,
           label="Counted by the plain sign test")
ax.set_xlim(0, 12); ax.set_ylim(-75, 75)
ax.set_xlabel("Seconds")
ax.set_ylabel("Pixels from the counting line")
ax.text(0.2, M + 3, "margin band", fontsize=12, color=INK2, va="bottom")
ax.text(6, -45, f"Plain sign change: {naive_n[-1]} counts\nWith a {M} px margin: {hyst_n[-1]} count",
        ha="center", va="center", fontsize=13, color=INK,
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=GRID))
ax.set_title("One person pausing on the line: a plain sign test counts every wobble", loc="left")
ax.legend(loc="upper left", fontsize=12)
print("naive", n_naive, "hyst", n_h)
save(fig, f"{SLUG}-jitter-hysteresis.png")
