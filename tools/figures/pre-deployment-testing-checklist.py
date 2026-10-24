"""Figures for pre-deployment-testing-checklist.md"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, CRIT, WARN, OUT, save
import detect

SLUG = "pre-deployment-testing-checklist"


def draw(img, dets, scale=1.0, fs=0.6):
    """Boxes with labels kept inside the frame."""
    im = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC) if scale != 1 else img.copy()
    H, W = im.shape[:2]
    col = (92, 107, 11)
    for x1, y1, x2, y2, s, n in dets:
        x1, y1, x2, y2 = [int(round(v * scale)) for v in (x1, y1, x2, y2)]
        cv2.rectangle(im, (x1, y1), (x2, y2), col, 2)
        t = f"{n} {s:.2f}"
        (tw, th), _ = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, fs, 1)
        lx = min(max(x1, 0), W - tw - 6)
        ly = y1 if y1 - th - 8 >= 0 else y1 + th + 8
        cv2.rectangle(im, (lx, ly - th - 8), (lx + tw + 6, ly), col, -1)
        cv2.putText(im, t, (lx + 3, ly - 5), cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 255), 1, cv2.LINE_AA)
    return im


def box(ax, x, y, w, h, color, fill=0.12, lw=1.6, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw, ls=ls))


def arrow(ax, p1, p2, color=INK2, rad=0.0):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8, mutation_scale=16,
                                                      connectionstyle=f"arc3,rad={rad}"))


# 1. A pretrained model on an overhead camera (real detections)
fig, axes = plt.subplots(1, 2, figsize=(12, 3.75))
plt.subplots_adjust(wspace=0.03)
for ax, t in zip(axes, (0.26, 0.74)):
    img = detect.frame("traffic", t)
    d = detect.detect(img)
    print(t, [(n, round(s, 2)) for *_, s, n in d])
    ax.imshow(cv2.cvtColor(draw(img, d, scale=1.5, fs=0.85), cv2.COLOR_BGR2RGB))
    ax.axis("off")
axes[0].set_title("Overhead car labelled \"cell phone\"", loc="left", fontsize=13, weight="bold")
axes[1].set_title("Red car labelled \"bus\"", loc="left", fontsize=13, weight="bold")
fig.savefig(OUT / f"{SLUG}-overhead-camera.jpg", dpi=130, bbox_inches="tight", pad_inches=0.1,
            pil_kwargs={"quality": 85})
plt.close(fig)

# 2. Staged rollout with a tested rollback
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.set_xlim(0, 12.4); ax.set_ylim(0, 5.3); ax.axis("off")
ax.text(0.05, 5.25, "Go live in steps, with a way back at every step", fontsize=14, weight="bold", va="top")
stages = [
    ("Offline tests", "held-out footage,\nedge cases, soak,\nfailure drills", C[0]),
    ("Shadow mode", "runs and logs,\nno real alerts", C[6]),
    ("One camera live", "real alerts,\nclose monitoring", C[1]),
    ("Wider rollout", "more cameras\nand sites", C[2]),
]
xs = [0.1, 3.25, 6.4, 9.55]
for (title, sub, col), x in zip(stages, xs):
    box(ax, x, 2.1, 2.75, 2.3, col)
    ax.text(x + 1.375, 3.95, title, ha="center", fontsize=13, weight="bold")
    ax.text(x + 1.375, 3.0, sub, ha="center", va="center", fontsize=12, color=INK2, linespacing=1.35)
for x in xs[:-1]:
    arrow(ax, (x + 2.8, 3.25), (x + 3.2, 3.25))
box(ax, 3.25, 1.2, 9.05, 0.65, ACCENT, fill=0.08)
ax.text(7.775, 1.525, "Monitor: counts per camera, confidence, uptime, frame rate",
        ha="center", va="center", fontsize=12)
ax.plot([10.9, 1.475], [0.7, 0.7], color=CRIT, lw=1.8)
ax.annotate("", xy=(1.475, 2.08), xytext=(1.475, 0.7),
            arrowprops=dict(arrowstyle="-|>", color=CRIT, lw=1.8, mutation_scale=16))
ax.plot([10.9, 10.9], [0.7, 1.2], color=CRIT, lw=1.8)
ax.text(6.2, 0.3, "Rollback: previous model + config, tested before launch", ha="center", va="center",
        fontsize=12, color=CRIT)
save(fig, f"{SLUG}-rollout.png")

# 3. Monitoring catches a moved camera (illustrative)
rng = np.random.default_rng(7)
hours = np.arange(0, 24 * 7)
hod = hours % 24
base = 4 + 26 * np.exp(-((hod - 13) / 4.2) ** 2)
counts = rng.poisson(base).astype(float)
moved = hours >= 24 * 4 + 10
counts[moved] = rng.poisson(base[moved] * 0.25)
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.plot(hours, counts, color=C[0], lw=1.6)
ax.axvline(24 * 4 + 10, color=CRIT, lw=1.4, ls="--")
ax.text(24 * 4 + 12, counts.max() * 0.95, "camera knocked\nout of position", color=INK, fontsize=12, va="top")
ax.set_xticks(np.arange(0, 24 * 7 + 1, 24))
ax.set_xticklabels([f"day {i + 1}" for i in range(7)] + [""])
for lbl in ax.get_xticklabels():
    lbl.set_horizontalalignment("left")
ax.set_xlim(0, 24 * 7)
ax.set_ylabel("Detections per hour (illustrative)")
ax.set_title("No error is raised, but the daily pattern collapses", loc="left")
save(fig, f"{SLUG}-monitoring.png")
