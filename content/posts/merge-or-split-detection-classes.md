---
title: "Single-Class or Multi-Class: When to Merge or Split Detection Classes"
description: "Should car, van and truck be one class or three? How to decide a detector's classes, and why labelling fine and training coarse keeps options open."
category: "YOLO and Detection Basics"
date: 2026-11-15
tags: [classes, dataset-design, yolo, classification, labelling]
---

Early in every detection project someone writes the class list, and it is rarely revisited. Yet the class list shapes everything after it: how long labelling takes, how much data each class needs, which errors the model makes and which numbers end up in the report. Too many classes and the model confuses near-identical ones; too few and you cannot make the decision the client needs.

This article gives a practical way to decide whether classes should be merged or split, and a design that keeps both options open.

## Start from the decision

Classes exist to support decisions. For each proposed class, ask: does the system do something different for this class? If cars, vans and trucks all lead to the same action, such as "vehicle in the fire lane", they are one class for that system. If trucks trigger a different rule, such as a height restriction, trucks need to be distinguished.

Classes that change no decision cost labelling time, split the training data into smaller pieces, and create confusion errors that do not matter but still appear in the metrics.

## Reasons to merge

- **The classes look alike at your resolution.** If labellers struggle to tell them apart on your camera images, the model will too. A distinction that needs detail the pixels do not contain is not learnable. See [Input Resolution or Model Size](post:input-resolution-or-model-size).
- **One class is rare.** A class with a few dozen examples will have poor accuracy and noisy metrics. Merged into a related class, its examples help instead of being wasted.
- **They lead to the same action.** As above.
- **The boundary is fuzzy.** Where does a van end and a small truck begin? Fuzzy boundaries cause label disagreement, which shows up as model confusion that is really labelling noise. See [Measuring Label Quality with Annotator Agreement](post:measuring-label-quality-annotator-agreement).

## Reasons to split

- **Different actions.** The system treats them differently.
- **Clearly different appearance.** Merging very different things into one class, such as "obstruction" covering pallets, people and bins, makes the class hard to learn.
- **Different error costs.** If missing one subtype is much worse, a separate class lets you set its own threshold. See [Confidence Thresholds](post:confidence-threshold-tuning).
- **Reporting needs.** A client who wants counts per vehicle type needs vehicle types.

## Detect broad, classify fine

A common and effective design separates the two jobs:

![Diagram: a detector finds broad classes, vehicle and person. Vehicle crops go to a second stage that classifies car, van or truck; person crops go to a second stage that decides helmet yes or no. Notes: merge when classes look alike, are rare, or lead to the same action; split when the action differs and the difference is visible; a second stage can be trained, tested and changed without touching the detector.](img:merge-or-split-detection-classes-two-stage.png "A diagram, not data. The detector handles localisation with plenty of data per class; the finer decision is made on crops by a separate, smaller model or an attribute head.")

1. A detector finds broad classes, such as "person" and "vehicle". With fewer, larger classes, each has plenty of data and localisation is reliable.
2. A second stage looks at each detected crop and makes the finer decision: vehicle type, helmet or not, vest colour.

The advantages are practical. The crop classifier sees the object at a higher effective resolution, because a crop can be resized up to the classifier's input. It can be retrained when the client adds a vehicle type without touching the detector. Its errors are easier to analyse, since localisation and classification errors are separated. The cost is an extra model in the pipeline and some extra compute per detection.

For attributes of people, such as PPE, this pattern is often more robust than training a detector with classes like "person with helmet" and "person without helmet". Those combined classes split the person data in half and make the detector learn two hard things at once.

## Label fine, train coarse

The most useful rule of all: **label at the finest level you might ever need, and merge at training time.** Merging labels later is a one-line mapping. Splitting labels later means relabelling every image of that class.

If there is a reasonable chance the client will later want vans separated from cars, label "car" and "van" now, and train a "vehicle" detector by mapping both to one class. The extra labelling effort is small when the labeller is already drawing the box; the saving later can be weeks.

Do this within reason. Labelling twenty vehicle subtypes because someone might want them one day slows labelling and invites disagreement. Pick the distinctions with a real chance of being needed.

## Watch what the metrics do

Changing classes changes the numbers, which can mislead:

- **mAP is a mean over classes.** Splitting a strong class into three weaker ones can lower mAP even if the system is just as useful. Merging a weak class into a strong one can raise mAP while the weak case remains weak. Compare per-class results and decision-level results, not mAP across different class lists. See [What mAP Hides](post:what-map-hides).
- **Confusions become visible or invisible.** When two classes are merged, confusion between them disappears from the confusion matrix, as it should if it does not matter.
- **Results are not comparable across class lists.** A model with five classes and one with two are measured on different tasks. Evaluate both on the decision the client cares about, such as event-level alerts, to compare them fairly.

## A quick procedure

1. List the decisions the system must make.
2. For each candidate class, note which decision it supports and how many examples you expect.
3. Check a sample of images: can people reliably tell the classes apart at your resolution?
4. Merge classes that fail any of these tests; plan a second stage for distinctions that only some decisions need.
5. Label one level finer than you train, where a split is plausible later.
6. Write the class definitions and boundaries into the annotation guide. See [Writing an Annotation Guide Labellers Can Follow](post:annotation-guide-labellers-can-follow).

## Checklist

- Every class supports a decision.
- Classes are distinguishable at your camera resolution.
- Rare classes merged or given enough data.
- Fine distinctions handled by a second stage where useful.
- Labels one level finer than training classes, where a split is plausible.
- Class changes compared on per-class and decision-level results, not mAP alone.

Next steps: [Classification vs Detection vs Segmentation](post:classification-vs-detection-vs-segmentation) and [Class Imbalance and Small Objects](post:class-imbalance-and-small-objects).
