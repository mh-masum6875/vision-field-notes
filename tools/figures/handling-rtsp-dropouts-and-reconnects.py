"""Figures for handling-rtsp-dropouts-and-reconnects."""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from style import C, ACCENT, INK, INK2, MUTED, GRID, CRIT, save
import detect

SLUG = "handling-rtsp-dropouts-and-reconnects"

# 1. Reconnect attempts of 20 readers after a shared outage (illustrative simulation)
rng = np.random.default_rng(7)
N, OUTAGE_END, T_MAX = 20, 40.0, 75.0


def attempts(jitter):
    out = []
    for _ in range(N):
        t, d, ts = 0.0, 1.0, []
        while t < T_MAX:
            wait = d * rng.uniform(0.5, 1.5) if jitter else d
            t += wait
            ts.append(t)
            if t >= OUTAGE_END:      # first attempt after recovery succeeds
                break
            d = min(d * 2, 30.0)
        out.append(ts)
    return out


fig, axes = plt.subplots(2, 1, figsize=(10, 5.6), sharex=True)
for ax, jit, title in [(axes[0], False, "Backoff without jitter: every reader retries at the same instants"),
                       (axes[1], True, "Backoff with jitter: retries spread out")]:
    ax.axvspan(0, OUTAGE_END, color=GRID, alpha=0.6, lw=0)
    for i, ts in enumerate(attempts(jit)):
        ts = np.array(ts)
        fail, ok = ts[ts < OUTAGE_END], ts[ts >= OUTAGE_END]
        ax.scatter(fail, np.full(len(fail), i), s=22, color=C[1], zorder=3,
                   label="failed attempt" if i == 0 else None)
        ax.scatter(ok, np.full(len(ok), i), s=22, color=C[0], marker="s", zorder=3,
                   label="reconnected" if i == 0 else None)
    ax.set_ylim(-1, N + 2.2); ax.set_yticks([]); ax.grid(axis="y", visible=False)
    ax.set_ylabel(f"{N} readers")
    ax.set_title(title, loc="left", fontsize=13)
    ax.text(OUTAGE_END / 2, N + 1.9, "switch down", ha="center", va="top", fontsize=12, color=INK2)
axes[1].set_xlabel("Seconds since the outage began")
axes[1].set_xlim(0, T_MAX)
fig.tight_layout()
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="upper center", ncol=2, fontsize=12, bbox_to_anchor=(0.5, 0.0))
save(fig, f"{SLUG}-backoff-jitter.png")


# 2. Frame-change score on real footage, with a freeze injected for the demo
cap = cv2.VideoCapture(f"{detect.BENCH}/samples/safety.mp4")
fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
frames = []
while True:
    ok, im = cap.read()
    if not ok:
        break
    frames.append(im)
F0, F1 = 100, 220                       # simulated encoder hang: repeat frame F0-1
frames = frames[:F0] + [frames[F0 - 1]] * (F1 - F0) + frames[F1:]


def small(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return cv2.resize(g, (64, 36), interpolation=cv2.INTER_AREA).astype(np.float32)


score = np.array([np.mean(np.abs(small(a) - small(b))) for a, b in zip(frames[1:], frames[:-1])])
t = np.arange(1, len(frames)) / fps
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.axvspan(F0 / fps, F1 / fps, color=CRIT, alpha=0.08, lw=0)
ax.plot(t, score, color=C[0], lw=2, label="Mean absolute difference to previous frame")
ax.axhline(0.005, color=INK2, lw=1.2, ls="--", label="Example 'frozen' threshold")
ax.set_yscale("symlog", linthresh=0.01)
ax.set_ylim(-0.002, 40)
ax.set_yticks([0, 0.01, 0.1, 1])
ax.set_yticklabels(["0", "0.01", "0.1", "1"])
ax.yaxis.set_minor_locator(plt.NullLocator())
ax.set_xlim(0, t[-1])
ax.set_xlabel("Seconds into the clip")
ax.set_ylabel("Frame-change score (64x36 grey)")
ax.set_title("A frozen picture drops to exactly zero; a quiet live scene does not", loc="left")
ax.text((F0 + F1) / 2 / fps, 0.08, "simulated freeze:\nsame frame repeated", ha="center", va="center",
        fontsize=12, color=CRIT)
ax.legend(loc="upper right", fontsize=12)
save(fig, f"{SLUG}-frozen-check.png")
