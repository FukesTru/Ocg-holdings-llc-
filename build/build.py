#!/usr/bin/env python3
"""Assemble the OCG Financial static site from shared partials + content fragments.

Fragments live in ./content/*.html and use {{p}} as the relative-path prefix
back to the site root ("" for root pages, "../" for subdirectory pages).
"""
import hashlib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")

BASE = "https://www.ocgfinancial.com/"
BOOK = "https://api.leadconnectorhq.com/widget/bookings/book-a-readiness-assessment-ca"

# Verified business contact details. OCG Financial has no public street
# address, so none is published and none appears in structured data.
PHONE_DISPLAY = "(210) 416-3919"
PHONE_TEL = "+12104163919"
EMAIL = "oscar@ocgfinancial.com"

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -2 108 78'%3E"
           "%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='0.35' y2='1'%3E"
           "%3Cstop offset='0%25' stop-color='%23f0d078'/%3E%3Cstop offset='100%25' stop-color='%23c9a13b'/%3E"
           "%3C/linearGradient%3E%3C/defs%3E%3Cg fill='url(%23g)'%3E"
           "%3Cpath d='M10,64 A40,40 0 0 1 72.9,31.2' fill='none' stroke='url(%23g)' stroke-width='11'/%3E"
           "%3Crect x='24' y='51' width='6' height='13'/%3E%3Crect x='33' y='41' width='6' height='23'/%3E"
           "%3Crect x='42' y='33' width='6' height='31'/%3E%3Crect x='51' y='39' width='6' height='25'/%3E"
           "%3Crect x='60' y='35' width='6' height='29'/%3E%3Crect x='69' y='45' width='6' height='19'/%3E"
           "%3Cpath d='M22,55 L36,43 L47,48 L60,34 L78,17' fill='none' stroke='url(%23g)' stroke-width='6' "
           "stroke-linecap='round' stroke-linejoin='round'/%3E"
           "%3Cpolygon points='90,6 85.1,23.7 72.3,10.9'/%3E%3C/g%3E%3C/svg%3E")

SERVICES = [
    ("bookkeeping", "Bookkeeping", "The foundation of financial clarity"),
    ("fractional-cfo", "Fractional CFO Services", "Strategic financial leadership"),
    ("business-funding", "Business Funding", "Capital readiness and preparation"),
    ("tax-preparation", "Tax Preparation", "Filed on clean, organized books"),
]
LOCATIONS = [
    ("new-york", "New York City", "NY"),
    ("san-francisco", "San Francisco", "CA"),
    ("boston", "Boston", "MA"),
    ("chicago", "Chicago", "IL"),
    ("dallas", "Dallas", "TX"),
    ("miami", "Miami", "FL"),
    ("los-angeles", "Los Angeles", "CA"),
    ("washington-dc", "Washington", "DC"),
]

# Brand lockup, inlined so the wordmark renders in the page's Inter webfont.
# To use a raster original instead, swap the <svg> for:
#   <img src="/assets/img/ocg-logo.png" alt="OCG Financial" width="176" height="51">
LOGO_SVG = """<svg class="brand-logo" width="268" height="78" viewBox="9 11 268 78" role="img" aria-label="OCG Financial">
      <defs><linearGradient id="ocgGold__UID__" x1="0" y1="0" x2="0.35" y2="1">
        <stop offset="0%" stop-color="#fbeab4"/><stop offset="28%" stop-color="#f0d078"/>
        <stop offset="58%" stop-color="#c9a13b"/><stop offset="100%" stop-color="#c9a13b"/>
      </linearGradient></defs>
      <g transform="translate(2,8) scale(0.92)" fill="url(#ocgGold__UID__)">
        <path d="M10,64 A40,40 0 0 1 72.9,31.2" fill="none" stroke="url(#ocgGold__UID__)" stroke-width="11"/>
        <rect x="24" y="51" width="6" height="13" rx="1"/><rect x="33" y="41" width="6" height="23" rx="1"/>
        <rect x="42" y="33" width="6" height="31" rx="1"/><rect x="51" y="39" width="6" height="25" rx="1"/>
        <rect x="60" y="35" width="6" height="29" rx="1"/><rect x="69" y="45" width="6" height="19" rx="1"/>
        <path d="M22,55 L36,43 L47,48 L60,34 L78,17" fill="none" stroke="url(#ocgGold__UID__)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
        <polygon points="90,6 85.1,23.7 72.3,10.9"/>
      </g>
      <text x="106" y="56" fill="url(#ocgGold__UID__)" font-family="Inter,Helvetica Neue,Arial,sans-serif" font-weight="800" font-size="46" letter-spacing="1.5">OCG</text>
      <rect x="107" y="76" width="14" height="2" fill="url(#ocgGold__UID__)"/>
      <text x="129" y="82" fill="url(#ocgGold__UID__)" font-family="Inter,Helvetica Neue,Arial,sans-serif" font-weight="500" font-size="15" letter-spacing="5.4">FINANCIAL</text>
      <rect x="256" y="76" width="14" height="2" fill="url(#ocgGold__UID__)"/>
    </svg>"""

LOGO_HEADER = LOGO_SVG.replace("__UID__", "h")
LOGO_FOOTER = LOGO_SVG.replace("__UID__", "f")


PIN = ('<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="1.6" aria-hidden="true" style="display:inline;vertical-align:-1px;margin-right:6px">'
       '<path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>')

CARET = ("<svg width='10' height='7' viewBox='0 0 12 8' fill='none' stroke='currentColor' "
         "stroke-width='1.5' aria-hidden='true'><path d='M1 1l5 5 5-5'/></svg>")



def asset_v(rel):
    """Content hash for cache-busting immutably-cached assets."""
    try:
        with open(os.path.join(ROOT, rel), "rb") as fh:
            return hashlib.md5(fh.read()).hexdigest()[:8]
    except FileNotFoundError:
        return "0"


CSS_V = None
JS_V = None


def clean_path(path):
    """Extensionless site path: index.html -> '', dir/index.html -> dir, foo.html -> foo."""
    if path.endswith("index.html"):
        path = path[: -len("index.html")].rstrip("/")
    elif path.endswith(".html"):
        path = path[: -len(".html")]
    return path


def clean_links(html):
    """Rewrite internal links to root-absolute clean URLs (Vercel cleanUrls)."""
    html = html.replace('href="/index.html', 'href="/')
    html = re.sub(r'(href="/[^":]+?)/index\.html(["#])', r"\1\2", html)
    html = re.sub(r'(href="/[^":]*?)\.html(["#])', r"\1\2", html)
    html = re.sub(r"(https://www\.ocgfinancial\.com/[^\"\s<]*?)\.html", r"\1", html)
    return html



# ---------------------------------------------------------------
# Shared content snippets (substituted into fragments by token)
# ---------------------------------------------------------------

def _proof(num, label, count=None, suffix="", prefix=""):
    if count is None:
        inner = num
    else:
        inner = ('<span data-count-to="%s" data-prefix="%s" data-suffix="%s">%s0%s</span>'
                 % (count, prefix, suffix, prefix, suffix))
    return ('    <div class="proof-item">\n'
            '      <span class="pnum">%s</span>\n'
            '      <div class="prule"></div>\n'
            '      <div class="plabel">%s</div>\n'
            '    </div>' % (inner, label))


# Homepage credibility band. Order is deliberate: strongest proof first,
# years of experience demoted to a supporting trust line.
PROOF_HOME = ('<div class="proof-band reveal">\n  <div class="proof-grid">\n'
              + "\n".join([
                  _proof(None, "Investor-Ready Reporting", count="100", suffix="%"),
                  _proof(None, "Client Monthly Recurring Revenue", count="84", prefix="$", suffix="M"),
                  _proof(None, "In Capital Raised", count="35", prefix="$", suffix="M+"),
                  _proof(None, "Average DSO Improvement", count="14", suffix=" Days"),
              ])
              + '\n  </div>\n'
                '  <div class="proof-foot">\n'
                '    <span class="pf-num"><span data-count-to="7" data-suffix="+">0+</span></span>\n'
                '    <span class="pf-lbl">Years of Financial Expertise</span>\n'
                '    <span class="pf-sep">·</span>\n'
                '    <span class="pf-lbl">Founder-Led Engagements</span>\n'
                '  </div>\n</div>')

# Fractional CFO page band.
PROOF_CFO = ('<div class="proof-band compact reveal">\n  <div class="proof-grid">\n'
             + "\n".join([
                 _proof("$0", "Full-Time CFO Overhead"),
                 _proof(None, "In Capital Raised", count="35", prefix="$", suffix="M+"),
                 _proof(None, "Investor-Ready Reporting", count="100", suffix="%"),
                 _proof(None, "Average DSO Improvement", count="14", suffix=" Days"),
             ])
             + '\n  </div>\n</div>')



# Hero stat panel: the four headline proof points, presented plainly.
HERO_STATS = """<div class="hero-stats">
  <div class="hero-stats-head"><span class="pulse-dot"></span> What Our Clients' Numbers Look Like</div>
  <div class="hero-stats-grid">
    <div class="hs-item">
      <span class="hs-num"><span data-count-to="100" data-suffix="%">0%</span></span>
      <div class="hs-rule"></div>
      <div class="hs-lbl">Investor-Ready Reporting</div>
    </div>
    <div class="hs-item">
      <span class="hs-num"><span data-count-to="84" data-prefix="$" data-suffix="M">$0M</span></span>
      <div class="hs-rule"></div>
      <div class="hs-lbl">Client Monthly Recurring Revenue</div>
    </div>
    <div class="hs-item">
      <span class="hs-num"><span data-count-to="35" data-prefix="$" data-suffix="M+">$0M+</span></span>
      <div class="hs-rule"></div>
      <div class="hs-lbl">In Capital Raised</div>
    </div>
    <div class="hs-item">
      <span class="hs-num"><span data-count-to="14" data-suffix=" Days">0 Days</span></span>
      <div class="hs-rule"></div>
      <div class="hs-lbl">Average DSO Improvement</div>
    </div>
  </div>
  <div class="hero-stats-foot">
    <span class="hsf-k">Measured across our client base</span>
    <span>Founder-led engagements, nationwide</span>
  </div>
</div>"""

# Bookkeeping page: the financial recovery path, drawn in on scroll.
JOURNEY = """<div class="journey reveal">
  <div class="journey-title"><span class="pulse-dot"></span> The Path to Financial Clarity</div>
  <div class="journey-track">
    <div class="jstep is-start">
      <div class="js-stage">Where most owners start</div>
      <h4>Unclear Numbers</h4>
      <p>Books behind, accounts unreconciled, and no confident answer to what the business actually earned last month.</p>
    </div>
    <div class="jstep">
      <div class="js-stage">Stage One</div>
      <h4>Clean-Up and Organization</h4>
      <p>Records rebuilt, every account reconciled to statement, and the chart of accounts restructured so the numbers mean something.</p>
    </div>
    <div class="jstep">
      <div class="js-stage">Stage Two</div>
      <h4>Reporting and Clarity</h4>
      <p>A monthly close on a schedule you can plan around, with statements formatted to be read rather than filed.</p>
    </div>
    <div class="jstep">
      <div class="js-stage">Stage Three</div>
      <h4>Cash Flow Visibility</h4>
      <p>Margin trends and cash movement become visible month to month, so pressure shows up early instead of arriving as a surprise.</p>
    </div>
    <div class="jstep is-end">
      <div class="js-stage">The Outcome</div>
      <h4>Stronger Decisions</h4>
      <p>Hiring, pricing, and inventory calls made against numbers you trust, with the reporting to back them up when someone asks.</p>
    </div>
  </div>
</div>"""

# Business funding page: readiness stages, no outcome promises.
FUNDING_PATH = """<div class="fund-path reveal">
  <div class="fp-title"><span class="pulse-dot"></span> How We Prepare You for Funding</div>
  <div class="fp-stages">
    <div class="fp-stage">
      <div class="fp-n">01</div>
      <div>
        <h4>Understand Your Options</h4>
        <p>Bank and SBA lending, lines of credit, equipment and inventory financing, or equity. We walk through which routes realistically fit your business.</p>
      </div>
    </div>
    <div class="fp-stage">
      <div class="fp-n">02</div>
      <div>
        <h4>Strengthen the Financial Picture</h4>
        <p>Books reconciled, statements aligned with tax filings, and a forward forecast built on assumptions you can defend in a meeting.</p>
      </div>
    </div>
    <div class="fp-stage">
      <div class="fp-n">03</div>
      <div>
        <h4>Prepare for Lender Conversations</h4>
        <p>Documentation assembled the way reviewers expect it, and you rehearsed on the questions that come up so nothing catches you cold.</p>
      </div>
    </div>
  </div>
  <div class="fp-note">Lenders and investors make their own decisions on approval, rates, and terms. Our work is to make sure your financial information is not the reason a conversation stalls.</div>
</div>"""



def short_form(city):
    """Compact working enquiry form for the market pages. Posts to the same
    relay as the contact page; swap data-endpoint for the GHL embed later."""
    return ('<div class="contact-form-panel reveal reveal-delay-1">\n'
            '  <h2 style="font-size:23px;">Talk to us about your %s business</h2>\n'
            '  <p style="font-size:16px;">Two fields and a sentence. We reply personally, usually within one business day.</p>\n'
            '  <form class="enquiry-form" novalidate="" data-endpoint="https://formsubmit.co/ajax/%s">\n'
            '    <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;opacity:0;height:0;width:0;">\n'
            '    <input type="hidden" name="_subject" value="New enquiry from the %s page">\n'
            '    <input type="hidden" name="_captcha" value="false">\n'
            '    <input type="hidden" name="market" value="%s">\n'
            '    <div class="form-grid">\n'
            '      <div class="form-field full">\n'
            '        <label for="lf-name-%s">Your Name</label>\n'
            '        <input type="text" id="lf-name-%s" name="name" placeholder="Jane Founder" required autocomplete="name">\n'
            '      </div>\n'
            '      <div class="form-field full">\n'
            '        <label for="lf-email-%s">Email</label>\n'
            '        <input type="email" id="lf-email-%s" name="email" placeholder="you@company.com" required autocomplete="email">\n'
            '      </div>\n'
            '      <div class="form-field full">\n'
            '        <label for="lf-msg-%s">What Do You Need Help With?</label>\n'
            '        <textarea id="lf-msg-%s" name="message" placeholder="Where are the numbers letting you down right now?" required style="min-height:104px;"></textarea>\n'
            '      </div>\n'
            '    </div>\n'
            '    <div style="margin-top:22px;">\n'
            '      <button type="submit" class="btn btn-gold" style="width:100%%;">Send Message</button>\n'
            '    </div>\n'
            '    <p class="form-error" role="alert">Something went wrong sending that. Please email '
            '<a href="mailto:%s">%s</a> or call <a href="tel:%s">%s</a> and we will pick it up straight away.</p>\n'
            '  </form>\n'
            '  <div class="form-success" role="status">\n'
            '    <div class="icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg></div>\n'
            '    <h3>Message received.</h3>\n'
            '    <p>Thanks. We will be in touch shortly.</p>\n'
            '  </div>\n'
            '</div>' % (city, EMAIL, city, city, slugify(city), slugify(city), slugify(city),
                        slugify(city), slugify(city), slugify(city),
                        EMAIL, EMAIL, PHONE_TEL, PHONE_DISPLAY))


def slugify(v):
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in v).strip("-")


def ghl_slot(kind, title, body, tall=False):
    ico = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="1.4" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/>'
           '<path d="M3 10h18M8 3v4M16 3v4"/></svg>' if kind == "calendar" else
           '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="1.4" aria-hidden="true"><path d="M4 5h16v14H4z"/><path d="M8 10h8M8 14h5"/></svg>')
    label = "Booking Calendar" if kind == "calendar" else "GoHighLevel Form"
    marker = ("[Insert approved booking calendar embed here]" if kind == "calendar"
              else "[Insert approved GoHighLevel form embed here]")
    return ('<div class="embed-slot%s reveal">\n'
            '  <span class="es-tag">%s</span>\n'
            '  <span class="es-ico">%s</span>\n'
            '  <h3>%s</h3>\n'
            '  <p>%s</p>\n'
            '  <code>%s</code>\n'
            '</div>' % (" tall" if tall else "", label, ico, title, body, marker))



# Approved client logos, all destinations confirmed by the client against
# the live ocgfinancial.com site.
CLIENT_LOGOS = [
    # (brand, website, Wix CDN filename, local filename)
    ("Vincero", "https://vincerocollective.com", "94493f_9b8fefa27fdb4c1fbe4af7fa2f279020~mv2.png", "vincero.png"),
    ("Craftmix", "https://www.craftmix.com", "94493f_27655ebc461446a09e292ea352749812~mv2.png", "craftmix.png"),
    ("Super Fiber", "https://getbellway.com/", "94493f_29518f81bf744da6b2cd99e9fa6f4ea8~mv2.jpg", "super-fiber.jpg"),
    ("Lusso Cloud", "https://lussocloud.com", "94493f_f7db1bc04c4b4baebe8741a312a3b156~mv2.png", "lusso-cloud.png"),
    ("Better with Age", "https://betterwithage.co/", "94493f_f72cf45097bd490f905d7d25cf45bdab~mv2.png", "better-with-age.png"),
    ("Day Out Protein Balls", "https://getdayout.com", "94493f_0d335c03c5e74f21ac92dfd41dc812b6~mv2.png", "day-out.png"),
    ("Kayode", "https://kayodepet.com/", "94493f_605e242e19be468b9bcc9cd5ba8a277d~mv2.png", "kayode.png"),
    ("The Vin Store", "https://thevin.store", "94493f_b436f97fa2f94875a85dd4ffab7ff211~mv2.png", "the-vin-store.png"),
    ("VK Energy Bar", "https://vkenergybar.com", "94493f_c46243acffe744688df97435dc59ca1a~mv2.png", "vk-energy-bar.png"),
]
CDN = "https://static.wixstatic.com/media/"
FOUNDER_CDN_FILE = "94493f_c55f573e540c4e2f833e636db76b9985~mv2.jpg"
FOUNDER_LOCAL = "oscar-cancino.jpg"


def hosted(local_rel, cdn_file):
    """Prefer a locally hosted image; fall back to the Wix CDN until the
    asset has been pulled down by scripts/fetch-images.sh. Once the local
    file exists, the build emits the local path and the CDN dependency is
    gone with no markup changes."""
    if os.path.exists(os.path.join(ROOT, "assets/img", local_rel)):
        return "/assets/img/" + local_rel
    return CDN + cdn_file



def logo_marquee():
    """Two identical logo sets so the -50% translate loops with no gap."""
    def one(name, url, img, local, dup):
        alt = "" if dup else name
        extra = ' aria-hidden="true" tabindex="-1"' if dup else ""
        inner = ('<img src="%s" alt="%s" loading="lazy" referrerpolicy="no-referrer" '
                 'width="140" height="70">' % (hosted("clients/" + local, img), alt))
        if url:
            return ('<a class="logo-slot" href="%s" target="_blank" rel="noopener"%s>%s</a>'
                    % (url, extra, inner))
        return '<div class="logo-slot no-link"%s>%s</div>' % (extra, inner)

    sets = []
    for dup in (False, True):
        sets.append("\n      " + "\n      ".join(
            one(n, u, i, l, dup) for n, u, i, l in CLIENT_LOGOS))
    return "".join(sets) + "\n    "


def head(meta):
    p = meta["prefix"]
    canonical = BASE + clean_path(meta["out"])
    schema_blocks = "\n".join(
        '<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False)
        for s in meta.get("schema", [])
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="OCG Financial">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/css/styles.css?v={CSS_V}">
{schema_blocks}
</head>
<body>
"""


def nav(meta):
    p = meta["prefix"]
    cur = meta.get("nav", "")

    def curattr(key):
        return ' aria-current="page"' if cur == key else ""

    svc_links = "\n".join(
        f'        <a href="{p}services/{slug}.html">{name}<span class="d-sub">{sub}</span></a>'
        for slug, name, sub in SERVICES
    )
    half = (len(LOCATIONS) + 1) // 2
    def loc_col(items):
        return "\n".join(
            f'          <a href="{p}locations/{slug}.html">{name}<span class="d-sub">{st}</span></a>'
            for slug, name, st in items
        )
    loc_panel = f'''<div class="drop-cols">
          <div>
{loc_col(LOCATIONS[:half])}
          </div>
          <div>
{loc_col(LOCATIONS[half:])}
          </div>
        </div>
        <a class="drop-all" href="{p}locations/index.html">All Markets We Serve →</a>'''
    m_svc = "\n".join(f'      <a href="{p}services/{slug}.html">{name}</a>' for slug, name, _ in SERVICES)
    m_loc = "\n".join(f'      <a href="{p}locations/{slug}.html">{name}</a>' for slug, name, _ in LOCATIONS)
    m_loc += f'\n      <a href="{p}locations/index.html" style="color:var(--gold);">All Locations →</a>' 

    return f"""<header id="siteHeader">
  <nav class="container" aria-label="Main">
    <a href="{p}index.html" class="brand" aria-label="OCG Financial home">{LOGO_HEADER}</a>
    <ul class="nav-links">
      <li><a href="{p}index.html"{curattr('home')}>Home</a></li>
      <li><a href="{p}about.html"{curattr('about')}>About</a></li>
      <li class="has-drop">
        <button class="nav-drop-btn" type="button" aria-expanded="false" aria-haspopup="true">Services {CARET}</button>
        <div class="drop-panel">
{svc_links}
        </div>
      </li>
      <li class="has-drop">
        <button class="nav-drop-btn" type="button" aria-expanded="false" aria-haspopup="true">Locations {CARET}</button>
        <div class="drop-panel wide">
        {loc_panel}
        </div>
      </li>
      <li><a href="{p}industries.html"{curattr('industries')}>Industries</a></li>
      <li><a href="{p}resources.html"{curattr('resources')}>Resources</a></li>
      <li><a href="{p}contact.html"{curattr('contact')}>Contact</a></li>
    </ul>
    <a href="{BOOK}" target="_blank" rel="noopener" class="btn btn-gold nav-cta">Schedule a Consultation</a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </nav>
</header>

<div class="mobile-menu" id="mobileMenu">
  <a href="{p}index.html">Home</a>
  <a href="{p}about.html">About</a>
  <div class="m-group">
    <button class="m-group-btn" type="button" aria-expanded="false">Services {CARET}</button>
    <div class="m-sub">
{m_svc}
    </div>
  </div>
  <div class="m-group">
    <button class="m-group-btn" type="button" aria-expanded="false">Service Locations {CARET}</button>
    <div class="m-sub">
{m_loc}
    </div>
  </div>
  <a href="{p}industries.html">Industries</a>
  <a href="{p}resources.html">Resources</a>
  <a href="{p}contact.html">Contact</a>
  <a href="{BOOK}" target="_blank" rel="noopener" class="btn btn-gold">Schedule a Consultation</a>
</div>
"""


def breadcrumbs(meta):
    crumbs = meta.get("crumbs")
    if not crumbs:
        return ""
    p = meta["prefix"]
    parts = [f'<a href="{p}index.html">Home</a>']
    for label, href in crumbs:
        parts.append('<span class="sep">/</span>')
        if href:
            parts.append(f'<a href="{p}{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "".join(parts) + "</nav>"


def breadcrumb_schema(meta):
    crumbs = meta.get("crumbs")
    if not crumbs:
        return None
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
    pos = 2
    for label, href in crumbs:
        item = {"@type": "ListItem", "position": pos, "name": re.sub(r"&amp;", "&", label)}
        item["item"] = BASE + clean_path(href if href else meta["out"])
        items.append(item)
        pos += 1
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def footer(meta):
    p = meta["prefix"]
    svc = "\n".join(f'          <li><a href="{p}services/{slug}.html">{name}</a></li>' for slug, name, _ in SERVICES)
    loc = "\n".join(f'          <li><a href="{p}locations/{slug}.html">{name}</a></li>' for slug, name, _ in LOCATIONS)
    loc += f'\n          <li><a href="{p}locations/index.html" style="color:var(--gold);">All Locations →</a></li>' 
    return f"""<footer>
  <div class="container">
    <div class="footer-cta reveal">
      <div>
        <h3>Ready to stop guessing about your numbers?</h3>
        <p>Book a readiness assessment and see exactly where your financial infrastructure stands.</p>
      </div>
      <a href="{BOOK}" target="_blank" rel="noopener" class="btn btn-gold">Schedule a Consultation</a>
    </div>
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="{p}index.html" class="brand" aria-label="OCG Financial home">{LOGO_FOOTER}</a>
        <p>Strategic finance for business owners who refuse to guess. Funding, CFO strategy, tax-related support, and bookkeeping, built by someone who's actually run a business.</p>
        <div class="li-row"><a href="https://www.linkedin.com/in/oscar-cancino-056694174/" target="_blank" rel="noopener">Oscar on LinkedIn →</a></div>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <ul>
          <li><a href="{p}about.html">About</a></li>
          <li><a href="{p}industries.html">Industries</a></li>
          <li><a href="{p}client-results.html">Client Results</a></li>
          <li><a href="{p}contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Services</h5>
        <ul>
{svc}
        </ul>
      </div>
      <div class="footer-col">
        <h5>Locations</h5>
        <ul>
{loc}
        </ul>
      </div>
      <div class="footer-col">
        <h5>Resources</h5>
        <ul>
          <li><a href="{p}resources.html">Insights</a></li>
          <li><a href="{p}faqs.html">FAQs</a></li>
        </ul>
        <h5 style="margin-top:26px;">Legal</h5>
        <ul>
          <li><a href="{p}privacy-policy.html">Privacy Policy</a></li>
          <li><a href="{p}terms-of-service.html">Terms of Service</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span id="year"></span> OCG Holdings LLC, d/b/a OCG Financial. All rights reserved.</p>
      <div class="footer-legal">
        <a href="{p}privacy-policy.html">Privacy Policy</a>
        <a href="{p}terms-of-service.html">Terms of Service</a>
      </div>
    </div>
  </div>
</footer>

<script src="{p}assets/js/main.js?v={JS_V}" defer></script>

</body>
</html>
"""


ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "name": "OCG Financial",
    "legalName": "OCG Holdings LLC",
    "url": BASE,
    "description": "Founder-led financial partner for business owners nationwide: fractional CFO services, bookkeeping, tax support, business funding, and financial strategy.",
    "areaServed": {"@type": "Country", "name": "United States"},
    "founder": {"@type": "Person", "name": "Oscar Cancino", "sameAs": "https://www.linkedin.com/in/oscar-cancino-056694174/"},
    "sameAs": ["https://www.linkedin.com/in/oscar-cancino-056694174/"],
    "telephone": "+12104163919",
    "email": "oscar@ocgfinancial.com",
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "sales",
        "telephone": "+12104163919",
        "email": "oscar@ocgfinancial.com",
        "areaServed": "US",
        "availableLanguage": "English",
    },
}


def build_page(meta):
    frag_path = os.path.join(CONTENT, meta["fragment"])
    with open(frag_path, encoding="utf-8") as f:
        body = f.read()
    meta = dict(meta, prefix="/")
    p = meta["prefix"]
    body = body.replace("{{p}}", p).replace("{{book}}", BOOK)
    body = body.replace("{{crumbs}}", breadcrumbs(meta))
    body = body.replace("{{logos}}", logo_marquee())
    loc_chips = "\n      ".join(
        '<a class="loc-chip" href="%slocations/%s.html">%s%s, %s</a>' % (p, slug, PIN, name, st)
        for slug, name, st in LOCATIONS)
    body = body.replace("{{loc_chips}}", loc_chips)
    body = body.replace("{{founder_photo}}", hosted(FOUNDER_LOCAL, FOUNDER_CDN_FILE))
    body = body.replace("{{phone_display}}", PHONE_DISPLAY)
    body = body.replace("{{phone_tel}}", PHONE_TEL)
    body = body.replace("{{email}}", EMAIL)
    body = body.replace("{{hero_stats}}", HERO_STATS)
    body = body.replace("{{journey}}", JOURNEY)
    body = body.replace("{{funding_path}}", FUNDING_PATH)
    body = body.replace("{{proof_home}}", PROOF_HOME)
    body = body.replace("{{proof_cfo}}", PROOF_CFO)
    body = body.replace("{{ghl_form}}", ghl_slot(
        "form", "Contact form goes here",
        "This panel is reserved for the OCG Financial intake form. Drop the embed in and it inherits "
        "the surrounding spacing and styling with no layout changes.", tall=True))
    if "{{ghl_form_short}}" in body:
        city = meta.get("crumbs", [("", None), ("Your", None)])[-1][0].split(",")[0]
        body = body.replace("{{ghl_form_short}}", short_form(city))
    body = body.replace("{{ghl_calendar}}", ghl_slot(
        "calendar", "Booking calendar goes here",
        "Reserved for the live scheduling calendar. Until it is embedded, the consultation buttons on "
        "this page point to the current booking link."))

    schema = [ORG_SCHEMA] if meta.get("org_schema", True) else []
    bc = breadcrumb_schema(meta)
    if bc:
        schema.append(bc)
    schema.extend(meta.get("schema", []))
    meta = dict(meta, schema=schema)

    html = head(meta) + nav(meta) + "\n<main>\n" + body + "\n</main>\n\n" + footer(meta)
    html = clean_links(html)
    out = os.path.join(ROOT, meta["out"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return meta["out"]


def sitemap(pages):
    urls = []
    for m in pages:
        loc = BASE + clean_path(m["out"])
        pri = m.get("priority", "0.7")
        urls.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq><priority>{pri}</priority></url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(xml)
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % BASE)


def main():
    global CSS_V, JS_V
    CSS_V = asset_v("assets/css/styles.css")
    JS_V = asset_v("assets/js/main.js")
    from manifest import PAGES
    built = [build_page(m) for m in PAGES]
    sitemap(PAGES)
    print("Built %d pages:" % len(built))
    for b in built:
        print(" -", b)


if __name__ == "__main__":
    main()
