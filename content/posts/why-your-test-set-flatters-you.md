---
title: "Why Your Test Set Flatters You"
description: "Test scores often come out higher than live performance. The usual causes are leakage, selective sampling, missing empty frames and a reused test set."
category: "Datasets and Training"
date: 2026-10-31
tags: [evaluation, test-set, data-leakage, datasets]
---

A model scores well on the test set, goes live, and does noticeably worse. Usually nobody cheated. The test set was simply easier, or more familiar, than the cameras the model now faces. The score was honest about the test set and misleading about everything else.

This article lists the common ways a test set flatters a model, roughly in order of how much they matter, and what to do about each.

## 1. The test set has seen the training set

The best-known cause is leakage between training and test data. With video it is almost automatic: neighbouring frames are near-copies, so a random split puts a frame in the test set whose twin, one second earlier, is in the training set. The model is tested on what it memorised. [Train/Validation Split for Video Frames](post:train-val-test-split-video-frames) covers this in detail.

Splitting by clip is better than splitting by frame, but leakage is wider than that. If a camera appears in both training and test data, the model has learned that camera's background, lighting and mounting angle. It will do better on it than on a new camera, even if no frame is shared. The same applies to a site, a shift or a week of weather.

![Two grids of days for four cameras over eight weeks. Top, random split by day: test days are scattered between training days on every camera. Bottom: camera 4 is held out entirely and the last week of the other cameras is held out as test.](img:why-your-test-set-flatters-you-split-schematic.png "Schematic. In a random split, every test day has training days on each side from the same camera. Holding out a whole camera and the most recent week tests what the model will face: a new view and a later time.")

Decide what "new" means for your deployment and hold out on that axis:

- **New cameras at known sites:** hold out whole cameras.
- **New sites:** hold out whole sites.
- **The same cameras, running into the future:** hold out the most recent period, and train only on earlier data.

You can do more than one. A test set that holds out one camera and the last two weeks of the others answers two questions at once.

## 2. Someone picked the frames

People who extract frames for labelling tend to pick clear, interesting ones: a person in full view, a vehicle in good light, an event actually happening. They skip blurred frames, crowded frames where boxes would be tedious, and frames where they are not sure what they are looking at.

The result is a test set that is cleaner than reality. The hard cases the model will meet most often are exactly the ones underrepresented.

The fix is to sample test frames by rule, not by eye. Take frames at fixed intervals or at random times across the full period, label every one of them, and keep the ambiguous ones with a clear policy (label them, or mark them as ignore regions). Selection by hand is fine for building a training set. It is not fine for measuring.

## 3. There are no empty frames

Many datasets contain only frames with at least one object, because empty frames take effort to collect and add nothing to the labelling count. But a live camera spends much of its time watching an empty scene, and empty scenes are where false positives appear.

A test set without background frames cannot measure false alarms on empty scenes at all. Its precision figure only covers frames where objects were present. Add a realistic share of empty frames from the same cameras and times, and report false positives per hour or per thousand empty frames as well as precision.

## 4. Conditions are in the wrong proportions

If 90% of your test images are daytime and production is half night, the overall score is mostly a daytime score. The same goes for rain, glare, crowding, and unusual camera angles.

Two things help. First, report results per condition, not only in total: day, night, rain, crowded, by camera. A weak condition then shows up even when it is a small slice of the test set. Second, if a condition matters more than its share of the test set, build a dedicated test set for it; [a night and bad-weather test set](post:night-and-bad-weather-test-set) is the usual first one.

## 5. The same people labelled everything

When the same team, with the same habits, labels both training and test data, the model learns those habits and the test set rewards them. A model can score well by reproducing a labeller's quirks, such as always including a carried bag in the person box, or never labelling people who are more than half occluded.

This is mostly harmless until someone else's labels or someone else's definition of the target appears, for example the client's own review of alerts. Write down the labelling rules (see [writing an annotation guide labellers can follow](post:annotation-guide-labellers-can-follow)) and, for important test sets, have a second person review a sample.

## 6. The test set was used too often

Every time you look at the test score and change something, the test set becomes a little more like a validation set. After dozens of rounds of "try, check test score, keep it if it improved", the chosen model is partly fitted to the test set's quirks, and the score is optimistic. This is sometimes called adaptive overfitting.

The discipline is simple and hard to keep:

- Use a validation set for all tuning decisions: epochs, augmentations, thresholds, model choice.
- Keep the test set for a final check, ideally once per release.
- Do not tune confidence thresholds on the test set. Tune them on validation data and confirm on the test set.

If a test set has been used heavily, retire it into the validation pool and collect a new one.

## 7. Time has moved on

A test set collected in one month represents that month. Seasons change light angles and vegetation. Sites change: new racks, a repainted floor, a new uniform, more people after a hiring round. A test set that was perfect in March is out of date by September.

Collect a small fresh test set regularly, from current footage, and compare the score with the original. A drop is information: either the world changed or the original test set was flattering, and both are worth knowing.

## A cheaper reality check: shadow mode

The most honest test is the deployment itself. Before switching alerts on, run the model in shadow mode for a week or two: it processes live footage and logs what it would have alerted on, but nobody is notified. Then review a sample of the logged events and a sample of random clips for missed events.

This catches everything above at once, at the cost of some review time. When shadow-mode results are clearly worse than test results, look for the gap in the list above before blaming the model.

## Checklist

- Hold out data along the axis that will be new: camera, site or time.
- Sample test frames by rule across the full period, not by hand.
- Include empty frames and count false positives on them.
- Report results per condition and per camera.
- Write down labelling rules and review a sample of test labels.
- Tune on validation data; touch the test set rarely.
- Refresh the test set as the sites change.
- Run a shadow-mode period before going live.

Next steps: [Building a Night and Bad-Weather Test Set](post:night-and-bad-weather-test-set) and [What mAP Hides](post:what-map-hides).
