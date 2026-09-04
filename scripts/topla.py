#!/usr/bin/env python3
"""Diskteki tüm SKILL.md'leri tarar, kategorize eder ve kutuphane/ altına toplar.

Kaynak konumlarına dokunmaz — yalnızca kopyalar ve `katalog/manifest.json`
yazar. Kaynakları kütüphaneye bağlamak (symlink) ayrı bir iştir:
`scripts/bagla.py`.

Kullanım:
    python3 scripts/topla.py            # kuru çalıştırma, plan basar
    python3 scripts/topla.py --uygula   # kutuphane/ kurar, manifest yazar

Aynı isimli girdiler için adlandırma:
  * içerik özdeşse tek girdide birleşir;
  * yalnız gövde ayrışmışsa en yeni olan düz adı alır, diğerleri `--<kaynak>`;
  * açıklamalar da farklıysa (gerçekte farklı skill'ler) hepsi ek alır.
"""
import collections
import hashlib
import json
import os
import re
import shutil
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.expanduser("~")
KUTUPHANE = os.path.join(KOK, "kutuphane")
KATALOG = os.path.join(KOK, "katalog")

# claude.ai senkronunun yerel önbelleği. Oturum kimliği değişebilir; en yeni
# `skills` dizini otomatik bulunur.
CLOUD_KOK = os.path.join(
    EV, "Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"
)

# Tarama dışı: eski anlık görüntüler, IDE eklentileri, geçici iş dizinleri.
HARIC = (
    "/node_modules/",
    "/.git/",
    "/.claude/remote/plugins/",
    "/.vscode/",
    "/.antigravity-ide/",
    "/.gemini/antigravity",
    "/.claude/jobs/",
    "/_backup",
    "/.claude/worktrees/",
    "/Library/Application Support/Claude/local-agent-mode-sessions/",
    "/.claude/plugins/marketplaces/",
    "/skills/kutuphane/",
    # Satıcı paketleri ve editör yerleşikleri: Faruk'un skill'i değil.
    "/.claude/plugins/cache/",
    "/.cursor/skills-cursor/",
    # Tek seferlik zamanlanmış görev promptları; yeniden kullanılabilir skill değil.
    "/.claude/scheduled-tasks/",
)

KATEGORI = {
    "01-finans-yatirim": [
        "helal-yatirim-uzmani", "portfoy-tahmin", "tahmin-savcisi",
        "helal-portfoy-uzmanlari", "harcama-analizi", "ev-yatirim-analisti",
        "vakif-katilim-yatirim", "sahis-vergi-yukumluluk", "fiyatlandirma-uzmani",
        "domain-portfoy-degerleme", "startup-degerleme",
    ],
    "02-masifico-ahsap-oyuncak": [
        "masifico-uretim-muhendisi", "masifico-parti-uretim", "masifico-tedarik-rfq",
        "masifico-kalite-izlenebilirlik", "masifico-teknik-dosya",
        "masifico-maliyet-fiyat", "masifico-farklilasma", "masifico-ahsap-kultur",
        "masifico-urun-gorsel", "masifico-video-uretim", "oyuncak-mevzuat",
        "oyuncak-pazar-radari",
    ],
    "03-video-ses-uretim": [
        "headless-reel-forge", "physics-reel-forge", "ambient-video-forge",
        "stock-footage-forge", "shorts-strategy", "suno-composer",
        "retro-record-label", "weft-release", "weft-channel",
        "healing-audio-youtube-seo", "kling-video-uretim", "procedural-game-audio",
        "chibi-character-factory",
    ],
    "04-icerik-yazim-ceviri": [
        "insanca", "turkce-anlati", "english-narration", "ceviri", "icerik-strateji",
        "icerik-uret", "yeme-icme", "backlog-arastir", "backlog",
        "sosyal-medya-post-uret", "icerik-yaz",
    ],
    "05-pazarlama-buyume": [
        "seo-expert", "aso-expert", "aso-optimizer", "youtube-shorts-optimizer",
        "reklam-ve-performans",
        "viral-artifact-scout", "hedef-arastirma", "klinik-lead-akisi",
        "appstore-market-analyst",
    ],
    "06-ux-urun": [
        "mobile-ux-flow-expert", "web-ux-flow-expert", "ota-mobile-tablet-ux",
        "kartela-web-ux", "pm-decision-review", "arayuz-denetimi",
        "mobile-ux-architect", "mobile-puzzle-game-ui-designer",
        "mobile-puzzle-game-ux-audit-expert", "tacet-ui-ux-design",
        "jira-task-writer",
    ],
    "07-yazilim-muhendislik": [
        "nextjs-development", "react-patterns", "tailwind-css",
        "fastapi-microservices-development", "pydantic", "pytest", "postgresql",
        "docker-compose-orchestration", "oauth2-authentication", "gitnexus-guide",
        "gitnexus-cli", "gitnexus-exploring", "gitnexus-debugging",
        "gitnexus-impact-analysis", "gitnexus-refactoring", "hyperscaler-expert",
        "serverim-build", "apple-platform-architect",
    ],
    "08-ai-ml": [
        "ml-expert", "automl", "kaggle-kaggle-skill", "llm-engineering-expert",
        "slm-architecture-lead", "ab-gpu-hibe-uzmani",
    ],
    "09-cad-gorsel": [
        "mobilya-cad", "gorsel-uretim", "pexels-gorsel-bulucu", "pexels-media-scout",
        "post-forge",
    ],
    "10-yasam-turkiye": [
        "arac-uzmani", "urun-kesif", "konaklama-kesif", "ucuz-bilet-avcisi",
        "vize-giris-kurallari", "schengen-randevu-tr", "kultur-sanat-radari", "sahibinden-arama", "trip-konaklama-avcisi",
        "tech-etkinlik-kesif", "hak-arama-turkiye", "dijital-iz-denetcisi",
        "suriye-is-mevzuat",
    ],
    "11-ogrenme": ["arapca-ogretmeni", "ingilizce-kocu", "learn"],
    "12-marka-musteri": ["moonstone-residence", "kartela-icerik", "rpdm-mevzuat"],
    "13-ofis-belge": ["docx", "pptx", "xlsx", "pdf"],
    "14-meta-sistem": [
        "skill-creator", "kirkit-skill-author", "consolidate-memory",
        "import-memory", "morning", "schedule", "setup-cowork", "explain-usage",
    ],
}
KATEGORI_ESLEME = {ad: kat for kat, adlar in KATEGORI.items() for ad in adlar}
DIGER = "99-siniflandirilmamis"


def cloud_dizini():
    """claude.ai senkronunun en yeni yerel anlık görüntüsünü bulur."""
    adaylar = []
    for kok, dizinler, _ in os.walk(CLOUD_KOK):
        if kok.count(os.sep) - CLOUD_KOK.count(os.sep) > 3:
            dizinler[:] = []
            continue
        if os.path.basename(kok) == "skills":
            adaylar.append((os.path.getmtime(kok), kok))
            dizinler[:] = []
    return max(adaylar)[1] if adaylar else None


def dizin_ozeti(dizin):
    """Dizin içeriğinin kimliği — kopyaları ayırt etmek için."""
    ozet = hashlib.sha256()
    for kok, dizinler, dosyalar in os.walk(dizin):
        dizinler[:] = [d for d in dizinler if d not in (".git", "__pycache__")]
        for dosya in sorted(dosyalar):
            if dosya == ".DS_Store":
                continue
            yol = os.path.join(kok, dosya)
            ozet.update(os.path.relpath(yol, dizin).encode())
            try:
                ozet.update(open(yol, "rb").read())
            except OSError:
                pass
    return ozet.hexdigest()[:12]


def en_yeni(dizin):
    """Dizindeki en son değiştirilmiş dosyanın zamanı."""
    zaman = 0
    for kok, dizinler, dosyalar in os.walk(dizin):
        dizinler[:] = [d for d in dizinler if d not in (".git", "__pycache__")]
        for dosya in dosyalar:
            try:
                zaman = max(zaman, os.path.getmtime(os.path.join(kok, dosya)))
            except OSError:
                pass
    return zaman


def aciklama(dizin):
    """SKILL.md frontmatter'ından açıklamanın ilk 120 karakteri."""
    try:
        metin = open(
            os.path.join(dizin, "SKILL.md"), encoding="utf-8", errors="replace"
        ).read()
    except OSError:
        return ""
    bas = re.match(r"^---\s*\n(.*?)\n---\s*\n", metin, re.S)
    if not bas:
        return ""
    alan = re.search(
        r"^description:\s*>?\s*(.*?)(?=\n[a-zA-Z_-]+:\s|\Z)", bas.group(1), re.S | re.M
    )
    return " ".join(alan.group(1).split()).lower()[:120] if alan else ""


def tur(rel):
    """Konum gerçek bir skill kurulum noktası mı, proje içeriği mi, cloud mu?"""
    if rel.startswith("~/Library/"):
        return "cloud"
    if rel.startswith("~/.claude/skills/") or re.search(
        r"/\.claude/skills/[^/]+$", rel
    ):
        return "install"
    return "content"


def kok_etiket(kayit):
    if kayit["tur"] == "cloud":
        return "cloud"
    if kayit["dizin"].startswith("~/.gemini/"):
        return "gemini"
    if kayit["proje"]:
        return re.sub(r"[^a-z0-9]+", "-", kayit["proje"].lower()).strip("-")
    if "kirkit" in kayit["dizin"]:
        return "kirkit"
    return "global"


def etiket(kayit):
    kok = kok_etiket(kayit)
    return kok + "-gh" if kayit["dizin"].startswith("~/Documents/GitHub/") else kok


def bul():
    """Ev dizinini ve cloud önbelleğini tarayıp skill dizinlerini toplar."""
    bulunan = []
    for kok, dizinler, dosyalar in os.walk(EV):
        if any(h in kok + "/" for h in HARIC):
            dizinler[:] = []
            continue
        if kok.count(os.sep) - EV.count(os.sep) > 8:
            dizinler[:] = []
            continue
        if "SKILL.md" in dosyalar:
            bulunan.append(kok)
    cloud = cloud_dizini()
    if cloud:
        for kok, _, dosyalar in os.walk(cloud):
            if "SKILL.md" in dosyalar:
                bulunan.append(kok)

    kayitlar = []
    for dizin in sorted(set(bulunan)):
        rel = dizin.replace(EV + "/", "~/")
        proje = ""
        eslesme = re.search(r"~/(?:projects|Documents/GitHub)/([^/]+)/", rel + "/")
        if eslesme:
            proje = eslesme.group(1)
        kayitlar.append(
            {
                "dizin": rel,
                "ad": os.path.basename(dizin),
                "proje": proje,
                "tur": tur(rel),
                "ozet": dizin_ozeti(dizin),
                "zaman": en_yeni(dizin),
                "bayt": os.path.getsize(os.path.join(dizin, "SKILL.md")),
                "aciklama": aciklama(dizin),
            }
        )
    return kayitlar


def planla(kayitlar):
    gruplar = collections.defaultdict(list)
    for kayit in kayitlar:
        gruplar[kayit["ad"]].append(kayit)

    sira = {"install": 0, "content": 1, "cloud": 2}
    kullanilan, plan = set(), []
    for ad, uyeler in sorted(gruplar.items()):
        ozete_gore = collections.defaultdict(list)
        for uye in uyeler:
            ozete_gore[uye["ozet"]].append(uye)
        # Birincil: kurulum noktası > proje içeriği > cloud, sonra en yeni içerik.
        siralanmis = sorted(
            ozete_gore.items(),
            key=lambda kv: (
                min(sira[u["tur"]] for u in kv[1]),
                -max(u["zaman"] for u in kv[1]),
                -max(u["bayt"] for u in kv[1]),
            ),
        )
        # Açıklamalar da farklıysa bunlar gerçekte farklı skill'lerdir.
        hepsine_ek = len({u["aciklama"] for _, grup in siralanmis for u in grup}) > 1
        for indeks, (ozet, kaynaklar) in enumerate(siralanmis):
            slug = (
                ad
                if (indeks == 0 and not hepsine_ek)
                else f"{ad}--{etiket(kaynaklar[0])}"
            )
            if slug in kullanilan:
                slug = f"{slug}-{indeks + 1}"
            kullanilan.add(slug)
            plan.append(
                {
                    "name": ad,
                    "slug": slug,
                    "cat": KATEGORI_ESLEME.get(ad, DIGER),
                    "hash": ozet,
                    "variant": indeks,
                    "srcs": [k["dizin"] for k in kaynaklar],
                    "kinds": [k["tur"] for k in kaynaklar],
                    "bytes": max(k["bayt"] for k in kaynaklar),
                }
            )
    return plan


def main():
    uygula = "--uygula" in sys.argv
    kayitlar = bul()
    plan = planla(kayitlar)
    baglanabilir = sum(1 for p in plan for t in p["kinds"] if t == "install")
    print(f"bulunan kaynak: {len(kayitlar)}")
    print(f"kütüphane girdisi: {len(plan)} (benzersiz ad: {len({p['name'] for p in plan})})")
    print(f"bağlanabilir kurulum noktası: {baglanabilir}")
    siniflandirilmamis = [p["name"] for p in plan if p["cat"] == DIGER]
    if siniflandirilmamis:
        print(f"UYARI — kategorisiz: {sorted(set(siniflandirilmamis))}")
        print("  KATEGORI sözlüğüne ekle (bu dosya + scripts/katalog_uret.py).")
    if not uygula:
        print("\n[kuru çalıştırma — hiçbir şey değişmedi; --uygula ile kur]")
        return

    os.makedirs(KATALOG, exist_ok=True)
    manifest = []
    for p in plan:
        hedef = os.path.join(KUTUPHANE, p["cat"], p["slug"])
        os.makedirs(os.path.dirname(hedef), exist_ok=True)
        kaynak = p["srcs"][0].replace("~", EV)
        if not os.path.exists(hedef):
            shutil.copytree(
                kaynak,
                hedef,
                symlinks=False,
                ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"),
            )
        kayit = dict(p)
        kayit["lib"] = hedef.replace(EV, "~")
        kayit["linked"] = [r for r, t in zip(p["srcs"], p["kinds"]) if t == "install"]
        kayit["mirrored"] = [r for r, t in zip(p["srcs"], p["kinds"]) if t != "install"]
        manifest.append(kayit)
    json.dump(
        manifest,
        open(os.path.join(KATALOG, "manifest.json"), "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=1,
    )
    print(f"\n{len(manifest)} girdi kutuphane/ altına toplandı.")
    print("sıradaki: python3 scripts/katalog_uret.py")


if __name__ == "__main__":
    main()
