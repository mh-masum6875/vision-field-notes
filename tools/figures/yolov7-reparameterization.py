"""Figures for yolov7-reparameterization: training vs inference block, and kernel merge arithmetic (verified)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import style
from style import C, ACCENT, INK, INK2, MUTED, GRID

SLUG = "yolov7-reparameterization"


def rbox(ax, x, y, w, h, text, color, fs=12.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=color + "1f", ec=color, lw=1.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK, linespacing=1.25,
            weight="bold" if bold else "normal")


def arr(ax, p1, p2, color=INK2, lw=1.6, conn=None):
    props = dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=15)
    if conn:
        props["connectionstyle"] = conn
    ax.annotate("", xy=p2, xytext=p1, arrowprops=props)


def fig_blocks():
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    ax.axis("off")
    # training block (left)
    ax.text(22, 57, "Training time: three branches", ha="center", fontsize=14, weight="bold", color=INK)
    rbox(ax, 15, 46, 14, 6, "input", MUTED)
    bx = [0, 15.5, 31]
    labels = ["3x3 conv\n+ BN", "1x1 conv\n+ BN", "identity\n+ BN"]
    for x, l, c in zip(bx, labels, [C[0], C[1], C[2]]):
        rbox(ax, x, 26, 13, 10, l, c)
        arr(ax, (22, 45.6), (x + 6.5, 36.4))
        arr(ax, (x + 6.5, 25.6), (22, 18.6))
    ax.add_patch(plt.Circle((22, 16.5), 2.1, fc="white", ec=INK2, lw=1.6))
    ax.text(22, 16.5, "+", ha="center", va="center", fontsize=16, color=INK)
    rbox(ax, 15, 3, 14, 6.5, "activation", MUTED)
    arr(ax, (22, 14.2), (22, 9.9))
    # conversion arrow
    arr(ax, (47, 30), (60, 30), color=ACCENT, lw=2.4)
    ax.text(53.5, 34.5, "convert once,\nafter training", ha="center", va="bottom", fontsize=12, color=INK, weight="bold")
    ax.text(53.5, 25.5, "1. fold BN into\neach conv\n2. add the kernels\nand biases", ha="center", va="top", fontsize=11.5, color=INK2)
    # inference block (right)
    ax.text(83, 57, "Inference: one conv", ha="center", fontsize=14, weight="bold", color=INK)
    rbox(ax, 76, 46, 14, 6, "input", MUTED)
    rbox(ax, 72, 26, 22, 10, "one 3x3 conv\n(merged weights)", ACCENT)
    rbox(ax, 76, 3, 14, 6.5, "activation", MUTED)
    arr(ax, (83, 45.6), (83, 36.4))
    arr(ax, (83, 25.6), (83, 9.9))
    ax.text(83, 18, "same output,\nfewer operations", ha="center", va="center", fontsize=11.5, color=INK2,
            bbox=dict(fc="white", ec="none", pad=1))
    ax.set_xlim(-1, 101); ax.set_ylim(1, 61)
    style.save(fig, f"{SLUG}-train-vs-inference.png")


def conv2d_same(x, k):
    p = np.pad(x, 1)
    out = np.zeros_like(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            out[i, j] = (p[i:i + 3, j:j + 3] * k).sum()
    return out


def fig_kernels():
    # one input and one output channel, BN already folded; values are illustrative
    k3 = np.array([[0.1, -0.2, 0.0], [0.3, 0.5, -0.1], [0.0, 0.2, 0.1]])
    k1 = np.zeros((3, 3)); k1[1, 1] = 0.4      # the 1x1 kernel, zero-padded to 3x3
    kid = np.zeros((3, 3)); kid[1, 1] = 1.0    # identity as a 3x3 kernel
    merged = k3 + k1 + kid
    # verify: sum of branch outputs equals merged conv output
    x = np.random.default_rng(0).normal(size=(8, 8))
    branches = conv2d_same(x, k3) + 0.4 * x + x
    diff = np.abs(branches - conv2d_same(x, merged)).max()
    print("max abs difference between three-branch and merged output:", diff)
    assert diff < 1e-9
    kernels = [(k3, "3x3 branch"), (k1, "1x1 branch,\npadded to 3x3"), (kid, "identity branch\nas a 3x3 kernel"), (merged, "merged kernel")]
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.6))
    vmax = 1.6
    for idx, (ax, (k, title)) in enumerate(zip(axes, kernels)):
        for i in range(3):
            for j in range(3):
                v = k[i, j]
                fc = ACCENT if idx == 3 else C[0]
                alpha = min(abs(v) / vmax, 1) * 0.85 + 0.05 if v != 0 else 0
                ax.add_patch(Rectangle((j, i), 1, 1, fc=fc, alpha=alpha, ec="none"))
                ax.add_patch(Rectangle((j, i), 1, 1, fill=False, ec=GRID, lw=1.2))
                ax.text(j + 0.5, i + 0.5, f"{v:g}", ha="center", va="center", fontsize=13,
                        color="white" if abs(v) > 1.2 else INK)
        ax.set_xlim(-0.05, 3.05); ax.set_ylim(3.05, -0.05); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(title, fontsize=12.5, color=INK, weight="normal")
    for a, sym in zip(axes[:3], ["+", "+", "="]):
        a.text(3.55, 1.5, sym, ha="center", va="center", fontsize=24, color=INK2, transform=a.transData, clip_on=False)
    fig.suptitle("Three kernels add up to one, so three branches become one convolution", fontsize=14, weight="bold", y=0.99)
    fig.tight_layout(w_pad=3.5)
    style.save(fig, f"{SLUG}-kernel-merge.png")


if __name__ == "__main__":
    fig_blocks()
    fig_kernels()
