---
name: mobilya-cad
description: Levha mobilya (suntalam/MDF dolap, ayakkabılık, gardırop, raf, TV ünitesi) tasarımını parametrik Python modelinden üretim ve sunum paketine çeviren zincir: build123d 3B (STEP/GLB/STL), ezdxf ölçülü teknik çizim (görünüş + kesit + antet, DXF/PDF/PNG), kesim listesi ve BOM (net/kesim ölçüsü, bant payı düşülmüş), donanım listesi, kenar bandı metrajı, giyotin nesting ve fire, parça başına CNC DXF (R12), Blender 5.2 render ve 8 sayfalık tasarım dosyası PDF. Kullanıcı "ayakkabılık", "dolap", "gardırop", "raf", "mobilya çiz", "3D model", "render", "teknik çizim", "kesit", "ölçülendir", "kesim listesi", "BOM", "kaç levha çıkar", "fire", "nesting", "kenar bandı", "DXF", "CNC", "malzeme listesi", "raf sarkar mı", "kaç çift alır", "askı sığar mı", "doku", "görsel" dediğinde ya da bir mobilya ölçülendirilir, malzeme/donanım seçilir veya üretime dosya hazırlanırken kullan. 32'lik sistem, minifix/menteşe delikleri, EN 312 P2 sehim, EN 14749 devrilme, askı derinliği ve desen yönü kuralları hesaplara gömülüdür.
---

# Mobilya CAD — levhadan üretim paketine

Görev: bir mobilya fikrini **atölyeye soru sordurmadan üretilebilecek**
dosya paketine ve **müşteriye gösterilebilecek görsele** çevirmek — tamamı
bu Mac'te, terminalden.

Tek doğruluk kaynağı **parametrik Python modelidir**. Çizim, BOM, donanım
listesi, kesim planı, CNC dosyası, render ve PDF hepsi ondan türer. Çıktı
dosyaları elle düzenlenmez — model değiştirilip yeniden çalıştırılır.

## Araç zinciri (bu Mac'te doğrulandı — Ağustos 2026)

| İş | Araç | Not |
|---|---|---|
| Alan kuralları, BOM, donanım, bant, nesting, sehim, askı | **`mobilya.py`** (saf Python) | Ağır bağımlılık yok |
| Yerleşim veri tipleri (`Yerlestirme`, `Boru`) | **`geometri.py`** (saf Python) | dolap/gardirop CAD'siz çalışır |
| Bölge tabanlı gövde üreteci | **`dolap.py`** → `Dolap`, `Bolge` | tek kolon |
| Sütunlu gövde üreteci | **`gardirop.py`** → `Gardirop`, `Sutun` | `Dolap`'tan türer |
| Parametrik 3B, kesit, gizli-çizgi görünüş | **build123d 0.11.1** | OCCT HLR; STEP/GLB/STL |
| Ölçülü teknik çizim → DXF/PDF/PNG | **ezdxf 1.4.4** + PyMuPDF | Gerçek `DIMENSION` varlıkları |
| CNC DXF (R12) | build123d `ExportDXF(version="AC1009")` | Katman adında çap/derinlik |
| Tasarım dosyası PDF | **reportlab 5.0.1** | Türkçe TTF gömülü |
| Render · doku · ışık · USDZ/GLB | **Blender 5.2 LTS** | Cycles + Metal GPU |
| CC0 PBR doku / HDRI indirme | **`doku_indir.py`** | ambientCG + Poly Haven |

Kurulum: `bash scripts/kurulum.sh` (venv `~/mobilya-venv`, sürümler
`requirements.txt`'te sabit). Ortam değişkenleri: `MOBILYA_VENV`,
`MOBILYA_PYTHON`, `MOBILYA_BLENDER`, `MOBILYA_FONT_DIR`.
**Kurulum, API ayrıntıları ve 12 doğrulanmış tuzak: `references/toolchain.md`.**
**Levha/donanım/askı/standart verileri: `references/malzeme-donanim.md`.**

> **Blender teknik çizim için KULLANILMAZ.** Ölçülendirme sistemi yoktur,
> Grease Pencil SVG çıktısı ölçekli değildir, panel ölçüsü değişince elle
> konmuş yazılar sessizce eskir. 2B iş ezdxf'te kalır. FreeCAD TechDraw
> macOS'ta headless çalışmaz (segfault), CadQuery'de HLR yoktur.

## Testler — her kural değişikliğinden sonra

```bash
~/mobilya-venv/bin/python -m unittest discover -s .claude/skills/mobilya-cad/tests
```

`tests/` build123d İSTEMEZ (sistem python3 ile de koşar): bant payı,
nesting çakışması, sehim formülü, devrilme tetiği, askı yönü, eğimli raf
geometrisi, `Dolap`/`Gardirop` parça-yerleşim tutarlılığı, uyarı kuralları.
Yeni kural = yeni test. Kırmızı testle paket üretilmez.

## Akış — tek çağrı

Ürün tanımlanır, `paketle()` gerisini yapar: geometri → çizim → BOM +
donanım → kesim planı → CNC → 9 görünüş render → 8 sayfa PDF.

```python
from dolap import Dolap, Bolge
from paket import paketle

d = Dolap(genislik=600, derinlik=260, yukseklik=1850, kod="AYK-01",
          ad="MONOLİT", tam_kapak="tek", baza_icerlek="kapak",
          bolgeler=[Bolge("raf", 1502, egim=48.0,
                          raf_kotlari=(82, 285, 488, 691, 894, 1097)),
                    Bolge("raf", 214, raf=0, ayakkabi=False)])
sonuc = paketle(d, "cikti", doku="dokular/oak_veneer_02")
assert not sonuc["hatalar"], sonuc["hatalar"]     # render/nesting/PDF
print(sonuc["uyarilar"])                          # tasarım uyarıları
```

Sütunlu gövde (yan yana bölmeler, orta dikme, çekmece, yorgan gözü, L gövde):

```python
from gardirop import Gardirop, Sutun
g = Gardirop(genislik=1100, derinlik=482, yukseklik=2100, kapak="sutun",
             baza_icerlek="kapak", kod="GRD-A", ad="SADE",
             sutunlar=[Sutun([Bolge("aski", 1500, kiyafet="palto"),
                              Bolge("raf", 448, raf=0, ayakkabi=False)]),
                       Sutun([Bolge("cekmece", 700, raf=3),
                              Bolge("raf", 1248, raf=3, ayakkabi=False)])])
paketle(g, "cikti", olcek=20.0)
```

`kapak`: `"sutun"` her sütuna tek kanat · `"cift"` her sütuna çift dar kanat
· `Sutun(kapak="yok")` o sütun açık. `ortak_alt=Bolge(...)` + `kusak=100`
tam genişlik alt bölme; `Sutun(ust_yukseklik=0)` L gövde.

`paketle(..., render=False)` mevcut renderlarla PDF'i tazeler (BOM/kural
değişikliğinde Blender'ı beklemeden). `siki=True` hatayı exception yapar.

Ürün tanımları repo kökünde `uret_<urun>.py` dosyalarındadır (örn.
`uret_final.py` AYK-01, `uret_gardirop110.py` GRD-A..D). Modelin
nesnesi modül seviyesinde tanımlanır, `main()` paketler — testler ve
toplu yenileme betikleri onları import edebilir.

Doku bir kez indirilir (CC0, atıf gerekmez):
```bash
python3 doku_indir.py --ph oak_veneer_02 --klasor dokular
python3 doku_indir.py --liste ahsap     # doğrulanmış varlık listesi
```

## Klasör standardı — her mobilya KENDİ klasöründe

```
cikti/<KOD>/
  <KOD>-TASARIM-DOSYASI.pdf     ← müşteriye/atölyeye giden TEK dosya (8 sayfa)
  <KOD>-RAPOR.txt               ← mühendislik raporu + uyarılar
  <KOD>-BOM.csv                 ← kesim listesi (net VE kesim ölçüsü ayrı)
  <KOD>-DONANIM.csv             ← menteşe, boru, flanş, ray, braket
  <KOD>-CIZIM.pdf/.dxf/.png     ← ölçülü A3 teknik çizim
  <KOD>-<malzeme>-kesim-plani.* ← levha yerleşimi + verim
  <KOD>.step/.glb/.stl          ← 3B model
  cnc/<parça>.dxf               ← parça başına CNC (R12)
  render/  9 görünüş + goruntuler.json (açıklama VE ölçü pikselleri)
  render_notlari.json           ← açıklamaların 3B konumları
  render_olculeri.json          ← render üzerine çizilen ölçülerin 3B uçları
```

Git'te yalnız hafif teslimatlar tutulur (PDF, CSV, TXT, JSON); render PNG,
STEP/GLB/STL, CNC ve kesim planı DXF/PNG `.gitignore`'dadır — script'ten
yeniden üretilir.

## Tasarım dosyası PDF — 8 sayfa

1. **Kapak** — tek büyük kapalı render, ad, kod, açıklama, künye şeridi
   (dış ölçü **Y×G×D**, gövde, kapasite, ağırlık)
2. **Görünüşler** — ön · sağ · arka · sol · üç çeyrek · üst (kapalı)
3. **Ölçülü görsel** — renkli render ÜZERİNDE ölçü zinciri + dış ölçüler
4. **Açık hâl** — açıklama oklu render
5. **İç detay** — yakın açıklama oklu render
6. **Teknik çizim** — A3 yatay sayfa
7. **Kesim listesi** — BOM tablosu + malzeme/levha/bant özeti
8. **Donanım ve üretim notları** — donanım, iç düzen, kontroller, uyarılar

Render sayfaları render yoksa düşer; sayfa sayısı buna göre azalır.

**Açıklama sayfalarındaki oklu notlar ÖLÇÜ İÇERMEZ.** Render "bu ne"
anlatır. Açıklamalar `render_notlari()`'nden gelen **3B noktalara
bağlıdır** — Blender `world_to_camera_view` ile piksele çevrilir,
etiketler sol/sağ sütuna dağıtılıp dikeyde çakışmaz.

**Ölçüler renkli görselde de görünür — ama elle yazılarak değil.**
`render_olculeri()` ölçü çizgilerinin uçlarını **3B dünya koordinatında**
verir (zincir kotları `kot_zinciri()`'nden, yani teknik çizimle AYNI
kaynaktan); `render.py::olcu_pikselleri()` bunları kamera izdüşümüyle
piksele çevirir; `belge.py` ölçü çizgisini, uç tiklerini ve rakamı rendera
oturtur, çakışan rakamı kılavuz çizgisiyle dışarı iter. **Bağlayıcı ölçü
yine teknik çizimdedir** — sayfa altında yazılıdır.

Spec-sheet kuralı: **belirsiz sıfat yazma.** "Kaliteli levha" değil,
"EN 312 P2, 18 mm, E1, 2 mm PVC bant".

## Üretim paketi standardı (her SKU için 8 parça)

1. **Kesim listesi / BOM** (`*-BOM.csv`) — parça kodu, **net ölçü VE kesim
   ölçüsü ayrı sütun**, kalınlık, adet, malzeme, desen kodu (L/—),
   kenar bandı deseni (L1/L2/W1/W2), alan, ağırlık, not.
2. **Donanım listesi** (`*-DONANIM.csv`) — kod, ad, ölçü, adet, montaj notu.
   Levha değildir; satın almaya gider. Askı borusu boyu burada.
3. **Ölçülü teknik çizim** (`*-CIZIM.pdf/.dxf/.png`) — ön + yan + plan +
   kesit A-A, gizli çizgiler, zincir ölçü, ISO antet, ölçek sayfada yazılı.
4. **Kesim planı** (`*-kesim-plani.pdf`) — levha başına yerleşim, parça
   kodları, dönme işareti, **verim yüzdesi**.
5. **CNC DXF** (`cnc/*.dxf`) — parça başına, R12, origin sol-alt, delikler
   gerçek çapında daire, derinlik katman adında.
6. **3B model** — `.step` (master), `.glb` (render/web), `.stl`.
7. **Render seti** — hero + gerekiyorsa turntable; müşteriye çizim değil
   **görsel** gider. Görselsiz paket teslim edilmez.
8. **Mühendislik raporu** (`*-RAPOR.txt`) — kapasite, sehim, devrilme,
   **uyarılar** (malzeme özetinden önce), donanım.

## Tasarımdan önce daima netleştir

Ölçü, malzeme ve dekor netleşmeden çizim başlamaz:

* **Dış ölçü** (G × D × Y) ve baza yüksekliği — kapak dahil mi? (`Dolap`'a
  GÖVDE derinliği verilir; kapak +18 mm dışa taşar, antet bunu ölçer)
* **Malzeme + kalınlık + DEKOR** — dekor 18 mm dışında çöker, kalınlıkla
  birlikte teyit et
* **Kapak tipi**: devrilir / bindirmeli menteşeli / iç takma / açık
* **Bant sözleşmesi**: atölyeye NET ölçü mü, kesim ölçüsü mü gidiyor
* **Desen yönü** kilitli mi (dekorluysa görünen parçalarda evet)
* Gardıropta **askı yönü**: 500 mm gövde (467 iç) sıkışık öne bakan,
  600 mm rahat; 350 mm altı yalnız profilden (`aski_yonu()` karar verir)

## Hesaba gömülü kurallar (sessizce uygulanır, ihlalde UYARI verir)

| Kural | Değer | Kaynak |
|---|---|---|
| **18 mm suntalam raf açıklığı** | **≤ 750 mm** (E = 1600 MPa, 65 kg/m², L/240, ×1.5 sünme) | EN 312 P2 / CPA |
| Geniş açıklık tavanı | ön **kuşak** ile L kesit — `kusakli_sehim()`, 100 mm kuşak I'yı ~15 kat artırır | mukavemet |
| Devrilme testi tetiği | yükseklik > 600 mm **VE** h_cg(m) × kütle(kg) > 6 | EN 14749 6.2.1 |
| Devrilme braketi | **rijit metal** — kayış/kablo bağı OLMAZ | EN 14749 3.17 |
| Bant payı | kesim = net − (bant × o eksendeki banlı kenar), eşik ≥1.0 mm | MEGEP |
| Bant genişliği | panel kalınlığı **+ 4 mm** (18 → 22 mm) | sabittuncel |
| Bant kesim payı | banlı kenar başına **35–40 mm** + %8–12 fire | sabittuncel |
| 32'lik sistem | adım 32, Ø5×13, ön kenardan **37 mm** | Euro32 / Hettich |
| Minifix (18 mm) | göbek Ø15 × **13.5 mm**, cıvata Ø8, eksen **B = 34 mm** | Häfele |
| Menteşe | kap Ø35 × 11.5–12.8; vida aralığı **Blum 45 / Hettich 52**; kanat başına 1600 mm üstü gövdede 4, altı 3 | Blum / Hettich |
| Devrilir mekanizma | 1/2/3 sıra → min derinlik **189 / 255 / 310 mm**, ara raf **10 mm**, iç genişlik **−25 mm** | Häfele Dresscode |
| **Askı yönü** | net iç derinlik ≥ **550** rahat öne bakan · **460–550** sıkışık (boru tam ortaya, 420 mm ince askı öner) · < 460 profilden (önden arkaya boru, **alın paneli** şart) | `ASKI`, ⚠ atölye |
| Askı kapasitesi | ray boyunca mm/parça: gömlek 40 · ceket 60 · palto 100 | `ASKI_KALINLIK` ⚠ |
| Askı bölgesi net yükseklik | gömlek 900 · ceket 1100 · elbise 1400 · palto 1450 | `KIYAFET_BOYU_KONTROL` ⚠ |
| Çekmece ergonomisi | üst kenar ≤ **1350 mm**, çekmece yüksekliği 140–260 | atölye pratiği |
| Levha | 2100 × 2800 (AB menşei 2070!), tolerans **±0.3 mm** | Starwood |
| Ayakkabı | boy **320 mm**, çift **185 mm**, raf aralığı **180 mm** (`Bolge(ayakkabi_tipi=...)` bölge bazında ezer) | ölçüm + gerçek ürün |
| **Eğimli rafın yatay yeri** | `derinlik·cosθ + **T·sinθ**` — panelin KALINLIĞI da yatayda yer kaplar (18 mm/45° = 12.7 mm). Atlanırsa raf arkalığı deler | geometri — `raf_derinligi(egim)` |
| **Eğimli rafın tepe noktası** | ön-ÜST köşe = kot + `derinlik·sinθ + T·cosθ`. Yükleme açıklığı buradan ölçülür | geometri — `yukleme_acikligi()` |
| Eğimli rafta göz sayımı | dik açıklık ≥ **120 mm**; EN ÜST rafın ön-üst köşesi ile tavan arası ≥ **150 mm**; EN ALT gözün tabanı DÜZ olduğundan iç derinlik < ayakkabı boyu ise sayılmaz; eğimli rafın üstündeki 400 mm+ göz **çizme hacmi değildir** | geometri — `_goz_kapasitesi()` |
| Uzun çizme (dik) | net yükseklik **400–450 mm** | ayakkabı kutusu ölçüleri |
| Arkalık kanalı | 3 mm panel → 4 mm kanal × 8 mm derin, arkadan 12 mm; derinlik ≤ %50 | atölye pratiği |
| L gövde | dolapsız sütunun arkası **18 mm sırt paneli** + duvar braketi (yapısal) | `Gardirop` |

**Kanalı asla nominale açma** — 18 mm levha 17.7–18.3 arasıdır, partiyi ölç.
**Ebatlamadan önce düzeltme kesimi al** — 5.6 mm gönye sapması standartta yasaldır.

## Çizim sözleşmesi

Katmanlar: `00-CERCEVE · 01-GORUNEN · 02-GIZLI · 03-KESIT · 04-TARAMA ·
05-OLCU · 06-YAZI · 07-EKSEN`. Birim mm, ölçek antette yazılı, 3. açı izdüşüm.

`Sayfa.coklu_gorunus()` görünüşleri **önce ölçer**, sığmazsa ölçeği
otomatik büyütür (1:10 → 1:20 → 1:25 → 1:50). Kağıt dışına taşan çizim üretilmez.

## CNC teslim sözleşmesi

R12 (AC1009) · mm · 1:1 · origin sol-alt, tüm koordinatlar pozitif ·
yalnız `LINE/ARC/CIRCLE/POLYLINE` · delikler gerçek çapında tam daire ·
derinlik katman adında (`DELIK_5_13`) · panel konturu ayrı katmanda ·
**desen yönü ve kenar bandı DXF'te değil CSV'dedir** · varsayılan
**parça başına bir DXF + CSV** (atölyenin optimizatörü kendi kerfiyle nesting yapar).

Atölye Homag/Thermwood/TpaCAD şablonu istiyorsa katman adlarını
`references/toolchain.md`'deki tablodan uyarla — sabit değil, ayardır.

## Render sözleşmesi

* **Doku: gerçek CC0 PBR kullan.** `render.py::ahsap_prosedurel()` bir
  YEDEKTİR ve taranmış kaplamanın yerini tutmaz. `doku_indir.py` ile
  ambientCG/Poly Haven'dan indir (ikisi de CC0, atıf gerekmez).
  ⚠ sharetextings/freepbr/Poliigon **kullanma** — ToS botla indirmeyi
  yasaklıyor, ücretsiz katman ticari değil, ya da üyelik duvarı var.
* **Düz beyaz melamin dokusu hiçbir CC0 sitede YOK** — `melamin()`
  prosedürel üretir.
* **Renk yönetimi**: katalog/dekor rengi tutmalıysa `Standard` + 5000 K;
  pazarlama görselinde `Khronos PBR Neutral`. `look = 'None'`.
* **UV veri seviyesinde yazılır** (`kutu_uv`), `bpy.ops.uv.*` kullanılmaz —
  desen yönü parça bazında kontrol edilir, yatay tabla ile dikey panel
  farklı materyal varyantı alır.
* **Kenar bandı ayrı geometri değil, 2. materyal slotudur** (`bant_ata`).
  Panel kenarına 0.3–0.5 mm pah koy.
  `paketle(..., bant="antrasit")` rengi seçer; `bant="ayni"` dekor baskılı
  PVC bant görünümü için gövde materyalini kullanır.
* ~1 m mobilyada anahtar ışık **100–110 W** (500 W albedo'yu patlatır).
* Beyaz fon seviyesi view transform'a bağlıdır: Standard 1.0 ·
  Khronos 4.0 · AgX 16.0 — ve `film_transparent` açık olmalı.

## Dosyalar

```
requirements.txt   ← sabitlenmiş sürümler (build123d, ezdxf, PyMuPDF, Pillow, reportlab)
scripts/
  mobilya.py       ← alan çekirdeği: malzeme, Parca, BOM, donanım CSV, bant,
                     giyotin optimizasyon, sehim/kuşak, devrilme, askı,
                     donanım delik tabloları
  geometri.py      ← Yerlestirme, Boru (CAD bağımsız yerleşim tipleri)
  dolap.py         ← BÖLGE tabanlı üreteç + ORTAK yardımcılar (yan/tabla/
                     kapak/baza/arkalık parça + yerleşim, rapor iskeleti,
                     kot zinciri, render ölçüleri) + uret()  ⭐ taban sınıf
  gardirop.py      ← SÜTUNLU üreteç (Dolap'tan türer): dikme, kuşaklı ortak
                     alt bölme, çekmece, aynalı arkalık, L gövde
  cizim.py         ← build123d + ezdxf: 3B kur, HLR görünüş, kesit,
                     ölçülü A3 sayfa, CNC DXF, kesim planı
  render.py        ← Blender 5.2: UV, PBR/prosedürel materyal, kenar bandı
                     slotu, stüdyo ışık, kamera, Cycles, beyaz fon, USDZ
  belge.py         ← tasarım dosyası PDF şablonu (8 sayfa, Türkçe TTF gömülü)
  paket.py         ← CAD + render + PDF tek çağrıda  ⭐ giriş noktası
  doku_indir.py    ← CC0 doku + HDRI indirici
  kurulum.sh       ← venv + requirements + Blender kontrolü + testler
tests/
  test_mobilya.py  ← çekirdek kurallar      (saf Python)
  test_dolap.py    ← Dolap geometri/uyarı   (saf Python)
  test_gardirop.py ← Gardirop sütun/L gövde (saf Python)
references/
  toolchain.md         ← API + 12 doğrulanmış tuzak + CNC katman sözleşmeleri
  malzeme-donanim.md   ← levha, bant, donanım, askı, ayakkabı ölçüleri, EN standartları
```

**Yeni ürün tipi için `Dolap`'tan türet** (`gardirop.py` kalıptır):
`_duzen_ve_kontroller()` kotları ve uyarıları, `_parcalar()` parça listesini
(ortak yardımcılarla: `_parca_yan`, `_parca_tabla`, `_parca_kapak`,
`_parca_baza`, `_parca_arkalik`), `_yerlestir()` 3B konumları
(`_yerlestir_govde_kutusu`, `_yerlestir_kanatlar`, `_yerlestir_baza`,
`_yerlestir_arkalik`), `_kapasite()` sayımı kurar; `_rapor_duzen()` ve
`_rapor_yapisal()` raporun yalnız ürüne özgü bölümlerini ezer. Kontroller
`mobilya.py`'den gelir — ölçü değişince kendiliğinden yeniden koşar. Sonra
`tests/`'e ürün testi ekle.

## Dürüstlük kuralları

* Raporda **uyarıları gizleme.** Sehim veya mekanizma derinliği tutmuyorsa
  çizim yine üretilir ama uyarı raporda malzeme özetinden ÖNCE durur.
* `paketle()` dönüşündeki **`hatalar` ve `render_ok`'a bak.** Render veya
  PDF düşerse paket yine yazılır ama hata listesi boş değildir; toplu
  üretimde `siki=True` kullan. "Başarılı" demek için `hatalar == []` şart.
* `optimize_dogrula()` her yerleşimden sonra çalışır — sessiz çakışma en
  pahalı hata türüdür; sonucu `yerlesim_hatalari`'nda görünür.
* Doğrulanmamış sayıyı kural diye yazma. `references/`'ta ❌ ile
  işaretlenmiş kalemler (mekanizma taşıma kapasitesi, E1'in Türkiye'de
  yasal zorunluluğu, havalandırma açık alan yüzdesi) **bağlayıcı belgeye
  girmez** — gerekirse üreticiden yazılı iste. ⚠ işaretli askı değerleri
  atölye pratiğidir, katalog değeri değil.
* Ölçünün **net mi kesim mi** olduğunu her teslimde açıkça yaz.
* **Ölçüyü nominal değişkenden değil, çizilen geometriden al.** Kapak veya
  baza gövdeden taşınca (ör. kapak yüzeyi +18 mm) nominal ölçü yalan söyler.
  `coklu_gorunus()` görünüşü ölçer; ölçülendirme `model_gen`/`model_yuk`
  kullanır, antet de öyle.
