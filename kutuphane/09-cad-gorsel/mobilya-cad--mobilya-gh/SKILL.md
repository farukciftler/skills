---
name: mobilya-cad
description: Levha mobilya (suntalam/MDF dolap, ayakkabılık, gardırop, raf ünitesi, TV ünitesi, mutfak modülü) tasarımını uçtan uca üretim paketine çeviren mühendislik zinciri — parametrik 3B katı model (build123d → STEP/GLB/STL), ölçülendirilmiş teknik çizim (ezdxf → görünüş + kesit + antet, DXF/PDF/PNG), kesim listesi ve BOM (net/kesim ölçüsü, bant payı düşülmüş), kenar bandı metrajı, giyotin kesim optimizasyonu ve fire raporu, parça başına CNC DXF (R12), ve Blender 5.2 ile foto-gerçekçi render, PBR doku/mesh texture, USDZ/GLB çıktısı. Kullanıcı "ayakkabılık", "dolap", "gardırop", "raf", "mobilya çiz", "3D model", "render", "teknik çizim", "kesit", "görünüş", "ölçülendir", "kesim listesi", "parça listesi", "BOM", "kaç levha çıkar", "fire", "yerleşim/nesting", "kenar bandı", "DXF", "CNC dosyası", "malzeme listesi", "raf sarkar mı", "kaç çift alır", "texture", "kaplama", "doku", "mesh", "görsel/sunum" dediğinde; bir mobilya ölçülendirilirken, malzeme/donanım seçilirken, üretime gönderilecek dosya hazırlanırken veya ürün görseli istendiğinde bu skill'i kullan. 32'lik sistem, minifix/kavela/menteşe delik tabloları, EN 312 P2 sehim limitleri, EN 14749 devrilme eşiği, kenar bandı payı ve desen yönü kuralları hesaplara gömülüdür.
---

# Mobilya CAD — levhadan üretim paketine

Görev: bir mobilya fikrini **atölyeye soru sordurmadan üretilebilecek**
dosya paketine ve **müşteriye gösterilebilecek görsele** çevirmek — tamamı
bu Mac'te, terminalden.

Tek doğruluk kaynağı **parametrik Python modelidir**. Çizim, BOM, kesim
planı, CNC dosyası ve render hepsi ondan türer. Çıktı dosyaları elle
düzenlenmez — script değiştirilip yeniden çalıştırılır.

## Araç zinciri (bu Mac'te doğrulandı — Ağustos 2026)

| İş | Araç | Not |
|---|---|---|
| Alan kuralları, BOM, bant, nesting, sehim | **`mobilya.py`** (saf Python) | Ağır bağımlılık yok |
| Parametrik 3B, kesit, gizli-çizgi görünüş | **build123d 0.11.1** | OCCT HLR; STEP/GLB/STL |
| Ölçülü teknik çizim → DXF/PDF/PNG | **ezdxf 1.4.4** + PyMuPDF | Gerçek `DIMENSION` varlıkları |
| CNC DXF (R12) | build123d `ExportDXF(version="AC1009")` | Katman adında çap/derinlik |
| Render · doku · ışık · USDZ/GLB | **Blender 5.2 LTS** | Cycles + Metal GPU |
| CC0 PBR doku / HDRI indirme | **`doku_indir.py`** | ambientCG + Poly Haven |

Kurulum: `bash scripts/kurulum.sh` (venv `~/mobilya-venv`).
**Kurulum, API ayrıntıları ve 12 doğrulanmış tuzak: `references/toolchain.md`.**
**Levha/donanım/standart verileri: `references/malzeme-donanim.md`.**

> **Blender teknik çizim için KULLANILMAZ.** Ölçülendirme sistemi yoktur,
> Grease Pencil SVG çıktısı ölçekli değildir, panel ölçüsü değişince elle
> konmuş yazılar sessizce eskir. 2B iş ezdxf'te kalır. FreeCAD TechDraw
> macOS'ta headless çalışmaz (segfault), CadQuery'de HLR yoktur.

## Akış — tek çağrı

Ürün tanımlanır, `paketle()` gerisini yapar: geometri → çizim → BOM →
kesim planı → CNC → 9 görünüş render → tasarım dosyası PDF.

```python
from dolap import Dolap, Bolge
from paket import paketle

d = Dolap(genislik=600, derinlik=260, yukseklik=1850, kod="AYK-01",
          ad="MONOLİT", tam_kapak=None, baza_icerlek=50.0,
          bolgeler=[Bolge("raf", 1734, kapak="tek", egim=45.0,
                          raf_kotlari=(430, 630, 830, 1030, 1230, 1430))])
paketle(d, "cikti", doku="dokular/oak_veneer_02")
```

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
  <KOD>-CIZIM.pdf/.dxf/.png     ← ölçülü A3 teknik çizim
  <KOD>-<malzeme>-kesim-plani.* ← levha yerleşimi + verim
  <KOD>.step/.glb/.stl          ← 3B model
  cnc/<parça>.dxf               ← parça başına CNC (R12)
  render/  9 görünüş + goruntuler.json (açıklama VE ölçü pikselleri)
  render_notlari.json           ← açıklamaların 3B konumları
  render_olculeri.json          ← render üzerine çizilen ölçülerin 3B uçları
```

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

**Açıklama sayfalarındaki oklu notlar ÖLÇÜ İÇERMEZ.** Render "bu ne"
anlatır. Açıklamalar `Dolap.render_notlari()`'nden gelen **3B noktalara
bağlıdır** — Blender `world_to_camera_view` ile piksele çevrilir,
etiketler sol/sağ sütuna dağıtılıp dikeyde çakışmaz.

**Ölçüler renkli görselde de görünür — ama elle yazılarak değil.**
`Dolap.render_olculeri()` ölçü çizgilerinin uçlarını **3B dünya
koordinatında** verir (zincir kotları `kot_zinciri()`'nden, yani teknik
çizimle AYNI kaynaktan); `render.py::olcu_pikselleri()` bunları kamera
izdüşümüyle piksele çevirir; `belge.py` ölçü çizgisini, uç tiklerini ve
rakamı rendera oturtur, çakışan rakamı kılavuz çizgisiyle dışarı iter.
Ölçü değişince çizgi de rakam da kendiliğinden yerine düşer.
**Bağlayıcı ölçü yine teknik çizimdedir** — sayfa altında yazılıdır.

Spec-sheet kuralı: **belirsiz sıfat yazma.** "Kaliteli levha" değil,
"EN 312 P2, 18 mm, E1, 2 mm PVC bant".

## Üretim paketi standardı (her SKU için 7 parça)

1. **Kesim listesi / BOM** (`*-BOM.csv`) — parça kodu, **net ölçü VE kesim
   ölçüsü ayrı sütun**, kalınlık, adet, malzeme, desen kodu (L/W/—),
   kenar bandı deseni (L1/L2/W1/W2), alan, ağırlık, not.
2. **Ölçülü teknik çizim** (`*-CIZIM.pdf/.dxf/.png`) — ön + yan + plan +
   kesit A-A, gizli çizgiler, zincir ölçü, ISO antet, ölçek sayfada yazılı.
3. **Kesim planı** (`*-kesim-plani.pdf`) — levha başına yerleşim, parça
   kodları, dönme işareti, **verim yüzdesi**.
4. **CNC DXF** (`cnc/*.dxf`) — parça başına, R12, origin sol-alt, delikler
   gerçek çapında daire, derinlik katman adında.
5. **3B model** — `.step` (master), `.glb` (render/web), `.stl`.
6. **Render seti** — hero + gerekiyorsa turntable; müşteriye çizim değil
   **görsel** gider. Görselsiz paket teslim edilmez.
7. **Mühendislik raporu** (`*-RAPOR.txt`) — kapasite, sehim kontrolü,
   devrilme kontrolü, **uyarılar**.

## Tasarımdan önce daima netleştir

Ölçü, malzeme ve dekor netleşmeden çizim başlamaz:

* **Dış ölçü** (G × D × Y) ve baza yüksekliği
* **Malzeme + kalınlık + DEKOR** — dekor 18 mm dışında çöker, kalınlıkla
  birlikte teyit et
* **Kapak tipi**: devrilir / bindirmeli menteşeli / iç takma / açık
* **Bant sözleşmesi**: atölyeye NET ölçü mü, kesim ölçüsü mü gidiyor
* **Desen yönü** kilitli mi (dekorluysa görünen parçalarda evet)

## Hesaba gömülü kurallar (sessizce uygulanır, ihlalde UYARI verir)

| Kural | Değer | Kaynak |
|---|---|---|
| **18 mm suntalam raf açıklığı** | **≤ 750 mm** (E = 1600 MPa, 65 kg/m², L/240, ×1.5 sünme) | EN 312 P2 / CPA |
| Devrilme testi tetiği | yükseklik > 600 mm **VE** h_cg(m) × kütle(kg) > 6 | EN 14749 6.2.1 |
| Devrilme braketi | **rijit metal** — kayış/kablo bağı OLMAZ | EN 14749 3.17 |
| Bant payı | kesim = net − (bant × o eksendeki banlı kenar), eşik ≥1.0 mm | MEGEP |
| Bant genişliği | panel kalınlığı **+ 4 mm** (18 → 22 mm) | sabittuncel |
| Bant kesim payı | banlı kenar başına **35–40 mm** + %8–12 fire | sabittuncel |
| 32'lik sistem | adım 32, Ø5×13, ön kenardan **37 mm** | Euro32 / Hettich |
| Minifix (18 mm) | göbek Ø15 × **13.5 mm**, cıvata Ø8, eksen **B = 34 mm** | Häfele |
| Menteşe | kap Ø35 × 11.5–12.8; vida aralığı **Blum 45 / Hettich 52** | Blum / Hettich |
| Devrilir mekanizma | 1/2/3 sıra → min derinlik **189 / 255 / 310 mm**, ara raf **10 mm**, iç genişlik **−25 mm** | Häfele Dresscode |
| Levha | 2100 × 2800 (AB menşei 2070!), tolerans **±0.3 mm** | Starwood |
| Ayakkabı | boy **320 mm**, çift **185 mm**, raf aralığı **180 mm** | ölçüm + gerçek ürün |
| **Eğimli rafın yatay yeri** | `derinlik·cosθ + **T·sinθ**` — panelin KALINLIĞI da yatayda yer kaplar (18 mm/45° = 12.7 mm). Atlanırsa raf arkalığı deler, arkadan bakışta her rafta şerit görünür | geometri — `raf_derinligi(egim)` |
| **Eğimli rafın tepe noktası** | ön-ÜST köşe = kot + `derinlik·sinθ + T·cosθ`. Yükleme açıklığı buradan ölçülür | geometri — `yukleme_acikligi()` |
| Eğimli rafta göz sayımı | dik açıklık ≥ **120 mm**; EN ÜST rafın ön-üst köşesi ile tavan arası (yükleme açıklığı) ≥ **150 mm**; EN ALT gözün tabanı DÜZ olduğundan iç derinlik < ayakkabı boyu ise o göz sayılmaz; eğimli rafın üstündeki 400 mm+ göz **çizme hacmi değildir** (çizme dik duramaz) | geometri — `_goz_kapasitesi()` |
| Uzun çizme (dik) | net yükseklik **400–450 mm** | ayakkabı kutusu ölçüleri |
| Arkalık kanalı | 3 mm panel → 4 mm kanal × 8 mm derin, arkadan 12 mm; derinlik ≤ %50 | atölye pratiği |

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
* ~1 m mobilyada anahtar ışık **100–110 W** (500 W albedo'yu patlatır).
* Beyaz fon seviyesi view transform'a bağlıdır: Standard 1.0 ·
  Khronos 4.0 · AgX 16.0 — ve `film_transparent` açık olmalı.

## Dosyalar

```
scripts/
  mobilya.py       ← alan çekirdeği: malzeme, Parca, BOM, bant, giyotin
                     optimizasyon, sehim, devrilme, donanım delik tabloları
  cizim.py         ← build123d + ezdxf: 3B kur, HLR görünüş, kesit,
                     ölçülü A3 sayfa, CNC DXF, kesim planı
  render.py        ← Blender 5.2: UV, PBR/prosedürel materyal, kenar bandı
                     slotu, stüdyo ışık, kamera, Cycles, beyaz fon, USDZ
  dolap.py         ← BÖLGE tabanlı üreteç: raf/çizme/açık/devrilir/askı
                     bölgeleri, eğimli raf, tam boy kapak, kaide hizası,
                     askı borusu, ön alın paneli, kot zinciri + render ölçüleri
  belge.py         ← tasarım dosyası PDF şablonu (7 sayfa, Türkçe TTF gömülü)
  paket.py         ← CAD + render + PDF tek çağrıda  ⭐ giriş noktası
  ayakkabilik.py   ← eski sabit-düzen üreteç (dolap.py'yi tercih et)
  doku_indir.py    ← CC0 doku + HDRI indirici
  kurulum.sh
references/
  toolchain.md         ← API + 12 doğrulanmış tuzak + CNC katman sözleşmeleri
  malzeme-donanim.md   ← levha, bant, donanım, ayakkabı ölçüleri, EN standartları
```

Yeni bir ürün tipi için `ayakkabilik.py`'yi kalıp al: `_parcalar()` parça
listesini, `_yerlestir()` 3B konumları, `_hesapla()` kontrolleri kurar.
Kontroller `mobilya.py`'den gelir — ölçü değişince kendiliğinden yeniden koşar.

## Dürüstlük kuralları

* Raporda **uyarıları gizleme.** Sehim veya mekanizma derinliği tutmuyorsa
  çizim yine üretilir ama uyarı raporun başında durur.
* `optimize_dogrula()` her yerleşimden sonra çalışır — sessiz çakışma en
  pahalı hata türüdür.
* Doğrulanmamış sayıyı kural diye yazma. `references/`'ta ❌ ile
  işaretlenmiş kalemler (mekanizma taşıma kapasitesi, E1'in Türkiye'de
  yasal zorunluluğu, havalandırma açık alan yüzdesi) **bağlayıcı belgeye
  girmez** — gerekirse üreticiden yazılı iste.
* Ölçünün **net mi kesim mi** olduğunu her teslimde açıkça yaz.
* **Ölçüyü nominal değişkenden değil, çizilen geometriden al.** Kapak veya
  baza gövdeden taşınca (ör. kapak yüzeyi +18 mm) nominal ölçü yalan söyler.
  `coklu_gorunus()` görünüşü ölçer; ölçülendirme `model_gen`/`model_yuk`
  kullanır, antet de öyle.
