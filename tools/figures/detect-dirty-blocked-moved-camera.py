"""Figures for detect-dirty-blocked-moved-camera.

Sharpness values are computed here on two synthetic test scenes (drawn below), not taken from a camera.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, WARN, save

SLUG = "detect-dirty-blocked-moved-camera"
W, H = 640, 360
rng = np.random.default_rng(3)


def busy_scene():
    """Lots of edges: shelves, boxes and signs."""
    im = np.full((H, W), 150, np.uint8)
    for _ in range(140):
        x, y = int(rng.integers(0, W)), int(rng.integers(0, H))
        w, h = int(rng.integers(8, 70)), int(rng.integers(8, 50))
        cv2.rectangle(im, (x, y), (x + w, y + h), int(rng.integers(20, 240)), -1)
    for _ in range(40):
        p1 = (int(rng.integers(0, W)), int(rng.integers(0, H)))
        p2 = (int(rng.integers(0, W)), int(rng.integers(0, H)))
        cv2.line(im, p1, p2, int(rng.integers(0, 255)), 2)
    return im


def plain_scene():
    """Few edges: an empty corridor with smooth lighting."""
    xx, yy = np.meshgrid(np.linspace(0, 1, W), np.linspace(0, 1, H))
    im = (90 + 70 * xx + 30 * yy).astype(np.uint8)
    cv2.rectangle(im, (250, 80), (390, 330), 70, -1)      # doorway
    cv2.line(im, (0, 300), (250, 330), 60, 2)              # floor edge
    cv2.line(im, (390, 330), (W, 300), 60, 2)
    return im


def sharpness(gray):
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def frame(base, blur, noise=2.0):
    im = base.astype(np.float64)
    if blur > 0:
        im = cv2.GaussianBlur(im, (0, 0), blur)
    im = im + rng.normal(0, noise, im.shape)
    return np.clip(im, 0, 255).astype(np.uint8)


sigmas = np.linspace(0, 4, 17)
BUSY, PLAIN = busy_scene(), plain_scene()
scenes = [("Busy scene (shelves, signs)", BUSY, C[0]), ("Plain scene (empty corridor)", PLAIN, C[1])]
vals = {}
for name, base, _ in scenes:
    vals[name] = np.array([np.median([sharpness(frame(base, s)) for _ in range(5)]) for s in sigmas])
    print(name, [float(round(v, 1)) for v in vals[name]])

# 1. Absolute sharpness vs relative-to-baseline sharpness
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
ax = axes[0]
for name, _, c in scenes:
    ax.plot(sigmas, vals[name], color=c, marker="o", ms=4, label=name)
ax.set_yscale("log")
ax.set_xlabel("Gaussian blur applied (sigma, pixels)")
ax.set_ylabel("variance of Laplacian (log scale)")
ax.set_title("Absolute score depends on the scene", loc="left")
busy_blur = vals[scenes[0][0]][np.searchsorted(sigmas, 2.0)]
plain_sharp = vals[scenes[1][0]][0]
ax.annotate(f"plain scene, perfectly sharp: {plain_sharp:.0f}", xy=(0, plain_sharp), xytext=(0.9, 1500),
            fontsize=11, color=INK2, arrowprops=dict(arrowstyle="->", color=INK2))
ax.annotate(f"busy scene, badly blurred: {busy_blur:.0f}", xy=(2.0, busy_blur), xytext=(2.1, 300),
            fontsize=11, color=INK2, arrowprops=dict(arrowstyle="->", color=INK2))


ax = axes[1]
for name, _, c in scenes:
    ax.plot(sigmas, vals[name] / vals[name][0], color=c, marker="o", ms=4, label=name)
ax.axhline(0.5, color=INK2, ls="--", lw=1.2)
ax.text(4, 0.53, "alert below 0.5 x baseline", ha="right", fontsize=11, color=INK2)
ax.set_ylim(0, 1.08)
ax.set_xlabel("Gaussian blur applied (sigma, pixels)")
ax.set_ylabel("score / camera's own baseline")
ax.set_title("Against its own baseline, one threshold catches blur in both", loc="left")
ax.legend(handles=axes[0].get_lines(), loc="lower left", bbox_to_anchor=(0.3, 0.1), fontsize=11)
fig.suptitle("Sharpness computed on two synthetic test scenes, 640 x 360, mild sensor noise",
             fontsize=12.5, color=INK2, y=0.995)
fig.tight_layout()
save(fig, f"{SLUG}-sharpness-baseline.png")

# 2. Noise inflates the score: the same blurred frame with more sensor noise
base = BUSY
noises = [1, 2, 4, 8, 12, 16]
blurred = [np.median([sharpness(frame(base, 2.0, n)) for _ in range(5)]) for n in noises]
sharp_ref = np.median([sharpness(frame(base, 0, 2.0)) for _ in range(5)])
print("noise", list(zip(noises, [float(round(v, 1)) for v in blurred])), "sharp ref", float(round(sharp_ref, 1)))
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.bar([str(n) for n in noises], blurred, color=C[0], alpha=0.85, width=0.6)
ax.axhline(sharp_ref, color=ACCENT, lw=1.6)
ax.text(-0.35, sharp_ref * 1.03, f"same scene, sharp, low noise: {sharp_ref:.0f}", ha="left", va="bottom",
        fontsize=11, color=ACCENT)
ax.axhline(0.5 * sharp_ref, color=INK2, ls="--", lw=1.2)
ax.text(-0.35, 0.5 * sharp_ref * 1.03, "0.5 x baseline", ha="left", va="bottom", fontsize=11, color=INK2)
ax.set_xlabel("sensor noise added (standard deviation, grey levels)")
ax.set_ylabel("variance of Laplacian")
ax.set_title("A blurred frame (sigma 2) scores higher as noise rises, as it does at night", loc="left")
ax.grid(axis="x", visible=False)
save(fig, f"{SLUG}-noise-inflates.png")
