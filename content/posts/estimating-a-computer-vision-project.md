---
title: "Estimating a Computer Vision Project: Where the Time Really Goes"
description: "Model training is rarely the long part. How to estimate a vision project honestly: data access, labelling, integration, site testing and waiting."
category: "Career and Freelancing"
date: 2026-11-12
tags: [estimation, project-planning, freelancing, clients, scoping]
---

Ask an engineer how long a detection project will take and the answer often centres on the model: a few days to collect data, a week to train and tune. Then the project takes three months. The model took a week. The rest went on getting footage, labelling it, connecting to the client's systems, waiting for site access, testing at night, and revising after the first review.

This article breaks a typical vision project into the parts that consume time, explains which ones are usually underestimated, and gives a way to present an estimate a client can trust.

## Where the time goes

A project that ends in a deployed system usually includes most of these:

1. **Discovery.** Understanding the problem, looking at sample footage, agreeing what success means.
2. **Data access.** Getting real footage from the right cameras, at the right times, in a usable format.
3. **Labelling.** Writing a guide, labelling, reviewing, fixing.
4. **Model work.** Training, evaluating, iterating on data and settings.
5. **Pipeline.** Stream handling, tracking, rules, alerts, health checks.
6. **Integration.** Connecting to the client's video system, alarm system, dashboard or messaging.
7. **Deployment.** Hardware, installation, networking, security reviews.
8. **Testing on site.** Acceptance footage, day and night, false alarm review.
9. **Revisions.** Changes after the client sees results.
10. **Handover.** Documentation and training. See [Handover Documentation for a Computer Vision System](post:handover-documentation-for-cv-systems).

The model is one item out of ten. Estimating it well and the rest badly still gives a bad estimate.

## The usual underestimates

### Data access

Getting footage sounds trivial and often is not. Security footage is sensitive, so requests go through IT, security and sometimes legal. Recorders export in awkward formats. The cameras you need record only on motion, or keep footage for a few days. Night footage requires someone to export it after the night. Weeks can pass before you have what you need.

Ask for footage at the very start, in parallel with everything else, and treat its arrival as a dependency in the plan.

### Labelling

Labelling time is easy to estimate badly and easy to measure. Before quoting, label 50 representative images yourself with a draft guide and time it. Multiply by the number of images, add time for review and corrections, and add time for writing the guide and answering labellers' questions. Crowded scenes take far longer per image than sparse ones, so measure on realistic images. [How Many Images Do You Need?](post:how-many-images-do-you-need) helps with the image count, and [Pseudo-Labelling with a Larger Model](post:pseudo-labelling-with-a-larger-model) may cut the time, but measure that too.

### Integration

Every client's systems are different. Video management systems, alarm panels and messaging platforms have their own interfaces, documentation quality and access rules. Getting credentials, a test environment and someone on the client side to answer questions can take longer than writing the code.

### Waiting

Site visits need permits and escorts. Network changes need the client's IT team. Reviews need the client's time. None of this is your effort, but all of it is calendar time. Separate effort (days of work) from duration (calendar weeks) in the estimate, and say which parts depend on the client.

### Testing at night and in bad weather

If the system must work at night, you need night footage and night testing, which means waiting for nights, often with someone on site. If it must work in rain, you need rain. Plan for it rather than hoping a test week contains every condition.

### Revisions

The first time a client sees real alerts, they discover what they actually want: a different zone, a schedule, a class split in two. Budget at least one round of meaningful changes, and say so.

## Present a range, not a number

A single number for an uncertain project is a promise you probably cannot keep. Give ranges, with the reasons for the spread:

| Phase | Effort | Main uncertainty |
|---|---|---|
| Discovery | Small, fixed | Low |
| Data access | Small effort, uncertain duration | Client's process |
| Labelling | Depends on image count and density | Measured on a sample |
| Model and pipeline | Medium | Data quality, difficulty of the cameras |
| Integration | Small to large | Client's systems and access |
| Site testing and revisions | Medium | Conditions, client feedback |

A three-point estimate per phase (optimistic, likely, pessimistic) is a simple way to produce the ranges. The pessimistic case should be genuinely pessimistic: what happens if the footage is poor, the integration is undocumented, and the first review asks for changes.

Then reduce uncertainty early. A paid discovery phase that includes a look at real footage and a baseline model run removes much of the spread before the main estimate is agreed. See [Freelancing in Computer Vision](post:freelancing-in-computer-vision) and [When the Customer's Footage Doesn't Match the Demo](post:customer-footage-does-not-match-the-demo).

## Assumptions are part of the estimate

Write down what the estimate assumes:

- The client provides footage from named cameras, including night, by a given date.
- The client provides access to the systems to integrate with, and a contact who can answer questions.
- Labelling volume up to a stated number of images.
- One round of revisions after the first results.
- Hardware supplied by whom, and installed by whom.

When an assumption breaks, the estimate changes, and both sides can see why. Without written assumptions, every delay becomes an argument.

## Track and re-estimate

Keep a simple record of planned versus actual time per phase. It is the only way your next estimate improves. And re-estimate at each phase boundary: after discovery, after the first trained model, after the first site test. Each time, the uncertain parts shrink and the estimate becomes more reliable. Tell the client when it changes, early.

## Checklist

- Estimate all phases, not only the model.
- Request footage on day one and treat it as a dependency.
- Measure labelling time on a realistic sample.
- Separate effort from calendar duration.
- Plan for night and weather testing.
- Budget at least one revision round.
- Present ranges with reasons and written assumptions.
- Use a paid discovery phase to narrow the range.
- Record actual time per phase and re-estimate at boundaries.

Next steps: [Agreeing a Measurable Target with a Client](post:agree-a-measurable-target-with-a-client) and [Turning Down a Computer Vision Project](post:turning-down-a-computer-vision-project).
