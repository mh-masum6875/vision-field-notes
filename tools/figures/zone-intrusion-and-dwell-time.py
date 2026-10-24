"""Figures for zone-intrusion-and-dwell-time."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from style import C, ACCENT, INK, INK2, MUTED, GRID, CRIT, GOOD, OUT, save
import detect

SLUG = "zone-intrusion-and-dwell-time"


def hex2bgr(h):
    h = h.lstrip("#")
    return (int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16))


# Zone drawn on the real frame, following the red floor markings right of the hazard tape
ZONE = np.array([(235, 262), (400, 205), (600, 290), (515, 360), (290, 360)], np.int32)


def inside(p):
    return cv2.pointPolygonTest(ZONE, (float(p[0]), float(p[1])), False) >= 0


cap = cv2.VideoCapture(f"{detect.BENCH}/samples/safety.mp4")
fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
frames = []
while True:
    ok, im = cap.read()
    if not ok:
        break
    frames.append(im)

# first walk of the worker through the scene (frames 40-140)
track = []
for fi in range(40, 141):
    people = [d for d in detect.detect(frames[fi]) if d[5] == "person"]
    if people:
        track.append((fi, max(people, key=lambda d: d[4])))

# entry/exit events on the bottom-centre point, confirmed over 5 consecutive frames
CONFIRM = 5
state, run, events = False, 0, []
for fi, d in track:
    cut = d[3] >= frames[fi].shape[0] - 4
    now = inside(((d[0] + d[2]) / 2, d[3])) and not cut
    run = run + 1 if now != state else 0
    if run >= CONFIRM:
        state, run = now, 0
        events.append((fi, "entry" if now else "exit", ((d[0] + d[2]) / 2, d[3])))
print("events:", [(f, e) for f, e, _ in events])

zone_col = hex2bgr(C[1])


def draw_zone(im):
    ov = im.copy()
    cv2.fillPoly(ov, [ZONE], zone_col)
    im = cv2.addWeighted(ov, 0.18, im, 0.82, 0)
    cv2.polylines(im, [ZONE], True, zone_col, 2, cv2.LINE_AA)
    return im


# panel A: one frame where the two test points disagree
FA = 96
dA = dict(track)[FA]
a = draw_zone(frames[FA].copy())
x1, y1, x2, y2 = map(int, dA[:4])
cv2.rectangle(a, (x1, y1), (x2, y2), hex2bgr(ACCENT), 2)
foot = (int((x1 + x2) / 2), y2)
cen = (int((x1 + x2) / 2), int((y1 + y2) / 2))
cv2.circle(a, foot, 7, hex2bgr(C[0]), -1, cv2.LINE_AA)
cv2.circle(a, foot, 7, (255, 255, 255), 2, cv2.LINE_AA)
cv2.circle(a, cen, 7, (255, 255, 255), -1, cv2.LINE_AA)
cv2.circle(a, cen, 7, hex2bgr(INK2), 2, cv2.LINE_AA)
print("panel A foot inside:", inside(foot), "centre inside:", inside(cen))

# panel B: the whole walk, coloured by state
b = draw_zone(frames[5].copy())
pts = [((d[0] + d[2]) / 2, d[3], d[3] >= frames[fi].shape[0] - 4) for fi, d in track]
for (x, y, cut) in pts:
    if cut:
        cv2.circle(b, (int(x), int(y) - 3), 4, (170, 170, 170), 1, cv2.LINE_AA)
    else:
        cv2.circle(b, (int(x), int(y)), 4, hex2bgr(C[0]) if inside((x, y)) else (255, 255, 255), -1, cv2.LINE_AA)
for fi, kind, p in events:
    col = hex2bgr(CRIT) if kind == "entry" else hex2bgr(GOOD)
    cv2.drawMarker(b, (int(p[0]), int(p[1])), col, cv2.MARKER_DIAMOND, 18, 3, cv2.LINE_AA)
    txt = f"{kind} event"
    org = (int(p[0]) - 80, int(p[1]) + 32) if kind == "entry" else (int(p[0]) - 40, int(p[1]) - 18)
    (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)
    cv2.rectangle(b, (org[0] - 3, org[1] - th - 4), (org[0] + tw + 3, org[1] + 5), (30, 30, 30), -1)
    cv2.putText(b, txt, org, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
for ax, im, title in [(axes[0], a, "Feet in the zone, box centre not"),
                      (axes[1], b, "The whole walk, bottom-centre point")]:
    ax.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, loc="left", fontsize=12)
handles = [Line2D([], [], marker="o", ls="", color=C[0], ms=8, label="point inside zone"),
           Line2D([], [], marker="o", ls="", mfc="white", mec=INK2, ms=8, label="point outside zone"),
           Line2D([], [], marker="o", ls="", mfc="none", mec=MUTED, ms=8, label="box cut off by image edge"),
           Line2D([], [], color=C[1], lw=3, label="zone")]
fig.legend(handles=handles, loc="upper center", ncol=4, fontsize=11, bbox_to_anchor=(0.5, 0.1),
           handletextpad=0.3, columnspacing=1.2)
fig.subplots_adjust(wspace=0.03)
fig.savefig(OUT / f"{SLUG}-test-point.jpg", dpi=150, bbox_inches="tight", pad_inches=0.12,
            pil_kwargs={"quality": 85})
plt.close(fig)


# ---------------------------------------------------------------- 2. dwell timer with boundary flicker (illustrative)
rng = np.random.default_rng(11)
dt = 1 / 15
t = np.arange(0, 120, dt)
# a person stands close to the zone edge from 10 s to 110 s; the box jitter makes the point flicker outside
ins = (t >= 10) & (t < 110)
flick = ins & (rng.random(t.size) < 0.012)
for i in np.where(flick)[0]:
    ins[i:i + rng.integers(2, 10)] = False
ins[(t < 10) | (t >= 110)] = False

LIMIT, GRACE = 60.0, 2.0
naive, robust = np.zeros(t.size), np.zeros(t.size)
start_n = start_r = None
last_in = -1e9
alert_n = alert_r = None
for i, ti in enumerate(t):
    if ins[i]:
        start_n = ti if start_n is None else start_n
        last_in = ti
    else:
        start_n = None
    naive[i] = ti - start_n if start_n is not None else 0
    if ins[i] or ti - last_in <= GRACE:
        start_r = ti if start_r is None else start_r
    else:
        start_r = None
    robust[i] = ti - start_r if start_r is not None else 0
    if alert_n is None and naive[i] >= LIMIT:
        alert_n = ti
    if alert_r is None and robust[i] >= LIMIT:
        alert_r = ti
print("alerts naive:", alert_n, "robust:", alert_r)

fig, ax = plt.subplots(figsize=(10, 4.6))
ax.plot(t, naive, color=C[1], lw=2, label="Timer resets on every outside frame")
ax.plot(t, robust, color=C[0], lw=2, label=f"Timer with a {GRACE:.0f} s grace period")
ax.axhline(LIMIT, color=INK2, lw=1.2, ls="--")
ax.text(1, LIMIT + 1.5, "dwell limit", color=INK2, fontsize=12, va="bottom")
if alert_r is not None:
    ax.scatter([alert_r], [LIMIT], s=90, color=CRIT, zorder=4)
    ax.annotate("alert fires", xy=(alert_r, LIMIT), xytext=(alert_r + 6, LIMIT + 14), fontsize=12, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=1))
out_t = t[(~ins) & (t >= 10) & (t < 110)]
ax.scatter(out_t, np.full(out_t.size, -4), marker="|", s=60, color=INK2, lw=1, label="frames judged outside")
ax.set_xlim(0, 120); ax.set_ylim(-8, 110)
ax.set_xlabel("Seconds")
ax.set_ylabel("Measured time in zone (s)")
ax.set_title("Boundary flicker keeps resetting a naive dwell timer", loc="left")
ax.legend(loc="upper left", fontsize=12)
save(fig, f"{SLUG}-dwell-flicker.png")
