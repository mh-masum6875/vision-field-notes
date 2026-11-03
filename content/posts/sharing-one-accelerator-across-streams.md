---
title: "Sharing One Accelerator Across Many Streams"
description: "One GPU or NPU serving many cameras needs scheduling: one shared model, latest-frame queues, batching across streams and fair turns."
category: "Edge Hardware and Deployment"
date: 2026-11-20
tags: [scaling, gpu, batching, scheduling, edge-ai]
---

The simplest multi-camera pipeline starts one process per camera, each loading its own copy of the model. It works for two cameras. At ten it runs out of accelerator memory, the cameras compete for the device in an uncontrolled way, and latency on some cameras grows while others run fine.

An accelerator, whether a GPU, an NPU or a dedicated AI chip, is a shared resource, and it works best when it is shared deliberately. This article covers how to plan capacity, how to structure the pipeline around one shared model, and how to keep every camera served fairly.

## Plan capacity in inferences per second

Start with arithmetic. The accelerator can sustain some number of inferences per second for your model at your input size and precision; measure it on the device with the method in [Measuring FPS and Latency Correctly](post:measuring-fps-and-latency-correctly). Each camera needs as many inferences per second as its analysis frame rate. So:

cameras ≈ (capacity × planned load) / analysis frame rate

![Bar chart of how many cameras one accelerator can serve against the analysis frame rate per camera, for an example capacity of 200 inferences per second planned at 70% load: 140 cameras at 1 frame per second, 70 at 2, 46 at 3, 28 at 5, 17 at 8, 14 at 10, 9 at 15 and 5 at 25.](img:sharing-one-accelerator-across-streams-cameras-vs-fps.png "Arithmetic with an example capacity, not a benchmark. Analysis frame rate is the strongest lever: halving it doubles the cameras a device can serve.")

Plan for a load well below 100%, because traffic is bursty, other work shares the device, and thermal limits may reduce capacity over time. See [Thermal Throttling on Edge Devices](post:thermal-throttling-on-edge-devices). And remember the accelerator is only one stage: decoding and pre-processing must keep up too. See [Hardware Video Decoding on Edge Devices](post:hardware-video-decoding-on-edge).

## One model, many cameras

Load the model once and send frames from all cameras to it. Separate model copies per camera waste memory, compete for the device without coordination, and cannot batch together.

A common structure:

1. **Capture workers**, one per camera or a pool, decode frames and keep only the latest frame per camera.
2. **A scheduler** decides which cameras' frames go to the model next and groups them into a batch.
3. **One inference worker** owns the model and runs batches.
4. **Post-processing workers** apply NMS, tracking and rules per camera, since these are per-camera state.

Keep tracking and rules per camera. Only inference is shared.

## Latest frame, not every frame

For live analytics, an old frame is worth less than a new one. Each camera should hold only its most recent frame (or a very short queue). When the scheduler picks a camera, it takes that latest frame and discards anything older. This keeps latency bounded even when the device is temporarily overloaded: the system analyses fewer frames per second rather than falling further and further behind.

Record how many frames were dropped per camera; it is the first sign that capacity is running out. See [Metrics and Logging for a Vision Service](post:metrics-and-logging-for-vision-services).

## Batching across streams

Accelerators are usually more efficient with batches than with single images, because a batch uses the hardware more fully. Frames from several cameras can be stacked into one batch.

Two cautions:

- **Batching adds waiting time.** A frame may wait for others to fill the batch. Use a maximum wait: send the batch when it is full or when the oldest frame has waited a few milliseconds, whichever comes first. This is often called dynamic batching. Inference servers such as NVIDIA Triton provide it, and NVIDIA DeepStream batches multiple streams through its stream muxer.
- **Batch size must be supported by the model.** Exported models and engines often have fixed or limited batch sizes. Export with dynamic batch dimensions or a fixed size you will fill, and check the throughput at different batch sizes on your device; the benefit varies and sometimes flattens early.

Measure throughput and latency for batch sizes of 1, 2, 4 and 8 on the target device before choosing.

## Fairness and priorities

Without a scheduler, cameras that deliver frames slightly faster, or whose capture thread wins the race, get more inferences, and others starve. A simple fair scheme:

- **Round robin:** each scheduling round takes one frame from each camera that has a new frame due, according to its target analysis rate.
- **Per-camera target rates:** a doorway counter may need 10 fps while a yard camera needs 2. The scheduler serves each at its own rate.
- **Priorities under overload:** if capacity runs short, decide in advance which cameras keep their rate and which are slowed down. Safety-critical cameras first.

Time-based scheduling also protects you when cameras change frame rate at night. See [When the Camera Changes Its Frame Rate at Night](post:variable-frame-rate-at-night).

## Several models on one device

Many systems run more than one model: a detector plus a crop classifier, or different detectors for different cameras. Options:

- Run them sequentially in the same inference worker, which is simple and predictable.
- Run them in separate workers that share the device, which can improve utilisation but makes timing harder to reason about.

Second-stage models often run on far fewer inputs than the detector, only on detected crops, so batch their inputs across cameras too. Measure the combined load, not each model alone. See [Single-Class or Multi-Class](post:merge-or-split-detection-classes) for when a second stage is worth it.

## Failure isolation

One shared model means one shared failure point. If the inference worker crashes, every camera stops. Make sure:

- The inference worker restarts quickly and capture workers survive the restart.
- A single bad frame (corrupt, wrong size) cannot crash the batch; validate inputs before batching.
- Health checks cover the inference worker specifically. See [Watchdogs and Self-Recovery for Unattended Edge Boxes](post:watchdogs-for-unattended-edge-boxes).

## Checklist

- Measure the device's sustained inferences per second for your model.
- Plan cameras from analysis frame rates, with a load margin.
- Load the model once; keep tracking and rules per camera.
- Keep only the latest frame per camera; count dropped frames.
- Use dynamic batching with a maximum wait; measure batch sizes on the device.
- Schedule fairly with per-camera target rates and overload priorities.
- Measure combined load when running several models.
- Isolate failures and health-check the inference worker.

Next steps: [Scaling Video Analytics to Hundreds of Camera Streams](post:scaling-to-hundreds-of-camera-streams) and [CPU-Only Inference](post:cpu-only-inference-openvino-onnx-runtime).
