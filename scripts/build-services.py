#!/usr/bin/env python3
"""
Custom Creations Unlimited service-page generator.

Produces six self-contained, SEO-ready HTML pages in ../services from the
structured content below. Keeping copy in one place avoids drift across pages.
Run:  python3 scripts/build-services.py
"""
import os
from string import Template

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "services"))

# --------------------------------------------------------------------------
# Icon library (inline SVG)
# --------------------------------------------------------------------------
SVC_ICON = {
    "embroidery": '<svg viewBox="0 0 24 24" fill="none"><path d="M3 12h4l2-7 4 14 2-7h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "custom-apparel": '<svg viewBox="0 0 24 24" fill="none"><path d="M6 4l3 2h6l3-2 3 4-3 2v10H6V10L3 8z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "promotional-products": '<svg viewBox="0 0 24 24" fill="none"><path d="M4 8h16v12H4zM4 8l2-4h12l2 4M9 12h6" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></svg>',
    "awards": '<svg viewBox="0 0 24 24" fill="none"><path d="M8 4h8v4a4 4 0 01-8 0zM6 6H4v2a3 3 0 003 3M18 6h2v2a3 3 0 01-3 3M9 20h6l-1-4h-4z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></svg>',
    "laser-engraving": '<svg viewBox="0 0 24 24" fill="none"><path d="M3 17l8-8 4 4M14 6l4 4 3-3-4-4zM5 21l3-1 1-3" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></svg>',
    "personalized-gifts": '<svg viewBox="0 0 24 24" fill="none"><path d="M4 9h16v11H4zM3 5h18v4H3zM12 5v15M9 5s-2-3 1-3 2 3 2 3M15 5s2-3-1-3-2 3-2 3" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></svg>',
}

ICON = {
    "shield": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2l8 4v6c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10V6z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" fill="none"><path d="M13 2L4.5 13H11l-1 9 9-12h-6z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "proof": '<svg viewBox="0 0 24 24" fill="none"><path d="M4 7h16M4 12h16M4 17h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2v20M5 7h9a3 3 0 010 6H7a3 3 0 000 6h9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "team": '<svg viewBox="0 0 24 24" fill="none"><path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="8" cy="6" r="2" fill="currentColor"/><circle cx="16" cy="12" r="2" fill="currentColor"/><circle cx="10" cy="18" r="2" fill="currentColor"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "sparkle": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 16.8 5.7 21.4 8 14 2 9.4h7.6z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3l9 5-9 5-9-5zM3 13l9 5 9-5M3 17l9 5 9-5" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none"><path d="M3 6h11v9H3zM14 9h4l3 3v3h-7zM7 18a2 2 0 100-4 2 2 0 000 4zM18 18a2 2 0 100-4 2 2 0 000 4z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
    "infinity": '<svg viewBox="0 0 24 24" fill="none"><path d="M7 12c0-2 1.5-3.5 3-3.5S15 12 17 12s3-1.5 3-3.5S18.5 5 17 5s-3 1.5-5 3.5M17 12c0 2-1.5 3.5-3 3.5S9 12 7 12s-3 1.5-3 3.5S5.5 19 7 19s3-1.5 5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none"><path d="M5 21c0-9 6-15 15-15 0 9-6 15-15 15zM5 21c3-6 7-9 12-10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "palette": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3a9 9 0 100 18c1.5 0 2-1 2-2s-.5-1.5-.5-2.5S14 13 16 13h2a3 3 0 003-3 7 7 0 00-7-7z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="7.5" cy="11" r="1" fill="currentColor"/><circle cx="11" cy="7.5" r="1" fill="currentColor"/><circle cx="15.5" cy="9" r="1" fill="currentColor"/></svg>',
    "gem": '<svg viewBox="0 0 24 24" fill="none"><path d="M6 3h12l3 6-9 12L3 9zM3 9h18M9 3l-3 6 6 12M15 3l3 6-6 12" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 21s-7-4.5-9-9a4 4 0 017-3 4 4 0 017 3c-2 4.5-9 9-9 9z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
}

IND = {
    "schools": ("Schools", "Spirit wear & uniforms", '<svg viewBox="0 0 24 24" fill="none"><path d="M3 21h18M5 21V8l7-4 7 4v13M9 21v-6h6v6" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "churches": ("Churches", "Apparel & events", '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2v8M8 6h8M5 22V10h14v12M9 22v-5h6v5" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "construction": ("Construction", "Hi-vis & workwear", '<svg viewBox="0 0 24 24" fill="none"><path d="M3 21h18M6 21V8l6-4 6 4v13M10 12h4M10 16h4" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "restaurants": ("Restaurants", "Branded apparel", '<svg viewBox="0 0 24 24" fill="none"><path d="M5 11h14l-1 9H6zM9 11V7a3 3 0 016 0v4" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "healthcare": ("Healthcare", "Scrubs & recognition", '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3v18M3 12h18M7 7l10 10M17 7L7 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'),
    "government": ("Government", "Civic & safety", '<svg viewBox="0 0 24 24" fill="none"><path d="M3 21h18M5 21V7h14v14M9 11h2M13 11h2M9 15h2M13 15h2" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "sports": ("Sports Teams", "Uniforms & trophies", '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2l2.4 7.4H22l-6 4.6 2.3 7.4L12 16.8 5.7 21.4 8 14 2 9.4h7.6z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "corporate": ("Corporate", "Brand programs", '<svg viewBox="0 0 24 24" fill="none"><path d="M4 20V8l8-5 8 5v12M9 20v-6h6v6M4 8h16" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "realestate": ("Real Estate", "Signs & gifts", '<svg viewBox="0 0 24 24" fill="none"><path d="M3 9l9-6 9 6v11H3zM9 20v-6h6v6" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "nonprofits": ("Nonprofits", "Events & merch", '<svg viewBox="0 0 24 24" fill="none"><path d="M12 21s-7-4.5-9-9a4 4 0 017-3 4 4 0 017 3c-2 4.5-9 9-9 9z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "manufacturing": ("Manufacturing", "Workwear & PPE", '<svg viewBox="0 0 24 24" fill="none"><path d="M4 21V5l8-3 8 3v16M8 9h2M14 9h2M8 13h2M14 13h2" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
    "weddings": ("Weddings & Events", "Favors & keepsakes", '<svg viewBox="0 0 24 24" fill="none"><path d="M12 21s-7-4.5-9-9a4 4 0 017-3 4 4 0 017 3c-2 4.5-9 9-9 9z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'),
}

# --------------------------------------------------------------------------
# Service content
# --------------------------------------------------------------------------
SERVICES = {
    "embroidery": {
        "label": "Custom Embroidery",
        "nav": "Embroidery",
        "meta_title": "Custom Embroidery | Polos, Caps, Jackets & Uniforms | Custom Creations Unlimited",
        "meta_desc": "Premium custom embroidery in Atlanta — logos stitched on polos, caps, jackets, beanies and bags for company uniforms, schools, churches and teams. Free proofs, no minimums on most items.",
        "keywords": "custom embroidery, embroidered polos, embroidered caps, company uniforms, logo embroidery, embroidered jackets, monogramming, Atlanta embroidery",
        "eyebrow": "Custom Embroidery",
        "h1_html": 'Embroidery that wears your <em class="text-gradient">logo with pride.</em>',
        "hero_sub": "Crisp, durable, dimensional stitching on apparel and accessories — the most premium way to put your brand on uniforms, caps and corporate gear.",
        "hero_visual": "Embroidered polo",
        "stats": [("3.2M", "stitches a day"), ("No min.", "on most items"), ("7–10 days", "standard turnaround")],
        "overview_h": "Stitched to last, finished to impress.",
        "overview_p": [
            "Embroidery is the gold standard for branded apparel — it never cracks, peels or fades like prints can, and the raised thread gives logos a tactile, high-end finish customers notice.",
            "We digitize your logo in-house for clean, accurate stitching at any size, then run it on commercial multi-head machines for consistent quality across orders of one or ten thousand.",
        ],
        "checklist": [
            ("Free logo digitizing", "We convert your artwork into a precise stitch file — yours to keep."),
            ("Threads matched to your brand", "Hundreds of colors, including metallics and PMS matching."),
            ("Left chest, sleeve, cap & full-back", "Any placement, sized perfectly for the garment."),
            ("Names & numbers", "Personalize uniforms and team gear individually."),
            ("Premium garment selection", "Top brands — Nike, Carhartt, Port Authority and more."),
            ("Consistent across reorders", "Your stitch file is saved for one-click repeats."),
        ],
        "overview_media": "Digitizing closeup",
        "benefits": [
            ("shield", "Permanent & durable", "Stitched thread outlasts the garment — no cracking, peeling or fading wash after wash."),
            ("sparkle", "Premium, tactile finish", "Dimensional embroidery signals quality the moment someone touches it."),
            ("palette", "Exact brand colors", "In-house thread matching keeps your logo on-brand every time."),
            ("infinity", "Saved for easy reorders", "We keep your digitized file so repeat runs are fast and identical."),
        ],
        "products": [
            ("Polo Shirts", "Left-chest logos"), ("Caps & Hats", "Front & side"),
            ("Jackets & Vests", "Back & chest"), ("Beanies", "Cuff embroidery"),
            ("Work Shirts", "Names & logos"), ("Tote & Duffel Bags", "Branded"),
            ("Quarter-Zips", "Corporate"), ("Aprons", "Hospitality"),
        ],
        "gallery": ["Corporate polo program", "Embroidered cap drop", "Varsity jackets", "Church staff shirts", "Construction hi-vis", "Monogrammed bags"],
        "industries": ["corporate", "construction", "schools", "churches", "restaurants", "sports"],
        "testi": ("Custom Creations Unlimited outfitted our entire 240-person team in branded polos and jackets. The embroidery is flawless and they hit every deadline.", "Dana Klein", "Operations Director, Apex Construction", "DK"),
        "faqs": [
            ("What artwork do you need for embroidery?", "A vector file (AI, EPS, PDF, SVG) is ideal, but we can work from a clear PNG or JPG. We digitize it into a stitch file for free and send a proof before stitching."),
            ("Is there a setup or digitizing fee?", "Standard logos are digitized at no charge with your first order. Highly complex artwork may carry a small one-time digitizing fee, which we'll always quote up front."),
            ("Can you embroider garments I provide?", "Yes — we offer contract embroidery on customer-supplied goods, subject to a quick suitability check on fabric and construction."),
            ("How small can text be?", "Clean, legible lettering generally needs to be about 1/4\" (6mm) tall or larger. We'll flag anything that won't stitch cleanly and suggest alternatives."),
        ],
        "related": ["custom-apparel", "promotional-products", "awards"],
    },
    "custom-apparel": {
        "label": "Custom Apparel",
        "nav": "Custom Apparel",
        "meta_title": "Custom T-Shirts & Apparel | DTF, Screen Print & HTV | Custom Creations Unlimited",
        "meta_desc": "Custom t-shirts, hoodies and performance wear in Atlanta. DTF printing, screen printing and heat transfer vinyl for teams, schools, events and businesses. Vivid color, soft feel, fast turnaround.",
        "keywords": "custom t-shirts, custom apparel, DTF printing, screen printing, heat transfer vinyl, custom hoodies, team shirts, event merch, school spirit wear",
        "eyebrow": "Custom Apparel",
        "h1_html": 'Custom apparel that <em class="text-gradient">turns heads.</em>',
        "hero_sub": "Vivid, full-color tees, hoodies and performance wear using the right print method for your design, quantity and budget — from a single shirt to a full team run.",
        "hero_visual": "Printed tees stack",
        "stats": [("4 methods", "DTF · screen · HTV · subli"), ("Full color", "photo-quality DTF"), ("Soft hand", "no heavy feel")],
        "overview_h": "The right print method, every time.",
        "overview_p": [
            "Not every job suits the same process. We match your design to DTF, screen printing, heat transfer vinyl or sublimation so you get the best color, durability and price for your order.",
            "From soft-feel retail tees to moisture-wicking team jerseys, we print on premium blanks and proof every design so what you approve is exactly what you get.",
        ],
        "checklist": [
            ("DTF printing", "Photo-quality, full-color graphics with a soft feel — great for small runs."),
            ("Screen printing", "Bold, long-lasting prints at the best per-piece price for larger orders."),
            ("Heat transfer vinyl", "Crisp names, numbers and single-color graphics for team wear."),
            ("Sublimation", "All-over, edge-to-edge color on performance polyester."),
            ("Premium blanks", "Bella+Canvas, Next Level, Gildan, Sport-Tek and more."),
            ("Mockups before print", "Approve a digital proof — no surprises."),
        ],
        "overview_media": "DTF press in action",
        "benefits": [
            ("layers", "Method matched to your job", "We pick DTF, screen, HTV or sublimation for the best result and price."),
            ("palette", "True, vibrant color", "Photo-grade detail and accurate brand colors on light or dark garments."),
            ("bolt", "Fast on rush orders", "Tight event deadline? Ask about rush — we deliver on time."),
            ("tag", "Volume pricing", "Per-piece cost drops fast as quantities climb — ideal for teams."),
        ],
        "products": [
            ("T-Shirts", "Cotton & blends"), ("Hoodies", "Pullover & zip"),
            ("Long Sleeve Tees", "Retail & team"), ("Performance Tees", "Moisture-wicking"),
            ("Sweatshirts", "Crewneck"), ("Tank Tops", "Summer & events"),
            ("Safety / Hi-Vis", "ANSI options"), ("Youth Sizes", "School-ready"),
        ],
        "gallery": ["School spirit wear run", "Conference merch line", "Event hoodies", "5K race tees", "Restaurant staff tees", "Team jerseys"],
        "industries": ["schools", "sports", "restaurants", "nonprofits", "corporate", "construction"],
        "testi": ("Eight days from quote to 300 event hoodies, printed perfectly. The color was exactly what we approved and the shirts feel premium.", "Sofia Park", "Marketing Manager, Summit Realty", "SP"),
        "faqs": [
            ("What's the difference between DTF and screen printing?", "DTF prints full-color, photo-quality detail with no setup, so it shines on small runs and complex art. Screen printing lays down thick, durable ink and gets cheaper per piece as quantities grow — best for big single- or few-color orders."),
            ("Do you have a minimum order?", "DTF and HTV have no minimum. Screen printing is most cost-effective at 12+ pieces. We'll always recommend the method that fits your quantity and budget."),
            ("Can I mix shirt sizes and colors in one order?", "Absolutely. Mix sizes, styles and garment colors — we'll confirm any impact on pricing in your quote."),
            ("Will the print crack or fade?", "When the right method and cure are used, prints stay vivid for the life of the shirt. We test and cure every job to spec."),
        ],
        "related": ["embroidery", "promotional-products", "personalized-gifts"],
    },
    "promotional-products": {
        "label": "Promotional Products",
        "nav": "Promotional Products",
        "meta_title": "Promotional Products | Branded Drinkware, Bags & Swag | Custom Creations Unlimited",
        "meta_desc": "Branded promotional products in Atlanta — tumblers, pens, bags, power banks and trade-show giveaways. Thousands of items, in-house decoration, and curated swag kits that get used.",
        "keywords": "promotional products, branded swag, custom tumblers, trade show giveaways, branded pens, custom bags, corporate gifts, employee gifts, power banks",
        "eyebrow": "Promotional Products",
        "h1_html": 'Swag people <em class="text-gradient">actually keep.</em>',
        "hero_sub": "Thousands of branded products — drinkware, bags, tech and trade-show giveaways — curated and decorated in-house so your logo stays in your customers' hands.",
        "hero_visual": "Branded swag kit",
        "stats": [("5,000+", "products to brand"), ("Kitting", "& fulfillment"), ("In-house", "decoration")],
        "overview_h": "Promo that earns its place on the desk.",
        "overview_p": [
            "Anyone can hand out cheap giveaways. We help you choose useful, well-made products people keep — the kind that quietly market your brand for years.",
            "From a single trade-show order to recurring company swag, we source, decorate, kit and ship — so you get one easy point of contact for everything branded.",
        ],
        "checklist": [
            ("Curated, quality products", "We steer you toward items that get used, not tossed."),
            ("In-house decoration", "Engraving, printing and embroidery under one roof for tight quality control."),
            ("Welcome & event kits", "Assembled, boxed and ready to hand out or mail."),
            ("Drop-ship & fulfillment", "Ship to one address or many — we handle logistics."),
            ("Brand-consistent", "Your colors and logo applied correctly, every time."),
            ("Budget-friendly tiers", "Options at every price point with transparent pricing."),
        ],
        "overview_media": "Tumblers being decorated",
        "benefits": [
            ("layers", "Massive product range", "Thousands of items across drinkware, bags, tech, apparel and more."),
            ("gem", "Quality that reflects you", "We avoid throwaway junk — only products worth your logo."),
            ("truck", "Kitting & fulfillment", "We assemble, box and ship kits to your team or event."),
            ("team", "One easy contact", "Sourcing, decoration and delivery, all handled by us."),
        ],
        "products": [
            ("Tumblers & Mugs", "Laser & print"), ("Pens", "Bulk-friendly"),
            ("Backpacks & Bags", "Branded"), ("Power Banks", "Tech swag"),
            ("Notebooks", "Corporate"), ("Coolers", "Events"),
            ("Keychains", "Giveaways"), ("Flashlights", "Promo"),
        ],
        "gallery": ["New-hire welcome kits", "Trade-show giveaways", "Branded tumbler sets", "Conference tote kits", "Tech swag bundle", "Golf-outing gifts"],
        "industries": ["corporate", "realestate", "nonprofits", "healthcare", "schools", "government"],
        "testi": ("Our new-hire kits look like they came from a Fortune 500. Custom Creations Unlimited sourced everything, branded it and shipped it assembled — we just hand them out.", "Marcus Reyes", "People Ops, Riverside District", "MR"),
        "faqs": [
            ("Can you build custom welcome or event kits?", "Yes — kitting is one of our specialties. We curate the items, brand them, assemble the kits and ship them to one location or many."),
            ("How do I pick the right products?", "Tell us your audience, goal and budget and we'll send curated recommendations with mockups — no need to dig through a giant catalog."),
            ("What are typical minimums?", "Minimums vary by item, from as few as 12 up to 100+ for some products. We'll show options at your quantity."),
            ("How fast can promo orders ship?", "Many items ship within 7–10 business days; rush production is available on a wide range of products for tight event dates."),
        ],
        "related": ["custom-apparel", "laser-engraving", "personalized-gifts"],
    },
    "awards": {
        "label": "Awards & Recognition",
        "nav": "Awards & Recognition",
        "meta_title": "Corporate Awards, Trophies & Plaques | Crystal & Glass | Custom Creations Unlimited",
        "meta_desc": "Premium corporate awards in Atlanta — crystal and glass awards, engraved plaques, acrylic awards and trophies for employee recognition, sales achievement, retirement and sports.",
        "keywords": "corporate awards, crystal awards, glass awards, engraved plaques, trophies, employee recognition awards, sales awards, acrylic awards, retirement awards",
        "eyebrow": "Awards & Recognition",
        "h1_html": 'Recognition that feels <em class="text-gradient">truly earned.</em>',
        "hero_sub": "Crystal and glass awards, engraved plaques and trophies with a weight and finish that make every honoree feel the moment — designed and engraved in-house.",
        "hero_visual": "Crystal award",
        "stats": [("Crystal & glass", "premium materials"), ("Free design", "layout proofs"), ("Bulk programs", "named & dated")],
        "overview_h": "Make the moment as premium as the achievement.",
        "overview_p": [
            "A great award does more than mark a milestone — it makes someone feel valued. We craft pieces with real heft, clean engraving and elegant presentation that look the part on any shelf.",
            "Running an annual recognition program? We handle layout, individual names and dates, and consistent quality across the whole set, year after year.",
        ],
        "checklist": [
            ("Crystal, glass & acrylic", "From sleek modern blocks to classic statements."),
            ("Laser & rotary engraving", "Crisp text and logos, deep and permanent."),
            ("Custom shapes & 3D", "Sub-surface 3D engraving and bespoke silhouettes."),
            ("Individual names & dates", "Personalized across an entire program."),
            ("Gift boxing", "Presentation boxes for a premium reveal."),
            ("Free layout proof", "Approve the design before we engrave."),
        ],
        "overview_media": "Engraving a plaque",
        "benefits": [
            ("gem", "Premium materials", "Genuine crystal and glass with the weight recipients remember."),
            ("target", "Precision engraving", "Sharp, permanent text and logos — even fine detail."),
            ("proof", "Free design proofs", "See the exact layout before anything is engraved."),
            ("infinity", "Consistent programs", "Same look and quality across years of recognition."),
        ],
        "products": [
            ("Crystal Awards", "Premium"), ("Glass Awards", "Modern"),
            ("Engraved Plaques", "Classic"), ("Acrylic Awards", "Budget-friendly"),
            ("Sports Trophies", "Teams & leagues"), ("Retirement Gifts", "Milestone"),
            ("Sales Awards", "Recognition"), ("Name Badges", "Staff"),
        ],
        "gallery": ["Annual sales recognition", "Employee of the year", "Retirement keepsake", "Crystal gala awards", "League trophy set", "Donor recognition wall"],
        "industries": ["corporate", "healthcare", "nonprofits", "government", "sports", "schools"],
        "testi": ("The crystal awards they engraved for our gala were stunning. Guests kept asking where we had them made — truly premium quality.", "Marcus Reyes", "Events Lead, Riverside District", "MR"),
        "faqs": [
            ("Can you engrave our logo into crystal awards?", "Yes. We laser-engrave logos and text, and offer sub-surface 3D engraving inside crystal for a striking effect. You'll approve a layout proof first."),
            ("Do you handle large recognition programs?", "Definitely — annual awards with dozens of individual names and dates are routine for us, with consistent quality across the full set."),
            ("Can I see a proof before engraving?", "Always. Every award includes a free digital layout proof so you can confirm spelling, fonts and placement before production."),
            ("Do awards come with gift boxes?", "Most crystal and glass awards include a presentation box; we can add custom or branded boxing on request."),
        ],
        "related": ["laser-engraving", "personalized-gifts", "promotional-products"],
    },
    "laser-engraving": {
        "label": "Laser Engraving",
        "nav": "Laser Engraving",
        "meta_title": "Laser Engraving | Wood, Glass, Metal, Leather & Acrylic | Custom Creations Unlimited",
        "meta_desc": "Precision laser engraving in Atlanta on wood, glass, metal, leather, slate and acrylic — tumblers, knives, cutting boards, signs and gifts. Permanent, photo-grade detail.",
        "keywords": "laser engraving, custom engraving, engraved tumblers, engraved knives, wood engraving, glass engraving, metal engraving, engraved signs, slate engraving",
        "eyebrow": "Laser Engraving",
        "h1_html": 'Permanent detail, <em class="text-gradient">etched to perfection.</em>',
        "hero_sub": "Photo-grade engraving on wood, glass, metal, leather, slate and acrylic — for gifts, signage, drinkware and products that are meant to last a lifetime.",
        "hero_visual": "Engraved cutting board",
        "stats": [("6+ materials", "wood · glass · metal…"), ("Photo-grade", "fine detail"), ("Permanent", "never fades")],
        "overview_h": "If it can be marked, we can make it yours.",
        "overview_p": [
            "Laser engraving removes or transforms the surface itself, so the mark is permanent — no ink to fade, no label to peel. The result is clean, precise and beautifully tactile.",
            "We engrave everything from a single sentimental gift to production runs of branded drinkware and signage, dialing in settings per material for crisp, consistent results.",
        ],
        "checklist": [
            ("Wood & bamboo", "Cutting boards, signs, plaques and keepsakes."),
            ("Glass & crystal", "Tumblers, barware, vases and awards."),
            ("Metal & stainless", "Tumblers, tools, knives and tags."),
            ("Leather", "Journals, patches, wallets and bags."),
            ("Slate & stone", "Coasters, signs and serving boards."),
            ("Acrylic", "Signage, displays and ornaments."),
        ],
        "overview_media": "Laser at work",
        "benefits": [
            ("target", "Photo-grade precision", "Fine lines, logos and even photographs reproduced cleanly."),
            ("shield", "Permanent & elegant", "Engraving is part of the material — it never fades or peels."),
            ("layers", "Almost any material", "Wood, glass, metal, leather, slate and acrylic, dialed in per surface."),
            ("heart", "One-off to production", "A single heirloom gift or thousands of branded pieces."),
        ],
        "products": [
            ("Tumblers", "Metal & glass"), ("Cutting Boards", "Wood & bamboo"),
            ("Knives & Tools", "Gifts"), ("Signs", "Wood & acrylic"),
            ("Slate Coasters", "Sets"), ("Leather Journals", "Personalized"),
            ("Glassware", "Barware"), ("Pet Tags", "Metal"),
        ],
        "gallery": ["Engraved cutting boards", "Memorial slate sign", "Custom tumbler set", "Engraved pocket knives", "Wooden welcome sign", "Leather journals"],
        "industries": ["weddings", "corporate", "restaurants", "realestate", "nonprofits", "healthcare"],
        "testi": ("The engraved cutting boards we ordered as client gifts were gorgeous. Every line was crisp and the wood finish felt expensive.", "Dana Klein", "Client Relations, Apex Group", "DK"),
        "faqs": [
            ("What materials can you engrave?", "Wood, bamboo, glass, crystal, stainless and coated metals, leather, slate, stone and acrylic. If you're unsure about a specific item, send it over and we'll test."),
            ("Can you engrave a photo?", "On the right materials — wood, slate, leather and coated metal — yes. We convert photos for engraving and proof them so you know how the detail will translate."),
            ("Can I supply my own items to engrave?", "Often, yes. We'll do a quick suitability check on the material and coating, then quote engraving on your goods."),
            ("Is engraving permanent?", "Completely. The mark is in the material itself, so it won't wash off, peel or fade with use."),
        ],
        "related": ["awards", "personalized-gifts", "promotional-products"],
    },
    "personalized-gifts": {
        "label": "Personalized Gifts",
        "nav": "Personalized Gifts",
        "meta_title": "Personalized Gifts | Weddings, Holidays & Milestones | Custom Creations Unlimited",
        "meta_desc": "Personalized gifts in Atlanta for weddings, birthdays, anniversaries, graduations, holidays and corporate milestones — engraved, embroidered and printed keepsakes they'll treasure.",
        "keywords": "personalized gifts, custom gifts, wedding gifts, engraved gifts, corporate gifts, graduation gifts, anniversary gifts, memorial gifts, custom keepsakes",
        "eyebrow": "Personalized Gifts",
        "h1_html": 'Gifts they\'ll <em class="text-gradient">treasure for years.</em>',
        "hero_sub": "Thoughtful, personalized keepsakes for weddings, milestones, holidays and corporate moments — engraved, embroidered and printed to feel one-of-a-kind.",
        "hero_visual": "Personalized keepsake",
        "stats": [("One-of-a-kind", "personalized"), ("Gift-ready", "boxing available"), ("Any occasion", "big or small")],
        "overview_h": "The gift that says you put thought into it.",
        "overview_p": [
            "A name, a date, a few meaningful words — personalization turns an ordinary item into something kept on a shelf for decades. We help you get it exactly right.",
            "Whether it's one heartfelt keepsake or a hundred client gifts, we combine engraving, embroidery and printing to make each piece feel intentional and premium.",
        ],
        "checklist": [
            ("Weddings & anniversaries", "Favors, party gifts and couple keepsakes."),
            ("Graduations & birthdays", "Milestone gifts that mark the moment."),
            ("Holiday gifting", "Personalized seasonal gifts in bulk or one-off."),
            ("Corporate & client gifts", "Branded thank-yous that impress."),
            ("Memorial keepsakes", "Handled with care and craftsmanship."),
            ("Gift boxing", "Presentation-ready packaging on request."),
        ],
        "overview_media": "Wrapping a gift",
        "benefits": [
            ("heart", "Genuinely meaningful", "Names, dates and messages make each gift personal."),
            ("gem", "Premium keepsakes", "Quality materials and finishes worth keeping."),
            ("palette", "Many techniques", "Engraving, embroidery and printing for any item."),
            ("sparkle", "Gift-ready", "Optional boxing and presentation for the perfect reveal."),
        ],
        "products": [
            ("Engraved Tumblers", "Couples & grads"), ("Cutting Boards", "Wedding gifts"),
            ("Photo Frames", "Keepsakes"), ("Ornaments", "Holiday"),
            ("Leather Journals", "Personalized"), ("Glassware Sets", "Anniversary"),
            ("Custom Apparel", "Family & events"), ("Memorial Pieces", "Tribute"),
        ],
        "gallery": ["Wedding party gifts", "Engraved anniversary set", "Graduation keepsakes", "Holiday client gifts", "Personalized ornaments", "Memorial tribute piece"],
        "industries": ["weddings", "corporate", "nonprofits", "healthcare", "churches", "realestate"],
        "testi": ("I ordered personalized gifts for my whole wedding party and they were perfect — beautifully engraved and boxed. Everyone was blown away.", "Sofia Park", "Bride & repeat client", "SP"),
        "faqs": [
            ("Can I order just one personalized gift?", "Yes — we love single, meaningful pieces as much as big batches. There's no minimum on most personalized items."),
            ("How far in advance should I order for a wedding?", "We recommend 2–3 weeks for personalized wedding gifts and favors, but ask about rush options if your date is close."),
            ("Can you gift-box the items?", "Many items include or offer presentation boxing — just ask and we'll make it gift-ready."),
            ("Can you combine different techniques?", "Absolutely. We mix engraving, embroidery and printing across a gift set so everything feels cohesive."),
        ],
        "related": ["laser-engraving", "awards", "custom-apparel"],
    },
}

ORDER = ["embroidery", "custom-apparel", "promotional-products", "awards", "laser-engraving", "personalized-gifts"]

# --------------------------------------------------------------------------
# Section builders
# --------------------------------------------------------------------------
def mega_links():
    out = []
    for s in ORDER:
        d = SERVICES[s]
        out.append(f'''<a class="mega-link" href="{s}.html" role="menuitem">
          <span class="mega-link__icon">{SVC_ICON[s]}</span>
          <span><span class="mega-link__title">{d["nav"]}</span><span class="mega-link__desc">{d["meta_desc"][:38].rsplit(" ",1)[0]}…</span></span>
        </a>''')
    return "\n".join(out)

ARROW = '<svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
STAR = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>'

def build(slug):
    d = SERVICES[slug]
    stats = "".join(f'<div class="svc-stat"><strong>{a}</strong><span>{b}</span></div>' for a, b in d["stats"])
    overview_p = "".join(f"<p>{p}</p>" for p in d["overview_p"])
    checklist = "".join(f'<li>{CHECK}<span><strong>{t}</strong> — {x}</span></li>' for t, x in d["checklist"])
    benefits = "".join(
        f'''<div class="card feature" data-reveal data-delay="{i%4}"><div class="feature__icon">{ICON[ic]}</div><h3>{t}</h3><p>{x}</p></div>'''
        for i, (ic, t, x) in enumerate(d["benefits"]))
    products = "".join(
        f'''<article class="prod" data-reveal data-delay="{i%4}"><div class="prod__media"><div class="ph" data-label="{n}"></div></div><div class="prod__body"><div class="prod__name">{n}</div><div class="prod__meta">{m}</div></div></article>'''
        for i, (n, m) in enumerate(d["products"]))
    spans = ["span-6 tall", "span-6", "span-4", "span-4", "span-4", "span-6"]
    gallery = "".join(
        f'''<figure class="gallery-item {spans[i%len(spans)]}" data-reveal><div class="ph" data-label="{g}"></div><figcaption class="gallery-item__overlay"><span class="gallery-item__cat">{d["label"]}</span><span class="gallery-item__title">{g}</span></figcaption></figure>'''
        for i, g in enumerate(d["gallery"]))
    industries = "".join(
        f'''<a class="industry-chip" href="../industries.html"><span class="industry-chip__icon">{IND[k][2]}</span><span>{IND[k][0]}<small>{IND[k][1]}</small></span></a>'''
        for k in d["industries"])
    faqs = "".join(
        f'''<div class="faq-item"><button class="faq-q" aria-expanded="false"><span>{q}</span><span class="faq-icon"><svg viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span></button><div class="faq-a"><div class="faq-a__inner">{a}</div></div></div>'''
        for q, a in d["faqs"])
    related = "".join(
        f'''<a class="related-card" href="{r}.html"><span class="related-card__icon">{SVC_ICON[r]}</span><h3>{SERVICES[r]["nav"]}</h3><p>{SERVICES[r]["hero_sub"][:90].rsplit(" ",1)[0]}…</p><span class="link-arrow">Explore {ARROW}</span></a>'''
        for r in d["related"])
    tq, tn, tr, ti = d["testi"]

    return TEMPLATE.safe_substitute(
        slug=slug, meta_title=d["meta_title"], meta_desc=d["meta_desc"], keywords=d["keywords"],
        label=d["label"], eyebrow=d["eyebrow"], h1_html=d["h1_html"], hero_sub=d["hero_sub"],
        hero_icon=SVC_ICON[slug], hero_visual=d["hero_visual"], stats=stats,
        overview_h=d["overview_h"], overview_p=overview_p, checklist=checklist, overview_media=d["overview_media"],
        benefits=benefits, products=products, gallery=gallery, industries=industries,
        testi_quote=tq, testi_name=tn, testi_role=tr, testi_initials=ti,
        faqs=faqs, related=related, mega=mega_links(),
    )

# --------------------------------------------------------------------------
# Page template
# --------------------------------------------------------------------------
TEMPLATE = Template(r"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#0a0a0f" />
  <title>$meta_title</title>
  <meta name="description" content="$meta_desc" />
  <meta name="keywords" content="$keywords" />
  <link rel="canonical" href="https://www.ccucustom.com/services/$slug.html" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Custom Creations Unlimited" />
  <meta property="og:title" content="$meta_title" />
  <meta property="og:description" content="$meta_desc" />
  <meta property="og:url" content="https://www.ccucustom.com/services/$slug.html" />
  <meta property="og:image" content="https://www.ccucustom.com/assets/img/og-cover.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../assets/css/styles.css?v=2" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230a0a0f'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-family='Georgia,serif' font-size='11' font-weight='700' fill='%23c8a24a'%3ECCU%3C/text%3E%3C/svg%3E" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": "$label",
    "name": "$label",
    "description": "$meta_desc",
    "areaServed": { "@type": "City", "name": "Atlanta" },
    "provider": {
      "@type": "LocalBusiness",
      "name": "Custom Creations Unlimited",
      "telephone": "+1-404-967-8028",
      "address": { "@type": "PostalAddress", "addressLocality": "Atlanta", "addressRegion": "GA", "postalCode": "30318", "addressCountry": "US" }
    }
  }
  </script>
  <script type="application/ld+json">
  { "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://www.ccucustom.com/"},
    {"@type":"ListItem","position":2,"name":"Services","item":"https://www.ccucustom.com/#services"},
    {"@type":"ListItem","position":3,"name":"$label","item":"https://www.ccucustom.com/services/$slug.html"}
  ]}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header" id="header">
    <div class="container header-inner">
      <a class="brand" href="../index.html" aria-label="Custom Creations Unlimited home">
        <svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true">
          <rect width="40" height="40" rx="9" fill="currentColor" style="color:var(--ink-900)"/>
          <text x="20" y="26" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="13" font-weight="700" fill="var(--gold-400)" style="letter-spacing:.5px">CCU</text>
        </svg>
        <span class="brand__name">Custom Creations</span>
      </a>
      <nav class="primary-nav" aria-label="Primary">
        <ul class="nav-list">
          <li class="nav-item"><a class="nav-link" href="../index.html">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="../about.html">About</a></li>
          <li class="nav-item nav-item--has-mega">
            <a class="nav-link" href="../index.html#services" aria-haspopup="true">Services
              <svg class="chev" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <div class="mega" role="menu">
              <div class="mega-grid">
                $mega
              </div>
              <div class="mega-foot">
                <span>Not sure where to start? Our team will guide you.</span>
                <a class="link-arrow" href="../quote.html">Request a quote <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
              </div>
            </div>
          </li>
          <li class="nav-item"><a class="nav-link" href="../shop.html">Shop</a></li>
          <li class="nav-item"><a class="nav-link" href="../gallery.html">Gallery</a></li>
          <li class="nav-item"><a class="nav-link" href="../industries.html">Industries</a></li>
          <li class="nav-item"><a class="nav-link" href="../blog/index.html">Blog</a></li>
          <li class="nav-item"><a class="nav-link" href="../faq.html">FAQ</a></li>
          <li class="nav-item"><a class="nav-link" href="../contact.html">Contact</a></li>
        </ul>
      </nav>
      <div class="header-actions">
        <button class="icon-btn theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
          <svg class="sun" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          <svg class="moon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
        </button>
        <a class="btn btn--gold" href="../quote.html">Request a Quote</a>
        <button class="icon-btn nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        </button>
      </div>
    </div>
  </header>

  <div class="mobile-nav" id="mobileNav" aria-hidden="true">
    <ul class="mobile-nav__list">
      <li><a class="mobile-nav__link" href="../index.html">Home</a></li>
      <li><a class="mobile-nav__link" href="../about.html">About</a></li>
      <li>
        <button class="mobile-nav__link" data-sub="m-services" aria-expanded="false">Services
          <svg viewBox="0 0 24 24" fill="none" width="20"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div class="mobile-nav__sub" id="m-services">
          <a href="embroidery.html">Embroidery</a><a href="custom-apparel.html">Custom Apparel</a><a href="promotional-products.html">Promotional Products</a>
          <a href="awards.html">Awards &amp; Recognition</a><a href="laser-engraving.html">Laser Engraving</a><a href="personalized-gifts.html">Personalized Gifts</a>
        </div>
      </li>
      <li><a class="mobile-nav__link" href="../shop.html">Shop</a></li>
      <li><a class="mobile-nav__link" href="../gallery.html">Gallery</a></li>
      <li><a class="mobile-nav__link" href="../industries.html">Industries</a></li>
      <li><a class="mobile-nav__link" href="../blog/index.html">Blog</a></li>
      <li><a class="mobile-nav__link" href="../faq.html">FAQ</a></li>
      <li><a class="mobile-nav__link" href="../contact.html">Contact</a></li>
    </ul>
    <div class="mobile-nav__cta">
      <a class="btn btn--gold btn--lg btn--block" href="../quote.html">Request a Quote</a>
      <a class="btn btn--ghost btn--lg btn--block" href="tel:+14049678028">Call (404) 967-8028</a>
    </div>
  </div>

  <main id="main">
    <!-- HERO -->
    <section class="svc-hero" aria-labelledby="svc-h">
      <div class="svc-hero__bg" aria-hidden="true"></div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb" data-reveal>
          <a href="../index.html">Home</a>
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <a href="../index.html#services">Services</a>
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span aria-current="page">$label</span>
        </nav>
        <div class="svc-hero__inner">
          <div>
            <span class="eyebrow" data-reveal>$eyebrow</span>
            <h1 id="svc-h" data-reveal data-delay="1">$h1_html</h1>
            <p class="svc-hero__sub" data-reveal data-delay="2">$hero_sub</p>
            <div class="svc-hero__cta" data-reveal data-delay="3">
              <a class="btn btn--gold btn--lg" href="../quote.html">Request a Quote
                <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
              <a class="btn btn--ghost btn--lg" href="#work">View Examples</a>
            </div>
            <div class="svc-hero__stats" data-reveal data-delay="4">$stats</div>
          </div>
          <div class="svc-hero__visual" data-reveal data-delay="2" aria-hidden="true">
            <div class="media-frame"><div class="ph" data-label="$hero_visual"></div></div>
            <div class="hero-badge float">
              <span class="hero-badge__icon">$hero_icon</span>
              <div><strong>In-house</strong><span>craftsmanship</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- OVERVIEW -->
    <section class="section" aria-labelledby="ov-h">
      <div class="container split">
        <div data-reveal>
          <span class="eyebrow">Overview</span>
          <h2 id="ov-h" style="margin:1rem 0 1.2rem">$overview_h</h2>
          $overview_p
          <ul class="check-list">$checklist</ul>
        </div>
        <div class="media-frame split__media" data-reveal data-delay="1" aria-hidden="true"><div class="ph" data-label="$overview_media"></div></div>
      </div>
    </section>

    <!-- BENEFITS -->
    <section class="section section--tight" aria-labelledby="ben-h" style="background:var(--bg-soft)">
      <div class="container">
        <div class="section-head section-head--center" data-reveal>
          <span class="eyebrow eyebrow--center">Why Custom Creations Unlimited</span>
          <h2 id="ben-h">Benefits that show in the finished product.</h2>
        </div>
        <div class="grid grid--4">$benefits</div>
      </div>
    </section>

    <!-- POPULAR PRODUCTS -->
    <section class="section" aria-labelledby="prod-h">
      <div class="container">
        <div class="section-head" data-reveal>
          <span class="eyebrow">Popular products</span>
          <h2 id="prod-h">What we make most.</h2>
          <p class="lead">A starting point — if you don't see it here, just ask. We can brand almost anything.</p>
        </div>
        <div class="prod-grid">$products</div>
      </div>
    </section>

    <!-- GALLERY -->
    <section class="section section--tight" id="work" aria-labelledby="gal-h">
      <div class="container">
        <div class="section-head" data-reveal>
          <span class="eyebrow">Recent work</span>
          <h2 id="gal-h">A look at what's possible.</h2>
        </div>
        <div class="gallery-grid">$gallery</div>
      </div>
    </section>

    <!-- INDUSTRIES -->
    <section class="section section--tight" aria-labelledby="ind-h" style="background:var(--bg-soft)">
      <div class="container">
        <div class="section-head section-head--center" data-reveal>
          <span class="eyebrow eyebrow--center">Who it's for</span>
          <h2 id="ind-h">Industries we serve.</h2>
        </div>
        <div class="industry-grid">$industries</div>
      </div>
    </section>

    <!-- TESTIMONIAL -->
    <section class="section section--tight" aria-label="Client testimonial">
      <div class="container" style="max-width:780px">
        <article class="card testi-card" data-reveal style="text-align:center;align-items:center">
          <span class="stars" aria-label="5 out of 5 stars">$star$star$star$star$star</span>
          <p class="testi-card__quote" style="font-size:1.4rem;margin-top:1rem">“$testi_quote”</p>
          <div class="testi-card__author" style="border:0;justify-content:center;margin-top:1.4rem;padding-top:0">
            <span class="testi-card__avatar">$testi_initials</span>
            <div style="text-align:left"><div class="testi-card__name">$testi_name</div><div class="testi-card__role">$testi_role</div></div>
          </div>
        </article>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section" aria-labelledby="faq-h" style="background:var(--bg-soft)">
      <div class="container">
        <div class="section-head section-head--center" data-reveal>
          <span class="eyebrow eyebrow--center">Good to know</span>
          <h2 id="faq-h">$label questions, answered.</h2>
        </div>
        <div class="faq-list" data-reveal>$faqs</div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section" id="quote">
      <div class="container">
        <div class="cta-banner" data-reveal>
          <div class="cta-banner__inner">
            <span class="eyebrow eyebrow--center" style="color:var(--gold-300)">Request a quote</span>
            <h2>Ready to make your mark?</h2>
            <p>Tell us about your project and we'll send a free design proof and exact quote — usually within one business day.</p>
            <div class="hero__cta">
              <a class="btn btn--gold btn--lg" href="../quote.html">Start my quote
                <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
              <a class="btn btn--light btn--lg" href="tel:+14049678028">Call (404) 967-8028</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- RELATED -->
    <section class="section section--tight" aria-labelledby="rel-h">
      <div class="container">
        <div class="section-head" data-reveal>
          <span class="eyebrow">Keep exploring</span>
          <h2 id="rel-h">Related services.</h2>
        </div>
        <div class="related-grid">$related</div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <a class="brand" href="../index.html" aria-label="Custom Creations Unlimited home">
            <svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true">
              <rect width="40" height="40" rx="9" fill="#16161f"/>
              <text x="20" y="26" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="13" font-weight="700" fill="var(--gold-400)" style="letter-spacing:.5px">CCU</text>
            </svg>
            <span class="brand__name">Custom Creations</span>
          </a>
          <p>A premium custom branding house — embroidery, apparel, promotional products, awards, laser engraving and personalized gifts, all under one roof.</p>
          <div class="footer-social">
            <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 9h3V6h-3c-2 0-3 1.3-3 3.2V11H8v3h3v7h3v-7h2.5l.5-3H14V9.5c0-.3.2-.5.6-.5z"/></svg></a>
            <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><circle cx="17" cy="7" r="1.2" fill="currentColor"/></svg></a>
            <a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.5 8A1.5 1.5 0 106.5 5 1.5 1.5 0 006.5 8zM5 10h3v9H5zM10 10h3v1.3c.5-.8 1.5-1.5 3-1.5 2.2 0 3 1.4 3 3.8V19h-3v-4.6c0-1.1-.4-1.8-1.4-1.8s-1.6.7-1.6 1.8V19h-3z"/></svg></a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Services</h4>
          <a href="embroidery.html">Embroidery</a><a href="custom-apparel.html">Custom Apparel</a><a href="promotional-products.html">Promotional Products</a>
          <a href="awards.html">Awards &amp; Recognition</a><a href="laser-engraving.html">Laser Engraving</a><a href="personalized-gifts.html">Personalized Gifts</a>
        </div>
        <div class="footer-col">
          <h4>Company</h4>
          <a href="../about.html">About Us</a><a href="../shop.html">Shop</a><a href="../gallery.html">Gallery</a><a href="../industries.html">Industries</a>
          <a href="../index.html#reviews">Reviews</a><a href="../index.html#faq">FAQ</a><a href="../contact.html">Contact</a>
        </div>
        <div class="footer-col">
          <h4>Get in touch</h4>
          <a href="tel:+14049678028">(404) 967-8028</a>
          <a href="mailto:info@ccucustom.com">info@ccucustom.com</a>
          <a href="../contact.html">1180 Industrial Park Blvd<br>Atlanta, GA 30318</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span id="year"></span> Custom Creations Unlimited All rights reserved. · Atlanta, GA</span>
        <nav aria-label="Legal"><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Accessibility</a></nav>
      </div>
    </div>
  </footer>

  <div class="floating">
    <a class="fab fab--call" href="tel:+14049678028" aria-label="Call us">
      <svg viewBox="0 0 24 24" fill="none"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.7A2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 2 .7 2.9a2 2 0 01-.4 2.1L8.1 9.9a16 16 0 006 6l1.2-1.3a2 2 0 012.1-.4c.9.3 1.9.6 2.9.7a2 2 0 011.7 2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
    </a>
    <a class="fab fab--quote" href="../quote.html" aria-label="Request a quote">
      <svg viewBox="0 0 24 24" fill="none"><path d="M4 5h16v11H8l-4 4z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8 9h8M8 12h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </a>
  </div>
  <button class="back-to-top" id="backToTop" aria-label="Back to top">
    <svg viewBox="0 0 24 24" fill="none"><path d="M12 19V5M5 12l7-7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>

  <script src="../assets/js/main.js?v=2" defer></script>
</body>
</html>
""")

# inject star glyph into template substitution (kept separate for readability)
def main():
    os.makedirs(OUT, exist_ok=True)
    for slug in ORDER:
        html = build(slug).replace("$star", STAR)
        path = os.path.join(OUT, f"{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", os.path.relpath(path, os.path.join(HERE, "..")))

if __name__ == "__main__":
    main()
