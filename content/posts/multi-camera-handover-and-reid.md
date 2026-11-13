---
title: "Following a Person Across Cameras: Handover and Re-ID"
description: "Tracking within one view is routine. Matching the same person across non-overlapping cameras is a different problem with different failure modes."
category: "Video Analytics"
date: 2026-11-25
tags: [tracking, re-identification, multi-camera, video-analytics]
---

Single-camera tracking is a solved-enough problem. ByteTrack or BoT-SORT on a decent detector will hold an identity across a view for as long as the person stays visible. Ask the same system "is the person who just walked into camera 4 the one who left camera 2 ninety seconds ago?" and it has nothing to say.

That is a different problem, and it is worth being clear about which one you are being asked to solve, because the cost difference is large.

## Two problems that look like one

**Overlapping cameras** share a field of view. A person is visible in both at the same moment, so you can match on geometry: project both detections to a common ground plane and see whether they land in the same place. This is reliable when you have calibration, and it mostly reduces to a surveying exercise.

**Non-overlapping cameras** have a gap. The person disappears from one view and appears in another some seconds later. There is no shared moment to match on, so you are matching on appearance, timing, and topology. This is much harder and the accuracy is much lower.

People asking for "tracking across the site" usually mean the second one and are imagining the reliability of the first.

## Appearance alone will disappoint you

Re-identification models embed a person crop into a vector and match by cosine distance. On academic benchmarks they do well. On a real site they are fighting several things at once.

Lighting changes between cameras, sometimes dramatically — daylight near an entrance, fluorescent inside, IR in a corridor. The same jacket is a different colour in each.

Viewpoint changes. A model that saw someone from the front has to match them from behind.

And the base rate works against you. In a shop with three people in it, picking the right match out of three is easy. In a warehouse with eighty people in similar high-visibility vests, appearance embeddings have very little to separate them, and that is exactly the environment where clients most want this.

Treat re-ID similarity as one piece of evidence, never as the decision.

## Use the building

The constraint that helps most is the one people forget: the person has to physically walk there.

Build a topology — which camera views connect to which, and the plausible transit time between them. A person leaving camera 2 heading east can appear in camera 4 or camera 5, in roughly 40 to 120 seconds on foot. They cannot appear in camera 9 at all without passing another view, and they cannot appear in camera 4 in three seconds.

This prunes the candidate set enormously before appearance matching runs. It converts an open-set problem into a small, time-bounded one, which is the single biggest accuracy gain available.

![Two panels. Left, two overlapping histograms of appearance similarity: wrong pairs peak around 0.33, true pairs around 0.72, with a wide overlap between them. A dashed threshold line at 0.62 leaves 29% of true pairs below it and 5% of wrong pairs above it. Right, a bar chart of how many matches are correct as the candidate pool shrinks: 7% against every person seen today, 200 of them, with 9.2 wrong candidates above the threshold; 21% after a time window cuts the pool to 60, with 2.7 wrong candidates; 56% after time and topology cut it to 12, with 0.5 wrong candidates.](img:multi-camera-handover-and-reid-overlap-and-gating.png "Simulated similarity scores, not a benchmark. The model, the embedding and the threshold are identical across all three bars. Only the number of people it is allowed to consider changes.")

The right-hand panel is the argument for all of this. The model does not change between those three bars. The threshold does not change. The only thing that changes is how many people the system is permitted to consider, and correct matches go from 7% to 56%. A better embedding moves the left-hand distributions slightly further apart; knowing which door someone walked out of removes most of the candidates outright.

It is also worth sitting with the fact that 56% is where that ends up. Even with topology, timing and a decent model, roughly two in five matches are wrong. That is the honest ceiling for non-overlapping re-ID on a busy site, and it is the number to put in front of a client before anyone builds anything.

You get the transit times by measuring them, not by estimating them. Walk it with a stopwatch, or mine them from a few days of recorded transitions.

## Score, then threshold, then decide what unmatched means

A workable matcher combines three terms: appearance distance, transit-time plausibility, and direction of travel consistency. Weight them, produce a score, and apply the Hungarian algorithm over the candidate pairs in a time window rather than greedily taking the best match.

Then make a deliberate choice about the threshold, because the two errors are not symmetric.

A **missed link** splits one person's journey into two tracks. Your dwell-time report says two visitors of five minutes each instead of one visitor of ten.

A **false link** merges two different people. Your report now contains a journey that nobody made, and if anyone acts on it, they are acting on fiction.

For analytics and reporting, bias hard towards missing links. An honest "we could not follow this person" is far better than a confident invention. Keep an explicit "unmatched" state and count it, rather than forcing every track to join something.

## What to measure

Within-camera tracking metrics do not tell you whether handover works. Measure it directly.

Walk a known route through the site several times and check whether the system produces one journey or several. Do it at different times of day, and with different numbers of other people present, because performance against an empty site tells you nothing about performance at shift change.

Report the handover accuracy separately from the detection and tracking accuracy. A system with excellent detection and 60% handover will produce confident, wrong journey analytics, and the headline numbers will hide it.

## When to say no

This is worth saying plainly, because it saves everyone money.

If the cameras do not overlap, the population is large, the clothing is uniform, and the client wants individual journeys rather than aggregate flows, the honest answer is that appearance-based re-ID will not give them what they are imagining. You can build it, and it will be wrong often enough that they stop trusting the output.

Often what they actually need is flow counts: how many people went from zone A to zone B, rather than which specific person did. That is a counting problem across a boundary, it is far more robust, and it answers the business question just as well.

Ask what decision the output will drive. If the answer is "we want to understand customer flow", aggregate counts will do it. If the answer is "we need to follow a specific individual", you are in a different and much more expensive conversation, and one worth having before the quote rather than after.
