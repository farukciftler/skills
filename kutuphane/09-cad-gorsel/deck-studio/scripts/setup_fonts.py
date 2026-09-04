#!/usr/bin/env python3
"""Install real typefaces into the sandbox so LibreOffice, Chromium and sharp
can all render them, and so they can be embedded into the .pptx.

    python scripts/setup_fonts.py --list
    python scripts/setup_fonts.py inter fraunces jetbrains-mono
    python scripts/setup_fonts.py --check "Space Grotesk"

Fonts come from the google/fonts GitHub mirror (raw.githubusercontent.com is
reachable from the sandbox; fonts.googleapis.com is not). Everything here is
OFL/Apache licensed, which permits both installation and .pptx embedding.
"""
import argparse
import os
import subprocess
import sys
import urllib.parse
import urllib.request

FONT_DIR = os.path.expanduser("~/.fonts")
BASE = "https://raw.githubusercontent.com/google/fonts/main"

# key -> (family name as it must be written into the deck, repo path)
CATALOG = {
    # --- grotesque / neo-grotesque workhorses ---
    "inter":              ("Inter",               "ofl/inter/Inter[opsz,wght].ttf"),
    "public-sans":        ("Public Sans",         "ofl/publicsans/PublicSans[wght].ttf"),
    "work-sans":          ("Work Sans",           "ofl/worksans/WorkSans[wght].ttf"),
    "figtree":            ("Figtree",             "ofl/figtree/Figtree[wght].ttf"),
    "schibsted-grotesk":  ("Schibsted Grotesk",   "ofl/schibstedgrotesk/SchibstedGrotesk[wght].ttf"),
    "instrument-sans":    ("Instrument Sans",     "ofl/instrumentsans/InstrumentSans[wdth,wght].ttf"),
    # --- characterful sans (display + UI) ---
    "space-grotesk":      ("Space Grotesk",       "ofl/spacegrotesk/SpaceGrotesk[wght].ttf"),
    "bricolage":          ("Bricolage Grotesque", "ofl/bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf"),
    "archivo":            ("Archivo",             "ofl/archivo/Archivo[wdth,wght].ttf"),
    "epilogue":           ("Epilogue",            "ofl/epilogue/Epilogue[wght].ttf"),
    "outfit":             ("Outfit",              "ofl/outfit/Outfit[wght].ttf"),
    "manrope":            ("Manrope",             "ofl/manrope/Manrope[wght].ttf"),
    "gabarito":           ("Gabarito",            "ofl/gabarito/Gabarito[wght].ttf"),
    "geologica":          ("Geologica",           "ofl/geologica/Geologica[CRSV,SHRP,slnt,wght].ttf"),
    "dm-sans":            ("DM Sans",             "ofl/dmsans/DMSans[opsz,wght].ttf"),
    "syne":               ("Syne",                "ofl/syne/Syne[wght].ttf"),
    "unbounded":          ("Unbounded",           "ofl/unbounded/Unbounded[wght].ttf"),
    # --- serifs: text ---
    "source-serif":       ("Source Serif 4",      "ofl/sourceserif4/SourceSerif4[opsz,wght].ttf"),
    "literata":           ("Literata",            "ofl/literata/Literata[opsz,wght].ttf"),
    "newsreader":         ("Newsreader",          "ofl/newsreader/Newsreader[opsz,wght].ttf"),
    "lora":               ("Lora",                "ofl/lora/Lora[wght].ttf"),
    "crimson-pro":        ("Crimson Pro",         "ofl/crimsonpro/CrimsonPro[wght].ttf"),
    "eb-garamond":        ("EB Garamond",         "ofl/ebgaramond/EBGaramond[wght].ttf"),
    # --- serifs: display ---
    "fraunces":           ("Fraunces",            "ofl/fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf"),
    "playfair":           ("Playfair Display",    "ofl/playfairdisplay/PlayfairDisplay[wght].ttf"),
    "instrument-serif":   ("Instrument Serif",    "ofl/instrumentserif/InstrumentSerif-Regular.ttf"),
    "dm-serif-display":   ("DM Serif Display",    "ofl/dmserifdisplay/DMSerifDisplay-Regular.ttf"),
    # --- condensed / poster ---
    "anton":              ("Anton",               "ofl/anton/Anton-Regular.ttf"),
    "bebas-neue":         ("Bebas Neue",          "ofl/bebasneue/BebasNeue-Regular.ttf"),
    # --- mono ---
    "jetbrains-mono":     ("JetBrains Mono",      "ofl/jetbrainsmono/JetBrainsMono[wght].ttf"),
    "space-mono":         ("Space Mono",          "ofl/spacemono/SpaceMono-Regular.ttf"),
}

# Characters a Turkish-language deck must render. If a face is missing any of
# these the deck will show tofu or, worse, silently substitute mid-headline.
TR_PROBE = "ıİğĞşŞçÇöÖüÜ"


def install(key: str) -> str:
    if key not in CATALOG:
        sys.exit(f"unknown font key '{key}'. Run --list to see the catalog.")
    family, path = CATALOG[key]
    os.makedirs(FONT_DIR, exist_ok=True)
    dest = os.path.join(FONT_DIR, os.path.basename(path))
    if not os.path.exists(dest):
        url = BASE + "/" + urllib.parse.quote(path)
        with urllib.request.urlopen(url, timeout=60) as r, open(dest, "wb") as f:
            f.write(r.read())
    return dest


def coverage(dest: str) -> list:
    """Return the probe characters this font file has no glyph for."""
    from fontTools.ttLib import TTFont
    font = TTFont(dest, fontNumber=0, lazy=True)
    cmap = set()
    for table in font["cmap"].tables:
        cmap.update(table.cmap.keys())
    font.close()
    return [c for c in TR_PROBE if ord(c) not in cmap]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fonts", nargs="*", help="catalog keys to install")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--check", metavar="FAMILY", help="verify a family is visible to fontconfig")
    a = ap.parse_args()

    if a.list:
        for k, (fam, _) in CATALOG.items():
            print(f"{k:20} {fam}")
        return

    if a.check:
        out = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout
        found = any(a.check.lower() in line.lower() for line in out.splitlines())
        print(("OK   " if found else "MISS ") + a.check)
        sys.exit(0 if found else 1)

    if not a.fonts:
        sys.exit("nothing to install; pass catalog keys or --list")

    for key in a.fonts:
        dest = install(key)
        missing = coverage(dest)
        family = CATALOG[key][0]
        note = "" if not missing else f"  !! NO TURKISH GLYPHS FOR: {''.join(missing)}"
        print(f"installed  {family:22} {os.path.basename(dest)}{note}")

    subprocess.run(["fc-cache", "-f"], capture_output=True)
    print(f"\nfontconfig refreshed. Write these exact family names into the deck.")
    print("Embed them with scripts/embed_fonts.py or the reader sees a substitute.")


if __name__ == "__main__":
    main()
