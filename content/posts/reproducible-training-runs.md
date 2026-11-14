---
title: "Reproducible Training Runs: Seeds, Versions and What Still Varies"
description: "Setting a seed is not enough to reproduce a detector. What else to pin, which differences remain even then, and how to work with the variation."
category: "Tools and Workflow"
date: 2026-11-22
tags: [reproducibility, training, seeds, pytorch, workflow]
---

You retrain last month's model with the same data and settings, and the new one scores a point lower. Is something broken, or is that normal? Without knowing how much a training run varies on its own, you cannot tell, and every comparison between models becomes guesswork.

![Two panels. The left shows one training run of an old config at 54.3 mAP and one of a new config at 52.7, a gap of 1.6 points, labelled as the comparison usually looks. The right shows the same two configs trained eight times each: the old config averages 54.07 with a standard deviation of 0.61, the new averages 53.62 with 0.71, and the two clouds of points overlap heavily. The single pair from the left panel is circled, and sits at the top of one cloud and the bottom of the other.](img:reproducible-training-runs-run-to-run-spread.png "Simulated runs with a spread typical of a detector fine-tune. The real difference between these two configs is 0.45 points.")

The circled pair is the trap. Those two runs are both perfectly ordinary — one happens to sit near the top of its spread, the other near the bottom — and comparing them suggests the new config costs you **1.6 points**. Train both eight times and the real difference is **0.45**.

Nothing was broken, nobody made a mistake, and the conclusion was still wrong by a factor of three. That is what one run against one run buys you, and it is why the first number worth measuring is not a model's score but your own spread.

This article covers what it takes to reproduce a detector training run, what variation remains even when you do everything right, and how to work with that variation.

## Two kinds of reproducibility

It helps to separate two goals:

- **Exact reproduction:** the same inputs give bit-for-bit the same weights. Useful for debugging and audits, and hard to guarantee across machines.
- **Statistical reproduction:** rerunning gives a model whose results fall within a known, small range. This is what you need for decisions, and it is achievable.

Aim for the second, and get as close to the first as is practical.

## What must be pinned

### Data

The exact images, labels and splits. A dataset that has grown by a few hundred images since the last run is a different experiment. Train from a named dataset version. See [Versioning Datasets and Models Together](post:versioning-datasets-and-models).

### Code and configuration

The commit of the training code, with no uncommitted changes, and the full configuration actually used, saved with the run. Ultralytics saves the resolved arguments as `args.yaml` in each run folder; keep it.

### Environment

Library versions matter: PyTorch, CUDA, cuDNN, the training framework, OpenCV and NumPy. Defaults and algorithms change between versions, sometimes in ways that affect results. Pin them with a lockfile or a container image, and record the GPU type and driver. See [Setting Up a Clean Python Environment for Computer Vision](post:python-environment-for-computer-vision).

### Randomness

Seeds control data order, augmentation choices and the initialisation of new layers. Set them, and record them. In Ultralytics, the `seed` and `deterministic` training arguments control this; check the current defaults in the documentation or your saved `args.yaml`.

## What still varies

Even with everything above pinned, results can differ between runs:

- **Non-deterministic GPU operations.** Some GPU kernels, for speed, do not guarantee the same order of floating-point additions, so results differ in the last bits. Over many training steps, those differences grow into slightly different models. PyTorch offers `torch.use_deterministic_algorithms(True)` and related cuDNN settings to avoid them, at some cost in speed, and some operations have no deterministic version and will raise an error.
- **Data loading with multiple workers.** Worker processes need their own seeding. Frameworks handle this, but custom datasets and augmentations can break it.
- **Different hardware.** A different GPU model, or a different number of GPUs, changes how computation is split and ordered. Exact reproduction across hardware is generally not expected.
- **Mixed precision.** Automatic mixed precision adds its own small numerical differences.
- **Early stopping and best-epoch selection.** Small differences in validation metrics can change which epoch is chosen, which magnifies tiny differences into visible ones.

None of this is a bug. It means that a model's score is one sample from a distribution of possible scores.

## Measure the variation

The most useful single habit: **train the baseline more than once.** Run the same configuration with two or three different seeds, and look at the spread of the metrics you care about. That spread is your noise level.

Then, when comparing a change against the baseline:

- A difference much larger than the spread is probably real.
- A difference within the spread is not established, however good it looks.
- If the difference matters and is close to the spread, run more seeds of both.

Seed noise is separate from test-set noise, which comes from the limited number of test images. Both add up. [Comparing Two Detectors Fairly](post:comparing-two-detectors-fairly) covers the test-set side and how to combine them.

Cost is the obvious objection. Training several times is expensive. But one extra run of the baseline, done once per project or per major dataset change, is cheap compared with weeks spent chasing an improvement that was noise.

## Record everything automatically

Do not rely on memory or notes. For each run, record automatically:

- Run ID, date, machine, GPU type and driver.
- Git commit and a flag for uncommitted changes.
- Dataset version.
- Full resolved configuration and seed.
- Environment lockfile or container image digest.
- Final and best metrics, with the epoch chosen.
- Paths and hashes of output weights.

Experiment trackers do most of this. See [Experiment Tracking: TensorBoard, Weights & Biases and MLflow](post:experiment-tracking-tensorboard-wandb-mlflow). Make the dataset version a required argument so it is never missing.

## Practical settings

- Fix seeds for routine runs, and vary them deliberately when measuring noise.
- Use deterministic settings when debugging a specific difference; accept non-determinism for routine training if it is noticeably faster.
- Run comparisons on the same hardware type where possible.
- Keep the evaluation deterministic: same test set version, same evaluation code and settings, batch size and image size recorded. Evaluation variation is easy to remove completely, so remove it.
- Archive the exact container or environment used for any model that goes to production, so it can be retrained later.

## Checklist

- Named dataset version for every run.
- Committed code and saved resolved configuration.
- Pinned environment, recorded hardware and driver.
- Seeds set and recorded; deterministic mode available for debugging.
- Baseline trained at least twice to estimate seed noise.
- Changes judged against seed noise and test-set noise.
- Run metadata recorded automatically.
- Evaluation fully deterministic.

Next steps: [Comparing Two Detectors Fairly](post:comparing-two-detectors-fairly) and [Reading YOLO Training Curves](post:reading-yolo-training-curves).
