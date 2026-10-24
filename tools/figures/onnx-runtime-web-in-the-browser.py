"""Figures for onnx-runtime-web-in-the-browser (pure diagrams)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import style
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, WARN, CRIT, save

SLUG = "onnx-runtime-web-in-the-browser"


def box(ax, x, y, w, h, text, fc="#ffffff", ec=INK2, size=11.5, weight="normal", family=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight,
            linespacing=1.25, family=family)


def arrow(ax, x1, y1, x2, y2, label=None, lx=0, ly=0, color=INK2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16, shrinkA=0, shrinkB=0))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=11, weight="bold", color=INK2,
                ha="center", va="center")


# 1. Data flow: files come down once, images never go up
fig, ax = plt.subplots(figsize=(10.5, 5.8))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.8)
ax.axis("off")
box(ax, 0.1, 4.0, 3.4, 1.3, "Static web host\nHTML + JS, WASM runtime,\nmodel.onnx", fc="#f7f6f2")
arrow(ax, 1.8, 4.0, 1.8, 3.15)
ax.text(1.95, 3.58, "downloaded once,\nthen cached", fontsize=11, color=INK2, va="center")
ax.add_patch(FancyBboxPatch((0.1, 0.15), 10.3, 2.85, boxstyle="round,pad=0.02,rounding_size=0.15",
                            fc="#f3f8fd", ec=C[0], lw=1.8))
ax.text(0.3, 2.65, "Visitor's browser, on their own device", fontsize=12.5, weight="bold", color=C[0])
steps = ["Camera or\nimage file", "Pre-process\non a canvas", "ONNX Runtime Web\n(WebGPU or WASM)",
         "Decode +\nNMS in JS", "Draw boxes\non a canvas"]
ws = [1.55, 1.65, 2.6, 1.5, 1.6]
x = 0.3
for i, (s, w) in enumerate(zip(steps, ws)):
    box(ax, x, 0.95, w, 1.2, s, fc="#ffffff", ec=C[0] if i != 2 else ACCENT,
        weight="bold" if i == 2 else "normal", size=11)
    if i < len(steps) - 1:
        arrow(ax, x + w, 1.55, x + w + 0.25, 1.55)
    x += w + 0.25
ax.text(5.25, 0.45, "The image is processed here and does not need to be uploaded", ha="center",
        fontsize=11.5, color=GOOD, weight="bold")
box(ax, 5.9, 4.1, 4.5, 1.2, "No inference server.\nStill say so only if nothing else\n(analytics, error reports) sends data.",
    fc="#ffffff", ec=MUTED, size=11)
ax.set_title("In-browser detection: files come down once, images stay on the device", loc="left")
save(fig, f"{SLUG}-data-flow.png")

# 2. Execution provider fallback
fig, ax = plt.subplots(figsize=(10.5, 5.4))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.4)
ax.axis("off")
box(ax, 0.1, 3.9, 3.3, 1.0, 'executionProviders:\n["webgpu", "wasm"]', fc="#f7f6f2", family="DejaVu Sans Mono", size=11)
arrow(ax, 3.4, 4.4, 3.9, 4.4)
box(ax, 3.9, 3.9, 2.8, 1.0, "WebGPU available\nin this browser?", ec=ACCENT, weight="bold")
arrow(ax, 6.7, 4.4, 7.3, 4.4, "yes", ly=0.22)
box(ax, 7.3, 3.9, 3.1, 1.0, "GPU path\n(often fastest)", fc="#e7f5e7", ec=GOOD)
arrow(ax, 5.3, 3.9, 5.3, 3.1, "no", lx=0.3)
box(ax, 3.9, 2.1, 2.8, 1.0, "WASM on the CPU.\nPage cross-origin\nisolated?", ec=ACCENT, weight="bold", size=11)
arrow(ax, 6.7, 2.6, 7.3, 2.6, "yes", ly=0.22)
box(ax, 7.3, 2.1, 3.1, 1.0, "Multi-threaded WASM\n(SharedArrayBuffer)", fc="#e7f5e7", ec=GOOD)
arrow(ax, 5.3, 2.1, 5.3, 1.3, "no", lx=0.3)
box(ax, 3.9, 0.3, 2.8, 1.0, "Single-threaded\nWASM (slowest)", fc="#fdf0e9", ec=C[1])
ax.text(0.1, 2.6, "Cross-origin isolation\nneeds COOP and COEP\nresponse headers.\nSome static hosts\ncannot set them.",
        fontsize=11, color=INK2, va="center")
ax.set_title("Which backend you get depends on the visitor's browser and your host's headers", loc="left")
save(fig, f"{SLUG}-provider-fallback.png")
