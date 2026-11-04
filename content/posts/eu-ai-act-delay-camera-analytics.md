---
title: "The EU AI Act Delay: What Camera Analytics Teams Should Know"
description: "The Digital Omnibus moved the EU AI Act's high-risk deadlines to December 2027. What changed, what did not, and what it means for video analytics."
category: "Video Analytics"
date: 2026-11-07
tags: [news, eu-ai-act, regulation, privacy, video-analytics]
---

In July 2026 the EU adopted the "Digital Omnibus on AI", an amending regulation that postpones the main obligations for high-risk AI systems under the AI Act. Several clients and colleagues have read the headlines as "the AI Act has been delayed". It has, in part. Some of what matters most for camera analytics was not delayed at all.

This post summarises the changes relevant to people building video analytics, as of early November 2026. It is not legal advice. If your system could fall into a high-risk or prohibited category, get advice from someone qualified in EU law.

## What changed

The amending regulation is Regulation (EU) 2026/1744, dated 8 July 2026, and in force since 27 July 2026. For this field, the key changes are:

- **High-risk systems listed in Annex III** must meet the high-risk requirements from **2 December 2027** instead of 2 August 2026. Annex III covers, among other areas, biometrics, critical infrastructure, education and employment.
- **High-risk systems that are safety components of products** regulated under Annex I follow from **2 August 2028**.
- **Simplified documentation and quality management** are allowed for SMEs and some small mid-cap companies, and fine caps are adjusted for them.
- **The AI literacy obligation** is reworded towards supporting AI literacy among staff, rather than requiring a set level.

## What did not change

The prohibitions in Article 5 of the AI Act have applied since 2 February 2025, and the omnibus did not delay them. Several of them touch camera systems directly, including:

- Building or expanding facial recognition databases by untargeted scraping of facial images from the internet or CCTV footage.
- Emotion recognition in workplaces and educational institutions, except for medical or safety reasons.
- Biometric categorisation that infers sensitive characteristics, such as race, political opinions or sexual orientation.
- Real-time remote biometric identification in publicly accessible spaces for law enforcement, except under narrow, defined conditions.

The omnibus also adds new prohibitions on systems that generate non-consensual intimate imagery or child sexual abuse material, applying from 2 December 2026. These are not camera analytics features, but they show the direction of travel: prohibitions are being added, not relaxed.

Data protection law, such as the GDPR, applies to camera footage of people regardless of the AI Act's timetable.

## Where typical video analytics sits

Most object-level analytics, such as counting people, detecting vehicles in a zone or spotting a missing hard hat without identifying anyone, is not listed as high-risk by itself. But a few common product directions come close to the lines:

- **Identifying individuals** from video is remote biometric identification, which is listed in Annex III and, in some law-enforcement uses, prohibited.
- **Monitoring and evaluating workers.** Annex III includes AI systems intended to monitor and evaluate the performance and behaviour of people in work relationships. A PPE compliance system that only raises safety alerts is different from one that scores individual workers, but where exactly the line falls for a given product is a legal question.
- **Emotion or attention detection** on staff is prohibited in workplaces except for medical or safety reasons.

Design choices matter here. A system that counts and alerts without identifying people, keeps footage briefly and aggregates results is in a very different position from one that tracks named individuals over time. See [Privacy and Ethics in Camera Analytics](post:privacy-and-ethics-camera-analytics).

## What to do with the extra time

If any of your products could be high-risk, the delay gives time to prepare properly rather than a reason to stop. Useful work now:

- **Classify each product honestly.** Write down what it does, who it is used on and what decisions it supports, and get a qualified view on whether it falls into a high-risk category.
- **Build the evidence you would need anyway.** Documented datasets, versioned models, test results by condition and a record of what runs where are expected for high-risk systems, and are good engineering regardless. See [Versioning Datasets and Models Together](post:versioning-datasets-and-models) and [Building a Night and Bad-Weather Test Set](post:night-and-bad-weather-test-set).
- **Design for human oversight.** Alerts reviewed by people, clear explanations of why an alert fired, and easy ways to correct errors. See [Debug Overlays That Actually Help](post:debug-overlays-that-help).
- **Avoid features near the prohibited lines,** such as emotion recognition on staff, unless you have clear legal confirmation that a specific use is allowed.
- **Keep a short regulatory note in the handover documents** for each client, stating the assumptions under which the system was designed. See [Handover Documentation for a Computer Vision System](post:handover-documentation-for-cv-systems).

Teams outside the EU should not ignore this. The AI Act applies to systems placed on the EU market or whose output is used in the EU, and clients with European operations will ask.

## Sources

- Regulation (EU) 2026/1744 (Digital Omnibus on AI), consolidated reading on the AI Act Explorer: [artificialintelligenceact.eu/ai-act-explorer/digital-omnibus](https://artificialintelligenceact.eu/ai-act-explorer/digital-omnibus/)
- Orrick, "EU AI Act Update: Digital Omnibus Finalizes 8 Compliance Changes" (July 2026): [orrick.com](https://www.orrick.com/en/Insights/2026/07/EU-AI-Act-Update-Digital-Omnibus-Finalizes-8-Compliance-Changes)
- Gibson Dunn, "EU AI Act Omnibus Agreement — Postponed High-Risk Deadlines and Other Key Changes": [gibsondunn.com](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)

For the authoritative text, use the version published in the Official Journal of the EU on EUR-Lex.

Next steps: [Privacy and Ethics in Camera Analytics](post:privacy-and-ethics-camera-analytics) and [Turning Down a Computer Vision Project](post:turning-down-a-computer-vision-project).
