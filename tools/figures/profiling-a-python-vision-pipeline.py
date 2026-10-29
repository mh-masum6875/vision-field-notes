"""Figures for profiling-a-python-vision-pipeline.

Real timings, measured by this script on whatever machine runs it, of common pre-processing steps on one
synthetic 1080p frame. No model inference is included. The machine is printed and shown in the figure.
"""
import platform, time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from style import C, INK, INK2, MUTED, GRID, save

SLUG = "profiling-a-python-vision-pipeline"
rng = np.random.default_rng(0)
frame = rng.integers(0, 255, (1080, 1920, 3), np.uint8)
frame = cv2.GaussianBlur(frame, (0, 0), 3)          # smoother, more camera-like content for JPEG
jpg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])[1]


def letterbox(img, s=640):
    h, w = img.shape[:2]
    r = s / max(h, w)
    nh, nw = int(round(h * r)), int(round(w * r))
    out = np.full((s, s, 3), 114, np.uint8)
    out[:nh, :nw] = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
    return out


small = letterbox(frame)
steps = [
    ("decode 1080p JPEG", lambda: cv2.imdecode(jpg, cv2.IMREAD_COLOR)),
    ("copy 1080p frame", lambda: frame.copy()),
    ("letterbox to 640 (cv2.resize)", lambda: letterbox(frame)),
    ("normalise in NumPy (float64)", lambda: (small[:, :, ::-1].transpose(2, 0, 1)[None] / 255.0)),
    ("normalise in NumPy (float32)", lambda: (small[:, :, ::-1].transpose(2, 0, 1)[None].astype(np.float32) * (1 / 255))),
    ("cv2.dnn.blobFromImage", lambda: cv2.dnn.blobFromImage(small, 1 / 255, swapRB=True)),
    ("BGR to RGB on 1080p, then resize", lambda: cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (640, 360))),
    ("resize first, then BGR to RGB", lambda: cv2.cvtColor(cv2.resize(frame, (640, 360)), cv2.COLOR_BGR2RGB)),
]
cv2.setNumThreads(1)
res = []
for name, fn in steps:
    for _ in range(20):
        fn()
    t = []
    for _ in range(200):
        t0 = time.perf_counter(); fn(); t.append((time.perf_counter() - t0) * 1000)
    res.append((name, float(np.median(t))))
    print(f"{name:40s} {np.median(t):7.2f} ms")
cpu = platform.processor() or platform.machine()
print("machine:", cpu)

fig, ax = plt.subplots(figsize=(10.5, 4.8))
y = np.arange(len(res))
cols = [C[0]] * 6 + [C[1], C[2]]
ax.barh(y, [v for _, v in res], color=cols, alpha=0.85, height=0.6)
for i, (_, v) in enumerate(res):
    ax.text(v * 1.03 + 0.05, i, f"{v:.2f} ms", va="center", fontsize=10.5, color=INK)
ax.set_yticks(y); ax.set_yticklabels([n for n, _ in res])
ax.invert_yaxis()
ax.set_xlabel("median time per call (ms), single OpenCV thread")
ax.grid(axis="y", visible=False)
ax.set_title("Pre-processing steps on one 1080p frame, measured on a laptop CPU", loc="left")
ax.text(1.0, -0.22, f"Measured on: {cpu}; OpenCV {cv2.__version__}, NumPy {np.__version__}; your numbers will differ.",
        transform=ax.transAxes, ha="right", fontsize=9.5, color=INK2)
save(fig, f"{SLUG}-preprocess-timings.png")
