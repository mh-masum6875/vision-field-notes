---
title: "YOLO27 Announced: What to Check Before You Switch"
description: "Ultralytics announced YOLO27 in September 2026. What was actually said, what is still unknown, and how to evaluate it on your own data when it ships."
category: "YOLO and Detection Basics"
date: 2026-11-05
tags: [news, yolo27, ultralytics, model-selection, yolo]
---

Ultralytics announced YOLO27 at its YOLO Vision 2026 event on 13 September 2026. Every new YOLO generation brings the same question from clients and colleagues: should we switch? This post summarises what was announced, separates claims from things that are still unknown, and sets out how to decide once the models are actually available.

This is written as of early November 2026. Details may change before release, so check the sources at the end.

## What was announced

According to Ultralytics' own summary of the event:

- **Four model sizes:** n and s for edge devices, m for demanding detection tasks that still need real-time speed, and l for high-precision work. There is no x size this time.
- **Seven tasks:** object detection, instance segmentation, semantic segmentation, depth estimation, classification, pose estimation and oriented object detection, giving 28 models in total.
- **An accuracy claim:** YOLO27l is described as the first Ultralytics model to pass 60 mAP on COCO. No full benchmark table or evaluation settings were published in the summary.
- **YOLOE-27:** a new generation of the open-vocabulary models, which detect and segment objects from text or visual prompts.
- **Domain models:** "YOLO27 Enterprise" variants pretrained for retail, warehousing, security and aerial imagery.
- **Timing:** release "later this year", with a waitlist. At the time of writing, I have not found a general release.

The previous generation, YOLO26, released in January 2026, introduced an end-to-end head that can run without NMS and removed the distribution focal loss from the detection head, partly to make export simpler. The YOLO27 announcement does not describe its architecture in detail.

## What is still unknown

Before any decision, these are the questions that matter, and none of them is answered by the announcement:

- **Licence.** YOLO26's code and models are offered under AGPL-3.0 and an enterprise licence. The YOLO27 announcement does not state a licence. For commercial products this is often the deciding factor; see [YOLO Licenses Explained](post:yolo-licenses-explained).
- **Speed on your hardware.** A higher COCO score from the largest model says nothing about the n or s model on a Jetson, a Hailo accelerator or a CPU.
- **Export and runtime support.** New architectures sometimes use operations that a particular export path, compiler or accelerator toolchain does not support yet. Edge toolchains often lag behind new model releases.
- **Small-object and night performance.** COCO is mostly daylight photos. It does not represent overhead security cameras or infrared night images. See [What mAP Hides](post:what-map-hides).
- **Accuracy at your operating point.** A higher mAP does not guarantee better recall at the precision your alerts need.

## Should you switch?

Not on the announcement alone. A sensible plan:

1. **Do nothing to production now.** A model that is working on your cameras is worth more than a promised improvement.
2. **When it ships, check the licence first.** If it does not fit your product, stop there.
3. **Fine-tune it on your own data** with the same dataset version, training budget and image size as your current model.
4. **Compare fairly** on your own test set, at your operating threshold, per class and by object size, with more than one training run if the difference is small. See [Comparing Two Detectors Fairly](post:comparing-two-detectors-fairly).
5. **Export and measure on the target device,** with the same method as your current model. See [Measuring FPS and Latency Correctly](post:measuring-fps-and-latency-correctly).
6. **Run the replay set** at the event level before any rollout. See [Building a Replay Set of Recorded Footage](post:building-a-replay-set).
7. **Roll out in stages** if it wins. See [Updating Models on Edge Devices Without Bricking Them](post:updating-models-on-edge-devices).

If the gains on your data are within the noise between training runs, staying on the current model is a perfectly good outcome. The work of re-tuning thresholds, re-validating exports and re-testing at night is real, and it should buy a measurable improvement.

## Where the new pieces may matter

Two parts of the announcement may be more interesting for production work than the headline mAP:

- **Open-vocabulary models (YOLOE-27)** can be useful for pre-labelling new classes before you have training data, as a teacher in a pseudo-labelling workflow. Treat their output as suggestions and review it. See [Pseudo-Labelling with a Larger Model](post:pseudo-labelling-with-a-larger-model).
- **Domain-pretrained models** for retail, warehouses and security could shorten fine-tuning for those settings, if their training data resembles your cameras. Test that claim on your own footage; "security" pretraining on one kind of camera may not transfer to another.

## Sources

- Ultralytics, "Key highlights from Ultralytics YOLO Vision 2026" (15 September 2026): [ultralytics.com/blog/key-highlights-from-ultralytics-yolo-vision-2026](https://www.ultralytics.com/blog/key-highlights-from-ultralytics-yolo-vision-2026)
- Ultralytics YOLO26 documentation: [docs.ultralytics.com/models/yolo26](https://docs.ultralytics.com/models/yolo26/)
- Ultralytics YOLO Vision 2026 event page: [ultralytics.com/events/yolovision](https://www.ultralytics.com/events/yolovision)

Next steps: [YOLOv5 vs YOLOv8 vs YOLO11: Which Should You Use?](post:yolov5-vs-yolov8-vs-yolo11) and [Comparing Two Detectors Fairly](post:comparing-two-detectors-fairly).
