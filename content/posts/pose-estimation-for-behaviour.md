---
title: "Using Pose Estimation for Behaviour, Not Just Keypoints"
description: "Keypoints are easy to get and hard to turn into reliable behaviour alerts. What works between the skeleton and the alert."
category: "Video Analytics"
date: 2026-11-27
tags: [pose-estimation, keypoints, behaviour, alerts, video-analytics]
---

Running a pose model is straightforward. YOLO-pose or similar gives you seventeen keypoints per person at a usable frame rate on modest hardware. Turning those keypoints into "this person fell over" or "this person is not wearing their harness correctly" is where the work actually is, and it is mostly not machine learning.

## Keypoints are noisy in ways that matter

Before building anything on top of a skeleton, look at the raw output on your own footage for a few minutes. Three things will be obvious.

Keypoints jitter frame to frame even when the person is still. Occluded joints are guessed, confidently and often wrongly — a hand behind a back gets placed somewhere plausible rather than marked absent. And left and right limbs swap, especially when someone turns.

Every one of these breaks naive rules. "Alert when the wrist is above the shoulder" will fire constantly on jitter alone.

## Use the confidences, do not just read the coordinates

Pose models output a confidence per keypoint, and most people ignore it.

That field is the difference between "the elbow is at this position" and "the model has no idea where the elbow is and has guessed". If your rule depends on a joint, check its confidence first and refuse to decide when it is low. An honest "cannot determine" is far better than a confident alert built on an invented coordinate.

This alone removes a large fraction of false alarms in occluded environments, which is most real environments.

## Normalise before comparing anything

Raw pixel coordinates are nearly useless for comparison. A person near the camera has a skeleton ten times the size of one at the back of the room, and the same posture produces completely different numbers.

Normalise by something that scales with the person: torso length, or the bounding box diagonal. Work in ratios and angles rather than pixels. The angle between the torso and the vertical is comparable across the frame; the y-coordinate of the hip is not.

If the camera has significant perspective — a wall-mounted camera looking down a corridor — consider projecting to a ground plane first, as the same posture at different distances will otherwise look different even after scale normalisation.

## Angles and ratios beat coordinates

Most useful behaviour rules reduce to a handful of derived quantities:

- **Torso angle from vertical** — the core of fall detection and posture work
- **Ratio of bounding box width to height** — a crude but robust proxy for lying down versus standing
- **Angle at a joint** — elbow, knee, hip, for reach and squat detection
- **Distance between keypoints, normalised** — hand to head for phone use, hand to hand for carrying

These are stable under the noise that breaks coordinate rules, and they are explainable to a client, which matters when someone asks why an alert fired.

## Nothing instant is reliable

A single frame is never enough. Not for falls, not for posture, not for anything.

A fall is not "torso angle exceeded 60 degrees". It is a rapid change in torso angle followed by the person remaining near the floor for several seconds. The second half is what separates a fall from sitting down quickly, bending to pick something up, or a keypoint glitch.

Build an N-of-M requirement into every rule: the condition must hold for at least N of the last M frames. This single pattern removes most false positives and costs nothing. Tune N and M on real footage rather than guessing — too short and jitter gets through, too long and you miss short events.

## When to stop writing rules and train a classifier

Hand-written rules work well for behaviours with clear geometric definitions: lying down, arms raised, crouching, reaching into a zone.

They work badly for behaviours people describe but cannot define: "acting suspiciously", "working unsafely", "struggling with the load". If you find yourself adding a fifth condition to a rule and it still misfires, that is the signal.

The alternative is a small temporal classifier over a window of normalised keypoints. A modest network over a few seconds of skeleton sequence learns things that are tedious to express as rules. The cost is that you now need labelled examples of the behaviour, which for rare safety events is exactly what you do not have — which is often why the rule-based approach was chosen in the first place.

Be honest about that loop rather than discovering it halfway through.

## Privacy, which is a real advantage here

Pose estimation has a genuine deployment benefit worth raising with clients: the skeleton can be stored and processed without the image.

If the behaviour analytics run on keypoints, you can discard the frames and keep coordinate streams, which are far less sensitive. In workplaces, healthcare and anywhere with a works council, that difference is sometimes what makes a project approvable at all.

It is worth designing for from the start rather than retrofitting, because it affects where in the pipeline you drop the pixels.
