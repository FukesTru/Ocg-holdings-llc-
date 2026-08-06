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
| `about.html`, `contact.html`, `faqs.html`, `industries.html`, `client-results.html`, `resources.html` | Core pages |
| `privacy-policy.html`, `terms-of-service.html` | Legal |
| `services/*.html` | Four service pages: bookkeeping, fractional CFO, business funding, tax preparation |
| `locations/index.html` | Markets hub |
| `locations/*.html` | Eight market pages: New York City, San Francisco, Boston, Chicago, Dallas, Miami, Los Angeles, Washington DC |
| `resources/*.html` | Long-form guides |
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

**Contact form.** `contact.html` posts to FormSubmit, which relays messages
to oscar@ocgfinancial.com. No account or API key is needed, but the *first*
submission triggers a one-time activation email to that address — click the
link in it once and every later submission arrives automatically. To swap in
a GoHighLevel embed at final handover, replace the `data-endpoint` attribute
on the form (or the whole panel; it is sized so the change needs no layout
work).

**Still to come.**

- Video embeds for the three reserved slots near the top of `/resources`.
- The logo is a vector re-creation of the supplied artwork; swap in the
  original file (see above) if exact reproduction matters.

**Domain.** Canonical URLs, `sitemap.xml`, and structured data all point at
`https://www.ocgfinancial.com/`, which is where this site is intended to
live. No change needed. If it is ever served from a different domain, those
three places must be updated together.

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
