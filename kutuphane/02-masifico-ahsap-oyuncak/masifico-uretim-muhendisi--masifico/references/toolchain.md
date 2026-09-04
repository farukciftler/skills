# Araç zinciri referansı — macOS (Apple Silicon), Ağustos 2026'da bu Mac'te doğrulandı

Sürüm anlık görüntüsü: build123d 0.11.1 · ezdxf 1.4.4 · trimesh 5.0.0 · manifold3d 3.5.2 · shapely 2.1.2 · rectpack 0.2.2 · reportlab 5.0.0 · weasyprint 69.0 · f3d 3.5.0 · PrusaSlicer 2.9.6 · OrcaSlicer 2.4.2 · Inkscape 1.4.4 · FreeCAD 1.1.3.

## Kurulum (öncelik sırasıyla)

```bash
# 1. Çekirdek Python CAD yığını (admin gerekmez, ~2 dk)
/opt/homebrew/bin/python3.13 -m venv ~/masifico-venv
~/masifico-venv/bin/pip install build123d ezdxf matplotlib pymupdf trimesh \
  manifold3d shapely svgwrite rectpack reportlab weasyprint numpy-stl
# 2. Render + mesh onarım
brew install f3d admesh          # f3d FORMULA'dır, cask değil (STEP desteği OCCT ile gelir)
# 3. Dilimleyici (tek gerekli cask)
brew install --cask prusaslicer  # ikincil: orcaslicer
# 4. Opsiyonel
brew install --cask inkscape     # SVG→PDF/DXF çevrim
brew install --cask freecad      # TechDraw yedeği — normalde gerekmez
```

Tuzaklar:
- Sistem Python 3.9.6 — yığının tamamı ≥3.10 ister; venv'i daima `/opt/homebrew/bin/python3.13` ile kur.
- `pip install build123d` Apple Silicon'da artık düz çalışır (cadquery-ocp arm64 wheel'i var); conda gerekmiyor.
- Slicer'ların CLI symlink'i yok — binary `.app` içinde çağrılır (aşağıda).
- Bambu Studio macOS'ta x86-only (Rosetta) — kullanma; OrcaSlicer Bambu yazıcıları da kapsar.
- OpenSCAD stable cask 2021'de kalmış; gerekirse `openscad@snapshot`. build123d varken gereksiz.
- CAMotics brew'da yok, sürümleri bayat — G-code kontrolü slicer GUI'sinde yapılır.
- WeasyPrint'in istediği pango/cairo/gdk-pixbuf bu Mac'te brew ile zaten kurulu.

## build123d — model + tüm exportlar (test edildi)

```python
from build123d import *
from build123d.exporters import ExportDXF, ExportSVG, ColorIndex, LineType  # * ile GELMEZ
with BuildPart() as wheel:
    Cylinder(20, 12); Cylinder(3.1, 12, mode=Mode.SUBTRACT)
    chamfer(wheel.edges().filter_by(GeomType.CIRCLE).group_by(SortBy.RADIUS)[-1], 1.5)
p = wheel.part
export_step(p, "wheel.step"); export_stl(p, "wheel.stl")
m = Mesher(); m.add_shape(p); m.write("wheel.3mf")
sec = section(p, Plane.XY)                       # 2,5D CNC profili
dx = ExportDXF(unit=Unit.MM); dx.add_layer("KESIM", color=ColorIndex.RED)
dx.add_shape(sec, layer="KESIM"); dx.write("wheel_cnc.dxf")
vis, hid = p.project_to_viewport((70, -50, 40))  # izometrik görünüş
sv = ExportSVG(scale=4); sv.add_layer("v"); sv.add_layer("h", line_type=LineType.ISO_DASH)
sv.add_shape(vis, "v"); sv.add_shape(hid, "h"); sv.write("wheel_iso.svg")
```

build123d'de ölçülendirme YOK — doğru akış: build123d geometri → DXF → ezdxf ile DIM ekle.

## ezdxf — ölçülü çizim + PNG/SVG/PDF (test edildi)

```python
import ezdxf
doc = ezdxf.new("R2010", setup=True)   # setup=True olmadan dim stilleri yok
msp = doc.modelspace()
msp.add_linear_dim(base=(0, -12), p1=(0, 0), p2=(120, 0), dimstyle="EZDXF").render()  # .render() ZORUNLU
msp.add_diameter_dim(center=(30, 15), radius=8, angle=45, dimstyle="EZ_RADIUS").render()
doc.saveas("plaka.dxf")

# PDF (PyMuPdf backend):
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.pymupdf import PyMuPdfBackend
from ezdxf.addons.drawing.layout import Page
b = PyMuPdfBackend(); Frontend(RenderContext(doc), b).draw_layout(msp, finalize=True)
open("plaka.pdf", "wb").write(b.get_pdf_bytes(Page(297, 210)))  # A4 yatay
```

```bash
ezdxf draw plaka.dxf -o onizleme.png --dpi 200   # hızlı PNG önizleme (CLI)
```

## PrusaSlicer CLI (birincil dilimleyici)

```bash
PS="/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer"
"$PS" --info model.stl                                              # boyut kontrolü
"$PS" --export-gcode --load prototip_pla.ini --output out.gcode model.stl
grep "estimated printing time" out.gcode    # "; estimated printing time (normal mode) = 1h 32m"
grep "filament used \[g\]" out.gcode
```

Profil: GUI'den bir kez File > Export Config (.ini) → sonrası hep CLI. Prototip profili önerisi: PLA 0,2 mm katman, 3 duvar, %15 gyroid dolgu; geçme kuponlarında %100 dolgu küçük parça.

## OrcaSlicer CLI (ikincil)

```bash
ORCA="/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer"
"$ORCA" --slice 1 --load-settings "machine.json;process.json" \
  --load-filaments "filament.json" --outputdir out/ --arrange 1 model.stl
# DİKKAT: tek --load-settings argümanında machine ÖNCE, process SONRA — ters sıra sessizce bozulur.
# Profiller: ~/Library/Application Support/OrcaSlicer/system/<Vendor>/ ; çıktı: out/plate_1.gcode
```

## f3d — render (STEP'i doğrudan açar)

```bash
f3d wheel.step --output=render.png --resolution=1920,1080 \
  --anti-aliasing=ssaa --tone-mapping --ambient-occlusion --camera-zoom-factor=0.9
# --no-background → şeffaf PNG · --edges → kenar çizgili görünüm
```

## Mesh sağlığı (baskı öncesi)

```python
import trimesh
m = trimesh.load("part.stl")
assert m.is_watertight, "delikli mesh — onar"
fixed = trimesh.boolean.union([m], engine="manifold")   # manifold3d motoru
```

```bash
admesh --fill-holes --write-binary-stl=fixed.stl part.stl
```

## Kerf/ofset (yalnız not düşülen özel durumda)

```python
from shapely.geometry import Polygon
telafili = Polygon(noktalar).buffer(takım_çapı / 2, join_style=2)  # mitre köşe
```

## Nesting (plaka yerleşimi)

```python
from rectpack import newPacker
p = newPacker(rotation=True)
for w, h, pid in parçalar: p.add_rect(w + 8, h + 8, pid)  # 8 mm takım payı
p.add_bin(1250, 250)                                       # Snc plaka ebadı
p.pack()
# çıktıya kullanım oranını yaz: toplam parça alanı / plaka alanı
```

## Inkscape CLI — çevrimler

```bash
INK="/Applications/Inkscape.app/Contents/MacOS/inkscape"
"$INK" dosya.svg --export-type=pdf --export-filename=cikti.pdf
"$INK" dosya.svg --actions="select-all:all;object-to-path" --export-type=dxf \
  --export-extension=org.ekips.output.dxf_outlines --export-filename=cikti.dxf
```

## Lazer SVG sözleşmesi

- Gerçek dünya birimi: `width="300mm" height="200mm" viewBox="0 0 300 200"`.
- Renk kodu: **kırmızı rgb(255,0,0) = kesim · siyah = gravür · mavi rgb(0,0,255) = çizik (score)**.
- Kesim çizgileri stroke-only, hairline **≤0,025 mm** (LightBurn <0,02 mm'yi otomatik kesim sayar); raster gravür alanları dolgu ile.
- Parça konturu %50 gri ayrı referans katmanında (lazerci hizalama için kullanır, işlemez).

## Paket PDF'i

reportlab (bağımlılıksız, programatik) veya weasyprint (HTML/CSS → PDF; şablonlu güzel sayfa). Üretim paketi tek PDF: kapak (SKU, sürüm, tarih) → BOM → çizimler → torna kartı → montaj → EN 71 satırı.
