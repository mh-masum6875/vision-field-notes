"""Figures for deduplicating-video-frames-before-labelling.

A synthetic 60-second clip at 5 fps is generated below: a static scene with sensor noise, and a moving
block during two short periods. The keep-if-different rule is then applied and the result plotted.
Everything here is computed; nothing is camera footage.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, WARN, save

SLUG = "deduplicating-video-frames-before-labelling"
rng = np.random.default_rng(1)
FPS, T = 5, 60
H, W = 180, 320
base = np.full((H, W), 120, np.float32)
cv2.rectangle(base, (20, 120), (300, 170), 80, -1)
cv2.rectangle(base, (200, 20), (280, 100), 160, -1)


def frame(i):
    t = i / FPS
    im = base.copy()
    for a, b in [(12, 20), (38, 47)]:
        if a <= t < b:
            x = int(10 + (t - a) / (b - a) * 280)
            cv2.rectangle(im, (x, 60), (x + 25, 130), 30, -1)
    return np.clip(im + rng.normal(0, 3, im.shape), 0, 255).astype(np.uint8)


def small(im):
    return cv2.resize(im, (64, 36), interpolation=cv2.INTER_AREA).astype(np.float32)


frames = [frame(i) for i in range(FPS * T)]
THRESH = 2.0
kept, last, diffs = [], None, []
for i, f in enumerate(frames):
    s = small(f)
    d = 999.0 if last is None else float(np.abs(s - last).mean())
    diffs.append(min(d, 12))
    if d > THRESH:
        kept.append(i); last = s
every_n = list(range(0, len(frames), FPS * 2))
print(f"frames {len(frames)}, kept by change {len(kept)}, kept by every 2 s {len(every_n)}")
print("kept by change during motion:", sum(1 for k in kept if 12 * FPS <= k < 20 * FPS or 38 * FPS <= k < 47 * FPS))

t = np.arange(len(frames)) / FPS
fig, ax = plt.subplots(figsize=(11, 4.4))
for a, b in [(12, 20), (38, 47)]:
    ax.axvspan(a, b, color=WARN, alpha=0.18, lw=0)
ax.plot(t, diffs, color=C[0], lw=1.2, label="difference from last kept frame")
ax.axhline(THRESH, color=INK2, ls="--", lw=1.1)
ax.text(59.5, THRESH + 0.3, "keep threshold", ha="right", fontsize=10.5, color=INK2)
ax.vlines(np.array(kept) / FPS, -1.6, -0.6, color=C[1], lw=1.2)
ax.vlines(np.array(every_n) / FPS, -2.9, -1.9, color=MUTED, lw=1.2)
ax.text(0.3, -1.1, f"kept by change: {len(kept)}", fontsize=10.5, color=C[1], va="center",
        bbox=dict(fc="white", ec="none", pad=1))
ax.text(0.3, -2.4, f"every 2 s: {len(every_n)}", fontsize=10.5, color=INK2, va="center",
        bbox=dict(fc="white", ec="none", pad=1))
ax.set_ylim(-3.2, 12.5); ax.set_xlim(0, 60)
ax.set_yticks([0, 4, 8, 12])
ax.set_xlabel("seconds (yellow = something moving)")
ax.set_ylabel("mean abs difference")
ax.set_title("A synthetic 60 s clip: change-based selection keeps the moving periods, skips the static ones",
             loc="left", fontsize=13)
save(fig, f"{SLUG}-selection.png")
