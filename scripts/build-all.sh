#!/usr/bin/env bash
# Rebuild the whole MARQUE site in the correct order.
# Run from anywhere: bash scripts/build-all.sh
set -e
cd "$(dirname "$0")/.."

echo "→ service pages";      python3 scripts/build-services.py >/dev/null
echo "→ top-level pages";    python3 scripts/build-pages.py    >/dev/null
echo "→ blog";               python3 scripts/build-blog.py     >/dev/null
echo "→ sitemap + robots";   python3 scripts/build-sitemap.py
echo "→ apply images";       python3 scripts/apply-images.py
echo "→ tools menu";         python3 scripts/add-tools-nav.py

echo "✓ build complete"
