#!/usr/bin/env python3
"""
Publish a proof page built in Mockup Studio.

    python3 scripts/publish-proof.py ~/Downloads/1042-a7f3c9.html

Moves it into proof/, commits, pushes, and prints the live URL. The mockup is
embedded in the file, so there is nothing else to upload.
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SITE = "https://www.ccucustom.com"


def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: publish-proof.py <downloaded-proof.html>")
    src = os.path.expanduser(sys.argv[1])
    if not os.path.exists(src):
        sys.exit("not found: " + src)
    name = os.path.basename(src)
    if not name.endswith(".html"):
        sys.exit("expected an .html file from Mockup Studio")

    os.makedirs(os.path.join(ROOT, "proof"), exist_ok=True)
    dest = os.path.join(ROOT, "proof", name)
    shutil.move(src, dest)
    size = os.path.getsize(dest) / 1e6
    print(f"moved   proof/{name}  ({size:.1f} MB)")

    run("git", "add", "proof/" + name)
    c = run("git", "commit", "-m", "Add proof " + name)
    if c.returncode and "nothing to commit" not in (c.stdout + c.stderr):
        sys.exit("commit failed:\n" + c.stdout + c.stderr)
    p = run("git", "push")
    if p.returncode:
        sys.exit("push failed:\n" + p.stdout + p.stderr)

    url = f"{SITE}/proof/{name}"
    print("pushed  live in a few minutes")
    print("\n  " + url + "\n")
    try:
        subprocess.run(["pbcopy"], input=url, text=True)
        print("(URL copied to your clipboard)")
    except Exception:
        pass


if __name__ == "__main__":
    main()
