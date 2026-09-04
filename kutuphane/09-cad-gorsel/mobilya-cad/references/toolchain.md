# Araç zinciri referansı — macOS Apple Silicon, Ağustos 2026

Bu belgedeki her API adı ve tuzak, bu Mac'te **çalıştırılarak** doğrulandı.
Sürümler: build123d **0.11.1** · ezdxf **1.4.4** · PyMuPDF · Pillow ·
Blender **5.2.0 LTS** (hash `fbe6228777e7`, 2026-07-14, bundled Python 3.13).

## Mimari kararı — neden bu bölünme

> `Yerlestirme`/`Boru` veri tipleri `geometri.py`'de durur; `dolap.py` ve
> `gardirop.py` build123d olmadan çalışır (BOM, rapor, testler). `cizim.py`
> bu tipleri katı modele çevirir ve aynı adlarla dışa açar.

| İş | Araç | Neden |
|---|---|---|
| Parametrik 3B, kesit, gizli-çizgi projeksiyon | **build123d** | OCCT `HLRBRep` ile gerçek HLR. Pip'le kurulur, Qt yok. |
| Ölçülü teknik çizim, DXF, PDF/PNG | **ezdxf** | Gerçek `DIMENSION` varlıkları; AutoCAD'de düzenlenebilir. |
| Kesim listesi, bant, sehim, nesting | **saf Python** (`mobilya.py`) | Ağır bağımlılık yok; CAD kurulu olmasa da çalışır. |
| Materyal, doku, ışık, render, USDZ/GLB | **Blender 5.2** | Cycles + Metal GPU; USDZ/glTF yerleşik. |

**Blender 2B teknik çizim için KULLANILMAZ.** Line Art'ın ortografik
kamerada boş SVG üreten eski hatası 5.2'de düzelmiş olsa da Blender'da
ölçülendirme sistemi (associative dimension, tolerans, antet, sayfa
ölçeği) hiç yoktur ve GP SVG çıktısı ölçekli değildir — `viewBox` çizgi
sınırlarına oturur. Panel ölçüsü değişince elle konmuş yazılar sessizce
eskir; mobilya işinin kaldıramayacağı hata biçimi budur.

**FreeCAD TechDraw da elenmiştir**: `exportPageAsPdf`/`AsSvg` yalnız
`TechDrawGui`'de kayıtlıdır (GUI'siz çalışmaz), headless export talebi
(FreeCAD #5710) hâlâ açık ve `-platform offscreen` çözümü macOS'ta
segfault veriyor.

**CadQuery elenmiştir**: `project_to_viewport` karşılığı yoktur — HLR
yapamaz. Ayrıca `cadquery-ocp` ile build123d'nin `cadquery-ocp-novtk`'sı
**aynı dosya yollarını** yazar; ikisi bir venv'de OCP'yi bozar
(`ImportError: cannot import name 'IVtkOCC_Shape'`). Tek istisnası
`DxfDocument(approx="arc")` — spline'ı gerçek ARC'a çevirir; gerekirse
AYRI bir venv'de kullan.

---

## Kurulum

```bash
bash scripts/kurulum.sh          # venv + requirements.txt + Blender kontrolü + testler
```

Elle:

```bash
/opt/homebrew/bin/python3.13 -m venv ~/mobilya-venv     # 3.10–3.13; 3.12/3.13 tercih
~/mobilya-venv/bin/pip install -r requirements.txt      # build123d ezdxf PyMuPDF Pillow reportlab
```

* Sürümler `requirements.txt`'te SABİTTİR (build123d 0.11.1, ezdxf 1.4.4,
  PyMuPDF 1.28.2, Pillow 12.3.0, reportlab 5.0.1). Aşağıdaki tuzaklar bu
  sürümlerde doğrulandı; yükseltince önce testleri, sonra bir paketi koştur.
* `ezdxf[draw]` **KURMA** — PySide6 (443 MB) çeker. Headless için
  `PyMuPDF` yeter, ama `Pillow` zorunludur: `ezdxf.addons.drawing.frontend`
  onu doğrudan import eder, yoksa `ModuleNotFoundError: No module named 'PIL'`.
* `reportlab` tasarım dosyası PDF'i (belge.py) için şart; Türkçe için TTF
  gömer — Arial (macOS Supplemental) yoksa DejaVu Sans / Liberation Sans
  aranır, `MOBILYA_FONT_DIR` ile klasör gösterilebilir.
* build123d Apple Silicon'da temiz kurulur (`cadquery-ocp-novtk` arm64
  wheel'i var, derleme yok). Venv ≈ 700 MB.
* Sistem python3.9 kullanma; yığın ≥3.10 ister. Saf Python testleri
  (`tests/`) 3.9'da da koşar ama CAD katmanı koşmaz.
* Blender yolu: `MOBILYA_BLENDER` ortam değişkeni, yoksa
  `/Applications/Blender.app/Contents/MacOS/Blender`. Yoksa `paketle()`
  render adımını atlar ve `hatalar` listesine yazar.

---

## build123d — doğrulanmış API

### Panel ve yerleştirme

```python
from build123d import *
p = Box(900, 320, 18, align=(Align.MIN, Align.MIN, Align.MIN))  # origin sol-alt
p.label = "P01 Yan panel"      # STEP + glTF'e yazılır
p.color = Color("burlywood")   # Color iterable; .to_tuple() YOK
yerlestirilmis = Pos(100, 0, 80) * Rot(0, 0, 30) * p
asm = Compound(children=[...]); asm.label = "Dolap"
```

`Align`: `MIN | CENTER | MAX`. `Shape.volume` ve `.area` **property**'dir.

### ⚠ Tuzak 1 — `project_to_viewport`'a `look_at` DAİMA ver

```python
def gorunus(sekil, yon, up, mesafe=1e5):
    c = sekil.bounding_box().center()
    return sekil.project_to_viewport(
        viewport_origin=c + Vector(yon) * mesafe,
        viewport_up=up,
        look_at=c)            # <<< bunu atlarsan görünüş EĞRİLİR
```

`look_at` verilmezse bakış yönü `shape_center - viewport_origin`'den
türetilir; ölçülen sonuç 400×100 yerine **274.9×121.0** çıkar.
`focus=None` iken projeksiyon gerçekten ortografiktir (100 ile 1 000 000
mesafede aynı boy). Dönen `(gorunen, gizli)` kenarları Z=0 düzlemindedir
ve `look_at`'ın izdüşümüne göre merkezlenir.

**Performans/gürültü:** 480 delikli bir gövdede ön görünüş **1993 gizli
kenar** üretti. Cephe görünüşlerini deliksiz modelden al ya da gizli
çizgileri at — yoksa DXF hem okunmaz hem devasa olur.

### ⚠ Tuzak 2 — `section()` kesme düzleminin DÜNYA konumunda kalır

```python
sec = section(kati, Plane.YZ.offset(400))     # Sketch, x=400'de duruyor
sec_2d = Plane.YZ.to_local_coords(sec)        # XY'ye indir — ÇİZİM İÇİN ŞART
```

### Dışa aktarım

```python
export_step(asm, "m.step", unit=Unit.MM)   # renk + isim + hiyerarşi korunur
export_gltf(asm, "m.glb", unit=Unit.MM, binary=True)   # Blender'a en iyi yol
export_stl(asm, "m.stl")
Mesher(unit=Unit.MM) -> .add_shape(...) -> .write("m.3mf")
```

`export_svg` / `export_dxf` **top-level fonksiyon olarak YOK**:

```python
from build123d.exporters import ExportDXF, ExportSVG, ColorIndex, LineType, Drawing
```

* `ExportDXF(version="AC1009")` = R12 (CNC için doğru sürüm).
* `ColorIndex` yalnız 9 renk: `BLACK RED YELLOW GREEN CYAN BLUE MAGENTA GRAY LIGHT_GRAY`.
* `exporter._document` / `._modelspace` canlı ezdxf nesneleridir — aynı
  belgeye ezdxf TEXT/DIMENSION eklemek için kullanılır. **Private API**;
  build123d sürümünü sabitle.

### ⚠ Tuzak 3 — GLB Blender'a METRE olarak gelir

`export_gltf(unit=Unit.MM)` glTF sözleşmesine uyar ve **metre** yazar.
Blender'da ayrıca 0.001 ile ölçekleme **YAPMA** — model 1 mm'ye düşer.
`render.py` bunu ölçerek karar verir (10 m'den büyükse mm kabul eder).

### ⚠ Tuzak 4 — `bounding_box()` dünya eksenlerine hizalıdır

Döndürülmüş panelin bbox'ı yanlış kesim ölçüsü verir
(`Rot(0,0,37) * Box(300,900,18)` → 782×838). Kesim listesi ölçülerini
**parçanın nominal L/W/T metadata'sından** al, bbox'tan değil.
`mobilya.py` zaten böyle yapar.

### `build123d.drafting` (yerleşik ISO çizim modülü)

`Draft`, `DimensionLine`, `ExtensionLine`, `TechnicalDrawing` gerçekten
paketin içinde gelir ve A3 antetli sayfa üretebilir. **Ama** ölçüler
DXF `DIMENSION` varlığı değil, dolu yüzey geometrisidir — AutoCAD'de
düzenlenemez. `drawing_scale` sadece kozmetiktir (kaynak satırı
`"1:" + str(drawing_scale)`). Atölyeye giden çizim için **ezdxf yolunu**
kullan; bu modül hızlı iç PDF'ler için uygundur.

---

## ezdxf — doğrulanmış API

### ⚠ Tuzak 5 — `setup=True` ölçü stilleri METRE varsayar

`EZDXF`, `EZ_M_10_H25_CM` vb. `dimlfac=100` ile gelir; mm mobilya işinde
yanlıştır. Kendi stilini tanımla (`cizim.py::Sayfa._dimstyle`).

### ⚠ Tuzak 6 — kağıt alanı VIEWPORT'u ezdxf RENDER EDEMEZ

Paper-space layout + VIEWPORT içeren belge AutoCAD'de doğrudur ama
ezdxf'in drawing add-on'u viewport içeriğini çizmez (test edildi: sadece
çerçeve ve yazı, 4 path). **Çözüm — bu skill'in kullandığı yöntem:**

> Her şeyi **modelspace'e, gerçek kağıt milimetresiyle** çiz. Geometriyi
> `1/ÖLÇEK` ile kendin küçült. `DIMLFAC = ÖLÇEK` ver ki ölçü yazısı
> gerçek mm göstersin. `DIMSCALE = 1` kalsın (yazılar zaten kağıt mm).
> Sayfayı `Settings(scale=1, fit_page=False)` ile bas.

Doğrulandı: 1/10 küçültülmüş geometriden A3'te **800, 280, 1150, 345**
okunuyor — gerçek milimetreler.

### ⚠ Tuzak 7 — `RenderContext` varsayılanı KOYU temadır

Arka plan `#212830`, ön plan `#ffffff`. Düzeltmezsen beyaz sayfaya beyaz
çizer, **çıktı bomboş gelir**.

```python
from ezdxf.addons.drawing import Frontend, RenderContext, layout
from ezdxf.addons.drawing.properties import LayoutProperties
from ezdxf.addons.drawing.pymupdf import PyMuPdfBackend

ctx = RenderContext(doc); be = PyMuPdfBackend()
lp = LayoutProperties.from_layout(msp)
lp.set_colors("#ffffff", "#000000")          # <<< ZORUNLU
Frontend(ctx, be).draw_layout(msp, finalize=True, layout_properties=lp)
sayfa = layout.Page(420, 297, layout.Units.mm, layout.Margins.all(0))
ayar = layout.Settings(scale=1, fit_page=False)
open("s.pdf","wb").write(be.get_pdf_bytes(sayfa, settings=ayar))
open("s.png","wb").write(be.get_pixmap_bytes(sayfa, fmt="png", dpi=300, settings=ayar))
```

`SVGBackend` çizgileri **konturlu dolu yüzeye** çevirir (stroke yok); PDF'e
tekrar çevirirsen sayfa simsiyah olur. PDF/PNG için **PyMuPdfBackend**
kullan, SVG'yi yalnız SVG nihai tüketiciyse üret.

### Ölçüler

Hepsi `DimStyleOverride` döner ve **`.render()` çağrılmalıdır**
(tek istisna `add_multi_point_linear_dim`, kendi içinde render eder).

```python
msp.add_linear_dim(base=(0,-12), p1=(0,0), p2=(120,0), dimstyle="MOB").render()
msp.add_multi_point_linear_dim(base=(x,0), points=[...], angle=90, dimstyle="MOB")
msp.add_radius_dim_cra(center, radius, angle, dimstyle="EZ_RADIUS").render()
msp.add_angular_dim_2l(base, line1, line2, dimstyle="EZ_CURVED").render()
```

ezdxf'in kendi uyarısı: *"does not consider all DIMSTYLE variables"* —
render sonucu CAD uygulamalarından biraz farklı çıkar.

### R12'ye çevirme (CNC)

```python
from ezdxf.addons import r12export
r12export.saveas(doc, "cikti_R12.dxf", max_sagitta=0.01)
```

`Drawing units ($INSUNITS) are not exported for DXF R12` uyarısı
**normaldir** — R12'de birim başlığı yoktur, mm olduğunu dosya adında ve
teslim notunda belirt.

---

## Blender 5.2 — 4.x'ten kırılan her şey

| 4.x | 5.x |
|---|---|
| `'BLENDER_EEVEE_NEXT'` | **`'BLENDER_EEVEE'`** (`_NEXT` reddedilir) |
| `scene.node_tree` | **`scene.compositing_node_group`** (eski adı KALDIRILDI) |
| `scene['cycles']` sözlük erişimi | KALDIRILDI — `scene.cycles` (öznitelik) |
| `scene.cycles.feature_set` | KALDIRILDI (5.2) |
| `ShaderNodeTexMusgrave` | KALDIRILDI → `TexNoise.noise_type` |
| tüm `Fac` soketleri | **`Factor`** |
| `Material.use_nodes` | DEPRECATED (6.0'da gidecek); `node_tree` zaten hazır gelir |
| `Boolean` solver `'FAST'` | `'FLOAT'` (+ yeni `'MANIFOLD'`) |
| `Action.fcurves` | KALDIRILDI (slotted actions) |
| Collada `.dae`, X3D | TAMAMEN KALDIRILDI |
| `mesh.use_auto_smooth` | KALDIRILDI (4.1'den beri) |
| `'Raw'` / `'Linear'` colorspace | KALDIRILDI → `'Non-Color'` / `'Linear Rec.709'` |
| Geometry Nodes `mod["Socket_2"]` | `mod.properties.inputs.Socket_2.value` |

Principled BSDF adları: `Specular`→**`Specular IOR Level`**,
`Transmission`→**`Transmission Weight`**, `Clearcoat`→**`Coat Weight`**,
`Emission`→**`Emission Color`**, `Subsurface`→**`Subsurface Weight`**.
Yeni: **`Thin Wall`** (BOOLEAN, float değil).

Sürüm-güvenli soket erişimi için `render.py::sok()` kullan.

### ⚠ Tuzak 8 — `media_type`, `file_format`'tan ÖNCE

```python
r.image_settings.media_type = 'IMAGE'    # 'IMAGE'|'MULTI_LAYER_IMAGE'|'VIDEO'
r.image_settings.file_format = 'PNG'
```
Ters sırada geçerli formatlar bile `enum ... not found` ile reddedilir.

### ⚠ Tuzak 9 — macOS'ta tek geçerli değerler

```python
prefs.compute_device_type = 'METAL'        # 'NONE' ve 'METAL' DIŞINDA hepsi TypeError
scene.cycles.denoiser = 'OPENIMAGEDENOISE' # 'OPTIX' NVIDIA'ya özel, TypeError
scene.cycles.denoising_use_gpu = True      # varsayılan False!
```
`--factory-startup` GPU seçimini sıfırlar; cihaz kurulumunu **her
script'te** tekrar çalıştır, kayıtlı tercihe güvenme.

**İlk render'da Metal kernel derlemesi ~60–90 sn sürer** (ölçüldü: soğuk
77.3 s → sıcak 1.03 s). Süre ölçerken soğuk çalıştırmayı sayma.

### ⚠ Tuzak 10 — dinamik enum'lar boş introspect edilir

`view_transform`, `look`, `denoiser`, `compute_device_type`,
`render.engine` için `bl_rna.properties[...].enum_items` **`[]` döner**.
Listeye bakıp doğrulama yapma; `try/except TypeError` ile ata.

Ayrıca `hasattr(bpy.ops.wm, "collada_export")` **yalan söyler** (lazy stub
üretir). Operatör varlığını `dir()` veya `get_rna_type()` ile sına.

### ⚠ Tuzak 11 — `default_value` DAİMA scene-linear

sRGB hex/0-1 rengi doğrudan atarsan aşırı parlak çıkar. `s2l()` ile çevir.

### Renk yönetimi

`view_transform` geçerli değerler: `Standard`, `AgX`, `Filmic`,
`Filmic Log`, `Khronos PBR Neutral`, `False Color`, `Raw`.
`look` değerleri **önekli**: `'AgX - Punchy'` çalışır, `'Punchy'` çalışmaz.

* **Katalog / dekor rengi tutmalı** → `'Standard'` + 5000 K ışık.
  Ölçüldü: bilinen swatch 2/255 sapmayla üretildi.
* **Vitrin / pazarlama görseli** → `'Khronos PBR Neutral'` (ürün render'ı
  için tasarlandı; AgX'in doygunluk kaybı yok).
* `look = 'None'` — katalog işinde her look bir renk müdahalesidir.

### ⚠ Tuzak 12 — beyaz fon seviyesi view transform'a bağlı

Kompozitör scene-linear çalışır; **1.0 ekranda beyaz değildir**.
Köşe pikseli ölçümü:

| view transform | 1.0 verir | ~254 için gereken |
|---|---|---|
| Standard | 251 | **1.0** |
| Khronos PBR Neutral | 246 | **4.0** |
| AgX | 226 | **16.0** |

Ayrıca `AlphaOver`'ın çalışması için `render.film_transparent = True`
olmalı; yoksa arka plan siyah kalır (bu skill'de `beyaz_fon()` kendisi
açar).

### Işık gücü — ölçülmüş

~1 m yüksek mobilya için **anahtar ışık ≈ 100–110 W**. 500 W albedo'yu
patlatır ve deseni yok eder; `Standard` 150 W üstünde sert klipler.
`light.use_temperature` / `.temperature` 5.2'de birinci sınıf özelliktir —
RGB tint hesaplama.

### Import / export (5.2'de geçerli operatörler)

| Format | Import | Export |
|---|---|---|
| glTF/GLB | `import_scene.gltf` | `export_scene.gltf` (`'GLTF_EMBEDDED'` KALDIRILDI) |
| USD/USDZ | `wm.usd_import` | `wm.usd_export` (ayrı usdz op YOK — uzantı .usdz ver) |
| OBJ/PLY/STL | `wm.obj_import` / `wm.ply_import` / `wm.stl_import` | `wm.*_export` |
| FBX | `wm.fbx_import` (yeni C++) | `export_scene.fbx` (hâlâ addon) |

**STEP ve DXF için yerleşik destek YOKTUR** — ne import ne export.
CAD alışverişi build123d/ezdxf tarafında kalır.

USDZ'de `generate_preview_surface=True` **AR Quick Look için zorunludur**.

### UV — panel mobilyada operatör kullanma

`bpy.ops.uv.*` mod değiştirmeyi gerektirir, paketlemede deterministik
değildir ve desen yönünü kontrol ettirmez. Eksen hizalı levha parçaları
için UV'yi **veri seviyesinde** yaz (`render.py::kutu_uv`): 1 UV birimi =
1 m olur, teksel yoğunluğu her parçada aynıdır, desen yönü parça bazında
seçilir. `uv.cube_project(cube_size=1.0)` de 1 birim = 1 m verir ama her
yüzü kendi baskın eksenine göre açar — yatay tabla ile dikey yan panel
**farklı desen yönü** alır; gerçek mobilyada desen her parçanın uzun
ekseninde akar, o yüzden iki materyal varyantı gerekir.

### Kenar bandı — ayrı geometri DEĞİL, 2. materyal slotu

Kalınlık yüzlerini `material_index = 1`'e ata (`render.py::bant_ata`).
Ayrı şerit modellemek nesne sayısını ikiye katlar ve z-fighting riski
getirir; dokuya boyamak parça yeniden boyutlandığında bozulur. Slot
yöntemi ölçü değişimine dayanır, glTF/USDZ'ye doğru gider ve bant rengi
dekordan bağımsız değişir — gerçekte de ayrı SKU'durlar.
Panel kenarına **0.3–0.5 mm pah** koy; ışığı yakalar, plastik görüntüyü kırar.

---

## CC0 doku kaynakları — lisans durumu (2026-08 doğrulandı)

| Site | Lisans | Atıf | Yeniden dağıtım | Programatik indirme |
|---|---|---|---|---|
| **ambientCG** | Gerçek CC0 | gerekmez | serbest | ✅ v3 API + `get?file=` |
| **Poly Haven** | Varlıklar CC0 | gerekmez | serbest | ✅ `api.polyhaven.com`, **kendi User-Agent'ını gönder (ToS §2.4)** |
| cgbookcase | Gerçek CC0 | gerekmez | serbest | ✅ ama `Referer` şart |
| texturecan | Gerçek CC0 | gerekmez | serbest | ✅ |
| 3dtextures.me | Gerçek CC0 | gerekmez | serbest | kısmen (Google Drive) |
| **sharetextures** | "Custom CC0 + kısıt" | — | **yasak** | ❌ **ToS botla indirmeyi açıkça yasaklıyor** |
| **freepbr** | ücretsiz katman **ticari değil** ($21 ticari) | — | **yasak** | ❌ robots.txt ClaudeBot'u engelliyor |
| **Poliigon** | geri alınabilir, kısıtlı EULA | — | **yasak** | ❌ üyelik duvarı |

İndirme URL kalıpları:
```
ambientCG : https://ambientcg.com/get?file=<Id>_<1K|2K|4K>-<JPG|PNG>.zip
PolyHaven : https://api.polyhaven.com/files/<slug>   -> map/res/format/url
            (indirme host'u dl.polyhaven.org; cdn.polyhaven.com 404 verir)
```

**Mobilya için doğrulanmış varlıklar:**
* Meşe — `Wood049`, `Wood092`, `Wood094` · `oak_veneer_02`, `white_oak_veneer`
* Ceviz — `Wood051`, `Wood067` · `black_walnut_veneer_01`, `american_walnut_veneer`
* Kayın — **Poly Haven'da kayın/huş YOK**; `white_maple_veneer` en iyi vekil.
  ambientCG'de `Wood090A/B`, `Wood091A/B`, `Wood095`.
* Kontrplak/yonga kenarı — `Wood087/088/089`, `Chipboard001-008`, `plywood`
* **Düz beyaz melamin İKİ SİTEDE DE YOK.** `render.py::melamin()` prosedürel
  üretir — doku aramaya çalışma.

**Stüdyo HDRI:** `white_studio_04/05`, `monochrome_studio_02` (5500 K),
`brown_photostudio_02` (5800 K).
⚠ `studio_small_09` en çok indirilen stüdyo HDRI'sidir ama beyaz dengesi
**2750 K** — ahşabı turuncuya çeker. Jelli/renkli stüdyo setlerinden uzak dur.

---

## Nesting / kesim optimizasyonu

Panel testere **giyotin** kesim ister (her kesim baştan başa); CNC router
serbest nesting yapabilir. Mobilyada belirleyici olan testere yoludur.

`mobilya.py` kendi giyotin optimizatörünü taşır (First-Fit-Decreasing +
Best-Area-Fit, kerf ve kenar traşı dahil). `rectpack` ile aynı girdide
**birebir aynı verim** (%61.3) alındı — bağımsız çapraz doğrulama.
`rectpack` kullanacaksan kerf parametresi yoktur; parçayı kerf kadar
şişir, levhayı traş kadar küçült.

`nest2D`/`pynest2d` PyPI'de **yok**; `svgnest` py2.7 döneminden kalma.
Bunlara göre plan yapma.

**Her optimizasyondan sonra `optimize_dogrula()` çalıştır** — çakışma ve
levha dışına taşma denetimi. Sessiz çakışma en pahalı hata türüdür.

---

## CNC atölyesinin beklediği DXF

**Yayınlanmış açık standart yoktur**; her sistem katman adı sözleşmesiyle
çalışır. Katman şablonunu **sabit değil, ayar** yap.

* **Sürüm: R12 (AC1009)** ağaç işlerinde doğru cevaptır (Magi-Cut yalnız
  R12 okur; TpaCAD spline için ücretli ek kütüphane ister). Sac/lazer
  dünyasının "R2000+" tavsiyesini buraya taşıma.
* Yalnız `LINE`, `ARC`, `CIRCLE`, `POLYLINE` üret. Spline, ellips, MTEXT,
  hatch, blok, dimension **CNC dosyasına girmez**.
* Katman adı ≤31 karakter, büyük harf, `[A-Z0-9_-]`.
  Yaygın kalıp: `<İŞLEM>_<ÇAP>_<DERİNLİK>`.
* **Delikler tam daire (`CIRCLE`) olarak, gerçek çapında** çizilir;
  derinlik katman adından okunur. `POINT` kullanma.
* Origin **sol-alt**, tüm koordinatlar pozitif; panel konturunu ayrı
  katmanda mutlaka ver (TpaCAD ve Magi-Cut (0,0)'ı ondan türetir).
* Birim mm, 1:1 — R12 birim başlığı taşımaz, dosya adında/teslim notunda yaz.
* **Desen yönü ve kenar bandı DXF'te değil, CSV'dedir.** Ölçünün net mi
  kesim mi olduğunu açıkça belirt.
* Varsayılan: **parça başına bir DXF + CSV kesim listesi.** Atölyenin
  optimizatörü (Cut Rite / OptiCut / Ardis) kendi kerf ve stok artığıyla
  yerleştirir; önceden nesting genelde değer kaybettirir.

Bilinen sistemler: Homag woodWOP `ProcPart_19`, `V_Drill<mod>_<derinlik>` ·
Thermwood `outline z#p#`, `drill z#p#` · Magi-Cut `M_BORDER`, `M_VBORE` ·
TpaCAD `SETM1T10S4000F5Z12_8`.
⚠ **Biesse bSolid katman adından işlem türetmez** — geometrinin boyutsal
özelliklerine bakar; otomasyon için CIX/BPP gerekir.
⚠ TpaCAD'de "minimum circle radius" (varsayılan 0.0) altındaki daireler
delik değil **frezelenmiş yay** olarak alınır.
