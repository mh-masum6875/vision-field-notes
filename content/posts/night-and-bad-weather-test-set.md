---
title: "Building a Night and Bad-Weather Test Set"
description: "Average scores hide night, rain and glare. How to collect, label and use a dedicated test set for hard conditions so weaknesses show early."
category: "Datasets and Training"
date: 2026-11-20
tags: [test-set, night, weather, evaluation, datasets]
---

Most test sets are dominated by daytime footage in good weather, because that is what is easiest to collect and label. A model can score well on such a set and still be weak for the many hours a day the cameras spend in infrared night mode, in rain or in low sun. The overall number averages the weakness away.

A dedicated test set for hard conditions makes the weakness visible and measurable. This article covers what to put in one, how to collect it, how to label it, and how to use it.

## Why a separate set

Two reasons.

**Visibility.** If night images are 10% of your test set, a large drop in night performance moves the overall score by a small amount. On a separate night set, the same drop is the headline.

**Stability.** Hard conditions vary a lot, so you need enough examples of each to get a number that does not jump around between versions. A dedicated set lets you collect enough without distorting the main test set's proportions.

Keep the main test set representative of reality, and report the hard-conditions set alongside it, not merged into it. See [Why Your Test Set Flatters You](post:why-your-test-set-flatters-you).

## What to include

Start from the conditions your sites actually have, not a generic list:

- **Night with infrared.** Monochrome images, illuminator fall-off, overexposed near objects. See [Day/Night Switching](post:day-night-switching-ir-cut-filter).
- **Night with artificial light.** Colour images with strong shadows, light pools and sodium or LED colour casts.
- **Dusk and dawn.** Mode switches and mixed light.
- **Rain.** Drops on the lens, reflections on wet ground, umbrellas and rain gear changing people's shapes.
- **Fog, haze or smoke,** where relevant.
- **Low sun and glare.** Long shadows, lens flare, people silhouetted against bright doorways.
- **Headlights and flashing beacons** at night.
- **Heat shimmer** on long outdoor views in hot climates.
- **Dirty or wet lenses,** if they occur in practice. See [Detecting a Dirty, Blocked or Moved Camera](post:detect-dirty-blocked-moved-camera).

Tag every image with its conditions. One image can be "night, IR, rain". The tags are what let you report results per condition.

## Collecting it

Hard conditions are, by nature, not always available. Some practical ways:

- **Record continuously for a period and select later.** Weather is unpredictable; recordings let you pick the rainy hours afterwards.
- **Ask the site.** Staff know when the low sun hits the loading bay and which nights the yard floods.
- **Use more than one season** where seasons differ. A set collected in one month misses the others.
- **Stage what you can.** People walking through the area at night at agreed times gives you labelled events in exactly the conditions you need.
- **Cover several cameras.** Night performance differs a lot between cameras with different illuminators and lenses.

Keep these images out of training data. If you also want hard-condition data for training, collect it from different days or cameras, so the test set stays independent.

## How many images

Enough per condition to make the result meaningful. As a rough guide, aim for at least a few hundred labelled objects per condition you report separately, more for rare classes. With fewer, the per-condition numbers are noisy; see [Comparing Two Detectors Fairly](post:comparing-two-detectors-fairly) for how noisy.

If some conditions are hard to collect in quantity, report them anyway with their counts, and treat the numbers as indicative.

## Labelling hard images

Hard images are hard for labellers too. Expect:

- More uncertain objects. Use ignore regions for objects nobody can identify confidently, rather than forcing a guess.
- More disagreement between labellers. Double-label a sample and resolve differences, especially for the test set. See [Measuring Label Quality with Annotator Agreement](post:measuring-label-quality-annotator-agreement).
- More time per image. Budget for it.

Labellers should work on the image at full resolution, with the brightness adjusted for viewing if the tool allows it, but labels must be drawn on the original image the model will see.

## Using it

Report, for every model version:

| Condition | Images | Objects | Recall at operating threshold | False positives per image |
|---|---:|---:|---:|---:|
| Day, clear | ... | ... | ... | ... |
| Night, IR | ... | ... | ... | ... |
| Rain | ... | ... | ... | ... |
| Low sun | ... | ... | ... | ... |

Then use the table to decide:

- **Where to collect training data next.** The weakest condition with a meaningful share of operating hours is usually the best investment.
- **Whether per-condition settings are justified,** such as a different threshold in night mode. See [Why a Detector's Confidence Is Not a Probability](post:detector-confidence-is-not-a-probability).
- **What to tell the client.** If night recall at the far end is weak, say so, with the number. See [Writing a Results Report a Non-Technical Client Will Read](post:writing-results-reports-for-clients).
- **Whether a camera or lighting change would help more** than model work.

Also run the event-level replay set in the same conditions, since temporal filtering can hide or amplify frame-level weaknesses. See [Building a Replay Set of Recorded Footage](post:building-a-replay-set).

## Keep it current

Add new hard conditions as you meet them: a new site with fog, a camera with a new illuminator, a client complaint about a particular weather pattern. Version the set and report results only on matching versions. See [Versioning Datasets and Models Together](post:versioning-datasets-and-models).

## Checklist

- Separate hard-conditions set, reported alongside the main test set.
- Conditions chosen from your real sites, tagged per image.
- Collected over time and seasons, from several cameras, with staged events where needed.
- Independent of training data.
- Enough labelled objects per reported condition.
- Ignore regions and double-labelling for uncertain cases.
- Results reported per condition, with counts.
- Used to direct data collection, settings and client communication.

Next steps: [Day/Night Switching: Why Detections Change When the IR Filter Flips](post:day-night-switching-ir-cut-filter) and [Data Augmentation for Object Detection](post:data-augmentation-for-detection).
