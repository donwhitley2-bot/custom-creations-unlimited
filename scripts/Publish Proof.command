#!/bin/bash
# Double-click to publish the proof you just built in Mockup Studio.
# Works from any Mac that has this repo cloned — it locates the project from
# its own location, so no path is hard-coded. Safe to alias onto the Desktop.

SRC="${BASH_SOURCE[0]}"
while [ -L "$SRC" ]; do                       # follow a Desktop alias/symlink
  DIR="$(cd -P "$(dirname "$SRC")" && pwd)"
  SRC="$(readlink "$SRC")"
  [[ $SRC != /* ]] && SRC="$DIR/$SRC"
done
ROOT="$(cd -P "$(dirname "$SRC")/.." && pwd)"

if [ ! -f "$ROOT/scripts/publish-proof.py" ]; then
  echo "Couldn't find the project folder from $ROOT"
  echo "Run this copy of the file that lives inside the repo."
  read -n1 -r -p "Press any key to close."; exit 1
fi

cd "$ROOT" || exit 1
echo "Publishing proof…"; echo
python3 scripts/publish-proof.py "$@"
echo
read -n1 -r -p "Press any key to close."
