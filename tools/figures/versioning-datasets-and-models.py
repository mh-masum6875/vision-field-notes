"""Figures for versioning-datasets-and-models. A diagram, no data."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, INK, INK2, MUTED, save

SLUG = "versioning-datasets-and-models"


def box(ax, x, y, w, h, color, title, lines):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=color + "24", ec=color, lw=1.6))
    ax.text(x + 0.2, y + h - 0.35, title, fontsize=12.5, weight="bold", va="center")
    ax.text(x + 0.2, y + h - 0.75, lines, fontsize=10.5, color=INK2, va="top", family="DejaVu Sans Mono",
            linespacing=1.45)


def arrow(ax, a, b):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4))


fig, ax = plt.subplots(figsize=(12, 4.6))
ax.set_xlim(0, 12.4); ax.set_ylim(0, 4.6); ax.axis("off")
H = 3.2
box(ax, 0.1, 0.4, 2.9, H, C[0], "Dataset version", "dataset: ppe-2026-11-02\nfiles: manifest.csv\n  (path, sha256)\nlabels: v14\nsplits: by camera\nguide: v3")
box(ax, 3.3, 0.4, 2.9, H, C[6], "Training run", "run: 0412\ncode: git a1b2c3d\ndataset: ppe-2026-11-02\nconfig: train.yaml\nseed: 0\nenv: lockfile")
box(ax, 6.5, 0.4, 2.7, H, C[2], "Model", "model: ppe-1.8.0\nfrom run: 0412\nweights: sha256\nexport: onnx fp16\nmetrics: report.json")
box(ax, 9.5, 0.4, 2.8, H, C[1], "Deployment", "site: warehouse-2\ncameras: 3, 7, 9\nmodel: ppe-1.8.0\nthresholds: v6\nsince: 2026-11-05")
for x in (3.0, 6.2, 9.2):
    arrow(ax, (x, 2.0), (x + 0.3, 2.0))
ax.text(0.1, 4.35, "Every deployed model should trace back to exact data and code", fontsize=14,
        weight="bold", va="center")
save(fig, f"{SLUG}-lineage.png")
