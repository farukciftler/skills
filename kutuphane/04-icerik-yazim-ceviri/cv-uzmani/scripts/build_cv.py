#!/usr/bin/env python3
"""
build_cv.py — Master CV veri dosyasindan (YAML) parse-guvenli .docx ve .md uretir.

Tasarim kararlari (hepsi ATS ayristiricisi icin):
  - tek sutun, tablo yok, metin kutusu yok
  - iletisim bilgisi belgenin govdesinde (header/footer'da degil)
  - standart bolum basliklari, gercek liste madde isaretleri
  - hedef ulkeye gore kisisel alanlarin otomatik cikarilmasi

Kullanim:
    python3 build_cv.py cv-verisi.yaml --out ./cikti --locale intl --lang en
    python3 build_cv.py cv-verisi.yaml --locale tr --lang tr --name Ad-Soyad-CV-TR

Locale profilleri:
    intl  (varsayilan) ABD/UK/Kanada/Avustralya  -> fotograf, dogum tarihi, uyruk, askerlik YOK
    tr    Turkiye                                 -> fotograf ve dogum tarihi opsiyonel, askerlik dahil
    de    Almanya/Avusturya/Isvicre               -> fotograf ve dogum tarihi dahil
    gulf  Korfez                                  -> fotograf, dogum tarihi, uyruk, medeni hal dahil
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML gerekli:  pip install pyyaml")

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt, RGBColor
except ImportError:
    sys.exit("python-docx gerekli:  pip install python-docx")


# --- locale profilleri: hangi kisisel alan hangi pazarda yer alir --------------
LOCALES = {
    "intl": {"foto": False, "dogum": False, "uyruk": False, "medeni": False, "askerlik": False},
    "tr":   {"foto": True,  "dogum": True,  "uyruk": False, "medeni": False, "askerlik": True},
    "de":   {"foto": True,  "dogum": True,  "uyruk": True,  "medeni": False, "askerlik": False},
    "gulf": {"foto": True,  "dogum": True,  "uyruk": True,  "medeni": True,  "askerlik": False},
}

HEADINGS = {
    "tr": {
        "ozet": "Özet", "deneyim": "Deneyim", "projeler": "Projeler",
        "egitim": "Eğitim", "beceriler": "Beceriler",
        "sertifikalar": "Sertifikalar", "diller": "Diller", "devam": "Devam",
    },
    "en": {
        "ozet": "Summary", "deneyim": "Experience", "projeler": "Projects",
        "egitim": "Education", "beceriler": "Skills",
        "sertifikalar": "Certifications", "diller": "Languages", "devam": "Present",
    },
}

ACCENT = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x55, 0x55, 0x55)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def contact_line(kisi, prof):
    """Iletisim satiri — govdede, tek satir, ayrilmis."""
    parts = [kisi.get(k) for k in ("email", "telefon", "konum", "linkedin", "site", "github")]
    extras = []
    if prof["dogum"] and kisi.get("dogum_tarihi"):
        extras.append(str(kisi["dogum_tarihi"]))
    if prof["uyruk"] and kisi.get("uyruk"):
        extras.append(str(kisi["uyruk"]))
    if prof["medeni"] and kisi.get("medeni_hal"):
        extras.append(str(kisi["medeni_hal"]))
    if prof["askerlik"] and kisi.get("askerlik"):
        extras.append(str(kisi["askerlik"]))
    return [p for p in parts + extras if p]


def setup_styles(doc, base_font="Calibri", base_size=10.5):
    normal = doc.styles["Normal"]
    normal.font.name = base_font
    normal.font.size = Pt(base_size)
    normal.paragraph_format.space_after = Pt(2)
    normal.paragraph_format.line_spacing = 1.05
    for sec in doc.sections:
        sec.top_margin = Cm(1.5)
        sec.bottom_margin = Cm(1.5)
        sec.left_margin = Cm(1.8)
        sec.right_margin = Cm(1.8)


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(10.5)
    run.font.color.rgb = ACCENT
    # ince ayirici cizgi: tablo degil, paragraf alt kenarligi
    pPr = p._p.get_or_add_pPr()
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "BBBBBB")
    borders.append(bottom)
    pPr.append(borders)
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Cm(0.5)
    return p


def date_range(item, headings):
    bas = item.get("baslangic", "")
    bit = item.get("bitis") or headings["devam"]
    return f"{bas} – {bit}".strip(" –")


def build_docx(data, prof, headings, out_path, warnings):
    doc = Document()
    setup_styles(doc)
    kisi = data.get("kisi", {})

    # --- isim ve unvan ---
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(kisi.get("ad", ""))
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = ACCENT

    if kisi.get("unvan"):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(kisi["unvan"])
        r.font.size = Pt(11.5)
        r.font.color.rgb = MUTED

    # --- iletisim (govdede) ---
    line = contact_line(kisi, prof)
    if line:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run("  ·  ".join(str(x) for x in line))
        r.font.size = Pt(9.5)
        r.font.color.rgb = MUTED

    if prof["foto"] and kisi.get("fotograf"):
        fp = Path(kisi["fotograf"])
        if fp.exists():
            doc.add_picture(str(fp), height=Cm(3.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            warnings.append(f"Fotograf bulunamadi, atlandi: {fp}")

    # --- ozet ---
    if data.get("ozet"):
        add_section_heading(doc, headings["ozet"])
        doc.add_paragraph(str(data["ozet"]).strip())

    # --- deneyim ---
    if data.get("deneyim"):
        add_section_heading(doc, headings["deneyim"])
        for job in data["deneyim"]:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(5)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(job.get("unvan", ""))
            r.bold = True
            sirket = job.get("sirket", "")
            konum = job.get("konum", "")
            tail = " — " + sirket if sirket else ""
            if konum:
                tail += f", {konum}"
            r2 = p.add_run(tail)
            r2.font.color.rgb = ACCENT

            meta = doc.add_paragraph()
            meta.paragraph_format.space_after = Pt(2)
            mr = meta.add_run(date_range(job, headings))
            mr.font.size = Pt(9.5)
            mr.font.color.rgb = MUTED
            if job.get("sirket_aciklama"):
                mr2 = meta.add_run("  ·  " + job["sirket_aciklama"])
                mr2.font.size = Pt(9.5)
                mr2.italic = True
                mr2.font.color.rgb = MUTED

            for b in job.get("bulletlar", []) or []:
                add_bullet(doc, str(b).strip())

    # --- projeler ---
    if data.get("projeler"):
        add_section_heading(doc, headings["projeler"])
        for pr in data["projeler"]:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(pr.get("ad", ""))
            r.bold = True
            if pr.get("link"):
                r2 = p.add_run("  ·  " + pr["link"])
                r2.font.size = Pt(9.5)
                r2.font.color.rgb = MUTED
            if pr.get("aciklama"):
                doc.add_paragraph(pr["aciklama"])
            for b in pr.get("bulletlar", []) or []:
                add_bullet(doc, str(b).strip())

    # --- egitim ---
    if data.get("egitim"):
        add_section_heading(doc, headings["egitim"])
        for ed in data["egitim"]:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(ed.get("derece", ""))
            r.bold = True
            tail = " — " + ed.get("kurum", "") if ed.get("kurum") else ""
            if ed.get("konum"):
                tail += f", {ed['konum']}"
            p.add_run(tail)
            meta_bits = [date_range(ed, headings)]
            if ed.get("not"):
                meta_bits.append(str(ed["not"]))
            meta = doc.add_paragraph()
            meta.paragraph_format.space_after = Pt(2)
            mr = meta.add_run("  ·  ".join(b for b in meta_bits if b))
            mr.font.size = Pt(9.5)
            mr.font.color.rgb = MUTED

    # --- beceriler ---
    if data.get("beceriler"):
        add_section_heading(doc, headings["beceriler"])
        for grp in data["beceriler"]:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(f"{grp.get('grup', '')}: ")
            r.bold = True
            p.add_run(", ".join(str(x) for x in grp.get("ogeler", []) or []))

    # --- sertifikalar ---
    if data.get("sertifikalar"):
        add_section_heading(doc, headings["sertifikalar"])
        for c in data["sertifikalar"]:
            bits = [c.get("ad", ""), c.get("kurum", ""), str(c.get("yil", ""))]
            add_bullet(doc, " — ".join(b for b in bits if b))

    # --- diller ---
    if data.get("diller"):
        add_section_heading(doc, headings["diller"])
        doc.add_paragraph(", ".join(str(d) for d in data["diller"]))

    # --- serbest ek bolumler ---
    for extra in data.get("ek_bolumler", []) or []:
        add_section_heading(doc, extra.get("baslik", ""))
        for m in extra.get("maddeler", []) or []:
            add_bullet(doc, str(m))

    doc.save(out_path)


def build_md(data, prof, headings):
    kisi = data.get("kisi", {})
    L = [f"# {kisi.get('ad', '')}"]
    if kisi.get("unvan"):
        L.append(f"**{kisi['unvan']}**")
    line = contact_line(kisi, prof)
    if line:
        L.append(" · ".join(str(x) for x in line))
    if data.get("ozet"):
        L += ["", f"## {headings['ozet']}", "", str(data["ozet"]).strip()]
    if data.get("deneyim"):
        L += ["", f"## {headings['deneyim']}"]
        for j in data["deneyim"]:
            L += ["", f"### {j.get('unvan','')} — {j.get('sirket','')}",
                  f"*{date_range(j, headings)}*" + (f" · {j['sirket_aciklama']}" if j.get("sirket_aciklama") else ""), ""]
            L += [f"- {b}" for b in j.get("bulletlar", []) or []]
    if data.get("projeler"):
        L += ["", f"## {headings['projeler']}"]
        for p in data["projeler"]:
            L += ["", f"### {p.get('ad','')}"]
            if p.get("aciklama"):
                L.append(p["aciklama"])
            L += [f"- {b}" for b in p.get("bulletlar", []) or []]
    if data.get("egitim"):
        L += ["", f"## {headings['egitim']}"]
        for e in data["egitim"]:
            L.append(f"- **{e.get('derece','')}** — {e.get('kurum','')}, {date_range(e, headings)}")
    if data.get("beceriler"):
        L += ["", f"## {headings['beceriler']}"]
        for g in data["beceriler"]:
            L.append(f"- **{g.get('grup','')}:** " + ", ".join(str(x) for x in g.get("ogeler", []) or []))
    if data.get("sertifikalar"):
        L += ["", f"## {headings['sertifikalar']}"]
        for c in data["sertifikalar"]:
            L.append(f"- {c.get('ad','')} — {c.get('kurum','')}, {c.get('yil','')}")
    if data.get("diller"):
        L += ["", f"## {headings['diller']}", "", ", ".join(str(d) for d in data["diller"])]
    for extra in data.get("ek_bolumler", []) or []:
        L += ["", f"## {extra.get('baslik','')}"]
        L += [f"- {m}" for m in extra.get("maddeler", []) or []]
    return "\n".join(L) + "\n"


def content_warnings(data, prof):
    """Uretim aninda icerik kalitesi uyarilari — dosya yine de uretilir."""
    w = []
    bullets = []
    for j in data.get("deneyim", []) or []:
        bullets += [str(b) for b in j.get("bulletlar", []) or []]
    if bullets:
        quantified = [b for b in bullets if re.search(r"\d", b)]
        oran = len(quantified) / len(bullets)
        if oran < 0.4:
            w.append(f"Rakam/kapsam iceren bullet orani dusuk: %{oran*100:.0f} "
                     f"({len(quantified)}/{len(bullets)}). Hedef: %45+")
        uzun = [b for b in bullets if len(b) > 200]
        if uzun:
            w.append(f"{len(uzun)} bullet 200 karakteri asiyor — iki satiri gecer, ilk taramada okunmaz.")
        placeholders = [b for b in bullets if re.search(r"\[[^\]]{1,30}\]", b)]
        if placeholders:
            w.append(f"{len(placeholders)} bullet'ta doldurulmamis koseli parantez var — gondermeden once doldur.")
    if not data.get("ozet"):
        w.append("Ozet bolumu yok. Ilk 10 saniye sinyalini zayiflatir.")
    kisi = data.get("kisi", {})
    if not prof["dogum"] and kisi.get("dogum_tarihi"):
        w.append("Dogum tarihi bu locale'de cikarildi (dosyada var, ciktida yok).")
    if not prof["foto"] and kisi.get("fotograf"):
        w.append("Fotograf bu locale'de cikarildi.")
    return w


def main():
    ap = argparse.ArgumentParser(description="YAML master CV verisinden parse-guvenli .docx + .md uretir")
    ap.add_argument("veri", help="YAML veri dosyasi")
    ap.add_argument("--out", default=".", help="cikti dizini")
    ap.add_argument("--locale", default="intl", choices=sorted(LOCALES), help="hedef pazar profili")
    ap.add_argument("--lang", default=None, choices=["tr", "en"], help="bolum basligi dili (varsayilan: locale'e gore)")
    ap.add_argument("--name", default=None, help="cikti dosya adi govdesi, orn. Ad-Soyad-CV-US")
    ap.add_argument("--json", action="store_true", help="ozeti JSON olarak yazdir")
    args = ap.parse_args()

    data = load(args.veri)
    prof = LOCALES[args.locale]
    lang = args.lang or ("tr" if args.locale == "tr" else "en")
    headings = HEADINGS[lang]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    ad = data.get("kisi", {}).get("ad", "CV")
    stem = args.name or re.sub(r"[^A-Za-z0-9]+", "-", ad).strip("-") + f"-CV-{args.locale.upper()}"

    docx_path = out_dir / f"{stem}.docx"
    md_path = out_dir / f"{stem}.md"

    warnings = []
    build_docx(data, prof, headings, docx_path, warnings)
    md_path.write_text(build_md(data, prof, headings), encoding="utf-8")
    warnings += content_warnings(data, prof)

    result = {"docx": str(docx_path), "md": str(md_path), "locale": args.locale,
              "lang": lang, "uyarilar": warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"✓ {docx_path}\n✓ {md_path}\n  locale={args.locale} lang={lang}")
        if warnings:
            print("\nUyarilar:")
            for x in warnings:
                print(f"  ! {x}")
        print("\nSonraki adim:  python3 parse_check.py " + str(docx_path))


if __name__ == "__main__":
    main()
