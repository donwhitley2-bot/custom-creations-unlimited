#!/usr/bin/env python3
"""
Preview the gallery with the real-work pieces added — nothing is published.

    python3 scripts/build-gallery-preview.py   -> preview/gallery-new.html

Reads the live gallery.html and injects the new items at the top of the grid.
It deliberately does NOT touch scripts/build-pages.py or gallery.html, so the
live page stays exactly as it is until this is approved.

Photos come from scripts/prep-work-photos.py, which normalises the sources into
a matched set first. Portrait pieces use span-4 + tall so object-fit:cover has a
portrait tile to fill and doesn't crop the top and bottom off an award.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "preview")

# (category, category label, caption, grid span, image)
# Portrait pieces get span-4 + tall so the tile is roughly portrait too — in a
# wide tile, object-fit:cover would crop the top and bottom off the award.
NEW_WORK = [
    ("awards", "Awards", "Fire academy alumni award", "span-4 tall",
     "img-work/work-award-arrowhead.webp"),
    ("laser", "Laser Engraving", "Subsurface crystal logo cube", "span-4",
     "img-work/work-crystal-cube.webp"),
    ("laser", "Laser Engraving", "Subsurface crystal chess knight", "span-4 tall",
     "img-work/work-crystal-knight.webp"),
]

CSS = """
<style>
/* preview-only: stand-ins for photos that aren't on disk yet */
.gallery-item.is-new .phx{
  position:absolute; inset:0; display:flex; flex-direction:column; gap:.5rem;
  align-items:center; justify-content:center; text-align:center; padding:1.2rem;
  background:
    radial-gradient(120% 90% at 50% 18%, #2b2b33 0%, #14141b 55%, #0b0b10 100%);
  color:#9d9890; font-size:.78rem; line-height:1.45;
}
.gallery-item.is-new .phx b{ color:#e3c988; font-size:.95rem; font-weight:600;
  font-family:var(--font-display) }
.gallery-item.is-new .phx i{ font-style:normal; font-size:.7rem; letter-spacing:.14em;
  text-transform:uppercase; color:#6f6a63 }
.gallery-item.is-new{ position:relative }
.gallery-item.is-new::after{
  content:"NEW"; position:absolute; top:.6rem; left:.6rem; z-index:3;
  background:var(--grad-gold); color:#1a1408; font-size:.6rem; font-weight:800;
  letter-spacing:.12em; padding:.2rem .45rem; border-radius:.3rem;
}
.pv-note{ background:#14141b; color:#e3dccf; padding:.9rem 1rem; text-align:center;
  font-size:.85rem; position:sticky; top:0; z-index:99 }
.pv-note b{ color:#e3c988 }
</style>
"""

BANNER = ('<div class="pv-note"><b>PREVIEW — not published.</b> '
          'The three gold-tagged tiles are your real work — everything else is '
          'the existing AI imagery. Use the sun/moon icon to compare light mode.</div>')


def tile(cat, label, title, span, img):
    return (f'<figure class="gallery-item is-new {span}" data-cat="{cat}" '
            f'data-cat-label="{label}" data-title="{title}" data-reveal>'
            f'<img class="ph-img" src="{img}" alt="{title}" loading="lazy" decoding="async" />'
            f'<figcaption class="gallery-item__overlay">'
            f'<span class="gallery-item__cat">{label}</span>'
            f'<span class="gallery-item__title">{title}</span></figcaption></figure>')


def main():
    src = os.path.join(ROOT, "gallery.html")
    s = open(src, encoding="utf-8").read()

    marker = '<div class="gallery-grid">'
    i = s.find(marker)
    if i < 0:
        sys.exit("gallery-grid not found in gallery.html")
    i += len(marker)

    s = s[:i] + "".join(tile(*n) for n in NEW_WORK) + s[i:]

    # one directory down
    s = re.sub(r'(src|href)="(?!https?:|//|#|mailto:|tel:|\.\./|data:|img-work/)', r'\1="../', s)
    s = re.sub(r'(\s)(assets/img/[^\s"]+)', r'\1../\2', s)

    s = s.replace("</head>", CSS + "</head>", 1)
    s = s.replace("<title>", "<title>PREVIEW · ", 1)
    s = s.replace('<meta name="robots"', '<meta name="robots-x"')
    s = s.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    s = re.sub(r"(<body[^>]*>)", r"\1" + BANNER, s, count=1)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "gallery-new.html")
    open(path, "w", encoding="utf-8").write(s)
    print(f"  preview/gallery-new.html   {os.path.getsize(path)/1e3:.0f} KB")
    print("  (live gallery.html and build-pages.py untouched)")


if __name__ == "__main__":
    main()
