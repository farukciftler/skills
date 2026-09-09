#!/usr/bin/env python3
"""LaTeX kaynak denetçisi — Türkçe dizgi ve genel kalite kontrolleri.

Derleme hatası vermeyen ama çıktıyı bozan şeyleri yakalar:
motor/paket uyuşmazlığı, babel shorthand, düz tırnak, kaçırılmamış %,
\\label yeri, kırılmayan boşluk eksikliği, matematik modunda Türkçe ondalık.

Kullanım:  python3 lint.py belge.tex [belge2.tex ...]
"""
import re
import sys
from pathlib import Path

SEV = {"HATA": "HATA ", "UYARI": "UYARI", "BILGI": "bilgi"}


def strip_comments(line: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", line)


def lint(path: Path):
    src = path.read_text(encoding="utf-8", errors="replace")
    lines = src.splitlines()
    body = "\n".join(strip_comments(l) for l in lines)
    f = []  # (severity, line_no, message)

    def add(sev, ln, msg):
        f.append((sev, ln, msg))

    unicode_engine = bool(re.search(r"\\usepackage(\[[^\]]*\])?\{(fontspec|polyglossia|unicode-math)\}", body))
    has_turkish = bool(re.search(r"turkish", body, re.I)) or bool(re.search(r"[ğşıİĞŞÇç]", src))

    # --- motor / paket uyuşmazlığı
    if unicode_engine:
        for i, l in enumerate(lines, 1):
            if re.search(r"\\usepackage(\[[^\]]*\])?\{(inputenc|fontenc)\}", strip_comments(l)):
                add("HATA", i, "XeLaTeX/LuaLaTeX belgesinde inputenc/fontenc kullanılmaz — kaldır.")
    else:
        if has_turkish and not re.search(r"\\usepackage\[T1\]\{fontenc\}", body):
            add("HATA", 0, "pdfLaTeX + Türkçe: [T1]{fontenc} eksik. ğ/ş/ı bozuk çıkar veya kopyalanamaz.")
        if has_turkish and not re.search(r"\{(lmodern|newtx|tgtermes|tgpagella|charter)\}", body):
            add("UYARI", 0, "pdfLaTeX + T1: lmodern yüklü değil — Computer Modern bitmap fontu bulanık çıkabilir.")

    # --- babel shorthand
    m = re.search(r"\\usepackage\[([^\]]*)\]\{babel\}", body)
    if m and "turkish" in m.group(1) and "shorthands=off" not in m.group(1):
        ln = next((i for i, l in enumerate(lines, 1) if "{babel}" in l), 0)
        add("HATA", ln, "babel-turkish shorthands açık: = : ! karakterleri TikZ/tablo/matematikte patlar. "
                        "[shorthands=off,turkish] yaz.")

    # --- dil paketi hiç yok
    if has_turkish and not re.search(r"(babel|polyglossia|setmainlanguage)", body):
        add("HATA", 0, "Türkçe metin var ama dil paketi yok: hece bölme ve Şekil/Tablo/Kaynaklar etiketleri yanlış olur.")

    # --- MakeUppercase riski
    for i, l in enumerate(lines, 1):
        if re.search(r"\\(MakeUppercase|uppercase)\b", strip_comments(l)) and has_turkish:
            add("UYARI", i, "MakeUppercase + Türkçe: 'i' harfi 'I' olur (doğrusu 'İ'). PDF'te başlıkları gözle kontrol et.")

    # --- düz tırnak
    for i, l in enumerate(lines, 1):
        c = strip_comments(l)
        if re.search(r'(?<![\\=])"(?!\})', c) and "verbatim" not in c:
            add("UYARI", i, 'Düz " karakteri: LaTeX tipografik tırnak üretmez. ``...\'\' veya \\enquote{...} kullan.')

    # --- kaçırılmamış %
    for i, l in enumerate(lines, 1):
        if re.search(r"(?<![\\\d])\s%\s*\d", l):
            add("UYARI", i, "Kaçırılmamış % olabilir: satırın kalanı yorum olur ve sessizce kaybolur. \\% yaz.")

    # --- \label \caption'dan önce
    for i, l in enumerate(lines, 1):
        c = strip_comments(l)
        if "\\label" in c and "\\caption" in c and c.index("\\label") < c.index("\\caption"):
            add("HATA", i, "\\label \\caption'dan ÖNCE: numara yanlış çıkar. Sırayı değiştir.")
    for i in range(len(lines) - 1):
        a, b = strip_comments(lines[i]), strip_comments(lines[i + 1])
        if a.strip().startswith("\\label") and b.strip().startswith("\\caption"):
            add("HATA", i + 1, "\\label \\caption'dan ÖNCE: numara yanlış çıkar.")

    # --- kırılmayan boşluk
    for i, l in enumerate(lines, 1):
        if re.search(r"\b(Şekil|Tablo|Çizelge|Bölüm|Denklem|Figure|Table|Section|Eq\.)\s+\\(ref|cref|eqref)", strip_comments(l)):
            add("BILGI", i, "Referans öncesi ~ yok: 'Şekil~\\ref{...}' yaz, yoksa satır sonunda ayrılır.")

    # --- matematik modunda Türkçe ondalık
    for i, l in enumerate(lines, 1):
        if re.search(r"\$[^$]*\d,\d[^$]*\$", strip_comments(l)):
            add("UYARI", i, "Matematik modunda 'x,y': virgül liste ayıracı sayılır, fazla boşluk açar. 3{,}14 yaz.")

    # --- eqnarray
    for i, l in enumerate(lines, 1):
        if "eqnarray" in strip_comments(l):
            add("UYARI", i, "eqnarray bozuk boşluk üretir — amsmath'ın align/gather ortamını kullan.")

    # --- hyperref sırası
    pkgs = re.findall(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", body)
    flat = [p.strip() for grp in pkgs for p in grp.split(",")]
    if "hyperref" in flat:
        after = flat[flat.index("hyperref") + 1:]
        bad = [p for p in after if p not in ("cleveref", "bookmark", "glossaries", "algorithm2e")]
        if bad:
            add("UYARI", 0, f"hyperref'ten sonra yüklenen paketler var ({', '.join(bad[:4])}). "
                            "hyperref cleveref hariç en son yüklenmelidir.")
    if "cleveref" in flat and "hyperref" in flat and flat.index("cleveref") < flat.index("hyperref"):
        add("HATA", 0, "cleveref, hyperref'ten ÖNCE yüklenmiş — ters çevir.")

    # --- kaynakça tutarlılığı
    if "\\cite" in body and not re.search(r"(\\bibliography\{|\\printbibliography|\\addbibresource)", body):
        add("HATA", 0, "\\cite var ama kaynakça komutu yok: atıflar [?] çıkar.")
    if "biblatex" in flat and "natbib" in flat:
        add("HATA", 0, "biblatex ve natbib birlikte yüklenemez.")

    # --- ortam dengesi
    begins = re.findall(r"\\begin\{(\w+\*?)\}", body)
    ends = re.findall(r"\\end\{(\w+\*?)\}", body)
    for env in set(begins) | set(ends):
        if begins.count(env) != ends.count(env):
            add("HATA", 0, f"Ortam dengesiz: {env} — \\begin {begins.count(env)}, \\end {ends.count(env)}")

    return f


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    total = 0
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"HATA: {p} yok"); continue
        findings = lint(p)
        print(f"\n─── {p.name} ───")
        if not findings:
            print("temiz.")
            continue
        order = {"HATA": 0, "UYARI": 1, "BILGI": 2}
        for sev, ln, msg in sorted(findings, key=lambda x: (order[x[0]], x[1])):
            loc = f"satır {ln}" if ln else "genel"
            print(f"  [{SEV[sev]}] {loc}: {msg}")
        total += sum(1 for s, _, _ in findings if s == "HATA")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
