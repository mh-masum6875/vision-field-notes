---
title: "Reading YOLO Training Curves: When to Stop and What to Change"
description: "What YOLO loss and metric curves tell you, the shapes of overfitting and under-training, and the quirks in the curves that are not problems."
category: "Datasets and Training"
date: 2026-11-25
tags: [training, yolo, overfitting, loss-curves, ultralytics]
---

Every Ultralytics training run leaves a `results.csv` and a `results.png` in its run folder: a grid of loss and metric curves over epochs. Most people glance at the final mAP and move on. The curves say much more: whether training finished, whether the model memorised the training set, whether the data or the settings are the problem, and how many epochs the next run needs.

This article explains how to read those curves, the shapes worth recognising, and a few features of the curves that look alarming but are normal.

## What is plotted

For detection, the run records, per epoch:

- **Training losses:** box loss (how well boxes fit), classification loss (how well classes are predicted) and, in recent YOLO versions, a distribution focal loss (DFL) related to box edge prediction.
- **Validation losses:** the same three, computed on the validation set.
- **Metrics on the validation set:** precision, recall, mAP50 and mAP50-95.

The losses are what the optimiser minimises. The metrics are what you care about. They usually move together, but not always, so read both.

## Three shapes worth recognising

![Three panels of constructed train and validation loss curves over 200 epochs. Left, healthy: both fall and flatten with a small steady gap. Middle, overfitting: training loss keeps falling while validation loss reaches a minimum and then rises, with a dashed line marking the best validation point. Right, not finished: both curves are still falling at the last epoch.](img:reading-yolo-training-curves-shapes.png "Constructed curves, not a real run. The gap between the two curves, and what the validation curve does late in training, tell you whether to stop earlier, train longer or change the data.")

### Healthy

Training and validation losses both fall and then flatten, with a modest, stable gap between them. Validation mAP rises and plateaus. More epochs would not help much; to improve further, change the data or the model, not the schedule.

### Overfitting

Training loss keeps falling while validation loss stops falling and starts to rise, and validation mAP plateaus or falls. The model is memorising the training set. Common causes and fixes:

- **Too little or too repetitive data,** for example many near-identical video frames. See [Deduplicating Video Frames Before Labelling](post:deduplicating-video-frames-before-labelling).
- **Too large a model** for the amount of data. Try a smaller one.
- **Too little augmentation.** See [Data Augmentation for Object Detection](post:data-augmentation-for-detection).
- **Too many epochs.** Stop earlier, or rely on early stopping.

[How to Spot Overfitting in Object Detection](post:spotting-overfitting-in-detection) goes deeper.

### Not finished

Both curves are still falling clearly at the last epoch, and mAP is still rising. Train longer. If time is limited, it is better to know the model is under-trained than to conclude that the approach does not work.

## Other patterns

- **Validation loss far above training loss from the start.** The validation set differs from the training set: different cameras, conditions or label conventions. That may be intended (a deliberately harder held-out set) or a sign of a labelling mismatch. Check that both follow the same guide.
- **Metrics stuck near zero.** Usually a data problem: labels in the wrong format, class IDs that do not match the class list, coordinates not normalised, or images and labels mismatched. Look at the training batch images Ultralytics saves in the run folder, with labels drawn on them. If the boxes there are wrong, everything else is too.
- **Very noisy validation metrics.** A small validation set. One image more or less changes the metrics. Treat small differences between epochs as noise. See [Comparing Two Detectors Fairly](post:comparing-two-detectors-fairly).
- **Precision high, recall low, flat.** The model is conservative, often because of missing labels: unlabelled objects in training images teach the model that those objects are background. See [Annotation Mistakes That Quietly Ruin Your Model](post:annotation-mistakes-that-hurt-models).
- **One loss falls, another does not.** If box loss falls but classification loss stays high, the model finds objects but confuses classes; check class definitions and balance.

## Things that look odd but are normal

- **A bump in the first few epochs.** Ultralytics uses a learning-rate warm-up at the start of training (three epochs by default at the time of writing). Early curves can move unevenly.
- **A change near the end.** By default, Ultralytics turns off mosaic augmentation for the last few epochs (`close_mosaic`, 10 by default at the time of writing). Training images suddenly look more like validation images, and losses and metrics often jump slightly. This is expected.
- **Training loss above validation loss.** Augmentation makes training images harder than validation images, so training loss can be higher, especially early on. It is not a bug.

Defaults change between versions, so check the documentation or the `args.yaml` saved in your run folder for the values actually used.

## Which weights to keep

Ultralytics saves `last.pt` (the final epoch) and `best.pt`. The best epoch is chosen by a fitness score computed from validation metrics, which in current versions weights mAP50-95 much more heavily than mAP50. That is a sensible default but not necessarily your criterion. If you care about recall at a fixed precision, or about one class, evaluate a few candidate epochs on your own criterion. See [What mAP Hides](post:what-map-hides).

Note too that "best on validation" is chosen using the validation set, so its validation score is slightly optimistic. Confirm on a separate test set. See [Why Your Test Set Flatters You](post:why-your-test-set-flatters-you).

## Early stopping and epoch budgets

Ultralytics has a `patience` setting: training stops if the fitness has not improved for that many epochs. It saves time on runs that have plateaued, but stopping is triggered by noisy validation metrics, so a very small patience can stop too early on small validation sets.

Use the curves from one full run to set the budget for the next ones. If the healthy plateau starts around epoch 120, there is little reason to train for 300 next time with the same data and model. When you change data volume or model size significantly, run long once again and look.

## Compare curves across runs

Curves are most useful side by side. Overlay validation mAP from two runs that differ in one thing: data version, augmentation, model size. An experiment tracker makes this easy; see [Experiment Tracking: TensorBoard, Weights & Biases and MLflow](post:experiment-tracking-tensorboard-wandb-mlflow). Look for differences in the shape, not only the final number: a run that reaches the same mAP in half the epochs, or that overfits later, tells you something.

## Checklist

- Read losses and validation metrics, not just final mAP.
- Recognise healthy, overfitting and unfinished shapes.
- Check the saved training batch images when metrics stay near zero.
- Expect warm-up bumps and an end-of-training change from mosaic closing.
- Choose the epoch by your own criterion if it differs from the default fitness.
- Confirm the chosen weights on a separate test set.
- Set epoch budgets and patience from full runs.
- Compare curves across runs that differ in one thing.

Next steps: [How to Spot Overfitting in Object Detection](post:spotting-overfitting-in-detection) and [Reproducible Training Runs](post:reproducible-training-runs).
