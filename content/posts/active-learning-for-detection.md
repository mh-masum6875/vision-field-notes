---
title: "Choosing What to Label Next: Active Learning That Works"
description: "Labelling budget is finite. Picking frames by uncertainty beats picking at random, if you avoid the three ways it goes wrong."
category: "Datasets and Training"
date: 2026-11-28
tags: [active-learning, labelling, datasets, training, workflow]
---

You have ten thousand hours of production footage and budget to label two thousand frames. Picking them at random is the baseline. Picking them well is worth a surprising amount — often the difference between a model that improves and one that does not move.

The idea is simple: label the frames the model finds hardest. Doing it without poisoning your dataset takes a bit more care.

## Four ways to pick, in increasing order of usefulness

**Low confidence.** Score every frame by its lowest-confidence detection, or by the count of detections near your threshold. Easy, and a reasonable first pass.

**Model disagreement.** Run two models — different architectures, or different training seeds — and select frames where they disagree most. Stronger than confidence alone, because a single model can be confidently wrong in a consistent way, and two rarely are in the same way.

**Temporal inconsistency.** This one is specific to video and underused. Track detections across a few frames. A track that appears, vanishes for two frames and reappears is a near-certain model failure, and you did not need a second model to find it. Flickering tracks are a rich, cheap source of hard examples.

**Prediction count anomalies.** Frames where the model found far more or far fewer objects than neighbouring frames. Usually either a genuine event or a failure, and both are worth looking at.

Temporal inconsistency and disagreement give the best return in my experience, because they find failures rather than just uncertainty.

## The three ways it goes wrong

**Near-duplicates.** Video is 25 frames a second of almost the same picture. An uncertainty score picks the hardest frame, and then the next 24 frames are equally hard and nearly identical. You spend your whole budget labelling one difficult moment.

Fix it by deduplicating before selection: enforce a minimum time gap between chosen frames, and cluster by embedding similarity to drop near-identical picks from different moments.

**Distribution skew.** Uncertainty sampling concentrates on the hard tail by design. Do it for several rounds and your training set is almost entirely edge cases, with the easy majority under-represented. The model gets better at the tail and worse at the ordinary cases that make up most of production.

Fix it by mixing: roughly 70% selected by uncertainty, 30% uniformly at random. The random portion keeps the distribution anchored.

**Labelling the garbage.** The highest-uncertainty frames are often uncertain because they are unusable — motion blur so severe nothing is visible, a frame captured during a stream glitch, a camera mid-reposition. Labellers waste time and the labels add noise.

Fix it with a quick quality filter before the queue: drop frames below a sharpness threshold, and let labellers mark "unusable" as a first-class outcome rather than forcing a box.

## Run it in rounds, and measure

Active learning is a loop, not a one-off:

1. Train on what you have
2. Score the unlabelled pool
3. Select a batch, deduplicated and mixed with random
4. Label it
5. Retrain and evaluate on a **fixed** held-out test set
6. Repeat

Step 5 is the one people skip and it is the one that tells you whether any of this is working. The test set must be fixed across rounds and selected randomly, never by uncertainty, or you cannot compare rounds at all.

Plot test performance against labels spent, with a random-selection baseline on the same axes. If your clever selection is not beating random, stop doing it and label randomly — that happens more often than the literature suggests, particularly when the pool is small or already well covered.

## Batch size matters

Selecting one frame, retraining, and selecting again is optimal and impractical. Selecting all two thousand in one shot wastes the loop entirely.

Something in the region of a few hundred per round is a reasonable compromise for most projects: large enough that labelling is efficient and retraining is not constant, small enough that later rounds benefit from earlier ones.

## Where it pays off most

Active learning is most valuable when the unlabelled pool is large and varied, and when there is a real class imbalance — rare events buried in hours of nothing.

It is least valuable when the pool is small, when it is already well covered by what you have labelled, or when your real problem is label quality rather than label quantity. In that last case the budget is better spent re-labelling what you have with a clearer annotation guide.

Diagnose which problem you have before building the loop. A model that is wrong because the labels disagree with each other will not be fixed by adding more of the same.
