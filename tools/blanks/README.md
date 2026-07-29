# Garment blanks for Mockup Studio

Put every blank photo in **this one folder** — no subfolders. The picker groups
them by vendor automatically using the first word of the filename.

    bella-3001-white.jpg        -> Bella   ▸ 3001 · White
    bella-3001-black.jpg        -> Bella   ▸ 3001 · Black
    bella-3719-hoodie-navy.jpg  -> Bella   ▸ 3719 Hoodie · Navy
    gildan-5000-sand.jpg        -> Gildan  ▸ 5000 · Sand

After adding or removing files:

    python3 scripts/build-blanks.py

That rewrites `blanks.json`, which the Studio reads (a static page can't list
a folder on its own).

## Shooting or choosing blanks
- Straight-on, flat lay or on a hanger — angled shots fight artwork placement
- Even light, no hard shadow across the chest
- Plain background
- Same framing for every blank, so placement carries between them
- Square images work best (they're drawn into a 1000×1000 canvas)

## Print area
The first time you pick a blank, hit **Set print area on this blank** and drag a
box across the chest. The placement presets then land correctly on that garment.
It's saved in your browser, so redo it once per computer.
