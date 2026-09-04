#!/usr/bin/env python3
"""Embed typefaces into a .pptx so the deck keeps its typography on a machine
that has never heard of the font.

    python scripts/embed_fonts.py deck.pptx --font "Fraunces" --font "Inter"
    python scripts/embed_fonts.py deck.pptx --font "Inter" --out deck-embedded.pptx

Without this, a deck set in Fraunces opens in Calibri on the client's laptop and
every line length you QA'd is wrong. Fonts are resolved from ~/.fonts (install
them first with setup_fonts.py).

Variable fonts are the catch: PowerPoint reads a variable TTF at its default
instance only, so a 700-weight headline renders at 400 with a fake-bold smear.
This script therefore snaps each variable font to static Regular (400) and Bold
(700) instances with fontTools before embedding, which is what PowerPoint wants.

Two things to tell the recipient:
  - PowerPoint for macOS ignores embedded fonts. Mac reviewers see substitutes;
    send them the PDF instead.
  - Only embed fonts whose licence allows it. Everything in setup_fonts.py's
    catalogue is OFL or Apache, which does.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

FONT_DIR = os.path.expanduser("~/.fonts")
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_FONT = NS_R + "/font"


def find_font_file(family: str) -> str:
    """Locate the installed .ttf for a family name via fontconfig."""
    out = subprocess.run(["fc-match", "-f", "%{file}", family],
                         capture_output=True, text=True).stdout.strip()
    if out and os.path.exists(out):
        # fc-match always returns *something*; make sure it is really this family
        fam = subprocess.run(["fc-match", "-f", "%{family}", family],
                             capture_output=True, text=True).stdout
        if family.lower() in fam.lower():
            return out
    hits = glob.glob(os.path.join(FONT_DIR, "*.ttf"))
    key = family.replace(" ", "").lower()
    for h in hits:
        if os.path.basename(h).replace(" ", "").lower().startswith(key):
            return h
    sys.exit(f"'{family}' is not installed. Run: python scripts/setup_fonts.py --list")


def static_instances(path: str, workdir: str, family: str):
    """Return [(style, ttf_path)] — static Regular/Bold cuts of a variable font."""
    from fontTools.ttLib import TTFont
    font = TTFont(path, lazy=True)
    is_variable = "fvar" in font
    axes = {a.axisTag: (a.minValue, a.maxValue) for a in font["fvar"].axes} if is_variable else {}
    font.close()

    if not is_variable or "wght" not in axes:
        return [("regular", path)]

    from fontTools.varLib import instancer
    lo, hi = axes["wght"]
    out = []
    for style, wght in (("regular", 400), ("bold", 700)):
        w = min(max(wght, lo), hi)
        dest = os.path.join(workdir, f"{family.replace(' ', '')}-{style}.ttf")
        f = TTFont(path)
        instancer.instantiateVariableFont(f, {"wght": w}, inplace=True, updateFontNames=False)
        f.save(dest)
        f.close()
        out.append((style, dest))
    return out


def embed(pptx_path: str, families: list, out_path: str):
    tmp = tempfile.mkdtemp()
    unpacked = os.path.join(tmp, "unpacked")
    with zipfile.ZipFile(pptx_path) as z:
        z.extractall(unpacked)

    fonts_dir = os.path.join(unpacked, "ppt", "fonts")
    os.makedirs(fonts_dir, exist_ok=True)

    pres_path = os.path.join(unpacked, "ppt", "presentation.xml")
    rels_path = os.path.join(unpacked, "ppt", "_rels", "presentation.xml.rels")
    ct_path = os.path.join(unpacked, "[Content_Types].xml")
    pres = open(pres_path, encoding="utf-8").read()
    rels = open(rels_path, encoding="utf-8").read()
    ct = open(ct_path, encoding="utf-8").read()

    used = [int(m) for m in re.findall(r'Id="rId(\d+)"', rels)]
    next_id = max(used) + 1 if used else 1
    n_font = len(glob.glob(os.path.join(fonts_dir, "*.fntdata"))) + 1

    entries = []
    for family in families:
        src = find_font_file(family)
        cuts = static_instances(src, tmp, family)
        parts = []
        for style, ttf in cuts:
            name = f"font{n_font}.fntdata"
            shutil.copy(ttf, os.path.join(fonts_dir, name))
            rid = f"rId{next_id}"
            rels = rels.replace(
                "</Relationships>",
                f'<Relationship Id="{rid}" Type="{REL_FONT}" Target="fonts/{name}"/></Relationships>')
            parts.append(f'<p:{style} r:id="{rid}"/>')
            next_id += 1
            n_font += 1
        entries.append(f'<p:embeddedFont><p:font typeface="{family}" pitchFamily="34" '
                       f'charset="0"/>{"".join(parts)}</p:embeddedFont>')
        print(f"embedded {family}  ({', '.join(s for s, _ in cuts)})")

    block = "<p:embeddedFontLst>" + "".join(entries) + "</p:embeddedFontLst>"

    # Schema order: embeddedFontLst sits after notesSz and before defaultTextStyle.
    # Insert without touching any existing child — reordering <p:presentation>
    # is what makes PowerPoint refuse the file.
    if "<p:embeddedFontLst>" in pres:
        pres = pres.replace("<p:embeddedFontLst>", block[:-len("</p:embeddedFontLst>")]
                            .replace("<p:embeddedFontLst>", "<p:embeddedFontLst>"), 1)
    elif "<p:defaultTextStyle>" in pres:
        pres = pres.replace("<p:defaultTextStyle>", block + "<p:defaultTextStyle>", 1)
    else:
        pres = pres.replace("</p:presentation>", block + "</p:presentation>", 1)

    if "embedTrueTypeFonts" not in pres:
        pres = re.sub(r"(<p:presentation\b[^>]*?)(\s*>)", r'\1 embedTrueTypeFonts="1"\2',
                      pres, count=1)

    if 'Extension="fntdata"' not in ct:
        ct = ct.replace("<Default", '<Default Extension="fntdata" '
                        'ContentType="application/x-fontdata"/><Default', 1)

    open(pres_path, "w", encoding="utf-8").write(pres)
    open(rels_path, "w", encoding="utf-8").write(rels)
    open(ct_path, "w", encoding="utf-8").write(ct)

    if os.path.exists(out_path):
        os.remove(out_path)
    out_abs = os.path.abspath(out_path)
    subprocess.run(["zip", "-Xr", out_abs, "."], cwd=unpacked,
                   check=True, capture_output=True)
    shutil.rmtree(tmp)
    size = os.path.getsize(out_abs) / 1e6
    print(f"\nwrote {out_path}  ({size:.1f} MB)")
    print("Now run the pptx skill's validate.py on it before shipping.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--font", action="append", required=True, dest="fonts",
                    help="family name exactly as written in the deck; repeatable")
    ap.add_argument("--out", help="defaults to overwriting the input")
    a = ap.parse_args()
    embed(a.pptx, a.fonts, a.out or a.pptx)


if __name__ == "__main__":
    main()
