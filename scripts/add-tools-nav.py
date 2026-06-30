#!/usr/bin/env python3
"""
Insert the password-gated "Tools" dropdown into every page's primary + mobile
nav, immediately before the Contact item. Runs as a post-process step (after the
page generators) so the menu stays reproducible. Idempotent: skips files that
already contain the Tools links.

The password gate itself lives in assets/js/main.js (click handler on
.js-tools-link) and in each tools/*.html file (inline guard).
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

TOOLS = [
    ("bulk-tee-generator", "Bulk Tee Generator", "Bulk t-shirt design generator"),
    ("pattern-press",      "Pattern Press",      "Pattern-fill text generator"),
    ("slogan-generator",   "Slogan Generator",   "Slogan &amp; graphic generator"),
]
ICON = ('<svg viewBox="0 0 24 24" fill="none"><path d="M14.7 6.3a4 4 0 01-5.4 5.4l-5 5a1.5 1.5 0 002 2l5-5a4 4 0 005.4-5.4l-2.3 2.3-2-2z" '
        'stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>')
CHEV = ('<svg class="chev" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
CHEV_M = ('<svg viewBox="0 0 24 24" fill="none" width="20"><path d="M6 9l6 6 6-6" '
          'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def desktop(p):
    items = "".join(
        f'<a class="mega-link js-tools-link" href="{p}tools/{s}.html" role="menuitem">'
        f'<span class="mega-link__icon">{ICON}</span>'
        f'<span><span class="mega-link__title">{t}</span><span class="mega-link__desc">{d}</span></span></a>'
        for s, t, d in TOOLS)
    return (f'<li class="nav-item nav-item--has-mega">'
            f'<a class="nav-link js-tools-link" href="{p}tools/{TOOLS[0][0]}.html" aria-haspopup="true">Tools {CHEV}</a>'
            f'<div class="mega mega--tools" role="menu"><div class="mega-grid">{items}</div>'
            f'<div class="mega-foot"><span>&#128274; Password-protected staff tools.</span></div></div></li>')

def mobile(p):
    links = "".join(f'<a class="js-tools-link" href="{p}tools/{s}.html">{t}</a>' for s, t, d in TOOLS)
    return (f'<li><button class="mobile-nav__link" data-sub="m-tools" aria-expanded="false">Tools {CHEV_M}</button>'
            f'<div class="mobile-nav__sub" id="m-tools">{links}</div></li>')

DESK_RE = re.compile(r'<li class="nav-item"><a class="nav-link" href="((?:\.\./)?)contact\.html"[^>]*>Contact</a></li>')
MOB_RE  = re.compile(r'<li><a class="mobile-nav__link" href="((?:\.\./)?)contact\.html">Contact</a></li>')

def process(path):
    s = open(path, encoding="utf-8").read()
    if "js-tools-link" in s:
        return 0
    n = 0
    m = DESK_RE.search(s)
    if m:
        s = s[:m.start()] + desktop(m.group(1)) + s[m.start():]; n += 1
    m = MOB_RE.search(s)
    if m:
        s = s[:m.start()] + mobile(m.group(1)) + s[m.start():]; n += 1
    if n:
        open(path, "w", encoding="utf-8").write(s)
    return n

def main():
    targets = [os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.endswith(".html")]
    for sub in ("services", "blog"):
        d = os.path.join(ROOT, sub)
        if os.path.isdir(d):
            targets += [os.path.join(d, f) for f in os.listdir(d) if f.endswith(".html")]
    total = 0
    for path in sorted(targets):
        inserted = process(path)
        if inserted:
            total += 1
            print(f"  {os.path.relpath(path, ROOT):34} Tools nav added")
    print(f"\nTools menu added to {total} page(s).")

if __name__ == "__main__":
    main()
