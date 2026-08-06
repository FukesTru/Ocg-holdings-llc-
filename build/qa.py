#!/usr/bin/env python3
"""Site QA: links, SEO metadata, logo presence/sizing, asset cache-busting."""
import hashlib
import os
import re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = [os.path.relpath(os.path.join(dp, f), root)
         for dp, ds, fs in os.walk(root)
         if not any(x in dp for x in ('.git', 'node_modules', os.sep + 'build'))
         for f in fs if f.endswith('.html')]

LOGO_CLASS = 'class="brand-logo"'


def resolve(url):
    path = url.split('#')[0].split('?')[0].lstrip('/')
    if path == '':
        return 'index.html'
    for c in (path, path + '.html', os.path.join(path, 'index.html')):
        if os.path.exists(os.path.join(root, c)):
            return c
    return None


errors, titles, css_v, js_v = [], {}, set(), set()
for p in sorted(pages):
    html = open(os.path.join(root, p), encoding='utf-8').read()
    if '{{' in html:
        errors.append(p + ": leftover template token")
    for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
        u = m.group(1)
        if u.startswith(('http', 'data:', 'mailto:', 'tel:', '#')):
            continue
        if not u.startswith('/'):
            errors.append(p + ": relative link " + u)
            continue
        if resolve(u) is None:
            errors.append(p + ": broken link " + u)
        if u.split('?')[0].endswith('.html'):
            errors.append(p + ": .html link " + u)
    for m in re.finditer(r'href="#([^"]+)"', html):
        if 'id="' + m.group(1) + '"' not in html:
            errors.append(p + ": missing anchor #" + m.group(1))

    t = re.search(r'<title>(.*?)</title>', html, re.S)
    if not t:
        errors.append(p + ": no title")
        continue
    titles.setdefault(t.group(1), []).append(p)

    d = re.search(r'<meta name="description" content="(.*?)"', html)
    if not d or not (50 <= len(d.group(1)) <= 175):
        errors.append(p + ": meta description length")
    if len(re.findall(r'<h1[^>]*>', html)) != 1:
        errors.append(p + ": h1 count")

    # Logo: present twice (header + footer) with intrinsic dimensions
    n_logos = html.count(LOGO_CLASS)
    if n_logos != 2:
        errors.append(p + ": expected 2 logos, found " + str(n_logos))
    if LOGO_CLASS + ' width="268" height="78"' not in html:
        errors.append(p + ": logo missing intrinsic width/height")

    v = re.search(r'styles\.css\?v=([a-f0-9]+)', html)
    j = re.search(r'main\.js\?v=([a-f0-9]+)', html)
    if not v:
        errors.append(p + ": css not cache-busted")
    else:
        css_v.add(v.group(1))
    if not j:
        errors.append(p + ": js not cache-busted")
    else:
        js_v.add(j.group(1))

    c = re.search(r'rel="canonical" href="([^"]+)"', html)
    if c and c.group(1).endswith('.html'):
        errors.append(p + ": canonical ends .html")

for t, ps in titles.items():
    if len(ps) > 1:
        errors.append("duplicate title " + t + ": " + str(ps))

real_css = hashlib.md5(open(os.path.join(root, 'assets/css/styles.css'), 'rb').read()).hexdigest()[:8]
real_js = hashlib.md5(open(os.path.join(root, 'assets/js/main.js'), 'rb').read()).hexdigest()[:8]
if css_v != {real_css}:
    errors.append("css hash mismatch: html=%s actual=%s" % (css_v, real_css))
if js_v != {real_js}:
    errors.append("js hash mismatch: html=%s actual=%s" % (js_v, real_js))

print("%d pages | css v=%s | js v=%s" % (len(pages), real_css, real_js))
print("ISSUES:" if errors else "All checks passed.")
for e in errors[:25]:
    print(" -", e)
