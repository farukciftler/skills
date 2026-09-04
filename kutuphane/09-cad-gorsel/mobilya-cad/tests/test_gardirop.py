"""gardirop.Gardirop — sütunlu gövde: dikme, kuşak, çekmece, L gövde."""
import unittest

import _yol  # noqa: F401
from dolap import Bolge
from gardirop import Gardirop, Sutun

G, D, T = 1100.0, 482.0, 18.0


def sutunlu(**ek):
    ust = 2100 - 80 - 2 * T
    args = dict(genislik=G, derinlik=D, yukseklik=2100, baza=80,
                baza_icerlek="kapak", kapak="sutun", kod="T-GRD",
                sutunlar=[
                    Sutun([Bolge("aski", 1500, kiyafet="palto", ad="askı"),
                           Bolge("raf", ust - T - 1500, raf=0, ayakkabi=False,
                                 ad="depo")], ad="askı"),
                    Sutun([Bolge("cekmece", 700, raf=3, ad="çekmece"),
                           Bolge("raf", ust - T - 700, raf=3, ayakkabi=False,
                                 ad="raf")], ad="raf")])
    args.update(ek)
    return Gardirop(**args)


class Sutunlu(unittest.TestCase):
    def setUp(self):
        self.g = sutunlu()

    def test_dikme_yapisal(self):
        g = self.g
        self.assertEqual(g.dikme_sayisi, 1)
        self.assertIsNotNone(g.p_dikme)
        self.assertAlmostEqual(sum(g.sutun_gen) + T, g.ic_genislik)
        self.assertTrue(g.sehim["uygun"])                 # sütun açıklığı
        self.assertGreater(g.ic_genislik, g.max_ack)      # dikmesiz aşardı

    def test_parca_ve_yerlesim_tutarli(self):
        kodlar = [p.kod for p in self.g.parcalar]
        self.assertEqual(len(kodlar), len(set(kodlar)))
        for y in self.g.yerlesim:
            self.assertIn(y.kod, kodlar)
        for k in kodlar:
            self.assertTrue(any(y.kod == k for y in self.g.yerlesim), k)

    def test_bolgeler_kotlar_hizali(self):
        # Dolap arayüzü: düzleştirilmiş bölge ve kot listeleri aynı boyda
        self.assertEqual(len(self.g.bolgeler), len(self.g.kotlar))
        self.assertEqual(len(self.g.bolgeler), 4)

    def test_cekmece_ergonomi(self):
        self.assertFalse(any("1350" in u for u in self.g.uyarilar))
        ters = sutunlu(sutunlar=[
            Sutun([Bolge("raf", 1200, raf=3, ayakkabi=False),
                   Bolge("cekmece", 2100 - 80 - 3 * T - 1200, raf=3)])])
        self.assertTrue(any("1350" in u for u in ters.uyarilar))

    def test_cekmece_donanim_ve_bom(self):
        self.assertTrue(any("ray" in x[1].lower() for x in self.g.donanim))
        self.assertTrue(any(p.grup == "çekmece" and p.adet == 3
                            for p in self.g.parcalar))

    def test_kapak_kurali_cift(self):
        g = sutunlu(kapak="cift")
        self.assertTrue(all(adet == 2 for _, adet in g.p_kapak.values()))
        self.assertEqual(len(g.p_kapak), 2)

    def test_kapaksiz_sutun(self):
        g = sutunlu(sutunlar=[Sutun([Bolge("raf", 1966, raf=6, ayakkabi=False)],
                                    kapak="yok"),
                              Sutun([Bolge("aski", 1966, kiyafet="palto")])])
        self.assertEqual(list(g.p_kapak), [1])

    def test_mentese_adedi(self):
        m = [x for x in self.g.donanim if "menteşe" in x[1].lower()]
        self.assertEqual(len(m), 2)
        self.assertTrue(all(x[3] == 4 for x in m))     # gövde 2020 > 1600

    def test_rapor_sutun_duzeni(self):
        r = self.g.rapor()
        self.assertIn("-- SÜTUN DÜZENİ", r)
        self.assertIn("Sütun açıklığı", r)
        self.assertIn("-- DONANIM", r)


class OrtakAltVeL(unittest.TestCase):
    def kur(self, kusak=100.0, l_govde=True):
        yorgan = 600.0
        ust = 2200 - 80 - T - yorgan - T - T
        sag = (Sutun([], ad="açık", kapak="yok", ayna_arkalik=True,
                     ust_yukseklik=0.0) if l_govde else
               Sutun([Bolge("raf", ust, raf=3, ayakkabi=False)]))
        return Gardirop(
            genislik=G, derinlik=D, yukseklik=2200, baza=80,
            baza_icerlek="kapak", kapak="sutun", kod="T-L", kusak=kusak,
            ortak_alt=Bolge("raf", yorgan, raf=0, ayakkabi=False,
                            kapak="cift", ad="yorgan"),
            sutunlar=[Sutun([Bolge("aski", ust, kiyafet="palto")], ad="askı"),
                      sag])

    def test_kusak_zorunlu(self):
        self.assertTrue(any("ÖN KUŞAK" in u for u in self.kur(kusak=0).uyarilar))
        g = self.kur(kusak=100)
        self.assertFalse(any("ÖN KUŞAK" in u for u in g.uyarilar))
        self.assertTrue(g.kusak_sehim["uygun"])
        self.assertIsNotNone(g.p_kusak)

    def test_l_govde(self):
        g = self.kur()
        self.assertTrue(g.L_govde)
        self.assertTrue(any("L gövde" in u for u in g.uyarilar))
        self.assertIsNotNone(g.p_yan_sol)
        self.assertIsNotNone(g.p_yan_sag)
        self.assertIsNotNone(g.p_ark2)
        self.assertEqual(list(g.p_sirt), [1])
        self.assertTrue(any(x[0].endswith("-DB") for x in g.donanim))
        sol = next(p for p in g.parcalar if p.kod == g.p_yan_sol)
        sag = next(p for p in g.parcalar if p.kod == g.p_yan_sag)
        self.assertGreater(sol.boy, sag.boy)
        self.assertIn("L2", sag.bant)          # üst kenarı görünür, bantlı

    def test_ortak_kapak_tam_genislik(self):
        g = self.kur()
        k, adet = g.p_ortak_kapak
        kapak = next(p for p in g.parcalar if p.kod == k)
        self.assertEqual(adet, 2)
        self.assertAlmostEqual(kapak.en, (G - 3 * 3.0) / 2)

    def test_dikdortgen_govde_tek_arkalik(self):
        g = self.kur(l_govde=False)
        self.assertFalse(g.L_govde)
        self.assertIsNone(g.p_ark2)
        self.assertEqual(g.p_sirt, {})


if __name__ == "__main__":
    unittest.main()
