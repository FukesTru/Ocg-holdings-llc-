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
| `index.html` | Homepage (approved design, expanded with industries/FAQ/insights previews) |
| `about.html`, `contact.html`, `faqs.html`, `industries.html`, `case-studies.html`, `resources.html` | Core pages |
| `privacy-policy.html`, `terms-of-service.html` | Legal |
| `services/*.html` | Six dedicated service pages (CFO, bookkeeping, tax, funding, strategy, fractional CFO) |
| `locations/index.html` | Service-locations hub (nationwide) |
| `locations/*.html` | 14 city SEO landing pages — national: New York, Los Angeles, Chicago, Dallas, Houston, Atlanta, Austin, Denver; Florida: Miami, Orlando, Tampa, Jacksonville, Fort Lauderdale, West Palm Beach |
| `resources/*.html` | Insight articles |
| `sitemap.xml`, `robots.txt` | SEO plumbing (canonical base: `https://www.ocgfinancial.com/`) |

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

No build step is required to serve the site — it is plain HTML/CSS/JS.
