#!/usr/bin/env python3
"""
Build the video hero PREVIEW — not wired into the live site.

    python3 scripts/build-hero-video.py

Encodes the marketing footage into web loops plus a poster frame, then writes
preview/hero-video.html. Open it directly; nothing links to it, nothing is
committed.

The source is a 12s one-way dolly-in, so a plain loop snaps from close-up back
to wide every pass. It is encoded as a palindrome (forward, then reversed) and
the camera simply breathes in and out — no seam to notice.
"""
import argparse, base64, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "preview")
VID = os.path.join(OUT, "video")   # reassigned by main() when SLUG is set

SRC = os.path.expanduser(
    "~/Downloads/modern-craft-shop-hero-live-stock-1920x1080.mp4")
SLUG = ""            # "" -> hero-video.html + video/ ; else -<slug> on both

# The stock clip is a four-shot edit (embroidery head, hand-stamping, laser
# cutting) rather than one continuous move, so there is no one-way camera push
# to undo — it just loops. It happens to open and close on the embroidery head,
# which makes the wrap read as one more cut. PALINDROME is kept for the old
# single-move footage.
PALINDROME = False

RENDITIONS = [(1920, 30), (1280, 31), (860, 32)]   # width, crf

CLIP = None          # seconds to keep, or None for the whole clip


def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-1500:])
    return r


def encode():
    os.makedirs(VID, exist_ok=True)
    if not os.path.exists(SRC):
        sys.exit("source footage not found:\n  " + SRC)

    for w, crf in RENDITIONS:
        dst = os.path.join(VID, f"hero-loop-{w}.mp4")
        # split -> reverse one copy -> concat. Trimming a frame off each end of
        # the reversed half kills the duplicated frame at both turnarounds.
        chain = (("[0:v]split[a][b];"
                   "[b]reverse,trim=start_frame=1,setpts=PTS-STARTPTS[r];"
                   "[a][r]concat=n=2:v=1:a=0,")
                 if PALINDROME else "[0:v]")
        run("ffmpeg", "-y", "-v", "error",
            *(("-t", str(CLIP)) if CLIP else ()), "-i", SRC, "-filter_complex",
            chain + f"scale={w}:-2:flags=lanczos,fps=30[v]",
            "-map", "[v]", "-an",
            "-c:v", "libx264", "-crf", str(crf), "-preset", "slow",
            "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", dst)
        print(f"  {os.path.basename(VID)}/hero-loop-{w}.mp4   {os.path.getsize(dst)/1e6:.1f} MB")

    # Poster = first frame. It is what actually paints for LCP, so the video
    # never has to be on the critical path.
    poster = os.path.join(VID, "hero-poster.jpg")
    run("ffmpeg", "-y", "-v", "error", "-i", SRC, "-frames:v", "1",
        "-vf", "scale=1920:-2", "-q:v", "4", poster)   # this ffmpeg has no webp encoder
    print(f"  {os.path.basename(VID)}/hero-poster.jpg   {os.path.getsize(poster)/1e6:.2f} MB")
    return poster


HERO = """
    <!-- ===================== HERO (video preview) ===================== -->
    <section class="hero hero--laser hero--vid" id="heroLaser" aria-labelledby="hero-h">
      <div class="hero-vid" aria-hidden="true">
        <video id="heroVideo" class="hero-vid__el"
               poster="__V__/hero-poster.jpg"
               muted playsinline loop preload="none" disablepictureinpicture>
          <source data-src="__V__/hero-loop-1920.mp4" type="video/mp4" media="(min-width:1400px)">
          <source data-src="__V__/hero-loop-1280.mp4" type="video/mp4" media="(min-width:800px)">
          <source data-src="__V__/hero-loop-860.mp4"  type="video/mp4">
        </video>
      </div>
      <div class="hero-vid__scrim" aria-hidden="true"></div>

      <div class="container hero__inner" id="heroInner">
        <div class="hero__copy">
          <div class="hero__rating" data-reveal>
            <span class="stars" aria-hidden="true">__STARS__</span>
            <span><strong>4.9/5</strong> from 1,280+ reviews</span>
          </div>

          <h1 id="hero-h" data-reveal data-delay="1">Custom branding<br>that makes your<br>business <em class="text-gradient">stand out.</em></h1>

          <p class="hero__sub" data-reveal data-delay="2">From embroidered apparel and
            promotional products to laser engraving and personalized gifts — we help
            businesses, schools, organizations and individuals bring their ideas to life.</p>

          <div class="hero__cta" data-reveal data-delay="3">
            <a class="btn btn--gold btn--lg" href="../shop.html">Shop Custom Items
              <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <a class="btn btn--ghost btn--lg" href="../quote.html">Request a Quote</a>
          </div>

          <div class="hero__proof" data-reveal data-delay="4">
            <span><b>15,000+</b> brands served</span>
            <span><b>No minimums</b> on most items</span>
            <span><b>Free</b> design proofs</span>
          </div>
        </div>
      </div>

      <button class="hero-vid__btn" id="heroVidBtn" type="button"
              aria-label="Pause background video">
        <svg viewBox="0 0 24 24" fill="currentColor" class="i-pause"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>
        <svg viewBox="0 0 24 24" fill="currentColor" class="i-play"><path d="M8 5l11 7-11 7z"/></svg>
      </button>
    </section>
"""

CSS = """
/* ============ preview-only video hero ============ */
.hero--vid{ position:relative; min-height:100svh; display:flex; align-items:center;
  overflow:hidden; background:#0c0a08 }
.hero-vid{ position:absolute; inset:0 }
.hero-vid__el{ width:100%; height:100%; object-fit:cover; display:block;
  transform:scale(1.02); filter:saturate(.95) brightness(.88) }           /* hides any edge softness from the encode */

/* Two scrims, not one: a left-to-right wash so the copy always has contrast,
   plus a floor gradient so the section hands off to the page below. */
.hero-vid__scrim{ position:absolute; inset:0; pointer-events:none;
  background:
    linear-gradient(90deg, rgba(8,7,6,.84) 0%, rgba(8,7,6,.70) 32%,
                           rgba(8,7,6,.42) 60%, rgba(8,7,6,.18) 100%),
    linear-gradient(180deg, rgba(8,7,6,.62) 0%, rgba(8,7,6,.18) 30%,
                            rgba(8,7,6,.22) 60%, rgba(8,7,6,.78) 100%) }

.hero--vid .hero__inner{ position:relative; z-index:2; padding-block:clamp(5rem,12vh,8rem) }
/* copy width, h1 size, text colour and shadows all come from .hero--laser */

.hero__proof{ display:flex; flex-wrap:wrap; gap:.55rem 1.5rem; margin-top:1.9rem;
  padding-top:1.35rem; border-top:1px solid rgba(255,255,255,.16);
  font-size:.88rem; color:#cfc9bf }
.hero__proof b{ color:#fff; font-weight:700 }

/* bottom-LEFT: the floating call/chat buttons own the bottom-right corner */
.hero-vid__btn{ position:absolute; left:1.15rem; bottom:1.15rem; z-index:3;
  width:2.5rem; height:2.5rem; border-radius:50%; cursor:pointer;
  display:grid; place-items:center; color:#fff;
  background:rgba(12,10,8,.5); border:1px solid rgba(255,255,255,.28);
  backdrop-filter:blur(6px); opacity:.55; transition:opacity .2s }
.hero-vid__btn:hover,.hero-vid__btn:focus-visible{ opacity:1 }
.hero-vid__btn svg{ width:15px; height:15px }
.hero-vid__btn .i-play{ display:none }
.hero-vid__btn.paused .i-pause{ display:none }
.hero-vid__btn.paused .i-play{ display:block }

@media (max-width:719px){
  .hero-vid__scrim{ background:
    linear-gradient(180deg, rgba(8,7,6,.74) 0%, rgba(8,7,6,.62) 40%, rgba(8,7,6,.92) 100%) }
  .hero__proof{ gap:.4rem 1.1rem; font-size:.82rem }
}

/* Anyone who asks for less motion just gets the poster frame. */
@media (prefers-reduced-motion:reduce){
  .hero-vid__el{ display:none }
  .hero-vid{ background:url(__V__/hero-poster.jpg) center/cover no-repeat }
  .hero-vid__btn{ display:none }
}
"""

JS = """
<script>
(function(){
  var v = document.getElementById('heroVideo'), btn = document.getElementById('heroVidBtn');
  if(!v) return;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce) return;

  // The poster paints first; the video only starts downloading once the page
  // is up, so it never competes with the largest contentful paint.
  function load(){
    if(v.dataset.on) return;
    v.dataset.on = '1';
    [].forEach.call(v.querySelectorAll('source'), function(s){
      if(s.dataset.src) s.src = s.dataset.src;
    });
    v.load();
    v.play().catch(function(){ mark(true); });   // autoplay refused: show play
  }
  if(document.readyState === 'complete') setTimeout(load, 180);
  else addEventListener('load', function(){ setTimeout(load, 180); });

  function mark(paused){ btn.classList.toggle('paused', paused);
    btn.setAttribute('aria-label', paused ? 'Play background video' : 'Pause background video'); }

  btn.addEventListener('click', function(){
    if(v.paused){ v.play(); mark(false); } else { v.pause(); mark(true); }
  });

  // Don't burn cycles decoding video that isn't on screen.
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!v.dataset.on || btn.classList.contains('paused')) return;
        if(e.isIntersecting) v.play().catch(function(){}); else v.pause();
      });
    }, {threshold:0.05}).observe(v);
  }
  document.addEventListener('visibilitychange', function(){
    if(!v.dataset.on || btn.classList.contains('paused')) return;
    if(document.hidden) v.pause(); else v.play().catch(function(){});
  });
})();
</script>
"""


def build_page():
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    a = src.find('<section class="hero hero--laser"')
    b = src.find("</section>", src.find("hero-chips__bar")) + len("</section>")
    if a < 0:
        sys.exit("could not locate the hero section in index.html")

    stars = re.search(r'<span class="stars"[^>]*>(.*?)</span>', src, re.S).group(1)
    head, tail = src[:a], src[b:]

    def rebase(s):
        s = re.sub(r'(src|href)="(?!https?:|//|#|mailto:|tel:|\.\./|data:|video/)', r'\1="../', s)
        return re.sub(r'(\s)(assets/img/[^\s"]+)', r'\1../\2', s)

    vdir = "video" + (("-" + SLUG) if SLUG else "")
    page = rebase(head) + HERO.replace("__STARS__", stars) + rebase(tail)
    page = page.replace("__V__", vdir)
    page = page.replace("</head>", "<style>" + CSS.replace("__V__", vdir) + "</style>\n</head>", 1)
    page = page.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    page = page.replace("<title>", "<title>PREVIEW · ", 1)
    page = page.replace("</body>", JS + "\n</body>")

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "hero-video" + (("-" + SLUG) if SLUG else "") + ".html")
    open(path, "w", encoding="utf-8").write(page)
    print(f"  {os.path.basename(path):25} {os.path.getsize(path)/1e6:.2f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src"); ap.add_argument("--slug", default="")
    a = ap.parse_args()
    if a.src:
        SRC = os.path.expanduser(a.src)
    SLUG = a.slug
    if SLUG:
        VID = os.path.join(OUT, "video-" + SLUG)
    encode()
    build_page()
    print("  (not linked from the site, not committed)")
