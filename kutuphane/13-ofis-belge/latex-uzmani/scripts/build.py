#!/usr/bin/env python3
"""LaTeX derleyici + log analizcisi.

Motoru preamble'dan sezer, latexmk ile derler, log'u ayrıştırıp
hataları / uyarıları / eksik karakterleri özetler, PDF'i doğrular.

Kullanım:
    python3 build.py belge.tex
    python3 build.py belge.tex --engine xelatex
    python3 build.py belge.tex --clean          # önce yardımcı dosyaları temizle
    python3 build.py belge.tex --quiet          # sadece özet
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ENGINE_FLAG = {"pdflatex": "-pdf", "xelatex": "-pdfxe", "lualatex": "-pdflua"}


def detect_engine(tex: Path) -> str:
    """Preamble'a bakarak motoru sez. fontspec/polyglossia => xelatex."""
    try:
        src = tex.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "pdflatex"
    head = src[:8000]
    # Açık direktif: % !TEX program = xelatex
    m = re.search(r"%\s*!TEX\s+(?:TS-)?program\s*=\s*(\w+)", head, re.I)
    if m and m.group(1).lower() in ENGINE_FLAG:
        return m.group(1).lower()
    if re.search(r"\\usepackage(\[[^\]]*\])?\{(fontspec|polyglossia|unicode-math)\}", head):
        return "lualatex" if "luacode" in head or "luatex" in head.lower() else "xelatex"
    return "pdflatex"


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="replace")


def parse_log(log_text: str):
    """Log'tan hata, uyarı ve taşma bilgisi çıkar."""
    errors, undefined_refs, undefined_cites, missing_chars, overfull, warnings = [], [], [], [], [], []
    lines = log_text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("!"):
            ctx = [line]
            for nxt in lines[i + 1: i + 6]:
                ctx.append(nxt)
                if nxt.startswith("l."):
                    break
            errors.append("\n".join(ctx).strip())
        elif "Reference" in line and "undefined" in line:
            m = re.search(r"Reference [`'\"]([^'\"`]+)'", line)
            if m:
                undefined_refs.append(m.group(1))
        elif "Citation" in line and "undefined" in line:
            m = re.search(r"Citation [`'\"]([^'\"`]+)'", line)
            if m:
                undefined_cites.append(m.group(1))
        elif line.startswith("Missing character:"):
            m = re.search(r"There is no (.+?) in font", line)
            if m:
                missing_chars.append(m.group(1))
        elif "Overfull \\hbox" in line:
            m = re.search(r"Overfull \\hbox \(([\d.]+)pt too wide\)(.*)", line)
            if m:
                overfull.append((float(m.group(1)), m.group(2).strip()))
        elif re.match(r"(LaTeX|Package|Class) .*Warning", line):
            if "undefined" not in line and "Rerun" not in line:
                warnings.append(line.strip())
    return {
        "errors": errors,
        "undefined_refs": sorted(set(undefined_refs)),
        "undefined_cites": sorted(set(undefined_cites)),
        "missing_chars": sorted(set(missing_chars)),
        "overfull": sorted(overfull, key=lambda x: -x[0]),
        "warnings": warnings,
    }


def pdf_info(pdf: Path):
    if not shutil.which("pdfinfo"):
        return {}
    out = run(["pdfinfo", str(pdf)], pdf.parent).stdout
    info = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--engine", choices=list(ENGINE_FLAG))
    ap.add_argument("--clean", action="store_true", help="derlemeden önce latexmk -C")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--shell-escape", action="store_true", help="minted vb. için")
    args = ap.parse_args()

    tex = Path(args.tex).resolve()
    if not tex.exists():
        print(f"HATA: {tex} yok"); sys.exit(2)
    cwd = tex.parent
    engine = args.engine or detect_engine(tex)

    if args.clean:
        run(["latexmk", "-C", tex.name], cwd)

    cmd = ["latexmk", ENGINE_FLAG[engine], "-interaction=nonstopmode",
           "-file-line-error", "-halt-on-error" if False else "-f", tex.name]
    if args.shell_escape:
        cmd.insert(-1, "-shell-escape")

    print(f"→ motor: {engine}")
    proc = run(cmd, cwd)

    log_path = cwd / (tex.stem + ".log")
    log_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else proc.stdout
    r = parse_log(log_text)
    pdf = cwd / (tex.stem + ".pdf")

    print("=" * 64)
    ok = True

    if r["errors"]:
        ok = False
        print(f"HATA ({len(r['errors'])}) — ilkini çöz, gerisi çığ olabilir:\n")
        for e in r["errors"][:3 if args.quiet else 8]:
            print("  " + e.replace("\n", "\n  "))
            print()
    if r["missing_chars"]:
        ok = False
        print(f"EKSİK KARAKTER — font bu glifleri basmıyor, PDF'te kayıp: {' '.join(r['missing_chars'])}")
        print("  → Türkçe glifleri kapsayan bir fonta geç (bkz. references/ortam.md)\n")
    if r["undefined_refs"]:
        ok = False
        print(f"ÇÖZÜLMEMİŞ REFERANS ({len(r['undefined_refs'])}): {', '.join(r['undefined_refs'][:12])}\n")
    if r["undefined_cites"]:
        ok = False
        print(f"ÇÖZÜLMEMİŞ ATIF ({len(r['undefined_cites'])}): {', '.join(r['undefined_cites'][:12])}")
        print("  → .bib anahtarını kontrol et; latexmk bibtex/biber turunu yaptı mı?\n")

    big = [o for o in r["overfull"] if o[0] >= 10]
    if big:
        print(f"TAŞAN SATIR ({len(big)} adet ≥10pt) — metin kenara taşıyor:")
        for pt, ctx in big[:5]:
            print(f"  {pt:.1f}pt  {ctx}")
        print()
    elif r["overfull"] and not args.quiet:
        print(f"(küçük taşma: {len(r['overfull'])} adet <10pt, göz ardı edilebilir)\n")

    if pdf.exists():
        info = pdf_info(pdf)
        print(f"PDF: {pdf.name}  |  {info.get('Pages','?')} sayfa  |  {info.get('Page size','?')}")
    else:
        ok = False
        print("PDF ÜRETİLMEDİ.")

    print("=" * 64)
    print("SONUÇ: TEMİZ" if ok else "SONUÇ: DÜZELTİLECEK SORUN VAR")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
