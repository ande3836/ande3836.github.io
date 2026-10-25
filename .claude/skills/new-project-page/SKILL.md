---
name: new-project-page
description: Add a new project to the portfolio — create its detail page from the template and add its card to the Selected Projects carousel in index.html. Use when Andrew says to add, write up, or showcase a new project.
disable-model-invocation: true
argument-hint: "[project name] [optional: dates or category]"
---

# Add a project page

Adds one project: a detail page built from `template.html` (in this skill's folder) and a matching card in `index.html`.

## 1. Gather the content

Get these from Andrew's message, attached files, or by asking. Ask everything that's missing in one message:

- **Title** (e.g. "Western Filament Coating Line") and a **slug** for the file name: lowercase-with-hyphens (`western-filament.html`)
- **Dates or category** for the small label above the title (e.g. "Aug 2026 – May 2027" or "Senior Design")
- **Subtitle**: one short line (e.g. "Mechanical Design & Prototyping")
- **Summary**: two short paragraphs in Andrew's voice (first person is fine; keep his wording when he provides it)
- **Tools/skills** for the badges (3–5)
- **Main image** plus alt text describing what it shows
- **Optional PDFs** (report, poster, journal) with a heading for each

Never invent facts, numbers, dates, or results. If something is unknown, ask or leave it out.

## 2. Add the assets

- Images go in `images/` with lowercase-hyphen names (`images/western-filament-assembly.jpg`). Resize anything wider than 1400px and save JPEGs at quality ~82 (Pillow is fine). Convert opaque PNG photos to JPEG.
- PDFs go in the repo root. If a PDF is over ~5 MB, offer to compress it (downsample scanned pages to ~150 dpi) before adding it.

## 3. Create the page

Copy `template.html` to `<slug>.html` in the repo root and replace every `{{PLACEHOLDER}}`:

- `{{TITLE}}`, `{{SLUG}}`, `{{SUBTITLE}}`, `{{DATES_OR_CATEGORY}}`
- `{{META_DESCRIPTION}}`: one sentence, about 150 characters, saying what the project was and what Andrew did
- `{{IMAGE}}` (file name inside `images/`), `{{IMAGE_ALT}}`
- `{{SUMMARY_PARAGRAPH_1}}`, `{{SUMMARY_PARAGRAPH_2}}`
- One `<span class="badge bg-secondary me-1">` per tool
- The document section: one block per PDF, or delete the whole section if there are none

When done, `grep '{{' <slug>.html` must return nothing.

## 4. Add the card to index.html

Inside `<section id="projects">` → `.swiper-wrapper`, add a `swiper-slide` copied from an existing card. Put it in date order, newest first. Update:

- both `href`s to `<slug>.html`
- the image `src="images/..."` and its `alt`
- `.date-text` (same label as the page), the `<h3 class="subtitle">` title, and a one-sentence description
- keep `loading="lazy"` on the image

## 5. Check it

1. The link-check hook runs automatically after edits. Fix anything it reports.
2. Preview with `python3 -m http.server 8000` and open `http://localhost:8000/<slug>.html`. If the Playwright MCP is available, screenshot the new page and the projects carousel at 390px and 1440px wide and look for overflow or broken images.
3. Don't commit or push. Tell Andrew it's ready and that `/publish` will put it live.
