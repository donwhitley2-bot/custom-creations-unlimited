#!/usr/bin/env python3
"""
Preview an editorial, light hero — the "award-winning" direction, no video.

    python3 scripts/build-hero-editorial.py   -> preview/hero-editorial.html

Clones index.html's head/promo/header so it reads in context, swaps only the
hero section, and writes to preview/. Does NOT touch index.html — nothing here
is live until approved and wired in separately.

Direction: the loud dark full-bleed video hero is what most local-service
sites already do. Awwwards-style "elegant" hero rooms almost always go the
other way — light ground, oversized quiet typography, one real photograph
treated as a framed object rather than a background, generous negative space.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "preview")

HERO = """
    <!-- ===================== HERO (editorial preview) ===================== -->
    <section class="hero hero--ed" id="heroLaser" aria-labelledby="hero-h">
      <div class="container hero--ed__inner">

        <div class="hero--ed__copy">
          <div class="hero--ed__eyebrow" data-reveal>
            <span class="rule"></span>
            <span>Atlanta, Georgia &nbsp;·&nbsp; 18 years in business</span>
          </div>

          <h1 id="hero-h" class="hero--ed__h1" data-reveal data-delay="1">
            Custom branding that makes your business <em>stand out.</em>
          </h1>

          <p class="hero--ed__sub" data-reveal data-delay="2">From embroidered apparel and
            promotional products to laser engraving and personalized gifts — we help
            businesses, schools, organizations and individuals bring their ideas to life.</p>

          <div class="hero--ed__cta" data-reveal data-delay="3">
            <a class="btn btn--gold btn--lg" href="../shop.html">Shop Custom Items
              <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <a class="btn btn--outline-ed btn--lg" href="../quote.html">Request a Quote</a>
          </div>

          <div class="hero--ed__proof" data-reveal data-delay="4">
            <span class="stars" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>
            </span>
            <span><b>4.9/5</b> from 1,280+ reviews &nbsp;·&nbsp; <b>15,000+</b> brands served</span>
          </div>
        </div>

        <div class="hero--ed__art" data-reveal data-delay="2">
          <figure class="hero--ed__frame">
            <img src="../assets/img/embroidery-1.webp"
                 alt="An embroidered navy polo and cap with a gold crest">
          </figure>
          <div class="hero--ed__art-back" aria-hidden="true"></div>
        </div>
      </div>

      <a class="hero--ed__scroll" href="#servicesGrid" aria-label="Scroll to see our services">
        <span>Scroll</span>
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 4v15m0 0l-6-6m6 6l6-6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
    </section>
"""

CSS = """
<style>
/* The header has no background until scrolled — it relies on a body class to
   recolor nav text for whatever sits behind it. has-dark-hero (pale text)
   already exists for the old dark hero; this is its mirror for a pinned-light
   one. Needed for real visitors, not just this preview: the header has a
   light/dark toggle, and in the site's dark theme --text flips to near-white,
   which would vanish against this hero's ivory ground without this override.
   For the real wire-in this block belongs in styles.css next to
   has-dark-hero, and index.html's <body> class swaps accordingly. */
body.has-light-hero .site-header:not(.is-scrolled) .brand__name,
body.has-light-hero .site-header:not(.is-scrolled) .nav-link { color: rgba(16,16,25,.88); }
body.has-light-hero .site-header:not(.is-scrolled) .nav-link:hover,
body.has-light-hero .site-header:not(.is-scrolled) .nav-item:hover .nav-link { color: var(--gold-700); }
body.has-light-hero .site-header:not(.is-scrolled) .icon-btn { color: rgba(16,16,25,.82); border-color: rgba(16,16,25,.18); }
body.has-light-hero .site-header:not(.is-scrolled) .icon-btn:hover { border-color: var(--gold-600); color: var(--gold-700); }
body.has-light-hero .site-header:not(.is-scrolled) .brand__mark rect { fill: rgba(16,16,25,.08); }

/* ============ editorial hero (preview) ============ */
/* Pinned light regardless of the site's dark-mode toggle — same principle as
   the old dark video hero, which was pinned dark regardless of theme. A photo
   presented as a framed object needs a fixed, deliberate ground; letting it
   flip to the dark palette would also silently swap --text to near-white,
   which is invisible against this section's ivory background. Every color
   below is a raw token (--ink-*, --ivory-*, --gold-*) rather than a semantic
   one (--text, --bg) for exactly that reason. */
.hero--ed{ position:relative; min-height:100svh; display:flex; align-items:center;
  background:var(--ivory-50); overflow:hidden; padding-top:var(--header-h); color-scheme:light; }

.hero--ed__inner{ position:relative; z-index:1; display:grid; gap:clamp(2rem,4.5vw,3.4rem);
  grid-template-columns:1fr; align-items:center; padding-block:clamp(1.6rem,4.5vh,3rem); }
@media (min-width:980px){
  .hero--ed__inner{ grid-template-columns:minmax(0,1.16fr) minmax(0,.84fr); }
}

.hero--ed__copy{ max-width:42rem }
.hero--ed__eyebrow{ display:flex; align-items:center; gap:.7rem; font-size:.8rem; letter-spacing:.08em;
  color:var(--ink-500); margin-bottom:1.1rem }
.hero--ed__eyebrow .rule{ width:2.4rem; height:2px; background:linear-gradient(90deg,var(--gold-500),var(--gold-700)) }

/* Flowing, not stacked: hard line-breaks tuned for one column width look
   broken at another, and with a headline this large, forcing five short
   lines pushed the buttons below the fold on an ordinary laptop screen.
   Letting it wrap naturally keeps the section to two or three lines at any
   width. */
.hero--ed__h1{ font-family:var(--font-display); font-weight:600; letter-spacing:-.01em;
  font-size:clamp(2.1rem,1.4rem + 2.4vw,3.4rem); line-height:1.13; color:var(--ink-800); margin-bottom:1.1rem }
.hero--ed__h1 em{ font-style:italic; color:var(--gold-600) }

.hero--ed__sub{ font-size:clamp(.98rem,.92rem + .25vw,1.08rem); line-height:1.6; color:var(--ink-500);
  max-width:36ch; margin-bottom:1.6rem }

.hero--ed__cta{ display:flex; gap:.8rem; flex-wrap:wrap; margin-bottom:1.7rem }
.btn--outline-ed{ display:inline-flex; align-items:center; gap:.4rem; padding:.85rem 1.5rem;
  border-radius:var(--pill,999px); border:1.5px solid var(--ink-800); color:var(--ink-800);
  font-weight:600; text-decoration:none; transition:background .2s,color .2s }
.btn--outline-ed:hover{ background:var(--ink-800); color:#fff }

.hero--ed__proof{ display:flex; align-items:center; gap:.6rem; font-size:.9rem; color:var(--ink-500);
  padding-top:1.15rem; border-top:1px solid rgba(20,20,28,.10) }
.hero--ed__proof .stars{ display:inline-flex; gap:1px }
.hero--ed__proof .stars svg{ width:15px; height:15px; color:var(--gold-500) }
.hero--ed__proof b{ color:var(--ink-800); font-weight:700 }

/* the single photograph, presented as a framed object rather than a backdrop */
.hero--ed__art{ position:relative; justify-self:center; width:100%; max-width:28rem }
.hero--ed__art-back{ position:absolute; inset:1.1rem -1.1rem -1.1rem 1.1rem; z-index:0;
  border:1.5px solid var(--gold-300); border-radius:var(--radius-lg); }
.hero--ed__frame{ position:relative; z-index:1; margin:0; border-radius:var(--radius-lg);
  overflow:hidden; box-shadow:var(--shadow-lg); background:var(--ivory-200); }
.hero--ed__frame img{ width:100%; aspect-ratio:4/3; object-fit:cover; display:block }


.hero--ed__scroll{ position:absolute; left:50%; bottom:1.6rem; transform:translateX(-50%);
  display:flex; flex-direction:column; align-items:center; gap:.35rem; z-index:1;
  color:var(--ink-500); text-decoration:none; font-size:.68rem; letter-spacing:.14em;
  text-transform:uppercase; opacity:.75 }
.hero--ed__scroll svg{ width:15px; height:15px; animation:edbob 2.2s ease-in-out infinite }
@keyframes edbob{ 0%,100%{ transform:translateY(0) } 50%{ transform:translateY(5px) } }

@media (max-width:979px){
  .hero--ed{ text-align:center }
  .hero--ed__copy{ max-width:none; margin-inline:auto }
  .hero--ed__eyebrow,.hero--ed__cta{ justify-content:center }
  .hero--ed__art{ max-width:16rem }
  .hero--ed::before{ display:none }
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]) .hero--ed{ background:var(--ivory-50) !important }
}
</style>
"""


def main():
    src = os.path.join(ROOT, "index.html")
    s = open(src, encoding="utf-8").read()

    a = s.find('<section class="hero')
    b = s.find("</section>", s.find("hero-vid__btn")) + len("</section>")
    if a < 0 or b < len("</section>"):
        sys.exit("could not locate the current hero section in index.html")

    head, tail = s[:a], s[b:]

    # has-dark-hero is a hardcoded class on <body>, not something JS toggles —
    # it exists only because the hero has always been dark, and it pales the
    # header nav text to be readable over that. This hero is light, so the
    # same class would wash the nav out against ivory. A real wire-in needs
    # this class removed from index.html's <body>, not just skipped here.
    head = head.replace('class="has-promo has-dark-hero"', 'class="has-promo has-light-hero"', 1)

    def rebase(t):
        t = re.sub(r'(src|href)="(?!https?:|//|#|mailto:|tel:|\.\./|data:)', r'\1="../', t)
        return re.sub(r'(\s)(assets/img/[^\s"]+)', r'\1../\2', t)

    page = rebase(head) + HERO + rebase(tail)
    page = page.replace("</head>", CSS + "</head>", 1)
    page = page.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    page = page.replace("<title>", "<title>PREVIEW · ", 1)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "hero-editorial.html")
    open(path, "w", encoding="utf-8").write(page)
    print(f"  preview/hero-editorial.html   {os.path.getsize(path)/1e3:.0f} KB")
    print("  (index.html untouched, nothing live)")


if __name__ == "__main__":
    main()
