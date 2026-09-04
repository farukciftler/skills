"""
belge.py — ürün tasarım dosyası (PDF) şablonu.

Her mobilya için tek dosyada: kapak · her yönden render · açıklamalı iç
detay · ölçülü teknik çizim · kesim listesi · donanım · üretim notları.

Kaynak: spec sheet / tear sheet pratiği —
  • kapak sayfasında TEK büyük görsel, sayfanın yarısından fazlası
  • dış ölçü DAİMA Y × G × D mm olarak, en üstte
  • malzeme "kaliteli ahşap" gibi belirsiz değil, ÖLÇÜLEBİLİR yazılır
    (EN 312 P2, 18 mm, E1, 2 mm PVC bant)
  • mekanizma, taşıma kapasitesi ve geçerli test standardı ayrı satır
  • montaj/özel işlem notları ayrı bölüm
  https://pro.houzz.com/pro-learn/blog/startup-guide-interior-design-how-to-make-spec-sheet-with-template
  https://oaklandfurnitures.com/how-to-write-office-furniture-specification/

Açıklama sayfalarındaki oklu notlar ÖLÇÜ İÇERMEZ — render "bu ne" anlatır.
Ölçüler iki yerde durur: bağlayıcı olan teknik çizim, ve ayrı bir
"Ölçülü görsel" sayfası — orada ölçü çizgileri 3B modelden kamera
izdüşümüyle rendera oturtulur (elle konmuş yazı yoktur, ölçü değişince
çizgi de rakam da kendiliğinden yerine düşer).

Kullanım:
    from belge import TasarimBelgesi
    TasarimBelgesi(dolap, "cikti/AYK-01").uret()
"""

from __future__ import annotations

import csv
import datetime as _dt
import json
import math
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

# ---------------------------------------------------------------------------
# Kimlik
# ---------------------------------------------------------------------------

MUREKKEP = HexColor("#211F1B")
SOLUK = HexColor("#6B665C")
MESE = HexColor("#A8763A")
CIZGI = HexColor("#DED8CD")
ZEMIN = HexColor("#F6F4EF")
BEYAZ = HexColor("#FFFFFF")

_FONTLAR = [
    ("Gov", "/System/Library/Fonts/Supplemental/Arial.ttf"),
    ("GovB", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("GovI", "/System/Library/Fonts/Supplemental/Arial Italic.ttf"),
]


def _fontlari_yukle():
    """Türkçe karakter için TTF gömülür — reportlab'ın yerleşik Helvetica'sı
    WinAnsi'dir ve ş/ğ/ı taşımaz."""
    for ad, yol in _FONTLAR:
        if ad in pdfmetrics.getRegisteredFontNames():
            continue
        if not os.path.exists(yol):
            raise FileNotFoundError(f"Font yok: {yol}")
        pdfmetrics.registerFont(TTFont(ad, yol))


MM = 72.0 / 25.4      # mm -> punto


# ---------------------------------------------------------------------------
# Açıklama etiketi yerleşimi
# ---------------------------------------------------------------------------

ETIKET_GEN = 33.0 * MM      # açıklama sütunu genişliği
ETIKET_SATIR = 3.4 * MM     # satır yüksekliği
ETIKET_PUNTO = 7.6


def _satirla(metin, gen=ETIKET_GEN, font="Gov", punto=ETIKET_PUNTO):
    """Metni verilen genişliğe göre satırlara böler."""
    satirlar, cur = [], ""
    for k in metin.split():
        dene = (cur + " " + k).strip()
        if pdfmetrics.stringWidth(dene, font, punto) > gen and cur:
            satirlar.append(cur)
            cur = k
        else:
            cur = dene
    if cur:
        satirlar.append(cur)
    return satirlar


def _etiket_yerlesimi(notlar, res_x, res_y, res_g, res_y_boy,
                      sol_gen, sag_gen, satir_yuk):
    """Okların etiketlerini sol/sağ sütuna dağıtır, dikeyde çakıştırmaz.

    Hedefi görüntünün solunda kalanlar SOL sütuna, sağında kalanlar SAĞ
    sütuna gider; her sütunda etiketler hedef yüksekliğine göre sıralanıp
    minimum aralık zorlanır (klasik atıf yerleşimi).

    Etiketin yüksekliği SATIR SAYISINDAN gelir — sabit satır aralığı
    kullanılırsa 5 satırlık bir açıklama bir üstündekinin içine girer.
    Metin `ey`'den YUKARI doğru yazıldığı için sınır, bloğun tepesidir.
    """
    sol, sag = [], []
    for n in notlar:
        if not n.get("gorunur", True):
            continue
        hx = res_x + n["x"] / n["_gen"] * res_g
        hy = res_y + n["y"] / n["_yuk"] * res_y_boy
        (sol if n["x"] < n["_gen"] * 0.5 else sag).append(
            {"metin": n["metin"], "hx": hx, "hy": hy,
             "_sat": len(_satirla(n["metin"]))})

    def diz(grup, x_etiket):
        grup.sort(key=lambda a: -a["hy"])          # üstten alta
        ust = res_y + res_y_boy
        for a in grup:
            tepe_payi = (a["_sat"] - 1) * ETIKET_SATIR
            y = min(a["hy"], ust - tepe_payi)
            a["ex"], a["ey"] = x_etiket, y
            ust = y - max(satir_yuk * 0.25, ETIKET_SATIR * 0.9)
        # sayfa dışına taşarsa yukarı kaydır
        tasma = res_y - ust
        if tasma > 0:
            for a in grup:
                a["ey"] += tasma
        return grup

    return (diz(sol, res_x - 4 * MM), diz(sag, res_x + res_g + 4 * MM))


# ---------------------------------------------------------------------------
# Belge
# ---------------------------------------------------------------------------

def _cakisma(lx, ly, gen, yuk, yerlesik) -> bool:
    """Etiket kutusu daha önce yerleştirilmiş bir kutuyla kesişiyor mu."""
    for x, y, w, hh in yerlesik:
        if (abs(lx - x) < (gen + w) / 2 + 1.2 * MM
                and abs(ly - y) < (yuk + hh) / 2 + 1.0 * MM):
            return True
    return False


class TasarimBelgesi:
    def __init__(self, dolap, klasor: str, marka: str = "",
                 render_klasor: str = "render", dekor: str = "Meşe"):
        self.d = dolap
        self.klasor = klasor
        self.marka = marka
        self.dekor = dekor
        self.rk = os.path.join(klasor, render_klasor)
        self.tarih = _dt.date.today().isoformat()
        _fontlari_yukle()
        self.gor = {}
        yol = os.path.join(self.rk, "goruntuler.json")
        if os.path.exists(yol):
            self.gor = json.load(open(yol, encoding="utf-8"))

    # -- yardımcılar -------------------------------------------------------
    def _resim(self, ad):
        k = self.gor.get(ad)
        if not k:
            return None
        y = os.path.join(self.rk, k["dosya"])
        return y if os.path.exists(y) else None

    def _sayfa_basligi(self, c, W, H, ust: str, alt: str = ""):
        c.setFont("GovB", 8)
        c.setFillColor(MESE)
        c.drawString(18 * MM, H - 13 * MM, ust.upper())
        if alt:
            c.setFont("Gov", 8)
            c.setFillColor(SOLUK)
            c.drawRightString(W - 18 * MM, H - 13 * MM, alt)
        c.setStrokeColor(CIZGI)
        c.setLineWidth(0.5)
        c.line(18 * MM, H - 16 * MM, W - 18 * MM, H - 16 * MM)

    def _altbilgi(self, c, W, no, toplam):
        c.setStrokeColor(CIZGI)
        c.setLineWidth(0.5)
        c.line(18 * MM, 14 * MM, W - 18 * MM, 14 * MM)
        c.setFont("Gov", 7)
        c.setFillColor(SOLUK)
        c.drawString(18 * MM, 10 * MM,
                     f"{self.d.kod} · {self.d.ad}"
                     + (f" · {self.marka}" if self.marka else ""))
        c.drawCentredString(W / 2, 10 * MM, "Ölçüler mm")
        c.drawRightString(W - 18 * MM, 10 * MM, f"{no} / {toplam}")

    def _kucult(self, yol, hedef_px):
        """PNG renderları sayfada gerekenden çok daha büyük; PDF'e JPEG
        olarak, hedef genişlikte gömülür. 12 MB -> ~2 MB, gözle fark yok."""
        try:
            from PIL import Image
        except ImportError:
            return yol
        onbellek = os.path.join(self.rk, "_pdf")
        os.makedirs(onbellek, exist_ok=True)
        cikti = os.path.join(onbellek,
                             os.path.splitext(os.path.basename(yol))[0]
                             + f"_{hedef_px}.jpg")
        if os.path.exists(cikti) and \
                os.path.getmtime(cikti) > os.path.getmtime(yol):
            return cikti
        im = Image.open(yol).convert("RGB")
        if im.width > hedef_px:
            im = im.resize((hedef_px, round(im.height * hedef_px / im.width)),
                           Image.LANCZOS)
        im.save(cikti, "JPEG", quality=88, optimize=True)
        return cikti

    def _oran_ciz(self, c, yol, x, y, gen, yuk, hedef_px=1000):
        """Görüntüyü (x,y,gen,yuk) kutusuna oranı bozmadan sığdırır.
        Yerleştirilen gerçek dikdörtgeni döndürür."""
        yol = self._kucult(yol, hedef_px)
        im = ImageReader(yol)
        iw, ih = im.getSize()
        o = min(gen / iw, yuk / ih)
        g, h = iw * o, ih * o
        px, py = x + (gen - g) / 2, y + (yuk - h) / 2
        c.drawImage(im, px, py, g, h, mask="auto")
        return px, py, g, h

    # -- 1. kapak ----------------------------------------------------------
    def _kapak(self, c, W, H):
        d = self.d
        c.setFillColor(ZEMIN)
        c.rect(0, 0, W, H, stroke=0, fill=1)

        c.setFont("Gov", 8)
        c.setFillColor(SOLUK)
        c.drawString(18 * MM, H - 20 * MM,
                     (self.marka + "  ·  " if self.marka else "")
                     + "ÜRÜN TASARIM DOSYASI")
        c.drawRightString(W - 18 * MM, H - 20 * MM, self.tarih)

        c.setFont("GovB", 30)
        c.setFillColor(MUREKKEP)
        c.drawString(18 * MM, H - 34 * MM, d.ad)
        c.setFont("Gov", 11)
        c.setFillColor(MESE)
        c.drawString(18 * MM, H - 41 * MM, d.kod)

        if d.aciklama:
            c.setFont("Gov", 9.5)
            c.setFillColor(SOLUK)
            yy = H - 50 * MM
            for satir in d.aciklama.split("\n"):
                c.drawString(18 * MM, yy, satir)
                yy -= 4.6 * MM

        # hero
        hero = self._resim("uc_ceyrek") or self._resim("on")
        if hero:
            self._oran_ciz(c, hero, 18 * MM, 62 * MM,
                           W - 36 * MM, H - 128 * MM)

        # künye şeridi
        y0 = 30 * MM
        c.setStrokeColor(CIZGI)
        c.setLineWidth(0.5)
        c.line(18 * MM, y0 + 20 * MM, W - 18 * MM, y0 + 20 * MM)
        c.line(18 * MM, y0, W - 18 * MM, y0)

        kunye = self._kunye()
        n = len(kunye)
        gen = (W - 36 * MM) / n
        for i, (bas, deg) in enumerate(kunye):
            x = 18 * MM + i * gen
            if i:
                c.setStrokeColor(CIZGI)
                c.line(x - 3 * MM, y0, x - 3 * MM, y0 + 20 * MM)
            c.setFont("Gov", 7)
            c.setFillColor(SOLUK)
            c.drawString(x, y0 + 14.5 * MM, bas.upper())
            c.setFont("GovB", 12)
            c.setFillColor(MUREKKEP)
            c.drawString(x, y0 + 6.5 * MM, deg)

    def _kunye(self):
        d = self.d
        dis = self._dis_olcu()
        k = [("Dış ölçü (Y×G×D)",
              f"{dis[2]:.0f}×{dis[0]:.0f}×{dis[1]:.0f}"),
             ("Gövde", f"{d.T:g} mm suntalam")]
        aski = [b for b in d.bolgeler if b.tip == "aski"]
        if aski:
            n = sum(int(cc.split()[0]) for _, cc in d.detay if "askı" in cc)
            k.append(("Askı", f"{n} adet"))
        if d.cift:
            k.append(("Kapasite", f"~{d.cift} çift"))
        k.append(("Ağırlık",
                  f"{sum(p.agirlik_kg() for p in d.parcalar):.0f} kg"))
        return k

    def _dis_olcu(self):
        """Kapak/baza dahil GERÇEK dış ölçü (G, D, Y)."""
        d = self.d
        return (d.G, d.D - d.on_yuzey(), d.H)

    # -- 2. görünüşler -----------------------------------------------------
    def _gorunusler(self, c, W, H):
        self._sayfa_basligi(c, W, H, "Görünüşler",
                            "kapalı hâl · her yönden")
        setler = ["on", "sag", "arka", "sol", "uc_ceyrek", "ust"]
        setler = [a for a in setler if self._resim(a)]
        sut, sat = 3, 2
        gx = (W - 36 * MM) / sut
        gy = (H - 46 * MM) / sat
        for i, ad in enumerate(setler[:sut * sat]):
            cx = 18 * MM + (i % sut) * gx
            cy = H - 24 * MM - (i // sut + 1) * gy
            self._oran_ciz(c, self._resim(ad), cx, cy + 7 * MM,
                           gx - 4 * MM, gy - 12 * MM, hedef_px=520)
            c.setFont("Gov", 8)
            c.setFillColor(SOLUK)
            c.drawString(cx, cy + 2 * MM,
                         self.gor[ad]["baslik"].upper())

    # -- 3. açıklamalı iç detay -------------------------------------------
    def _ic_detay(self, c, W, H, ad, baslik):
        self._sayfa_basligi(c, W, H, baslik,
                            "açıklamalar ölçü içermez — ölçüler teknik çizimde")
        k = self.gor.get(ad)
        yol = self._resim(ad)
        if not yol:
            return
        # görüntüyü ortaya, iki yanda etiket sütunu bırakarak yerleştir
        kutu_x = 38 * MM
        kutu_g = W - 76 * MM
        kutu_y = 20 * MM
        kutu_yuk = H - 44 * MM
        px, py, g, h = self._oran_ciz(c, yol, kutu_x, kutu_y, kutu_g, kutu_yuk)

        notlar = []
        for n in k.get("notlar", []):
            n = dict(n)
            n["_gen"], n["_yuk"] = k["gen"], k["yuk"]
            notlar.append(n)
        if not notlar:
            return
        # PDF'te y yukarı artar; render y'si üstten aşağı -> ters çevir
        for n in notlar:
            n["y"] = k["yuk"] - n["y"]
        sol, sag = _etiket_yerlesimi(notlar, px, py, g, h,
                                     0, 0, 13 * MM)

        c.setLineWidth(0.6)
        for grup, saga_hizali in ((sol, True), (sag, False)):
            for a in grup:
                c.setStrokeColor(MESE)
                uc = a["ex"] + (0 if saga_hizali else 0)
                c.line(a["hx"], a["hy"], uc, a["ey"])
                # hedefte küçük daire
                c.setFillColor(MESE)
                c.circle(a["hx"], a["hy"], 1.1 * MM, stroke=0, fill=1)
                # metin
                c.setFillColor(MUREKKEP)
                c.setFont("Gov", 7.6)
                self._sarmalı_yaz(c, a["metin"], uc, a["ey"],
                                  33 * MM, saga_hizali)

    def _sarmalı_yaz(self, c, metin, x, y, gen, saga_hizali, satir=3.4):
        satirlar = _satirla(metin, gen)
        for i, s in enumerate(satirlar):
            yy = y + (len(satirlar) - 1 - i) * satir * MM - 1 * MM
            if saga_hizali:
                c.drawRightString(x - 2 * MM, yy, s)
            else:
                c.drawString(x + 2 * MM, yy, s)

    # -- ölçülü görsel -----------------------------------------------------
    def _olcu_gorunusu(self):
        """Ölçülendirmeye en uygun render: iç düzeni gösteren, gövdenin
        sağında ölçü zincirine yer kalan kare."""
        for ad in ("acik", "acik_ceyrek", "ic_detay", "on", "uc_ceyrek"):
            if self.gor.get(ad, {}).get("olculer") and self._resim(ad):
                return ad
        return None

    def _olculu_gorsel(self, c, W, H):
        ad = self._olcu_gorunusu()
        if not ad:
            return
        self._sayfa_basligi(c, W, H, "Ölçülü görsel",
                            "ölçüler 3B modelden projekte edildi · mm")
        k = self.gor[ad]
        px, py, g, h = self._oran_ciz(c, self._resim(ad), 12 * MM, 30 * MM,
                                      W - 24 * MM, H - 56 * MM, hedef_px=1500)
        self._olcu_ciz(c, k.get("olculer", []), px, py, g, h,
                       k["gen"], k["yuk"])
        c.setFont("Gov", 7.5)
        c.setFillColor(SOLUK)
        c.drawString(18 * MM, 22 * MM,
                     "Zincir ölçüler: kaide üstü · her göz · bölge sınırları "
                     "— NET iç ölçüdür. Koyu ölçüler kapak ve kaide dahil "
                     "dış ölçüdür.")
        c.drawString(18 * MM, 18.5 * MM,
                     "Ölçü çizgileri 3B modelin kamera izdüşümüdür; "
                     "BAĞLAYICI ölçü teknik çizim sayfasındadır.")

    def _olcu_ciz(self, c, olculer, px, py, g, h, gen, yuk, punto=6.6):
        """Render üzerine ölçü çizgisi + rakam.

        Uç noktalar 3B'den geldiği için perspektifle uyumludur. Rakam,
        ölçü doğrusunun DIŞ tarafına, arkasına opak plaka konarak yazılır;
        çakışan rakamlar kılavuz çizgisiyle dışarı itilir.
        """
        if not olculer:
            return
        sx, sy = g / gen, h / yuk

        def P(x, y):
            return px + x * sx, py + h - y * sy

        yerlesik = []
        c.setLineWidth(0.5)
        for o in olculer:
            if not o.get("kadrajda", True):
                continue
            ax, ay = P(o["ax"], o["ay"])
            bx, by = P(o["bx"], o["by"])
            dx, dy = P(o["dx"], o["dy"])
            uzun = math.hypot(bx - ax, by - ay)
            if uzun < 0.7 * MM:
                continue
            ux, uy = (bx - ax) / uzun, (by - ay) / uzun
            # dışa kaçış yönünü doğrultuya DİK bileşene indirge
            wx, wy = dx - ax, dy - ay
            t = wx * ux + wy * uy
            nx, ny = wx - t * ux, wy - t * uy
            nn = math.hypot(nx, ny) or 1.0
            nx, ny = nx / nn, ny / nn

            dis = o.get("sinif") == "dis"
            renk = MUREKKEP if dis else MESE
            c.setStrokeColor(renk)
            c.setLineWidth(0.7 if dis else 0.5)
            c.line(ax, ay, bx, by)
            tik = 1.5 * MM if dis else 1.15 * MM
            for ex, ey in ((ax, ay), (bx, by)):
                c.line(ex - nx * tik, ey - ny * tik,
                       ex + nx * tik, ey + ny * tik)

            metin = o["etiket"]
            fnt = "GovB" if dis else "Gov"
            gen_m = pdfmetrics.stringWidth(metin, fnt, punto)
            yuk_m = punto * 0.72
            mx, my = (ax + bx) / 2, (ay + by) / 2
            off = (3.0 if dis else 2.4) * MM + gen_m / 2 * abs(nx)
            lx, ly = mx + nx * off, my + ny * off
            adim = 0
            while adim < 7 and _cakisma(lx, ly, gen_m, yuk_m, yerlesik):
                adim += 1
                lx += nx * 3.6 * MM
                ly += ny * 3.6 * MM
            if adim:
                c.setLineWidth(0.35)
                c.line(mx + nx * 1.2 * MM, my + ny * 1.2 * MM,
                       lx - nx * (gen_m / 2 + 0.8 * MM),
                       ly - ny * (yuk_m / 2 + 0.6 * MM))
            yerlesik.append((lx, ly, gen_m, yuk_m))

            c.saveState()
            c.setFillColor(BEYAZ)
            c.setFillAlpha(0.88)
            c.rect(lx - gen_m / 2 - 0.9 * MM, ly - yuk_m / 2 - 0.6 * MM,
                   gen_m + 1.8 * MM, yuk_m + 1.2 * MM, stroke=0, fill=1)
            c.restoreState()
            c.setFont(fnt, punto)
            c.setFillColor(renk)
            c.drawCentredString(lx, ly - yuk_m * 0.42, metin)

    # -- 4. teknik çizim ---------------------------------------------------
    def _teknik_cizim(self, c, W, H):
        self._sayfa_basligi(c, W, H, "Teknik çizim",
                            "ön · yan · plan · kesit A-A")
        png = os.path.join(self.klasor, f"{self.d.kod}-CIZIM.png")
        if os.path.exists(png):
            self._oran_ciz(c, png, 12 * MM, 18 * MM,
                           W - 24 * MM, H - 40 * MM, hedef_px=2600)

    # -- 5. kesim listesi --------------------------------------------------
    def _kesim_listesi(self, c, W, H):
        self._sayfa_basligi(c, W, H, "Kesim listesi",
                            "kesim ölçüsü = net ölçü − kenar bandı payı")
        yol = os.path.join(self.klasor, f"{self.d.kod}-BOM.csv")
        if not os.path.exists(yol):
            return
        satirlar = list(csv.DictReader(open(yol, encoding="utf-8-sig"),
                                       delimiter=";"))
        basliklar = [("Kod", 20), ("Parça", 44), ("Net", 22), ("Kesim", 22),
                     ("Kal.", 11), ("Ad.", 8), ("Desen", 13), ("Bant", 22)]
        x0, y = 18 * MM, H - 26 * MM
        c.setFont("Gov", 6.5)
        c.setFillColor(SOLUK)
        x = x0
        for b, w in basliklar:
            c.drawString(x, y, b.upper())
            x += w * MM
        y -= 2 * MM
        c.setStrokeColor(MUREKKEP)
        c.setLineWidth(0.7)
        c.line(x0, y, W - 18 * MM, y)
        y -= 4.5 * MM

        for r in satirlar:
            if y < 26 * MM:
                break
            x = x0
            hucre = [r["Kod"], r["Parça"][:40],
                     f'{r["Net_Boy"]}×{r["Net_En"]}',
                     f'{r["Kesim_Boy"]}×{r["Kesim_En"]}',
                     r["Kalınlık"], r["Adet"], r["Desen"],
                     r["Bant_L1/L2/W1/W2"]]
            for (b, w), v in zip(basliklar, hucre):
                c.setFont("GovB" if b == "Kod" else "Gov", 7)
                c.setFillColor(MUREKKEP if b in ("Kod", "Parça") else SOLUK)
                c.drawString(x, y, str(v))
                x += w * MM
            y -= 3 * MM
            c.setStrokeColor(CIZGI)
            c.setLineWidth(0.3)
            c.line(x0, y, W - 18 * MM, y)
            y -= 3.6 * MM

        # malzeme özeti
        y -= 4 * MM
        c.setFont("GovB", 8)
        c.setFillColor(MUREKKEP)
        c.drawString(x0, y, "MALZEME")
        y -= 5 * MM
        c.setFont("Gov", 7.5)
        c.setFillColor(SOLUK)
        from mobilya import MALZEMELER, bant_ozeti, optimize
        for (mlz, kal) in sorted({(p.malzeme, p.kalinlik)
                                  for p in self.d.parcalar}):
            grup = [p for p in self.d.parcalar
                    if p.malzeme == mlz and p.kalinlik == kal]
            lv = optimize(grup, mlz, kal)
            m = MALZEMELER[mlz]
            alan = sum(p.alan_m2() for p in grup)
            brut = len(lv) * m.levha_alani()
            c.drawString(x0, y, f"{m.ad} {kal:g} mm — {len(lv)} levha "
                                f"({m.levha_boy:g}×{m.levha_en:g}), "
                                f"{alan:.2f} m² parça, verim %{100*alan/brut:.0f}")
            y -= 4 * MM
        for t, dd in bant_ozeti(self.d.parcalar).items():
            c.drawString(x0, y, f"Kenar bandı {t:g} mm × "
                                f"{self.d.T + 4:g} mm PVC — sipariş "
                                f"{dd['siparis_m']:.1f} m "
                                f"(kesim payı ve %10 fire dahil)")
            y -= 4 * MM

    # -- 6. donanım + notlar ----------------------------------------------
    def _notlar(self, c, W, H):
        d = self.d
        self._sayfa_basligi(c, W, H, "Donanım ve üretim notları")
        x0, y = 18 * MM, H - 26 * MM

        if getattr(d, "donanim", None):
            c.setFont("GovB", 9)
            c.setFillColor(MUREKKEP)
            c.drawString(x0, y, "DONANIM")
            y -= 6 * MM
            for kod, ad, olcu, adet, notu in d.donanim:
                c.setFont("GovB", 7.5)
                c.setFillColor(MUREKKEP)
                c.drawString(x0, y, kod)
                c.setFont("Gov", 7.5)
                c.drawString(x0 + 24 * MM, y, ad)
                c.setFillColor(SOLUK)
                c.drawString(x0 + 90 * MM, y, f"{olcu}  × {adet}")
                y -= 3.6 * MM
                if notu:
                    c.setFont("Gov", 6.8)
                    c.drawString(x0 + 24 * MM, y, notu)
                    y -= 3.6 * MM
                y -= 1.6 * MM
            y -= 4 * MM

        # bölge düzeni
        c.setFont("GovB", 9)
        c.setFillColor(MUREKKEP)
        c.drawString(x0, y, "İÇ DÜZEN")
        y -= 6 * MM
        for i, b in enumerate(d.bolgeler):
            c.setFont("GovB", 7.5)
            c.setFillColor(MUREKKEP)
            c.drawString(x0, y, f"{i+1}. {b.ad or b.tip}")
            c.setFont("Gov", 7.5)
            c.setFillColor(SOLUK)
            c.drawString(x0 + 46 * MM, y,
                         f"net {b.yukseklik:.0f} mm"
                         + (f" · {b.raf} raf" if b.raf else "")
                         + (f" · {b.egim:g}° eğimli" if b.egim else ""))
            y -= 3.6 * MM
            if b.not_:
                c.setFont("Gov", 6.8)
                for s in self._boler(b.not_, 150 * MM, 6.8):
                    c.drawString(x0 + 4 * MM, y, s)
                    y -= 3.2 * MM
            y -= 1.6 * MM

        # kontroller / standart
        y -= 3 * MM
        c.setFont("GovB", 9)
        c.setFillColor(MUREKKEP)
        c.drawString(x0, y, "KONTROLLER VE STANDART")
        y -= 6 * MM
        s = d.sehim
        dv = d.devrilme
        kontrol = [
            f"Raf sehimi — {s['aciklik_mm']:.0f} mm açıklıkta "
            f"{s['sehim_sunmeli_mm']} mm (sünme dahil) = {s['oran']}; "
            f"kabul {s['limit']} (EN 14749 65 kg/m² tasarım yükü).",
            f"Devrilme — h={dv['yukseklik_mm']:.0f} mm, kütle "
            f"{dv['kutle_kg']} kg, h_ağırlık×kütle = {dv['h_cg_m_x_kg']} "
            f"(EN 14749 md. 6.2.1 eşiği 6).",
        ]
        if dv["stabilite_testi_gerekli"]:
            kontrol.append(
                "Devrilme braketi ZORUNLU — EN 14749 md. 3.17 RİJİT METAL "
                "braket şart koşar; naylon kayış veya kablo bağı kabul "
                "edilmez. Braket ve montaj talimatı ürünle verilir.")
        kontrol.append(
            f"Levha — EN 312 P2, kalınlık toleransı ±0,3 mm. Kanal ve "
            f"geçmeler nominal {d.T:g} mm'ye göre değil, gelen partinin "
            f"ölçülen kalınlığına göre açılır.")
        for t in kontrol:
            c.setFont("Gov", 7.5)
            c.setFillColor(SOLUK)
            for ss in self._boler(t, 158 * MM, 7.5):
                c.drawString(x0, y, ss)
                y -= 3.4 * MM
            y -= 2 * MM

        # Kapasiteye SAYILMAYAN gözler — sayı şişirmemek için burada durur
        gn = getattr(d, "goz_notlari", [])
        if gn:
            y -= 2 * MM
            c.setFont("GovB", 9)
            c.setFillColor(MUREKKEP)
            c.drawString(x0, y, "KAPASİTE — SAYILMAYAN GÖZLER")
            y -= 6 * MM
            for n in gn:
                c.setFont("Gov", 7.5)
                c.setFillColor(SOLUK)
                for ss in self._boler(n, 158 * MM, 7.5):
                    c.drawString(x0, y, ss)
                    y -= 3.4 * MM
                y -= 2 * MM

        if d.uyarilar:
            y -= 2 * MM
            c.setFont("GovB", 9)
            c.setFillColor(MESE)
            c.drawString(x0, y, "UYARILAR")
            y -= 6 * MM
            for u in d.uyarilar:
                c.setFont("Gov", 7.5)
                c.setFillColor(MESE)
                for ss in self._boler(u, 158 * MM, 7.5):
                    c.drawString(x0, y, ss)
                    y -= 3.4 * MM
                y -= 2 * MM

    def _boler(self, metin, gen, punto):
        kel, out, cur = metin.split(), [], ""
        for k in kel:
            dene = (cur + " " + k).strip()
            if pdfmetrics.stringWidth(dene, "Gov", punto) > gen and cur:
                out.append(cur)
                cur = k
            else:
                cur = dene
        if cur:
            out.append(cur)
        return out

    # -- üret --------------------------------------------------------------
    def uret(self, dosya: str = None) -> str:
        d = self.d
        dosya = dosya or os.path.join(self.klasor,
                                      f"{d.kod}-TASARIM-DOSYASI.pdf")
        A4d = A4
        A3y = landscape(A3)
        c = rl_canvas.Canvas(dosya, pagesize=A4d)
        c.setTitle(f"{d.kod} {d.ad} — Tasarım Dosyası")
        c.setAuthor(self.marka or "mobilya-cad")

        sayfalar = []
        sayfalar.append(("kapak", A4d))
        if self.gor:
            sayfalar.append(("gorunusler", A4d))
            if self._olcu_gorunusu():
                sayfalar.append(("olculu", A4d))
            if self._resim("acik_ceyrek"):
                sayfalar.append(("acik", A4d))
            if self._resim("ic_detay"):
                sayfalar.append(("detay", A4d))
        sayfalar.append(("cizim", A3y))
        sayfalar.append(("bom", A4d))
        sayfalar.append(("notlar", A4d))
        n = len(sayfalar)

        for i, (tip, boyut) in enumerate(sayfalar, 1):
            c.setPageSize(boyut)
            W, H = boyut
            if tip == "kapak":
                self._kapak(c, W, H)
            elif tip == "gorunusler":
                self._gorunusler(c, W, H)
            elif tip == "olculu":
                self._olculu_gorsel(c, W, H)
            elif tip == "acik":
                self._ic_detay(c, W, H, "acik_ceyrek",
                               "Açık hâl · parça açıklamaları")
            elif tip == "detay":
                self._ic_detay(c, W, H, "ic_detay",
                               "İç detay · yakın görünüş")
            elif tip == "cizim":
                self._teknik_cizim(c, W, H)
            elif tip == "bom":
                self._kesim_listesi(c, W, H)
            elif tip == "notlar":
                self._notlar(c, W, H)
            if tip != "kapak":
                self._altbilgi(c, W, i, n)
            c.showPage()

        c.save()
        print(f"[belge] {dosya}  ({n} sayfa)")
        return dosya
