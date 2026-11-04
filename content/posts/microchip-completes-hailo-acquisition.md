---
title: "Microchip Completes Its Hailo Acquisition: What It Means for Edge Vision Projects"
description: "Microchip closed its acquisition of edge AI chipmaker Hailo in September 2026. What is known, what is not, and how to manage accelerator vendor risk."
category: "Edge Hardware and Deployment"
date: 2026-11-06
tags: [news, hailo, edge-ai, accelerators, vendor-risk]
---

Hailo, the company behind the Hailo-8 accelerators and the chips on the Raspberry Pi AI Kit and AI HAT+ boards, is now part of Microchip Technology. Microchip announced the agreement in late July 2026 and completed the acquisition on 21 September 2026. Terms were not disclosed.

If you have Hailo hardware in the field, or are designing a product around it, this is worth a few minutes of thought. This post covers what has been said, what has not, and what a sensible engineering response looks like. It is written as of early November 2026.

## What has been said

- **The deal is complete.** Microchip announced completion on 21 September 2026. Trade coverage reports that terms were not disclosed and that Microchip does not expect a material effect on its financial results.
- **Hailo's products join Microchip's embedded line-up.** Microchip describes adding Hailo's AI accelerators, vision processors and AI software to its embedded systems portfolio, aiming at complete platforms for intelligent systems.
- **Continued support was stated.** When the agreement was announced, Hailo told its developer community it remains committed to supporting the people building with its products. Asked on Hailo's community forum about the Hailo-10H on the Raspberry Pi AI HAT+ 2, a Hailo representative replied: "All products will continue to be supported and maintained."

## What has not been said

As far as I can find, there has been no public detail on:

- Long-term roadmaps for specific chips or modules.
- Changes, if any, to the software stack, such as the compiler, runtime and model zoo, or to their licences.
- Pricing or distribution changes for existing products.
- How Hailo's products will be combined with Microchip's own processors and FPGAs.

None of this is unusual straight after an acquisition, and none of it is a reason for alarm. But it is a reason to check your assumptions.

## What I would do as an engineer

Acquisitions are one form of a general risk: your accelerator vendor changes direction. The same advice applies whatever the vendor.

### Keep the model portable

Keep your trained model in a framework-neutral form, such as ONNX, alongside the vendor-compiled file, and keep the full training setup reproducible. Then moving to another accelerator means recompiling and revalidating, not retraining from scratch. See [Export YOLO to ONNX and Run It with ONNX Runtime](post:export-yolo-to-onnx) and [Reproducible Training Runs](post:reproducible-training-runs).

### Pin and archive the toolchain

Vendor compilers and runtimes change between versions, and old versions can become hard to download. Archive the exact compiler, runtime and drivers you use, with the calibration set used for quantization. If you ever need to rebuild a model for hardware in the field, you will need them. See [Versioning Datasets and Models Together](post:versioning-datasets-and-models).

### Keep the pipeline hardware-agnostic

Put the accelerator behind a small interface in your code: load a model, run a batch, return outputs. Decoding, tracking, rules and alerts should not know which chip runs inference. This also makes it easy to benchmark alternatives. See [Sharing One Accelerator Across Many Streams](post:sharing-one-accelerator-across-streams).

### Check supply for products, not prototypes

If you ship hardware, ask your distributor about lead times and long-term availability for the exact modules you use, and record the answer. That applies to every component, not only accelerators.

### Have a tested fallback

Know which alternative you would move to, and test your model on it once: a Jetson, a CPU with OpenVINO or ONNX Runtime, or another accelerator. Accuracy after quantization differs between toolchains, so a fallback is only real once it has been validated on your data. See [CPU-Only Inference](post:cpu-only-inference-openvino-onnx-runtime) and [INT8 Quantization for Detectors](post:int8-quantization-explained).

## For Raspberry Pi users

If you use the Raspberry Pi AI Kit or AI HAT+ boards, nothing changes for working systems in the short term, based on the statements above. Keep your current software versions pinned on deployed devices, test updates on a spare board before rolling them out, and watch the official Raspberry Pi and Hailo channels for announcements. See [Raspberry Pi AI Kit and Hailo Accelerators: Is It Worth It?](post:raspberry-pi-ai-kit-hailo).

## Sources

- Microchip Technology press release, "Microchip Technology Completes Acquisition of Hailo" (21 September 2026), via Nasdaq: [nasdaq.com](https://www.nasdaq.com/press-release/microchip-technology-completes-acquisition-hailo-2026-09-21)
- Jon Peddie Research, "Microchip acquires edge AI leader Hailo" (24 September 2026): [jonpeddie.com](https://www.jonpeddie.com/news/microchip-acquires-edge-ai-leader-hailo/)
- Hailo Community announcement and replies (27–28 July 2026): [community.hailo.ai](https://community.hailo.ai/t/microchip-technology-signs-definitive-agreement-to-acquire-hailo/19608)

Next steps: [Raspberry Pi vs Jetson Orin Nano for Object Detection](post:raspberry-pi-vs-jetson-orin-nano) and [Updating Models on Edge Devices Without Bricking Them](post:updating-models-on-edge-devices).
