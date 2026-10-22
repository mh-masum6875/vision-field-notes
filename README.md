# Vision Field Notes

Source for the blog at https://mh-masum6875.github.io/vision-field-notes/ — practical computer vision and edge AI.

## Write a post

Add `content/posts/<slug>.md` with front matter:

```
---
title: "Post title"
description: "140-160 character summary"
category: "Datasets and Training"
date: 2026-10-22
tags: [yolo, training]
---
```

Link another post with `[text](post:other-slug)`. Link a product with `[text](aff:key)`; keys live in `affiliates.json`.

## Build

```
pip install markdown pyyaml jinja2
python build.py
```

The site is written to `docs/` (served by GitHub Pages from `main` / `docs`).

## Settings

`site.json` holds the site name, author, base URL, contact email and the AdSense IDs. Leave the AdSense fields empty until the site is approved; ads and the consent banner appear only when they are set.
