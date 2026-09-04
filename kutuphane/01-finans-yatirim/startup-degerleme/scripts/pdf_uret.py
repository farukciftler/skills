#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf_uret.py — Rapor icerigini Abdullah Faruk Ciftler kimligiyle A4 PDF'e cevirir.

Palet ve tipografi abdullahfarukcom deposundan aliniyor (src/styles/global.css),
Newsreader Variable dosyalari PDF'e gomuluyor; sonuc her makinede ayni goruntuyu verir.

Kullanim:
    python3 pdf_uret.py --icerik uniboom-icerik.html --cikti raporlar/Uniboom.pdf

--icerik dosyasi yalnizca <section> bloklari ve kapak div'i icerir, <html>/<head> yazma.
Kapak ve sinif adlari icin assets/rapor-iskelet.html dosyasina bak.
Yazim kurallari (tire yasagi dahil) references/yazim-kurallari.md icinde.
"""
import base64, pathlib, subprocess, sys

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--icerik", required=True, help="Icerik HTML dosyasi (section blokları)")
ap.add_argument("--cikti", required=True, help="Uretilecek PDF yolu")
ap.add_argument("--baslik", default="Rapor", help="PDF meta basligi")
ap.add_argument("--fontlar", default="/Users/farukciftler/projects/abdullahfarukcom/"
                "node_modules/@fontsource-variable/newsreader/files",
                help="Newsreader woff2 dizini")
A = ap.parse_args()

FONTS = pathlib.Path(A.fontlar)
if not FONTS.exists():
    sys.exit(f"Font dizini yok: {FONTS}\nabdullahfarukcom deposunda 'npm install' calistir.")
ICERIK = pathlib.Path(A.icerik).resolve()
CIKTI = pathlib.Path(A.cikti).resolve()


def b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()


faces = ""
for subset, rng in [
    ("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
              "U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"),
    ("latin-ext", "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,"
                  "U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,"
                  "U+2113,U+2C60-2C7F,U+A720-A7FF"),
]:
    for style, f in [("normal", f"newsreader-{subset}-wght-normal.woff2"),
                     ("italic", f"newsreader-{subset}-wght-italic.woff2")]:
        faces += (f"@font-face{{font-family:'Newsreader';font-style:{style};font-weight:200 800;"
                  f"font-display:block;src:url(data:font/woff2;base64,{b64(f)}) format('woff2-variations');"
                  f"unicode-range:{rng};}}\n")

body = ICERIK.read_text(encoding="utf-8")

for kotu, iyi in (("\u2014", "tire"), ("\u2013", "tire"), (" - ", "tire")):
    if kotu in body:
        sys.exit(f"Icerikte {iyi} var: {kotu!r}. references/yazim-kurallari.md")

html = f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><title>{A.baslik}</title>
<style>
{faces}
:root{{
  --paper:#fdfcfa; --paper-2:#f5f2ec; --ink:#1a1917; --ink-2:#4a4740; --ink-3:#78736a;
  --rule:#e4dfd5; --rule-2:#d5cfc2; --accent:#b3541e; --accent-2:#8f4218; --accent-bg:#f6ece3;
  --serif:'Newsreader', Georgia, serif;
}}
@page{{ size:A4; margin:19mm 20mm 17mm; }}
@page:first{{ margin:0; }}
*{{box-sizing:border-box;margin:0;}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
body{{
  background:var(--paper); color:var(--ink); font-family:var(--serif);
  font-size:9.6pt; line-height:1.55; font-weight:390;
  font-variant-numeric:proportional-nums lining-nums;
}}
p{{margin:0 0 .62em;text-align:justify;hyphens:auto;orphans:3;widows:3;
   overflow-wrap:break-word;}}
li{{orphans:2;widows:2;}}
h1,h2,h3{{font-weight:560;line-height:1.2;letter-spacing:-.011em;}}
strong{{font-weight:640;}}
em{{font-style:italic;color:var(--ink-2);}}

/* Kapak */
.cover{{
  height:297mm; padding:26mm 24mm 20mm; display:flex; flex-direction:column;
  background:var(--paper); page-break-after:always; position:relative;
}}
.cover__brand{{
  font-size:11.5pt; font-weight:620; letter-spacing:-.01em; color:var(--ink);
}}
.cover__brandsub{{
  font-size:7.6pt; letter-spacing:.11em; text-transform:uppercase; color:var(--ink-3);
  margin-top:.35em;
}}
.cover__rule{{height:2px;background:var(--accent);width:44mm;margin:9mm 0 0;}}
.cover__mid{{margin-top:auto;}}
.cover__kicker{{
  font-size:7.8pt; letter-spacing:.15em; text-transform:uppercase; color:var(--accent-2);
  margin-bottom:5mm;
}}
.cover__title{{font-size:34pt;line-height:1.05;letter-spacing:-.022em;font-weight:520;}}
.cover__sub{{font-size:12.5pt;color:var(--ink-2);margin-top:3.5mm;line-height:1.4;}}
.cover__legal{{font-size:8.6pt;color:var(--ink-3);margin-top:2.5mm;letter-spacing:.01em;}}
.cover__meta{{
  margin-top:14mm; border-top:1px solid var(--rule-2); padding-top:5mm;
  display:grid; grid-template-columns:repeat(3,1fr); gap:6mm; font-size:8.4pt;
}}
.cover__meta dt{{
  font-size:7.2pt;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-bottom:1.2mm;
}}
.cover__meta dd{{margin:0;color:var(--ink);}}
.cover__foot{{
  margin-top:auto;padding-top:8mm;border-top:1px solid var(--rule);
  display:flex;justify-content:space-between;font-size:7.8pt;color:var(--ink-3);
}}
.cover__headline{{
  margin-top:9mm;background:var(--accent-bg);border-left:2px solid var(--accent);
  padding:5mm 6mm;
}}
.cover__headline .lab{{font-size:7.2pt;letter-spacing:.1em;text-transform:uppercase;color:var(--accent-2);}}
.cover__headline .val{{font-size:19pt;font-weight:560;letter-spacing:-.02em;margin-top:1.5mm;}}
.cover__headline .note{{font-size:8.2pt;color:var(--ink-2);margin-top:1.5mm;}}

/* Icerik */
/* Bolumler dogal aksin. Zorunlu sayfa sonu yalnizca .pagebreak ile,
   ve o da sadece gercekten gerekliyse: yoksa sayfalar yariya kadar bos kalir. */
section{{break-inside:auto;}}
h2{{
  font-size:14pt;margin:9mm 0 3mm;padding-bottom:2mm;border-bottom:1px solid var(--rule-2);
  break-after:avoid;break-inside:avoid;
}}
h2 .num{{color:var(--accent);font-weight:560;margin-right:.5em;}}
h2:first-of-type{{margin-top:0;}}
h3{{font-size:10.4pt;margin:5mm 0 1.8mm;color:var(--ink);break-after:avoid;break-inside:avoid;}}

/* Uzun tablo sayfaya sigmiyorsa bolunsun ama satir ortadan kesilmesin ve
   yeni sayfada basligi tekrarlansin. Tabloyu butun halde tutmaya calismak
   sayfalarin yarisini bos birakiyor. */
table{{
  width:100%;border-collapse:collapse;margin:3mm 0 4mm;font-size:8.5pt;
  break-inside:auto;
}}
thead{{display:table-header-group;}}
/* Kisa ve butunluk isteyen tablolara class="tight" ver: iki sayfaya bolununce
   ikinci sayfada baslik ve tek satir kalir, kotu gorunur. */
table.tight{{break-inside:avoid;}}
tr{{break-inside:avoid;break-after:auto;}}
th{{
  text-align:left;font-weight:600;font-size:7.4pt;letter-spacing:.07em;text-transform:uppercase;
  color:var(--ink-3);border-bottom:1px solid var(--rule-2);padding:1.6mm 2.4mm 1.6mm 0;
}}
td{{padding:1.7mm 2.4mm 1.7mm 0;border-bottom:1px solid var(--rule);vertical-align:top;
    overflow-wrap:break-word;}}
tr:last-child td{{border-bottom:1px solid var(--rule-2);}}
td.num,th.num{{text-align:right;padding-left:5mm;white-space:nowrap;}}
/* Son sutun sayfa kenarina yapismasin: sifir bosluk 'icerik kesilmis' hissi veriyor. */
td.num:last-child,th.num:last-child{{padding-right:1.6mm;}}
td:last-child,th:last-child{{padding-right:1.6mm;}}
td.num:not(:last-child),th.num:not(:last-child){{padding-right:4mm;}}
td:not(.num)+td:not(.num){{padding-left:0;}}
tr.total td{{font-weight:620;background:var(--paper-2);border-bottom:1px solid var(--rule-2);}}
tr.self td{{background:var(--accent-bg);font-weight:600;}}

ul,ol{{margin:0 0 .7em;padding-left:4.5mm;}}
li{{margin-bottom:.42em;text-align:justify;}}
li::marker{{color:var(--accent);}}

.callout{{
  background:var(--paper-2);border-left:2px solid var(--accent);padding:3.6mm 4.5mm;
  margin:3.5mm 0;font-size:9pt;break-inside:avoid;
}}
.callout p:last-child{{margin-bottom:0;}}
.quote{{
  font-style:italic;color:var(--ink-2);border-left:1px solid var(--rule-2);
  padding-left:4mm;margin:2.5mm 0;font-size:8.8pt;
}}
.quote span{{display:block;font-style:normal;font-size:7.6pt;color:var(--ink-3);margin-top:1mm;}}
.tag{{
  display:inline-block;font-size:6.6pt;letter-spacing:.06em;padding:.1em .38em;
  border:1px solid var(--rule-2);color:var(--ink-3);border-radius:2px;vertical-align:.12em;
  line-height:1.25;
}}
.tag.d{{color:var(--accent-2);border-color:var(--accent);background:var(--accent-bg);}}
.lead{{font-size:10.4pt;color:var(--ink-2);line-height:1.55;}}
.small{{font-size:7.8pt;color:var(--ink-3);line-height:1.5;}}
.small a{{color:var(--ink-3);}}
.kpi{{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin:4mm 0 5mm;break-inside:avoid;}}
.kpi div{{border-top:2px solid var(--accent);padding-top:2.5mm;}}
.kpi .lab{{font-size:7pt;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);}}
.kpi .val{{font-size:15pt;font-weight:560;letter-spacing:-.02em;margin-top:1mm;}}
.kpi .sub{{font-size:7.6pt;color:var(--ink-3);margin-top:.8mm;}}
.pagebreak{{break-before:page;}}
a{{color:inherit;text-decoration:none;}}
</style></head><body>
{body}
</body></html>"""

CIKTI.parent.mkdir(parents=True, exist_ok=True)
ara = CIKTI.with_suffix(".html")
ara.write_text(html, encoding="utf-8")

pdf = CIKTI
subprocess.run([
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--disable-gpu", "--no-pdf-header-footer",
    "--virtual-time-budget=8000",
    f"--print-to-pdf={pdf}", ara.as_uri(),
], check=True, capture_output=True)
print(f"PDF: {pdf} ({pdf.stat().st_size/1024:.0f} KB)")
