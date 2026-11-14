---
title: "CPU-Only Inference: Getting the Most from OpenVINO and ONNX Runtime"
description: "No GPU on site? Detectors can still run on x86 CPUs. How to export, tune threads, pick input size and precision, and measure what a CPU can carry."
category: "Edge Hardware and Deployment"
date: 2026-11-17
tags: [cpu, openvino, onnx-runtime, inference, edge-ai]
---

Not every site has a GPU, and not every project can justify one. Many deployments end up on an industrial PC, a small-form-factor office machine or an existing server, with nothing but an x86 CPU. Detectors can run there, and for a modest number of cameras at sensible frame rates they often run well enough. But the gap between a naive setup and a tuned one is large.

This article covers the practical steps for CPU-only detection: choosing a runtime, exporting the model, tuning threads, choosing input size and precision, and measuring capacity honestly.

## Pick the right runtime

Running inference through a training framework on a CPU works but is rarely the fastest option. Two inference runtimes are common choices:

- **OpenVINO** is Intel's toolkit for optimised inference on Intel CPUs, integrated GPUs and NPUs. It converts models to its own format and applies optimisations for that hardware.
- **ONNX Runtime** runs ONNX models on many platforms, with a default CPU execution provider and optional providers for other hardware, including an OpenVINO provider.

Ultralytics can export directly to both formats (`format="onnx"` and `format="openvino"`). On an Intel CPU, try both. On other x86 CPUs, ONNX Runtime's default CPU provider is the safe starting point; check OpenVINO's documentation for which processors it supports before relying on it. See [Export YOLO to ONNX and Run It with ONNX Runtime](post:export-yolo-to-onnx).

Whatever you choose, measure on the exact machine you will deploy on. CPU inference speed varies with core count, instruction set support, memory bandwidth and cache sizes, so numbers from another CPU do not transfer well.

## Choose the model and input size for the CPU

On a CPU, compute is the limit, and the two big levers are model size and input size. Convolution cost grows roughly with the number of input pixels, so going from 640 to 480 cuts the work by almost half, and from 640 to 320 by three quarters. A nano model at 640 does a fraction of the work of a small model at 640.

![Two panels. The left is a bar chart of work relative to an input size of 640, for sizes from 320 to 1280: 320 is 0.25 times, 416 is 0.42, 480 is 0.56, 544 is 0.72, 640 is 1.00, 768 is 1.44, 960 is 2.25 and 1280 is 4.00. The right panel turns the same arithmetic into cameras per box on one CPU, relative to 640: 320 pixels gives 4 times the cameras, 480 gives 1.78 times, 640 gives 1 and 960 gives 0.44.](img:cpu-only-inference-openvino-onnx-runtime-input-size-cost.png "Arithmetic from pixel count alone. Real throughput also depends on the CPU, the runtime and threading, which is why the capacity section says to measure.")

The right-hand panel is the one to take to a budget conversation. Dropping from 640 to 480 is not a 25% saving because the side shrank by 25%; it is a **44% saving**, because both sides did. That is the difference between four cameras on a box and seven.

It also runs the other way, which is the part people get caught by. Someone raises the input size to 1280 to help with small objects and quietly asks the machine for **four times** the work. Nothing errors. The queue just grows until frames start being dropped, and the symptom shows up somewhere else entirely.

Start with the smallest model and input size that meet your accuracy needs on your own footage, then move up only if necessary. [Input Resolution or Model Size](post:input-resolution-or-model-size) explains which to change first for small objects.

## Tune threads

Thread settings matter more on a CPU than almost anything else, and the defaults are designed for one model running alone.

With ONNX Runtime:

```python
import onnxruntime as ort

opts = ort.SessionOptions()
opts.intra_op_num_threads = 4          # threads used inside one inference
opts.inter_op_num_threads = 1
opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
sess = ort.InferenceSession("model.onnx", opts, providers=["CPUExecutionProvider"])
```

The trade-off is between latency and throughput:

- **One inference using all cores** gives the lowest latency per frame but may not use cores efficiently, because parts of the network do not parallelise well.
- **Several inferences in parallel, each with fewer threads,** often gives higher total throughput across many cameras.

Try a few combinations, for example one session with all physical cores, two sessions with half each, four with a quarter, and measure total frames per second across all cameras and latency per frame. Remember that decoding, pre-processing and tracking also need cores; reserve some for them. OpenVINO exposes similar choices through performance hints for latency or throughput.

Physical cores usually matter more than logical ones. Hyper-threading can help a little or not at all for this kind of work, so compare thread counts equal to physical and logical cores.

## Precision: FP32, INT8

On most CPUs, FP32 is the default. FP16 is generally not a speed-up on CPUs unless the processor has specific support for it. INT8 can be substantially faster on CPUs with good integer instruction support, and both OpenVINO (through its post-training quantization tools) and ONNX Runtime (through its quantization utilities) can produce INT8 models from a calibration set.

INT8 comes with accuracy risks, especially for small objects and box precision. Calibrate with representative images from your cameras, validate against the FP32 model, and re-tune thresholds. [INT8 Quantization for Detectors](post:int8-quantization-explained) covers the process.

## Do not let pre-processing eat the CPU

On a GPU system, the CPU's job is mostly decoding and pre-processing. On a CPU-only system, those tasks compete with inference for the same cores. Every millisecond saved in pre-processing is a millisecond available for inference.

- Use camera substreams at a resolution close to the model input. See [Main Stream or Substream](post:main-stream-or-substream-for-analytics).
- Use hardware video decoding if the CPU's integrated graphics supports it. See [Hardware Video Decoding on Edge Devices](post:hardware-video-decoding-on-edge).
- Resize before converting colour, avoid copies, and drop frames you will not analyse as early as possible. See [Profiling a Python Vision Pipeline](post:profiling-a-python-vision-pipeline).
- Analyse at the frame rate the use case needs, not the camera's full rate. See [How Many Frames per Second Does Your Analytics Need?](post:how-many-fps-does-analytics-need).

## Measure capacity honestly

To know how many cameras one machine can carry:

1. Run the complete pipeline, with real streams or replayed recordings, at the planned analysis frame rate.
2. Add cameras one at a time, recording total processed frames per second, per-camera latency and CPU use.
3. Note the point where frames start to be dropped or latency rises sharply. That is the limit.
4. Run at a level below the limit for several hours, to include thermal effects and background tasks, and confirm it holds.
5. Plan production at a comfortable margin below the measured limit.

Use the method in [Measuring FPS and Latency Correctly](post:measuring-fps-and-latency-correctly): warm-up, steady state, percentiles, not just averages.

## When a CPU is not enough

If the measured capacity is far below what you need even after tuning, look at the alternatives before buying a large GPU server: a small accelerator card or USB accelerator, a machine with a capable integrated GPU or NPU, or an edge device per group of cameras. Sometimes the cheapest option is reducing the work: fewer cameras analysed, lower frame rates, or a smaller model where accuracy allows.

## Checklist

- Use an inference runtime, not the training framework.
- Try both OpenVINO and ONNX Runtime where supported, on the target CPU.
- Start with the smallest model and input size that meet accuracy needs.
- Tune intra-op threads and the number of parallel sessions for throughput.
- Reserve cores for decoding and pre-processing.
- Consider INT8 with careful calibration and validation.
- Cut pre-processing cost and analysis frame rate.
- Measure capacity with the full pipeline, over hours, and keep a margin.

Next steps: [Running Object Detection in the Browser with ONNX Runtime Web](post:onnx-runtime-web-in-the-browser) and [Sharing One Accelerator Across Many Streams](post:sharing-one-accelerator-across-streams).
