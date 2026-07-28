#!/usr/bin/env python3
"""
Craft-show digital signage builder — portrait 1080x1920.

Produces two things from one source:
  signage/index.html   a self-running slide deck (use directly if the CMS
                       accepts a URL; ?s=N renders a single slide)
  signage/ccu-signage-1080x1920.mp4   a looping video for any CMS

Pipeline: compose slides in HTML/CSS -> screenshot each with headless Chrome
-> assemble with ffmpeg (gentle Ken Burns + crossfades).

Run:  python3 scripts/build-signage.py            (html only)
      python3 scripts/build-signage.py --video    (html + mp4, needs ffmpeg)
"""
import os, re, json, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT  = os.path.join(ROOT, "signage")
W, H = 1080, 1920

SITE_URL  = "https://www.ccucustom.com/shop.html"
PHONE     = "(404) 967-8028"
CHROME    = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Seconds each slide holds (before the crossfade into the next)
HOLD_OPEN, HOLD_TITLE, HOLD_PROD, HOLD_GAL, HOLD_QR = 5.5, 3.5, 6.0, 4.0, 8.0
XFADE = 0.9

# --------------------------------------------------------------------------
# Content pulled from the live site so prices/captions can't drift
# --------------------------------------------------------------------------
def education_products():
    s = open(os.path.join(ROOT, "assets/js/shop.js"), encoding="utf-8").read()
    table = {g: (float(y), float(a)) for g, y, a in
             re.findall(r'"([^"]+)":\s*\{\s*Youth:\s*([\d.]+),\s*Adult:\s*([\d.]+)', s)}
    out = []
    for m in re.finditer(r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*price:\s*([\d.]+)(.*?)\},', s, re.S):
        pid, name, price, rest = m.groups()
        if 'cat: "Education"' not in rest:
            continue
        img = re.search(r'img:\s*"([^"]+)"', rest)
        v = re.search(r'"%s":\s*\{([^}]*)\}' % re.escape(pid), s)
        vb = v.group(1) if v else ""
        flat = re.search(r'flat:\s*([\d.]+)', vb)
        frm = False
        if flat:
            price = flat.group(1)
        elif "garments:" in vb:
            # price varies by garment -> quote the cheapest as "from"
            age = "Youth" if 'age: "Youth"' in vb else "Adult"
            cands = [table[g][0 if age == "Youth" else 1]
                     for g in table if '"%s"' % g in vb]
            if cands:
                price, frm = f"{min(cands):.2f}", True
        out.append({"id": pid, "name": name, "price": float(price), "from": frm,
                    "img": img.group(1) if img else ""})
    return out


def gallery_items():
    g = open(os.path.join(ROOT, "gallery.html"), encoding="utf-8").read()
    pairs = re.findall(
        r'data-cat="([^"]+)"[^>]*>.*?src="(assets/img/[^"]+)"[^>]*alt="([^"]+)"', g, re.S)
    return [{"cat": c, "img": i, "cap": a} for c, i, a in pairs]


def qr_svg(url):
    """High-res PNG data-URI. segno's SVG carries no viewBox, so scaling it in
    CSS stretches the canvas and leaves the code tiny — a raster avoids that."""
    sys.path.insert(0, os.path.join(HERE, "_pylibs"))
    import segno, io, base64
    buf = io.BytesIO()
    segno.make(url, error="h").save(buf, kind="png", scale=22, border=0,
                                    dark="#0a0a0f", light="#fbfaf6")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<img src="data:image/png;base64,{b64}" alt="QR code">'


# --------------------------------------------------------------------------
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --ink:#0a0a0f; --ink2:#14141d; --ivory:#fbfaf6;
  --g2:#ecd9a8; --g4:#d4b066; --g5:#c8a24a; --rose:#e0a87e;
  --grad:linear-gradient(120deg,#e3c988,#c8a24a 45%,#e0a87e);
}
html,body{width:1080px;height:1920px;background:var(--ink);overflow:hidden}
body{font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.slide{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;display:none}
.slide.on{display:block}
.bg{position:absolute;inset:0}
.bg img{width:100%;height:100%;object-fit:cover;display:block}
.tint{position:absolute;inset:0}
.pad{position:absolute;inset:0;padding:110px 90px;display:flex;flex-direction:column}
h1,h2,h3{font-family:Fraunces,Georgia,serif;font-weight:600;letter-spacing:-.015em;line-height:1.02}
.eyebrow{font-size:30px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--g4)}
.rule{width:120px;height:5px;background:var(--grad);border-radius:9px}

/* opening */
.open .tint{background:linear-gradient(180deg,rgba(7,7,11,.80),rgba(7,7,11,.45) 40%,rgba(7,7,11,.92))}
.mark{width:170px;height:170px;border-radius:40px;background:var(--grad);
  display:grid;place-items:center;font-family:Fraunces,serif;font-weight:700;font-size:64px;color:#1a1408}
.open h1{font-size:150px;color:var(--ivory);margin:52px 0 30px}
.open .sub{font-size:44px;color:rgba(251,250,246,.82);line-height:1.35;max-width:20ch}
.tag{margin-top:auto;font-size:32px;letter-spacing:.2em;text-transform:uppercase;color:var(--g4);font-weight:600}

/* section title */
.title .tint{background:linear-gradient(180deg,rgba(7,7,11,.90),rgba(7,7,11,.72))}
.title .pad{justify-content:center;align-items:flex-start;gap:40px}
.title h2{font-size:132px;color:var(--ivory);max-width:15ch}
.title .sub{font-size:42px;color:rgba(251,250,246,.78);max-width:24ch;line-height:1.4}

/* product grid */
.prods{background:linear-gradient(165deg,#12121a,#0a0a0f)}
.prods .pad{gap:56px}
.prods h3{font-size:56px;color:var(--ivory)}
.grid{display:flex;flex-direction:column;gap:44px;flex:1}
.card{flex:1;display:flex;gap:44px;align-items:center;background:rgba(251,250,246,.05);
  border:1px solid rgba(251,250,246,.13);border-radius:36px;padding:34px;overflow:hidden}
.card img{width:330px;height:330px;object-fit:cover;border-radius:26px;flex:none;background:#fff}
.card .n{font-family:Fraunces,serif;font-size:50px;font-weight:600;color:var(--ivory);line-height:1.14}
.card .p{margin-top:22px;font-size:60px;font-weight:700;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.card .p small{font-size:28px;font-weight:600;color:var(--g4);-webkit-text-fill-color:var(--g4);margin-right:10px}

/* gallery */
.gal .tint{background:linear-gradient(180deg,rgba(7,7,11,.34) 0%,rgba(7,7,11,0) 32%,rgba(7,7,11,.30) 62%,rgba(7,7,11,.93))}
.gal .pad{justify-content:flex-end;gap:26px}
.gal .cap{font-family:Fraunces,serif;font-size:82px;font-weight:600;color:var(--ivory);max-width:17ch;line-height:1.08}
.gal .cat{font-size:30px;letter-spacing:.2em;text-transform:uppercase;color:var(--g4);font-weight:700}

/* QR */
.qr{background:linear-gradient(165deg,#14141d,#0a0a0f)}
.qr .pad{align-items:center;text-align:center;justify-content:center;gap:0}
.qr h2{font-size:118px;color:var(--ivory);margin-bottom:34px}
.qr .sub{font-size:44px;color:rgba(251,250,246,.80);max-width:22ch;line-height:1.38}
.qrbox{margin:76px 0 64px;width:660px;height:660px;background:var(--ivory);
  border-radius:44px;padding:46px;box-shadow:0 40px 110px rgba(0,0,0,.55)}
.qrbox img{width:100%;height:100%;display:block;image-rendering:pixelated}
.url{font-size:46px;font-weight:700;color:var(--g2);letter-spacing:.01em}
.ph{margin-top:22px;font-size:40px;color:rgba(251,250,246,.72)}
"""

JS = """
(function(){
  var p=new URLSearchParams(location.search), one=p.get('s'), S=[].slice.call(document.querySelectorAll('.slide'));
  if(one!==null){ document.body.setAttribute('data-single',''); var el=S[+one]; if(el) el.classList.add('on'); return; }
  var i=0, hold=S.map(function(s){return +s.dataset.hold*1000;});
  S[0].classList.add('on');
  (function step(){ setTimeout(function(){ S[i].classList.remove('on'); i=(i+1)%S.length; S[i].classList.add('on'); step(); }, hold[i]); })();
})();
"""


def build_html():
    prods, gal = education_products(), gallery_items()
    # Lead with the client's own products, biggest sellers first
    order = ["haec-tshirt", "haec-tshirt-youth", "haec-adult-hoodie",
             "haec-youth-hoodie", "haec-toddler-tee", "haec-beanie",
             "haec-tote", "haec-mug", "haec-tumbler"]
    prods.sort(key=lambda p: order.index(p["id"]) if p["id"] in order else 99)

    hero = "assets/img/hero-laser-2560.webp"
    S = []

    S.append(f"""<section class="slide open" data-hold="{HOLD_OPEN}">
      <div class="bg"><img src="../{hero}" alt=""></div><div class="tint"></div>
      <div class="pad">
        <div class="mark">CCU</div>
        <h1>Custom<br>Creations<br>Unlimited</h1>
        <div class="rule" style="margin:8px 0 34px"></div>
        <p class="sub">Embroidery, custom apparel, laser engraving &amp; personalized gifts &mdash; made in-house in Atlanta.</p>
        <div class="tag">Your Vision &middot; Our Craftsmanship</div>
      </div></section>""")

    S.append(f"""<section class="slide title" data-hold="{HOLD_TITLE}">
      <div class="bg"><img src="../assets/img/shop-haec-tshirt.webp" alt=""></div><div class="tint"></div>
      <div class="pad">
        <div class="eyebrow">Official Spirit Wear</div>
        <h2>Made for High Achievers</h2>
        <div class="rule"></div>
        <p class="sub">H.A.E.C tees, hoodies, drinkware &amp; gifts &mdash; PTO and non-PTO pricing.</p>
      </div></section>""")

    for c in range(0, 9, 3):
        chunk = prods[c:c + 3]
        cards = ""
        for p in chunk:
            frm = '<small>from</small> ' if p["from"] else ''
            nm = p["name"].replace("H.A.E.C ", "")
            cards += (f'<div class="card"><img src="../{p["img"]}" alt="">'
                      f'<div><div class="n">{nm}</div>'
                      f'<div class="p">{frm}${p["price"]:.2f}</div></div></div>')
        S.append(f"""<section class="slide prods" data-hold="{HOLD_PROD}">
          <div class="pad"><h3>H.A.E.C Collection</h3>
          <div class="grid">{cards}</div></div></section>""")

    S.append(f"""<section class="slide title" data-hold="{HOLD_TITLE}">
      <div class="bg"><img src="../assets/img/prod-polos.webp" alt=""></div><div class="tint"></div>
      <div class="pad">
        <div class="eyebrow">Our Work</div>
        <h2>15,000+ brands served</h2>
        <div class="rule"></div>
        <p class="sub">Uniform programs, awards, promo kits and one-off keepsakes.</p>
      </div></section>""")

    picks = ["prod-polos", "prod-salesawards", "prod-cuttingboards", "prod-laser-tumblers",
             "promo-1", "prod-caps", "gifts-1", "prod-glass"]
    for key in picks:
        it = next((g for g in gal if key in g["img"]), None)
        if not it:
            continue
        S.append(f"""<section class="slide gal" data-hold="{HOLD_GAL}">
          <div class="bg"><img src="../{it['img']}" alt=""></div><div class="tint"></div>
          <div class="pad"><div class="cat">{it['cat']}</div>
          <div class="cap">{it['cap']}</div></div></section>""")

    S.append(f"""<section class="slide qr" data-hold="{HOLD_QR}">
      <div class="pad">
        <div class="eyebrow">Scan for the full catalog</div>
        <h2 style="margin-top:26px">Shop everything online</h2>
        <p class="sub">Sizes, colors, bulk pricing and secure checkout.</p>
        <div class="qrbox">{qr_svg(SITE_URL)}</div>
        <div class="url">ccucustom.com</div>
        <div class="ph">{PHONE} &middot; info@ccucustom.com</div>
      </div></section>""")

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>CCU Signage 1080x1920</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{''.join(S)}
<script>{JS}</script></body></html>"""

    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    holds = [float(x) for x in re.findall(r'data-hold="([\d.]+)"', html)]
    print(f"signage/index.html  ->  {len(holds)} slides, loop {sum(holds):.1f}s")
    return holds


def build_video(holds):
    frames = os.path.join(OUT, "_frames")
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames, exist_ok=True)
    src = "file://" + os.path.join(OUT, "index.html")

    for i in range(len(holds)):
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={W},{H}",
                        "--virtual-time-budget=6000", "--allow-file-access-from-files",
                        f"--screenshot={frames}/s{i:02d}.png", f"{src}?s={i}"],
                       check=True, capture_output=True)
        print(f"  shot slide {i+1}/{len(holds)}")

    # Ken Burns per slide, then chain crossfades.
    # NOTE: zoompan's `d` is output frames PER INPUT FRAME. With a looped still
    # that multiplies the clip length, so keep d=1 and drive the zoom off `on`
    # (the output frame index) instead of accumulating `zoom`.
    parts, filt = [], []
    for i, hold in enumerate(holds):
        dur = hold + XFADE
        n = max(1, int(dur * 30))
        parts += ["-loop", "1", "-framerate", "30", "-t", f"{dur}",
                  "-i", f"{frames}/s{i:02d}.png"]
        z = 1.0 + (0.055 if i % 2 == 0 else 0.04)
        filt.append(
            f"[{i}:v]scale={int(W*1.2)}:{int(H*1.2)}:flags=lanczos,"
            f"zoompan=z='min(1+{(z-1)/n:.8f}*on,{z})':d=1:x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30,setsar=1[v{i}]")
    chain, off = "[v0]", 0.0
    for i in range(1, len(holds)):
        off += holds[i-1]
        nxt = f"[x{i}]" if i < len(holds)-1 else "[out]"
        filt.append(f"{chain}[v{i}]xfade=transition=fade:duration={XFADE}:offset={off:.3f}{nxt}")
        chain = f"[x{i}]"
    out = os.path.join(OUT, "ccu-signage-1080x1920-silent.mp4")
    # crf 23 + a bitrate ceiling keeps it well under typical CMS upload limits
    subprocess.run(["ffmpeg", "-y", *parts, "-filter_complex", ";".join(filt),
                    "-map", "[out]", "-c:v", "libx264", "-profile:v", "high",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
                    "-crf", "23", "-maxrate", "6M", "-bufsize", "12M",
                    "-movflags", "+faststart", out],
                   check=True, capture_output=True)
    print("signage/ccu-signage-1080x1920-silent.mp4 ->",
          f"{os.path.getsize(out)/1e6:.1f} MB")
    add_music(out, sum(holds) + XFADE)
    shutil.rmtree(frames, ignore_errors=True)


def add_music(silent, dur):
    """Mux the ambient bed on: trim to length, normalise to a background level,
    fade both ends so the loop seam dips to silence."""
    bed = os.path.join(OUT, "audio", "bed.mp3")
    out = os.path.join(OUT, "ccu-signage-1080x1920.mp4")
    if not os.path.exists(bed):
        print("no signage/audio/bed.mp3 — skipping music")
        return
    fo = max(0.0, dur - 2.5)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-stream_loop", "-1", "-i", bed,
                    "-filter_complex",
                    f"[1:a]atrim=0:{dur},asetpts=N/SR/TB,loudnorm=I=-17:TP=-1.5:LRA=11,"
                    f"afade=t=in:st=0:d=2,afade=t=out:st={fo:.2f}:d=2.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "44100",
                    "-shortest", "-movflags", "+faststart", out],
                   check=True, capture_output=True)
    print("signage/ccu-signage-1080x1920.mp4 (with music) ->",
          f"{os.path.getsize(out)/1e6:.1f} MB")


if __name__ == "__main__":
    h = build_html()
    if "--video" in sys.argv:
        build_video(h)
