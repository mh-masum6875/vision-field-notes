---
title: "Thermal Cameras for Detection: What Transfers and What Does Not"
description: "Thermal sees through darkness and smoke, and sees none of the texture your detector learned from. What changes when you swap the sensor."
category: "Edge Hardware and Deployment"
date: 2027-01-10
tags: [thermal, cameras, detection, training, deployment]
---

Thermal imaging solves problems visible-light cameras cannot. It works in total darkness without illumination, sees through smoke and light fog, and is largely indifferent to glare and headlights. For perimeter security, maritime work and anything involving fire, it is often the right sensor.

Then you point your detector at it and get nothing useful, because almost everything the model learned is absent.

## What the model loses

A COCO-trained detector recognises a person partly by shape and partly by an enormous amount of texture and colour: faces, clothing patterns, hair, the relationship between skin and fabric. A thermal frame has none of that. It has a warm shape against a cooler background, rendered in a false-colour palette or greyscale.

Shape survives. Everything else does not. A detector that relies on texture will fail, and fine-tuning on a handful of thermal images will not fix it — the gap is too large.

In practice this means a thermal deployment needs a model trained on thermal data. Public thermal detection datasets exist and are far smaller and less varied than visible-light ones, so expect to collect and label your own for anything beyond the common classes.

## The palette is a trap

Thermal cameras output a false-colour image, and the palette is a display setting. White-hot, black-hot, ironbow, rainbow — same sensor data, completely different pixels.

![Four renderings of one synthetic thermal scene containing a standing person and a vehicle with a hot engine bay. White-hot shows warm objects bright on a dark background; black-hot inverts it; ironbow runs dark purple through red and orange to white; rainbow runs blue through green and yellow to dark red. A green circle marks the same pixel on the person's head in each panel. Below each panel, a colour swatch and its value: RGB 172, 172, 172 for white-hot, RGB 83, 83, 83 for black-hot, RGB 232, 120, 13 for ironbow, and RGB 251, 182, 55 for rainbow.](img:thermal-cameras-for-detection-palette-trap.png "A synthetic temperature field, not a real capture. The sensor reading at the circled pixel is identical in all four panels at 38.8 °C. The numbers underneath are what the detector actually receives.")

Look at what the detector gets. One point on one scene, at one temperature, arrives as `172, 172, 172` under white-hot and `232, 120, 13` under ironbow. Nothing in the convolution stack knows those are the same measurement. As far as the model is concerned, somebody swapped the sensor.

Train on ironbow and deploy on a camera set to white-hot and your model will fail entirely. This catches people because the palette is changed in the camera's web interface by whoever set it up, often for human viewing preference, with no idea it matters.

Two defences. Fix the palette in the camera configuration and document it as a deployment requirement. Or, better, convert to single-channel greyscale before inference so the palette becomes irrelevant — then train on greyscale too.

If the camera can output raw radiometric data rather than a rendered image, that is better still, because you get actual temperature values rather than a visualisation of them.

## Thermal contrast is the weather now

With a visible camera you worry about light. With thermal you worry about the temperature difference between the subject and the background.

A person on cold ground at night is a bright, unambiguous shape. The same person on tarmac that has been in the sun all day, when air temperature is near body temperature, can be nearly invisible. Detection performance varies with ambient temperature, time of day and season in ways that have no equivalent in visible-light work.

This matters for how you test. A system validated in January on a British site may behave very differently in July. If you are quoting on performance, specify the conditions, and collect evaluation footage across the temperature range the site will actually see.

## What it is genuinely good at

**Darkness** without any illumination, which also means without the IR floodlight that tells everyone where your camera is.

**Smoke and fire**, where visible cameras are blind and thermal is at its most useful. Hot-spot detection is largely a thresholding problem rather than a detection problem.

**Glare and headlights**, which wreck visible-light detection at vehicle entrances and barely affect thermal.

**Camouflage and foliage**, where a warm body is obvious regardless of how well it matches the background visually.

**Privacy**, which is worth raising with clients. A thermal frame generally does not identify an individual. In workplaces and residential settings that can be the difference between a project being approved and not.

## What it is bad at

**Classification beyond coarse categories.** Thermal will tell you "person" reliably and "person wearing a high-visibility vest" not at all, because the vest is the same temperature as the jacket.

**Anything requiring text or colour.** No plate reading, no container codes, no colour-based rules.

**Resolution per pound.** Thermal sensors are dramatically more expensive per pixel. A 640×480 thermal camera costs what a very good 4K visible camera costs. That changes what you can detect at distance, and it changes the project budget.

**Glass.** Thermal does not see through ordinary glass, which surprises people planning to watch through a window.

## The usual answer is both

Many serious deployments pair a thermal and a visible camera on the same mount, and that is usually the right design rather than a compromise.

Thermal does the detection — reliable in all conditions, immune to lighting. Visible does the identification and the classification, and provides footage a human can interpret and that stands up as evidence.

The engineering cost is the registration between them: a transform that maps a detection in the thermal frame to the corresponding region in the visible frame. With fixed cameras this is a one-off calibration and it is worth doing properly, because every downstream feature depends on it.

If you are specifying a system and the requirement is "detect intrusion at night and tell us who it was", one sensor will not do both well. Say so during the specification rather than after the install.
