---
title: "Debug Overlays That Actually Help"
description: "A good overlay on the video answers 'why did it alert?' at a glance. What to draw: track IDs, rule state, below-threshold boxes, zones and a status bar."
category: "Tools and Workflow"
date: 2026-12-01
tags: [debugging, visualisation, opencv, video-analytics, workflow]
---

When an alert looks wrong, the first thing anyone does is watch the video. If the video shows only boxes and class names, the question "why did it alert?" stays unanswered: was it the detector, the tracker, the zone, the timer or the schedule? A well-designed debug overlay puts the whole decision on the screen, so the answer takes seconds instead of an afternoon in the logs.

This article describes what to draw on a debug overlay, how to keep it readable, and how to use it without slowing down production.

## What a debug overlay is for

The overlay is not the product. Clients rarely need to see it. It is a tool for engineers and, sometimes, for trained operators investigating an alert. Its job is to show the pipeline's state at each frame:

- What the detector saw, including what it nearly saw.
- How the tracker linked detections over time.
- What each rule thought about each track.
- The state of the system: time, frame rates, model and configuration versions.

![A synthetic warehouse frame with a status bar at the top showing camera, local time with offset, model and threshold version, input and processed frame rates, latency and night mode. A shaded loading-bay zone is labelled with its active hours. A person inside the zone has a red box labelled track 7, person 0.81, with a note in zone 12.4 seconds of 10, alert sent. A person outside the zone has a green box labelled track 3. A dashed yellow box labelled person 0.31 is marked below threshold 0.45.](img:debug-overlays-that-help-overlay.png "A synthetic frame with made-up values. Everything needed to explain the alert is on screen: the track, its score, its time in the zone against the rule, the zone's schedule, and the versions in use.")

## What to draw

### Detections, with what matters about them

- Box, class and confidence for detections above the threshold.
- **Detections just below the threshold**, drawn differently (dashed, faded). These explain most "why didn't it alert?" questions: the object was seen, just not confidently enough.
- Track ID on each box, so you can follow an object across frames and spot ID switches. See [Tracker ID Switches and Double Counting](post:tracker-id-switches-and-double-counting).

### Rule state

This is the part most overlays leave out, and the most useful:

- Zones and lines, with names and whether each is currently active (schedules).
- For each track in a zone: time in zone against the rule's threshold, for example "12.4 s / 10 s".
- Filter state, such as "detected 4 of last 8" for an N-of-M filter.
- Cooldown state: "alerted 47 s ago, cooldown 120 s".
- A clear marker on the frame where an alert was sent.

With rule state visible, you can see whether an alert came from a real long stay, a flickering detection that just met the filter, or a zone that should have been inactive.

### A status bar

One line at the top or bottom of the frame:

- Camera ID and local time with time zone. See [Alerts at the Wrong Time of Day](post:alerts-at-the-wrong-time-of-day).
- Model version and threshold version.
- Frames received per second and frames processed per second.
- Inference latency.
- Day or night mode, and any health warnings.

When a screenshot of the overlay is attached to a bug report, the status bar alone answers half the questions.

## Keep it readable

- **Colour by meaning, consistently.** One colour for "alerting", one for "tracked, not alerting", one for "below threshold". Do not colour by class unless class is the point.
- **Scale text with the frame.** Text that is readable on 1080p is unreadable on 4K and huge on 360p. Compute font size from frame height.
- **Put labels where they do not cover the object,** usually above the box, and keep them inside the frame.
- **Use translucent fills** for zones so the scene stays visible.
- **Let people toggle layers.** A busy scene with every layer on is unreadable. Switches for below-threshold boxes, track trails and rule details help.
- **Draw track trails sparingly.** A short trail of recent bottom-centre positions shows direction and jitter; long trails clutter.

## Make it cheap or optional

Drawing on every frame costs CPU time, and encoding annotated video for viewing costs more. In production:

- Draw only when someone is watching, or for frames around alerts.
- Draw on the downscaled frame used for viewing, not on full-resolution frames.
- Keep drawing out of the main processing loop, for example in a viewer process that receives detections and rule state as data. See [Profiling a Python Vision Pipeline](post:profiling-a-python-vision-pipeline).

A good pattern is to log the per-frame data (boxes, IDs, scores, rule states) for a window around every alert, and render the overlay later, on demand, from the recording plus that log. The live pipeline stays fast, and every alert can still be replayed with full explanation.

## Use it in reviews

The overlay makes several routine tasks faster:

- **Alert reviews.** Operators marking alerts true or false can see why each one fired. See [Hard Negative Mining from Production Footage](post:hard-negative-mining-from-production).
- **Threshold tuning.** Below-threshold boxes show how many real objects a lower threshold would catch, and what else it would let in. See [Confidence Thresholds](post:confidence-threshold-tuning).
- **Zone checks after a camera moves.** Zones drawn on the live view show immediately whether they still fit.
- **Replay comparisons.** Rendering the same clip with two model versions side by side makes differences obvious. See [Building a Replay Set of Recorded Footage](post:building-a-replay-set).

## Privacy

Annotated recordings are still recordings of people. Apply the same access and retention rules as to the original footage, and blur faces in screenshots shared outside the team. See [Privacy and Ethics in Camera Analytics](post:privacy-and-ethics-camera-analytics).

## Checklist

- Boxes with class, confidence and track ID.
- Below-threshold detections drawn distinctly.
- Zones and lines with names and active state.
- Rule state per track: timers, filter counts, cooldowns, alert markers.
- A status bar with camera, local time, versions, frame rates, latency and mode.
- Consistent colours, scaled text, translucent zones, toggleable layers.
- Rendering kept out of the main loop; per-frame data logged around alerts.
- Same privacy rules as for raw footage.

Next steps: [OpenCV Essentials Every Computer Vision Engineer Needs](post:opencv-essentials-for-cv-engineers) and [Designing Alert Rules: Schedules, Cooldowns and Escalation](post:designing-alert-rules).
