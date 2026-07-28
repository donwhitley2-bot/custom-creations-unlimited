# Craft-show signage — portrait 1080×1920

Two ways to run it. Both come from the same source.

## 1. MP4 (works on any CMS)  ← recommended
`ccu-signage-1080x1920.mp4` — 1080×1920, 30 fps, ~71 s, ~12 MB.
Upload it and set the playlist item to **loop**. No network or browser
needed on the screen.

## 2. Live web page (only if your CMS has a URL / web zone)
`index.html` advances itself and loops forever. Point the zone at it and it
picks up product/price changes automatically — no re-export.
`?s=N` renders a single slide (used by the build script).

## Rebuilding after products change
    python3 scripts/build-signage.py            # HTML only
    python3 scripts/build-signage.py --video    # HTML + MP4 (needs ffmpeg)

Prices and captions are read from `assets/js/shop.js` and `gallery.html`, so
the board can't drift from the site.

## Running order (~71 s)
1. Brand open
2. "Made for High Achievers"
3–5. All 9 H.A.E.C products with prices
6. "15,000+ brands served"
7–14. Eight gallery pieces
15. QR → ccucustom.com/shop.html

## Notes
- QR target is set by `SITE_URL` in `scripts/build-signage.py`.
- **Test-scan the QR with a phone before the event.**
- Slide timings: `HOLD_*` constants at the top of the build script.
