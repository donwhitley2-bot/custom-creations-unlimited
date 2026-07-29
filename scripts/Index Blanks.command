#!/bin/bash
# Double-click after adding or removing garment photos in tools/blanks/.
# Rebuilds the index Mockup Studio reads. Works on any Mac with this repo.

SRC="${BASH_SOURCE[0]}"
while [ -L "$SRC" ]; do
  DIR="$(cd -P "$(dirname "$SRC")" && pwd)"
  SRC="$(readlink "$SRC")"
  [[ $SRC != /* ]] && SRC="$DIR/$SRC"
done
ROOT="$(cd -P "$(dirname "$SRC")/.." && pwd)"

if [ ! -f "$ROOT/scripts/build-blanks.py" ]; then
  echo "Couldn't find the project from $ROOT"
  read -n1 -r -p "Press any key to close."; exit 1
fi

cd "$ROOT" || exit 1
echo "Indexing garment blanks…"; echo
python3 scripts/build-blanks.py
echo
echo "Now commit + push so the blanks appear on the live site:"
read -n1 -r -p "  press any key to do that, or close this window to skip."
echo
git add tools/blanks >/dev/null 2>&1
git commit -m "Update garment blanks" >/dev/null 2>&1 && git push && echo "pushed." || echo "nothing new to push."
echo
read -n1 -r -p "Press any key to close."
