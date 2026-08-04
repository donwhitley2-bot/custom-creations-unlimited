#!/usr/bin/env python3
"""
Build the print-ready tri-fold brochure.

    python3 scripts/build-brochure.py            # HTML + PDF, with fold ticks
    python3 scripts/build-brochure.py --no-marks # for a commercial printer

Writes print/brochure.html and print/ccu-brochure.pdf — two US-Letter landscape
pages (11 x 8.5in): page 1 is the OUTSIDE of the sheet, page 2 the INSIDE.

Panel widths are NOT equal thirds. In a letter fold the left panel tucks inside
the other two, so it must be 1/16in narrower or it buckles against the fold.
Flipping the sheet mirrors the panels, which is why the inside page carries the
narrow panel on the right.

All copy is pulled from the live site's own wording so the brochure and the
website never drift apart.
"""
import argparse, base64, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "print")
sys.path.insert(0, os.path.join(HERE, "_pylibs"))

SITE = "https://www.ccucustom.com"
PHONE = "(404) 967-8028"
EMAIL = "info@ccucustom.com"
ADDR = "1180 Industrial Park Blvd, Suite 200<br>Atlanta, GA 30318"

CHROME = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
          "/Applications/Chromium.app/Contents/MacOS/Chromium",
          "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")

SERVICES = [
    ("Embroidery", "embroidery-1.webp",
     "Logos stitched on polos, caps, jackets, beanies and bags for company "
     "uniforms, schools, churches and teams."),
    ("Custom Apparel", "apparel-1.webp",
     "DTF printing, screen printing and heat-transfer vinyl on tees, hoodies "
     "and performance wear. Vivid color, soft feel."),
    ("Promotional Products", "drinkware-1.webp",
     "Tumblers, pens, bags, power banks and trade-show giveaways — curated "
     "swag that actually gets used."),
    ("Laser Engraving", "laser-1.webp",
     "Wood, glass, metal, leather, slate and acrylic. Tumblers, knives, "
     "cutting boards, signs and gifts in photo-grade detail."),
    ("Awards &amp; Recognition", "awards-1.webp",
     "Crystal and glass awards, engraved plaques and trophies for employee "
     "recognition, sales milestones and retirements."),
    ("Personalized Gifts", "gifts-1.webp",
     "Weddings, birthdays, anniversaries, graduations and holidays — "
     "keepsakes they'll actually hold onto."),
]

INDUSTRIES = [
    ("Schools", "Spirit wear &amp; uniforms"), ("Churches", "Apparel &amp; events"),
    ("Construction", "Hi-vis &amp; workwear"), ("Restaurants", "Branded apparel"),
    ("Healthcare", "Scrubs &amp; recognition"), ("Government", "Civic &amp; safety"),
    ("Sports Teams", "Uniforms &amp; trophies"), ("Corporate", "Brand programs"),
    ("Real Estate", "Signs &amp; gifts"), ("Nonprofits", "Events &amp; merch"),
]

STEPS = [
    ("Tell us what you need", "Send a logo, artwork, or just an idea and a deadline."),
    ("We quote and proof", "You get a free digital proof. Nothing is charged until you approve it."),
    ("You approve", "We produce exactly what is on the proof — no surprises."),
    ("We deliver", "Atlanta pickup, local delivery, or shipped anywhere."),
]

WHY = [
    "No minimums on most items",
    "Free design proofs, every time",
    "Rush turnaround when deadlines are tight",
    "Decorated in-house — we don't broker it out",
    "98% delivered on time",
]


def data_uri(relpath):
    p = os.path.join(ROOT, relpath)
    ext = os.path.splitext(p)[1].lstrip(".").lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "webp": "image/webp"}[ext]
    with open(p, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def qr_uri(url):
    """A high-res PNG, not segno's SVG: the SVG carries no viewBox, so scaling
    it in CSS stretches the canvas instead of the code."""
    import io, segno
    buf = io.BytesIO()
    # Opaque white quiet zone matching the panel — a transparent QR loses its
    # light border, which scanners need.
    segno.make(url, error="h").save(buf, kind="png", scale=20, border=2,
                                    dark="#101019", light="#ffffff")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --ink:#101019; --ink-soft:#1d1d28; --ivory:#f7f4ee; --ivory-2:#efe9df;
  --gold:#c8a24a; --gold-lt:#e3c988; --gold-dk:#8a6c2c;
  --text:#14141b; --muted:#565663;
  --pad:.30in;                 /* keeps ink clear of trim and fold lines */
}
@page{ size:11in 8.5in; margin:0 }
html,body{ width:11in; background:#fff; color:var(--text);
  font-family:"Inter","Helvetica Neue",Arial,sans-serif; font-size:9pt; line-height:1.42;
  -webkit-print-color-adjust:exact; print-color-adjust:exact }
.sheet{ width:11in; height:8.5in; display:flex; overflow:hidden; position:relative;
  page-break-after:always; break-after:page }
.sheet:last-child{ page-break-after:auto; break-after:auto }
.panel{ height:8.5in; padding:var(--pad); position:relative; overflow:hidden;
  display:flex; flex-direction:column }
.w-narrow{ width:3.625in; flex:0 0 3.625in }
.w-wide  { width:3.6875in; flex:0 0 3.6875in }
/* Every panel is bare white. A toner-heavy panel cracks along the folds and
   eats a cartridge, and no laser can reach the sheet edge — the unprintable
   margin would frame any full-panel fill, tint or black, in ragged white.
   Warmth comes from the gold rules and the ivory blocks instead. */
.soft,.tint{ background:#fff }   /* see note above — no full-panel fills */

h1,h2,h3,.disp{ font-family:"Fraunces",Georgia,"Times New Roman",serif; font-weight:600;
  line-height:1.1; letter-spacing:-.01em }
.eyebrow{ font-size:6.6pt; letter-spacing:.19em; text-transform:uppercase;
  font-weight:700; color:var(--gold-dk) }
.rule{ height:2px; width:1.1in; background:linear-gradient(90deg,var(--gold-lt),var(--gold-dk));
  border-radius:2px }
.muted{ color:var(--muted) }
.grow{ flex:1 }
.hair{ border-top:1px solid rgba(20,20,28,.14) }

/* ---- front cover ---- */
.cover-in{ display:flex; flex-direction:column; height:100% }
.mark{ height:.62in; width:auto; align-self:flex-start; flex:none }
.cover-in h1{ font-size:25pt; margin:.16in 0 .10in }
.cover-in h1 em{ font-style:normal; color:var(--gold-dk) }
.cover-tag{ font-size:9.4pt; color:var(--muted); max-width:2.8in }
.cover-foot{ font-size:7.6pt; letter-spacing:.13em; text-transform:uppercase;
  color:var(--gold-dk); font-weight:700 }

/* ---- generic blocks ---- */
.stack > * + *{ margin-top:.19in }
.svc{ display:flex; gap:.14in; align-items:flex-start }
.svc img{ width:1.02in; height:1.02in; object-fit:cover; border-radius:.06in; flex:none }
.svc h3{ font-size:11.5pt; margin-bottom:.035in }
.svc p{ font-size:8.6pt; line-height:1.42; color:var(--muted) }
.band{ width:100%; object-fit:cover; border-radius:.07in; display:block }

.steps{ counter-reset:s; list-style:none }
.steps li{ counter-increment:s; position:relative; padding-left:.38in; margin-bottom:.19in }
.steps li::before{ content:counter(s); position:absolute; left:0; top:-.01in;
  width:.27in; height:.27in; border-radius:50%;
  background:linear-gradient(135deg,var(--gold-lt),var(--gold-dk)); color:var(--ink);
  font-size:8.2pt; font-weight:800; display:flex; align-items:center; justify-content:center }
.steps b{ display:block; font-size:9.6pt }
.steps span{ font-size:8.4pt; color:var(--muted); line-height:1.4 }

.ticks{ list-style:none }
.ticks li{ position:relative; padding-left:.24in; margin-bottom:.10in; font-size:9pt }
.ticks li::before{ content:"✓"; position:absolute; left:0; color:var(--gold-dk); font-weight:800 }
.dark .ticks li::before{ color:var(--gold-lt) }

.inds{ display:grid; grid-template-columns:1fr 1fr; gap:.09in }
.inds div{ background:var(--ivory); border:1px solid rgba(20,20,28,.10); border-radius:.05in; padding:.085in .09in }
.inds b{ display:block; font-size:8.6pt } .inds span{ font-size:7pt; color:var(--muted) }

.stat{ display:flex; gap:.16in; margin-top:.04in }
.stat b{ font-family:"Fraunces",Georgia,serif; font-size:14pt; display:block; line-height:1;
  color:var(--gold-dk) }
.dark .stat b{ color:var(--gold-lt) }
.stat span{ font-size:6.6pt; text-transform:uppercase; letter-spacing:.09em; color:var(--muted) }

.qr-card{ width:1.66in; margin:0 auto }
.qr{ width:1.66in; height:1.66in; display:block }
.qr-cap{ text-align:center; font-size:8pt; color:var(--muted); margin-top:.09in }
.svclist{ text-align:center; max-width:2.45in; margin:0 auto; font-size:8pt; line-height:1.75 }
.svclist b{ color:var(--gold-dk); font-weight:600 }
.contact{ font-size:9.4pt; line-height:1.6 }
.contact a{ color:inherit; text-decoration:none }
.contact .big{ font-family:"Fraunces",Georgia,serif; font-size:15pt; color:var(--gold-dk) }

.cta{ background:linear-gradient(135deg,var(--gold-lt),var(--gold-dk)); color:#1a1408;
  border-radius:.07in; padding:.12in .13in; text-align:center }
.cta b{ display:block; font-family:"Fraunces",Georgia,serif; font-size:11pt }
.cta span{ font-size:7.4pt }

.spread-head{ text-align:center }
.spread-head h2{ font-size:15pt }
.spread-head .rule{ margin:.08in auto 0 }

/* Fold ticks sit in the top/bottom 0.1in, which most home printers cannot
   reach anyway — they guide the fold without marking the finished piece. */
.tick{ position:absolute; z-index:20; width:0; border-left:.75pt dashed #8f8f8f; height:.13in }
.tick.t{ top:0 } .tick.b{ bottom:0 }
"""


def cover(assets):
    return f"""<div class="panel w-wide soft">
  <div class="cover-in">
    <img class="mark" src="{assets['dark']}" alt="Custom Creations Unlimited">
    <div class="grow"></div>
    <p class="eyebrow">Atlanta, Georgia</p>
    <h1>Custom branding that makes your business <em>stand out.</em></h1>
    <div class="rule" style="margin:.12in 0 .14in"></div>
    <p class="cover-tag">Embroidery, apparel, promotional products, awards,
      laser engraving and personalized gifts — all decorated in-house.</p>
    <img class="band" src="{assets['hero']}" alt="" style="height:3.05in;margin-top:.28in">
    <div class="grow"></div>
    <p class="cover-foot hair" style="padding-top:.16in">ccucustom.com &nbsp;·&nbsp; {PHONE}</p>
  </div>
</div>"""


def back(assets):
    names = " &nbsp;·&nbsp; ".join(n for n, _, _ in SERVICES)
    return f"""<div class="panel w-wide tint">
  <div style="text-align:center">
    <img class="mark" src="{assets['dark']}" alt="" style="align-self:center;margin:0 auto">
    <p class="eyebrow" style="margin-top:.16in">Atlanta's in-house branding shop</p>
    <div class="rule" style="margin:.10in auto .16in"></div>
    <p class="svclist"><b>{names}</b></p>
  </div>
  <div class="grow"></div>
  <div class="qr-card"><img class="qr" src="{assets['qr']}" alt="QR code to ccucustom.com"></div>
  <p class="qr-cap">Scan to browse products, see our work<br>and request a quote in about a minute</p>
  <div class="grow"></div>
  <div class="rule" style="margin:0 auto .18in"></div>
  <div class="contact" style="text-align:center">
    <span class="big">{PHONE}</span><br>
    <a href="mailto:{EMAIL}">{EMAIL}</a><br>
    <span class="muted" style="font-size:8.4pt">{ADDR}</span>
  </div>
  <div class="grow"></div>
  <p class="qr-cap hair" style="font-size:7.2pt;margin:0;padding-top:.14in">
    Custom Creations Unlimited &nbsp;·&nbsp; ccucustom.com</p>
</div>"""


def flap(assets):
    steps = "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in STEPS)
    ticks = "".join(f"<li>{w}</li>" for w in WHY)
    return f"""<div class="panel w-narrow tint">
  <p class="eyebrow">How it works</p>
  <div class="rule" style="margin:.07in 0 .18in"></div>
  <ol class="steps">{steps}</ol>
  <img class="band" src="{assets['work']}" alt="" style="height:1.55in;margin:.04in 0 .26in">
  <p class="eyebrow">Why people stay with us</p>
  <div class="rule" style="margin:.07in 0 .16in"></div>
  <ul class="ticks">{ticks}</ul>
  <div class="grow"></div>
  <div class="stat">
    <div><b>15,000+</b><span>Brands served</span></div>
    <div><b>4.9/5</b><span>1,280+ reviews</span></div>
  </div>
</div>"""


def svc_block(items, assets):
    return "".join(
        f"""<div class="svc"><img src="{assets['svc'][img]}" alt="">
        <div><h3>{name}</h3><p>{copy}</p></div></div>"""
        for name, img, copy in items)


def inside_left(assets):
    return f"""<div class="panel w-wide soft">
  <div class="spread-head" style="text-align:left">
    <p class="eyebrow">What we make</p>
    <h2 style="font-size:16pt;margin-top:.04in">Six ways to put<br>your name on it.</h2>
    <div class="rule" style="margin:.09in 0 0"></div>
  </div>
  <div class="stack" style="margin-top:.22in">{svc_block(SERVICES[:3], assets)}</div>
  <div class="grow"></div>
  <img class="band" src="{assets['shop']}" alt="" style="height:2.15in;margin-bottom:.2in">
  <p class="muted" style="font-size:8.4pt;border-top:1px solid rgba(20,20,28,.12);padding-top:.13in">
    One shirt or ten thousand — there is <b>no minimum</b> on most items, and every
    order gets a free proof before anything is produced.</p>
</div>"""


def inside_mid(assets):
    return f"""<div class="panel w-wide soft">
  <div class="stack" style="margin-top:.02in">{svc_block(SERVICES[3:], assets)}</div>
  <div class="grow"></div>
  <p class="eyebrow">Who we serve</p>
  <div class="rule" style="margin:.07in 0 .16in"></div>
  <div class="inds">""" + "".join(
        f"<div><b>{n}</b><span>{d}</span></div>" for n, d in INDUSTRIES) + """</div>
  <p class="muted" style="font-size:8pt;margin-top:.14in">…and plenty that don't
    fit a category. If you can put a logo on it, ask us.</p>
</div>"""


def inside_right(assets):
    return f"""<div class="panel w-narrow tint">
  <p class="eyebrow">Ready when you are</p>
  <div class="rule" style="margin:.07in 0 .16in"></div>
  <h2 style="font-size:15.5pt">Send us your logo.<br>We'll do the rest.</h2>
  <p class="muted" style="font-size:8.8pt;margin-top:.13in">
    Tell us what you're making, how many, and when you need it. You'll get a
    quote and a free digital proof — and we don't produce a thing until you
    say the proof is right.</p>
  <div class="cta" style="margin-top:.20in">
    <b>Request a quote</b><span>ccucustom.com &nbsp;·&nbsp; {PHONE}</span></div>
  <img class="band" src="{assets['branding']}" alt="" style="height:1.9in;margin-top:.24in">
  <div class="grow"></div>
  <p class="eyebrow">What to send us</p>
  <div class="rule" style="margin:.07in 0 .14in"></div>
  <p class="muted" style="font-size:8.6pt">A PNG, PDF, AI or EPS of your logo is
    ideal. Only have a photo or a business card? Send that — we'll redraw it
    clean before it goes anywhere near a machine.</p>
  <p class="eyebrow" style="margin-top:.24in">Need it fast?</p>
  <div class="rule" style="margin:.07in 0 .14in"></div>
  <p class="muted" style="font-size:8.6pt">Rush service is available on most
    products. Tell us your deadline up front and we'll say straight away
    whether we can hit it.</p>
  <div class="grow"></div>
  <div class="contact" style="margin-top:.18in;font-size:9pt;border-top:1px solid rgba(20,20,28,.12);padding-top:.14in">
    <b>{PHONE}</b><br><span class="muted">{EMAIL}</span></div>
</div>"""


def ticks_for(widths):
    """Fold guides at the panel boundaries, top and bottom."""
    out, x = [], 0.0
    for w in widths[:-1]:
        x += w
        out.append(f'<span class="tick t" style="left:{x}in"></span>'
                   f'<span class="tick b" style="left:{x}in"></span>')
    return "".join(out)


def build(marks=True):
    os.makedirs(OUT, exist_ok=True)
    assets = {
        # Chosen by measured mean luminance (0-255). The old picks — the dark
        # laser hero at 98, branding-1 at 71, embroidery-2 at 86 — laid down a
        # lot of toner as large bands. These sit at 117-161.
        "hero": data_uri("assets/img/laser-2.webp"),          # 161
        "dark": data_uri("signage/assets/ccu-mark-dark.png"),
        "branding": data_uri("assets/img/apparel-2.webp"),    # 117
        "work": data_uri("assets/img/gifts-2.webp"),          # 145
        "shop": data_uri("assets/img/printing-1.webp"),       # 118
        "qr": qr_uri(SITE),
        "svc": {img: data_uri("assets/img/" + img) for _, img, _ in SERVICES},
    }

    # Outside: the narrow tuck-in flap is on the left. Flipping the sheet
    # mirrors that, so the inside page carries the narrow panel on the right.
    out_w = [3.625, 3.6875, 3.6875]
    in_w = [3.6875, 3.6875, 3.625]

    m1 = ticks_for(out_w) if marks else ""
    m2 = ticks_for(in_w) if marks else ""

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Custom Creations Unlimited — tri-fold brochure</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="sheet">{m1}{flap(assets)}{back(assets)}{cover(assets)}</div>
<div class="sheet">{m2}{inside_left(assets)}{inside_mid(assets)}{inside_right(assets)}</div>
</body></html>"""

    hpath = os.path.join(OUT, "brochure.html")
    open(hpath, "w", encoding="utf-8").write(html)
    print(f"  print/brochure.html      {os.path.getsize(hpath)/1e6:.1f} MB")

    chrome = next((c for c in CHROME if os.path.exists(c)), None)
    if not chrome:
        print("  (Chrome not found — open the HTML and print to PDF manually)")
        return
    pdf = os.path.join(OUT, "ccu-brochure.pdf")
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf-no-header", "--virtual-time-budget=12000",
                    "--print-to-pdf=" + pdf, "file://" + hpath],
                   capture_output=True)
    if os.path.exists(pdf):
        print(f"  print/ccu-brochure.pdf   {os.path.getsize(pdf)/1e6:.1f} MB")
    else:
        print("  PDF render failed — open print/brochure.html and print to PDF")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-marks", action="store_true",
                    help="omit fold ticks (use for a commercial printer)")
    build(marks=not ap.parse_args().no_marks)
