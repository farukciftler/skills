"""
mobilya.py — levha mobilya tasarım çekirdeği (CAD bağımsız, saf Python).

Malzeme kütüphanesi · Parça/BOM modeli · kenar bandı hesabı · giyotin
optimizasyon (kerf'li) · raf sehimi kontrolü · devrilme (EN 14749) kontrolü.

Bu modülün HİÇBİR ağır bağımlılığı yoktur — build123d/ezdxf kurulu olmasa da
çalışır. Geometri/çizim işleri cizim.py'de, render işleri render.py'de.

Birim sözleşmesi: uzunluk mm, kütle kg, kuvvet N, gerilme N/mm2 (MPa).
Ölçü sözleşmesi: "boy" (L) = DESEN YÖNÜ, "en" (W) = desene dik. Levhada
desen 2800 boyunca akar.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field, asdict
from typing import Iterable, Literal

# ---------------------------------------------------------------------------
# 1. MALZEME KÜTÜPHANESİ
#    Kaynak: EN 312 P2 tablosu (Kronospan MF PB datasheet), Starwood Levha
#    Kullanım Kılavuzu, Yıldız Entegre teknik dokümanlar. Ayrıntı ve kaynak
#    linkleri: references/malzeme-donanim.md
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Malzeme:
    kod: str
    ad: str
    yogunluk: float          # kg/m3  (18 mm nominal)
    e_modul: float           # N/mm2  EN 310 MOE — sehim hesabının girdisi
    mor: float               # N/mm2  EN 310 eğilme dayanımı
    tolerans: float          # ± mm   kalınlık toleransı
    desenli: bool            # True ise lif/desen yönü kilitlenebilir
    levha_en: float = 2100.0     # mm — desene DİK yön
    levha_boy: float = 2800.0    # mm — desen yönü
    kalinliklar: tuple[float, ...] = (8.0, 18.0, 25.0)

    def kg_m2(self, t: float) -> float:
        return self.yogunluk * t / 1000.0

    def levha_alani(self) -> float:
        """m2"""
        return self.levha_en * self.levha_boy / 1e6


MALZEMELER: dict[str, Malzeme] = {
    # Suntalam = melaminli yonga levha (MFC). Mobilya gövdesi = P2 "Süper Fine".
    "suntalam": Malzeme(
        "suntalam", "Suntalam (melaminli yonga levha, EN 312 P2)",
        yogunluk=630, e_modul=1600, mor=11.0, tolerans=0.3, desenli=True,
        kalinliklar=(8.0, 18.0, 25.0),
    ),
    # Su bazlı / yeşil P7 — ıslak alan.
    "suntalam_p7": Malzeme(
        "suntalam_p7", "Su bazlı suntalam (EN 312 P7)",
        yogunluk=680, e_modul=1800, mor=15.0, tolerans=0.3, desenli=True,
        kalinliklar=(18.0,),
    ),
    "mdflam": Malzeme(
        "mdflam", "MDFLAM (melamin kaplı MDF)",
        yogunluk=730, e_modul=1800, mor=14.0, tolerans=0.2, desenli=True,
        kalinliklar=(8.0, 18.0, 25.0),
    ),
    "mdf": Malzeme(
        "mdf", "Ham MDF (lake/boya altı)",
        yogunluk=730, e_modul=1800, mor=14.0, tolerans=0.2, desenli=False,
        levha_en=1830.0, levha_boy=3660.0,
        kalinliklar=(3.0, 6.0, 8.0, 16.0, 18.0, 25.0),
    ),
    # Arkalık. 2500x1300 satılır ama nesting'e 1300x2500 olarak girer.
    "hdf": Malzeme(
        "hdf", "HDF arkalık (duralit)",
        yogunluk=850, e_modul=3000, mor=30.0, tolerans=0.2, desenli=False,
        levha_en=1300.0, levha_boy=2500.0,
        kalinliklar=(3.0, 4.0, 5.0),
    ),
    "kontrplak": Malzeme(
        "kontrplak", "Kontrplak (kayın/huş)",
        yogunluk=700, e_modul=8000, mor=40.0, tolerans=0.5, desenli=True,
        levha_en=1220.0, levha_boy=2440.0,
        kalinliklar=(6.0, 9.0, 12.0, 15.0, 18.0),
    ),
}

# Kenar bandı: kalınlık -> (rulo boyu m, kullanım notu)
BANT_KALINLIK = {
    0.4: "iç/gizli kenarlar, raf alt-üst",
    0.8: "gövde iç kenarları, ekonomik segment",
    1.0: "genel standart — gövde ve kapak",
    2.0: "kapak/çekmece önü, darbeye açık ön kenarlar",
}

# Bant genişliği = panel kalınlığı + 4 mm (freze payı). 18 mm -> 22 mm.
BANT_GENISLIK_PAYI = 4.0


# ---------------------------------------------------------------------------
# 2. PARÇA MODELİ
# ---------------------------------------------------------------------------

Kenar = Literal["L1", "L2", "W1", "W2"]
# L1/L2 = boy (uzun) kenarların ikisi; W1/W2 = en (kısa) kenarların ikisi.


@dataclass
class Parca:
    """Tek bir levha parçası.

    boy/en NET (bitmiş) ölçüdür — yani bantlar yapıştıktan sonraki ölçü.
    Kesim ölçüsü kesim_olcusu() ile bant payı düşülerek hesaplanır.
    """
    kod: str                       # AYK-P01
    ad: str                        # "Yan panel (sol)"
    boy: float                     # mm — desen yönü
    en: float                      # mm
    kalinlik: float                # mm
    malzeme: str = "suntalam"
    adet: int = 1
    desen_kilit: bool = False      # True -> nesting'de döndürülemez
    bant: dict[str, float] = field(default_factory=dict)   # {"L1": 2.0, ...}
    grup: str = ""                 # "gövde" / "kapak" / "raf"
    not_: str = ""

    # -- türetilenler ------------------------------------------------------
    @property
    def mat(self) -> Malzeme:
        return MALZEMELER[self.malzeme]

    def kesim_olcusu(self, esik: float = 1.0) -> tuple[float, float]:
        """Bant payı düşülmüş kesim ölçüsü (boy, en).

        Kural (MEGEP "Mobilya Üretimini Planlama"): parça, banda kaplanacak
        her kenar için bant kalınlığı kadar KÜÇÜK kesilir.
        `esik` altındaki bantlar düşülmez — 0.4 mm iki kenarda 0.8 mm eder,
        bu levhanın kendi ±0.3 mm toleransının içinde kalır.
        """
        b = self.boy - sum(t for k, t in self.bant.items()
                           if k in ("W1", "W2") and t >= esik)
        e = self.en - sum(t for k, t in self.bant.items()
                          if k in ("L1", "L2") and t >= esik)
        return round(b, 1), round(e, 1)

    def bant_metraji(self) -> dict[float, float]:
        """{bant_kalinligi: toplam_metre} — adet dahil."""
        out: dict[float, float] = {}
        for k, t in self.bant.items():
            uzunluk = self.boy if k in ("L1", "L2") else self.en
            out[t] = out.get(t, 0.0) + uzunluk * self.adet / 1000.0
        return out

    def alan_m2(self) -> float:
        return self.boy * self.en * self.adet / 1e6

    def agirlik_kg(self) -> float:
        return self.alan_m2() * self.mat.kg_m2(self.kalinlik)

    def bant_kodu(self) -> str:
        """Kesim listesinde gösterilen bant deseni, ör. '2/2/0.8/0.8'."""
        return "/".join(f"{self.bant.get(k, 0):g}" for k in ("L1", "L2", "W1", "W2"))

    def desen_kodu(self) -> str:
        if not self.mat.desenli or not self.desen_kilit:
            return "—"
        return "L"      # desen boy yönünde akar


# ---------------------------------------------------------------------------
# 3. BOM / KESİM LİSTESİ
# ---------------------------------------------------------------------------

def bom_satirlari(parcalar: Iterable[Parca], esik: float = 1.0) -> list[dict]:
    rows = []
    for p in parcalar:
        kb, ke = p.kesim_olcusu(esik)
        rows.append({
            "Kod": p.kod, "Parça": p.ad, "Grup": p.grup,
            "Net_Boy": f"{p.boy:g}", "Net_En": f"{p.en:g}",
            "Kesim_Boy": f"{kb:g}", "Kesim_En": f"{ke:g}",
            "Kalınlık": f"{p.kalinlik:g}", "Adet": p.adet,
            "Malzeme": p.mat.ad, "Desen": p.desen_kodu(),
            "Bant_L1/L2/W1/W2": p.bant_kodu(),
            "Alan_m2": f"{p.alan_m2():.3f}", "Ağırlık_kg": f"{p.agirlik_kg():.2f}",
            "Not": p.not_,
        })
    return rows


def bom_csv(parcalar: Iterable[Parca], yol: str, esik: float = 1.0) -> str:
    rows = bom_satirlari(parcalar, esik)
    with open(yol, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(rows)
    return yol


def donanim_csv(donanim: Iterable[tuple], yol: str) -> str:
    """Donanım listesi (menteşe, boru, flanş, ray, braket) → CSV.

    Levha BOM'undan AYRI dosyadır: kesim listesi ebatlama tezgâhına,
    donanım listesi satın almaya gider. Satır: (kod, ad, ölçü, adet, not).
    """
    with open(yol, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Kod", "Donanım", "Ölçü", "Adet", "Not"])
        for kod, ad, olcu, adet, notu in donanim:
            w.writerow([kod, ad, olcu, adet, notu])
    return yol


def bant_ozeti(parcalar: Iterable[Parca], fire: float = 0.10,
               kesim_payi_mm: float = 37.5) -> dict[float, dict]:
    """Kenar bandı metrajı.

    kesim_payi_mm: otomatik bantlama makinesinde her banlı kenar için giriş
    (15 mm) + çıkış (20-25 mm) fazlası kesilir. Kısa parçalarda bu, yüzde
    fireden çok daha baskındır — o yüzden sabit mm olarak modellenir.
    """
    ham: dict[float, float] = {}
    kenar_sayisi: dict[float, int] = {}
    for p in parcalar:
        for t, m in p.bant_metraji().items():
            ham[t] = ham.get(t, 0.0) + m
        for k, t in p.bant.items():
            kenar_sayisi[t] = kenar_sayisi.get(t, 0) + p.adet

    out = {}
    for t, m in sorted(ham.items()):
        trim = kenar_sayisi.get(t, 0) * kesim_payi_mm / 1000.0
        toplam = (m + trim) * (1 + fire)
        out[t] = {
            "net_m": round(m, 2),
            "kesim_payi_m": round(trim, 2),
            "fire_pay": fire,
            "siparis_m": round(toplam, 1),
            "genislik_mm": None,   # aşağıda doldurulur
        }
    return out


# ---------------------------------------------------------------------------
# 4. GİYOTİN OPTİMİZASYON (panel testere uyumlu — her kesim baştan başa)
# ---------------------------------------------------------------------------

@dataclass
class Yerlesim:
    kod: str
    x: float
    y: float
    boy: float
    en: float
    dondu: bool


@dataclass
class _Bos:
    x: float
    y: float
    boy: float
    en: float


class Levha:
    """Tek bir levha üzerinde giyotin yerleşim."""

    def __init__(self, boy: float, en: float, kerf: float = 3.5,
                 kenar_trasi: float = 10.0):
        self.boy, self.en = boy, en
        self.kerf, self.tras = kerf, kenar_trasi
        self.bos = [_Bos(kenar_trasi, kenar_trasi,
                         boy - 2 * kenar_trasi, en - 2 * kenar_trasi)]
        self.yerlesim: list[Yerlesim] = []

    def _bol(self, f: _Bos, b: float, e: float, yatay: bool) -> list[_Bos]:
        k = self.kerf
        out = []
        if yatay:
            if f.boy - b - k > 0:
                out.append(_Bos(f.x + b + k, f.y, f.boy - b - k, e))
            if f.en - e - k > 0:
                out.append(_Bos(f.x, f.y + e + k, f.boy, f.en - e - k))
        else:
            if f.en - e - k > 0:
                out.append(_Bos(f.x, f.y + e + k, b, f.en - e - k))
            if f.boy - b - k > 0:
                out.append(_Bos(f.x + b + k, f.y, f.boy - b - k, f.en))
        return out

    def yerlestir(self, kod: str, boy: float, en: float,
                  dondurulebilir: bool) -> bool:
        en_iyi = None
        for i, f in enumerate(self.bos):
            adaylar = [(boy, en, False)]
            if dondurulebilir:
                adaylar.append((en, boy, True))
            for b, e, dn in adaylar:
                if b <= f.boy + 1e-9 and e <= f.en + 1e-9:
                    atik = f.boy * f.en - b * e          # Best-Area-Fit
                    if en_iyi is None or atik < en_iyi[0]:
                        en_iyi = (atik, i, b, e, dn)
        if en_iyi is None:
            return False
        _, i, b, e, dn = en_iyi
        f = self.bos.pop(i)
        self.yerlesim.append(Yerlesim(kod, f.x, f.y, b, e, dn))
        self.bos.extend(self._bol(f, b, e, yatay=(f.boy - b) <= (f.en - e)))
        return True

    @property
    def kullanilan_alan(self) -> float:
        return sum(y.boy * y.en for y in self.yerlesim)

    @property
    def verim(self) -> float:
        return 100.0 * self.kullanilan_alan / (self.boy * self.en)


def optimize(parcalar: Iterable[Parca], malzeme: str, kalinlik: float,
             kerf: float = 3.5, kenar_trasi: float = 10.0,
             esik: float = 1.0) -> list[Levha]:
    """First-Fit-Decreasing, uzun kenara göre. Tek malzeme+kalınlık için."""
    mat = MALZEMELER[malzeme]
    kalemler = []
    for p in parcalar:
        if p.malzeme != malzeme or p.kalinlik != kalinlik:
            continue
        kb, ke = p.kesim_olcusu(esik)
        dondurulebilir = not (mat.desenli and p.desen_kilit)
        for n in range(p.adet):
            kalemler.append((f"{p.kod}#{n+1}", kb, ke, dondurulebilir))

    kalemler.sort(key=lambda k: (max(k[1], k[2]), k[1] * k[2]), reverse=True)

    levhalar: list[Levha] = []
    for kod, b, e, dn in kalemler:
        for lv in levhalar:
            if lv.yerlestir(kod, b, e, dn):
                break
        else:
            lv = Levha(mat.levha_boy, mat.levha_en, kerf, kenar_trasi)
            if not lv.yerlestir(kod, b, e, dn):
                raise ValueError(
                    f"{kod} {b}x{e} levhaya sığmıyor "
                    f"({mat.levha_boy}x{mat.levha_en}, traş {kenar_trasi})")
            levhalar.append(lv)
    return levhalar


def optimize_dogrula(levhalar: list[Levha]) -> list[str]:
    """Çakışma / levha dışına taşma denetimi. Her optimizasyondan sonra ÇALIŞTIR."""
    hatalar = []
    for n, lv in enumerate(levhalar, 1):
        for i, a in enumerate(lv.yerlesim):
            if (a.x < -1e-6 or a.y < -1e-6
                    or a.x + a.boy > lv.boy + 1e-6 or a.y + a.en > lv.en + 1e-6):
                hatalar.append(f"levha{n}: {a.kod} levha dışında")
            for b in lv.yerlesim[i + 1:]:
                if (a.x < b.x + b.boy - 1e-9 and b.x < a.x + a.boy - 1e-9
                        and a.y < b.y + b.en - 1e-9 and b.y < a.y + a.en - 1e-9):
                    hatalar.append(f"levha{n}: ÇAKIŞMA {a.kod} / {b.kod}")
    return hatalar


# ---------------------------------------------------------------------------
# 5. YAPISAL KONTROLLER
# ---------------------------------------------------------------------------

# EN 14749 Tablo 1 — yatay depolama yüzeyi tasarım yükü
EN14749_TASARIM_YUKU = 65.0     # kg/m2
EN14749_STABILITE_YUKU = 32.5   # kg/m2
SEHIM_SINIRI = 240              # CPA Technical Bulletin: L/240 (sünme dahil)
SUNME_CARPANI = 1.5             # uzun vadede +%50


def raf_sehimi(aciklik: float, derinlik: float, kalinlik: float,
               malzeme: str = "suntalam",
               yuk_kg_m2: float = EN14749_TASARIM_YUKU,
               mesnet: Literal["basit", "iki_aciklik"] = "basit") -> dict:
    """Tek açıklıklı, düzgün yayılı yüklü raf sehimi.

    δ = 5wL⁴/(384·E·I),  I = b·h³/12  (b = derinlik, h = kalınlık)
    """
    L = aciklik
    mat = MALZEMELER[malzeme]
    E = mat.e_modul
    I = derinlik * kalinlik ** 3 / 12.0                 # mm4
    # yayılı yük: kg/m2 -> N/mm (raf derinliği boyunca)
    w = yuk_kg_m2 * 9.81 * derinlik / 1e6               # N/mm
    if mesnet == "basit":
        delta = 5 * w * L ** 4 / (384 * E * I)
    else:
        delta = w * L ** 4 / (185 * E * I)
    delta_sunme = delta * SUNME_CARPANI
    oran = L / delta if delta > 0 else float("inf")
    return {
        "aciklik_mm": L,
        "sehim_mm": round(delta, 2),
        "sehim_sunmeli_mm": round(delta_sunme, 2),
        "oran": f"L/{oran:.0f}",
        "limit": f"L/{SEHIM_SINIRI}",
        "uygun": oran >= SEHIM_SINIRI,
        "yuk_kg": round(yuk_kg_m2 * L * derinlik / 1e6, 1),
    }


def max_aciklik(derinlik: float, kalinlik: float, malzeme: str = "suntalam",
                yuk_kg_m2: float = EN14749_TASARIM_YUKU,
                limit: int = SEHIM_SINIRI) -> float:
    """L/limit'i sağlayan en büyük açıklık (mm). L_max = ∛(384·E·I/(5·w·limit))"""
    mat = MALZEMELER[malzeme]
    I = derinlik * kalinlik ** 3 / 12.0
    w = yuk_kg_m2 * 9.81 * derinlik / 1e6
    return (384 * mat.e_modul * I / (5 * w * limit)) ** (1 / 3)


def kusakli_sehim(aciklik: float, derinlik: float, kalinlik: float,
                  kusak_yuksekligi: float = 0.0, kusak_kalinligi: float = None,
                  malzeme: str = "suntalam",
                  yuk_kg_m2: float = EN14749_TASARIM_YUKU,
                  tekil_yuk_kg: float = 0.0) -> dict:
    """ÖN KUŞAKLI (nosing) yatay panelin sehimi — L kesitli kompozit.

    Düz panel yerine ön kenarına düşey bir kuşak eklenince kesit L olur ve
    atalet momenti kat kat artar. Geniş açıklıklı tam genişlik bölmelerin
    (ör. yorgan gözü) tavanını taşımanın standart yolu budur.

    tekil_yuk_kg: açıklığın ORTASINA gelen tekil yük (ör. üstteki dikmenin
    aktardığı yük). Tekil yük yayılı yükten daha zorlayıcıdır.
    """
    mat = MALZEMELER[malzeme]
    E = mat.e_modul
    b, h = derinlik, kalinlik
    kk = kusak_kalinligi if kusak_kalinligi else kalinlik
    kh = kusak_yuksekligi

    # L kesit: üstte yatay panel (flanş), önde düşey kuşak (gövde)
    A1, y1 = b * h, h / 2.0
    A2, y2 = kk * kh, h + kh / 2.0
    A = A1 + A2
    yb = (A1 * y1 + A2 * y2) / A if A else 0.0
    I = (b * h ** 3 / 12.0 + A1 * (yb - y1) ** 2)
    if kh > 0:
        I += (kk * kh ** 3 / 12.0 + A2 * (y2 - yb) ** 2)

    L = aciklik
    w = yuk_kg_m2 * 9.81 * derinlik / 1e6            # N/mm
    d_udl = 5 * w * L ** 4 / (384 * E * I)
    P = tekil_yuk_kg * 9.81
    d_tek = P * L ** 3 / (48 * E * I) if P else 0.0
    delta = d_udl + d_tek
    sunmeli = delta * SUNME_CARPANI
    oran = L / sunmeli if sunmeli > 0 else float("inf")

    I_duz = b * h ** 3 / 12.0
    return {
        "aciklik_mm": L,
        "kusak_mm": kh,
        "I_mm4": round(I),
        "I_duz_mm4": round(I_duz),
        "kazanc": round(I / I_duz, 1) if I_duz else 0,
        "sehim_mm": round(delta, 2),
        "sehim_sunmeli_mm": round(sunmeli, 2),
        "oran": f"L/{oran:.0f}",
        "limit": f"L/{SEHIM_SINIRI}",
        "uygun": oran >= SEHIM_SINIRI,
    }


def devrilme_kontrolu(yukseklik: float, kutle: float,
                      agirlik_merkezi_yuksekligi: float) -> dict:
    """EN 14749 madde 6.2.1 — İKİ parçalı tetik.

    Stabilite şartları YALNIZCA şu ikisi birden sağlanınca uygulanır:
      (a) üst yüzey yüksekliği > 600 mm  VE
      (b) h_ag(m) × kütle(kg) > 6
    """
    carpim = (agirlik_merkezi_yuksekligi / 1000.0) * kutle
    tetik = yukseklik > 600.0 and carpim > 6.0
    return {
        "yukseklik_mm": yukseklik,
        "kutle_kg": round(kutle, 1),
        "h_cg_m_x_kg": round(carpim, 2),
        "stabilite_testi_gerekli": tetik,
        "aciklama": (
            "EN 14749 5.4 stabilite şartları uygulanır — RİJİT METAL duvar "
            "bağlantı braketi verilmeli (madde 3.17: kayış/kablo bağı OLMAZ)."
            if tetik else
            "Stabilite tetiği oluşmadı; yine de devrilme braketi önerilir."),
    }


# ---------------------------------------------------------------------------
# 6. DONANIM GEOMETRİSİ (delik tabloları)
# ---------------------------------------------------------------------------

SISTEM32 = {
    "adim": 32.0,
    "cap": 5.0,
    "derinlik": 13.0,
    "on_kenar_mesafe": 37.0,      # bindirmeli kapak. İç takma kapakta 57.
    "arka_kenar_mesafe": 37.0,
    "ilk_delik": 64.0,            # ATÖLYE PARAMETRESİ — tek standart yok
}

MINIFIX = {
    18.0: {"govde_cap": 15.0, "govde_derinlik": 13.5, "A": 9.0,
           "civata_cap": 8.0, "B": 34.0},
    16.0: {"govde_cap": 15.0, "govde_derinlik": 12.5, "A": 8.0,
           "civata_cap": 8.0, "B": 34.0},
    19.0: {"govde_cap": 15.0, "govde_derinlik": 14.0, "A": 9.5,
           "civata_cap": 8.0, "B": 34.0},
}

KAVELA = {  # (yüz panel derinliği, cumba derinliği) — toplam boy+1 mm olmalı
    (8.0, 30.0): (13.5, 17.5),
    (8.0, 35.0): (14.0, 22.5),
    (8.0, 40.0): (14.0, 27.5),
}

MENTESE = {"cap": 35.0, "derinlik": 12.0, "vida_araligi_blum": 45.0,
           "vida_araligi_hettich": 52.0, "boss_offset": 9.5}

# Devrilir (tip-out) ayakkabılık mekanizması — Häfele Dresscode
DEVRILIR_AYAKKABILIK = {
    1: {"art": "892.14.791", "min_derinlik": 189.0, "montaj_yuksekligi": 265.0,
        "aci_derece": 54.5, "cep_kosegen": 325.0},
    2: {"art": "892.14.792", "min_derinlik": 255.0, "montaj_yuksekligi": 310.0,
        "aci_derece": 50.6, "cep_kosegen": 401.0},
    3: {"art": "892.14.353", "min_derinlik": 310.0, "montaj_yuksekligi": None,
        "aci_derece": None, "cep_kosegen": None},
}
DEVRILIR_GENISLIK_KAYBI = 25.0    # iç genişlikten düşülür
DEVRILIR_ARA_RAF_KALINLIK = 10.0  # 18 DEĞİL — mekanizma 10 mm ister
DEVRILIR_MIN_RAF_YUKSEKLIK = 145.0

# ---------------------------------------------------------------------------
# GARDIROP / ASKI
# Kaynak: standart askı 430-450 mm (fcilondon, furnitureinfashion),
# öne bakan askı için 600 mm gövde / ~550 mm net iç derinlik RAHAT.
# Askının fiziksel sığma sınırı: 450 mm askı + 5 mm/yan pay = 460 mm.
# 500 mm gövdeli (467 mm iç) gardırop piyasada soldan-sağa boruyla satılır;
# kalın palto kapağa sürter, gömlek/ceket/elbise sorun çıkarmaz.
# ---------------------------------------------------------------------------

ASKI = {
    "askilik_genislik": 450.0,     # standart elbise askısı (430-450)
    "askilik_ince": 420.0,         # ince/kadın askısı — sığ gövdede önerilir
    "on_bakan_min_ic": 550.0,      # RAHAT öne bakan askı (net iç derinlik)
    "on_bakan_sikisik": 460.0,     # askı SIĞAR (450 + 2×5 pay), kalın giysi kapağa değer
    "on_bakan_min_govde": 600.0,   # ... karşılığı gövde derinliği
    "yan_bakan_min_govde": 350.0,  # profilden asma için pratik alt sınır
    "boru_cap_yuvarlak": 25.0,     # Ø25 krom boru (Ø19 hafif iş)
    "boru_oval": (30.0, 15.0),     # 30x15 oval küpeşte
    "mesnet_araligi": 800.0,       # ara mesnetsiz maks. boru açıklığı
}

# Askıdaki kıyafetin RAY BOYUNCA kapladığı kalınlık (mm/parça)
ASKI_KALINLIK = {
    "gomlek": 40.0, "ceket": 60.0, "takim": 70.0,
    "palto": 100.0, "elbise": 50.0, "karma": 55.0,
}

# Askıda asılı kıyafetin DÜŞEY boyu (mm) — askı kotu planlaması için
KIYAFET_BOYU = {
    "gomlek": 800.0, "ceket": 1000.0, "pantolon_katli": 800.0,
    "elbise": 1300.0, "palto": 1350.0, "uzun_elbise": 1500.0,
}


def aski_kapasitesi(boru_boyu: float, tip: str = "karma") -> int:
    """Verilen boru uzunluğuna sığan askı adedi."""
    return int(boru_boyu // ASKI_KALINLIK[tip])


def aski_yonu(ic_derinlik: float, ic_genislik: float) -> dict:
    """Bu gövdede askı hangi yönde kurulabilir?

    Öne bakan askı (boru soldan sağa): askının 450 mm genişliği DERİNLİĞE
    yayılır; ≥ 550 mm net iç derinlik RAHAT, 460–550 mm SIKIŞIK (boru
    derinliğin tam ortasına alınır, ince askı önerilir), < 460 mm SIĞMAZ.
    Yandan bakan askı (boru önden arkaya): askının genişliği GENİŞLİĞE
    yayılır; derinlik yalnız kaç kıyafet sığacağını belirler. Yalnız öne
    bakan askı fiziksel olarak sığmadığında kullanılır.

    Dönen sözlükte `boru_y`: soldan-sağa borunun ÖN yüzden ölçülen derinlik
    konumu. Rahat gövdede biraz arkaya (kapak payı), sıkışık gövdede tam
    ortaya — askının iki yanına eşit pay kalsın.
    """
    one = ic_derinlik >= ASKI["on_bakan_sikisik"]
    rahat = ic_derinlik >= ASKI["on_bakan_min_ic"]
    yana = ic_genislik >= ASKI["askilik_genislik"] + 40
    pay = (ic_derinlik - ASKI["askilik_genislik"]) / 2
    return {
        "one_bakan": one,
        "rahat": rahat,
        "yana_bakan": yana,
        "yon": "x" if one else ("y" if yana else None),
        "boru_boyu": ic_genislik if one else ic_derinlik,
        "boru_y": ic_derinlik / 2 + (10.0 if rahat else 0.0),
        "aciklama": (
            "Öne bakan askı — boru soldan sağa, kıyafetler öne bakar."
            if rahat else
            f"Öne bakan askı SIĞAR ama SIKIŞIK: net iç derinlik "
            f"{ic_derinlik:.0f} mm, standart askı "
            f"{ASKI['askilik_genislik']:.0f} mm — askının önüne ve arkasına "
            f"{pay:.0f} mm pay kalıyor. Boru derinliğin tam ortasına. "
            f"Gömlek/ceket/elbise sorun değil; kalın palto omzu kapağa "
            f"sürter — {ASKI['askilik_ince']:.0f} mm ince askı önerilir. "
            f"Rahat kullanım için {ASKI['on_bakan_min_govde']:.0f} mm gövde "
            f"gerekir."
            if one else
            "Öne bakan askı SIĞMAZ (net iç derinlik "
            f"{ic_derinlik:.0f} mm < {ASKI['on_bakan_sikisik']:.0f} mm = "
            f"askı {ASKI['askilik_genislik']:.0f} + pay). "
            "Boru ÖNDEN ARKAYA takılır, kıyafetler profilden asılır."
            if yana else
            "Askı kurulamaz — iç genişlik 490 mm'nin altında."),
    }


# Ayakkabı antropometrisi — tasarım değerleri
AYAKKABI = {
    "kadin": {"boy": 300.0, "cift_genislik": 175.0},
    "karma": {"boy": 320.0, "cift_genislik": 185.0},   # EU 43-45 dahil — VARSAYILAN
    "buyuk": {"boy": 350.0, "cift_genislik": 220.0},
}
RAF_ARALIGI = {"duz": 150.0, "karma": 180.0, "bilekli": 200.0, "bot": 280.0}


def egim_gerekli(raf_derinlik: float, ayakkabi_boy: float = None,
                 tip: str = "karma") -> float:
    """Ayakkabının rafa SIĞMASI için gereken minimum eğim açısı (derece).

    Düz rafta ayakkabı boyu kadar yatay derinlik gerekir. Raf eğilince
    yatay izdüşüm boy·cos(θ)'ya iner. Sığma şartı: boy·cos(θ) <= raf_derinlik.
    """
    L = ayakkabi_boy or AYAKKABI[tip]["boy"]
    if raf_derinlik >= L:
        return 0.0
    return math.degrees(math.acos(raf_derinlik / L))


def egimli_raf(raf_derinlik: float, aci: float, dusey_adim: float,
               ayakkabi_boy: float = None, tip: str = "karma") -> dict:
    """Eğimli raf geometrisi ve kontrolü.

    raf_derinlik : rafın YATAY izdüşümü (mm)
    aci          : eğim açısı (derece), arkaya doğru aşağı
    dusey_adim   : raflar arası DÜŞEY mesafe (mm)

    Paralel eğimli raflarda ayakkabı yüksekliği için kritik olan DİK
    açıklıktır: dik_aciklik = dusey_adim · cos(aci).
    """
    L = ayakkabi_boy or AYAKKABI[tip]["boy"]
    r = math.radians(aci)
    egim_boyu = raf_derinlik / math.cos(r) if aci else raf_derinlik
    return {
        "aci": aci,
        "gereken_aci": round(egim_gerekli(raf_derinlik, L, tip), 1),
        "raf_egim_boyu": round(egim_boyu, 1),      # kesilecek parça derinliği
        "yukselme": round(raf_derinlik * math.tan(r), 1),  # ön kenarın yükselmesi
        "ayakkabi_yatay": round(L * math.cos(r), 1),
        "sigar": L * math.cos(r) <= raf_derinlik + 1e-6,
        "boy_sigar": L <= egim_boyu + 1e-6,
        "dik_aciklik": round(dusey_adim * math.cos(r), 1),
    }


def cift_sayisi(net_genislik: float, tip: str = "karma") -> int:
    """Bir rafa sığan ayakkabı çifti (burun içeri yerleşim)."""
    return int(net_genislik // AYAKKABI[tip]["cift_genislik"])


# ---------------------------------------------------------------------------
# 7. RAPOR
# ---------------------------------------------------------------------------

def ozet_rapor(parcalar: list[Parca], kerf: float = 3.5,
               bant_fire: float = 0.10) -> str:
    sat = []
    sat.append("=" * 74)
    sat.append("MALZEME ÖZETİ")
    sat.append("=" * 74)

    toplam_kg = sum(p.agirlik_kg() for p in parcalar)
    gruplar: dict[tuple[str, float], list[Parca]] = {}
    for p in parcalar:
        gruplar.setdefault((p.malzeme, p.kalinlik), []).append(p)

    toplam_levha = 0
    for (mlz, kal), grup in sorted(gruplar.items()):
        mat = MALZEMELER[mlz]
        levhalar = optimize(grup, mlz, kal, kerf=kerf)
        hatalar = optimize_dogrula(levhalar)
        toplam_levha += len(levhalar)
        alan = sum(p.alan_m2() for p in grup)
        brut = len(levhalar) * mat.levha_alani()
        sat.append(f"\n{mat.ad} — {kal:g} mm")
        sat.append(f"  parça       : {sum(p.adet for p in grup)} adet, "
                   f"{alan:.2f} m2")
        sat.append(f"  levha       : {len(levhalar)} adet "
                   f"({mat.levha_boy:g}x{mat.levha_en:g}), {brut:.2f} m2")
        sat.append(f"  VERİM       : %{100*alan/brut:.1f}  "
                   f"(fire %{100*(brut-alan)/brut:.1f})")
        for i, lv in enumerate(levhalar, 1):
            sat.append(f"    levha {i}: {len(lv.yerlesim):2d} parça, "
                       f"verim %{lv.verim:.1f}")
        if hatalar:
            sat.append("  !! " + "; ".join(hatalar))

    sat.append("\n" + "-" * 74)
    sat.append("KENAR BANDI")
    sat.append("-" * 74)
    for t, d in bant_ozeti(parcalar, fire=bant_fire).items():
        genislik = None
        for p in parcalar:
            if t in p.bant.values():
                genislik = p.kalinlik + BANT_GENISLIK_PAYI
                break
        sat.append(f"  {t:g} mm x {genislik:g} mm : net {d['net_m']:.1f} m + "
                   f"kesim payı {d['kesim_payi_m']:.1f} m + fire "
                   f"%{d['fire_pay']*100:.0f} → SİPARİŞ {d['siparis_m']:.1f} m")

    sat.append("\n" + "-" * 74)
    sat.append(f"TOPLAM: {toplam_levha} levha · {toplam_kg:.1f} kg ürün ağırlığı")
    sat.append("-" * 74)
    return "\n".join(sat)


if __name__ == "__main__":
    # Kendi kendini test — kütüphane doğru mu?
    p = Parca("T01", "test raf", 750, 300, 18, bant={"L1": 2.0, "L2": 0.8})
    # L1/L2 = boy kenarları -> EN ölçüsünü kısaltır. 0.8 mm eşiğin altında,
    # düşülmez; sadece 2.0 mm düşer.
    assert p.kesim_olcusu() == (750.0, 298.0), p.kesim_olcusu()
    assert p.kesim_olcusu(esik=0.5) == (750.0, 297.2), p.kesim_olcusu(esik=0.5)
    s = raf_sehimi(aciklik=750, derinlik=300, kalinlik=18)
    print("750 mm açıklık:", s)
    print("max açıklık   :", round(max_aciklik(300, 18), 0), "mm")
    print(ozet_rapor([Parca("T01", "yan", 1150, 280, 18, adet=2,
                            bant={"W1": 2.0}, desen_kilit=True)]))
