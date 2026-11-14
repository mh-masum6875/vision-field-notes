---
title: "Turning Down a Computer Vision Project (and Offering Something Better)"
description: "Some vision projects should not be accepted as asked. How to spot them, say no without losing the client, and offer a version that works."
category: "Career and Freelancing"
date: 2026-11-17
tags: [freelancing, clients, scoping, ethics, career]
---

Early in a freelance or consulting career, every enquiry looks like an opportunity. Later you learn that some projects cost more than they pay: in time, in reputation, and in the stress of promising something that cannot be delivered. Learning to say no, and to say it well, is one of the most valuable skills in applied computer vision.

This article covers the projects worth declining or reshaping, how to tell the client, and how a good "no" often turns into better work.

## Projects to be careful with

### The cameras cannot see it

The client wants to read number plates at 60 metres from a wide-angle overview camera, or check whether workers wear gloves from a camera on the ceiling of a large hall. If the detail is not in the pixels, no model will find it. A quick calculation of pixels on target settles this before any work starts.

![A line chart of pixels across a 52 cm number plate against distance, for a 1080p camera at three fields of view. Horizontal bands mark what each pixel count allows: below 25 pixels nothing usable, 25 to 70 a box but no characters, above 70 characters readable. The 90 degree wide overview lens falls below 70 pixels beyond about 7 metres and reaches only 8 pixels at 60 metres. The 50 degree medium lens gives 107 pixels at 10 metres and 18 at 60. The 20 degree zoomed lens stays readable to about 40 metres.](img:turning-down-a-computer-vision-project-pixels-on-target.png "Geometry only. Pixels across equals the object width divided by the scene width at that distance, times the image width. The bands are the usual rules of thumb for plate reading.")

That chart is the conversation. A plate at 60 metres on a 90° camera is **8 pixels across** — narrower than this full stop is wide on your screen. There is no model, no upscaler and no budget that reads seven characters from eight pixels, and the honest answer takes about thirty seconds to work out:

```text
pixels across = plate width / scene width at that distance × image width
              = 0.52 m / 120 m × 1920
              = 8 px
```

Do that sum in the first meeting. It is far easier to say no before you have quoted than after you have failed. See [When the Customer's Footage Doesn't Match the Demo](post:customer-footage-does-not-match-the-demo).

### The accuracy expectation is impossible

"It must never miss" or "zero false alarms" is not a specification any detector meets. If the process truly cannot tolerate errors, the design needs human review, redundant sensors or physical controls. Accepting the project as stated sets up a failure.

### There is no data and no way to get it

The event is very rare, the client cannot share footage, and staged data is not allowed. Without examples of the thing to detect, you cannot train it or prove it works.

### Success cannot be defined

The client cannot or will not say what a good result looks like, and resists any written target. That project ends in an argument. See [Agreeing a Measurable Target with a Client](post:agree-a-measurable-target-with-a-client).

### The purpose is harmful or unlawful

Covert surveillance of employees, identifying individuals without a lawful basis, inferring sensitive characteristics, or systems whose errors would fall hardest on people who cannot challenge them. Some of these are illegal in many places; others are legal and still harmful. You are entitled to decline work you consider wrong, and in some cases you should. See [Privacy and Ethics in Camera Analytics](post:privacy-and-ethics-camera-analytics). This is not legal advice.

### It is not your area

A medical imaging diagnosis, a safety-certified control system, or a domain with regulation you do not know. Taking it on to learn is fine in some settings, but not when the client believes they are hiring an expert.

### The budget and the scope do not match

A full multi-site deployment for the price of a prototype. Or a fixed price on something with large unknowns. See [Estimating a Computer Vision Project](post:estimating-a-computer-vision-project).

## How to say no

Be prompt, specific and kind. Long delays waste the client's time, and vague refusals leave them confused.

1. **Thank them and show you understood the problem.** Restate it in one or two sentences.
2. **Explain the specific reason,** in their terms. "From the sample images, a glove covers about 3 pixels at the far end of the hall, which is not enough for any detector to see reliably" is clear and checkable. "It's not feasible" is not.
3. **Offer an alternative if there is one** (see below).
4. **If there is no alternative, say so,** and if you can, point them to someone better suited.

A specific, honest refusal often earns more respect than an eager yes. Clients remember who told them the truth early, and many come back with a better-defined project.

## Offering something better

Most "no" answers are really "not like this". Common alternatives:

### A smaller scope

Instead of all 40 cameras, the six where the problem actually occurs. Instead of detecting five PPE items, the one that drives most incidents. A narrow system that works is worth more than a broad one that does not, and it builds the evidence for expansion.

### A paid feasibility study

When the honest answer is "I don't know if this can work", sell the answer. A short, fixed-price discovery phase reviews real footage, runs a baseline and reports what is possible, with numbers. Both sides learn cheaply, and the result is useful even if it is "no".

### Change the cameras, not the model

Moving a camera, changing a lens, adding light or adding a camera close to the area of interest can turn an impossible task into a routine one. Recommend it explicitly, with the reason. See [Site Surveys: What to Check Before Promising a Result](post:site-surveys-before-promising-results).

### Human in the loop

If errors are not tolerable, design the system to assist people rather than replace them: flag candidates for review, prioritise footage, summarise events. The detector's errors then cost a few seconds of review instead of a missed incident.

### A different technology

Sometimes vision is the wrong tool. A beam sensor, a door contact, a weight sensor or an RFID tag may solve the problem more cheaply and reliably. Saying so builds trust, even if it means less work for you this time.

## When to reconsider a "no"

Circumstances change. The client may agree to move cameras, provide footage, accept a human review step, or narrow the scope. Make it easy for them to come back by explaining what would change your answer: "If we can add a camera above the loading bay and get two weeks of footage, I'd be glad to quote for a prototype."

## Protect your own judgement

It helps to decide some rules in advance, while there is no client in front of you: the kinds of purposes you will not work on, the minimum information you need before quoting, the budget below which you will not take a fixed-price project. Pressure in the moment, especially when work is scarce, makes these decisions harder. Rules made earlier make them easier.

## Checklist

- Check pixels on target before accepting detail-dependent work.
- Decline impossible accuracy demands or redesign with human review.
- Require access to real data and a definable success measure.
- Decline harmful or unlawful purposes.
- Say no promptly, with a specific reason in the client's terms.
- Offer a smaller scope, a feasibility study, camera changes, human review or a different technology.
- Explain what would change your answer.

Next steps: [Freelancing in Computer Vision: Winning Your First Jobs](post:freelancing-in-computer-vision) and [Site Surveys: What to Check Before Promising a Result](post:site-surveys-before-promising-results).
