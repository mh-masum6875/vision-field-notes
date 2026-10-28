"""Figures for evaluate-video-analytics-by-events.

A constructed example: the ground-truth events and the per-frame detections are generated below,
then frame-level and event-level scores are computed from them. Not footage, not a real system.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from style import C, INK, INK2, MUTED, GRID, GOOD, CRIT, save

SLUG = "evaluate-video-analytics-by-events"
FPS, T = 5, 120
n = FPS * T
rng = np.random.default_rng(2)
gt = np.zeros(n, bool)
events = [(8, 20), (34, 38), (52, 75), (88, 90), (100, 112)]
for a, b in events:
    gt[a * FPS:b * FPS] = True
det = np.zeros(n, bool)
for a, b in events:
    if (a, b) == (88, 90):
        continue                                   # a short event the system misses entirely
    idx = np.arange(a * FPS, b * FPS)
    det[idx] = rng.random(len(idx)) < 0.55          # flickering detections inside the event
det[(44 * FPS):(44 * FPS + 4)] = True               # a brief false blip
det[(80 * FPS):(83 * FPS)] = True                   # a persistent false object


def alerts(d, need=5, window=8, cooldown=10):
    """N of M rule, then a cooldown. Returns alert times in seconds."""
    out, last = [], -1e9
    for i in range(window, n):
        if d[i - window:i].sum() >= need and i / FPS - last > cooldown:
            out.append(i / FPS); last = i / FPS
    return out


al = alerts(det)
tol = 3.0
matched_events = [any(a - 0 <= t <= b + tol for t in al) for a, b in events]
tp_alerts = [t for t in al if any(a <= t <= b + tol for a, b in events)]
fp_alerts = [t for t in al if t not in tp_alerts]
frame_tp = (det & gt).sum(); frame_fp = (det & ~gt).sum(); frame_fn = (~det & gt).sum()
fr_p, fr_r = frame_tp / (frame_tp + frame_fp), frame_tp / (frame_tp + frame_fn)
ev_r = sum(matched_events) / len(events)
print(f"frame precision {fr_p:.2f} recall {fr_r:.2f}; alerts {len(al)} tp {len(tp_alerts)} fp {len(fp_alerts)}; "
      f"event recall {ev_r:.2f} ({sum(matched_events)}/{len(events)})")

fig, ax = plt.subplots(figsize=(11.5, 4.4))
ax.set_xlim(0, T); ax.set_ylim(-0.3, 3.4); ax.set_yticks([0.5, 1.5, 2.6])
ax.set_yticklabels(["alerts", "per-frame\ndetections", "true events"])
ax.grid(axis="y", visible=False)
for (a, b), m in zip(events, matched_events):
    ax.add_patch(Rectangle((a, 2.3), b - a, 0.6, fc=GOOD if m else CRIT, alpha=0.35, ec="none"))
t = np.arange(n) / FPS
ax.vlines(t[det], 1.2, 1.8, color=C[0], lw=0.8)
for x in tp_alerts:
    ax.plot([x], [0.5], "v", color=GOOD, ms=11)
for x in fp_alerts:
    ax.plot([x], [0.5], "v", color=CRIT, ms=11)
ax.set_xlabel("seconds")
ax.set_title(f"Frames say recall {fr_r:.2f}; events say {sum(matched_events)} of {len(events)} found, "
             f"{len(fp_alerts)} false alert (constructed example)", loc="left", fontsize=13)
ax.text(T, 3.25, "green = found   red = missed or false", ha="right", fontsize=11, color=INK2)
save(fig, f"{SLUG}-timeline.png")
