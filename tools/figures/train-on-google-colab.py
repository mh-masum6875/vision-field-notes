"""Figures for train-on-google-colab.md"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from style import C, ACCENT, INK, INK2, MUTED, GRID, GOOD, CRIT, save

SLUG = "train-on-google-colab"


def box(ax, x, y, w, h, text, color, fs=12, weight="normal", fill=0.12, ls="-", lw=1.6, ha="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.15",
                                fc=color + "%02x" % int(fill * 255), ec=color, lw=lw, ls=ls))
    tx = x + w / 2 if ha == "center" else x + 0.2
    ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=fs, color=INK, weight=weight, linespacing=1.4)


def arrow(ax, p1, p2, color=INK2, text=None, toff=(0, 0.25), rad=0.0):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8,
                                                      mutation_scale=16, connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((p1[0] + p2[0]) / 2 + toff[0], (p1[1] + p2[1]) / 2 + toff[1], text, ha="center",
                va="bottom", fontsize=11.5, color=INK2)


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(10, 10 * h / w))
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    return fig, ax


# 1. What lives where: runtime disk vs Drive
fig, ax = canvas(12, 6.4)
ax.text(0.1, 6.15, "Only what is on Drive survives the end of a session", fontsize=14, weight="bold", va="top")
# runtime area
box(ax, 0.2, 0.9, 5.0, 4.5, "", CRIT, fill=0.05, ls="--")
ax.text(2.7, 5.05, "Colab runtime (local disk)", ha="center", fontsize=13, weight="bold")
ax.text(2.7, 4.65, "deleted when the session ends", ha="center", fontsize=11.5, color=CRIT)
box(ax, 0.5, 3.2, 4.4, 0.95, "/content/dataset/\n(unzipped images + data.yaml)", C[0])
box(ax, 0.5, 1.25, 4.4, 1.2, "Training process\nproject=\".../MyDrive/runs\"", C[0])
# drive area
box(ax, 7.4, 0.9, 4.4, 4.5, "", GOOD, fill=0.05)
ax.text(9.6, 5.05, "Google Drive", ha="center", fontsize=13, weight="bold")
ax.text(9.6, 4.65, "persists between sessions", ha="center", fontsize=11.5, color="#087a08")
box(ax, 7.7, 3.2, 3.8, 0.95, "dataset.zip  (one file)", C[2])
box(ax, 7.7, 1.25, 3.8, 1.2, "runs/exp1/weights/\nlast.pt   best.pt", C[2])
arrow(ax, (7.7, 3.67), (4.9, 3.67), text="copy + unzip\nat start", toff=(0, 0.1))
arrow(ax, (4.9, 1.85), (7.7, 1.85), text="saves\ncheckpoints", toff=(0, 0.1))
arrow(ax, (2.7, 3.2), (2.7, 2.45), text="")
ax.text(2.85, 2.8, "fast local reads", fontsize=11, color=INK2, va="center")
ax.text(6.0, 0.35, "A new session repeats the top step, then resumes from last.pt.",
        ha="center", fontsize=12, color=INK2)
save(fig, f"{SLUG}-storage.png")

# 2. Resumable training across sessions (illustrative)
fig, ax = plt.subplots(figsize=(10, 3.9))
ax.grid(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_visible(False)
rows = {"Saving to Drive,\nresume=True": 1.0, "Local disk only": 0.0}
# sessions: (start_hour, end_hour)
sessions = [(0, 4.2), (5.0, 9.2), (10.0, 12.6)]
epochs_per_hour = 9
done = 0
for i, (a, b) in enumerate(sessions):
    e0 = done + 1
    done = 100 if i == len(sessions) - 1 else done + int((b - a) * epochs_per_hour)
    ax.barh(1.0, b - a, left=a, height=0.45, color=C[0], alpha=0.85)
    ax.text((a + b) / 2, 1.0, f"epochs {e0}-{done}", ha="center", va="center", color="white", fontsize=11.5, weight="bold")
    if i < len(sessions) - 1:
        ax.annotate("", xy=(sessions[i + 1][0], 1.0), xytext=(b, 1.0),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.5, mutation_scale=14))
done = 0
for i, (a, b) in enumerate(sessions[:2]):
    ax.barh(0.0, b - a, left=a, height=0.45, color=MUTED, alpha=0.6)
    ax.text((a + b) / 2, 0.0, f"epochs 1-{int((b - a) * epochs_per_hour)}", ha="center", va="center", color=INK, fontsize=11.5)
for a, b in sessions[:2]:
    ax.plot([b, b], [-0.32, 1.32], color=CRIT, lw=1.2, ls=":")
    ax.text(b, 1.38, "session ends", ha="center", fontsize=11, color=CRIT)
ax.text(9.6, 0.0, "weights lost, start over", va="center", fontsize=11.5, color=CRIT)
ax.set_yticks(list(rows.values()))
ax.set_yticklabels(list(rows.keys()), fontsize=12, color=INK)
ax.tick_params(axis="y", length=0)
ax.set_xlim(0, 13)
ax.set_ylim(-0.45, 1.6)
ax.set_xlabel("Time (illustrative)")
ax.set_xticks([])
ax.set_title("A 100-epoch run finishes across three sessions only if checkpoints survive", loc="left", pad=22)
save(fig, f"{SLUG}-resume.png")
