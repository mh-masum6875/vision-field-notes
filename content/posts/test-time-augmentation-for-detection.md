---
title: "Test-Time Augmentation for Detection: When It Is Worth the Cost"
description: "Running a detector on flipped and rescaled copies can raise accuracy at two or more times the compute. Where TTA helps, where it hurts."
category: "YOLO and Detection Basics"
date: 2026-11-29
tags: [tta, augmentation, inference, accuracy, yolo]
---

Test-time augmentation (TTA) runs the model several times on modified copies of the same image, such as flipped or rescaled versions, and merges the results. It often improves accuracy a little without any retraining, which makes it tempting. It also multiplies inference cost, and in a live video system that cost is usually better spent elsewhere.

This article explains how TTA works for detection, what it costs, the situations where it is worth it, and the ones where it quietly causes problems.

## How it works

1. Make several versions of the input: the original, a horizontal flip, and one or more rescaled copies.
2. Run the detector on each.
3. Transform the boxes back to the original image's coordinates (un-flip, un-scale).
4. Merge all boxes from all passes, typically with NMS or weighted box fusion, so that the same object detected in several passes becomes one box.

The idea is that each version gives the model a slightly different view. An object missed in one pass may be found in another, and boxes from several passes average out small localisation errors.

In Ultralytics, TTA is enabled with `augment=True` at prediction or validation time. In the current source, it runs three passes: the original image, a 0.83 scale with a horizontal flip, and a 0.67 scale. The details may change between versions.

## What it costs

Each pass costs roughly in proportion to the number of pixels it processes, so a pass at scale *s* costs about *s*² of the original.

![Horizontal bars of relative inference compute: single pass 1.00x, adding a horizontal flip 2.00x, the Ultralytics augment option with scales 1.0, 0.83 flipped and 0.67 2.14x, scales 1.0, 1.25 and 1.5 4.81x, and scales 1.0 and 1.5 each with a flip 6.50x.](img:test-time-augmentation-for-detection-cost.png "Arithmetic, not a benchmark: the sum of squared scales over the passes, ignoring the extra cost of merging boxes. Real timings depend on hardware, batching and post-processing.")

So the default Ultralytics TTA costs a little over twice a single pass. Variants that add larger scales, which help small objects, can cost four to seven times as much. There is also the merging step, and latency increases unless the passes run in parallel.

## Where it helps

### Offline and batch processing

When time is not critical, such as reviewing recorded footage, processing a backlog of images, or producing pre-labels for annotation, a few percent more accuracy can be worth two or three times the compute. TTA is a reasonable default for pseudo-labelling with a teacher model; see [Pseudo-Labelling with a Larger Model](post:pseudo-labelling-with-a-larger-model).

### Evaluating hard cases

TTA can be a quick probe. If TTA with larger scales finds many objects the single pass misses, the model is limited by object size, and a larger input size or tiling may help in production. That is useful information even if you never deploy TTA. See [Input Resolution or Model Size](post:input-resolution-or-model-size).

### Low-frequency, high-value decisions

A system that analyses one image per event, such as a photo at a gate, can afford several passes per image.

## Where it does not help, or hurts

### Live multi-camera video

At two or more times the cost per frame, TTA cuts the number of cameras a box can handle by half or more. The same compute spent on a larger model, a larger input size or a higher analysis frame rate usually gives a bigger and more predictable gain. Video also has its own form of "augmentation": the same object appears in many frames, and temporal filtering combines evidence across them. See [Reducing False Alarms in Production Video Analytics](post:reduce-false-alarms-in-production).

### Flips that change meaning

A horizontal flip turns a left-pointing arrow into a right-pointing one, mirrors text, and swaps left and right hands. If any class depends on direction or handedness, flip-based TTA can produce confident wrong labels. The same caution applies to flips in training augmentation. See [Data Augmentation for Object Detection](post:data-augmentation-for-detection).

### Changed confidence and thresholds

Merged boxes have different score distributions from single-pass boxes. Thresholds tuned without TTA do not transfer. If you switch TTA on or off, re-tune thresholds on validation data. See [Why a Detector's Confidence Is Not a Probability](post:detector-confidence-is-not-a-probability).

### More duplicates in crowds

Merging boxes from several passes in crowded scenes can produce extra duplicates or merge neighbours, depending on the merging method and IoU threshold. Check results in your busiest scenes.

## How to decide with data

1. Choose your operating constraint, such as recall at a required precision.
2. Validate with and without TTA on a test set that represents deployment, with thresholds re-tuned for each.
3. Compare per class and by object size, not only overall mAP. TTA gains are often concentrated in small objects.
4. Measure the time per image on the target hardware for both.
5. Compare TTA with the alternatives at similar cost: a larger model, a larger input, tiling.
6. For video systems, compare at the event level, since temporal filtering may already capture the gain. See [Measuring Video Analytics by Events, Not Frames](post:evaluate-video-analytics-by-events).

If TTA wins on accuracy per unit of compute for your use, use it. If a larger model or input matches it for the same cost, the single-pass option is simpler to run and to reason about.

## Checklist

- Know how many passes and which scales your TTA uses.
- Estimate cost as the sum of squared scales, then measure.
- Use TTA for offline work, pseudo-labelling and probing small-object limits.
- Avoid it for live multi-camera video unless measured to be worth it.
- Disable flips for direction-dependent classes.
- Re-tune thresholds when switching TTA on or off.
- Compare against a larger model or input at the same cost.

Next steps: [Nano, Small, Medium: How to Choose a YOLO Model Size](post:choosing-yolo-model-size) and [Comparing Two Detectors Fairly](post:comparing-two-detectors-fairly).
