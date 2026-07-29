#!/usr/bin/env python3
"""
Index the garment blanks in tools/blanks/ for Mockup Studio.

A static page can't list a directory, so this writes tools/blanks/blanks.json
from whatever images are in the folder. Run it after adding or removing blanks:

    python3 scripts/build-blanks.py

Naming: the filename becomes the label. Use "<style> <color>.jpg", e.g.
    bella-3001 white.jpg     -> "Bella 3001 · White"
    bella-3719 hoodie black.jpg -> "Bella 3719 Hoodie · Black"
Anything is accepted; tidy names just read better in the picker.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DIR = os.path.join(ROOT, "tools", "blanks")
EXT = (".jpg", ".jpeg", ".png", ".webp")

# Trailing resolution/qualifier tokens suppliers append, e.g. "..._Front_High"
QUALIFIERS = {"high", "med", "medium", "low", "hi", "lg", "sm", "large", "small"}
VIEWS = {"front": "Front", "back": "Back", "side": "Side",
         "flat": "Flat", "detail": "Detail", "model": "Model"}
STYLE_RE = re.compile(r"^[0-9]{3,5}[A-Za-z]{0,3}$")


def parse(stem):
    """Split a supplier filename into vendor / style / colour / view.

    Handles the S&S export shape, e.g.
        BELLA_+_CANVAS_3001_Baby_Blue_Front_High -> Bella + Canvas / 3001 /
        Baby Blue / Front
    and degrades gracefully to "whatever the filename said" for other naming.
    """
    tok = [t for t in re.split(r"[-_ ]+", stem.strip()) if t]
    while tok and tok[-1].lower() in QUALIFIERS:
        tok.pop()

    view = ""
    for i, t in enumerate(tok):
        if t.lower() in VIEWS:
            view = VIEWS[t.lower()]
            tok.pop(i)
            break

    si = next((i for i, t in enumerate(tok) if STYLE_RE.match(t)), None)
    if si is None:
        return {"vendor": tok[0].capitalize() if tok else "Other",
                "style": "", "color": " ".join(tok[1:]).title(), "view": view}

    vendor = " ".join(t if t == "+" else t.capitalize() for t in tok[:si]) or "Other"
    return {"vendor": vendor, "style": tok[si].upper(),
            "color": " ".join(t.capitalize() for t in tok[si + 1:]), "view": view}


def main():
    os.makedirs(DIR, exist_ok=True)
    files = sorted(f for f in os.listdir(DIR)
                   if f.lower().endswith(EXT) and not f.startswith("."))
    blanks = []
    for f in files:
        p = parse(os.path.splitext(f)[0])
        label = " · ".join(x for x in (p["style"], p["color"]) if x) or f
        if p["view"] and p["view"] != "Front":
            label += f" ({p['view'].lower()})"
        blanks.append({"file": f, "label": label, **p})
    # fronts first, then colour — the order the picker shows
    blanks.sort(key=lambda b: (b["vendor"], b["style"],
                               b["view"] != "Front", b["color"]))
    out = os.path.join(DIR, "blanks.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(blanks, fh, indent=1)
    print(f"indexed {len(blanks)} blank(s) -> tools/blanks/blanks.json")
    for b in blanks:
        print(f"    {b['vendor']:<16} {b['label']}")
    if not blanks:
        print("\n   Drop garment photos into tools/blanks/ and run this again.")


if __name__ == "__main__":
    main()
