---
title: "Detecting Model Drift in Production Without Labels"
description: "Your detector was fine in March and quietly worse by September. How to notice drift when nobody is labelling production footage."
category: "Video Analytics"
date: 2026-11-24
tags: [monitoring, drift, production, metrics, deployment]
---

A detector does not usually fail suddenly. It degrades. Vegetation grows in front of a camera, a car park gets resurfaced and changes colour, a shop rearranges its shelves, winter arrives and everyone is wearing dark coats. Each change is small. Together, six months later, recall is noticeably worse and nobody noticed the day it happened.

The obvious fix is to keep labelling production footage and track mAP over time. In practice almost nobody does this, because labelling is expensive and the people running the system are not the people who built it. So you need signals that do not require ground truth.

None of them tells you accuracy. All of them tell you that something changed, which is the part you actually need to know.

## Track the confidence distribution, not the mean

The mean confidence of your detections is a weak signal because it moves for boring reasons. The shape of the distribution is much more informative.

A healthy detector on familiar data gives you a bimodal histogram: a cluster of confident detections near the top, and a tail of marginal ones near your threshold. When the domain shifts, the confident cluster thins out and the tail fattens. The mean may barely move while that is happening.

Record a histogram of detection confidences per camera per day. Compare it against a baseline period using something like a Kolmogorov-Smirnov statistic or simply the proportion of detections above 0.8. A camera whose high-confidence fraction halves over a month is telling you something, and it costs nothing to compute.

Do this per camera. Aggregating across a site averages away exactly the signal you want, because drift is usually local to one view.

## Watch detection counts against their own seasonality

Counts are the easiest thing to monitor and the easiest to misread.

A car park sees more cars on weekdays. A shop sees more people at lunchtime. A street camera sees almost nothing at 4am. Comparing today's count against yesterday's will generate alerts constantly and teach everyone to ignore them.

What works is comparing each hour against the same hour on the same weekday, averaged over the previous several weeks. Alert on a sustained deviation, not a single hour. A camera that detects 40% fewer people every weekday morning for a week has either changed or broken, and either way you want to know.

This catches the dramatic failures — a camera knocked out of position, a lens gone out of focus, a stream silently dropping to a lower resolution — faster than anything else.

## Compare against a second opinion

If you have the compute, run a larger and slower model on a small sample of frames, say one frame a minute, and compare its detections against the production model's.

This is not ground truth. The big model is wrong too. But the *disagreement rate* between two models is a usable signal, because it is stable while the data looks like the training distribution and rises when it does not.

The appeal of this approach is that it is cheap to run on a sample and it points at specific frames. When the disagreement rate climbs, you have a pile of frames where the two models differ, which is exactly the set you want to look at and, eventually, to label.

That makes it an active learning loop as well as a monitoring signal, which is a rare two-for-one.

## Watch the input, not just the output

Some of the most useful signals never touch the model.

Mean frame brightness and contrast, per camera per hour, catch exposure changes, a failing IR illuminator, and a camera that has started pointing at a wall. Sharpness, measured as the variance of a Laplacian, catches a dirty or defocused lens. The compression bitrate reported by the stream catches a camera that has silently been reconfigured.

These are a few lines of code each and they catch the majority of real-world degradation, because most of it is physical rather than statistical.

## What to do when a signal fires

The first question is always whether the camera changed or the world changed, and the answer is usually visible in ten seconds of footage. Keep a handful of sample frames per camera per week so you can compare against what the view looked like before.

If the camera moved, dirtied or refocused, fix the camera. No amount of retraining substitutes for cleaning a lens.

If the view is the same and the world changed, you need data from the new world. This is where the disagreement sampling pays off: you already have a set of frames where the models differ, which is a far better labelling queue than a random sample.

## What this does not give you

Be honest with yourself and with whoever is paying. Every signal here detects *change*, not *correctness*. A model that was always bad at detecting cyclists will keep being bad at it, consistently, and none of this will fire.

For that you need a labelled evaluation set, refreshed periodically from real production footage. The monitoring above tells you when to go and build one. It does not replace it.

## A reasonable starting point

For a system you want to keep alive for years without a dedicated ML team, this is roughly the minimum that earns its keep:

- Per-camera, per-hour detection counts, compared against a trailing same-hour baseline
- Per-camera, per-day confidence histograms
- Per-camera brightness and Laplacian variance
- A weekly sample frame archived from every camera

That is a few hundred lines of code and a small database table. It will not tell you your mAP. It will tell you which of your forty cameras is the one that started lying to you, which is the question you will actually be asked.
