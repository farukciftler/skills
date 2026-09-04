"""mobilya.py — saf Python çekirdek: BOM, bant, nesting, sehim, devrilme, askı.

Çalıştırma (build123d GEREKMEZ):
    python3 -m unittest discover -s .claude/skills/mobilya-cad/tests
"""
import math
import os
import tempfile
import unittest

import _yol  # noqa: F401
from mobilya import (
    EN14749_TASARIM_YUKU, MALZEMELER, SEHIM_SINIRI, Parca, aski_kapasitesi,
    aski_yonu, bant_ozeti, bom_satirlari, cift_sayisi, devrilme_kontrolu,
    donanim_csv, egim_gerekli, egimli_raf, kusakli_sehim, max_aciklik,
    optimize, optimize_dogrula, raf_sehimi,
)


class KesimOlcusu(unittest.TestCase):
    def test_bant_payi_esikle_dusulur(self):
        # L1/L2 boy kenarları -> EN kısalır. 0.8 mm eşiğin altında, düşülmez.
        p = Parca("T01", "raf", 750, 300, 18, bant={"L1": 2.0, "L2": 0.8})
        self.assertEqual(p.kesim_olcusu(), (750.0, 298.0))
        self.assertEqual(p.kesim_olcusu(esik=0.5), (750.0, 297.2))

    def test_w_kenarlari_boyu_kisaltir(self):
        p = Parca("T02", "yan", 1770, 260, 18, bant={"W1": 2.0, "W2": 2.0})
        self.assertEqual(p.kesim_olcusu(), (1766.0, 260.0))

    def test_bant_metraji_adet_dahil(self):
        p = Parca("T03", "kapak", 750, 300, 18, adet=2,
                  bant={"L1": 2.0, "W1": 2.0})
        self.assertAlmostEqual(p.bant_metraji()[2.0], (750 + 300) * 2 / 1000)

    def test_bom_satiri_net_ve_kesim_ayri(self):
        p = Parca("T04", "raf", 750, 300, 18, bant={"L1": 2.0})
        r = bom_satirlari([p])[0]
        self.assertEqual((r["Net_Boy"], r["Net_En"]), ("750", "300"))
        self.assertEqual((r["Kesim_Boy"], r["Kesim_En"]), ("750", "298"))
        self.assertEqual(r["Bant_L1/L2/W1/W2"], "2/0/0/0")

    def test_bant_ozeti_kesim_payi_ve_fire(self):
        p = Parca("T05", "raf", 1000, 300, 18, adet=1, bant={"L1": 2.0})
        o = bant_ozeti([p], fire=0.10, kesim_payi_mm=37.5)[2.0]
        self.assertAlmostEqual(o["net_m"], 1.0)
        self.assertAlmostEqual(o["kesim_payi_m"], 0.04, places=2)
        self.assertAlmostEqual(o["siparis_m"], round((1.0 + 0.0375) * 1.1, 1))


class Nesting(unittest.TestCase):
    def test_giyotin_yerlesim_cakismasiz(self):
        parcalar = [Parca(f"P{i:02d}", "x", 600, 400, 18, adet=3)
                    for i in range(4)]
        lv = optimize(parcalar, "suntalam", 18.0)
        self.assertEqual(optimize_dogrula(lv), [])
        self.assertEqual(sum(len(l.yerlesim) for l in lv), 12)
        for l in lv:
            self.assertTrue(0 < l.verim <= 100)

    def test_desen_kilitli_parca_dondurulmez(self):
        # 2700 x 400: desen yönünde levhaya (2800) sığar; döndürülse en'e sığmaz.
        p = Parca("K01", "kapak", 2700, 400, 18, adet=2, desen_kilit=True)
        lv = optimize([p], "suntalam", 18.0)
        self.assertEqual(optimize_dogrula(lv), [])
        self.assertTrue(all(not y.dondu for l in lv for y in l.yerlesim))

    def test_levhaya_sigmayan_parca_hata(self):
        with self.assertRaises(ValueError):
            optimize([Parca("B01", "dev", 3000, 500, 18)], "suntalam", 18.0)

    def test_farkli_malzeme_karistirilmaz(self):
        pp = [Parca("S1", "a", 600, 400, 18, malzeme="suntalam"),
              Parca("H1", "b", 600, 400, 3, malzeme="hdf")]
        lv = optimize(pp, "hdf", 3.0)
        self.assertEqual([y.kod for l in lv for y in l.yerlesim], ["H1#1"])


class Sehim(unittest.TestCase):
    def test_formul(self):
        # δ = 5wL⁴/(384EI) — elle hesapla
        L, b, h = 700.0, 300.0, 18.0
        E = MALZEMELER["suntalam"].e_modul
        I = b * h ** 3 / 12
        w = EN14749_TASARIM_YUKU * 9.81 * b / 1e6
        delta = 5 * w * L ** 4 / (384 * E * I)
        s = raf_sehimi(L, b, h)
        self.assertAlmostEqual(s["sehim_mm"], round(delta, 2))
        self.assertAlmostEqual(s["sehim_sunmeli_mm"], round(delta * 1.5, 2))
        self.assertTrue(s["uygun"])

    def test_max_aciklik_limitte(self):
        # max_aciklik'te L/δ tam SEHIM_SINIRI olmalı
        Lmax = max_aciklik(300, 18)
        s = raf_sehimi(Lmax, 300, 18)
        self.assertAlmostEqual(Lmax / s["sehim_mm"], SEHIM_SINIRI, delta=2)
        # 18 mm suntalamda 750 mm civarı — SKILL.md'deki kural
        self.assertTrue(700 < max_aciklik(245, 18) < 760)

    def test_genis_aciklik_uygun_degil(self):
        self.assertFalse(raf_sehimi(1064, 467, 18)["uygun"])

    def test_kusak_atalet_kazanci(self):
        duz = kusakli_sehim(1064, 467, 18, 0)
        kusakli = kusakli_sehim(1064, 467, 18, 100)
        self.assertAlmostEqual(duz["kazanc"], 1.0)
        self.assertGreater(kusakli["kazanc"], 10)
        self.assertLess(kusakli["sehim_mm"], duz["sehim_mm"])
        tekil = kusakli_sehim(1064, 467, 18, 100, tekil_yuk_kg=25)
        self.assertGreater(tekil["sehim_mm"], kusakli["sehim_mm"])


class Devrilme(unittest.TestCase):
    def test_iki_parcali_tetik(self):
        # EN 14749 6.2.1: yükseklik > 600 VE h_cg(m)·m > 6 birlikte
        self.assertTrue(devrilme_kontrolu(1850, 57.5, 832)["stabilite_testi_gerekli"])
        self.assertFalse(devrilme_kontrolu(1850, 5.0, 832)["stabilite_testi_gerekli"])
        self.assertFalse(devrilme_kontrolu(550, 80.0, 250)["stabilite_testi_gerekli"])

    def test_rijit_braket_metni(self):
        d = devrilme_kontrolu(1850, 57.5, 832)
        self.assertIn("RİJİT METAL", d["aciklama"])
        self.assertIn("kayış", d["aciklama"].lower())


class Aski(unittest.TestCase):
    def test_one_bakan_rahat(self):
        a = aski_yonu(560, 1000)
        self.assertTrue(a["one_bakan"] and a["rahat"])
        self.assertEqual((a["yon"], a["boru_boyu"]), ("x", 1000))

    def test_one_bakan_sikisik(self):
        a = aski_yonu(480, 1000)
        self.assertTrue(a["one_bakan"])
        self.assertFalse(a["rahat"])
        self.assertIn("SIKIŞIK", a["aciklama"])

    def test_sig_govde_profilden(self):
        a = aski_yonu(167, 664)
        self.assertEqual((a["yon"], a["boru_boyu"]), ("y", 167))
        self.assertIn("ÖNDEN ARKAYA", a["aciklama"])

    def test_aski_kurulamaz(self):
        self.assertIsNone(aski_yonu(167, 400)["yon"])

    def test_kapasite(self):
        self.assertEqual(aski_kapasitesi(432, "palto"), 4)
        self.assertEqual(aski_kapasitesi(432, "gomlek"), 10)


class Ayakkabi(unittest.TestCase):
    def test_egim_gerekli(self):
        self.assertEqual(egim_gerekli(320), 0.0)
        self.assertAlmostEqual(egim_gerekli(245), math.degrees(math.acos(245 / 320)), places=6)

    def test_egimli_raf(self):
        e = egimli_raf(245, 48, 203)
        self.assertTrue(e["sigar"])
        self.assertAlmostEqual(e["dik_aciklik"], round(203 * math.cos(math.radians(48)), 1))
        self.assertAlmostEqual(e["raf_egim_boyu"], round(245 / math.cos(math.radians(48)), 1))
        self.assertFalse(egimli_raf(245, 30, 203)["sigar"])

    def test_cift_sayisi(self):
        self.assertEqual(cift_sayisi(564), 3)
        self.assertEqual(cift_sayisi(564, "buyuk"), 2)


class DonanimCSV(unittest.TestCase):
    def test_yazilir(self):
        with tempfile.TemporaryDirectory() as kl:
            yol = donanim_csv([("X-D01", "Menteşe", "-", 4, "not")],
                              os.path.join(kl, "d.csv"))
            satirlar = open(yol, encoding="utf-8-sig").read().splitlines()
        self.assertEqual(satirlar[0], "Kod;Donanım;Ölçü;Adet;Not")
        self.assertEqual(satirlar[1], "X-D01;Menteşe;-;4;not")


if __name__ == "__main__":
    unittest.main()
