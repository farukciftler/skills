"""
cizim.py — build123d (3D) + ezdxf (2D ölçülü çizim) katmanı.

Sağladıkları:
  • Parça listesinden 3B katı model (Compound, renkli, isimli)
  • STEP (master) · GLB (Blender'a devir) · STL
  • Ortografik görünüşler (gizli çizgi atımlı, OCCT HLR)
  • Kesit (section) + tarama (poché)
  • Ölçülendirilmiş A3 teknik çizim → DXF + PDF + PNG
  • Parça başına CNC DXF (R12, katman adlarında delik çapı/derinliği)

Çalıştırma: ~/mobilya-venv/bin/python cizim.py
Kurulum   : scripts/kurulum.sh

DİKKAT — bu dosyadaki üç şey deneyle bulunmuş, değiştirme:
  1. project_to_viewport'a look_at DAİMA açıkça verilir; verilmezse görünüş
     eğrilir (400x100 yerine 274.9x121.0 çıkar).
  2. ezdxf RenderContext varsayılanı KOYU temadır; lp.set_colors(...)
     çağrılmazsa beyaz sayfaya beyaz çizer, çıktı bomboş olur.
  3. Kağıt alanı (paper space) VIEWPORT içeriğini ezdxf render EDEMEZ.
     Bu yüzden her şey modelspace'e kağıt-mm olarak, 1/ÖLÇEK küçültülmüş
     çizilir ve DIMLFAC=ÖLÇEK ile ölçü yazıları gerçek mm gösterir.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass

from build123d import (
    Align, Axis, Box, Color, Compound, Cylinder, GeomType, Plane, Pos,
    Rot, Unit, Vector, export_gltf, export_step, export_stl, section,
)
from build123d.exporters import ColorIndex, ExportDXF

import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.addons.drawing import Frontend, RenderContext, layout
from ezdxf.addons.drawing.properties import LayoutProperties
from ezdxf.addons.drawing.pymupdf import PyMuPdfBackend

# ---------------------------------------------------------------------------
# 1. 3B MODEL
# ---------------------------------------------------------------------------

# Malzeme -> görsel renk (STEP + glTF'e gömülür, Blender'da başlangıç rengi)
RENKLER = {
    "suntalam": "burlywood",
    "mdflam": "burlywood",
    "mdf": "#C8A882",
    "hdf": "#8B7355",
    "kontrplak": "#D2B48C",
    "kapak": "#E8DCC8",
    "mekanizma": "#4A4A4A",
}


@dataclass
class Yerlestirme:
    """Bir parçanın 3B'deki konumu.

    İKİ eksen birden verilir — tek eksen belirsizdir ve parçayı 90° döndürür.

    konum      : parçanın MIN köşesinin (x, y, z) dünya koordinatı, mm
    eksen      : KALINLIĞIN oturduğu dünya ekseni — "x" | "y" | "z"
                 x = dikey yan panel · y = ön/arka panel · z = yatay tabla
    boy_ekseni : parçanın BOY (= desen yönü) ölçüsünün oturduğu eksen.
                 Kalan eksene otomatik olarak "en" gider.

    Örnekler:
      yan panel   eksen="x", boy_ekseni="z"   (boy = yükseklik, en = derinlik)
      raf/tabla   eksen="z", boy_ekseni="x"   (boy = genişlik, en = derinlik)
      kapak       eksen="y", boy_ekseni="z"   (boy = yükseklik, en = genişlik)
      arkalık     eksen="y", boy_ekseni="z"
    """
    kod: str
    konum: tuple[float, float, float]
    eksen: str = "z"
    boy_ekseni: str = "x"
    donus_x: float = 0.0        # derece — eğimli raf (arkaya doğru aşağı)
    donus_z: float = 0.0        # derece — devrilir kapak vb. için
    renk: str | None = None


def kati(parca, yer: Yerlestirme):
    """Parca + Yerlestirme -> yerleştirilmiş build123d Solid."""
    ekseni = {"x": 0, "y": 1, "z": 2}
    if yer.eksen not in ekseni or yer.boy_ekseni not in ekseni:
        raise ValueError("eksen/boy_ekseni 'x'|'y'|'z' olmalı")
    if yer.eksen == yer.boy_ekseni:
        raise ValueError(
            f"{yer.kod}: kalınlık ve boy aynı eksende olamaz "
            f"('{yer.eksen}')")

    t_i, b_i = ekseni[yer.eksen], ekseni[yer.boy_ekseni]
    e_i = ({0, 1, 2} - {t_i, b_i}).pop()
    dims = [0.0, 0.0, 0.0]
    dims[t_i] = parca.kalinlik
    dims[b_i] = parca.boy
    dims[e_i] = parca.en

    p = Box(*dims, align=(Align.MIN, Align.MIN, Align.MIN))
    if yer.donus_x:
        # Ön-alt kenar (y=0, z=0) etrafında döner; negatif açı arka kenarı
        # aşağı indirir — eğimli ayakkabı rafının doğru yönü.
        p = Rot(yer.donus_x, 0, 0) * p
    if yer.donus_z:
        p = Rot(0, 0, yer.donus_z) * p
    p = Pos(*yer.konum) * p
    p.label = f"{parca.kod} {parca.ad}"
    p.color = Color(yer.renk or RENKLER.get(parca.malzeme, "burlywood"))
    return p


@dataclass
class Boru:
    """Askı borusu / küpeşte gibi silindirik donanım.

    Levha parçası DEĞİLDİR — kesim listesine girmez, donanım listesine girer.

    eksen : borunun uzadığı dünya ekseni
            "y" = önden arkaya (SIĞ dolapta askı bu yönde olur)
            "x" = soldan sağa (normal derin gardırop askısı)
    konum : borunun BAŞLANGIÇ ucunun merkez koordinatı
    """
    kod: str
    ad: str
    cap: float                       # mm
    boy: float                       # mm
    konum: tuple[float, float, float]
    eksen: str = "x"
    renk: str = "#B8BCC0"            # krom


def boru_kati(b: Boru):
    from build123d import Cylinder
    c = Cylinder(b.cap / 2, b.boy, align=(Align.CENTER, Align.CENTER, Align.MIN))
    donus = {"x": Rot(0, 90, 0), "y": Rot(-90, 0, 0), "z": Rot(0, 0, 0)}[b.eksen]
    p = Pos(*b.konum) * donus * c
    p.label = f"{b.kod} {b.ad}"
    p.color = Color(b.renk)
    return p


def model_kur(parcalar: list, yerlestirmeler: list[Yerlestirme],
              ad: str = "Mobilya", borular: list = None) -> Compound:
    """Parça listesi + yerleştirme listesinden montaj Compound'u üretir."""
    idx = {p.kod: p for p in parcalar}
    cocuklar = []
    for y in yerlestirmeler:
        if y.kod not in idx:
            raise KeyError(f"Yerleştirmede olan '{y.kod}' parça listesinde yok")
        cocuklar.append(kati(idx[y.kod], y))
    for b in (borular or []):
        cocuklar.append(boru_kati(b))
    asm = Compound(children=cocuklar)
    asm.label = ad
    return asm


def disa_aktar(asm: Compound, klasor: str, ad: str) -> dict[str, str]:
    """STEP (master) + GLB (Blender) + STL. Yolları döndürür."""
    os.makedirs(klasor, exist_ok=True)
    yollar = {}
    step = os.path.join(klasor, f"{ad}.step")
    export_step(asm, step, unit=Unit.MM)
    yollar["step"] = step

    glb = os.path.join(klasor, f"{ad}.glb")
    # binary=True -> tek dosya .glb; isim + hiyerarşi + renk korunur.
    export_gltf(asm, glb, unit=Unit.MM, binary=True)
    yollar["glb"] = glb

    stl = os.path.join(klasor, f"{ad}.stl")
    export_stl(asm, stl)
    yollar["stl"] = stl
    return yollar


# ---------------------------------------------------------------------------
# 2. ORTOGRAFİK GÖRÜNÜŞ + KESİT
# ---------------------------------------------------------------------------

# Yön tanımları: (bakış yönü, yukarı vektörü)
GORUNUSLER = {
    "on":    ((0, -1, 0), (0, 0, 1)),    # önden
    "arka":  ((0, 1, 0), (0, 0, 1)),
    "sag":   ((1, 0, 0), (0, 0, 1)),     # sağ yan
    "sol":   ((-1, 0, 0), (0, 0, 1)),
    "ust":   ((0, 0, 1), (0, 1, 0)),     # plan
}


def gorunus(sekil, yon: str, mesafe: float = 1e5):
    """Ortografik gizli-çizgi atımlı görünüş -> (gorunen_kenarlar, gizli).

    look_at DAİMA verilir. Verilmezse bakış yönü shape_center'a göre
    hesaplanır ve görünüş eğrilir.
    """
    d, up = GORUNUSLER[yon]
    c = sekil.bounding_box().center()
    return sekil.project_to_viewport(
        viewport_origin=c + Vector(d) * mesafe,
        viewport_up=up,
        look_at=c,
    )


def kesit(sekil, duzlem: Plane):
    """Verilen düzlemde kesit alır ve XY'ye indirir (çizilebilir hale getirir).

    section() dönen Sketch'i kesim düzleminin DÜNYA konumunda bırakır;
    to_local_coords ile XY'ye taşımazsan çizim yanlış yere düşer.
    """
    s = section(sekil, duzlem)
    return duzlem.to_local_coords(s)


# ---------------------------------------------------------------------------
# 3. ÖLÇÜLÜ TEKNİK ÇİZİM (ezdxf)
# ---------------------------------------------------------------------------

KATMANLAR = [
    # (ad, aci renk, kalem 1/100 mm, çizgi tipi)
    ("00-CERCEVE", 7, 50, "CONTINUOUS"),
    ("01-GORUNEN", 7, 35, "CONTINUOUS"),
    ("02-GIZLI", 8, 18, "DASHED"),
    ("03-KESIT", 1, 50, "CONTINUOUS"),
    ("04-TARAMA", 9, 9, "CONTINUOUS"),
    ("05-OLCU", 3, 13, "CONTINUOUS"),
    ("06-YAZI", 7, 13, "CONTINUOUS"),
    ("07-EKSEN", 4, 9, "CENTER"),
]

SAYFA = {"A4": (297.0, 210.0), "A3": (420.0, 297.0), "A2": (594.0, 420.0)}


class Sayfa:
    """Modelspace'te kağıt-mm olarak kurulan ölçekli teknik çizim sayfası."""

    def __init__(self, olcek: float = 10.0, boyut: str = "A3"):
        self.olcek = float(olcek)
        self.k = 1.0 / self.olcek          # model mm -> kağıt mm
        self.gen, self.yuk = SAYFA[boyut]
        self.boyut = boyut

        self.doc = ezdxf.new("R2010", setup=True)
        self.doc.units = ezdxf.units.MM
        self.doc.header["$INSUNITS"] = 4
        self.doc.header["$MEASUREMENT"] = 1
        self.msp = self.doc.modelspace()

        for ad, renk, kalem, ctip in KATMANLAR:
            self.doc.layers.add(ad, color=renk, lineweight=kalem, linetype=ctip)

        self._dimstyle()
        self._cerceve()

    # -- kurulum -----------------------------------------------------------
    def _dimstyle(self):
        """Kendi ölçü stilimiz.

        setup=True'nun getirdiği EZDXF/EZ_M_* stilleri çizim biriminin METRE
        olduğunu varsayar (dimlfac=100) — mm mobilya işinde YANLIŞTIR.
        Geometriyi 1/ölçek küçülttüğümüz için dimlfac=ölçek verip ölçü
        yazısının gerçek mm göstermesini sağlıyoruz.
        """
        ds = self.doc.dimstyles.add("MOB")
        d = ds.dxf
        d.dimtxt = 2.5          # yazı yüksekliği, KAĞIT mm
        d.dimasz = 2.5          # ok/çizik boyu
        d.dimexe = 1.25         # ölçü çizgisini aşan uzantı
        d.dimexo = 0.625        # parçadan uzaklık
        d.dimgap = 0.625
        d.dimdec = 0            # tam mm
        d.dimlfac = self.olcek  # <<< gerçek mm yazdıran ayar
        d.dimscale = 1.0        # geometri zaten kağıt boyutunda
        d.dimtad = 1            # yazı ölçü çizgisinin üstünde
        d.dimtih = 0
        d.dimtoh = 0            # ISO: yazı daima ölçü çizgisine paralel
        d.dimblk = "ARCHTICK"   # mimari çizik; "" = ok
        d.dimzin = 8            # sondaki sıfırları at
        try:
            d.dimtxsty = "LiberationSans"
        except Exception:
            pass

    def _cerceve(self):
        m = 10.0
        self.msp.add_lwpolyline(
            [(m, m), (self.gen - m, m), (self.gen - m, self.yuk - m),
             (m, self.yuk - m)], close=True, dxfattribs={"layer": "00-CERCEVE"})

    # -- içerik ------------------------------------------------------------
    def kenarlar(self, kenarlar, katman: str, dx: float, dy: float,
                 merkezle=None):
        """build123d projeksiyon kenarlarını (dx,dy)'ye ölçekleyerek yazar."""
        k = self.k
        ox = oy = 0.0
        if merkezle is not None:
            ox, oy = merkezle
        for e in kenarlar:
            gt = e.geom_type
            if gt == GeomType.LINE:
                a, b = e @ 0, e @ 1
                self.msp.add_line(
                    ((a.X - ox) * k + dx, (a.Y - oy) * k + dy),
                    ((b.X - ox) * k + dx, (b.Y - oy) * k + dy),
                    dxfattribs={"layer": katman})
            elif gt == GeomType.CIRCLE:
                c, r = e.arc_center, e.radius
                cx, cy = (c.X - ox) * k + dx, (c.Y - oy) * k + dy
                if e.is_closed:
                    self.msp.add_circle((cx, cy), r * k,
                                        dxfattribs={"layer": katman})
                else:
                    a, b = e @ 0, e @ 1
                    sa = math.degrees(math.atan2(a.Y - c.Y, a.X - c.X))
                    ea = math.degrees(math.atan2(b.Y - c.Y, b.X - c.X))
                    self.msp.add_arc((cx, cy), r * k, sa, ea,
                                     dxfattribs={"layer": katman})
            else:   # elips/spline -> polyline (CAM güvenli)
                pts = [(((e @ (i / 24)).X - ox) * k + dx,
                        ((e @ (i / 24)).Y - oy) * k + dy) for i in range(25)]
                self.msp.add_lwpolyline(pts, dxfattribs={"layer": katman})

    def gorunus_yerlestir(self, sekil, yon: str, dx: float, dy: float,
                          gizli: bool = True, baslik: str = ""):
        """Bir ortografik görünüşü sayfaya yerleştirir. Konum = görünüşün
        SOL-ALT köşesi (kağıt mm)."""
        gor, giz = gorunus(sekil, yon)
        tum = list(gor) + list(giz)
        xs = [p.X for e in tum for p in (e @ 0, e @ 1)]
        ys = [p.Y for e in tum for p in (e @ 0, e @ 1)]
        ox, oy = min(xs), min(ys)
        if gizli:
            self.kenarlar(giz, "02-GIZLI", dx, dy, (ox, oy))
        self.kenarlar(gor, "01-GORUNEN", dx, dy, (ox, oy))
        if baslik:
            self.yazi(baslik, dx, dy - 6, h=3.0)
        return {"x": dx, "y": dy, "ox": ox, "oy": oy,
                "gen": (max(xs) - ox) * self.k, "yuk": (max(ys) - oy) * self.k,
                "model_gen": max(xs) - ox, "model_yuk": max(ys) - oy}

    def kesit_yerlestir(self, sekil, duzlem: Plane, dx: float, dy: float,
                        baslik: str = "KESİT A-A", tarama: bool = True):
        s = kesit(sekil, duzlem)
        bb = s.bounding_box()
        ox, oy = bb.min.X, bb.min.Y
        k = self.k
        for f in s.faces():
            for w in [f.outer_wire()] + list(f.inner_wires()):
                pts = []
                for e in w.edges():
                    for i in range(9):
                        p = e @ (i / 8)
                        pts.append(((p.X - ox) * k + dx, (p.Y - oy) * k + dy))
                self.msp.add_lwpolyline(pts, close=True,
                                        dxfattribs={"layer": "03-KESIT"})
                if tarama:
                    h = self.msp.add_hatch(color=9,
                                           dxfattribs={"layer": "04-TARAMA"})
                    h.set_pattern_fill("ANSI31", scale=0.4, angle=45)
                    h.paths.add_polyline_path(pts, is_closed=True)
        if baslik:
            self.yazi(baslik, dx, dy - 6, h=3.0)
        return {"x": dx, "y": dy, "ox": ox, "oy": oy,
                "gen": (bb.max.X - ox) * k, "yuk": (bb.max.Y - oy) * k,
                "model_gen": bb.max.X - ox, "model_yuk": bb.max.Y - oy}

    def olcu(self, sekil, yon: str):
        """Bir görünüşün KAĞIT mm cinsinden (genişlik, yükseklik)'i."""
        gor, giz = gorunus(sekil, yon)
        tum = list(gor) + list(giz)
        xs = [p.X for e in tum for p in (e @ 0, e @ 1)]
        ys = [p.Y for e in tum for p in (e @ 0, e @ 1)]
        return (max(xs) - min(xs)) * self.k, (max(ys) - min(ys)) * self.k

    def coklu_gorunus(self, sekil, yonler=("on", "sag", "ust"),
                      kesit_duzlemi: Plane | None = None,
                      sol: float = 26.0, alt: float = 52.0,
                      ust_bosluk: float = 22.0, sag_bosluk: float = 20.0,
                      bosluk: float = 26.0) -> dict:
        """3. açı izdüşüm düzeninde otomatik yerleşim.

           ÜST(plan)
           ÖN        YAN      KESİT

        Görünüşler önce ölçülür; sayfaya sığmıyorsa ölçek otomatik
        büyütülür (1:10 -> 1:20 -> 1:25 -> 1:50). Böylece hiçbir zaman
        kağıt dışına taşan çizim üretilmez.
        """
        adaylar = [self.olcek] + [o for o in (10, 15, 20, 25, 50, 100)
                                  if o > self.olcek]
        for olcek in adaylar:
            self.olcek, self.k = float(olcek), 1.0 / float(olcek)
            self._dimstyle_guncelle()
            ol = {y: self.olcu(sekil, y) for y in yonler}
            if kesit_duzlemi is not None:
                s = kesit(sekil, kesit_duzlemi)
                bb = s.bounding_box()
                ol["kesit"] = ((bb.max.X - bb.min.X) * self.k,
                               (bb.max.Y - bb.min.Y) * self.k)
            satir_gen = sum(ol[y][0] for y in ol if y != "ust") \
                + bosluk * (len(ol) - 2)
            ana_yuk = max(ol[y][1] for y in ol if y != "ust")
            toplam_yuk = ana_yuk + bosluk + (ol["ust"][1] if "ust" in ol else 0)
            if (satir_gen <= self.gen - sol - sag_bosluk
                    and toplam_yuk <= self.yuk - alt - ust_bosluk):
                break
        else:
            raise ValueError("Çizim hiçbir ölçekte A3'e sığmadı")

        y0 = alt
        yerler = {}
        x = sol
        for yon in yonler:
            if yon == "ust":
                continue
            yerler[yon] = self.gorunus_yerlestir(
                sekil, yon, x, y0, gizli=(yon != "ust"),
                baslik={"on": "ÖN GÖRÜNÜŞ", "sag": "YAN GÖRÜNÜŞ",
                        "sol": "SOL GÖRÜNÜŞ",
                        "arka": "ARKA GÖRÜNÜŞ"}.get(yon, yon.upper()))
            x += ol[yon][0] + bosluk

        if kesit_duzlemi is not None:
            yerler["kesit"] = self.kesit_yerlestir(
                sekil, kesit_duzlemi, x, y0, baslik="KESİT A-A")
            x += ol["kesit"][0] + bosluk

        if "ust" in yonler:
            yerler["ust"] = self.gorunus_yerlestir(
                sekil, "ust", sol, y0 + ana_yuk + bosluk, gizli=False,
                baslik="PLAN")

        yerler["_olcek"] = self.olcek
        yerler["_boyut"] = ol
        return yerler

    def _dimstyle_guncelle(self):
        self.doc.dimstyles.get("MOB").dxf.dimlfac = self.olcek

    # -- ölçülendirme ------------------------------------------------------
    def olcu_yatay(self, x1: float, x2: float, y: float, taban_y: float):
        self.msp.add_linear_dim(
            base=(0, taban_y), p1=(x1, y), p2=(x2, y),
            dimstyle="MOB", dxfattribs={"layer": "05-OLCU"}).render()

    def olcu_dikey(self, y1: float, y2: float, x: float, taban_x: float):
        self.msp.add_linear_dim(
            base=(taban_x, 0), p1=(x, y1), p2=(x, y2), angle=90,
            dimstyle="MOB", dxfattribs={"layer": "05-OLCU"}).render()

    def olcu_zinciri(self, noktalar: list[float], sabit: float,
                     taban: float, dikey: bool = True):
        """Raf yükseklikleri gibi zincir ölçü. noktalar KAĞIT mm."""
        pts = [(sabit, v) for v in noktalar] if dikey else [(v, sabit) for v in noktalar]
        self.msp.add_multi_point_linear_dim(
            base=(taban, 0) if dikey else (0, taban),
            points=pts, angle=90 if dikey else 0,
            dimstyle="MOB", dxfattribs={"layer": "05-OLCU"})

    def model_kagit(self, gor: dict, ma: float, mb: float) -> tuple:
        """Görünüşün MODEL koordinatını (ma, mb) kağıt mm'ye çevirir."""
        return (gor["x"] + (ma - gor["ox"]) * self.k,
                gor["y"] + (mb - gor["oy"]) * self.k)

    def oklu_not(self, metin: str, hedef: tuple, dx: float = 22.0,
                 dy: float = 12.0, h: float = 2.2):
        """Hedef noktayı gösteren atıf oku + açıklama yazısı.

        dx/dy: yazının hedefe göre kağıt mm cinsinden ötelenmesi.
        Negatif dx sola çeker (yazı sağdan sola hizalanır).
        """
        hx, hy = hedef
        kx, ky = hx + dx, hy + dy
        ux = kx + (6.0 if dx >= 0 else -6.0)
        self.msp.add_leader([(hx, hy), (kx, ky), (ux, ky)],
                            dxfattribs={"layer": "05-OLCU"})
        hiza = (TextEntityAlignment.LEFT if dx >= 0
                else TextEntityAlignment.RIGHT)
        self.msp.add_text(metin, height=h,
                          dxfattribs={"layer": "06-YAZI"}).set_placement(
            (ux + (1.5 if dx >= 0 else -1.5), ky + 1.0), align=hiza)

    def yazi(self, metin: str, x: float, y: float, h: float = 2.5,
             katman: str = "06-YAZI", hiza=TextEntityAlignment.LEFT):
        self.msp.add_text(metin, height=h,
                          dxfattribs={"layer": katman}).set_placement((x, y),
                                                                      align=hiza)

    def antet(self, baslik: str, alt: str, cizim_no: str, tarih: str,
              malzeme: str = "", cizen: str = ""):
        """ISO 7200 benzeri antet — sayfanın sağ-alt köşesi."""
        w, h = 150.0, 32.0
        x0, y0 = self.gen - 10 - w, 10.0
        self.msp.add_lwpolyline([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h),
                                 (x0, y0 + h)], close=True,
                                dxfattribs={"layer": "00-CERCEVE"})
        for dy in (8, 16, 24):
            self.msp.add_line((x0, y0 + dy), (x0 + w, y0 + dy),
                              dxfattribs={"layer": "00-CERCEVE"})
        self.msp.add_line((x0 + 95, y0), (x0 + 95, y0 + 24),
                          dxfattribs={"layer": "00-CERCEVE"})
        self.yazi(baslik, x0 + 3, y0 + 26.5, h=4.0)
        self.yazi(alt, x0 + 3, y0 + 18, h=2.5)
        self.yazi(f"Malzeme: {malzeme}", x0 + 3, y0 + 10, h=2.5)
        self.yazi(f"Çizen: {cizen}", x0 + 3, y0 + 2.5, h=2.5)
        self.yazi(f"Ölçek 1:{self.olcek:g}", x0 + 98, y0 + 18, h=2.5)
        self.yazi(f"Çizim no: {cizim_no}", x0 + 98, y0 + 10, h=2.5)
        self.yazi(tarih, x0 + 98, y0 + 2.5, h=2.5)
        self.yazi("Ölçüler mm · Birim: mm · 3. açı izdüşüm",
                  10 + 2, self.yuk - 10 - 5, h=2.5)

    # -- çıktı -------------------------------------------------------------
    def kaydet(self, klasor: str, ad: str, dpi: int = 300) -> dict[str, str]:
        os.makedirs(klasor, exist_ok=True)
        yollar = {}
        dxf = os.path.join(klasor, f"{ad}.dxf")
        self.doc.saveas(dxf)
        yollar["dxf"] = dxf

        sayfa = layout.Page(self.gen, self.yuk, layout.Units.mm,
                            layout.Margins.all(0))
        ayar = layout.Settings(scale=1, fit_page=False)   # 1 DXF birimi = 1 mm

        # TUZAK: bir PyMuPdfBackend'den HEM pdf HEM pixmap alma. İlk çıktı
        # backend'in içeriğini tüketiyor; ikincisi ölçeği ve konumu kaymış
        # (sayfaya sığdırılmış) bir görüntü veriyordu — PNG teknik çizim
        # sayfasında yarısı boş bir kağıt olarak görünüyordu.
        # Her çıktı için TEMİZ backend kurulur.
        def _backend():
            ctx = RenderContext(self.doc)
            be = PyMuPdfBackend()
            lp = LayoutProperties.from_layout(self.msp)
            lp.set_colors("#ffffff", "#000000")  # ZORUNLU — varsayılan koyu tema
            Frontend(ctx, be).draw_layout(self.msp, finalize=True,
                                          layout_properties=lp)
            return be

        pdf = os.path.join(klasor, f"{ad}.pdf")
        with open(pdf, "wb") as f:
            f.write(_backend().get_pdf_bytes(sayfa, settings=ayar))
        yollar["pdf"] = pdf

        png = os.path.join(klasor, f"{ad}.png")
        with open(png, "wb") as f:
            f.write(_backend().get_pixmap_bytes(sayfa, fmt="png", dpi=dpi,
                                                settings=ayar))
        yollar["png"] = png
        return yollar


# ---------------------------------------------------------------------------
# 4. CNC DXF (parça başına, R12)
# ---------------------------------------------------------------------------

def cnc_dxf(parca, delikler: list[dict], klasor: str,
            olcu: str = "kesim") -> str:
    """Tek parça için CNC DXF. Origin sol-alt, tüm koordinatlar pozitif.

    delikler: [{"x":.., "y":.., "cap":.., "derinlik":.., "tip":"pim"}, ...]
              x/y parçanın sol-alt köşesinden, mm.
    olcu    : "kesim" (bant payı düşülmüş — atölyeye giden) | "net"

    Katman sözleşmesi: KESIM / DELIK_<capx10>_<derinlikx10>.
    Atölye Homag/Thermwood/TpaCAD şablonu istiyorsa katman adlarını
    references/toolchain.md'deki tablodan uyarlayın — sabit değil.
    """
    os.makedirs(klasor, exist_ok=True)
    if olcu == "kesim":
        L, W = parca.kesim_olcusu()
    else:
        L, W = parca.boy, parca.en
    T = parca.kalinlik

    def katman_adi(cap: float, derinlik: float) -> str:
        return f"DELIK_{cap:g}_{derinlik:g}".replace(".", "P")

    # Delikleri gerçek silindir olarak üst yüzeyden çıkar
    p = Box(L, W, T, align=(Align.MIN, Align.MIN, Align.MIN))
    for d in delikler:
        c = Cylinder(d["cap"] / 2, d["derinlik"] + 0.5,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))
        p -= Pos(d["x"], d["y"], T - d["derinlik"]) * c

    ust = p.faces().sort_by(Axis.Z)[-1]
    duz = Pos(0, 0, -T) * ust        # Z=0'a indir; yoksa "non-planar" uyarısı

    exp = ExportDXF(version="AC1009", unit=Unit.MM)   # AC1009 = R12
    exp.add_layer("KESIM", color=ColorIndex.RED)
    exp.add_layer("CEP", color=ColorIndex.CYAN)
    exp.add_layer("ETIKET", color=ColorIndex.GRAY)
    for ad in {katman_adi(d["cap"], d["derinlik"]) for d in delikler}:
        exp.add_layer(ad, color=ColorIndex.BLUE)

    exp.add_shape(duz.outer_wire(), "KESIM")

    # İç konturları çaplarına göre katmanlara ayır
    for w in duz.inner_wires():
        es = w.edges()
        if len(es) == 1 and es[0].geom_type == GeomType.CIRCLE:
            r = es[0].radius
            eslesen = min(delikler, key=lambda d: abs(d["cap"] / 2 - r))
            ad = katman_adi(eslesen["cap"], eslesen["derinlik"])
        else:
            ad = "CEP"
        exp.add_shape(w, ad)

    exp._modelspace.add_text(
        f"{parca.kod} {L:g}x{W:g}x{T:g}", height=15,
        dxfattribs={"layer": "ETIKET"}).set_placement((20, W / 2))

    yol = os.path.join(klasor, f"{parca.kod}.dxf")
    exp.write(yol)
    return yol


# ---------------------------------------------------------------------------
# 5. YERLEŞİM (nesting) ŞEMASI ÇİZİMİ
# ---------------------------------------------------------------------------

def yerlesim_dxf(levhalar, klasor: str, ad: str, malzeme_adi: str,
                 olcek: float = 20.0) -> dict[str, str]:
    """mobilya.optimize() çıktısını görsel kesim planına çevirir."""
    s = Sayfa(olcek=olcek, boyut="A3")
    k = s.k
    x0, y0 = 20.0, 60.0
    for i, lv in enumerate(levhalar, 1):
        gx = x0 + (i - 1) * (lv.boy * k + 15)
        s.msp.add_lwpolyline(
            [(gx, y0), (gx + lv.boy * k, y0), (gx + lv.boy * k, y0 + lv.en * k),
             (gx, y0 + lv.en * k)], close=True,
            dxfattribs={"layer": "00-CERCEVE"})
        for y in lv.yerlesim:
            px, py = gx + y.x * k, y0 + y.y * k
            s.msp.add_lwpolyline(
                [(px, py), (px + y.boy * k, py),
                 (px + y.boy * k, py + y.en * k), (px, py + y.en * k)],
                close=True, dxfattribs={"layer": "01-GORUNEN"})
            s.yazi(f"{y.kod}", px + 1.5, py + y.en * k / 2, h=2.0)
            s.yazi(f"{y.boy:g}x{y.en:g}{' ↻' if y.dondu else ''}",
                   px + 1.5, py + y.en * k / 2 - 3, h=1.8)
        s.yazi(f"Levha {i} — verim %{lv.verim:.1f}", gx, y0 + lv.en * k + 4, h=3.5)
    s.antet(f"KESİM PLANI — {ad}", malzeme_adi,
            f"{ad}-NEST", "", malzeme_adi)
    return s.kaydet(klasor, f"{ad}-kesim-plani")
