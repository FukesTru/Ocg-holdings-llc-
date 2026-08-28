# OCG Financial — Website

Static, dependency-free website for OCG Holdings LLC, d/b/a OCG Financial.
The design system (dark charcoal + gold, Cormorant Garamond / Inter) originates
from the approved homepage and is shared across every page via
`assets/css/styles.css` and `assets/js/main.js`.

## Deploy on Vercel

The repo is ready to import as-is — no build step, no framework.

1. Go to [vercel.com/new](https://vercel.com/new) and sign in (with GitHub is easiest).
2. Import the `FukesTru/Ocg-holdings-llc-` repository (grant the Vercel GitHub
   app access to it if prompted).
3. Leave every setting at its default: Framework Preset **Other**, no Build
   Command, no Output Directory override. Click **Deploy**.
4. In under a minute you'll get a live `*.vercel.app` URL. Every future push
   to the production branch redeploys automatically; pushes to other branches
   get their own preview URLs.

`vercel.json` is already configured: **clean URLs** (pages are served at
`/about`, `/services/fractional-cfo`, etc. — all internal links use this
form), long-lived caching for `/assets/*`, and standard security headers.
To attach the real domain later, add it under Project → Settings → Domains
and update the canonical base (see below).

CLI alternative: `npm i -g vercel && vercel` from the repo root.

Local preview that mirrors Vercel's clean-URL behavior: `npx serve .`

## Structure

| Path | Purpose |
| --- | --- |
| `index.html` | Homepage |
| `about.html`, `contact.html`, `faqs.html`, `industries.html`, `client-results.html`, `tax-news.html` | Core pages |
| `privacy-policy.html`, `terms-of-service.html` | Legal |
| `services/*.html` | Four service pages: bookkeeping, fractional CFO, business funding, tax preparation |
| `locations/index.html` | Markets hub |
| `locations/*.html` | Eight market pages: New York City, San Francisco, Boston, Chicago, Dallas, Miami, Los Angeles, Washington DC |
| `resources/*.html` | Long-form guides |
| `api/tax-news.js` | Serverless RSS aggregator behind `/tax-news` |
| `build/` | Sources the pages are generated from (see "Editing the site") |
| `scripts/fetch-images.sh` | Pulls images off the Wix CDN and hosts them locally |
| `vercel.json` | Clean URLs, caching, security headers, and 301s for retired URLs |
| `sitemap.xml`, `robots.txt` | SEO plumbing (canonical base: `https://www.ocgfinancial.com/`) |

Retired URLs (the old six-service and fourteen-city structure, `/videos`,
`/case-studies`) 301-redirect to their replacements via `vercel.json`.

## Brand logo

The header/footer lockup is an inline SVG (arc + rising bars + breakout arrow,
"OCG" wordmark, rules-flanked "FINANCIAL"), rebuilt as vector art so it stays
sharp at any size and matches the site's gold gradient. A standalone copy lives
at `assets/img/ocg-logo.svg`; the favicon uses the mark alone.

To use the original raster artwork instead, drop the file at
`assets/img/ocg-logo.png` and replace the `<svg class="brand-logo">…</svg>`
block in the header and footer of each page with:

```html
<img class="brand-logo" src="/assets/img/ocg-logo.png" alt="OCG Financial">
```

## Notes before launch

**Images are still hosted on Oscar's Wix CDN.** The founder photo and the
nine client logos load from `static.wixstatic.com`. When the old Wix site is
taken down those URLs stop working and the images disappear. Fix it with one
command, from any machine with normal internet access:

```bash
bash scripts/fetch-images.sh
```

That downloads all ten images into `assets/img/`, repoints every page at the
local copies, and verifies nothing still references the CDN. Commit the
result. The script is safe to re-run and makes no changes unless every
download succeeded.

**Contact form and chat.** Both are live GoHighLevel embeds, so submissions
land in the GHL account rather than anywhere in this repo.

- The form ("Website Form (Ocg financial)") appears on `contact.html` and on
  all eight market pages. Its markup comes from `ghl_form()` in
  `build.py`, and `form_embed.js` is included only on the pages that render
  it. To point at a different form, change `GHL_FORM_ID` at the top of
  `build.py` and rebuild.
- The chat widget loads on every page from the footer; its ID is
  `CHAT_WIDGET_ID` in `build.py`.

The form's own colors, fields, and copy are controlled in GoHighLevel's form
builder, not here. If it renders light against the dark page, set the form
background to transparent (or dark) in GHL.

**Still to come.**

- The GHL form ID for "Subscribe for Tax & Financial Updates", if a
  subscribe form is ever wanted on the news pages. `ghl_subscribe()` and the
  `{{ghl_subscribe}}` token in `build.py` are wired and unused; set
  `GHL_SUBSCRIBE_FORM_ID` and drop the token into a fragment.
- Confirm the RSS feed URLs once (see "Tax News" above).
- The logo is a vector re-creation of the supplied artwork; swap in the
  original file (see above) if exact reproduction matters.

**Domain.** Canonical URLs, `sitemap.xml`, and structured data all point at
`https://www.ocgfinancial.com/`, which is where this site is intended to
live. No change needed. If it is ever served from a different domain, those
three places must be updated together.

## Tax News

`/tax-news` is populated at runtime from
`api/tax-news.js`, a Vercel serverless function that pulls the configured
RSS feeds, normalizes each item to `{ title, source, date, excerpt, link }`,
dedupes by link, sorts newest first and returns the top 20. Each feed is
fetched inside its own try/catch, and each source lists fallback URLs, so a
publisher moving or breaking one feed never takes down the rest.

Freshness comes from the CDN rather than a framework. The function sends
`Cache-Control: public, s-maxage=14400, stale-while-revalidate=86400`, which
is the direct equivalent of Next.js's `export const revalidate = 14400`:
Vercel serves a cached response for four hours, then refreshes in the
background while still serving the previous copy, so nobody waits on the
upstream feeds.

**Verify the feed URLs after the first deploy** by opening:

```
https://<your-domain>/api/tax-news?debug=1
```

It reports, per source, which candidate URL answered and why any failed.
Fix or replace any source showing zero items by editing `SOURCES` at the top
of `api/tax-news.js`. The URLs shipped are the conventional paths for each
publication but could not be reached from the build environment, so this
check is worth doing once.

Items are then narrowed by a relevance filter, since these publications
also run firm-management, staffing, conference and vendor stories that have
nothing to do with what OCG does. An item is kept only if its title or
excerpt touches tax, accounting and reporting, or the money mechanics of
running a business; events, awards, people moves and sponsored posts are
dropped. Both lists live in `TOPIC_PATTERNS` and `EXCLUDE_PATTERNS` at the
top of `api/tax-news.js`. Matching is deliberately strict: a headline needs
a genuinely domain-specific term, not a word that merely appears in
financial writing, and nothing off-topic is ever shown as a fallback — if
no item qualifies the page says so instead.

`?debug=1` reports fetched-versus-kept counts **and lists every rejected
headline**, which is the fastest way to tune the patterns against the live
feed: anything off-topic still appearing on the page means adding a term to
`EXCLUDE_PATTERNS`, and anything useful in the rejected list means adding
one to `TOPIC_PATTERNS`.

Excerpts are the feed's own summary, capped at ~150 characters — never the
full article body, and never machine-generated. Every headline links out to
the publisher. Feed text is rendered with `textContent`, never `innerHTML`,
so nothing in a third-party feed can inject markup into the page.

`package.json` exists only so Vercel installs `rss-parser` for this
function; the pages themselves still have no build step.

## Editing the site

The pages in this repo are **generated**. Do not hand-edit the HTML at the
root, in `services/`, `locations/`, or `resources/` — the next build will
overwrite it. Edit the sources in `build/` instead:

| Path | What it holds |
| --- | --- |
| `build/content/*.html` | The body copy of each page, one fragment per page |
| `build/manifest.py` | Page list, titles, meta descriptions, schema |
| `build/build.py` | Header, nav, footer, shared components, contact details |
| `build/gen_locations.py` | Per-market copy for the eight location pages |
| `build/qa.py` | Link, heading, metadata and asset checks |

Regenerate and verify:

```bash
cd build
python3 gen_locations.py   # only if you changed location copy
python3 build.py           # writes the HTML, sitemap.xml, robots.txt
python3 qa.py              # should print "All checks passed."
```

Python 3 with no third-party packages is the only requirement. Common edits:
the phone number, email, and booking link are constants at the top of
`build.py`; the client logo list and their destination URLs are in
`CLIENT_LOGOS` in the same file.

Serving the built site needs no build step — it is plain HTML, CSS, and JS.
