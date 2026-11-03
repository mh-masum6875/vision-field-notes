---
title: "Tracker ID Switches and Double Counting: Diagnosing Count Errors"
description: "When counts drift high or low, the tracker is often to blame. Why IDs switch, how a switch becomes a double count, and counting rules that tolerate it."
category: "Video Analytics"
date: 2026-11-19
tags: [tracking, counting, bytetrack, id-switch, video-analytics]
---

A people counter reports 1,340 entries for a day when the door staff are sure it was nearer 1,100. The detector finds people reliably. The problem is in what happens next: the tracker gives one person two IDs, and the counting rule counts each ID. Or it merges two people into one ID, and the count falls short.

This article explains why trackers switch IDs, how switches turn into count errors, how to measure them, and how to design counting rules that survive them. The basics of tracking are covered in [Object Tracking Explained: SORT, ByteTrack and Friends](post:object-tracking-bytetrack-explained); this article is about what goes wrong in production.

## What an ID switch is

A tracker links detections across frames into tracks, each with an ID. An ID switch happens when the same physical object ends up with a different ID, or when an ID moves from one object to another. Common forms:

- **Fragmentation:** a track is lost and the object reappears with a new ID.
- **Swap:** two objects cross, and their IDs exchange.
- **Merge:** two objects close together are followed as one track for a while.

For counting, fragmentation causes over-counting and merges cause under-counting. Swaps can do either, depending on the rule.

## Why IDs switch

### Occlusion longer than the tracker's memory

When a person passes behind a pillar, a shelf or another person, detections stop. The tracker keeps the lost track for a while, predicting where it should be, and re-links it if a matching detection appears in time. If the gap is longer than that memory, a new track starts. In many trackers the memory is set in frames (for example `track_buffer` in Ultralytics' ByteTrack configuration), so it also depends on the frame rate.

### Detection gaps

A detector that misses a person for several frames in a row, in shadow, at the edge of the frame, or at low confidence, creates the same effect as an occlusion. Better detection in those conditions reduces switches more than any tracker setting.

### Motion between frames

Trackers like SORT and ByteTrack match detections to tracks mainly by box overlap with the predicted position. If objects move far between analysed frames, because they are fast or because the analysis frame rate is low, predictions and detections stop overlapping and matching fails. See [How Many Frames per Second Does Your Analytics Need?](post:how-many-fps-does-analytics-need).

### Crowds

When people walk close together, boxes overlap heavily. Matching by overlap alone becomes ambiguous, and swaps and merges increase. Trackers that also use appearance features help, at a cost in compute.

### Frame-rate changes

If the camera drops its frame rate at night, frame-based tracker settings change meaning, and switches can increase at night without any other cause. See [When the Camera Changes Its Frame Rate at Night](post:variable-frame-rate-at-night).

## How a switch becomes a count error

![Two panels showing a person walking left to right past a counting line and then behind a pillar. Top: with a rule that counts every new ID seen past the line, the person is counted as ID 7 at the line and again as ID 12 when they reappear after the pillar. Bottom: with a rule that counts a track only when it crosses the line, plus a short window that re-links the reappearing person to ID 7, the person is counted once.](img:tracker-id-switches-and-double-counting-double-count.png "A constructed scenario, no tracker was run. The same ID switch causes a double count under one rule and no error under another.")

The counting rule determines how harmful a switch is. A rule that counts "new IDs that appear in an area" counts every fragment. A rule that counts "tracks that cross a line from one side to the other" only counts a fragment if the switch happens right at the line. So the first defence is the rule, not the tracker.

## Counting rules that tolerate switches

- **Count crossings, not appearances.** Require a track to be seen on one side of the line and then the other. A track that starts on the far side of the line does not count.
- **Count each ID at most once per direction,** and keep a short memory of recently counted IDs.
- **Require a stable track before counting.** Ignore tracks younger than a few frames or shorter than a minimum distance travelled; brief fragments are often noise.
- **Use a band, not a thin line.** Require the track to go from clearly before a band to clearly after it. Jitter around a single line no longer produces back-and-forth crossings.
- **Place the line well.** Put it where people are fully visible and not occluded, away from pillars and doorframes, and where people walk straight across rather than standing.
- **Use the bottom-centre of the box** (roughly the feet) for line and zone tests. It is more stable than the box centre and matches where people actually are on the floor.

[People Counting with Line Crossing](post:people-counting-line-crossing) shows the basic implementation; these refinements make it robust.

## Re-linking fragments

When a new track starts close in time and space to where an old track was lost, they are probably the same person. A simple re-link step joins them: if a track was lost within the last couple of seconds near this position, moving in a consistent direction, give the new track the old ID. Some trackers have this built in through a longer memory or appearance matching. Keep the window short, or you will start merging different people.

## Measure it

Count accuracy is easy to state and easy to measure:

1. Record a few hours at each counting location, at busy and quiet times, day and night.
2. Count manually from the video, ideally two people independently for the busiest periods.
3. Compare the system's count per time interval, for example per 15 minutes, with the manual count.
4. Look at the error by interval. Over-counting in busy periods points to fragmentation; under-counting in busy periods points to merges or missed detections.

For deeper analysis, label tracks on a short clip and compute standard multi-object tracking metrics, such as the number of ID switches and IDF1, which measures how consistently identities are kept. Tools exist for this, but for a counting system the interval comparison usually tells you enough. Keep these clips in your replay set; see [Building a Replay Set of Recorded Footage](post:building-a-replay-set).

## Fix in this order

1. Fix the counting rule: crossings, bands, stable tracks, good line placement.
2. Fix detection gaps in the problem areas: more data, better camera position, lighting.
3. Make tracker settings time-based and suited to the frame rate.
4. Raise the analysis frame rate for fast or crowded locations.
5. Add re-linking or an appearance-based tracker where occlusions are unavoidable.

## Checklist

- Know which switch type you have: fragmentation, swap or merge.
- Count line crossings with a band, not new IDs in an area.
- Require stable tracks and count each ID once per direction.
- Place lines away from occluders, using the bottom-centre of boxes.
- Re-link short fragments within a brief time and distance window.
- Scale tracker memory with the frame rate.
- Measure counts against manual counts per interval, day and night.

Next steps: [People Counting with Line Crossing: A Practical Tutorial](post:people-counting-line-crossing) and [Measuring Video Analytics by Events, Not Frames](post:evaluate-video-analytics-by-events).
