---
title: "PTZ Cameras and Analytics: Why Your Zones Stop Working"
description: "A camera that moves breaks every assumption fixed-camera analytics makes. What survives, what does not, and how to handle presets."
category: "Video Analytics"
date: 2026-11-28
tags: [ptz, cameras, zones, calibration, video-analytics]
---

Fixed-camera analytics quietly assumes the camera does not move. Zones are drawn in image coordinates. Background models accumulate over time. Calibration maps pixels to the ground plane. Every one of those assumptions dies the moment someone grabs the joystick and pans to look at something.

PTZ cameras are common because they are useful to the humans watching. They are frequently also connected to analytics, because they are there. The two uses conflict, and it is better to design for that than to discover it.

## What breaks

**Zones.** A polygon drawn at one pan position covers something completely different at another. Intrusion alerts fire on the wrong area, or stop firing entirely. This is the most common and most confusing failure, because the detections still look correct.

![A schematic yard seen through a camera. At preset 1 a dashed intrusion zone sits over a gateway in a building, and a person walking into the gateway turns the zone red and raises an alert. The camera then pans right. At preset 2 the zone has stayed in the same place on screen, so it now covers open ground beside a fence while the gateway sits to its left. A person standing in that same gateway raises no alert, and the same person walking on to the empty ground inside the drifted zone raises one.](vid:ptz-zone-drift.mp4 "Schematic, not footage. The zone never moves on screen because it is stored in image coordinates. The scene moves underneath it.")

Watch what the zone does in that clip: nothing. It cannot move, because it is stored as image coordinates — a list of pixel positions in the frame. The scene slides underneath it. After the pan the gateway the zone was drawn around is still in shot, just to the left, and someone standing in it raises nothing. Walk a few metres further, onto open ground nobody cares about, and the system reports an intrusion.

Both failures are worse than a crash, because nothing looks wrong. The detector still boxes the person correctly, the alerts still arrive, and the log still fills up. Only the meaning is gone.

**Background subtraction.** Any method that accumulates a model of the static scene is invalidated by movement. The whole frame registers as foreground for several seconds after a move.

**Calibration.** Ground-plane projection depends on the camera's orientation. Pan, tilt or zoom and your metres become fiction. Dwell times and speeds derived from them are wrong in a way nothing reports.

**Tracking.** A fast pan looks to a tracker like every object in the scene teleporting simultaneously. Expect ID switches and lost tracks across every movement.

## What survives

Plain detection is fine. A detector does not care where the camera is pointing; it detects what is in the frame. Counting detections per frame, classification, and anything that does not depend on where an object is relative to the scene continues to work.

That is a useful boundary to hold on to: **anything frame-relative survives, anything scene-relative does not**.

## The preset approach, which is what usually works

Most PTZ cameras in practice do not move continuously. They sit at one of a handful of preset positions, and occasionally a human moves them.

That makes the tractable design: treat each preset as a separate virtual camera.

Define zones, calibration and background models per preset. Query the camera's current position over ONVIF, match it against the known presets, and load that preset's configuration. If the camera is somewhere that is not a known preset — because a guard is driving it manually — suspend scene-relative analytics and fall back to detection only.

The crucial part is the suspension. Running zone logic with the wrong zones is worse than running none, because it produces confident, wrong alerts that someone may act on.

## Detecting that it moved

You cannot always trust the camera to tell you. ONVIF position queries may be slow, may be unavailable, or may report the commanded position rather than the settled one.

A cheap, reliable backstop is to detect motion from the pixels. Compute a frame-to-frame global shift — phase correlation or sparse optical flow on corner features is enough — and treat a large global displacement as a camera move rather than a scene event.

When that trips: mark the stream as in-motion, suspend scene-relative analytics, and wait for a stable period before resuming. Resuming too early, while the camera is still settling or auto-focusing, produces a burst of nonsense.

## The settling problem

After a move, the image is not immediately usable. Autofocus hunts, auto-exposure adjusts, and the encoder has a keyframe to catch up on. For a second or two the frames are blurry, badly exposed, or heavily compressed.

Detections during this window are unreliable in both directions — missed objects and spurious ones. Discard them. A fixed delay after motion stops is crude and works; checking sharpness until it stabilises is better.

## Talking to the client about it

The conversation worth having early is who controls the camera.

If the security team needs to drive it manually, accept that analytics coverage will have gaps and say so explicitly in the specification. Gaps that were agreed in advance are a feature of the design. Gaps discovered afterwards are a defect.

Often the better answer is a fixed camera for the analytics and a PTZ alongside it for the humans. It is more hardware and it removes an entire category of problem. If the budget allows it, propose it — the cost of the second camera is usually less than the engineering cost of making PTZ analytics reliable.

If it does not allow it, the preset approach with explicit suspension is the honest middle ground. Just make sure the gaps are visible in whatever reporting the client sees, so that a quiet period reads as "camera was being driven" rather than "nothing happened".
