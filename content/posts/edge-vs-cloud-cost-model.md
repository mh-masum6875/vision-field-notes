---
title: "Edge or Cloud: Building the Cost Model Before You Choose"
description: "The architecture decision is usually made on instinct. A simple model over three years makes it obvious, and sometimes surprising."
category: "Edge Hardware and Deployment"
date: 2026-11-27
tags: [edge, cloud, cost, architecture, deployment]
---

"Should this run on the edge or in the cloud?" gets answered on instinct far more often than on arithmetic. The instinct is usually "edge is cheaper because there is no bill", which is sometimes true and frequently not once you count everything.

The arithmetic is not hard and it takes about an hour. It is worth doing before the hardware is ordered rather than after.

## Count all four cost lines

**Hardware.** The box, the accelerator, the enclosure, the mounting. Divide by the replacement life you actually expect, not the warranty. An edge box in a dusty warehouse does not last as long as one in a server room.

**Connectivity.** Streaming video to a cloud endpoint costs bandwidth continuously. One 2 Mbps stream is roughly 650 GB a month. Multiply by cameras and by however long the contract runs. For a site on a business fibre line this may be free at the margin; for one on a 4G router it dominates everything else.

**Compute.** For cloud, the hourly rate of whatever instance runs the inference, times utilisation. For edge, the electricity, which is small, plus the amortised accelerator.

**Operations.** The line everyone forgets and the one that usually decides it. Someone has to deploy model updates, notice when a box has died, and physically visit when it has. Forty sites means forty things that can fail somewhere you are not.

## The shape of the answer

Run it over three years and the pattern is usually one of these.

![Two stacked bar charts of three-year cost, each comparing edge against cloud, broken into hardware, bandwidth, compute and operations. For 100 shops with two cameras each, 200 cameras in total, edge costs £330k, dominated by £150k of hardware and £180k of operations, while cloud costs £261k, so cloud is 21% cheaper. For one port with 60 cameras, edge costs £14k, almost all hardware, while cloud costs £65k, dominated by £39k of compute and £26k of bandwidth, so edge is 79% cheaper.](img:edge-vs-cloud-cost-model-three-year-cost.png "Illustrative rates, stated on the figure so you can substitute your own. The cost lines are identical in both scenarios; only the shape of the deployment changes.")

Both panels use the same four lines and the same rates. The only thing that changes is how the cameras are distributed, and that is enough to reverse the answer.

Look at what dominates each bar. In the hundred shops, edge is expensive because of **operations** — £180k of visiting and maintaining a hundred boxes, which is more than the hardware itself. At the port, cloud is expensive because of **compute and bandwidth** — 60 streams billed every month for three years, against a one-off £12k of hardware.

Neither of those lines is the one people argue about. The argument is usually about the hardware price, which is the smaller number in both cases.

**Few cameras, many sites** — a retail chain with two cameras per store — tends to favour the cloud. Per-site hardware is a poor deal when you are only running two streams, and the operational cost of maintaining hardware in a hundred shops is the real expense.

**Many cameras, one site** — a port, a factory, a large warehouse — strongly favours edge. One box can serve many streams, bandwidth to the cloud would be enormous, and there is one physical location to maintain.

**Anything with tight latency** — a barrier that must open before the vehicle stops, a safety stop — favours edge regardless of cost, because a round trip to a region several hundred kilometres away is not negotiable.

**Anything where footage cannot leave the premises** favours edge regardless of cost, for the same reason.

## Utilisation is where cloud estimates go wrong

The common error in cloud costing is pricing a GPU instance at 24/7 and concluding it is expensive.

Most analytics do not need every frame. If you process one frame per second rather than twenty-five, one instance serves many more streams. If the site is only active twelve hours a day, you can halve it again. Batching across cameras improves throughput further.

Work out the frames per second you actually need before pricing anything. A system that genuinely needs 25fps per camera and one that needs 2fps have cost models an order of magnitude apart, and the requirement is often assumed rather than examined.

## The hidden edge costs

On the other side, the edge estimate is usually too low because it omits:

**Spares.** You need replacement units on a shelf, or an SLA that gets one there. That is capital sitting idle.

**Site visits.** One engineer-day to a remote site can cost more than a year of cloud compute for that site. Two visits and the comparison inverts.

**Update risk.** Pushing a model to forty boxes is a deployment with failure modes. Pushing to one cloud service is not. Getting that right has engineering cost before it has operational cost.

**Thermal derating.** An accelerator rated for a workload in a lab does less in a hot cabinet. If you size on the datasheet you will under-provision. Measure in the enclosure you will actually use.

## The hybrid that usually wins

In practice many deployments end up split, and deliberately so.

Detection and tracking run at the edge, because that is the expensive, high-frequency part and it keeps raw video local. Only events and small crops go to the cloud — "person entered zone 3 at 14:22, here is a 200×200 thumbnail".

This collapses the bandwidth line from megabits continuously to kilobytes occasionally, keeps the latency-sensitive part local, and still gives you central dashboards, aggregation and model management.

It also means footage largely stays on site, which answers the privacy question before anyone has to ask it.

## Writing it down

Build the table before the meeting, with the assumptions visible: cameras per site, sites, fps, hours per day, bandwidth cost per GB, hardware life, site visit cost.

Then show it to whoever is paying and let them challenge the assumptions. They will — usually the site visit cost and the hardware life — and that conversation is more productive than arguing about architecture in the abstract.

The number itself matters less than having made the trade explicit. A decision with the assumptions written down can be revisited when one of them changes. One made on instinct cannot.
