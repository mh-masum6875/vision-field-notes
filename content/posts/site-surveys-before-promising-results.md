---
title: "Site Surveys: What to Check Before Promising a Result"
description: "A short visit or remote survey before quoting catches most problems that sink camera analytics projects. What to check, record and ask."
category: "Career and Freelancing"
date: 2026-11-27
tags: [site-survey, scoping, cameras, clients, freelancing]
---

Most failed camera analytics projects were decided before any code was written. The cameras were too far away, pointed into the sun, set to record at a low bitrate, or connected through a network that could not carry the streams. A few hours spent looking at the site would have revealed it, and changed the proposal, the price or the decision to take the work.

This article is a practical survey checklist: what to look at on site or remotely, what to record, and what to ask, before promising any result.

![A plan view of a schematic site. A camera is mounted 4.5 metres up on a building, with its field of view shaded across a yard towards a dashed area of interest. Two measured sight lines run into that area: at 18 metres a person is 74 pixels tall, at 44 metres a person is 30 pixels tall. A pillar stands between the camera and the area, marked as occluding. Parked vehicles are marked as moving. A low sun at the far corner is marked as shining into the lens at dusk. A comms cabinet in the near corner is marked with power, PoE and uplink, with an arrow asking how the streams get out and at what bitrate.](img:site-surveys-before-promising-results-what-to-measure.png "Not a real site. Every label is something the survey has to come back with a number or an answer for.")

Look at the two sight lines. The same person, the same camera, the same model: **74 pixels tall at the near edge and 30 at the far edge** of one zone. Whatever you promise has to be true at 30 pixels, not at 74, and that is decided by where the camera already is.

Nothing on that drawing is a modelling decision. The pillar, the sun, the mounting height and the uplink bitrate are all fixed before anyone opens a laptop, and all of them cap what the finished system can do.

## Remote or on site

An on-site visit is best for anything involving camera positions, lighting and installation. A remote survey, with footage, photos and a call with the site team, is often enough for a first assessment and for sites with many similar cameras. Either way, get real recordings from the actual cameras, including at night, before committing to numbers. See [When the Customer's Footage Doesn't Match the Demo](post:customer-footage-does-not-match-the-demo).

## 1. The problem, on the ground

Ask the people who work there, not only the person who wrote the request:

- Where exactly do the events happen? Walk the area and mark it on a plan.
- How often do they happen? Daily, weekly, rarely? This decides how you will test.
- What happens now when an event occurs, and who responds?
- What would a useful alert look like, and who would receive it?
- What looks like an event but is not? Authorised staff, cleaning crews, deliveries.

The answers often narrow the scope to a smaller area and a clearer rule than the original request.

## 2. Camera positions and views

For every camera that matters:

- **Height, angle and distance** to the area of interest. Note the nearest and farthest points.
- **Lens and field of view.** Wide lenses cover more and make everything smaller.
- **Pixels on target.** Take a frame, find a person or object at the farthest point that matters, and measure its size in pixels. Divide by the factor the model input will shrink the frame by. If it is very small, say so now. See [Input Resolution or Model Size](post:input-resolution-or-model-size).
- **Occlusions.** Racks, pillars, parked vehicles, signs, plants that will grow.
- **Overlap.** Is any area seen by more than one camera? That matters for counting and for double alerts.
- **Mounting.** Is it rigid? Does it vibrate when doors close or trucks pass?

Photograph each camera and its view from the camera position if you can reach it. Note where a better position or an extra camera would make the job easy.

## 3. Light, day and night

- Where does the sun come from at different times of day? Direct sun into a lens, low winter sun and reflections off floors and windows are common problems.
- What is the lighting at night? Does the camera switch to infrared? Do built-in illuminators light the far end? See [Day/Night Switching](post:day-night-switching-ir-cut-filter).
- Are there strong light changes: doors opening to daylight, vehicle headlights, flashing beacons?
- Does the camera lower its frame rate at night? See [When the Camera Changes Its Frame Rate at Night](post:variable-frame-rate-at-night).

If night matters, insist on night footage. Daytime footage says almost nothing about night performance.

## 4. Camera and recorder settings

Ask for access, or screenshots, of each camera's stream settings:

- Main stream and substream: resolution, frame rate, bitrate, codec, keyframe interval.
- Whether streams are taken from cameras directly or from a recorder, and connection limits.
- Time settings: time zone, NTP. See [Alerts at the Wrong Time of Day](post:alerts-at-the-wrong-time-of-day).
- Any built-in analytics or motion settings that might interact with yours.

Low-bitrate substreams and unsynchronised clocks are found on many sites and are easy to fix once known. See [Main Stream or Substream](post:main-stream-or-substream-for-analytics).

## 5. Network, power and placement of compute

- Where will the analytics hardware sit? Server room, cabinet, ceiling? What is the temperature there in summer?
- Is there power, and is it reliable? Is a UPS available?
- Can the network carry the streams from the cameras to that point? Count the cameras and their bitrates and compare with the links involved.
- Are cameras on a separate network or VLAN? Who can grant access, and how long will that take?
- Is internet access allowed for updates and alert delivery, or must the system work offline?

These questions often take longer to answer than the technical work, so ask them first. See [Power, Cooling and Storage for a Reliable Edge AI Box](post:power-cooling-storage-edge-ai-box).

## 6. Integration

- Where must alerts go? A video management system, an alarm panel, a messaging app, email, a dashboard?
- Is there documentation for those systems, and a test environment?
- Who on the client side can answer integration questions?

## 7. People and privacy

- Is there signage about camera monitoring, and does the new purpose fit what people have been told?
- Who has approved the use of footage for analysis, and is there a data protection contact?
- Will any footage leave the site, for labelling or support? Under what agreement?

See [Privacy and Ethics in Camera Analytics](post:privacy-and-ethics-camera-analytics). This is not legal advice.

## Record and report

Write the survey up as a short document: a plan of the area with camera positions, one frame per camera with the area of interest and the farthest target marked, the pixel measurements, the problems found, and recommended changes with rough costs. Share it with the client before quoting the main work.

This document does three jobs. It shows the client you understood their site. It records the conditions your estimate assumed. And it often sells the camera changes that make the project succeed.

## Checklist

- Talk to the people who see the events.
- Mark event areas on a plan and estimate event frequency.
- Record height, angle, lens, occlusions and pixels on target per camera.
- Check sun, reflections, infrared and night lighting; get night footage.
- Record stream settings, recorder use, time settings and connection limits.
- Check compute location, temperature, power, network capacity and access.
- Identify integration targets, documentation and contacts.
- Check signage, approvals and where footage may go.
- Write a short survey report before quoting.

Next steps: [Estimating a Computer Vision Project](post:estimating-a-computer-vision-project) and [Agreeing a Measurable Target with a Client](post:agree-a-measurable-target-with-a-client).
