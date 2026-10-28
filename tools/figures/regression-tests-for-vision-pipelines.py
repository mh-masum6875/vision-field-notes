"""Figures for regression-tests-for-vision-pipelines. A diagram, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, save

SLUG = "regression-tests-for-vision-pipelines"


def box(ax, x, y, w, h, color, fill=0.14):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=1.6))


layers = [
    ("Pre- and post-processing unit tests", "letterbox, colour order, box decoding, NMS", "seconds, every commit", C[0]),
    ("Rule logic tests on synthetic tracks", "zones, dwell time, cooldowns, schedules", "seconds, every commit", C[2]),
    ("Golden-image tests", "fixed images in, boxes out within tolerance", "a minute, every commit", C[6]),
    ("Export parity tests", "PyTorch vs ONNX / TensorRT on the same images", "minutes, every new model", C[3]),
    ("Replay tests on recorded clips", "expected events per clip, event-level scoring", "hours, before release", C[1]),
]
fig, ax = plt.subplots(figsize=(11, 5.8))
ax.set_xlim(0, 11); ax.set_ylim(0, len(layers) * 1.1 + 0.6); ax.axis("off")
for i, (name, what, when, col) in enumerate(layers):
    y = i * 1.1 + 0.2
    inset = (len(layers) - 1 - i) * 0.0 + i * 0.35
    box(ax, inset, y, 7.2 - 2 * inset + 3.0, 0.9, col)
    ax.text(inset + 0.25, y + 0.6, name, fontsize=12.5, weight="bold", va="center")
    ax.text(inset + 0.25, y + 0.26, what, fontsize=11.5, color=INK2, va="center")
    ax.text(10.2 - inset, y + 0.45, when, fontsize=11.5, color=INK2, va="center", ha="right")
ax.text(0, len(layers) * 1.1 + 0.45, "Cheap, fast tests at the bottom; slow, realistic ones at the top",
        fontsize=14, weight="bold", va="center")
save(fig, f"{SLUG}-layers.png")
