---
title: "YOLO Licenses Explained: AGPL, GPL and Commercial Use"
description: "YOLO licenses explained: what AGPL-3.0 and GPL-3.0 mean for YOLO projects, options for commercial products and safe habits. Not legal advice."
category: "YOLO and Detection Basics"
date: 2026-10-22
tags: [yolo, licensing, agpl, commercial-use]
---

Licensing is the part of a YOLO project that many engineers skip until a customer or a lawyer asks about it. By then the code is written and changing course is costly. This article explains the basics in plain language so you can ask the right questions early.

One clear disclaimer first. I am an engineer, not a lawyer, and this is not legal advice. Licences are legal documents, and their effect depends on how you use the software. Read the current licence text and get qualified advice before you ship a commercial product.

## The licences you will meet

| Project | Licence (as commonly published) | Notes |
|---|---|---|
| YOLOv5 (Ultralytics) | AGPL-3.0 | Commercial licence available from Ultralytics |
| YOLOv8 and YOLO11 (Ultralytics) | AGPL-3.0 | Commercial licence available from Ultralytics |
| YOLOv7 | GPL-3.0 | Check the repository for any other licensing options |

Licences can change and forks can differ. Always check the repository you actually use, at the version you actually use.

## What "open source" does and does not mean

Open source does not mean "free for anything". It means you get the source code under conditions. Those conditions fall into two broad groups.

- **Permissive licences** (for example MIT, BSD, Apache-2.0) let you use the code in closed products with light obligations, mostly keeping notices.
- **Copyleft licences** (GPL, AGPL) require that if you distribute or provide a work based on the code, you offer the source of that work under the same licence.

AGPL-3.0 and GPL-3.0 are copyleft. The difference between them is where the obligation starts.

## GPL-3.0 in plain words

Under GPL-3.0, the main trigger is distribution. If you give someone a copy of your program that includes or is derived from GPL code, for example by shipping a product or an installer, you must make the corresponding source available under the GPL too. If you only run the software on your own servers and never hand copies to anyone, the classic GPL obligations are usually not triggered. That gap is sometimes called the "SaaS loophole".

## AGPL-3.0 in plain words

AGPL-3.0 was written to close that gap. It adds a rule about network use: if users interact with a modified version of the program over a network, you must offer them the source of that version. So running modified AGPL code behind a web service can create an obligation to share your source, even though you never distribute a copy.

What counts as "modified", what counts as a "work based on" the code, and how far the obligation reaches into the rest of your system are exactly the questions where legal advice is worth paying for. Do not guess.

## Why this matters for YOLO

When you use the Ultralytics package in your application, you are using AGPL-licensed code. Typical situations:

- **Research, study, personal projects.** Usually low risk. You are not distributing a product.
- **An internal tool used only inside your company.** Often treated differently from a public product, but this is a question to confirm, not assume.
- **A product you sell or ship to customers**, such as a device with the model on it, or software that includes the library. Distribution is likely involved. This is the case where you need to decide how to comply.
- **A web service or API built on the library.** The network clause may apply. Take advice.

Note that the licence can cover more than the code. The pretrained weights, your trained weights and the training pipeline all raise questions. Ultralytics publishes its position on its own site; read it there rather than relying on a blog summary, including this one.

## Your options for commercial products

Broadly, you have four paths. Each has costs.

1. **Comply with the open licence.** Release the source of your application under the same licence as required. This suits open projects, or businesses where the code is not the secret ingredient. It does not suit closed products.
2. **Buy a commercial licence.** Ultralytics offers one for its models. Terms, price and scope are set by them, so contact them and read the agreement. Check the current price rather than trusting an old figure.
3. **Use a detector with a permissive licence.** Several detection models and libraries are released under licences such as Apache-2.0 or MIT. You then need to confirm the licence of the code, the pretrained weights and any dataset used for pretraining. A permissive code licence with restricted weights is still a restriction.
4. **Train your own model architecture** with permissively licensed components. This gives the most control and takes the most effort.

None of these is always best. It depends on whether your code can be open, your budget, and your customers' requirements.

## Common mistakes

- **Assuming a pip install makes it free.** Being able to download a package says nothing about what you may do with it commercially.
- **Checking only the code.** Weights and datasets can carry their own terms. A dataset licensed for research only can cause trouble for a commercial model trained on it.
- **Forgetting about forks and copies.** Code copied from a GitHub repository into your project keeps its original licence.
- **Mixing licences without checking.** GPL and AGPL code combined with permissive code is usually fine in one direction and a problem in the other. Combining with proprietary code is where problems appear.
- **Not recording the version.** A licence can change between releases. Record which version and which licence you used on the day you adopted it.
- **Treating a client's request as a legal review.** If a client says "just use YOLO", they may not know the licence either. Raise it early and put the decision in writing.

## Safe habits

A few practices keep you out of trouble and cost almost nothing.

- Keep a simple list of every model, library and dataset you use, with its licence and the link to the licence text.
- Decide the licensing route before building the product, not after the first demo.
- Save a copy of the licence text with each release you ship.
- Ask for the licence terms of any pretrained weights you download, not only the code.
- If you work for clients, tell them which components carry which obligations.
- When in doubt, ask the maintainers or a lawyer, and keep their answer.

If you are a freelancer or consultant, this is also a trust issue. Delivering a model to a client without telling them about the licence can create a problem for them later. A short note in your handover document is enough to prevent it.

## What I will not tell you

I will not tell you whether your specific use is allowed. The answer depends on how you build, deploy and distribute, and on your jurisdiction. Anyone who gives you a confident yes or no without those details is guessing. What I can tell you is how to find out: read the licence, list your components, and get advice for the commercial cases.

## Checklist

- Do you know which licence each model, library and dataset uses?
- Have you read the licence for the exact version you use?
- Will you distribute the software, or offer it over a network?
- Have you chosen a route: comply, buy a commercial licence, or use a permissive alternative?
- Are weights and training data covered by terms you can accept?
- Is the decision recorded and shared with your client or team?

Next steps: [YOLOv5 vs YOLOv8 vs YOLO11](post:yolov5-vs-yolov8-vs-yolo11) for the technical differences, and [How YOLOv7 Gets Real-Time Speed with Re-parameterization](post:yolov7-reparameterization) for the GPL-licensed alternative.
