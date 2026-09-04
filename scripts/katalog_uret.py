#!/usr/bin/env python3
"""Kütüphaneyi tarar; katalog dosyalarını ve dokümantasyonu yeniden üretir.

Tek doğruluk kaynağı `kutuphane/` dizinidir. Bir skill eklendiğinde,
silindiğinde veya açıklaması değiştiğinde bunu çalıştır:

    python3 scripts/katalog_uret.py

Üretilenler: katalog/skills.json, katalog/skills.csv, INDEX.md,
README.md'nin kategori tablosu ve her kategorinin README.md'si.
"""
import csv
import json
import os
import re
from collections import defaultdict
from datetime import date

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KUTUPHANE = os.path.join(KOK, "kutuphane")
KATALOG = os.path.join(KOK, "katalog")
EV = os.path.expanduser("~")

KATEGORI_BASLIK = {
    "01-finans-yatirim": (
        "Finans & Yatırım",
        "Helal/katılım esaslı yatırım, portföy kalibrasyonu, bütçe, vergi, "
        "fiyatlandırma ve değerleme.",
    ),
    "02-masifico-ahsap-oyuncak": (
        "Masifico — Ahşap Oyuncak",
        "Masif kayın oyuncak işinin uçtan uca zinciri: tasarım → üretim → "
        "kalite → mevzuat → pazar.",
    ),
    "03-video-ses-uretim": (
        "Video & Ses Üretimi",
        "Fizik ve ambient video hatları, müzik besteleme, plak etiketi, "
        "kanal yönetimi, prosedürel ses.",
    ),
    "04-icerik-yazim-ceviri": (
        "İçerik, Yazım & Çeviri",
        "Doğal Türkçe/İngilizce metin, dikey video anlatısı, çok dilli çeviri, "
        "içerik stratejisi ve üretimi.",
    ),
    "05-pazarlama-buyume": (
        "Pazarlama & Büyüme",
        "SEO/ASO denetimi, Shorts optimizasyonu, viral ürün avı, lead üretimi.",
    ),
    "06-ux-urun": (
        "UX & Ürün Yönetimi",
        "Mobil ve web akış tasarımı/denetimi, ürün kararı incelemesi.",
    ),
    "07-yazilim-muhendislik": (
        "Yazılım Mühendisliği",
        "Framework ve altyapı referansları, kod grafiği araçları, çoklu bulut "
        "ve sunucu operasyonu.",
    ),
    "08-ai-ml": (
        "AI & Makine Öğrenmesi",
        "Kaggle/ML iş akışı, AutoML, LLM ve SLM mimarisi, GPU kaynak hibeleri.",
    ),
    "09-cad-gorsel": (
        "CAD & Görsel Üretim",
        "Parametrik mobilya/CAD zinciri, markalı görsel hattı, stok görsel keşfi.",
    ),
    "10-yasam-turkiye": (
        "Yaşam & Türkiye Hizmetleri",
        "Satın alma, seyahat, vize, hak arama, dijital mahremiyet, etkinlik ve "
        "bölgesel mevzuat.",
    ),
    "11-ogrenme": (
        "Öğrenme & Dil",
        "Arapça ve İngilizce koçluğu, genel öğrenme rehberliği.",
    ),
    "12-marka-musteri": (
        "Marka & Müşteri Projeleri",
        "Belirli markalara bağlı kimlik, içerik ve mevzuat kaynakları.",
    ),
    "13-ofis-belge": (
        "Ofis & Belge",
        "Word/PowerPoint/Excel/PDF üretimi ve düzenlemesi (Anthropic yerleşik).",
    ),
    "14-meta-sistem": (
        "Meta & Sistem",
        "Skill yazımı ve değerlendirmesi, hafıza, zamanlama, kurulum, oturum araçları.",
    ),
}

KAYNAK_ETIKET = {
    "install": "kurulu",
    "content": "proje-içi",
    "cloud": "claude.ai",
}


def frontmatter(yol):
    """SKILL.md'nin frontmatter'ından ad ve açıklamayı çıkarır."""
    try:
        metin = open(yol, encoding="utf-8", errors="replace").read()
    except OSError:
        return {}
    eslesme = re.match(r"^---\s*\n(.*?)\n---\s*\n", metin, re.S)
    if not eslesme:
        return {"_satir": metin.count("\n") + 1, "_bayt": len(metin)}
    govde = eslesme.group(1)
    veri = {"_satir": metin.count("\n") + 1, "_bayt": len(metin)}
    for anahtar in ("name", "description", "license"):
        alan = re.search(
            rf"^{anahtar}:\s*>?\s*(.*?)(?=\n[a-zA-Z_-]+:\s|\Z)", govde, re.S | re.M
        )
        if alan:
            veri[anahtar] = " ".join(alan.group(1).split()).strip("'\"")
    return veri


def kisa(aciklama, sinir=165):
    """Uzun açıklamayı ilk cümle/tire öbeğine indirger."""
    if not aciklama:
        return ""
    metin = re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ])", aciklama)[0]
    if len(metin) > sinir:
        kesme = metin.rfind(" ", 0, sinir)
        metin = metin[: kesme if kesme > 60 else sinir].rstrip(" ,;") + "…"
    return metin


def tara():
    """kutuphane/ altındaki her skill'i okuyup manifest ile birleştirir."""
    manifest_yolu = os.path.join(KATALOG, "manifest.json")
    manifest = {}
    if os.path.exists(manifest_yolu):
        for kayit in json.load(open(manifest_yolu, encoding="utf-8")):
            manifest[(kayit["cat"], kayit["slug"])] = kayit

    kayitlar = []
    for kategori in sorted(os.listdir(KUTUPHANE)):
        kat_yolu = os.path.join(KUTUPHANE, kategori)
        if not os.path.isdir(kat_yolu):
            continue
        for slug in sorted(os.listdir(kat_yolu)):
            skill_yolu = os.path.join(kat_yolu, slug)
            skill_md = os.path.join(skill_yolu, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue
            fm = frontmatter(skill_md)
            ekler = []
            for kok, dizinler, dosyalar in os.walk(skill_yolu):
                dizinler[:] = [d for d in dizinler if d not in (".git", "__pycache__")]
                for dosya in dosyalar:
                    if dosya in ("SKILL.md", ".DS_Store"):
                        continue
                    ekler.append(
                        os.path.relpath(os.path.join(kok, dosya), skill_yolu)
                    )
            m = manifest.get((kategori, slug), {})
            kayitlar.append(
                {
                    "ad": fm.get("name", slug),
                    "slug": slug,
                    "kategori": kategori,
                    "kategori_adi": KATEGORI_BASLIK.get(kategori, (kategori, ""))[0],
                    "aciklama": fm.get("description", ""),
                    "ozet": kisa(fm.get("description", "")),
                    "yol": os.path.relpath(skill_yolu, KOK),
                    "bayt": fm.get("_bayt", 0),
                    "satir": fm.get("_satir", 0),
                    "ek_dosya": len(ekler),
                    "script_var": any(e.startswith("scripts/") for e in ekler),
                    "referans_var": any(e.startswith("references/") for e in ekler),
                    "varyant": m.get("variant", 0),
                    "kaynaklar": m.get("srcs", []),
                    "kaynak_tipleri": sorted(
                        {KAYNAK_ETIKET.get(k, k) for k in m.get("kinds", [])}
                    ),
                    "baglanacak": m.get("linked", []),
                    "ayna": m.get("mirrored", []),
                }
            )
    return kayitlar


def gizle(yol):
    """Cloud'un uzun efemer yolunu okunur hale getirir."""
    if "local-agent-mode-sessions" in yol:
        return "claude.ai senkronu (efemer önbellek)"
    return yol


def yaz_katalog(kayitlar):
    os.makedirs(KATALOG, exist_ok=True)
    json.dump(
        kayitlar,
        open(os.path.join(KATALOG, "skills.json"), "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=1,
    )
    with open(
        os.path.join(KATALOG, "skills.csv"), "w", encoding="utf-8-sig", newline=""
    ) as ch:
        yazici = csv.writer(ch)
        yazici.writerow(
            ["ad", "kategori", "ozet", "yol", "bayt", "ek_dosya", "script", "kaynak"]
        )
        for k in kayitlar:
            yazici.writerow(
                [
                    k["ad"],
                    k["kategori_adi"],
                    k["ozet"],
                    k["yol"],
                    k["bayt"],
                    k["ek_dosya"],
                    "evet" if k["script_var"] else "hayır",
                    ", ".join(k["kaynak_tipleri"]),
                ]
            )


def yaz_index(kayitlar):
    satirlar = [
        "# Alfabetik Skill Dizini",
        "",
        f"{len(kayitlar)} kütüphane girdisi. Kategori sayfaları için "
        "[README.md](README.md), Claude'un çalışma kuralları için "
        "[CLAUDE.md](CLAUDE.md).",
        "",
        "| Skill | Kategori | Ne yapar | Kaynak |",
        "|---|---|---|---|",
    ]
    for k in sorted(kayitlar, key=lambda x: x["slug"]):
        isaret = " ⚙️" if k["script_var"] else ""
        satirlar.append(
            f"| [`{k['slug']}`]({k['yol']}/SKILL.md){isaret} | {k['kategori_adi']} | "
            f"{k['ozet']} | {', '.join(k['kaynak_tipleri'])} |"
        )
    satirlar += [
        "",
        "⚙️ = çalıştırılabilir script içerir.",
        "",
        f"_Üretim: `scripts/katalog_uret.py` · {date.today().isoformat()}_",
    ]
    open(os.path.join(KOK, "INDEX.md"), "w", encoding="utf-8").write(
        "\n".join(satirlar) + "\n"
    )


def yaz_kategori_readme(kayitlar):
    gruplar = defaultdict(list)
    for k in kayitlar:
        gruplar[k["kategori"]].append(k)
    for kategori, uyeler in gruplar.items():
        baslik, ozet = KATEGORI_BASLIK.get(kategori, (kategori, ""))
        satirlar = [
            f"# {baslik}",
            "",
            ozet,
            "",
            f"{len(uyeler)} skill. Üst dizin: [../../README.md](../../README.md)",
            "",
        ]
        for k in sorted(uyeler, key=lambda x: x["slug"]):
            satirlar.append(f"## `{k['slug']}`")
            satirlar.append("")
            satirlar.append(f"[SKILL.md]({k['slug']}/SKILL.md)")
            satirlar.append("")
            satirlar.append(k["aciklama"] or "_Açıklama yok._")
            satirlar.append("")
            olcum = [
                f"{k['bayt']:,} bayt".replace(",", "."),
                f"{k['ek_dosya']} ek dosya",
            ]
            if k["script_var"]:
                olcum.append("script içerir")
            if k["referans_var"]:
                olcum.append("referans dosyaları var")
            satirlar.append("- **Ölçü:** " + " · ".join(olcum))
            satirlar.append(
                "- **Kaynak:** " + ", ".join(gizle(s) for s in k["kaynaklar"])
            )
            satirlar.append("")
        open(
            os.path.join(KUTUPHANE, kategori, "README.md"), "w", encoding="utf-8"
        ).write("\n".join(satirlar) + "\n")


def main():
    kayitlar = tara()
    yaz_katalog(kayitlar)
    yaz_index(kayitlar)
    yaz_kategori_readme(kayitlar)
    print(f"{len(kayitlar)} girdi tarandı.")
    print("yazıldı: katalog/skills.json, katalog/skills.csv, INDEX.md,")
    print(f"         {len(KATEGORI_BASLIK)} kategori README.md")


if __name__ == "__main__":
    main()
