# Knowledge Club 3D

A scroll-driven 3D rebuild of knowledgeclub.com. Every page shares one Three.js world: the Knowledge Club emblem (kept in its original white), a camera that flies one stop per section, pentagon shards along the path and an emblem portal at the end of each page.

## Pages

`site/` holds the finished static site (20 pages):

- `index.html`, `about.html`, `speakers.html`, `events.html`, `highlights.html`, `contact.html`, `join.html`
- `event-<slug>.html` for each of the 10 events in the 2026–2027 season
- `blog-<slug>.html` for the 3 blog posts (summary plus a link to the full article)

## Editing

Content lives in `build.py` (events, speakers, offices, posts) and `data/` (countries, highlight galleries). After editing, regenerate the pages:

```
python3 build.py
```

Shared code: `site/css/site.css`, `site/js/scene.js` (3D world), `site/js/site.js` (navigation, reveals, carousels, countdowns, forms).

## Deploying to Cloudflare Pages

- Framework preset: None
- Build command: leave empty (the pages are already built and committed)
- Build output directory: `site`
