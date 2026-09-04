# Skill Kütüphanesi

Faruk'un tüm Claude skill'lerinin tek merkezi. Projelerde, `~/.claude/skills`
altında, claude.ai'da ve GitHub depolarında dağınık duran **128 benzersiz skill**
burada kategorize edilmiş, ölçülmüş ve dokümante edilmiş halde duruyor.

| | |
|---|---|
| **Kütüphane girdisi** | 154 (128 benzersiz ad + 26 ayrışmış sürüm) |
| **Kategori** | 14 |
| **Toplam SKILL.md** | ~1,8 MB · 740 ek dosya |
| **Script içeren** | 47 skill |
| **Referans dosyası olan** | 81 skill |
| **Kaynak dağılımı** | 67 kurulu · 53 proje-içi · 50 claude.ai · 6 yalnız GitHub |

## Nereden başlamalı

| İhtiyaç | Dosya |
|---|---|
| Bir skill'i isimden aramak | **[INDEX.md](INDEX.md)** — 154 girdilik alfabetik tablo |
| Claude'un buradan nasıl çalışacağı | **[CLAUDE.md](CLAUDE.md)** |
| Ne taşındı, ne taşınmadı, nasıl geri alınır | **[TASIMA.md](TASIMA.md)** |
| Başka bir bilgisayarda kurmak | **[KURULUM.md](KURULUM.md)** |
| Makine okunur envanter | `katalog/skills.json` · `katalog/skills.csv` |

## Kategoriler

| # | Kategori | Adet | Kapsam |
|---|---|---|---|
| 01 | **[Finans & Yatırım](kutuphane/01-finans-yatirim/)** | 13 | Helal/katılım yatırım, portföy kalibrasyonu, bütçe, vergi, fiyatlandırma, değerleme |
| 02 | **[Masifico — Ahşap Oyuncak](kutuphane/02-masifico-ahsap-oyuncak/)** | 19 | Tasarım → üretim → kalite → CE mevzuatı → pazar zinciri |
| 03 | **[Video & Ses Üretimi](kutuphane/03-video-ses-uretim/)** | 15 | Fizik/ambient video hatları, besteleme, plak etiketi, kanal, prosedürel ses |
| 04 | **[İçerik, Yazım & Çeviri](kutuphane/04-icerik-yazim-ceviri/)** | 14 | Doğal Türkçe, dikey video anlatısı, çok dilli çeviri, içerik stratejisi |
| 05 | **[Pazarlama & Büyüme](kutuphane/05-pazarlama-buyume/)** | 10 | SEO/ASO denetimi, Shorts optimizasyonu, viral ürün avı, lead üretimi |
| 06 | **[UX & Ürün Yönetimi](kutuphane/06-ux-urun/)** | 12 | Mobil/web akış tasarımı ve denetimi, ürün kararı incelemesi |
| 07 | **[Yazılım Mühendisliği](kutuphane/07-yazilim-muhendislik/)** | 21 | Framework/altyapı referansları, kod grafiği, çoklu bulut, sunucu operasyonu |
| 08 | **[AI & Makine Öğrenmesi](kutuphane/08-ai-ml/)** | 8 | Kaggle/ML iş akışı, AutoML, LLM ve SLM mimarisi, GPU hibeleri |
| 09 | **[CAD & Görsel Üretim](kutuphane/09-cad-gorsel/)** | 9 | Parametrik mobilya zinciri, markalı görsel hattı, sunum tasarımı, stok görsel keşfi |
| 10 | **[Yaşam & Türkiye Hizmetleri](kutuphane/10-yasam-turkiye/)** | 13 | Satın alma, seyahat, vize, hak arama, mahremiyet, etkinlik, bölgesel mevzuat |
| 11 | **[Öğrenme & Dil](kutuphane/11-ogrenme/)** | 3 | Arapça ve İngilizce koçluğu, genel öğrenme rehberliği |
| 12 | **[Marka & Müşteri Projeleri](kutuphane/12-marka-musteri/)** | 4 | Markaya bağlı kimlik, içerik ve mevzuat kaynakları |
| 13 | **[Ofis & Belge](kutuphane/13-ofis-belge/)** | 4 | Word/PowerPoint/Excel/PDF (Anthropic yerleşik) |
| 14 | **[Meta & Sistem](kutuphane/14-meta-sistem/)** | 9 | Skill yazımı ve değerlendirmesi, hafıza, zamanlama, kurulum |

Her kategori klasöründe, o kategorideki her skill'in tam açıklamasını ve ölçüsünü
veren bir `README.md` var.

## Öne çıkan zincirler

Skill'lerin çoğu tek başına değil, birbirini çağıran zincirler halinde çalışıyor.
En olgun dördü:

**Masifico (ahşap oyuncak, uçtan uca üretim)**
`oyuncak-pazar-radari` → `masifico-farklilasma` → `masifico-uretim-muhendisi` →
`masifico-tedarik-rfq` → `masifico-parti-uretim` → `masifico-kalite-izlenebilirlik` →
`oyuncak-mevzuat` → `masifico-teknik-dosya` → `masifico-maliyet-fiyat` →
`masifico-urun-gorsel` / `masifico-video-uretim`

**Weft Records (müzik yayını)**
`suno-composer` (beste) → `retro-record-label` (kapak + isim) →
`ambient-video-forge` / `stock-footage-forge` (video) →
`healing-audio-youtube-seo` (başlık) → `weft-release` (katalog) → `weft-channel` (yayın sonrası)

**Portföy & para**
`portfoy-tahmin` (tahmin defteri) → `tahmin-savcisi` (adversaryal denetim) →
`helal-portfoy-uzmanlari` (panel yorumu) + `harcama-analizi` (ekstre) +
`helal-yatirim-uzmani` (fıkhi süzgeç) + `sahis-vergi-yukumluluk` (vergi)

**ComeSyria (çok dilli içerik sitesi)**
`backlog-arastir` (aday) → `icerik-strateji` (sıra) → `yeme-icme` (süzgeç) →
`icerik-uret` (üretim) → `ceviri` (TR/EN/AR) → `sosyal-medya-post-uret` (dağıtım)

## Bakım

```bash
python3 scripts/katalog_uret.py
```

`kutuphane/` tek doğruluk kaynağıdır. Skill ekledikten, sildikten veya bir
açıklamayı değiştirdikten sonra bunu çalıştır — `INDEX.md`, kategori
`README.md`'leri ve `katalog/` yeniden üretilir.

Kaynak konumlarını bu kütüphaneye bağlamak (symlink) için: **[TASIMA.md](TASIMA.md)**.
