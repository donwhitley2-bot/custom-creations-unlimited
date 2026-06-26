#!/usr/bin/env python3
"""
Generate sitemap.xml and robots.txt by scanning the actual .html files.
Run after the other generators:  python3 scripts/build-sitemap.py
"""
import os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DOMAIN = "https://www.customcreationsunlimited.com"
TODAY = datetime.date.today().isoformat()

def priority(rel):
    if rel == "index.html": return "1.0", "weekly"
    if rel in ("quote.html", "contact.html"): return "0.9", "monthly"
    if rel.startswith("services/"): return "0.8", "monthly"
    if rel in ("gallery.html", "industries.html", "about.html"): return "0.8", "monthly"
    if rel == "blog/index.html": return "0.7", "weekly"
    if rel.startswith("blog/"): return "0.6", "monthly"
    return "0.7", "monthly"  # faq + fallback

def loc(rel):
    if rel == "index.html": return DOMAIN + "/"
    if rel.endswith("/index.html"): return DOMAIN + "/" + rel[:-len("index.html")]
    return DOMAIN + "/" + rel

def collect():
    out = []
    for d in (".", "services", "blog"):
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base): continue
        for f in sorted(os.listdir(base)):
            if f.endswith(".html"):
                out.append(os.path.normpath(os.path.join(d, f)).replace(os.sep, "/"))
    # home first, then the rest by descending priority then name
    return sorted(out, key=lambda r: (-float(priority(r)[0]), r))

def main():
    pages = collect()
    urls = "\n".join(
        f"  <url>\n    <loc>{loc(r)}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>{priority(r)[1]}</changefreq>\n    <priority>{priority(r)[0]}</priority>\n  </url>"
        for r in pages)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{urls}\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    robots = ("User-agent: *\n"
              "Allow: /\n\n"
              "# Be polite to AI/marketing scrapers if desired by uncommenting:\n"
              "# User-agent: GPTBot\n# Disallow: /\n\n"
              f"Sitemap: {DOMAIN}/sitemap.xml\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print(f"wrote sitemap.xml ({len(pages)} URLs) and robots.txt")

if __name__ == "__main__":
    main()
