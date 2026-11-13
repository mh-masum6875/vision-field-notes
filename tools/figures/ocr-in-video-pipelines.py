"""Figures for ocr-in-video-pipelines.

Figure 1 is a simulation, not measurements. Each plate gets its own per-character
difficulty, so some characters are hard in every frame of that pass: a dirty
digit or a bad angle reads the same way each time. Those are the ones voting
cannot rescue, which is why the curves flatten below 100% instead of reaching it.
It shows the shape of the gain, not a read rate you should expect.
"""
import numpy as np
import matplotlib.pyplot as plt

import style
from style import C, INK, INK2, GRID, GOOD, CRIT, save

SLUG = "ocr-in-video-pipelines"

ALPHABET = 36          # A-Z and 0-9
PLATE_LEN = 7
TRIALS = 20000
rng = np.random.default_rng(11)


CONCENTRATION = 6.0    # lower means more variation between characters


def vote_plate_accuracy(p_char, n_reads, trials=TRIALS):
    """Fraction of plates read correctly after per-character majority voting.

    Each character of each plate gets its own accuracy, drawn around p_char.
    That accuracy holds for every frame of the pass, so a character the camera
    renders badly stays bad and voting converges on the wrong answer.
    """
    a = p_char * CONCENTRATION
    b = (1 - p_char) * CONCENTRATION
    p_tc = rng.beta(a, b, size=(trials, PLATE_LEN))[:, :, None]

    correct = rng.random((trials, PLATE_LEN, n_reads)) < p_tc
    # a wrong read lands on this character's usual confusion, 0 is the right answer
    confusion = rng.integers(1, ALPHABET, size=(trials, PLATE_LEN, 1))
    slips = rng.random((trials, PLATE_LEN, n_reads)) < 0.75
    scatter = rng.integers(1, ALPHABET, size=(trials, PLATE_LEN, n_reads))
    wrong_pick = np.where(slips, confusion, scatter)
    reads = np.where(correct, 0, wrong_pick)

    # majority vote per character: the modal value wins, ties go to the lowest id
    counts = np.zeros((trials, PLATE_LEN, ALPHABET), dtype=np.int16)
    idx0 = np.arange(trials)[:, None, None]
    idx1 = np.arange(PLATE_LEN)[None, :, None]
    np.add.at(counts, (idx0, idx1, reads), 1)
    voted = counts.argmax(axis=2)
    return float((voted == 0).all(axis=1).mean())


reads_axis = np.arange(1, 22, 2)
fig, axs = plt.subplots(1, 2, figsize=(11.6, 4.9))

ax = axs[0]
for i, p in enumerate([0.80, 0.90, 0.95]):
    ys = [vote_plate_accuracy(p, n) * 100 for n in reads_axis]
    ax.plot(reads_axis, ys, marker="o", ms=4.5, color=C[i],
            label=f"{int(p * 100)}% per character")
ax.set_xlabel("frames combined (majority vote per character)")
ax.set_ylabel("whole plates read correctly (%)")
ax.set_title("Voting across frames, 7-character plate", fontsize=12.5, loc="left")
ax.set_ylim(0, 103)
ax.set_xticks(reads_axis[::2])
ax.legend(title="single-frame accuracy", title_fontsize=10.5, fontsize=10.5, loc="lower right")

ax = axs[1]
singles = np.array([vote_plate_accuracy(p, 1) for p in (0.80, 0.90, 0.95)]) * 100
voted15 = np.array([vote_plate_accuracy(p, 15) for p in (0.80, 0.90, 0.95)]) * 100
x = np.arange(3)
ax.bar(x - 0.2, singles, 0.38, color=CRIT, label="one frame")
ax.bar(x + 0.2, voted15, 0.38, color=GOOD, label="15 frames voted")
for xi, (a, b) in enumerate(zip(singles, voted15)):
    ax.text(xi - 0.2, a + 1.5, f"{a:.0f}", ha="center", fontsize=11, color=INK)
    ax.text(xi + 0.2, b + 1.5, f"{b:.0f}", ha="center", fontsize=11, color=INK, weight="bold")
ax.set_xticks(x, ["80%", "90%", "95%"])
ax.set_xlabel("single-frame per-character accuracy")
ax.set_ylabel("whole plates read correctly (%)")
ax.set_title("The same model, read once or read often", fontsize=12.5, loc="left")
ax.set_ylim(0, 112)
ax.legend(fontsize=10.5, loc="upper left")

fig.suptitle("A mediocre recogniser read twenty times beats a good one read once",
             x=0.01, ha="left", fontsize=14.5, weight="bold")
fig.tight_layout()
save(fig, f"{SLUG}-voting-across-frames.png")

print("single-frame:", singles.round(1), " voted-15:", voted15.round(1))
