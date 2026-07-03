#!/usr/bin/env python3
"""
Replace every `.ph` placeholder block with a real <img> from assets/img,
choosing the image by matching the placeholder's data-label to a category.

Run LAST, after the page generators (build-services / build-pages / build-blog),
because those emit fresh `.ph` placeholders. `build-all.sh` does this in order.
Idempotent: if a file has no `.ph` blocks, it's left unchanged.
"""
import os, re, html as htmllib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
IMGDIR = os.path.join(ROOT, "assets", "img")

# Build category -> [filenames] by scanning the image folder.
CATS = {}
for fn in sorted(os.listdir(IMGDIR)):
    m = re.match(r"([a-z]+)-\d+\.webp$", fn)
    if m:
        CATS.setdefault(m.group(1), []).append("assets/img/" + fn)

# Keyword rules (first match wins) — specific categories before general ones.
RULES = [
    ("awards",    ["award","trophy","plaque","crystal","recognition","gala","retirement","sales award","donor","employee of"]),
    ("laser",     ["laser","engrav","cutting board","slate","knife","wood","leather journal"]),
    ("drinkware", ["tumbler","mug","drinkware","glassware","barware","bottle"]),
    ("embroidery",["embroid","polo","cap","beanie","monogram","stitch","digitiz","quarter-zip","work shirt","apron","uniform","staff shirt"]),
    ("apparel",   ["apparel","tee","t-shirt","shirt","hoodie","sweatshirt","jersey","dtf","screen","spirit wear","merch","tank","long sleeve","performance","safety","hi-vis","youth"]),
    ("promo",     ["promo","swag","giveaway","welcome kit","tote","backpack"," pen","power bank","notebook","cooler","keychain","flashlight","trade-show","trade show","golf","new-hire","kit","bag"]),
    ("gifts",     ["gift","wedding","anniversary","graduation","holiday","keepsake","ornament","memorial","frame","favor","baby"]),
    ("branding",  ["branding","brand rollout","signage","sign","banner","logo","collateral","packaging","retail","welcome sign"]),
    ("studio",    ["studio","equipment","machine","press","in action","at work","decorated","wrapping","community","process","our studio"]),
]
NAMES = {"jordan": 0, "riley": 1, "sam": 2, "taylor": 3}  # team headshots

# Exact placeholder label -> specific image (checked before keyword rules).
# Used for the Promotional Products "What we make most" grid so each card
# shows its own product.
LABEL_MAP = {
    "Printing": "printing-1.webp",
    "Branding": "uniform-1.webp",  # uniform-program blog post
    # Promotional Products
    "Tumblers & Mugs":  "prod-tumblers.webp",
    "Pens":             "prod-pens.webp",
    "Backpacks & Bags": "prod-bags.webp",
    "Power Banks":      "prod-powerbanks.webp",
    "Notebooks":        "prod-notebooks.webp",
    "Coolers":          "prod-coolers.webp",
    "Keychains":        "prod-keychains.webp",
    "Flashlights":      "prod-flashlights.webp",
    # Embroidery
    "Polo Shirts":        "prod-polos.webp",
    "Caps & Hats":        "prod-caps.webp",
    "Jackets & Vests":    "prod-jackets.webp",
    "Beanies":            "prod-beanies.webp",
    "Work Shirts":        "prod-workshirts.webp",
    "Tote & Duffel Bags": "prod-totebags.webp",
    "Quarter-Zips":       "prod-quarterzips.webp",
    "Aprons":             "prod-aprons.webp",
    # Custom Apparel
    "T-Shirts":         "prod-tshirts.webp",
    "Hoodies":          "prod-hoodies.webp",
    "Long Sleeve Tees": "prod-longsleeve.webp",
    "Performance Tees": "prod-performance.webp",
    "Sweatshirts":      "prod-sweatshirts.webp",
    "Tank Tops":        "prod-tanks.webp",
    "Safety / Hi-Vis":  "prod-hivis.webp",
    "Youth Sizes":      "prod-youth.webp",
    # Awards & Recognition
    "Crystal Awards":   "prod-crystal.webp",
    "Glass Awards":     "prod-glass.webp",
    "Engraved Plaques": "prod-plaques.webp",
    "Acrylic Awards":   "prod-acrylic.webp",
    "Sports Trophies":  "prod-trophies.webp",
    "Retirement Gifts": "prod-retirement.webp",
    "Sales Awards":     "prod-salesawards.webp",
    "Name Badges":      "prod-badges.webp",
    # Laser Engraving
    "Tumblers":         "prod-laser-tumblers.webp",
    "Cutting Boards":   "prod-cuttingboards.webp",
    "Knives & Tools":   "prod-knives.webp",
    "Signs":            "prod-signs.webp",
    "Slate Coasters":   "prod-slate.webp",
    "Leather Journals": "prod-journals.webp",
    "Glassware":        "prod-glassware.webp",
    "Pet Tags":         "prod-pettags.webp",
    # Personalized Gifts (Cutting Boards + Leather Journals reuse the laser images above)
    "Engraved Tumblers": "prod-engravedtumblers.webp",
    "Photo Frames":      "prod-frames.webp",
    "Ornaments":         "prod-ornaments.webp",
    "Glassware Sets":    "prod-glasswaresets.webp",
    "Custom Apparel":    "prod-customapparel.webp",
    "Memorial Pieces":   "prod-memorial.webp",
    # --- Gallery captions ("A look at what's possible" / portfolio) ---
    # Laser Engraving
    "Engraved cutting boards": "prod-cuttingboards.webp",
    "Memorial slate sign":     "prod-slate.webp",
    "Custom tumbler set":      "prod-laser-tumblers.webp",
    "Engraved pocket knives":  "prod-knives.webp",
    "Wooden welcome sign":     "prod-signs.webp",
    "Leather journals":        "prod-journals.webp",
    # Embroidery
    "Corporate uniform program": "prod-polos.webp",
    "Corporate polo program":    "prod-polos.webp",
    "Embroidered cap drop":      "prod-caps.webp",
    "Varsity jackets":           "prod-jackets.webp",
    "Church staff shirts":       "prod-workshirts.webp",
    "Construction hi-vis":       "prod-hivis.webp",
    "Monogrammed bags":          "prod-totebags.webp",
    # Custom Apparel
    "School spirit wear run": "apparel-1.webp",
    "Conference merch line":  "apparel-2.webp",
    "Event hoodies":          "prod-hoodies.webp",
    "5K race tees":           "prod-tshirts.webp",
    "Restaurant staff tees":  "prod-longsleeve.webp",
    "Team jerseys":           "prod-performance.webp",
    # Promotional Products
    "New-hire welcome kits": "promo-1.webp",
    "Trade-show giveaways":  "promo-2.webp",
    "Branded tumbler sets":  "prod-tumblers.webp",
    "Conference tote kits":  "prod-bags.webp",
    "Tech swag bundle":      "prod-powerbanks.webp",
    "Golf-outing gifts":     "prod-coolers.webp",
    # Awards & Recognition
    "Annual sales recognition": "prod-salesawards.webp",
    "Employee of the year":     "prod-crystal.webp",
    "Retirement keepsake":      "prod-retirement.webp",
    "Crystal gala awards":      "prod-glass.webp",
    "League trophy set":        "prod-trophies.webp",
    "Donor recognition wall":   "prod-plaques.webp",
    # Personalized Gifts
    "Wedding party gifts":       "gifts-1.webp",
    "Engraved anniversary set":  "prod-glasswaresets.webp",
    "Graduation keepsakes":      "prod-frames.webp",
    "Holiday client gifts":      "gifts-2.webp",
    "Personalized ornaments":    "prod-ornaments.webp",
    "Memorial tribute piece":    "prod-memorial.webp",
    # Gallery page / homepage extras
    "Full brand rollout":  "branding-1.webp",
    "Branded mug program": "drinkware-1.webp",
    "Personalized whiskey glasses": "drinkware-3.webp",
    "Signage & banners":   "prod-signs.webp",
    "Memorial engraving":  "prod-memorial.webp",
}

_counter = {}
def pick(cat):
    files = CATS.get(cat) or CATS.get("branding") or CATS.get("studio")
    if not files:
        return None
    i = _counter.get(cat, 0); _counter[cat] = i + 1
    return files[i % len(files)]

def image_for(label):
    if label in LABEL_MAP and os.path.isfile(os.path.join(IMGDIR, LABEL_MAP[label])):
        return "assets/img/" + LABEL_MAP[label]
    low = label.lower()
    if low in NAMES and CATS.get("team"):
        team = CATS["team"]
        return team[NAMES[low] % len(team)]
    for cat, kws in RULES:
        if any(k in low for k in kws):
            return pick(cat)
    return pick("branding")

# Cache-busting: bump the version when a file's contents change but its name
# stays the same, so browsers/CDNs fetch the fresh copy. Key = bare filename.
IMG_VERSION = {"drinkware-3.webp": "2"}

def versioned(f):
    base = f.split("/")[-1]
    return f + "?v=" + IMG_VERSION[base] if base in IMG_VERSION else f

PH_RE = re.compile(r'<div class="ph"\s+data-label="([^"]*)"[^>]*>.*?</div>', re.DOTALL)

def process(path, prefix):
    src = open(path, encoding="utf-8").read()
    def repl(m):
        label = m.group(1)
        f = image_for(label)
        if not f:
            return m.group(0)
        alt = htmllib.unescape(label)
        return (f'<img class="ph-img" src="{prefix}{versioned(f)}" alt="{alt}" '
                f'loading="lazy" decoding="async" />')
    out, n = PH_RE.subn(repl, src)
    if n:
        open(path, "w", encoding="utf-8").write(out)
    return n

def main():
    if not CATS:
        print("No images found in assets/img — run the Higgsfield generation first.")
        return
    targets = []
    for f in os.listdir(ROOT):
        if f.endswith(".html"): targets.append((os.path.join(ROOT, f), ""))
    for sub in ("services", "blog"):
        d = os.path.join(ROOT, sub)
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".html"): targets.append((os.path.join(d, f), "../"))
    total = 0
    for path, prefix in sorted(targets):
        # reset per-file counters so variant rotation restarts each page
        _counter.clear()
        n = process(path, prefix)
        total += n
        if n: print(f"{os.path.relpath(path, ROOT):34} {n} images")
    print(f"\nReplaced {total} placeholders across the site. Categories: {', '.join(sorted(CATS))}")

if __name__ == "__main__":
    main()
