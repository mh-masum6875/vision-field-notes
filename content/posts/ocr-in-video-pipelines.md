---
title: "Reading Text from Video: Plates, Containers and Hull Numbers"
description: "OCR on a still scan is solved. OCR on a moving subject through a camera outdoors is not. What changes, and how to get a usable read rate."
category: "Video Analytics"
date: 2026-11-25
tags: [ocr, anpr, text-recognition, video-analytics, deployment]
---

Reading a number plate off a clean, flat, well-lit photograph is close to solved. Reading the same plate off a camera at the entrance to a yard, at night, on a vehicle doing 30 km/h, at an angle, through rain, is a different problem — and it is the one you are usually asked to solve.

The same gap shows up with shipping container codes, hull numbers on vessels, wagon numbers on rail, and serial plates on equipment. The text is standardised and the OCR model is not the hard part. Everything around it is.

## Detect, then crop, then read

The single biggest mistake is running OCR on the full frame. Modern text recognisers want a tight crop of a single text region at a reasonable resolution. Give one a 4K frame with a plate occupying 60 by 20 pixels and it will fail, slowly.

The pipeline that works is almost always three stages:

1. Detect the object — the vehicle, the container, the vessel
2. Detect the text region within it — the plate, the code panel
3. Recognise the characters in that crop

Stage two matters more than people expect. Going straight from vehicle to OCR means the recogniser has to find the text itself, inside a crop full of bumper, headlights and reflections. A dedicated text-region detector is small, fast and dramatically improves what the recogniser sees.

## Never read once

This is the part that separates a demo from a system.

A single frame gives you one reading, with whatever motion blur, glare and occlusion that frame happened to have. A moving subject gives you twenty frames. Read as many as you can and aggregate.

Track the object so you know which readings belong to the same subject. Then combine them. Per-character voting across frames works well: for each character position, take the most frequent prediction weighted by its confidence. A plate where frame 3 says `B` and frames 4 through 11 say `8` resolves correctly, where any single frame might not.

Aggregation is also what lets you report a confidence you can act on. "Nine of eleven frames agree" is a far more useful signal than one softmax score.

![Two panels. Left, a line chart of whole plates read correctly against the number of frames combined by majority vote, for three single-frame accuracies. The 80% line rises from 21% at one frame to 77% at twenty-one; the 90% line from 48% to 95%; the 95% line from 70% to 98%. All three climb steeply over the first five frames, then flatten below 100%. Right, a bar chart comparing one frame against fifteen voted frames at each accuracy: 21 against 75, 47 against 94, and 70 against 98.](img:ocr-in-video-pipelines-voting-across-frames.png "Simulated, not measured. Each plate gets its own per-character difficulty that holds across the whole pass, so a digit the camera renders badly reads the same wrong way every frame. Those are the reads voting cannot rescue, which is why the curves flatten short of 100% rather than reaching it.")

The shape of that is worth internalising. Most of the gain arrives in the first five frames, and a recogniser at 90% per character goes from reading half the plates to reading almost all of them. But the curves flatten below 100%, and the gap that remains is systematic: a character that is dirty, clipped or badly angled reads the same wrong way in every frame, and fifty votes for the wrong answer is still the wrong answer. Voting fixes noise. It does not fix geometry, and that is the next section.

## Use the format

These codes are not arbitrary strings. They have structure, and ignoring it throws away free accuracy.

ISO 6346 container codes are four letters, six digits, and a check digit computed from the rest. If your read fails the check digit, you know it is wrong before anyone downstream does — and you can often repair it, because the common confusions are predictable.

Number plates follow national formats. A UK plate has a fixed letter-digit pattern. If position three must be a digit, then an `O` there is an `0`, and a `B` is an `8`.

Build the format into the post-processing as a constraint, not as a validation step at the end. The classic confusion pairs — `0`/`O`, `1`/`I`/`l`, `5`/`S`, `8`/`B`, `2`/`Z` — resolve almost completely once you know which positions must be numeric.

## Geometry is worth more than a better model

A plate photographed at 40 degrees off-axis is hard for any recogniser. The fix is not a bigger model; it is a perspective correction before the crop reaches it.

If your text detector gives you a quadrilateral rather than an axis-aligned box, you can warp it to a rectangle with a four-point transform. This is cheap, it is deterministic, and it tends to improve read rates more than swapping recognition models.

Mounting geometry matters even more. A camera positioned to see plates close to head-on will outperform a better algorithm on a badly-placed camera, every time. If you are consulted before installation, that is where your influence is worth most.

## Exposure for text, not for the scene

A camera exposed so the whole scene looks pleasant will usually blow out a retroreflective number plate at night, because the plate returns the IR illuminator straight back at the lens.

Dedicated ANPR cameras solve this with a short shutter and strong IR, which makes the plate readable and the rest of the frame nearly black. That looks wrong to a human reviewing footage and is exactly right for the machine.

If you are stuck with a general-purpose camera, a second stream with different exposure settings is often available and worth asking for. Trying to recover a saturated plate in software is a losing battle.

## Measure read rate, not character accuracy

Character accuracy sounds like the right metric and is nearly useless operationally. 95% character accuracy on a seven-character plate means roughly a third of plates have at least one wrong character.

The metric that matters is the proportion of subjects for which you produced a fully correct code. Measure it on real footage, per site, and break it down by the conditions you expect: day, night, rain, and whatever is specific to your environment.

Then track two numbers separately. **Miss rate** — the subject passed and you produced nothing — and **error rate** — you produced a code and it was wrong. These have very different consequences. A miss usually means a human checks manually. A confident wrong read can open a barrier for the wrong vehicle, or bill the wrong customer. Tune your confidence threshold with that asymmetry in mind rather than optimising a single number.

## Where the time actually goes

If you are estimating this kind of project, the recognition model is rarely the long pole. Expect the time to go into camera placement and exposure tuning, the tracking and aggregation layer, the format-aware post-processing, and the test set that tells you whether any of it worked.

Budget for a site visit. Read rates vary enormously between installations that look identical on paper, and the only way to know is to collect footage from the actual camera in the actual position.
