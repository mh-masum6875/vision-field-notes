---
title: "Running a Pilot Deployment: Scope, Duration and Exit Criteria"
description: "A pilot answers one question cheaply: will this work here, for these people? How to scope it, run shadow mode and decide go, fix or stop."
category: "Career and Freelancing"
date: 2026-12-11
tags: [pilot, deployment, clients, evaluation, project-management]
---

Between a promising prototype and a full rollout sits the pilot: a real deployment, on real cameras, used by real people, at a small scale. Done well, it answers whether the system works on this site for these users before the client pays for everything. Done badly, it drifts on for months as a free trial that nobody owns, and ends without a decision.

This article covers how to design a pilot that ends in a clear decision: what to include, how long to run it, how to run shadow mode and live mode, and how to write exit criteria.

## What a pilot is for

A pilot answers questions that a test on recorded footage cannot:

- Does the system hold up over weeks of real conditions, including nights, weather and busy days?
- Do alerts arrive in time, in the right place, to the right people?
- Do operators find the alerts useful, and do they act on them?
- Are false alerts at a level people will tolerate?
- Does the hardware run reliably in its real location?

It is not the place to discover whether the model can detect the objects at all. That belongs in discovery and prototype phases. See [Freelancing in Computer Vision](post:freelancing-in-computer-vision).

## Scope

Keep it small and representative:

- **A few cameras,** chosen to cover the typical views and at least one difficult one, not only the easiest.
- **A small group of users,** trained, with a named person on the client side who owns the pilot.
- **The real alert path,** into the systems people will actually use.
- **A fixed set of rules,** agreed in advance, with changes during the pilot recorded.

Write down what is out of scope: other cameras, other rules, integrations that come later.

## Stages

![Four boxes in a row. Install and check, about a week: streams, health, time, settings. Shadow mode, one to two weeks: alerts logged, not sent; reviewed daily. Live with a small group, two to four weeks: alerts to trained users, feedback on each. Decide: against the agreed exit criteria. A note says go means roll out, fix means change and repeat the last stage, and stop means the pilot did its job by answering the question cheaply.](img:running-a-pilot-deployment-stages.png "Example durations, not a rule. Each stage ends in a decision, so a pilot cannot drift on without one.")

### 1. Install and check

Install the hardware, connect the streams, and check the basics before anything else: frames arriving at the expected rate, clocks synchronised, health checks working, zones drawn on the real views, alerts reaching a test recipient. Problems found here are infrastructure problems, and they are cheaper to fix before anyone judges the analytics.

### 2. Shadow mode

Run the system fully but send no alerts to users. Log every alert it would have sent, with snapshots. Review them daily at first:

- What share were real events?
- What caused the false ones? Sort them into groups. See [Reducing False Alarms in Production Video Analytics](post:reduce-false-alarms-in-production).
- Were any real events missed? Check by reviewing sample clips and asking site staff.

Tune thresholds, masks and rules during this stage, and record each change. Shadow mode is the safest place to find out that the camera facing the car park produces fifty headlight alerts a night.

### 3. Live with a small group

Send alerts to the trained users. Give them a quick way to mark each alert as useful, false, or real but not useful. That third category matters: an alert can be correct and still not worth sending.

Track, per week: alerts per camera per day, the share marked false, the share acted on, missed events found, and time from event to alert. Hold a short weekly review with the client's pilot owner.

### 4. Decide

At the agreed end date, compare results with the exit criteria and make one of three decisions:

- **Go:** roll out, with the settings and lessons from the pilot.
- **Fix:** specific changes, then repeat the live stage for a defined period.
- **Stop:** the system does not meet the need here. A pilot that ends in "stop" after a few weeks has saved the client the cost of a full rollout. That is a success for the process, if not for the product.

## Exit criteria

Agree them before the pilot starts, in writing. Examples of the form, with placeholder numbers:

- Event recall of at least an agreed level on staged and logged real events across the pilot period.
- No more than an agreed number of false alerts per camera per day, averaged over the final two weeks.
- At least an agreed share of alerts rated useful by the users.
- Alert delivery within an agreed time in the large majority of cases.
- System availability over the period above an agreed level, with any downtime explained.

Use the same definitions as your acceptance tests; see [Agreeing a Measurable Target with a Client](post:agree-a-measurable-target-with-a-client). Include at least one user-facing criterion. A system that meets every technical number but that operators ignore has failed the pilot.

## Duration

Long enough to include the conditions that matter: several nights, a weekend, a busy period, and ideally some bad weather. Short enough that the decision is made while people still care. A few weeks of live operation after shadow mode is a common range. If an important condition, such as heavy rain, does not occur, say so in the decision rather than extending indefinitely.

## Common ways pilots fail

- **No owner on the client side.** Nobody reviews alerts or gives feedback.
- **Moving goalposts.** New cameras and rules added halfway, so nothing is measured cleanly.
- **No end date.** The pilot becomes a free service.
- **Only easy cameras.** The rollout then meets the hard ones without preparation.
- **Feedback not collected.** At the end, only opinions remain.
- **Pilot hardware not production hardware.** Reliability results do not transfer.

## Checklist

- Questions the pilot must answer, written down.
- Small, representative scope with a named client owner.
- Install-and-check stage before judging analytics.
- Shadow mode with daily review and recorded tuning changes.
- Live stage with one-click feedback and weekly reviews.
- Exit criteria agreed in advance, including a user-facing one.
- Fixed end date and a clear go, fix or stop decision.
- Lessons and final settings carried into rollout and handover.

Next steps: [Writing a Results Report a Non-Technical Client Will Read](post:writing-results-reports-for-clients) and [Handover Documentation for a Computer Vision System](post:handover-documentation-for-cv-systems).
