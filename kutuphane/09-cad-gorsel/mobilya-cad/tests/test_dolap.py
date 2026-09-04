"""dolap.Dolap — bölge tabanlı üreteç: geometri kuralları, kontroller, BOM.

Bu testler build123d İSTEMEZ: yerleşim tipleri geometri.py'den gelir.
AYK-01 (MONOLİT) tanımı uret_final.py ile aynıdır — orada değişince
burada da değişmeli.
"""
import math
import unittest

import _yol  # noqa: F401
from dolap import (
    ARA_ON_BOSLUK, DERZ, RAF_ARKA_BOSLUK, RAF_ON_BOSLUK, Bolge, Dolap,
)
from mobilya import RAF_ARALIGI


def ayk01():
    G, D, H, BAZA, T, EGIM = 600.0, 260.0, 1850.0, 80.0, 18.0, 48.0
    KOTLAR = tuple(82 + i * 203 for i in range(6))
    return Dolap(
        genislik=G, derinlik=D, yukseklik=H, baza=BAZA, tam_kapak="tek",
        baza_icerlek="kapak", kalinlik=T, kod="AYK-01", ad="MONOLİT",
        bolgeler=[Bolge("raf", 1502, raf_kotlari=KOTLAR, egim=EGIM,
                        ad="ayakkabı bölgesi"),
                  Bolge("raf", 214, raf=0, ayakkabi=False, ad="üst dolap")])


class Ayk01(unittest.TestCase):
    def setUp(self):
        self.d = ayk01()

    def test_uyarisiz_ve_kapasite(self):
        self.assertEqual(self.d.uyarilar, [])
        self.assertEqual(self.d.cift, 18)
        self.assertTrue(self.d.sehim["uygun"])
        self.assertTrue(self.d.devrilme["stabilite_testi_gerekli"])

    def test_egimli_raf_kalinligi_yatayda_yer_kaplar(self):
        d = self.d
        beklenen = (d.ic_derinlik - RAF_ON_BOSLUK - RAF_ARKA_BOSLUK
                    - 18 * math.sin(math.radians(48)))
        self.assertAlmostEqual(d.raf_derinligi(48), beklenen)
        self.assertLess(d.raf_derinligi(48), d.raf_derinligi(0))

    def test_yukleme_acikligi_yeterli(self):
        ya = self.d.yukleme_acikligi(self.d.bolgeler[0])
        self.assertIsNotNone(ya)
        self.assertGreaterEqual(ya, RAF_ARALIGI["duz"])
        self.assertIsNone(self.d.yukleme_acikligi(self.d.bolgeler[1]))

    def test_kot_zinciri(self):
        z = self.d.kot_zinciri()
        self.assertEqual(z, sorted(z))
        self.assertEqual(z[:2], [0.0, 80.0])
        # 6 raf kotu zincirde: bölge tabanı 98 + 82 + i*203
        for i in range(6):
            self.assertIn(98 + 82 + i * 203, z)

    def test_parca_kodlari_tekil_ve_yerlesim_tutarli(self):
        kodlar = [p.kod for p in self.d.parcalar]
        self.assertEqual(len(kodlar), len(set(kodlar)))
        for y in self.d.yerlesim:
            self.assertIn(y.kod, kodlar, f"yerleşimde tanımsız parça {y.kod}")
        # her parça en az bir kez yerleşmiş
        for k in kodlar:
            self.assertTrue(any(y.kod == k for y in self.d.yerlesim), k)

    def test_tam_kapak_ve_mentese(self):
        d = self.d
        k, adet = d.p_tam_kapak
        kapak = next(p for p in d.parcalar if p.kod == k)
        self.assertEqual((adet, kapak.boy, kapak.en), (1, 1770 - 2 * DERZ, 600 - 2 * DERZ))
        self.assertEqual(kapak.bant, {"L1": 2.0, "L2": 2.0, "W1": 2.0, "W2": 2.0})
        m = next(x for x in d.donanim if "menteşe" in x[1].lower())
        self.assertEqual(m[3], 4)      # gövde 1770 > 1600 -> 4 menteşe
        # bölge kapakları tam kapak varken iptal
        self.assertTrue(all(b.kapak is None for b in d.bolgeler))

    def test_baza_kapak_hizali(self):
        d = self.d
        self.assertEqual(d.baza_icerlek, -18.0)
        self.assertEqual(d.on_yuzey(), -18.0)
        on = next(p for p in d.parcalar if p.kod == d.p_baza_on)
        self.assertEqual(on.boy, 600.0)            # tam genişlik
        self.assertTrue(on.desen_kilit)

    def test_ara_tabla_arkaligi_delmez(self):
        d = self.d
        ara = next(p for p in d.parcalar if p.kod == d.p_ara)
        self.assertEqual(ara.en, d.ic_derinlik - ARA_ON_BOSLUK)

    def test_render_olculeri_dis_olcu(self):
        etiketler = {o["etiket"] for o in self.d.render_olculeri() if o["sinif"] == "dis"}
        self.assertEqual(etiketler, {"1850", "600", "278"})   # 260 + 18 kapak

    def test_raf_delikleri_32lik(self):
        dl = self.d.raf_delikleri()
        self.assertTrue(dl)
        xs = sorted({h["x"] for h in dl})
        self.assertTrue(all(abs((b - a) - 32) < 1e-6 for a, b in zip(xs, xs[1:])))
        self.assertEqual({h["cap"] for h in dl}, {5.0})


class Kurallar(unittest.TestCase):
    def test_genis_aciklik_uyarisi(self):
        d = Dolap(genislik=1100, derinlik=500, yukseklik=2100, kod="T",
                  bolgeler=[Bolge("raf", 1900, raf=3, ayakkabi=False)])
        self.assertFalse(d.sehim["uygun"])
        self.assertTrue(any("Orta dikme" in u for u in d.uyarilar))

    def test_duz_rafta_ayakkabi_egim_uyarisi(self):
        d = Dolap(genislik=600, derinlik=260, yukseklik=1850, kod="T",
                  bolgeler=[Bolge("raf", 1734, raf=4, kapak="tek")])
        self.assertTrue(any("eğim gerekir" in u for u in d.uyarilar))

    def test_bolge_ayakkabi_tipi_dolabi_ezer(self):
        def kur(tip):
            return Dolap(genislik=600, derinlik=400, yukseklik=1850, kod="T",
                         bolgeler=[Bolge("raf", 1734, raf=4, ayakkabi_tipi=tip)])
        self.assertLess(kur("buyuk").cift, kur(None).cift)

    def test_cizme_yuksekligi_uyarisi(self):
        d = Dolap(genislik=600, derinlik=400, yukseklik=1850, kod="T",
                  bolgeler=[Bolge("cizme", 300), Bolge("raf", 1416, raf=3)])
        self.assertTrue(any("çizme" in u and "400" in u for u in d.uyarilar))

    def test_aski_sig_govde_alin_paneli(self):
        d = Dolap(genislik=700, derinlik=182, yukseklik=1850, kod="T",
                  tam_kapak="cift", baza_icerlek="kapak",
                  bolgeler=[Bolge("aski", 1500, kiyafet="ceket", alin=120),
                            Bolge("raf", 216, raf=0, ayakkabi=False)])
        self.assertEqual(d.aski["yon"], "y")
        self.assertFalse(any("ALIN PANELİ yok" in u for u in d.uyarilar))
        self.assertEqual(len(d.borular), 1)
        self.assertTrue(any("boru" in x[1].lower() for x in d.donanim))
        d2 = Dolap(genislik=700, derinlik=182, yukseklik=1850, kod="T",
                   bolgeler=[Bolge("aski", 1500, kiyafet="ceket")])
        self.assertTrue(any("ALIN PANELİ yok" in u for u in d2.uyarilar))

    def test_bolgeler_sigmiyor_uyarisi(self):
        # Gövde iki tabla + bir ara tabla bile almıyorsa uyarı verilir.
        d = Dolap(genislik=600, derinlik=300, yukseklik=120, baza=80, kod="T",
                  bolgeler=[Bolge("raf", 300, ayakkabi=False),
                            Bolge("raf", 300, ayakkabi=False)])
        self.assertTrue(any("sığmıyor" in u for u in d.uyarilar))
        # Sığıyorsa fark en büyük raf bölgesine yedirilir, uyarı yok.
        d2 = Dolap(genislik=600, derinlik=300, yukseklik=1850, kod="T",
                   bolgeler=[Bolge("raf", 300, ayakkabi=False),
                             Bolge("raf", 300, ayakkabi=False)])
        self.assertEqual(d2.uyarilar, [])
        self.assertAlmostEqual(sum(b.yukseklik for b in d2.bolgeler),
                               1850 - 80 - 3 * 18)

    def test_rapor_uyarilari_gizlemez(self):
        d = Dolap(genislik=1100, derinlik=500, yukseklik=2100, kod="T",
                  bolgeler=[Bolge("raf", 1900, raf=3, ayakkabi=False)])
        r = d.rapor()
        self.assertIn("-- UYARILAR", r)
        self.assertLess(r.index("-- UYARILAR"), r.index("MALZEME ÖZETİ"))


if __name__ == "__main__":
    unittest.main()
