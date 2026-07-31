# OCG Financial — Website

Static, dependency-free website for OCG Holdings LLC, d/b/a OCG Financial.
The design system (dark charcoal + gold, Cormorant Garamond / Inter) originates
from the approved homepage and is shared across every page via
`assets/css/styles.css` and `assets/js/main.js`.

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
