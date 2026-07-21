#!/usr/bin/env python3
"""
Custom Creations Unlimited blog generator: blog/index.html + individual posts.
Lives one level deep, so all shared links use the '../' prefix.
Run:  python3 scripts/build-blog.py
"""
import os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "blog")
P = "../"  # prefix from inside /blog

SVC = [
    ("embroidery", "Embroidery"), ("custom-apparel", "Custom Apparel"),
    ("promotional-products", "Promotional Products"), ("awards", "Awards & Recognition"),
    ("laser-engraving", "Laser Engraving"), ("personalized-gifts", "Personalized Gifts"),
]
ARROW = '<svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
NAV = [(P+"index.html","Home","home"),(P+"about.html","About","about"),
       (P+"index.html#services","Services","services"),(P+"shop.html","Shop","shop"),
       (P+"gallery.html","Gallery","gallery"),(P+"industries.html","Industries","industries"),
       ("index.html","Blog","blog"),
       (P+"faq.html","FAQ","faq"),(P+"contact.html","Contact","contact")]

def header(active):
    mega = "".join(
        f'''<a class="mega-link" href="{P}services/{s}.html" role="menuitem"><span class="mega-link__icon"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/></svg></span><span><span class="mega-link__title">{n}</span></span></a>'''
        for s, n in SVC)
    items = []
    for href, label, key in NAV:
        if key == "services":
            items.append(f'''<li class="nav-item nav-item--has-mega"><a class="nav-link" href="{href}" aria-haspopup="true">Services <svg class="chev" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a><div class="mega" role="menu"><div class="mega-grid">{mega}</div><div class="mega-foot"><span>Not sure where to start? Our team will guide you.</span><a class="link-arrow" href="{P}quote.html">Request a quote {ARROW}</a></div></div></li>''')
        else:
            cur = ' aria-current="page"' if active == key else ""
            items.append(f'<li class="nav-item"><a class="nav-link" href="{href}"{cur}>{label}</a></li>')
    return f'''<header class="site-header" id="header"><div class="container header-inner">
      <a class="brand" href="{P}index.html" aria-label="Custom Creations Unlimited home"><svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="currentColor" style="color:var(--ink-900)"/><text x="20" y="26" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="13" font-weight="700" fill="var(--gold-400)" style="letter-spacing:.5px">CCU</text></svg><span class="brand__name">Custom Creations</span></a>
      <nav class="primary-nav" aria-label="Primary"><ul class="nav-list">{"".join(items)}</ul></nav>
      <div class="header-actions">
        <button class="icon-btn theme-toggle" id="themeToggle" aria-label="Toggle dark mode"><svg class="sun" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><svg class="moon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg></button>
        <a class="btn btn--gold" href="{P}quote.html">Request a Quote</a>
        <button class="icon-btn nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
      </div></div></header>
  <div class="mobile-nav" id="mobileNav" aria-hidden="true"><ul class="mobile-nav__list">
      <li><a class="mobile-nav__link" href="{P}index.html">Home</a></li>
      <li><a class="mobile-nav__link" href="{P}about.html">About</a></li>
      <li><button class="mobile-nav__link" data-sub="m-services" aria-expanded="false">Services <svg viewBox="0 0 24 24" fill="none" width="20"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <div class="mobile-nav__sub" id="m-services">{"".join(f'<a href="{P}services/{s}.html">{n}</a>' for s,n in SVC)}</div></li>
      <li><a class="mobile-nav__link" href="{P}shop.html">Shop</a></li>
      <li><a class="mobile-nav__link" href="{P}gallery.html">Gallery</a></li>
      <li><a class="mobile-nav__link" href="{P}industries.html">Industries</a></li>
      <li><a class="mobile-nav__link" href="index.html">Blog</a></li>
      <li><a class="mobile-nav__link" href="{P}faq.html">FAQ</a></li>
      <li><a class="mobile-nav__link" href="{P}contact.html">Contact</a></li>
    </ul>
    <div class="mobile-nav__cta"><a class="btn btn--gold btn--lg btn--block" href="{P}quote.html">Request a Quote</a><a class="btn btn--ghost btn--lg btn--block" href="tel:+14049678028">Call (404) 967-8028</a></div>
  </div>'''

FOOTER = f'''<footer class="site-footer"><div class="container"><div class="footer-top">
      <div class="footer-brand"><a class="brand" href="{P}index.html" aria-label="Custom Creations Unlimited home"><svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#16161f"/><text x="20" y="26" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="13" font-weight="700" fill="var(--gold-400)" style="letter-spacing:.5px">CCU</text></svg><span class="brand__name">Custom Creations</span></a>
        <p>A premium custom branding house — embroidery, apparel, promotional products, awards, laser engraving and personalized gifts, all under one roof.</p>
        <div class="footer-social"><a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 9h3V6h-3c-2 0-3 1.3-3 3.2V11H8v3h3v7h3v-7h2.5l.5-3H14V9.5c0-.3.2-.5.6-.5z"/></svg></a><a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><circle cx="17" cy="7" r="1.2" fill="currentColor"/></svg></a><a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.5 8A1.5 1.5 0 106.5 5 1.5 1.5 0 006.5 8zM5 10h3v9H5zM10 10h3v1.3c.5-.8 1.5-1.5 3-1.5 2.2 0 3 1.4 3 3.8V19h-3v-4.6c0-1.1-.4-1.8-1.4-1.8s-1.6.7-1.6 1.8V19h-3z"/></svg></a></div>
      </div>
      <div class="footer-col"><h4>Services</h4>{"".join(f'<a href="{P}services/{s}.html">{n}</a>' for s,n in SVC)}</div>
      <div class="footer-col"><h4>Company</h4><a href="{P}about.html">About Us</a><a href="{P}shop.html">Shop</a><a href="{P}gallery.html">Gallery</a><a href="{P}industries.html">Industries</a><a href="index.html">Blog</a><a href="{P}faq.html">FAQ</a><a href="{P}contact.html">Contact</a></div>
      <div class="footer-col"><h4>Get in touch</h4><a href="tel:+14049678028">(404) 967-8028</a><a href="mailto:info@ccucustom.com">info@ccucustom.com</a><a href="{P}contact.html">1180 Industrial Park Blvd<br>Atlanta, GA 30318</a></div>
    </div>
    <div class="footer-bottom"><span>© <span id="year"></span> Custom Creations Unlimited All rights reserved. · Atlanta, GA</span><nav aria-label="Legal"><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Accessibility</a></nav></div>
  </div></footer>
  <div class="floating"><a class="fab fab--call" href="tel:+14049678028" aria-label="Call us"><svg viewBox="0 0 24 24" fill="none"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.7A2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 2 .7 2.9a2 2 0 01-.4 2.1L8.1 9.9a16 16 0 006 6l1.2-1.3a2 2 0 012.1-.4c.9.3 1.9.6 2.9.7a2 2 0 011.7 2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg></a><a class="fab fab--quote" href="{P}quote.html" aria-label="Request a quote"><svg viewBox="0 0 24 24" fill="none"><path d="M4 5h16v11H8l-4 4z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8 9h8M8 12h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></a></div>
  <button class="back-to-top" id="backToTop" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none"><path d="M12 19V5M5 12l7-7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
  <script src="{P}assets/js/main.js?v=2" defer></script>'''

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin /><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230a0a0f'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-family='Georgia,serif' font-size='11' font-weight='700' fill='%23c8a24a'%3ECCU%3C/text%3E%3C/svg%3E"

def page(slug, title, desc, keywords, active, body, schema=""):
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="theme-color" content="#0a0a0f" />
  <title>{title}</title>
  <meta name="description" content="{desc}" /><meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="https://www.ccucustom.com/blog/{slug}" />
  <meta property="og:type" content="article" /><meta property="og:site_name" content="Custom Creations Unlimited" />
  <meta property="og:title" content="{title}" /><meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://www.ccucustom.com/blog/{slug}" />
  <meta property="og:image" content="https://www.ccucustom.com/assets/img/og-cover.jpg" /><meta name="twitter:card" content="summary_large_image" />
  {FONT}
  <link rel="stylesheet" href="{P}assets/css/styles.css?v=2" /><link rel="icon" href="{FAVICON}" />
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

def crumb(label, parent=True):
    chev = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    mid = f'<a href="index.html">Blog</a>{chev}' if parent else ''
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><a href="{P}index.html">Home</a>{chev}{mid}<span aria-current="page">{label}</span></nav>'

# ==========================================================================
# Posts
# ==========================================================================
POSTS = [
    {
        "slug": "advantages-of-uv-printing",
        "title": "The Advantages of UV Printing",
        "cat": "tips", "cat_label": "Printing",
        "excerpt": "UV printing cures ink instantly with light, laying down sharp, full-color, durable graphics on almost any material — from tumblers to acrylic signs. Here's why it's a game-changer for branded hard goods.",
        "date": "June 25, 2026", "read": "5 min read", "author": "Riley Chen", "ai": "RC",
        "tags": ["UV Printing", "Promotional Products", "Signage"],
        "lead": "Ever wondered how a full-color logo ends up crisp and vivid on a metal tumbler, an acrylic sign, or a phone case? Nine times out of ten, the answer is UV printing.",
        "blocks": [
            ("h2", "What UV printing actually is"),
            ("p", "UV printing is digital inkjet with a twist: instead of soaking into the surface and air-drying, the ink is cured — hardened instantly — by ultraviolet light the moment it's laid down. The ink sits crisply on top of the material, locked in with brilliant color and almost no bleed."),
            ("h2", "It prints on almost anything"),
            ("p", "Because the ink cures on contact instead of needing an absorbent surface, UV printing bonds to materials traditional printing struggles with — hard, smooth, and even clear ones."),
            ("ul", ["Drinkware — tumblers, bottles and mugs", "Signage, acrylic displays and nameplates", "Phone cases and tech accessories", "Promotional products and giveaways", "Awards, plaques and trophies", "Wood, leather, glass and metal"]),
            ("h2", "Vivid, photo-grade color"),
            ("p", "Full CMYK plus white ink means photographic detail, smooth gradients and bright, accurate brand colors — even on dark or transparent materials, where a white underbase makes the artwork pop. Your logo prints exactly as designed."),
            ("h2", "Fast, durable and clean"),
            ("p", "Instant curing means no drying time, which speeds up turnaround, and the finished print is scratch-, water- and fade-resistant — it stands up to the daily handling promo products and signage take. UV inks are also low-odor and low-VOC compared with solvent printing."),
            ("quote", "UV printing is the closest thing we have to “print your logo, in full color, on practically anything.”"),
            ("h2", "Special effects: white, gloss and texture"),
            ("p", "Beyond flat color, UV printing can lay down a white base for dark or clear items, add spot gloss for shine, and even build up raised, textured prints you can feel — a premium tactile touch for awards and high-end gifts."),
            ("h2", "When we reach for it"),
            ("p", "For full-color logos on hard goods, short runs with no screens or setup, and items embroidery or screen printing can't touch, UV printing is usually the best tool. For apparel we still lean on DTF, screen printing and embroidery — but for drinkware, signage, awards and promo, UV printing is hard to beat."),
        ],
        "related": ["promotional-products-worth-the-spend", "embroidery-vs-screen-print-vs-dtf"],
    },
    {
        "slug": "embroidery-vs-screen-print-vs-dtf",
        "title": "Embroidery vs. Screen Printing vs. DTF: Which Is Right for Your Order?",
        "cat": "tips", "cat_label": "Buying Guide",
        "excerpt": "The three most popular ways to decorate apparel — and a simple framework for choosing the right one for your logo, quantity and budget.",
        "date": "June 18, 2026", "read": "6 min read", "author": "Sam Delgado", "ai": "SD",
        "tags": ["Embroidery", "Apparel", "Printing"],
        "lead": "If you've ever stared at a quote wondering why the same shirt costs different amounts depending on the method, you're not alone. Here's how to choose with confidence.",
        "blocks": [
            ("h2", "Embroidery: premium, durable, tactile"),
            ("p", "Embroidery stitches your logo in thread, so it never cracks, peels or fades. The raised finish reads as high-end the moment someone touches it, which is why it's the default for polos, caps, jackets and corporate uniforms."),
            ("p", "It's best for logos and text. Very small lettering or photo-realistic art doesn't translate to thread, and large solid areas get heavy — so a full-back design may cost more than you'd expect."),
            ("h2", "Screen printing: the value champion at volume"),
            ("p", "Screen printing pushes thick, durable ink through a stencil. There's a setup step per color, so it shines on larger runs of the same design — the per-piece price drops fast as quantities climb."),
            ("p", "It's ideal for bold, 1–4 color designs on tees and hoodies for teams, events and giveaways. It's less suited to tiny orders or full-color, gradient-heavy artwork."),
            ("h2", "DTF: full color, no minimums"),
            ("p", "Direct-to-film (DTF) prints photo-quality, full-color transfers that bond to almost any fabric with a soft feel. There's no per-color setup, so it's perfect for small runs, complex art and mixed garment types in one order."),
            ("quote", "Our rule of thumb: embroidery for premium logo wear, screen printing for big single-design runs, DTF for everything full-color or low-quantity."),
            ("h2", "Still not sure? That's what we're here for"),
            ("p", "Send us your artwork, quantity and the garments you have in mind. We'll recommend the method that gives you the best look, durability and price — and show you a free proof before anything is produced."),
        ],
        "related": ["build-a-uniform-program", "promotional-products-worth-the-spend"],
    },
    {
        "slug": "build-a-uniform-program",
        "title": "How to Build a Company Uniform Program Employees Actually Wear",
        "cat": "branding", "cat_label": "Branding",
        "excerpt": "A great uniform program is equal parts brand consistency and employee buy-in. Here's how to nail both without the logistical headache.",
        "date": "June 9, 2026", "read": "5 min read", "author": "Taylor Brooks", "ai": "TB",
        "tags": ["Uniforms", "Embroidery", "Corporate"],
        "lead": "The best uniform isn't the one with the biggest logo — it's the one your team reaches for on their day off. Comfort and consistency win.",
        "blocks": [
            ("h2", "Start with garments people like wearing"),
            ("p", "Buy-in lives or dies on comfort and fit. Offer a small, curated range — a soft tee, a quality polo and a jacket — in modern cuts and inclusive sizing rather than one stiff option nobody loves."),
            ("h2", "Lock your brand standards once"),
            ("p", "Decide logo placement, thread or ink colors, and which garments are approved — then store those specs so every reorder is identical, no matter who places it or when."),
            ("ul", ["Left-chest logo for polos and jackets", "Consistent thread colors matched to your brand", "An approved garment list with set colors", "Optional names or departments for personalization"]),
            ("h2", "Make reordering effortless"),
            ("p", "Turnover and growth mean constant top-ups. A partner that keeps your artwork and specs on file turns a new-hire order into a one-line email instead of starting from scratch each time."),
            ("quote", "When the gear is comfortable and the process is easy, the program runs itself — and your brand shows up everywhere."),
            ("h2", "Plan for scale"),
            ("p", "If you're rolling out across locations, ask about kitting and split-shipping so each site or employee receives the right sizes, boxed and ready. It's the difference between a launch and a logistics nightmare."),
        ],
        "related": ["embroidery-vs-screen-print-vs-dtf", "corporate-gifting-that-works"],
    },
    {
        "slug": "promotional-products-worth-the-spend",
        "title": "Promotional Products That Are Actually Worth the Spend",
        "cat": "promotional", "cat_label": "Promotional",
        "excerpt": "Swag has a reputation problem. The fix isn't spending more — it's choosing items people genuinely keep and use.",
        "date": "May 28, 2026", "read": "4 min read", "author": "Jordan Avery", "ai": "JA",
        "tags": ["Promotional", "Drinkware", "Events"],
        "lead": "Every dollar on a giveaway nobody keeps is marketing thrown away. Spend it on something useful and it markets you for years.",
        "blocks": [
            ("h2", "Useful beats clever"),
            ("p", "The best promo products earn a place in someone's daily routine: a quality insulated tumbler, a sturdy tote, a power bank that actually holds a charge. Usefulness equals impressions."),
            ("h2", "Quality is the message"),
            ("p", "A flimsy item tells people exactly what you think their attention is worth. One well-made product leaves a far better impression than a bag of throwaways — and costs less in wasted spend."),
            ("ul", ["Insulated drinkware people use daily", "Bags that replace the one they own", "Tech that solves a small annoyance", "Notebooks and pens that feel premium"]),
            ("h2", "Match the item to the moment"),
            ("p", "Trade show? Pick something light and memorable. New-hire kit? Go for a curated set that says 'glad you're here.' Client gift? Lead with quality over quantity, every time."),
            ("quote", "Hand someone one thing they'll keep, not five they'll toss. Your logo lives longer and your budget goes further."),
        ],
        "related": ["corporate-gifting-that-works", "embroidery-vs-screen-print-vs-dtf"],
    },
    {
        "slug": "corporate-gifting-that-works",
        "title": "Corporate Gifting That Doesn't End Up in a Drawer",
        "cat": "promotional", "cat_label": "Gifting",
        "excerpt": "Thoughtful, well-made, personalized — the three traits that separate a memorable corporate gift from forgettable branded clutter.",
        "date": "May 14, 2026", "read": "5 min read", "author": "Sam Delgado", "ai": "SD",
        "tags": ["Gifts", "Engraving", "Corporate"],
        "lead": "A gift is a message about the relationship. Make it feel considered and it pays you back in goodwill and referrals.",
        "blocks": [
            ("h2", "Personalize beyond the logo"),
            ("p", "A logo says 'from us.' A name, date or short message says 'for you.' Laser-engraved drinkware, a personalized cutting board or a leather journal turns a giveaway into a keepsake."),
            ("h2", "Quality they can feel"),
            ("p", "Corporate gifts are seen by the people whose opinion you care about most — clients, partners, your best employees. Choose materials with weight and finish that reflect well on your brand."),
            ("quote", "The best corporate gifts don't shout your logo. They quietly say you paid attention."),
            ("h2", "Make it easy to scale"),
            ("p", "Gifting a hundred clients? We curate the item, personalize each one, gift-box it and ship — to one address or many. You approve a proof; we handle the rest."),
        ],
        "related": ["promotional-products-worth-the-spend", "awards-that-feel-earned"],
    },
    {
        "slug": "awards-that-feel-earned",
        "title": "Choosing Awards That Make Recognition Feel Earned",
        "cat": "awards", "cat_label": "Awards",
        "excerpt": "Recognition is only as meaningful as the object that marks it. Here's how to choose awards that honorees are proud to display.",
        "date": "April 30, 2026", "read": "4 min read", "author": "Taylor Brooks", "ai": "TB",
        "tags": ["Awards", "Recognition", "Engraving"],
        "lead": "The right award turns a milestone into a moment someone keeps on their shelf for decades. The wrong one gets a polite thank-you and a drawer.",
        "blocks": [
            ("h2", "Weight and material matter"),
            ("p", "Genuine crystal and glass have a heft that people instantly read as premium. That physical quality is a big part of why recognition lands — it feels like the achievement it represents."),
            ("h2", "Get the engraving right"),
            ("p", "Clean, well-laid-out engraving with correct names, dates and titles is non-negotiable. Always approve a proof — a misspelled name undoes the whole gesture."),
            ("ul", ["Crystal and glass for premium moments", "Engraved plaques for classic, wall-worthy recognition", "Acrylic for budget-friendly volume", "Gift boxing for a memorable presentation"]),
            ("h2", "Think program, not one-off"),
            ("p", "Annual awards look best when they're consistent year over year. We store your design and specs so every cycle matches — and individual names and dates are handled across the whole set."),
            ("quote", "Recognition is a feeling. The award is how you make that feeling something they can hold."),
        ],
        "related": ["corporate-gifting-that-works", "build-a-uniform-program"],
    },
]
# Dates are computed relative to today so the blog always looks current.
# Offsets (days ago) aligned to POSTS order (index 0 = featured/newest).
_today = datetime.date.today()
for _p, _ago in zip(POSTS, (2, 10, 19, 28, 38, 50)):
    _d = _today - datetime.timedelta(days=_ago)
    _p["date"] = f"{_d.strftime('%B')} {_d.day}, {_d.year}"

BYSLUG = {p["slug"]: p for p in POSTS}

def render_blocks(blocks):
    out = []
    for kind, content in blocks:
        if kind == "h2": out.append(f"<h2>{content}</h2>")
        elif kind == "p": out.append(f"<p>{content}</p>")
        elif kind == "quote": out.append(f"<blockquote>{content}</blockquote>")
        elif kind == "ul": out.append("<ul>" + "".join(f"<li>{x}</li>" for x in content) + "</ul>")
        elif kind == "ol": out.append("<ol>" + "".join(f"<li>{x}</li>" for x in content) + "</ol>")
    return "\n".join(out)

def post_page(post):
    import json
    schema = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"],
        "description": post["excerpt"], "datePublished": post["date"],
        "author": {"@type": "Person", "name": post["author"]},
        "publisher": {"@type": "Organization", "name": "Custom Creations Unlimited"},
        "mainEntityOfPage": f"https://www.ccucustom.com/blog/{post['slug']}.html",
    }) + '</script>'
    related = "".join(card(BYSLUG[s]) for s in post.get("related", []) if s in BYSLUG)
    body = f'''    <article>
    <section class="post-hero"><div class="page-hero__bg" aria-hidden="true"></div>
      <div class="container"><div class="post-hero__inner">
        {crumb(post["cat_label"])}
        <span class="post-cat" data-reveal>{post["cat_label"]}</span>
        <h1 data-reveal data-delay="1">{post["title"]}</h1>
        <div class="post-hero__meta" data-reveal data-delay="2">
          <span class="author"><span class="author__avatar">{post["ai"]}</span> By <strong>{post["author"]}</strong></span>
          <span>{post["date"]}</span><span class="post-meta__dot"></span><span>{post["read"]}</span>
        </div>
      </div></div>
    </section>
    <section class="section section--tight"><div class="container">
      <figure class="media-frame" style="max-width:960px;margin:0 auto 2.5rem;aspect-ratio:16/8" data-reveal><div class="ph" data-label="{post['cat_label']}"></div></figure>
      <div class="article" data-reveal>
        <p>{post["lead"]}</p>
        {render_blocks(post["blocks"])}
      </div>
      <div class="post-foot">
        <div class="post-tags">{"".join(f"<span>{t}</span>" for t in post["tags"])}</div>
        <a class="btn btn--gold" href="{P}quote.html">Start your project {ARROW}</a>
      </div>
    </div></section>
    </article>
    <section class="section section--tight" style="background:var(--bg-soft)"><div class="container">
      <div class="section-head" data-reveal><span class="eyebrow">Keep reading</span><h2>Related articles</h2></div>
      <div class="blog-grid" style="margin-top:2rem">{related}</div>
    </div></section>'''
    return page(f"{post['slug']}.html", f"{post['title']} | Custom Creations Unlimited Blog", post["excerpt"],
                ", ".join(post["tags"]) + ", custom branding, Atlanta", "blog", body, schema=schema)

def card(post, featured=False):
    meta = f'''<div class="post-meta"><span>{post["date"]}</span><span class="post-meta__dot"></span><span>{post["read"]}</span></div>'''
    if featured:
        return f'''<a class="featured-post" href="{post['slug']}.html" data-reveal>
          <div class="featured-post__media" style="position:relative"><span class="featured-tag">Featured</span><div class="ph" data-label="{post['cat_label']}"></div></div>
          <div class="featured-post__body"><span class="post-cat">{post['cat_label']}</span><h2>{post['title']}</h2><p>{post['excerpt']}</p>
          <div class="post-meta">{post['date']} <span class="post-meta__dot"></span> {post['read']} <span class="post-meta__dot"></span> By {post['author']}</div>
          <div style="margin-top:1.4rem"><span class="link-arrow">Read article {ARROW}</span></div></div></a>'''
    return f'''<a class="post-card" href="{post['slug']}.html" data-cat="{post['cat']}" data-reveal>
        <div class="post-card__media"><div class="ph" data-label="{post['cat_label']}"></div></div>
        <div class="post-card__body"><span class="post-cat">{post['cat_label']}</span><h3>{post['title']}</h3><p>{post['excerpt']}</p>{meta}</div></a>'''

def blog_index():
    featured = POSTS[0]
    rest = POSTS[1:]
    cats = [("all", "All posts"), ("branding", "Branding"), ("promotional", "Promotional"),
            ("awards", "Awards"), ("tips", "Buying Guides")]
    filters = "".join(f'<button class="filter-btn{" is-active" if k=="all" else ""}" data-filter="{k}">{n}</button>' for k, n in cats)
    grid = "".join(card(p) for p in rest)
    body = f'''    <section class="page-hero page-hero--center"><div class="page-hero__bg" aria-hidden="true"></div>
      <div class="container"><div class="page-hero__inner">
        {crumb("Blog", parent=False)}
        <span class="eyebrow eyebrow--center" data-reveal>The Custom Creations Unlimited journal</span>
        <h1 data-reveal data-delay="1">Ideas for <span class="text-gradient">branding better.</span></h1>
        <p data-reveal data-delay="2">Practical guides on apparel, promo, awards and gifting — from the team that makes them every day.</p>
      </div></div></section>

    <section class="section section--tight"><div class="container">
      {card(featured, featured=True)}
    </div></section>

    <section class="section--tight section" style="padding-top:0"><div class="container">
      <div class="gallery-filters" data-reveal role="tablist" aria-label="Filter articles">{filters}</div>
      <div class="blog-grid">{grid}</div>
    </div></section>

    <section class="section"><div class="container"><div class="cta-banner" data-reveal><div class="cta-banner__inner">
      <span class="eyebrow eyebrow--center" style="color:var(--gold-300)">Newsletter</span>
      <h2>Branding tips, in your inbox.</h2>
      <p>New products, seasonal offers and practical ideas — about once a month, no spam.</p>
      <form id="newsletter" class="footer-news" style="max-width:440px;margin:1.6rem auto 0" novalidate>
        <input type="email" name="email" placeholder="Your email" aria-label="Email address" required style="background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.2);color:#fff" />
        <button class="btn btn--gold" type="submit">Subscribe</button>
      </form>
      <p id="news-msg" style="font-size:.85rem;margin-top:.8rem;color:var(--gold-300)" hidden>Thanks — you're on the list!</p>
    </div></div></div></section>'''
    schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Blog","name":"Custom Creations Unlimited Journal","url":"https://www.ccucustom.com/blog/"}</script>'
    return page("index.html", "Blog | Custom Branding Tips & Guides | Custom Creations Unlimited",
        "The Custom Creations Unlimited journal — practical guides on custom apparel, embroidery, promotional products, awards and corporate gifting from a premium branding house.",
        "custom branding blog, embroidery tips, promotional products guide, corporate gifting, awards, apparel printing",
        "blog", body, schema=schema)

def main():
    os.makedirs(OUT, exist_ok=True)
    outputs = {"index.html": blog_index()}
    for p in POSTS:
        outputs[f"{p['slug']}.html"] = post_page(p)
    for fn, html in outputs.items():
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", "blog/" + fn)

if __name__ == "__main__":
    main()
