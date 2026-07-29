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

COLORS = ("white","black","navy","grey","gray","charcoal","red","royal","forest",
          "maroon","sand","natural","heather","athletic","pink","purple","olive",
          "teal","gold","orange","blue","green","tan","cream","silver","ash")


def label_for(stem):
    words = re.split(r"[-_ ]+", stem.strip())
    color = [w for w in words if w.lower() in COLORS]
    rest = [w for w in words if w.lower() not in COLORS]
    name = " ".join(w.upper() if re.fullmatch(r"\d{3,4}", w) else w.capitalize()
                    for w in rest) or stem
    return f"{name} · {' '.join(c.capitalize() for c in color)}" if color else name


def main():
    os.makedirs(DIR, exist_ok=True)
    files = sorted(f for f in os.listdir(DIR)
                   if f.lower().endswith(EXT) and not f.startswith("."))
    blanks = [{"file": f, "label": label_for(os.path.splitext(f)[0])} for f in files]
    out = os.path.join(DIR, "blanks.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(blanks, fh, indent=1)
    print(f"indexed {len(blanks)} blank(s) -> tools/blanks/blanks.json")
    for b in blanks:
        print("   ", b["label"], " (", b["file"], ")", sep="")
    if not blanks:
        print("\n   Drop garment photos into tools/blanks/ and run this again.")


if __name__ == "__main__":
    main()
