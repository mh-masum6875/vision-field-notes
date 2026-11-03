---
title: "From Research Code to Production Code in Computer Vision"
description: "A notebook that reaches a good score is not a system. What changes when vision code must run unattended for months, without a rewrite."
category: "Career and Freelancing"
date: 2026-11-22
tags: [production, software-engineering, research, career, workflow]
---

Many computer vision engineers come from research: a thesis, a lab, a set of experiments that ended in a table of results. The code that produced that table was written to answer a question once. Production code has a different job: run every day, on many cameras, for months, maintained by people who did not write it. The skills overlap, but the habits are different, and the gap surprises people moving in either direction.

This article describes what changes when research code becomes production code, which habits to keep, and how to make the move gradually.

## Different goals, different code

| | Research code | Production code |
|---|---|---|
| Goal | Answer a question, report a result | Deliver a service reliably |
| Runs | A few times, watched | Continuously, unattended |
| Inputs | A known dataset | Whatever the cameras send |
| Failure | Rerun the experiment | Missed events, angry clients |
| Readers | The author, maybe reviewers | A team, a client, a successor |
| Lifetime | Until the paper is done | Years |

Neither kind of code is better. Research code that is over-engineered slows down experiments. Production code written like an experiment fails in ways nobody can debug. The skill is knowing which you are writing.

## What production code needs that research code skips

### Handling bad input

Research datasets are clean. Live streams are not: dropped connections, corrupted frames, frames of the wrong size, cameras that send nothing for an hour, timestamps that jump. Production code must expect all of it and keep running. See [Handling RTSP Dropouts](post:handling-rtsp-dropouts-and-reconnects).

### Running unattended

No one is watching the terminal. The code must start on boot, restart after crashes, report its health and log what it does. See [Watchdogs and Self-Recovery for Unattended Edge Boxes](post:watchdogs-for-unattended-edge-boxes) and [Metrics and Logging for a Vision Service](post:metrics-and-logging-for-vision-services).

### Configuration instead of edits

In research, changing a threshold means editing a line. In production, settings differ per camera and change without code changes. They belong in validated configuration files. See [Managing Per-Camera Configuration at Scale](post:per-camera-configuration-at-scale).

### Tests

Research code is checked by looking at the results. Production code needs automated tests so that changes do not silently break it. See [Regression Tests for a Vision Pipeline](post:regression-tests-for-vision-pipelines).

### Performance as a requirement

In research, a slow evaluation is an inconvenience. In production, speed decides how many cameras a box can handle and what the hardware costs. Measure and budget it. See [Profiling a Python Vision Pipeline](post:profiling-a-python-vision-pipeline).

### Reproducible environments and versions

A production model must be traceable to its data and code, and the environment must be rebuildable months later. See [Versioning Datasets and Models Together](post:versioning-datasets-and-models).

### Licences

Research code often uses whatever is available. Production code must respect the licences of models, libraries and datasets, especially for commercial use. See [YOLO Licenses Explained](post:yolo-licenses-explained).

## Research habits worth keeping

Production engineering can learn from research too:

- **Measure before believing.** Researchers are trained to distrust a result without a baseline and an evaluation. Production teams that skip this ship changes that make things worse.
- **Look at the failures.** Reading error cases one by one is a research habit that finds more problems than any dashboard.
- **Ablations.** Changing one thing at a time and measuring it is the clearest way to know what helped.
- **Honest reporting.** Stating limitations and uncertainty plainly builds trust with clients as much as with reviewers.

## Making the move without a rewrite

The worst approach is to keep a notebook as the production system. The second worst is a big rewrite that loses what the notebook got right. A gradual path works better:

1. **Freeze what matters.** Export the trained model, record the exact pre-processing and post-processing used in evaluation, and write tests that reproduce the evaluation outputs on a few images. See [Preprocessing Mismatches That Silently Cost Accuracy](post:preprocessing-mismatches-that-cost-accuracy).
2. **Extract functions.** Move pre-processing, inference and post-processing out of notebook cells into a small package with clear inputs and outputs. Keep the notebook for exploration, importing the package.
3. **Wrap the input.** Replace "read images from a folder" with a stream reader that handles reconnects and timestamps.
4. **Add state carefully.** Tracking, rules and alerts are stateful and time-based. Write them as separate components with tests on synthetic tracks.
5. **Add operations.** Configuration, logging, metrics, health checks, a service definition.
6. **Run on recorded footage before live cameras.** A replay set catches most integration bugs safely. See [Building a Replay Set of Recorded Footage](post:building-a-replay-set).

At each step, the tests from step 1 confirm the model still behaves as it did in evaluation.

## For people hiring or working across the gap

If you lead a team with both backgrounds, pair them. Researchers bring evaluation rigour and model knowledge; engineers bring reliability and operations. A short written agreement about what "done" means for a model, such as tests passing, exported, versioned and evaluated at the operating threshold, removes much of the friction.

If you are moving from research into industry yourself, a portfolio project that shows the production side, with a running service, tests and monitoring, often says more than another accuracy table. See [Build a Computer Vision Portfolio That Gets Clients](post:computer-vision-portfolio-that-gets-clients).

## Checklist

- Know whether you are writing experiment code or production code.
- Expect bad input and keep running.
- Run as a service with health checks and logs.
- Move settings into validated configuration.
- Add automated tests, starting with evaluation parity.
- Treat speed as a requirement and measure it.
- Version models, data and environments; check licences.
- Keep the research habits: baselines, failure analysis, one change at a time.

Next steps: [Computer Vision Engineer Roadmap: What to Learn First](post:computer-vision-engineer-roadmap) and [Reading Computer Vision Papers as a Practitioner](post:reading-papers-as-a-practitioner).
