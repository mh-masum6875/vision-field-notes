---
title: "Agreeing a Measurable Target with a Client Before You Start"
description: "Turn 'it should work well' into a written acceptance test: what counts as an event, which footage, who labels it and what result counts as a pass."
category: "Career and Freelancing"
date: 2026-11-01
tags: [clients, acceptance-testing, scoping, freelancing, metrics]
---

Most disputes on computer vision projects are not about whether the model is good. They are about what "good" meant. The client expected one thing, the engineer measured another, and nobody wrote either down. Weeks later both sides are right and the project is stuck.

The cure is to agree a measurable target before the work starts. This article shows what such a target needs to contain, why each part matters, and how to keep it realistic. It is not legal advice; how you put it into a contract depends on your situation.

## "95% accuracy" is not a target

Clients often ask for a percentage, and the most common one is "95% accuracy". It sounds precise, but it leaves almost everything open:

- 95% of what? Frames, objects, events, days?
- Is it precision, recall, or something else?
- Measured on which footage, recorded when?
- Who decides what the correct answer was?
- What about the cases nobody could judge, such as a person mostly hidden behind a pillar?

A target that leaves these open will be interpreted differently by each side when it matters. So the job is to close them, one by one.

## What a usable target contains

A target that can be tested has these parts.

**1. The event.** Describe what the system must detect, in plain language, with edge cases. "A person enters the marked loading-bay zone while the forklift warning light is on. Entering means both feet inside the zone line. People inside a vehicle do not count."

**2. The unit and the metric.** For alerting systems, count events, not frames. Usually two numbers matter:

- **Event recall:** the share of real events that produced an alert within an agreed time.
- **False alerts:** the number of alerts with no real event, per camera per day (or per hour of footage).

Precision as a percentage is less useful than false alerts per day, because operators feel the daily number. See [Measuring Video Analytics by Events, Not Frames](post:evaluate-video-analytics-by-events) for how to score this.

**3. Time limits.** How quickly after the event must the alert arrive to count? Five seconds? Thirty? An alert two minutes late may be useless for safety and fine for reporting.

**4. The test footage.** Which cameras, how many hours, recorded when, covering which conditions. Include night if the system runs at night. Agree it is footage the model has not been trained on. Agree who records it and how it is handed over.

**5. Ground truth.** Who decides what really happened in the footage, and how disagreements are settled. Often the client's staff label events, or the engineer labels and the client reviews a sample. Write down the definition of an event used for labelling, the same one as in point 1.

**6. Exclusions.** Cases that do not count against the system, agreed in advance: objects smaller than a stated number of pixels, people more than a stated fraction occluded, footage during camera faults. Exclusions must be defined before testing, not argued about afterwards.

**7. The pass mark.** For example: "At least 90% event recall and no more than two false alerts per camera per day on the agreed test footage."

**8. What happens otherwise.** If the system misses the mark: an agreed further iteration period, a revised scope, or a stop. Agreeing this when everyone is still friendly is much easier than later.

## Keep the numbers honest

Two traps catch people when setting the pass mark.

### Small test sets cannot prove high numbers

If the test footage contains 20 real events, each one is 5% of event recall. One miss takes you from 100% to 95%. A pass mark of 95% on 20 events means "at most one miss", which is a coin toss for a good system.

And even a perfect result proves less than it seems. With zero misses in *n* events, the upper bound of a 95% confidence interval on the miss rate is about 3/*n* (the "rule of three").

![Line chart of the miss rate that cannot be ruled out, against the number of real events in the test, when zero misses are observed. The exact bound and the rule of three, 3 divided by n, nearly coincide. With 20 events the bound is 13.9%, with 50 it is 5.8%, with 100 it is 3.0% and with 200 it is 1.5%.](img:agree-a-measurable-target-with-a-client-rule-of-three.png "Pure arithmetic, not data. Even if the system catches every event in a test of 20, a true miss rate of up to about 14% is still consistent with that result at 95% confidence.")

So either collect enough events to support the number you want to claim, or set a pass mark the test can actually distinguish. For rare events, this often means staging some: asking staff to walk into the zone at agreed times, across lighting conditions. Staged events are less natural than real ones, so mix both if you can.

### Do not promise numbers before seeing footage

A target agreed before anyone has looked at the client's cameras is a guess. Put a short paid discovery phase first: review sample footage, run a baseline model, and only then agree the pass mark. [Freelancing in Computer Vision](post:freelancing-in-computer-vision) describes this phase structure, and [When the Customer's Footage Doesn't Match the Demo](post:customer-footage-does-not-match-the-demo) covers what to do when the footage turns out to be harder than expected.

## A short example

Here is what a written target can look like. The numbers are placeholders to show the form, not a recommendation:

> **Event:** a person inside the loading-bay zone (both feet past the painted line) while the warning light is on.
> **Test footage:** 48 hours from cameras 3 and 7, recorded after model training, including two nights. At least 40 real or staged events.
> **Ground truth:** events labelled by the site supervisor from the footage using the event definition above; the engineer reviews and both agree the final list before scoring.
> **Counts as detected:** an alert within 10 seconds of the start of the event.
> **Excluded:** events where the person is less than 40 pixels tall, or during a recorded camera fault.
> **Pass:** event recall of at least 90% and at most 2 false alerts per camera per 24 hours.
> **If not passed:** one further two-week tuning round, then re-test on new footage; if still not passed, the project stops after the discovery and prototype phases.

It fits on half a page. It removes most of the arguments that would otherwise come later.

## Benefits beyond avoiding disputes

A written target also helps you do the work:

- It tells you which metric to optimise, so you stop arguing with yourself over mAP50 versus mAP50-95.
- It forces the client to decide what matters, which often reveals that the real problem is narrower and easier than the first description.
- It gives you a natural end point. Without one, projects drift into endless tuning.

## Checklist

- Define the event in words, with edge cases.
- Count events, with recall and false alerts per camera per day.
- Agree the time limit for an alert to count.
- Agree the test footage, its conditions and that it is unseen.
- Agree who labels ground truth and how disagreements are settled.
- Agree exclusions before testing.
- Make sure the test has enough events to support the pass mark.
- Write down what happens if the mark is missed.

Next steps: [Running a Pilot Deployment: Scope, Duration and Exit Criteria](post:running-a-pilot-deployment) and [Handover Documentation for a Computer Vision System](post:handover-documentation-for-cv-systems).
