"""Figures for spotting-overfitting-in-detection (illustrative, simulated curves)."""
import numpy as np
import style
from style import plt, C, INK, INK2, MUTED, GRID, ACCENT

SLUG = "spotting-overfitting-in-detection"
rng = np.random.default_rng(3)
E = np.arange(1, 101)


def loss_curves():
    train_h = 0.55 + 1.6 * np.exp(-E / 18) + rng.normal(0, 0.012, E.size)
    val_h = 0.70 + 1.5 * np.exp(-E / 20) + rng.normal(0, 0.02, E.size)
    train_o = 0.15 + 1.9 * np.exp(-E / 22) + rng.normal(0, 0.012, E.size)
    val_o = 0.95 + 1.2 * np.exp(-E / 12) + 0.0065 * np.clip(E - 30, 0, None) + rng.normal(0, 0.02, E.size)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
    for ax, tr, va, title in [(axes[0], train_h, val_h, "Healthy: both fall and level off"),
                              (axes[1], train_o, val_o, "Overfitting: validation turns upward")]:
        ax.plot(E, tr, color=C[0], label="Training loss")
        ax.plot(E, va, color=C[1], label="Validation loss")
        ax.set_title(title, fontsize=13)
        ax.set_xlabel("Epoch")
        ax.set_yticklabels([])
        ax.tick_params(axis="y", length=0)
    axes[0].set_ylabel("Loss (illustrative)")
    axes[0].legend(loc="upper right", fontsize=12)
    k = int(np.argmin(np.convolve(val_o, np.ones(7) / 7, mode="same")[5:-5])) + 5
    axes[1].axvline(E[k], color=INK2, lw=1.2, ls="--")
    axes[1].annotate("useful learning\nends about here", xy=(E[k], val_o[k]), xytext=(E[k] + 14, 2.0),
                     fontsize=12, color=INK, arrowprops=dict(arrowstyle="->", color=INK2))
    axes[1].annotate("", xy=(93, train_o[92]), xytext=(93, val_o[92]),
                     arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.5))
    axes[1].text(90, (train_o[92] + val_o[92]) / 2, "the gap keeps\nwidening", ha="right", va="center",
                 fontsize=12, color=INK)
    fig.tight_layout()
    style.save(fig, f"{SLUG}-loss-curves.png")


def best_vs_last():
    base = 0.62 / (1 + np.exp(-(E - 18) / 7))
    drift = -0.0022 * np.clip(E - 55, 0, None)
    m = base + drift + rng.normal(0, 0.012, E.size)
    best = int(np.argmax(m))
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.plot(E, m, color=C[0], label="Validation mAP50-95 per epoch")
    ax.axvspan(E[best], min(E[best] + 30, 100), color=GRID, alpha=0.7, lw=0)
    stop = min(E[best] + 30, 100)
    ax.axvline(stop, color=INK2, lw=1.2, ls="--")
    ax.text(E[best] + 15, 0.05, "patience = 30:\nno new best,\nso early stopping\nends the run here",
            ha="center", fontsize=12, color=INK2)
    ax.plot(E[best], m[best], "o", ms=9, color=ACCENT)
    ax.annotate("best.pt", xy=(E[best], m[best]), xytext=(E[best] - 22, m[best] + 0.05), fontsize=13,
                fontweight="bold", color=INK, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.plot(E[-1], m[-1], "o", ms=9, color=C[1])
    ax.annotate("last.pt if run\nto epoch 100", xy=(E[-1], m[-1]), xytext=(E[-1] - 10, m[-1] - 0.2), fontsize=13,
                fontweight="bold", color=INK, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Validation metric (illustrative)")
    ax.set_yticklabels([])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(0, 0.78)
    ax.set_title("The last epoch is not the best one: keep best.pt")
    style.save(fig, f"{SLUG}-best-vs-last.png")
    print("best epoch", E[best])


if __name__ == "__main__":
    loss_curves()
    best_vs_last()
