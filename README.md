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

## Scheduling

A post is published on the `date` in its front matter. Posts with a future date are left out of the build. A GitHub Actions workflow rebuilds the site every day and on every content push, so scheduled posts go live on their own.

## Build

```
pip install markdown pyyaml jinja2
python build.py
```

The site is written to `docs/` (served by GitHub Pages from `main` / `docs`).

## Settings

`site.json` holds the site name, author, base URL, contact email and the AdSense IDs. Leave the AdSense fields empty until the site is approved; ads and the consent banner appear only when they are set.

## Search engines

- `docs/sitemap.xml` lists every published page; `docs/feed.xml` is an Atom feed of the latest 30 posts.
- Each post carries canonical, Open Graph and `article:*` tags and Article + BreadcrumbList structured data. The home page carries WebSite and Person data.
- Add profile links (LinkedIn, Google Scholar, ORCID) to `same_as` in `site.json`; they are published as the author's `sameAs`.
- Set `google_site_verification` in `site.json` to the code from Google Search Console (URL-prefix property for the blog's address), then submit `sitemap.xml` there.
- New URLs are sent to IndexNow (Bing and others) after every rebuild.
