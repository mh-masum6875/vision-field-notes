---
title: "When Synthetic Data Helps a Detector and When It Wastes a Month"
description: "Rendered and composited training data can fill gaps real footage will not. It can also teach a model shortcuts that break in production."
category: "Datasets and Training"
date: 2026-11-26
tags: [synthetic-data, training, datasets, augmentation]
---

Synthetic data gets proposed whenever a dataset is hard to collect: rare events, dangerous situations, or anything a client will not let you photograph. Sometimes it is exactly right. Sometimes it produces a model that scores well on your validation set and falls over on the first real frame.

The difference usually comes down to what kind of gap you are filling.

## Three things people mean by synthetic

**Compositing** — cutting real objects out of real photographs and pasting them onto real backgrounds, with some blending. Cheap, fast, and the pixels are genuine.

**Rendering** — building the scene in Blender or a game engine and producing images with perfect labels. Expensive to set up, unlimited once it works, and the pixels are not real.

**Generative** — using a diffusion model to produce images from prompts or to vary existing ones. Cheap per image, very hard to control, and labels are a problem because you do not know exactly what you generated.

These fail differently and it is worth not treating them as one option.

![A scatter plot with control over what the labels say on the horizontal axis and how real the pixels are on the vertical. Compositing sits top right, with genuine photographic pixels and partial label control, described as real objects on real backgrounds where blending seams are the risk. Rendering sits bottom right, with exact labels by construction but a rendered look, described as perfect labels and unlimited volume but expensive to set up. Generative sits upper left, with fairly real pixels but almost no label control, described as cheap per image, hard to control, and labels are the problem. The top right quadrant is shaded and marked as real pixels and trustworthy labels.](img:synthetic-data-for-detection-three-kinds.png "Positions are judgements from the post, not measurements. They exist to make the trade-off explicit rather than to rank the three.")

Nothing sits in the top-right corner, and that is the honest summary. Each approach gives up one of the two things you want. Compositing keeps real pixels and loses some label precision at the seams. Rendering gives exact labels and loses photographic realism. Generative gives cheap volume and loses both control and labels.

Choosing is therefore not about which is best. It is about which of those two losses your problem can absorb.

## The gap that synthetic data fills well

Synthetic data is good at **coverage of configurations**.

If your detector has seen forklifts from the side but never from above, and you have a forklift model, rendering overhead views fills a genuine hole. If you need a person lying down and your real footage contains only people standing, compositing or rendering gets you examples you could not otherwise obtain ethically.

It is also good at **rare combinations**. Fire at night in rain is hard to collect and easy to render. Safety violations are hard to collect precisely because the people being filmed know they are being filmed.

In both cases you are teaching the model that a thing can appear in a configuration it has not seen. That transfers.

## The gap it fills badly

Synthetic data is bad at **sensor characteristics**.

Real footage from a specific camera has a specific noise profile, a specific compression signature, specific lens softness at the edges, and specific colour rendering. Rendered images have none of that, and a model trained on them learns to rely on a cleanliness that production frames do not have.

This is where the month goes missing. The validation set, also synthetic, says 0.94 mAP. The real footage says something much worse, and the gap is not fixable by training longer.

## The shortcut problem

The specific failure to watch for is the model learning the generation process rather than the object.

If every composited person is pasted with a slightly different edge sharpness from the background, the model can learn "detect the blending seam" instead of "detect a person". It will score beautifully on held-out synthetic data, because that data has the same seams, and score terribly on real frames that have none.

The tell is a large gap between synthetic validation and real validation that does not close with more synthetic data. If adding 10,000 more rendered images moves your real-footage score by nothing, you are training on an artefact.

## How to use it without getting burned

**Always mix.** Train on synthetic plus real together, never synthetic alone. Even a small amount of real data anchors the model to real sensor characteristics. Many people find a modest fraction of synthetic data helps and a large fraction hurts; the right ratio is specific to your problem and worth finding empirically rather than assuming.

**Always validate on real.** Your validation and test sets must be real footage from the deployment cameras. If you cannot get enough real data for a test set, you cannot responsibly claim the model works, and no amount of synthetic data changes that.

**Degrade deliberately.** Add the noise, compression and blur the real camera produces. Encoding your rendered frames through the same codec and bitrate as the production stream is a cheap, surprisingly effective step.

**Randomise what you do not care about.** Lighting, texture, background, object pose, camera angle. The point is to make the model unable to use those as cues, so it has to use the object's actual shape.

**Check the failure modes by hand.** Run the trained model on real footage and look at what it gets wrong. Shortcut learning is usually obvious once you see the errors: the model fires on the wrong things in a consistent, explicable way.

## A reasonable decision rule

Ask what is missing from your real dataset.

If the answer is "examples of a configuration we cannot photograph", synthetic data is a good tool and worth the setup cost.

If the answer is "enough data from our cameras", synthetic data is the wrong tool. Collect more real footage, or use hard negative mining on production frames, or label more of what you already have.

If the answer is "any data at all, we have none", be careful. A system trained entirely on synthetic data with no real validation is not a system you can make claims about, and that is a commercial risk as much as a technical one.
