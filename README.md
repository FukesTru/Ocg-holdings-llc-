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
| `locations/*.html` | Six Florida SEO landing pages (Miami, Orlando, Tampa, Jacksonville, Fort Lauderdale, West Palm Beach) |
| `resources/*.html` | Insight articles |
| `sitemap.xml`, `robots.txt` | SEO plumbing (canonical base: `https://www.ocgfinancial.com/`) |

## Notes before launch

- Founder photo and client logos are hotlinked from OCG's Wix CDN — rehost locally.
- The contact form is handled client-side only; wire its submit to the CRM/booking backend.
- Video cards on the homepage are marked "Coming Soon" pending approved embeds.
- Update the canonical domain in every page's `<head>`, `sitemap.xml`, and `robots.txt` if the site is served from a different domain.

No build step is required to serve the site — it is plain HTML/CSS/JS.
