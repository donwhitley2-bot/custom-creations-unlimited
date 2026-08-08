#!/usr/bin/env python3
"""
Turn the raw photos of real jobs into a matched set for the gallery.

    python3 scripts/prep-work-photos.py            -> assets/img/work-*.webp
    python3 scripts/prep-work-photos.py --preview  -> preview/img-work/ instead

The three sources don't match each other: two are studio renders on black, one
is a phone photo of a lit bench under tungsten light. Dropped into the gallery
raw they read as three different sources, so each gets neutralised, darkened to
a common backdrop and vignetted.

The arrowhead award also carries a recipient's name engraved into the pixels.
retouch_name() rebuilds the panel behind it and sets a generic name, so the
piece can go in a public portfolio. Change NEW_NAME and re-run.
"""
import argparse, os, random, statistics, sys
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DL = os.path.expanduser("~/Downloads")

LONG_EDGE = 1400
NEW_NAME = "SARAH MITCHELL"
SERIF = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"

# The engraved name's true box, measured inside the dark panel only. The
# crystal's bevelled edges are bright and read as text if you scan the full
# width, which throws off both the patch and the replacement font size.
NAME_BOX = (363, 764, 641, 678)

# src, output stem, target aspect (w/h), white-balance amount, darken gamma
JOBS = [
    (os.path.join(DL, "Award.PNG"),         "work-award-arrowhead", 0.80, 0.0, 1.00),
    (os.path.join(DL, "crystal.PNG"),       "work-crystal-cube",    1.00, 0.0, 1.00),
    (os.path.join(DL, "SubsurfaceJPG.JPG"), "work-crystal-knight",  0.80, 1.0, 1.45),
]


def retouch_name(im):
    """Replace the engraved recipient name."""
    X0, X1, Y0, Y1 = NAME_BOX
    cx, cy, cap = (X0 + X1) // 2, (Y0 + Y1) // 2, Y1 - Y0
    orig = im.copy()
    px, op = im.load(), orig.load()
    random.seed(7)

    pad = 16
    bx0, bx1, by0, by1 = X0 - pad, X1 + pad, Y0 - pad, Y1 + pad
    # Rebuild each row from clean pixels on that same row, just outside the
    # text. Cloning a block from elsewhere drags the gold divider into frame.
    for y in range(by0, by1 + 1):
        lc = tuple(statistics.median([op[bx0 - 8 - i, y][c] for i in range(14)]) for c in range(3))
        rc = tuple(statistics.median([op[bx1 + 8 + i, y][c] for i in range(14)]) for c in range(3))
        span = bx1 - bx0
        for x in range(bx0, bx1 + 1):
            t = (x - bx0) / span
            n = random.randint(-2, 2)          # grain, so it isn't glassy-flat
            px[x, y] = tuple(max(0, min(255, int(lc[c] + (rc[c] - lc[c]) * t) + n))
                             for c in range(3))

    blend = Image.new("L", im.size, 0)
    ImageDraw.Draw(blend).rectangle([bx0, by0, bx1, by1], fill=255)
    im = Image.composite(im, orig, blend.filter(ImageFilter.GaussianBlur(7)))

    size = 10
    while size < 200:                          # match the original cap height
        if ImageFont.truetype(SERIF, size).getbbox("H")[3] - \
           ImageFont.truetype(SERIF, size).getbbox("H")[1] >= cap:
            break
        size += 1
    f = ImageFont.truetype(SERIF, size)
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), NEW_NAME, font=f)
    if bb[2] - bb[0] > 410:                    # never wider than the original line
        size = int(size * 410 / (bb[2] - bb[0]))
        f = ImageFont.truetype(SERIF, size)
        bb = d.textbbox((0, 0), NEW_NAME, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    tx, ty = cx - tw // 2 - bb[0], cy - th // 2 - bb[1]
    d.text((tx + 2, ty + 2), NEW_NAME, font=f, fill=(36, 36, 40))
    d.text((tx, ty), NEW_NAME, font=f, fill=(243, 243, 239))
    return im


def gray_world(im, amount):
    """Neutralise a colour cast. 0 leaves it alone, 1 corrects fully."""
    if amount <= 0:
        return im
    chans = im.split()
    means = [c.resize((1, 1), Image.BOX).getpixel((0, 0)) for c in chans]
    target = sum(means) / 3
    out = []
    for ch, m in zip(chans, means):
        s = 1.0 if m == 0 else target / m
        s = max(0.65, min(1.5, 1 + (s - 1) * amount))
        out.append(ch.point(lambda v, s=s: max(0, min(255, int(v * s)))))
    return Image.merge("RGB", out)


def darken_background(im, gamma):
    """Pull mids and lows down so a lit bench reads as a dark backdrop, while
    the crystal keeps its highlights."""
    if gamma <= 1.0:
        return im
    return im.point([min(255, int(255 * ((v / 255) ** gamma))) for v in range(256)] * 3)


def vignette(im, strength=0.30):
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([-w * .22, -h * .22, w * 1.22, h * 1.22], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.10))
    return Image.composite(im, Image.blend(im, Image.new("RGB", (w, h), (0, 0, 0)), strength), mask)


def crop_aspect(im, aspect):
    w, h = im.size
    if abs(w / h - aspect) < 0.01:
        return im
    if w / h > aspect:
        nw = int(h * aspect)
        return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = int(w / aspect)
    y = int((h - nh) * 0.45)                   # bias up: the piece sits high
    return im.crop((0, y, w, y + nh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true",
                    help="write to preview/img-work/ instead of assets/img/")
    a = ap.parse_args()
    out = os.path.join(ROOT, "preview", "img-work") if a.preview else os.path.join(ROOT, "assets", "img")
    os.makedirs(out, exist_ok=True)

    for src, name, aspect, wb, gamma in JOBS:
        if not os.path.exists(src):
            print(f"  ! missing {src}", file=sys.stderr)
            continue
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        before = im.size
        if name == "work-award-arrowhead":
            im = retouch_name(im)
        im = gray_world(im, wb)
        im = darken_background(im, gamma)
        im = crop_aspect(im, aspect)
        if im.width >= im.height:
            im = im.resize((LONG_EDGE, int(LONG_EDGE / im.width * im.height)), Image.LANCZOS)
        else:
            im = im.resize((int(LONG_EDGE / im.height * im.width), LONG_EDGE), Image.LANCZOS)
        im = ImageEnhance.Contrast(vignette(im)).enhance(1.06)
        dst = os.path.join(out, name + ".webp")
        im.save(dst, "WEBP", quality=84, method=6)
        print(f"  {name}.webp   {before[0]}x{before[1]} -> {im.size[0]}x{im.size[1]}"
              f"   {os.path.getsize(dst)/1e3:.0f} KB")


if __name__ == "__main__":
    main()
