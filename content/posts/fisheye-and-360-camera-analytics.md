---
title: "Running Analytics on Fisheye and 360 Cameras"
description: "Detectors trained on rectilinear images do badly on fisheye footage. Dewarping, training on warped frames, and when each one is the right call."
category: "Video Analytics"
date: 2026-11-24
tags: [fisheye, cameras, dewarping, detection, deployment]
---

A single fisheye camera on a ceiling can cover a room that would otherwise take four. That is why they keep turning up in retail, warehouses and offices. Then you point a detector at one and the results fall apart: people near the edge are bent sideways, boxes are enormous and wrong, and the counting logic you spent a week on returns nonsense.

The problem is not the detector. It is that almost every public detection model was trained on rectilinear images, where straight lines in the world stay straight in the picture. A fisheye lens breaks that assumption on purpose, in exchange for a much wider field of view.

There are three practical ways to deal with it. They suit different situations and it is worth knowing which one you are choosing.

## Dewarp first, then detect

The obvious approach: convert the fisheye image into one or more flat views, then run a normal detector on those.

For a ceiling-mounted camera the usual output is either a single panoramic strip or four "virtual cameras" pointing north, south, east and west. OpenCV's `fisheye` module will do the remapping once you have calibration parameters, and most camera vendors expose dewarped streams directly over RTSP.

What makes this attractive is that everything downstream stays normal. Your detector, your tracker, your zone logic, your annotation tooling — all of it works on ordinary images.

The costs are real though. Dewarping is a per-frame remap, which is cheap on a GPU and not free on a CPU. Running four virtual views means four detector passes instead of one, so your compute goes up roughly fourfold. And the stitching seams between views are a genuine source of tracking failures: a person walking from the north view into the east view is, as far as your tracker is concerned, one track ending and another starting.

If you go this way, overlap the virtual views deliberately and handle the handover explicitly rather than hoping the tracker copes.

## Train on the warped frames

The second option is to leave the image alone and teach the model what a fisheye person looks like.

This works better than people expect. A detector is perfectly capable of learning that a person at the frame edge is a curved, radially-oriented blob, as long as you show it enough of them. What it cannot do is generalise there from rectilinear training data.

The catch is annotation. You need your own labelled fisheye data, from cameras mounted the way yours are mounted. A ceiling fisheye at three metres and a wall fisheye at two metres produce different distortion, and a model trained on one will not transfer cleanly to the other.

Axis-aligned boxes are also a poor fit for radially-oriented objects. A person standing at the edge of a ceiling fisheye occupies a box containing mostly floor. If your downstream logic cares about box area or overlap, that matters. Rotated boxes or segmentation masks fit the geometry much better, at the cost of a more expensive model and more expensive labelling.

## Detect on the warped frame, reason in world coordinates

The third approach is a hybrid, and for counting and zone work it is often the best of the three.

Detect on the raw fisheye frame with a model trained for it, then project each detection's ground contact point through the calibration into floor coordinates. Do all your zone logic, distance measurement and tracking in that floor plane rather than in image space.

This is more work up front: you need the camera intrinsics and the mounting height, and you need to be honest about the fact that the ground-point assumption fails for anything not standing on the floor. But once it works, your zones are drawn on a floor plan rather than a distorted image, distances are in metres, and a person walking across the room moves in a straight line in your coordinate system instead of an arc.

For dwell time, occupancy and line crossing, reasoning on the floor plane removes a whole class of bugs that come from treating image pixels as if they were evenly spaced in the world.

## Choosing between them

Dewarping is the right call when you are integrating with something that expects normal images, when you have GPU headroom, and when you do not have labelled fisheye data. It gets you working quickly.

Training on warped frames is right when compute is tight, when you own the annotation pipeline, and when the camera geometry is consistent across the deployment.

The floor-plane hybrid is right when the analytics are spatial — occupancy, zones, distances — and when you can get calibration. It is the most work and the most robust.

## Things that catch people out

**Vendor dewarping is not free and not always good.** Some cameras do the remap on-board and hand you a clean panorama. Check what it costs in latency and whether the seam position is configurable, because a seam through the middle of a doorway will ruin counting.

**Calibration drifts.** A camera that gets knocked, or a mount that sags, invalidates your floor-plane projection silently. The detections still look fine; the metres are just wrong. Worth a periodic check against a known reference point.

**The centre is not the same as the edge.** Resolution per square metre of floor is far higher directly under a ceiling fisheye than at the periphery. A detector that works well in the middle of the frame may miss small objects at the edge simply because they occupy fewer pixels. Measure recall by radial zone, not just overall, or you will ship something that quietly fails around the walls.

**Test with the mount you will ship.** Distortion depends on the lens and the height. Footage from a tripod at eye level tells you very little about what a ceiling mount will do.

## Where to start

If you are evaluating whether a fisheye deployment is viable at all, dewarp into four views and run your existing detector. It will be slower than the final system and good enough to answer the question.

If the answer is yes and the project is going ahead, the floor-plane approach is usually where it ends up, because the analytics people actually want are spatial.
