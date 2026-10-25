---
name: publish
description: Check the portfolio for broken links and oversized files, commit the changes with a real message, and push to main so GitHub Pages deploys the live site.
disable-model-invocation: true
argument-hint: "[optional: what changed]"
---

# Publish the site

Pushing to `main` deploys https://ande3836.github.io within about a minute, so this only runs when Andrew invokes it.

## 1. Pre-flight

1. `git status` and `git diff --stat` to see what changed. If nothing changed, say so and stop.
2. Run the link checker across every page:
   `bash .claude/hooks/run.sh check_links.py`
   If it reports anything, fix it (or ask Andrew) before continuing. Don't publish broken links.
3. Look for large new or changed files: anything over 5 MB (`git diff --cached --stat` after staging, or `find . -size +5M -not -path './.git/*'`). Offer to compress images (≤1400px wide, JPEG ~82) or scanned PDFs (~150 dpi) before publishing.
4. Make sure no `{{PLACEHOLDER}}` text is left: `grep -l '{{' *.html` should return nothing.

## 2. Confirm

Show Andrew a short summary of what will go live (pages changed, files added or removed) and the commit message you plan to use. Wait for a yes, unless he already said to ship it without asking.

Commit message style: imperative and specific, e.g. "Add Western Filament project page" or "Fix hero overlap and compress images". Never "Add files via upload".

## 3. Commit and push

1. `git add -A` (the `.claude/` folder, `CLAUDE.md`, and `.mcp.json` are meant to be committed).
2. `git commit -m "<message>"`
3. If the current branch is `main`, run `git push origin main`. If it's another branch, push it and open a pull request into `main` with `gh pr create` instead.
4. Never force-push. A hook blocks it.

## 4. Confirm the deploy

If `gh` is available, run `gh run watch` (or `gh run list --limit 1`) to confirm the "Deploy static content to Pages" workflow finished. Then tell Andrew it's live at https://ande3836.github.io. Mention that a hard refresh may be needed to see CSS changes.
