#!/usr/bin/env python3
"""
Custom Creations Unlimited top-level page generator (root depth): gallery, industries, about,
contact, quote. Shares one header/footer so navigation stays consistent.
Run:  python3 scripts/build-pages.py
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

# ---- shared bits ----------------------------------------------------------
SVC = [
    ("embroidery", "Embroidery", 'M3 12h4l2-7 4 14 2-7h6'),
    ("custom-apparel", "Custom Apparel", 'M6 4l3 2h6l3-2 3 4-3 2v10H6V10L3 8z'),
    ("promotional-products", "Promotional Products", 'M4 8h16v12H4zM4 8l2-4h12l2 4M9 12h6'),
    ("awards", "Awards & Recognition", 'M8 4h8v4a4 4 0 01-8 0zM6 6H4v2a3 3 0 003 3M18 6h2v2a3 3 0 01-3 3M9 20h6l-1-4h-4z'),
    ("laser-engraving", "Laser Engraving", 'M3 17l8-8 4 4M14 6l4 4 3-3-4-4zM5 21l3-1 1-3'),
    ("personalized-gifts", "Personalized Gifts", 'M4 9h16v11H4zM3 5h18v4H3zM12 5v15M9 5s-2-3 1-3 2 3 2 3M15 5s2-3-1-3-2 3-2 3'),
]
ARROW = '<svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
STAR = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>'

def svc_icon(p):
    return f'<svg viewBox="0 0 24 24" fill="none"><path d="{p}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

NAV = [("index.html", "Home", "home"), ("about.html", "About", "about"),
       ("index.html#services", "Services", "services"), ("shop.html", "Shop", "shop"),
       ("gallery.html", "Gallery", "gallery"), ("industries.html", "Industries", "industries"),
       ("blog/index.html", "Blog", "blog"),
       ("faq.html", "FAQ", "faq"), ("contact.html", "Contact", "contact")]

def header(active):
    mega = "\n".join(
        f'''<a class="mega-link" href="services/{s}.html" role="menuitem">
              <span class="mega-link__icon">{svc_icon(p)}</span>
              <span><span class="mega-link__title">{n}</span></span>
            </a>''' for s, n, p in SVC)
    items = []
    for href, label, key in NAV:
        if key == "services":
            cur = ' aria-current="page"' if active == "services" else ""
            items.append(f'''<li class="nav-item nav-item--has-mega">
            <a class="nav-link" href="{href}" aria-haspopup="true"{cur}>Services
              <svg class="chev" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <div class="mega" role="menu"><div class="mega-grid">{mega}</div>
              <div class="mega-foot"><span>Not sure where to start? Our team will guide you.</span>
                <a class="link-arrow" href="quote.html">Request a quote {ARROW}</a></div>
            </div></li>''')
        else:
            cur = ' aria-current="page"' if active == key else ""
            items.append(f'<li class="nav-item"><a class="nav-link" href="{href}"{cur}>{label}</a></li>')
    nav = "\n".join(items)
    return f'''<header class="site-header" id="header">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Custom Creations Unlimited home">
        <svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true">
          <rect width="40" height="40" rx="9" fill="currentColor" style="color:var(--ink-900)"/>
          <text x="20" y="26" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="13" font-weight="700" fill="var(--gold-400)" style="letter-spacing:.5px">CCU</text>
        </svg>
        <span class="brand__name">Custom Creations</span>
      </a>
      <nav class="primary-nav" aria-label="Primary"><ul class="nav-list">{nav}</ul></nav>
      <div class="header-actions">
        <button class="icon-btn theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
          <svg class="sun" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          <svg class="moon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
        </button>
        <a class="btn btn--gold" href="quote.html">Request a Quote</a>
        <button class="icon-btn nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        </button>
      </div>
    </div>
  </header>
  <div class="mobile-nav" id="mobileNav" aria-hidden="true">
    <ul class="mobile-nav__list">
      <li><a class="mobile-nav__link" href="index.html">Home</a></li>
      <li><a class="mobile-nav__link" href="about.html">About</a></li>
      <li><button class="mobile-nav__link" data-sub="m-services" aria-expanded="false">Services
        <svg viewBox="0 0 24 24" fill="none" width="20"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <div class="mobile-nav__sub" id="m-services">
          {"".join(f'<a href="services/{s}.html">{n}</a>' for s,n,_ in SVC)}
        </div></li>
      <li><a class="mobile-nav__link" href="shop.html">Shop</a></li>
      <li><a class="mobile-nav__link" href="gallery.html">Gallery</a></li>
      <li><a class="mobile-nav__link" href="industries.html">Industries</a></li>
      <li><a class="mobile-nav__link" href="blog/index.html">Blog</a></li>
      <li><a class="mobile-nav__link" href="faq.html">FAQ</a></li>
      <li><a class="mobile-nav__link" href="contact.html">Contact</a></li>
    </ul>
    <div class="mobile-nav__cta">
      <a class="btn btn--gold btn--lg btn--block" href="quote.html">Request a Quote</a>
      <a class="btn btn--ghost btn--lg btn--block" href="tel:+14049678028">Call (404) 967-8028</a>
    </div>
  </div>'''

FOOTER = f'''<footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <a class="brand" href="index.html" aria-label="Custom Creations Unlimited home">
            <svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#16161f"/><text x="20" y="26" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="13" font-weight="700" fill="var(--gold-400)" style="letter-spacing:.5px">CCU</text></svg>
            <span class="brand__name">Custom Creations</span>
          </a>
          <p>A premium custom branding house — embroidery, apparel, promotional products, awards, laser engraving and personalized gifts, all under one roof.</p>
          <div class="footer-social">
            <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 9h3V6h-3c-2 0-3 1.3-3 3.2V11H8v3h3v7h3v-7h2.5l.5-3H14V9.5c0-.3.2-.5.6-.5z"/></svg></a>
            <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><circle cx="17" cy="7" r="1.2" fill="currentColor"/></svg></a>
            <a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.5 8A1.5 1.5 0 106.5 5 1.5 1.5 0 006.5 8zM5 10h3v9H5zM10 10h3v1.3c.5-.8 1.5-1.5 3-1.5 2.2 0 3 1.4 3 3.8V19h-3v-4.6c0-1.1-.4-1.8-1.4-1.8s-1.6.7-1.6 1.8V19h-3z"/></svg></a>
          </div>
        </div>
        <div class="footer-col"><h4>Services</h4>
          {"".join(f'<a href="services/{s}.html">{n}</a>' for s,n,_ in SVC)}
        </div>
        <div class="footer-col"><h4>Company</h4>
          <a href="about.html">About Us</a><a href="shop.html">Shop</a><a href="gallery.html">Gallery</a><a href="industries.html">Industries</a>
          <a href="index.html#reviews">Reviews</a><a href="index.html#faq">FAQ</a><a href="contact.html">Contact</a>
        </div>
        <div class="footer-col"><h4>Get in touch</h4>
          <a href="tel:+14049678028">(404) 967-8028</a>
          <a href="mailto:info@ccucustom.com">info@ccucustom.com</a>
          <a href="contact.html">1180 Industrial Park Blvd<br>Atlanta, GA 30318</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span id="year"></span> Custom Creations Unlimited All rights reserved. · Atlanta, GA</span>
        <nav aria-label="Legal"><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Accessibility</a></nav>
      </div>
    </div>
  </footer>
  <div class="floating">
    <a class="fab fab--call" href="tel:+14049678028" aria-label="Call us"><svg viewBox="0 0 24 24" fill="none"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.7A2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 2 .7 2.9a2 2 0 01-.4 2.1L8.1 9.9a16 16 0 006 6l1.2-1.3a2 2 0 012.1-.4c.9.3 1.9.6 2.9.7a2 2 0 011.7 2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg></a>
    <a class="fab fab--quote" href="quote.html" aria-label="Request a quote"><svg viewBox="0 0 24 24" fill="none"><path d="M4 5h16v11H8l-4 4z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8 9h8M8 12h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></a>
  </div>
  <button class="back-to-top" id="backToTop" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none"><path d="M12 19V5M5 12l7-7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
  <script src="assets/js/main.js?v=2" defer></script>'''

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin /><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230a0a0f'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-family='Georgia,serif' font-size='11' font-weight='700' fill='%23c8a24a'%3ECCU%3C/text%3E%3C/svg%3E"

def page(slug, title, desc, keywords, active, body, schema=""):
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#0a0a0f" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="https://www.ccucustom.com/{slug}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Custom Creations Unlimited" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://www.ccucustom.com/{slug}" />
  <meta property="og:image" content="https://www.ccucustom.com/assets/img/og-cover.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  {FONT}
  <link rel="stylesheet" href="assets/css/styles.css?v=2" />
  <link rel="icon" href="{FAVICON}" />
  {schema}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  {header(active)}
  <main id="main">
{body}
  </main>
  {FOOTER}
</body>
</html>'''

def breadcrumb(label, center=False):
    chev = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f'''<nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a>{chev}<span aria-current="page">{label}</span></nav>'''

CTA = '''<section class="section"><div class="container"><div class="cta-banner" data-reveal><div class="cta-banner__inner">
      <span class="eyebrow eyebrow--center" style="color:var(--gold-300)">Request a quote</span>
      <h2>Ready to make your mark?</h2>
      <p>Tell us about your project and we'll send a free design proof and exact quote — usually within one business day.</p>
      <div class="hero__cta"><a class="btn btn--gold btn--lg" href="quote.html">Start my quote ''' + ARROW + '''</a>
      <a class="btn btn--light btn--lg" href="tel:+14049678028">Call (404) 967-8028</a></div>
    </div></div></div></section>'''

# ==========================================================================
# GALLERY
# ==========================================================================
GAL_CATS = [("all","All work"),("embroidery","Embroidery"),("apparel","Apparel"),("promotional","Promotional"),
            ("awards","Awards"),("laser","Laser Engraving"),("drinkware","Drinkware"),("branding","Business Branding"),("gifts","Custom Gifts")]
GAL_ITEMS = [
    ("embroidery","Embroidery","Corporate uniform program","span-6 tall"),
    ("apparel","Apparel","School spirit wear run","span-6"),
    ("awards","Awards","Annual sales recognition","span-6"),
    ("laser","Laser Engraving","Engraved cutting boards","span-4"),
    ("drinkware","Drinkware","Custom tumbler set","span-4"),
    ("promotional","Promotional","New-hire welcome kits","span-4"),
    ("apparel","Apparel","Conference merch line","span-8"),
    ("embroidery","Embroidery","Embroidered cap drop","span-4"),
    ("branding","Business Branding","Full brand rollout","span-6"),
    ("gifts","Custom Gifts","Wedding party gifts","span-6"),
    ("awards","Awards","Crystal gala awards","span-4"),
    ("laser","Laser Engraving","Memorial slate sign","span-4"),
    ("drinkware","Drinkware","Branded mug program","span-4"),
    ("drinkware","Drinkware","Personalized whiskey glasses","span-4"),
    ("promotional","Promotional","Trade-show giveaways","span-6 tall"),
    ("branding","Business Branding","Signage & banners","span-6"),
    ("gifts","Custom Gifts","Holiday client gifts","span-6"),
]
def gallery_page():
    filters = "".join(f'<button class="filter-btn{" is-active" if k=="all" else ""}" data-filter="{k}">{n}</button>' for k,n in GAL_CATS)
    items = "".join(
        f'''<figure class="gallery-item {sp}" data-cat="{c}" data-cat-label="{cl}" data-title="{t}" data-reveal>
          <div class="ph" data-label="{t}"></div>
          <figcaption class="gallery-item__overlay"><span class="gallery-item__cat">{cl}</span><span class="gallery-item__title">{t}</span></figcaption>
        </figure>''' for c,cl,t,sp in GAL_ITEMS)
    lightbox = f'''<div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-label="Image preview">
    <button class="lb-btn lightbox__close" data-lb-close aria-label="Close"><svg viewBox="0 0 24 24" fill="none"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    <button class="lb-btn lightbox__nav lightbox__nav--prev" aria-label="Previous"><svg viewBox="0 0 24 24" fill="none"><path d="M15 6l-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <button class="lb-btn lightbox__nav lightbox__nav--next" aria-label="Next"><svg viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <div class="lightbox__content"><div class="lightbox__frame"></div>
      <div class="lightbox__cap"><span class="gallery-item__cat js-lb-cat"></span><div class="gallery-item__title js-lb-title"></div></div>
    </div></div>'''
    body = f'''    <section class="page-hero page-hero--center"><div class="page-hero__bg" aria-hidden="true"></div>
      <div class="container"><div class="page-hero__inner">
        {breadcrumb("Gallery", True)}
        <span class="eyebrow eyebrow--center" data-reveal>Portfolio</span>
        <h1 data-reveal data-delay="1">Our work, <span class="text-gradient">up close.</span></h1>
        <p data-reveal data-delay="2">A selection of recent projects across embroidery, apparel, awards, engraving and more. Click any piece to view it larger.</p>
      </div></div></section>

    <section class="section section--tight"><div class="container">
      <div class="gallery-filters" data-reveal role="tablist" aria-label="Filter portfolio">{filters}</div>
      <div class="gallery-grid">{items}</div>
    </div></section>
{CTA}
{lightbox}'''
    return page("gallery.html","Gallery | Custom Branding Portfolio | Custom Creations Unlimited",
        "Browse the Custom Creations Unlimited portfolio — custom embroidery, apparel, promotional products, awards, laser engraving and personalized gifts for businesses, schools and teams.",
        "embroidery portfolio, custom apparel gallery, awards, laser engraving examples, branding portfolio, Atlanta",
        "gallery", body)

# ==========================================================================
# INDUSTRIES
# ==========================================================================
INDUSTRIES = [
    ("schools","Schools & Universities","Spirit wear, staff uniforms, club apparel, fundraising merch and award nights — all in your colors.",["Spirit Wear","Uniforms","Trophies","Fan Gear"], 'M3 21h18M5 21V8l7-4 7 4v13M9 21v-6h6v6'),
    ("churches","Churches & Ministries","Volunteer and staff apparel, event tees, outreach giveaways and recognition gifts for your congregation.",["Team Apparel","Event Tees","Banners","Gifts"], 'M12 2v8M8 6h8M5 22V10h14v12M9 22v-5h6v5'),
    ("construction","Construction & Trades","Durable, OSHA-friendly hi-vis shirts, jackets, hard-hat decals and embroidered workwear that holds up on the job.",["Hi-Vis","Workwear","Embroidery","Safety"], 'M3 21h18M6 21V8l6-4 6 4v13M10 12h4M10 16h4'),
    ("restaurants","Restaurants & Cafés","Branded aprons, staff tees, hats and to-go merch that turn your team and customers into walking billboards.",["Aprons","Staff Tees","Hats","Drinkware"], 'M5 11h14l-1 9H6zM9 11V7a3 3 0 016 0v4'),
    ("healthcare","Healthcare & Wellness","Embroidered scrubs, polos, lab coats and patient-drive giveaways, plus recognition awards for your staff.",["Scrubs","Polos","Recognition","Promo"], 'M12 3v18M3 12h18M7 7l10 10M17 7L7 17'),
    ("government","Government & Civic","Department apparel, safety gear, event signage and recognition for agencies, cities and public programs.",["Apparel","Signage","Safety","Awards"], 'M3 21h18M5 21V7h14v14M9 11h2M13 11h2M9 15h2M13 15h2'),
    ("sports","Sports Teams & Leagues","Custom uniforms, fan gear, spirit packs and engraved trophies for leagues, clubs and tournaments.",["Uniforms","Fan Gear","Trophies","Banners"], 'M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 16.8 5.7 21.4 8 14 2 9.4h7.6z'),
    ("corporate","Corporate & Enterprise","Company-wide uniform programs, branded swag, executive gifts and recognition awards under one managed account.",["Uniforms","Swag","Gifts","Awards"], 'M4 20V8l8-5 8 5v12M9 20v-6h6v6M4 8h16'),
    ("smallbiz","Small Business","Everything you need to look established — logo apparel, signage, business cards' big sister: branded everything.",["Logo Apparel","Signage","Promo","Banners"], 'M4 9h16v11H4zM4 9l2-5h12l2 5M9 13h6'),
    ("realestate","Real Estate","Yard and open-house signs, branded closing gifts, agent apparel and client keepsakes that referrals remember.",["Signs","Closing Gifts","Apparel","Engraving"], 'M3 9l9-6 9 6v11H3zM9 20v-6h6v6'),
    ("nonprofits","Nonprofits & Causes","Affordable event tees, donor recognition, fundraising merch and volunteer gear that stretches your budget.",["Event Tees","Donor Gifts","Merch","Banners"], 'M12 21s-7-4.5-9-9a4 4 0 017-3 4 4 0 017 3c-2 4.5-9 9-9 9z'),
    ("manufacturing","Manufacturing & Industrial","Embroidered and printed workwear, PPE-compatible apparel, safety-award programs and facility signage.",["Workwear","PPE","Safety Awards","Signage"], 'M4 21V5l8-3 8 3v16M8 9h2M14 9h2M8 13h2M14 13h2'),
    ("retail","Retail & Brands","Private-label apparel, branded packaging extras, retail merch and in-store signage that elevates your shelf.",["Apparel","Merch","Packaging","Signage"], 'M6 2l-2 5v13h16V7l-2-5zM4 7h16M9 11h6'),
    ("hospitality","Hospitality & Events","Uniforms, name badges, branded amenities and event favors for hotels, venues, weddings and conferences.",["Uniforms","Badges","Favors","Drinkware"], 'M3 21h18M5 21v-9h14v9M5 12l7-7 7 7M10 21v-4h4v4'),
]
def industries_page():
    def icon(p): return f'<svg viewBox="0 0 24 24" fill="none"><path d="{p}" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></svg>'
    cards = "".join(
        f'''<article class="card ind-card" data-reveal data-delay="{i%3}">
          <span class="ind-card__icon">{icon(p)}</span>
          <h3>{name}</h3><p>{desc}</p>
          <div class="ind-card__tags">{"".join(f"<span>{t}</span>" for t in tags)}</div>
          <a class="link-arrow" href="quote.html">Get a quote {ARROW}</a>
        </article>''' for i,(k,name,desc,tags,p) in enumerate(INDUSTRIES))
    body = f'''    <section class="page-hero page-hero--center"><div class="page-hero__bg" aria-hidden="true"></div>
      <div class="container"><div class="page-hero__inner">
        {breadcrumb("Industries", True)}
        <span class="eyebrow eyebrow--center" data-reveal>Industries we serve</span>
        <h1 data-reveal data-delay="1">Branding for <span class="text-gradient">every kind</span> of organization.</h1>
        <p data-reveal data-delay="2">From a two-person startup to a city government, we tailor products, materials and pricing to how your organization actually works.</p>
      </div></div></section>

    <section class="section section--tight"><div class="container">
      <div class="grid grid--3">{cards}</div>
    </div></section>

    <section class="section--tight section"><div class="container"><div class="stats" data-reveal><div class="stats__grid">
      <div class="stat"><div class="stat__num" data-count="15000" data-suffix="+">0</div><div class="stat__label">Brands served</div></div>
      <div class="stat"><div class="stat__num" data-count="14" data-suffix="">0</div><div class="stat__label">Industries</div></div>
      <div class="stat"><div class="stat__num" data-count="98" data-suffix="%">0</div><div class="stat__label">On-time delivery</div></div>
      <div class="stat"><div class="stat__num" data-count="4.9" data-suffix="/5">0</div><div class="stat__label">Average rating</div></div>
    </div></div></div></section>
{CTA}'''
    return page("industries.html","Industries We Serve | Custom Creations Unlimited Custom Branding",
        "Custom Creations Unlimited serves schools, churches, construction, restaurants, healthcare, government, sports teams, corporate, nonprofits and more with custom branding, apparel and awards.",
        "branding for schools, church apparel, construction workwear, restaurant apparel, healthcare uniforms, corporate branding, nonprofit merch, Atlanta",
        "industries", body)

# ==========================================================================
# ABOUT
# ==========================================================================
VALUES = [
    ("Craftsmanship first","We treat every order — one gift or ten thousand shirts — like it carries our name, because it does.","M12 2l8 4v6c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10V6z M9 12l2 2 4-4"),
    ("Honest & clear","Transparent pricing, real timelines and straight answers. No surprises on your invoice or your ship date.","M4 7h16M4 12h16M4 17h10"),
    ("Genuinely helpful","Real people who pick up the phone, sweat your deadline and make the easy choice the right one.","M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"),
    ("Detail obsessed","Color matching, registration, stitch counts, engraving depth — the small things are the whole thing.","M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 16.8 5.7 21.4 8 14 2 9.4h7.6z"),
    ("Always on time","98% of orders ship on or ahead of schedule. When we commit to a date, we plan the whole job around it.","M12 7v5l3 2 M21 12a9 9 0 11-18 0 9 9 0 0118 0z"),
    ("Built for partnership","Most clients come back. We invest in long relationships, stored brand standards and easy reorders.","M3 12h18M3 6h18M3 18h18"),
]
EQUIP = [
    ("Multi-head embroidery","Commercial machines for fast, consistent stitching across large runs."),
    ("DTF & wide-format printing","Full-color, photo-grade transfers with a soft hand on any garment."),
    ("Automatic screen press","High-volume, durable prints at the best per-piece pricing."),
    ("CO₂ & fiber lasers","Precision engraving on wood, glass, metal, leather, slate and acrylic."),
    ("Sublimation","Edge-to-edge, all-over color on performance and promo products."),
    ("In-house design studio","Digitizing, vectorizing and original artwork — proofs before production."),
]
TEAM = [
    ("Don Whitley","Owner & CEO","Founded Custom Creations Unlimited on one rule — treat every logo like it's our own, and never ship anything less than perfect."),
    ("Riley Chen","Head of Production","Keeps every machine humming and every deadline met — the reason 98% of orders ship on time."),
    ("Sam Delgado","Design Director","Turns rough ideas and low-res logos into production-ready art that looks premium on anything."),
    ("Taylor Brooks","Client Success","Your single point of contact for quotes, proofs, reorders and the occasional last-minute rescue."),
]
def about_page():
    values = "".join(
        f'''<div class="card value-card feature" data-reveal data-delay="{i%3}"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none"><path d="{p}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>{t}</h3><p>{d}</p></div>'''
        for i,(t,d,p) in enumerate(VALUES))
    equip = "".join(
        f'''<div class="card" data-reveal data-delay="{i%3}" style="padding:1.5rem"><h3 style="font-size:1.12rem;margin-bottom:.4rem">{t}</h3><p class="muted" style="font-size:.92rem">{d}</p></div>'''
        for i,(t,d) in enumerate(EQUIP))
    def initials(name):
        parts = [p for p in name.split() if p]
        return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()
    team = "".join(
        f'''<article class="team-card" data-reveal data-delay="{i%4}"><div class="team-card__photo team-card__photo--mono" aria-hidden="true"><span class="team-mono">{initials(n)}</span></div><h3>{n}</h3><div class="role">{r}</div><p>{b}</p></article>'''
        for i,(n,r,b) in enumerate(TEAM))
    body = f'''    <section class="page-hero"><div class="page-hero__bg" aria-hidden="true"></div>
      <div class="container"><div class="page-hero__inner">
        {breadcrumb("About")}
        <span class="eyebrow" data-reveal>About Custom Creations Unlimited</span>
        <h1 data-reveal data-delay="1">Branding is personal. <span class="text-gradient">We treat it that way.</span></h1>
        <p data-reveal data-delay="2">For 18 years we've helped businesses, schools and organizations look the part — with craftsmanship, honesty and service that keeps them coming back.</p>
      </div></div></section>

    <section class="section"><div class="container split">
      <div data-reveal>
        <span class="eyebrow">Our story</span>
        <h2 style="margin:1rem 0 1.2rem">From one machine to a full branding house.</h2>
        <p>Custom Creations Unlimited began with a single embroidery machine and a simple belief: the things a company puts its name on should be made with real care. Word spread, the equipment multiplied, and the services grew — but the standard never changed.</p>
        <p>Today we run embroidery, printing, laser engraving and awards under one roof, so our clients get one trusted partner instead of five vendors. The garage is gone; the obsession with getting it right is not.</p>
        <ul class="check-list">
          <li>{CHECK}<span><strong>18 years</strong> serving Atlanta and beyond</span></li>
          <li>{CHECK}<span><strong>Everything in-house</strong> — total quality control</span></li>
          <li>{CHECK}<span><strong>15,000+ brands</strong> trusted us with their name</span></li>
        </ul>
      </div>
      <div class="media-frame split__media" data-reveal data-delay="1" aria-hidden="true"><div class="ph" data-label="Our studio"></div></div>
    </div></section>

    <section class="section section--tight" style="background:var(--bg-soft)"><div class="container split">
      <div class="card" data-reveal style="padding:2rem"><span class="eyebrow">Mission</span><h3 style="font-size:1.5rem;margin:.8rem 0 .6rem">Make great branding effortless.</h3><p class="muted">To give every organization — whatever its size or budget — premium, perfectly-executed branded products through one partner who makes the whole process easy.</p></div>
      <div class="card" data-reveal data-delay="1" style="padding:2rem"><span class="eyebrow">Vision</span><h3 style="font-size:1.5rem;margin:.8rem 0 .6rem">The name behind your name.</h3><p class="muted">To be the most trusted branding house in the Southeast — the team organizations think of the moment they need to put their logo on anything.</p></div>
    </div></section>

    <section class="section"><div class="container">
      <div class="section-head section-head--center" data-reveal><span class="eyebrow eyebrow--center">Core values</span><h2>What we stand behind.</h2></div>
      <div class="grid grid--3">{values}</div>
    </div></section>

    <section class="section section--tight" style="background:var(--bg-soft)"><div class="container">
      <div class="section-head section-head--center" data-reveal><span class="eyebrow eyebrow--center">How it works</span><h2>From idea to delivered in four steps.</h2></div>
      <div class="process-grid" style="margin-top:3rem">
        <div class="process-step" data-reveal><span class="process-step__num">01</span><h3>Share your idea</h3><p>Send your logo and what you need — or let our designers create it from scratch.</p></div>
        <div class="process-step" data-reveal data-delay="1"><span class="process-step__num">02</span><h3>Approve your proof</h3><p>We send a free digital proof and exact quote. Revise until it's perfect.</p></div>
        <div class="process-step" data-reveal data-delay="2"><span class="process-step__num">03</span><h3>We produce it</h3><p>Crafted in-house on premium products with rigorous quality control.</p></div>
        <div class="process-step" data-reveal data-delay="3"><span class="process-step__num">04</span><h3>Delivered on time</h3><p>Ship nationwide or pick up locally. Reorders saved for one click.</p></div>
      </div>
    </div></section>

    <section class="section"><div class="container">
      <div class="section-head" data-reveal><span class="eyebrow">Our equipment</span><h2>Serious gear, in-house.</h2><p class="lead">Owning our equipment means controlling quality, speed and cost — and never blaming a vendor for a missed date.</p></div>
      <div class="grid grid--3" style="margin-top:2.5rem">{equip}</div>
    </div></section>

    <section class="section section--tight" style="background:var(--bg-soft)"><div class="container">
      <div class="section-head section-head--center" data-reveal><span class="eyebrow eyebrow--center">Meet the team</span><h2>The people behind your projects.</h2></div>
      <div class="team-grid" style="margin-top:3rem">{team}</div>
    </div></section>

    <section class="section"><div class="container split">
      <div class="media-frame split__media" data-reveal aria-hidden="true"><div class="ph" data-label="In the community"></div></div>
      <div data-reveal data-delay="1">
        <span class="eyebrow">Community</span>
        <h2 style="margin:1rem 0 1.2rem">Proud to back our community.</h2>
        <p>We donate apparel and awards to local schools, youth leagues and nonprofits every year, and we love sponsoring the teams and causes our neighbors care about.</p>
        <p class="muted" style="margin-top:1rem">Running a fundraiser or community event? Ask about our nonprofit and school pricing.</p>
      </div>
    </div></section>
{CTA}'''
    return page("about.html","About Us | Custom Creations Unlimited Custom Branding House",
        "Meet Custom Creations Unlimited — an 18-year custom branding house in Atlanta. Our mission, values, process, equipment and team behind premium embroidery, apparel, awards and engraving.",
        "about Custom Creations Unlimited, custom branding company, Atlanta embroidery company, our process, our team",
        "about", body)

# ==========================================================================
# CONTACT
# ==========================================================================
def contact_page():
    info = f'''<div class="contact-info" data-reveal>
        <a class="contact-row" href="tel:+14049678028"><span class="contact-row__icon"><svg viewBox="0 0 24 24" fill="none"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.7A2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 2 .7 2.9a2 2 0 01-.4 2.1L8.1 9.9a16 16 0 006 6l1.2-1.3a2 2 0 012.1-.4c.9.3 1.9.6 2.9.7a2 2 0 011.7 2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg></span><span><span class="contact-row__label">Call us</span><strong>(404) 967-8028</strong></span></a>
        <a class="contact-row" href="mailto:info@ccucustom.com"><span class="contact-row__icon"><svg viewBox="0 0 24 24" fill="none"><path d="M4 5h16v14H4zM4 6l8 6 8-6" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg></span><span><span class="contact-row__label">Email us</span><strong>info@ccucustom.com</strong></span></a>
        <div class="contact-row"><span class="contact-row__icon"><svg viewBox="0 0 24 24" fill="none"><path d="M12 21s-7-5.5-7-11a7 7 0 0114 0c0 5.5-7 11-7 11z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="2"/></svg></span><span><span class="contact-row__label">Showroom &amp; studio</span><strong>1180 Industrial Park Blvd, Suite 200<br>Atlanta, GA 30318</strong></span></div>
        <div class="contact-row"><span class="contact-row__icon"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span><span><span class="contact-row__label">Hours</span><strong>Mon–Fri 9am–6pm · Sat 10am–2pm</strong></span></div>
      </div>'''
    form = f'''<div data-reveal data-delay="1">
        <div class="form-card">
          <form class="form" action="https://formspree.io/f/xykqkqao" method="POST" data-mailto-form data-mailto="info@ccucustom.com" data-subject="Website contact message" novalidate>
            <input type="hidden" name="_subject" value="New website contact message" />
            <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true" />
            <div class="form-row">
              <div class="field"><label for="c-name">Name <span class="req">*</span></label><input class="input" id="c-name" name="Name" data-label="Name" required /></div>
              <div class="field"><label for="c-company">Company / Organization</label><input class="input" id="c-company" name="Company" data-label="Company" /></div>
            </div>
            <div class="form-row">
              <div class="field"><label for="c-email">Email <span class="req">*</span></label><input class="input" type="email" id="c-email" name="Email" data-label="Email" required /></div>
              <div class="field"><label for="c-phone">Phone</label><input class="input" type="tel" id="c-phone" name="Phone" data-label="Phone" /></div>
            </div>
            <div class="field"><label for="c-subject">How can we help?</label>
              <select class="select" id="c-subject" name="Topic" data-label="Topic">
                <option value="">Choose a topic…</option><option>Request a quote</option><option>Question about a service</option>
                <option>Existing order / reorder</option><option>Corporate account</option><option>Something else</option>
              </select></div>
            <div class="field"><label for="c-msg">Message <span class="req">*</span></label><textarea class="textarea" id="c-msg" name="Message" data-label="Message" placeholder="Tell us what you're looking for…" required></textarea></div>
            <button class="btn btn--gold btn--lg" type="submit">Send message {ARROW}</button>
            <p class="muted" style="font-size:.82rem">Prefer to talk? Call <a href="tel:+14049678028" style="color:var(--accent)">(404) 967-8028</a> during business hours.</p>
          </form>
        </div>
        <div class="form-success"><div class="form-success__icon"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <h3 style="font-size:1.5rem">Thanks — your message has been sent!</h3>
          <p class="muted" style="margin-top:.6rem">We've received your message and will reply within one business day.</p>
        </div>
      </div>'''
    body = f'''    <section class="page-hero page-hero--center"><div class="page-hero__bg" aria-hidden="true"></div>
      <div class="container"><div class="page-hero__inner">
        {breadcrumb("Contact", True)}
        <span class="eyebrow eyebrow--center" data-reveal>Get in touch</span>
        <h1 data-reveal data-delay="1">Let's talk about <span class="text-gradient">your project.</span></h1>
        <p data-reveal data-delay="2">Questions, quotes or a quick hello — reach us however you like. Real people, fast replies.</p>
      </div></div></section>

    <section class="section section--tight"><div class="container">
      <div class="contact-strip">{info}{form}</div>
    </div></section>

    <section class="section--tight" style="padding-bottom:var(--space-section)"><div class="container">
      <div class="map-wrap" data-reveal aria-hidden="false"><iframe title="Custom Creations Unlimited studio location map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Atlanta%2C%20GA%2030318&output=embed"></iframe></div>
    </div></section>'''
    return page("contact.html","Contact Custom Creations Unlimited | Custom Branding in Atlanta, GA",
        "Contact Custom Creations Unlimited for custom embroidery, apparel, awards and engraving. Call (404) 967-8028, email info@ccucustom.com, or visit our Atlanta studio. Mon–Fri 9–6.",
        "contact Custom Creations Unlimited, custom branding Atlanta, embroidery near me, request a quote, branding studio Atlanta",
        "contact", body)

# ==========================================================================
# QUOTE BUILDER
# ==========================================================================
SIZES = ["XS","S","M","L","XL","2XL","3XL","Youth"]
COLORS = [("Black","#111"),("White","#fff"),("Navy","#1f2b4d"),("Gray","#8a8d93"),("Red","#b22"),("Royal","#1c5bd8"),("Forest","#1f5132"),("Gold","#c8a24a")]
def quote_page():
    svc_opts = "".join(f"<option>{n}</option>" for _,n,_ in SVC) + "<option>Signs &amp; Banners</option><option>Business Printing</option><option>Not sure yet</option>"
    sizes = "".join(f'<label class="chip-opt"><input type="checkbox" name="size" value="{s}" data-group="Sizes"><span>{s}</span></label>' for s in SIZES)
    colors = "".join(f'<label class="chip-opt"><input type="checkbox" name="color" value="{n}" data-group="Colors"><span><span class="swatch" style="background:{c}"></span>{n}</span></label>' for n,c in COLORS)
    body = f'''    <section class="page-hero page-hero--center"><div class="page-hero__bg" aria-hidden="true"></div>
      <div class="container"><div class="page-hero__inner">
        {breadcrumb("Request a Quote", True)}
        <span class="eyebrow eyebrow--center" data-reveal>Request a quote</span>
        <h1 data-reveal data-delay="1">Tell us about <span class="text-gradient">your project.</span></h1>
        <p data-reveal data-delay="2">Fill in what you know — even a rough idea is enough. We'll follow up with a free proof and an exact quote, usually within one business day.</p>
      </div></div></section>

    <section class="section section--tight"><div class="container">
      <div class="quote-grid">
        <div class="form-card" data-reveal>
          <form class="form" action="https://formspree.io/f/xykqkqao" method="POST" data-mailto-form data-mailto="info@ccucustom.com" data-subject="New quote request" novalidate>
            <input type="hidden" name="_subject" value="New quote request from the website" />
            <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true" />
            <div class="fieldset">
              <legend class="fieldset__legend"><span class="n">1</span> Your project</legend>
              <div class="form-row">
                <div class="field"><label for="q-svc">Service / product type <span class="req">*</span></label>
                  <select class="select" id="q-svc" name="Service" data-label="Service" required><option value="">Choose a service…</option>{svc_opts}</select></div>
                <div class="field"><label for="q-qty">Estimated quantity <span class="req">*</span></label><input class="input" type="number" min="1" id="q-qty" name="Quantity" data-label="Quantity" placeholder="e.g. 48" required /></div>
              </div>
              <div class="field"><label for="q-desc">What do you need? <span class="req">*</span></label>
                <textarea class="textarea" id="q-desc" name="Description" data-label="Description" placeholder="e.g. Embroidered polos for our sales team, left-chest logo, in 3 colors." required></textarea></div>
              <div class="field"><label for="q-date">Need it by</label><input class="input" type="date" id="q-date" name="Need-by date" data-label="Need-by date" /></div>
            </div>

            <div class="fieldset">
              <legend class="fieldset__legend"><span class="n">2</span> Details</legend>
              <p class="fieldset__hint">Optional, but the more you tell us, the faster we can quote.</p>
              <div class="field"><span class="field-label">Sizes needed</span><div class="chip-group">{sizes}</div></div>
              <div class="field" style="margin-top:1.2rem"><span class="field-label">Colors</span><div class="chip-group">{colors}</div></div>
              <div class="form-row" style="margin-top:1.2rem">
                <div class="field"><label for="q-budget">Budget range</label>
                  <select class="select" id="q-budget" name="Budget" data-label="Budget"><option value="">Prefer not to say</option><option>Under $250</option><option>$250–$500</option><option>$500–$1,000</option><option>$1,000–$5,000</option><option>$5,000+</option></select></div>
                <div class="field"><label for="q-ship">Delivery</label>
                  <select class="select" id="q-ship" name="Delivery" data-label="Delivery"><option value="">Choose…</option><option>Local pickup (Atlanta)</option><option>Ship to one address</option><option>Ship to multiple addresses</option></select></div>
              </div>
              <div class="field" style="margin-top:1.2rem"><label for="q-personal">Personalization</label><input class="input" id="q-personal" name="Personalization" data-label="Personalization" placeholder="Names, numbers, dates, monograms…" /></div>
              <div class="field" style="margin-top:1.2rem"><span class="field-label">Logo / artwork</span>
                <label class="upload"><input type="file" name="logo" accept="image/*,.pdf,.ai,.eps,.svg" multiple>
                  <svg viewBox="0 0 24 24" fill="none"><path d="M12 16V4M7 9l5-5 5 5M5 20h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <strong>Click to upload</strong> or drag &amp; drop<br><span style="font-size:.8rem">PNG, JPG, PDF, AI, EPS or SVG</span>
                  <span class="upload__name" hidden></span>
                </label>
                <span class="hint">Your file uploads securely with your request — no need to email it separately.</span></div>
            </div>

            <div class="fieldset">
              <legend class="fieldset__legend"><span class="n">3</span> Your contact</legend>
              <div class="form-row">
                <div class="field"><label for="q-name">Name <span class="req">*</span></label><input class="input" id="q-name" name="Name" data-label="Name" required /></div>
                <div class="field"><label for="q-company">Company / Organization</label><input class="input" id="q-company" name="Company" data-label="Company" /></div>
              </div>
              <div class="form-row">
                <div class="field"><label for="q-email">Email <span class="req">*</span></label><input class="input" type="email" id="q-email" name="Email" data-label="Email" required /></div>
                <div class="field"><label for="q-phone">Phone</label><input class="input" type="tel" id="q-phone" name="Phone" data-label="Phone" /></div>
              </div>
              <div class="field"><label for="q-notes">Special instructions</label><textarea class="textarea" id="q-notes" name="Special instructions" data-label="Special instructions" placeholder="Anything else we should know?"></textarea></div>
            </div>

            <button class="btn btn--gold btn--lg" type="submit">Submit quote request {ARROW}</button>
            <p class="muted" style="font-size:.82rem">No obligation. We'll reply with a free proof and exact pricing.</p>
          </form>
        </div>

        <aside class="quote-aside" data-reveal data-delay="1">
          <div class="aside-card">
            <h3>How it works</h3>
            <div class="aside-step"><span class="aside-step__n">1</span><p><strong>Submit this form</strong><br>Tell us as much as you know.</p></div>
            <div class="aside-step"><span class="aside-step__n">2</span><p><strong>Get a free proof</strong><br>Plus an exact quote, usually within a day.</p></div>
            <div class="aside-step"><span class="aside-step__n">3</span><p><strong>Approve &amp; relax</strong><br>We produce and deliver on time.</p></div>
          </div>
          <div class="aside-card">
            <h3>Why Custom Creations Unlimited</h3>
            <ul class="aside-trust">
              <li>{CHECK}<span>No minimums on most items</span></li>
              <li>{CHECK}<span>Free design proofs &amp; revisions</span></li>
              <li>{CHECK}<span>Everything made in-house</span></li>
              <li>{CHECK}<span>Rush turnaround available</span></li>
              <li>{CHECK}<span>4.9/5 from 1,280+ reviews</span></li>
            </ul>
          </div>
          <div class="aside-card" style="background:var(--grad-ink);color:var(--text-inverse);border:0">
            <h3 style="color:#fff">Rather just call?</h3>
            <p style="color:rgba(247,244,238,.8);font-size:.92rem;margin-bottom:1rem">Talk through your project with a real person.</p>
            <a class="btn btn--gold btn--block" href="tel:+14049678028">(404) 967-8028</a>
          </div>
        </aside>
      </div>
      <div class="form-success" style="max-width:640px;margin:2rem auto 0">
        <div class="form-success__icon"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <h2>Thanks — your quote request has been sent!</h2>
        <p class="muted" style="margin-top:.7rem">We've received your details and will get back to you within one business day with a free proof and exact pricing.</p>
        <div style="margin-top:1.4rem"><a class="btn btn--ghost" href="index.html">Back to home</a></div>
      </div>
    </div></section>'''
    return page("quote.html","Request a Quote | Custom Branding | Custom Creations Unlimited",
        "Request a free quote from Custom Creations Unlimited for custom embroidery, apparel, promotional products, awards, laser engraving and personalized gifts. Free proofs, fast turnaround, no obligation.",
        "request a quote, custom branding quote, embroidery quote, custom apparel quote, promotional products quote, Atlanta",
        "quote", body)

# ==========================================================================
# FAQ
# ==========================================================================
FAQ_GROUPS = [
    ("Ordering & quotes", [
        ("How do I get a quote?", "Use our <a href=\"quote.html\" style=\"color:var(--accent)\">quote builder</a>, email <a href=\"mailto:info@ccucustom.com\" style=\"color:var(--accent)\">info@ccucustom.com</a>, call (404) 967-8028, or stop by the studio. We reply with a free proof and exact pricing — usually within one business day."),
        ("Is there a minimum order?", "Most items have no minimum — order a single engraved gift or thousands of branded shirts. Screen printing is most cost-effective at 12+ pieces; we'll always recommend the best method for your quantity."),
        ("How much will my order cost?", "Pricing depends on the product, decoration method, quantity and number of colors. Per-piece cost drops as quantities grow. Send us the details and we'll give you transparent, itemized pricing — no hidden fees."),
        ("Do you require a deposit?", "For most orders we collect payment or a deposit once you approve your proof, before production begins. Established corporate accounts can be set up with terms."),
    ]),
    ("Artwork & design", [
        ("What file formats do you accept?", "Vector files (AI, EPS, PDF, SVG) are ideal, but we can work from high-resolution PNG or JPG too. Not sure? Send what you have and we'll tell you if anything's needed."),
        ("Do you help with design?", "Yes. Send your logo and we'll prepare it for production at no charge, or our in-house designers can create artwork from scratch. You'll always approve a free digital proof before we produce anything."),
        ("Will I see a proof before production?", "Always. Every order includes a free digital proof so you can confirm colors, placement, sizing and spelling. We revise until it's right — then nothing goes into production without your approval."),
        ("Can you match my exact brand colors?", "Yes — we match thread colors and PMS values for embroidery and printing so your logo stays on-brand across every product and reorder."),
    ]),
    ("Production & turnaround", [
        ("How fast can I get my order?", "Standard turnaround is 7–10 business days after proof approval. Rush service is available on most products — tell us your deadline in the quote and we'll confirm what's possible."),
        ("Can you handle rush orders?", "Often, yes. We keep capacity for tight deadlines and event dates. Share your in-hands date up front and we'll tell you immediately whether we can meet it."),
        ("Do you make everything in-house?", "Yes — embroidery, printing, laser engraving and awards are all produced under one roof. That means tighter quality control, faster turnaround and one point of contact."),
    ]),
    ("Shipping & pickup", [
        ("Do you ship nationwide?", "Yes. We ship anywhere in the US and can drop-ship to multiple addresses for company-wide rollouts. Local clients are welcome to pick up at our Atlanta studio."),
        ("Can you ship to multiple locations?", "Absolutely — kitting and split-shipping to individual team members or offices is one of our specialties for corporate accounts."),
    ]),
    ("Products & materials", [
        ("What can you put a logo on?", "Almost anything — apparel, caps, bags, drinkware, awards, signs, tech, leather, wood, glass and metal. If you have a product in mind we haven't listed, just ask."),
        ("Can I supply my own garments or items?", "Often, yes. We offer decoration on customer-supplied goods after a quick suitability check on the fabric, material or coating."),
        ("Is embroidery or printing more durable?", "Both last well when done right. Embroidery never cracks or fades and gives a premium, dimensional finish; printing is better for large, full-color or photographic designs. We'll recommend the best fit."),
    ]),
    ("Corporate accounts", [
        ("Do you offer corporate accounts?", "Yes. Corporate and recurring clients get dedicated account management, stored brand standards, volume pricing, online reorders and split shipping. Many run uniform and recognition programs with us year-round."),
        ("Can you manage an ongoing uniform program?", "That's a core service. We store your approved artwork and garment specs so reorders are fast, consistent and one click away — across years and locations."),
    ]),
]
def faq_page():
    import json
    sections = ""
    schema_items = []
    for gi, (title, qas) in enumerate(FAQ_GROUPS):
        items = "".join(
            f'''<div class="faq-item"><button class="faq-q" aria-expanded="false"><span>{q}</span><span class="faq-icon"><svg viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span></button><div class="faq-a"><div class="faq-a__inner">{a}</div></div></div>'''
            for q, a in qas)
        bg = ' style="background:var(--bg-soft)"' if gi % 2 else ''
        sections += f'''<section class="section section--tight"{bg}><div class="container">
          <div class="section-head" data-reveal style="margin-bottom:1.5rem"><span class="eyebrow">{title}</span></div>
          <div class="faq-list" data-reveal>{items}</div>
        </div></section>'''
        for q, a in qas:
            plain = re.sub(r'<[^>]+>', '', a)
            schema_items.append({"@type": "Question", "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": plain}})
    schema = '<script type="application/ld+json">' + json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": schema_items}) + '</script>'
    body = f'''    <section class="page-hero page-hero--center"><div class="page-hero__bg" aria-hidden="true"></div>
      <div class="container"><div class="page-hero__inner">
        {breadcrumb("FAQ", True)}
        <span class="eyebrow eyebrow--center" data-reveal>Help center</span>
        <h1 data-reveal data-delay="1">Frequently asked <span class="text-gradient">questions.</span></h1>
        <p data-reveal data-delay="2">Everything you need to know about ordering, artwork, turnaround and more. Still stuck? We're a call or click away.</p>
      </div></div></section>
{sections}
{CTA}'''
    return page("faq.html", "FAQ | Custom Branding Questions Answered | Custom Creations Unlimited",
        "Answers to common questions about Custom Creations Unlimited custom embroidery, apparel, awards and engraving — ordering, artwork, turnaround, shipping, minimums and corporate accounts.",
        "custom branding FAQ, embroidery questions, order minimums, turnaround time, artwork files, corporate accounts",
        "faq", body, schema=schema)

import re  # used by faq_page schema stripping

# ---- write ----------------------------------------------------------------
def main():
    pages = {
        "gallery.html": gallery_page(), "industries.html": industries_page(),
        "about.html": about_page(), "contact.html": contact_page(), "quote.html": quote_page(),
        "faq.html": faq_page(),
    }
    for fn, html in pages.items():
        with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", fn)

if __name__ == "__main__":
    main()
