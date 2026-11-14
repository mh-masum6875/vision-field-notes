---
title: "What Video Compression Does to Your Detector"
description: "Bitrate, keyframe interval and codec choice change detection accuracy measurably. Where the cliff is, and how to find yours."
category: "Video Analytics"
date: 2026-11-26
tags: [compression, codec, bitrate, accuracy, cameras]
---

Everyone tunes the model. Far fewer people tune the stream feeding it, and the stream is often where the accuracy went.

A detector does not see what the camera sensor saw. It sees what survived H.264 or H.265 encoding at whatever bitrate the installer left configured, decoded on your machine. On a static scene that loss is nearly invisible to a human and still invisible to the model. On a scene with motion, it is neither.

## Where the loss actually lands

Video codecs spend their bits where human eyes look. They are built to preserve large smooth areas and overall structure, and to discard high-frequency detail, especially in regions that are changing quickly.

That is precisely backwards for small-object detection. The things your model struggles with — a distant person, a plate, a small tool left on a floor — are small, high-frequency, and often moving. They are the first thing the encoder throws away.

The result is a failure mode that does not look like a failure. The frame looks fine. The large objects are detected fine. Recall on small objects has dropped and nothing in the pipeline reports it.

![Two panels. The left plots recall against stream bitrate on a log scale, for three object sizes. Large objects reach their ceiling of 94% below 1 Mbps. Medium objects reach 89% by about 2 Mbps. Small objects climb much later, reaching 78% only above 8 Mbps. A dashed line at 2 Mbps marks what the installer left configured: there, large objects are at 93% and small objects at 42%. The right panel shows recall lost at 2 Mbps against the same model at 12 Mbps: 1 point for large objects, 6 for medium and 36 for small.](img:video-compression-and-detection-accuracy-bitrate-cliff.png "Simulated curves with the shape the post describes. Measure your own cliff; it moves with resolution, scene motion and object size.")

Read the dashed line. At the same bitrate, on the same stream, from the same model: large objects lose **1 point** and small objects lose **36**.

That is why this is hard to catch. Anyone checking the system looks at the frame, sees vehicles and nearby people boxed correctly, and concludes the stream is fine. The thing that broke is the thing nobody can verify by looking.

## The three settings that matter

**Bitrate** is the big one. Below some threshold, accuracy falls off a cliff rather than degrading smoothly. Above it, extra bits buy you nothing. The threshold depends on resolution, scene motion and object size, so the number for one site is not the number for another.

**Keyframe interval** matters more than people expect. Frames immediately after an I-frame are cleaner than frames at the end of a long GOP, where accumulated prediction error is at its worst. With a two-second interval at 25fps, you have up to 50 frames of drift before the next reset. If your analytics samples one frame per second, which frame within the GOP you happen to land on affects what you see.

**Rate control** decides how the encoder behaves when the scene gets busy. Constant bitrate holds the bitrate and lets quality collapse when a lorry drives through. Variable bitrate holds quality and lets the bitrate spike. For analytics, VBR with a sensible cap is usually the better trade, because the moments when the scene is busy are the moments you care about.

## Find your own cliff

Do not take anyone's recommended bitrate, including mine. Measure it.

The experiment is simple and takes an afternoon:

1. Capture a representative clip at the highest quality the camera will produce, including the hard cases — distant objects, fast motion, low light
2. Label it, or use a strong model's output on the high-quality version as your reference
3. Re-encode the same clip at a range of bitrates with `ffmpeg`
4. Run your production detector on each version and measure recall against the reference

Plot recall against bitrate. You get a curve that is flat and then falls off. Set your stream a comfortable margin above the knee, not at it, because real scenes are harder than your test clip.

Do this per camera type and per scene, not once for the whole site. A camera looking at an empty corridor and one looking at a loading bay have very different answers.

## The substream trap

Many deployments run analytics on the camera's substream to save bandwidth and decode cost. That is often the right call and it is also where accuracy quietly disappears.

A 640×360 substream at 512 kbps is fine for detecting a person at five metres and hopeless for detecting one at forty. If you sized the model's input resolution against the main stream and then pointed it at the substream, you have changed the problem without changing the configuration.

If you use the substream, measure on the substream. The comparison that matters is not "does the model work" but "does the model work on exactly the pixels it will receive in production".

## Decode is not free either

Worth noting alongside this: higher bitrates cost more than bandwidth. Decoding is real CPU or dedicated hardware, and on edge boxes it is frequently the actual bottleneck rather than inference.

That makes the bitrate decision a genuine trade-off rather than a pure quality question. More bits means better recall and fewer streams per box. Knowing where your accuracy cliff is tells you how far down you can push before the saving stops being worth it.

## What to check on an existing deployment

If you have inherited a system and want to know whether this is costing you:

- Ask the camera what it is actually sending, rather than what the configuration page claims. `ffprobe` on the stream will tell you the real bitrate, resolution and codec
- Check whether anyone changed it. Installers frequently reduce bitrate to fit a recorder's storage budget, without telling the analytics team
- Compare detection recall on a handful of frames captured from the live stream against the same scene captured at high quality

That last check takes an hour and occasionally explains a problem people have been attributing to the model for months.
