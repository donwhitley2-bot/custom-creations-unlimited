#!/bin/bash
# Double-click this to publish the proof you just built in Mockup Studio.
# Keep it on your Desktop (or make an alias there) — it always uses the newest
# proof in ~/Downloads. You can also drag a specific proof file onto it.
cd "/Users/donwhitley/Documents/Website_New" || { echo "Project folder not found."; read -n1; exit 1; }
echo "Publishing proof…"
echo
python3 scripts/publish-proof.py "$@"
echo
echo "Press any key to close."
read -n1
