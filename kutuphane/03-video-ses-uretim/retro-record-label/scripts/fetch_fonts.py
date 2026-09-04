#!/usr/bin/env python3
"""fetch_fonts — pull era-appropriate typefaces from the google/fonts repo.

A headless Linux box usually has DejaVu and nothing else, so a cover designed
around a fat 70s slab silently renders in a generic sans and every measurement
you tuned is wrong. This installs real faces before you design.

    python scripts/fetch_fonts.py --era 1970s
    python scripts/fetch_fonts.py --families "Archivo Black,Instrument Serif,Bebas Neue"
    python scripts/fetch_fonts.py --list
    python scripts/fetch_fonts.py --era 1980s --check     # report Turkish glyph coverage

Fonts land in ~/.local/share/fonts and fc-cache is refreshed, so plain
`font-family: "Archivo Black"` works in the HTML afterwards — no @font-face,
no network at render time. Files come from raw.githubusercontent.com, which
tends to stay reachable when fonts.googleapis.com is firewalled.

All families here are open licence (OFL/Apache/UFL), so they are safe on
commercial covers — but the licence file ships next to each font; check it if
the artwork will be trademarked.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

RAW = "https://raw.githubusercontent.com/google/fonts/main"
API = "https://api.github.com/repos/google/fonts/contents"
DEST = pathlib.Path.home() / ".local/share/fonts/retro"

# Era kits. Not a costume box — each family is here because it is the closest
# open substitute for what that era's art departments actually set type in.
ERAS = {
    "1950s": ["Libre Franklin", "Archivo Black", "Oswald", "Playfair Display", "Special Elite"],
    "1960s": ["Archivo Black", "Bebas Neue", "Instrument Serif", "Rye", "Cormorant Garamond"],
    "1970s": ["Righteous", "Bevan", "Abril Fatface", "Josefin Sans", "Alfa Slab One", "Poiret One"],
    "1980s": ["Orbitron", "Audiowide", "Michroma", "Bebas Neue", "Monoton", "Chakra Petch"],
    "1990s": ["Space Mono", "Archivo Narrow", "Courier Prime", "Rubik Mono One", "VT323"],
    "punk": ["Special Elite", "Anton", "Archivo Black", "Courier Prime", "Oswald"],
    "psych": ["Rye", "Sancreek", "Ewert", "Monoton", "Bungee"],
    "jazz": ["Libre Franklin", "Archivo Black", "Oswald", "Bodoni Moda", "Archivo Narrow"],
    "vapor": ["Monoton", "Orbitron", "VT323", "Press Start 2P", "Space Mono"],
}

TURKISH = "ığüşöçİĞÜŞÖÇ"


def camel(name):
    return re.sub(r"[^A-Za-z0-9]", "", name)  # keep original case: VT323, Press Start 2P


def slug(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "retro-record-label"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def candidates(family):
    c, s = camel(family), slug(family)
    names = [f"{c}-Regular.ttf", f"{c}[wght].ttf", f"{c}[opsz,wght].ttf",
             f"{c}-VariableFont_wght.ttf",
             f"{c}-Bold.ttf", f"{c}-Black.ttf",
             f"static/{c}-Regular.ttf", f"static/{c}-Bold.ttf", f"static/{c}-Black.ttf"]
    for lic in ("ofl", "apache", "ufl"):
        for n in names:
            yield f"{RAW}/{lic}/{s}/{n}", n.split("/")[-1]


def via_api(family):
    """Ask GitHub what is actually in the family directory."""
    s = slug(family)
    for lic in ("ofl", "apache", "ufl"):
        try:
            data = json.loads(get(f"{API}/{lic}/{s}"))
        except Exception:
            continue
        files = [f for f in data if isinstance(f, dict) and f.get("name", "").endswith(".ttf")]
        prefer = [f for f in files if re.search(r"(\[wght\]|-Regular|-Bold|-Black)\.ttf$", f["name"])]
        for f in (prefer or files)[:3]:
            yield f["download_url"], f["name"]
        if files:
            return


def fetch(family, dest, verbose=False):
    got = []
    for url, name in candidates(family):
        try:
            blob = get(url)
        except urllib.error.HTTPError:
            continue
        except Exception as e:
            print(f"    ! {family}: {e}")
            continue
        (dest / name).write_bytes(blob)
        got.append(name)
        if len(got) >= 2:
            break
    if not got:
        for url, name in via_api(family):
            try:
                (dest / name).write_bytes(get(url))
                got.append(name)
            except Exception:
                pass
    print(f"  {'✓' if got else '✗'} {family:22} {', '.join(got) if got else 'NOT FOUND'}")
    return got


def check_turkish(dest):
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("\n(pip install fonttools for the Turkish glyph check)")
        return
    print("\nTurkish glyph coverage (ığüşöçİĞÜŞÖÇ):")
    for f in sorted(dest.glob("*.ttf")):
        try:
            cmap = set()
            for t in TTFont(f, fontNumber=0)["cmap"].tables:
                cmap |= set(t.cmap.keys())
            missing = [ch for ch in TURKISH if ord(ch) not in cmap]
        except Exception as e:
            print(f"  ? {f.name}: {e}")
            continue
        print(f"  {'✓' if not missing else '✗'} {f.name:34} "
              f"{'full' if not missing else 'missing ' + ''.join(missing)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--era", help=f"one of: {', '.join(ERAS)}")
    ap.add_argument("--families", help="comma-separated family names")
    ap.add_argument("--dest", default=str(DEST))
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--check", action="store_true", help="report Turkish glyph coverage")
    args = ap.parse_args()

    if args.list:
        for k, v in ERAS.items():
            print(f"{k:8} {', '.join(v)}")
        return

    fams = []
    if args.era:
        if args.era not in ERAS:
            sys.exit(f"unknown era. try: {', '.join(ERAS)}")
        fams += ERAS[args.era]
    if args.families:
        fams += [f.strip() for f in args.families.split(",") if f.strip()]
    dest = pathlib.Path(args.dest).expanduser()
    dest.mkdir(parents=True, exist_ok=True)

    if fams:
        for f in dict.fromkeys(fams):
            fetch(f, dest)
        subprocess.run(["fc-cache", "-f", str(dest)], capture_output=True)
        print(f"\ninstalled to {dest} — verify with: fc-list : family | sort -u | grep -i <name>")
    if args.check or not fams:
        check_turkish(dest)


if __name__ == "__main__":
    main()
