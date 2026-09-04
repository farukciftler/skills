"""
ayakkabilik.py — parametrik ayakkabılık üreteci (skill'in referans örneği).

İki tip:
  "devrilir" : ince koridor dolabı, devrilir (tip-out) kapaklı — Häfele
               Dresscode mekanizmasına göre boyutlanır
  "rafli"    : klasik raflı/kapaklı gövde

Çalıştırma:
    ~/mobilya-venv/bin/python ayakkabilik.py --tip devrilir --genislik 800

Tüm mühendislik kuralları mobilya.py'den gelir; burada sadece geometri
kurulur. Ölçü değiştirince kontroller otomatik yeniden çalışır.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mobilya import (
    AYAKKABI, DEVRILIR_AYAKKABILIK, DEVRILIR_ARA_RAF_KALINLIK,
    DEVRILIR_GENISLIK_KAYBI, DEVRILIR_MIN_RAF_YUKSEKLIK, MALZEMELER,
    RAF_ARALIGI, SISTEM32, Parca, bom_csv, cift_sayisi, devrilme_kontrolu,
    max_aciklik, optimize, optimize_dogrula, ozet_rapor, raf_sehimi,
)


# ---------------------------------------------------------------------------
# TASARIM
# ---------------------------------------------------------------------------

class Ayakkabilik:
    def __init__(self, *, tip="devrilir", genislik=800.0, derinlik=280.0,
                 yukseklik=1150.0, baza=80.0, kalinlik=18.0,
                 malzeme="suntalam", goz=3, sira=2, arkalik=3.0,
                 ayakkabi_tipi="karma", kod="AYK-01", ad="Ayakkabılık"):
        self.tip = tip
        self.G, self.D, self.H = float(genislik), float(derinlik), float(yukseklik)
        self.baza = float(baza)
        self.T = float(kalinlik)
        self.malzeme = malzeme
        self.goz = int(goz)          # devrilir kapak sayısı / raf gözü
        self.sira = int(sira)        # kapak başına ayakkabı sırası
        self.ark = float(arkalik)
        self.ayk = ayakkabi_tipi
        self.kod, self.ad = kod, ad

        self.uyarilar: list[str] = []
        self.parcalar: list[Parca] = []
        self.yerlesim = []
        self._hesapla()

    # -- türetilen ölçüler -------------------------------------------------
    @property
    def ic_genislik(self):
        return self.G - 2 * self.T

    @property
    def ic_derinlik(self):
        """Arkalık kanalı gerisini düşen net iç derinlik."""
        return self.D - self.ark - 12.0     # 12 mm kanal-arka kenar mesafesi

    @property
    def govde_yuksekligi(self):
        return self.H - self.baza

    def _hesapla(self):
        self.mek = DEVRILIR_AYAKKABILIK.get(self.sira) if self.tip == "devrilir" else None

        # --- kontrol: mekanizma derinliği
        if self.mek:
            if self.ic_derinlik < self.mek["min_derinlik"]:
                self.uyarilar.append(
                    f"İç derinlik {self.ic_derinlik:.0f} mm < mekanizma "
                    f"minimumu {self.mek['min_derinlik']:.0f} mm "
                    f"({self.sira} sıra, Häfele {self.mek['art']}). "
                    f"Toplam derinliği en az "
                    f"{self.mek['min_derinlik'] + self.ark + 12:.0f} mm yap.")
            self.net_genislik = self.ic_genislik - DEVRILIR_GENISLIK_KAYBI
        else:
            self.net_genislik = self.ic_genislik

        # --- kapasite
        self.cift_raf = cift_sayisi(self.net_genislik, self.ayk)
        self.toplam_cift = self.cift_raf * self.goz * (self.sira if self.mek else 1)

        # --- düşey bölünme
        ic_yuk = self.govde_yuksekligi - 2 * self.T
        self.goz_yuksekligi = ic_yuk / self.goz
        if self.mek and self.mek["montaj_yuksekligi"]:
            if self.goz_yuksekligi < self.mek["montaj_yuksekligi"]:
                self.uyarilar.append(
                    f"Göz yüksekliği {self.goz_yuksekligi:.0f} mm < mekanizma "
                    f"montaj yüksekliği {self.mek['montaj_yuksekligi']:.0f} mm. "
                    f"Göz sayısını azalt veya gövdeyi yükselt.")
        if not self.mek and self.goz_yuksekligi < RAF_ARALIGI[
                "karma" if self.ayk == "karma" else "duz"]:
            self.uyarilar.append(
                f"Raf aralığı {self.goz_yuksekligi:.0f} mm — "
                f"{RAF_ARALIGI['karma']:.0f} mm altı, ayakkabı sığmayabilir.")

        # --- sehim
        self.sehim = raf_sehimi(aciklik=self.ic_genislik,
                                derinlik=self.ic_derinlik,
                                kalinlik=self.T, malzeme=self.malzeme)
        self.max_ack = max_aciklik(self.ic_derinlik, self.T, self.malzeme)
        if not self.sehim["uygun"]:
            self.uyarilar.append(
                f"Raf açıklığı {self.ic_genislik:.0f} mm, {self.T:g} mm "
                f"{MALZEMELER[self.malzeme].ad} için fazla "
                f"(limit {self.max_ack:.0f} mm, sehim "
                f"{self.sehim['sehim_sunmeli_mm']} mm = {self.sehim['oran']}). "
                f"Orta dikme ekle veya ön kuşak koy.")

        self._parcalar()
        self._yerlestir()

        # --- devrilme (parça ağırlıkları hazır olduktan sonra)
        kutle = sum(p.agirlik_kg() for p in self.parcalar) + self.toplam_cift * 0.8
        self.devrilme = devrilme_kontrolu(self.H, kutle, self.H * 0.45)

    # -- parça listesi -----------------------------------------------------
    def _parcalar(self):
        T, G, D = self.T, self.G, self.D
        gy = self.govde_yuksekligi
        M = self.malzeme
        P = self.parcalar

        # Yan paneller: boy = yükseklik (desen dikey), en = derinlik
        P.append(Parca(f"{self.kod}-P01", "Yan panel", gy, D, T, M, adet=2,
                       desen_kilit=True, grup="gövde",
                       bant={"W1": 2.0, "L1": 0.8, "L2": 0.8},
                       not_="ön kenar 2 mm bant · desen dikey"))
        # Üst ve alt tabla: yanlar arasına girer
        P.append(Parca(f"{self.kod}-P02", "Üst tabla", self.ic_genislik, D, T, M,
                       adet=1, grup="gövde", bant={"W1": 2.0},
                       not_="yanlar arasına"))
        P.append(Parca(f"{self.kod}-P03", "Alt tabla", self.ic_genislik, D, T, M,
                       adet=1, grup="gövde", bant={"W1": 2.0}))

        if self.tip == "devrilir":
            # Kapaklar
            kapak_yuk = self.goz_yuksekligi - 4.0      # 4 mm derz
            kapak_gen = G - 4.0
            P.append(Parca(f"{self.kod}-P04", "Devrilir kapak", kapak_yuk,
                           kapak_gen, T, M, adet=self.goz, desen_kilit=True,
                           grup="kapak", bant={"L1": 2.0, "L2": 2.0,
                                               "W1": 2.0, "W2": 2.0},
                           not_="4 kenar 2 mm bant · desen dikey · "
                                "aralarında min 10 mm derz"))
            # Mekanizma ara rafı — 10 mm, 18 DEĞİL
            P.append(Parca(f"{self.kod}-P05", "Mekanizma ara rafı",
                           self.ic_genislik - 33.0, self.ic_derinlik - 20,
                           DEVRILIR_ARA_RAF_KALINLIK, M,
                           adet=self.goz * self.sira, grup="mekanizma",
                           bant={"W1": 0.8},
                           not_=f"KALINLIK {DEVRILIR_ARA_RAF_KALINLIK:g} mm — "
                                f"mekanizma şartı. Boy = iç genişlik - 33"))
            # Gözler arası sabit ara tabla
            if self.goz > 1:
                P.append(Parca(f"{self.kod}-P06", "Ara tabla",
                               self.ic_genislik, D - 20, T, M,
                               adet=self.goz - 1, grup="gövde",
                               bant={"W1": 2.0}))
        else:
            raf_adet = max(self.goz - 1, 1)
            P.append(Parca(f"{self.kod}-P04", "Raf", self.ic_genislik - 2.0,
                           D - 25.0, T, M, adet=raf_adet, grup="raf",
                           bant={"W1": 2.0},
                           not_="Ø5 pim üzerine · 32'lik sisteme oturur"))
            P.append(Parca(f"{self.kod}-P05", "Kapak", gy - 4.0,
                           (G - 6.0) / 2, T, M, adet=2, desen_kilit=True,
                           grup="kapak", bant={"L1": 2.0, "L2": 2.0,
                                               "W1": 2.0, "W2": 2.0},
                           not_="Ø35 menteşe yuvası, kenardan 22 mm eksen"))

        # Baza
        if self.baza > 0:
            P.append(Parca(f"{self.kod}-P07", "Baza ön", self.ic_genislik,
                           self.baza, T, M, adet=1, grup="gövde",
                           bant={"L1": 2.0},
                           not_="öne göre 50 mm içeri — süpürgelik payı"))
            P.append(Parca(f"{self.kod}-P08", "Baza yan", D - 60, self.baza,
                           T, M, adet=2, grup="gövde"))

        # Arkalık — HDF, kanal içine
        P.append(Parca(f"{self.kod}-P09", "Arkalık", gy - 2 * T + 16.0,
                       self.ic_genislik + 16.0, self.ark, "hdf", adet=1,
                       grup="gövde",
                       not_="4 mm kanal içine, kanal derinliği 8 mm, "
                            "arka kenardan 12 mm · havalandırma delikleri"))

    # -- 3B yerleştirme ----------------------------------------------------
    def _yerlestir(self):
        from cizim import Yerlestirme
        T, G, D = self.T, self.G, self.D
        b = self.baza
        gy = self.govde_yuksekligi
        Y = self.yerlesim

        # Yan paneller: kalınlık X'te, boy (yükseklik) Z'de
        Y.append(Yerlestirme(f"{self.kod}-P01", (0, 0, b), "x", "z"))
        Y.append(Yerlestirme(f"{self.kod}-P01", (G - T, 0, b), "x", "z"))
        # Tablalar: kalınlık Z'de, boy (genişlik) X'te
        Y.append(Yerlestirme(f"{self.kod}-P03", (T, 0, b), "z", "x"))
        Y.append(Yerlestirme(f"{self.kod}-P02", (T, 0, b + gy - T), "z", "x"))

        if self.tip == "devrilir":
            gh = self.goz_yuksekligi
            kh = gh - 4.0
            for i in range(self.goz):
                z = b + T + i * gh
                # Kapak: kalınlık Y'de, boy (yükseklik) Z'de
                Y.append(Yerlestirme(f"{self.kod}-P04", (2.0, -T, z + 2.0),
                                     "y", "z", renk="#E8DCC8"))
                for s in range(self.sira):
                    Y.append(Yerlestirme(
                        f"{self.kod}-P05",
                        (T + 16.5, 25,
                         z + 45 + s * (kh - 100) / max(self.sira, 1)),
                        "z", "x", renk="#B0A090"))
                if i < self.goz - 1:
                    Y.append(Yerlestirme(f"{self.kod}-P06",
                                         (T, 10, z + gh - T), "z", "x"))
        else:
            ic_yuk = gy - 2 * T
            for i in range(1, self.goz):
                Y.append(Yerlestirme(
                    f"{self.kod}-P04",
                    (T + 1, 12.5, b + T + i * ic_yuk / self.goz), "z", "x"))
            for i in range(2):
                Y.append(Yerlestirme(f"{self.kod}-P05",
                                     (2.0 + i * (G - 2.0) / 2, -T, b + 2.0),
                                     "y", "z", renk="#E8DCC8"))

        if self.baza > 0:
            # Baza ön: kalınlık Y'de, boy (genişlik) X'te, en = yükseklik Z
            Y.append(Yerlestirme(f"{self.kod}-P07", (T, 50, 0), "y", "x"))
            # Baza yan: kalınlık X'te, boy (derinlik) Y'de, en = yükseklik
            Y.append(Yerlestirme(f"{self.kod}-P08", (T, 50, 0), "x", "y"))
            Y.append(Yerlestirme(f"{self.kod}-P08", (G - 2 * T, 50, 0),
                                 "x", "y"))

        # Arkalık: kalınlık Y'de, boy (yükseklik) Z'de
        Y.append(Yerlestirme(f"{self.kod}-P09",
                             (T - 8, D - 12 - self.ark, b + T - 8),
                             "y", "z", renk="#8B7355"))

    # -- sistem 32 delik tablosu -------------------------------------------
    def raf_delikleri(self) -> list[dict]:
        """Yan panelin iç yüzündeki Ø5 raf pimi delikleri."""
        s = SISTEM32
        delikler = []
        y_on = s["on_kenar_mesafe"]
        y_arka = self.D - s["arka_kenar_mesafe"]
        z = s["ilk_delik"]
        ust_sinir = self.govde_yuksekligi - 2 * self.T - 50
        while z < ust_sinir:
            for y in (y_on, y_arka):
                delikler.append({"x": z, "y": y, "cap": s["cap"],
                                 "derinlik": s["derinlik"], "tip": "raf_pimi"})
            z += s["adim"]
        return delikler

    # -- rapor -------------------------------------------------------------
    def rapor(self) -> str:
        r = []
        r.append("=" * 74)
        r.append(f"{self.ad}  [{self.kod}]  —  {self.tip.upper()}")
        r.append("=" * 74)
        r.append(f"Dış ölçü        : {self.G:.0f} G × {self.D:.0f} D × "
                 f"{self.H:.0f} Y mm  (baza {self.baza:.0f})")
        r.append(f"İç ölçü         : {self.ic_genislik:.0f} × "
                 f"{self.ic_derinlik:.0f} mm")
        r.append(f"Malzeme         : {MALZEMELER[self.malzeme].ad} "
                 f"{self.T:g} mm  ·  arkalık {self.ark:g} mm HDF")
        if self.mek:
            r.append(f"Mekanizma       : Häfele {self.mek['art']} "
                     f"({self.sira} sıra) · min derinlik "
                     f"{self.mek['min_derinlik']:.0f} mm · eğim "
                     f"{self.mek['aci_derece']}° · cep köşegeni "
                     f"{self.mek['cep_kosegen']:.0f} mm")
            r.append(f"                  Net iç genişlik "
                     f"{self.net_genislik:.0f} mm (mekanizma −25 mm)")
        r.append(f"Kapasite        : göz başına {self.cift_raf} çift × "
                 f"{self.goz} göz"
                 + (f" × {self.sira} sıra" if self.mek else "")
                 + f" = ~{self.toplam_cift} ÇİFT")
        r.append(f"                  ({AYAKKABI[self.ayk]['boy']:.0f} mm "
                 f"ayakkabı boyu, {AYAKKABI[self.ayk]['cift_genislik']:.0f} "
                 f"mm/çift)")
        r.append("")
        r.append("-- YAPISAL KONTROL " + "-" * 55)
        r.append(f"Raf açıklığı    : {self.sehim['aciklik_mm']:.0f} mm  →  "
                 f"sehim {self.sehim['sehim_mm']} mm "
                 f"(sünmeyle {self.sehim['sehim_sunmeli_mm']} mm) = "
                 f"{self.sehim['oran']}  [limit {self.sehim['limit']}]  "
                 f"{'✓' if self.sehim['uygun'] else '✗'}")
        r.append(f"Maks. açıklık   : {self.max_ack:.0f} mm "
                 f"({self.T:g} mm {self.malzeme}, 65 kg/m² EN 14749 yükü)")
        d = self.devrilme
        r.append(f"Devrilme        : h={d['yukseklik_mm']:.0f} mm · "
                 f"m={d['kutle_kg']} kg · h_cg×m={d['h_cg_m_x_kg']} "
                 f"(eşik 6)  →  "
                 f"{'TEST GEREKLİ' if d['stabilite_testi_gerekli'] else 'tetik yok'}")
        r.append(f"                  {d['aciklama']}")
        if self.uyarilar:
            r.append("")
            r.append("-- UYARILAR " + "-" * 62)
            for u in self.uyarilar:
                r.append(f"  ⚠ {u}")
        r.append("")
        r.append(ozet_rapor(self.parcalar))
        return "\n".join(r)


# ---------------------------------------------------------------------------
# ÜRETİM
# ---------------------------------------------------------------------------

def uret(a: Ayakkabilik, klasor: str, olcek: float = 10.0,
         cnc: bool = True) -> dict:
    """Tam paket: 3B + BOM + teknik çizim + kesim planı + CNC DXF."""
    import cizim
    from build123d import Plane

    os.makedirs(klasor, exist_ok=True)
    cikti = {}
    tarih = _dt.date.today().isoformat()

    print(a.rapor())

    # 1. BOM
    cikti["bom"] = bom_csv(a.parcalar, os.path.join(klasor, f"{a.kod}-BOM.csv"))
    with open(os.path.join(klasor, f"{a.kod}-RAPOR.txt"), "w",
              encoding="utf-8") as f:
        f.write(a.rapor())

    # 2. 3B model
    asm = cizim.model_kur(a.parcalar, a.yerlesim, a.ad)
    cikti.update(cizim.disa_aktar(asm, klasor, a.kod))
    kati = asm.solids()
    birlesik = kati[0]
    for s in kati[1:]:
        birlesik = birlesik + s

    # 3. Teknik çizim — A3, 3 görünüş + kesit (otomatik yerleşim)
    s = cizim.Sayfa(olcek=olcek, boyut="A3")
    g = s.coklu_gorunus(birlesik, ("on", "sag", "ust"),
                        kesit_duzlemi=Plane.YZ.offset(a.G / 2))
    k = s.k
    on, sag = g["on"], g["sag"]

    # ölçüler (kağıt mm cinsinden; DIMLFAC gerçek mm yazdırır)
    s.olcu_yatay(on["x"], on["x"] + a.G * k, on["y"], on["y"] - 11)
    s.olcu_dikey(on["y"], on["y"] + a.H * k, on["x"], on["x"] - 11)
    s.olcu_yatay(sag["x"], sag["x"] + a.D * k, sag["y"], sag["y"] - 11)
    if a.tip == "devrilir" and a.goz > 1:
        gh = a.goz_yuksekligi * k
        s.olcu_zinciri(
            [on["y"] + a.baza * k + i * gh for i in range(a.goz + 1)],
            on["x"] + a.G * k, on["x"] + a.G * k + 12, dikey=True)

    s.yazi(f"Kapasite ~{a.toplam_cift} çift  ·  raf açıklığı "
           f"{a.ic_genislik:.0f} mm ({a.sehim['oran']})  ·  "
           f"{'devrilir mekanizma ' + a.mek['art'] if a.mek else 'raflı'}",
           26, s.yuk - 22, h=2.5)
    s.antet(a.ad, f"{a.G:.0f}×{a.D:.0f}×{a.H:.0f} mm · {a.tip}",
            f"{a.kod}-01", tarih, MALZEMELER[a.malzeme].ad, "mobilya-cad")
    cikti.update({f"cizim_{k2}": v
                  for k2, v in s.kaydet(klasor, f"{a.kod}-CIZIM").items()})

    # 4. Kesim planı
    for mlz, kal in sorted({(p.malzeme, p.kalinlik) for p in a.parcalar}):
        lv = optimize(a.parcalar, mlz, kal)
        hatalar = optimize_dogrula(lv)
        if hatalar:
            print("!! yerleşim hatası:", hatalar)
        y = cizim.yerlesim_dxf(lv, klasor, f"{a.kod}-{mlz}{kal:g}",
                               f"{MALZEMELER[mlz].ad} {kal:g} mm")
        cikti[f"kesim_{mlz}_{kal:g}"] = y["pdf"]

    # 5. CNC DXF — yan panel (delikli), diğerleri düz
    if cnc:
        cnc_klasor = os.path.join(klasor, "cnc")
        yan = a.parcalar[0]
        cikti["cnc_yan"] = cizim.cnc_dxf(yan, a.raf_delikleri(), cnc_klasor)
        for p in a.parcalar[1:]:
            cizim.cnc_dxf(p, [], cnc_klasor)

    return cikti


def main():
    ap = argparse.ArgumentParser(description="Parametrik ayakkabılık üreteci")
    ap.add_argument("--tip", default="devrilir", choices=["devrilir", "rafli"])
    ap.add_argument("--genislik", type=float, default=800)
    ap.add_argument("--derinlik", type=float, default=280)
    ap.add_argument("--yukseklik", type=float, default=1150)
    ap.add_argument("--baza", type=float, default=80)
    ap.add_argument("--kalinlik", type=float, default=18)
    ap.add_argument("--malzeme", default="suntalam")
    ap.add_argument("--goz", type=int, default=3)
    ap.add_argument("--sira", type=int, default=2)
    ap.add_argument("--kod", default="AYK-01")
    ap.add_argument("--ad", default="Ayakkabılık")
    ap.add_argument("--cikti", default="cikti")
    ap.add_argument("--olcek", type=float, default=10)
    a = ap.parse_args()

    dolap = Ayakkabilik(
        tip=a.tip, genislik=a.genislik, derinlik=a.derinlik,
        yukseklik=a.yukseklik, baza=a.baza, kalinlik=a.kalinlik,
        malzeme=a.malzeme, goz=a.goz, sira=a.sira, kod=a.kod, ad=a.ad)
    yollar = uret(dolap, a.cikti, olcek=a.olcek)
    print("\n-- ÇIKTILAR " + "-" * 62)
    for k, v in yollar.items():
        print(f"  {k:16s} {v}")


if __name__ == "__main__":
    main()
