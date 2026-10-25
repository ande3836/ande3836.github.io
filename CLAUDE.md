# Andrew De La Vara — portfolio site

Personal portfolio for Andrew De La Vara (mechanical engineering, CU Boulder, May 2027), live at https://ande3836.github.io. Audience: recruiters and hiring managers, often on a phone via LinkedIn.

## How it's built
- Plain static HTML. No build step and no package.json. Bootstrap 5.3, Swiper 11, AOS 2.3 and Font Awesome load from CDNs.
- Pages: `index.html` (everything on one page) plus one detail page per project: `frisco-transit-center.html`, `air-track.html`, `dynatronics.html`, `Parkinsons.html`.
- All custom CSS lives in `style.css`. Don't add `<style>` blocks or `!important` overrides to pages. Fix the rule in `style.css` instead.
- Deploy: pushing to `main` runs `.github/workflows/static.yml`, which checks links and then publishes the repo to GitHub Pages. A push to `main` is a live deploy.

## Preview locally
`python3 -m http.server 8000` (or `python -m http.server 8000` on Windows), then open http://localhost:8000. Opening the HTML files directly also works because every path is relative.

## Conventions
- Images go in `images/`, named lowercase-with-hyphens, ≤1400px wide, JPEG quality ~82. PDFs live in the repo root. Keep existing PDF names because people may have links to them. Keep scanned PDFs under ~5 MB.
- Use relative paths only (`images/foo.jpg`, not `/images/foo.jpg` or names with spaces).
- Every page needs a `<title>`, meta description, canonical, and Open Graph tags (copy the block from an existing page). Every image needs real alt text.
- Rows directly inside `.container` use `g-4 g-lg-5`, never bare `g-5`, which causes sideways scrolling on phones.
- AOS reveal states in `style.css` are scoped to `.aos-init` so content still shows if the CDN fails. Keep it that way for new animations.
- `resume.pdf` is the resume linked from the site. Replace that file to update it rather than adding a second copy.
- Copy is Andrew's. Don't invent dates, results, or numbers. Ask.

## Claude Code setup in this repo
- `/new-project-page`: scaffold a project page from the template and add its carousel card.
- `/publish`: link check, size check, commit with a real message, push to `main`.
- `site-reviewer` agent: read-only pre-share review (links, previews, weight, accessibility, mobile).
- Hooks (`.claude/settings.json`): after any edit, `check_links.py` verifies every local link, image, PDF and `#anchor`. Before any edit, `guard.py` blocks changes to the deploy workflow and force-pushes. Both run through `.claude/hooks/run.sh`, which finds Python on Windows, macOS or Linux.
- Playwright MCP (`.mcp.json`) lets Claude load the local preview in a real browser and screenshot it. On native Windows, if it fails to start, re-add it with `claude mcp add playwright -- cmd /c npx @playwright/mcp@latest`.
