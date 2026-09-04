"""
dolap.py — bölge (zone) tabanlı parametrik dolap üreteci.

Gövde, düşey olarak sıralanmış BÖLGE'lerden kurulur. Her bölge kendi
kapak tipini, raf sayısını ve iç düzenini bilir. Ayakkabılık, sığ
gardırop, TV ünitesi, kitaplık — hepsi aynı kalıptan çıkar.

    from dolap import Dolap, Bolge
    d = Dolap(genislik=600, derinlik=260, yukseklik=1850, kod="AYK-A",
              bolgeler=[Bolge("cizme", 450, kapak="tek"),
                        Bolge("raf", 900, raf=4, kapak="tek"),
                        Bolge("acik", 200)])

Bölge tipleri:
  "raf"      — raflı hacim (kapaklı veya açık)
  "cizme"    — uzun çizme hacmi (raf yok, net yükseklik korunur)
  "acik"     — açık niş (kapak yok)
  "devrilir" — devrilir (tip-out) ayakkabılık kapağı
  "aski"     — askı borusu (sığ gövdede önden arkaya)

Kapak tipleri: None (açık) · "tek" · "cift" · "devrilir"

Sütunlu (yan yana bölmeli) gövde için `gardirop.Gardirop` bu sınıftan
türer. Yan panel, tabla, kapak, baza ve arkalık parça/yerleşim
yardımcıları, rapor iskeleti ve `uret()` ORTAKTIR — bir kural düzeltmesi
tek yerde yapılır.

Bu modül build123d/ezdxf İSTEMEZ (yerleşim tipleri geometri.py'de);
yalnız `uret()` çizim katmanını içe alır.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mobilya import (
    ASKI, aski_kapasitesi, aski_yonu,
    AYAKKABI, egim_gerekli, egimli_raf, DEVRILIR_AYAKKABILIK,
    DEVRILIR_ARA_RAF_KALINLIK, DEVRILIR_GENISLIK_KAYBI, MALZEMELER,
    RAF_ARALIGI, SISTEM32, Parca, bom_csv, donanim_csv, cift_sayisi,
    devrilme_kontrolu, max_aciklik, optimize, optimize_dogrula, ozet_rapor,
    raf_sehimi,
)
from geometri import Boru, Yerlestirme

# Askı bölgesi için gereken NET yükseklik (kıyafet boyu + boru + pay).
# mobilya.KIYAFET_BOYU asılı kıyafetin kendi boyudur; buradaki değer
# üstüne boru kotu (tavandan 55 mm) ve askı kancası payını ekler.
KIYAFET_BOYU_KONTROL = {
    "gomlek": 900.0, "ceket": 1100.0, "karma": 1150.0,
    "elbise": 1400.0, "palto": 1450.0,
}

CIZME_NET_YUKSEKLIK = 400.0     # dik uzun çizme için net iç yükseklik
DERZ = 3.0                      # kapaklar arası / kapak-gövde derzi
RAF_ON_BOSLUK = 12.0            # raf ön kenarı - gövde ön yüzü
RAF_ARKA_BOSLUK = 3.0           # rafın arkalığa en yakın köşesi - arkalık
ARA_ON_BOSLUK = 10.0            # sabit ara tabla ön kenarı - gövde ön yüzü
ARKALIK_TASMA = 16.0            # arkalık kanala girer: her kenardan 8 mm
BANT_KAPAK = {"L1": 2.0, "L2": 2.0, "W1": 2.0, "W2": 2.0}   # 4 kenar 2 mm


@dataclass
class Bolge:
    tip: str                    # "raf"|"cizme"|"acik"|"devrilir"|"aski"|"cekmece"
    yukseklik: float            # bölgenin NET iç yüksekliği (mm)
    raf: int = 0                # ayarlanabilir raf sayısı (eşit dağıtılır)
    raf_kotlari: tuple = ()     # verilirse raflar TAM bu kotlara konur
                                # (bölge tabanından mm) — çizme hacmi gibi
                                # eşit olmayan düzenler için
    kapak: str | None = None    # None | "tek" | "cift" | "devrilir"
    sira: int = 1               # devrilir bölgede ayakkabı sırası
    ayna: bool = False          # kapak yüzeyinde ayna
    kiyafet: str = "karma"      # aski bölgesinde asılacak kıyafet tipi
    alin: float = 0.0           # ÖN ALIN PANELİ yüksekliği (mm).
                                # Üstteki tabladan aşağı iner.
                                # Önden-arkaya boruda ZORUNLU:
                                # borunun ön ucunu kapatır (askı
                                # kayıp düşmez) ve ön flanşa düşey
                                # yüzey verir; tablayı kirişler.
    ayakkabi: bool = True       # False -> bu bölge ayakkabı için değil
                                # (kutu/çanta/kıyafet); ayakkabı
                                # kontrolleri ve sayımı atlanır
    ayakkabi_tipi: str | None = None
                                # "kadin"|"karma"|"buyuk" — bu bölgenin
                                # ayakkabı antropometrisi. None -> dolabın
                                # varsayılanı (Dolap(ayakkabi_tipi=...))
    egim: float = 0.0           # raf eğimi (derece, arkaya doğru aşağı)
                                # 0 = düz. Çizme gözü DAİMA düzdür.
    ad: str = ""
    not_: str = ""


class Dolap:
    """Tek kolonlu gövde: bölgeler düşey sıralanır.

    Alt sınıflar (Gardirop) `_duzen_ve_kontroller`, `_kapasite`,
    `_parcalar`, `_yerlestir`, `_rapor_duzen`, `_rapor_yapisal`,
    `cizim_notlari`, `render_notlari` metotlarını ezer; parça/yerleşim
    yardımcılarını ve `rapor()` iskeletini aynen kullanır.
    """

    def __init__(self, *, genislik, derinlik, yukseklik, bolgeler,
                 tam_kapak=None,
                 baza=80.0, baza_icerlek=50.0,
                 kalinlik=18.0, malzeme="suntalam",
                 arkalik=3.0, ayakkabi_tipi="karma",
                 kod="DLP-01", ad="Dolap", aciklama=""):
        self.G, self.D, self.H = float(genislik), float(derinlik), float(yukseklik)
        self.baza, self.T = float(baza), float(kalinlik)
        # baza_icerlek: bazanın gövde ön yüzünden içeri çekilmesi.
        #   >0            klasik süpürgelik boşluğu
        #    0            gövde ön yüzüyle aynı hiza, tam genişlik
        #   "kapak"/<0    KAPAK yüzeyiyle aynı hiza (baza öne çıkar) —
        #                 kapalıyken kaide ve kapak tek düzlem olur
        if baza_icerlek == "kapak":
            baza_icerlek = -float(kalinlik)
        self.baza_icerlek = float(baza_icerlek)
        self.malzeme, self.ark = malzeme, float(arkalik)
        self.ayk = ayakkabi_tipi
        self.kod, self.ad, self.aciklama = kod, ad, aciklama
        self.bolgeler = list(bolgeler)
        # tam_kapak: "tek"|"cift" -> kapak TÜM gövdeyi kaplar,
        # bölgelerin kendi kapakları yok sayılır (gardırop düzeni).
        self.tam_kapak = tam_kapak
        if tam_kapak:
            for b in self.bolgeler:
                b.kapak = None

        self.uyarilar: list[str] = []
        self.parcalar: list[Parca] = []
        self.yerlesim: list[Yerlestirme] = []
        self.borular: list[Boru] = []
        self.donanim: list[tuple] = []     # (kod, ad, ölçü, adet, not)
        self.detay: list[tuple[str, str]] = []
        self.goz_notlari: list[str] = []
        self.p_alin: dict = {}
        self.p_kapak: dict = {}
        self.cift = 0
        self._hesapla()

    # ---- türetilen ölçüler ----------------------------------------------
    @property
    def ic_genislik(self):
        return self.G - 2 * self.T

    @property
    def ic_derinlik(self):
        return self.D - self.ark - 12.0

    @property
    def govde_yuksekligi(self):
        return self.H - self.baza

    def _ayk(self, b) -> str:
        """Bölgenin ayakkabı antropometrisi (bölge ezmiyorsa dolabınki)."""
        return getattr(b, "ayakkabi_tipi", None) or self.ayk

    def raf_derinligi(self, egim: float = 0.0) -> float:
        """Rafın YATAY izdüşümü (ön ve arka boşluk düşülmüş).

        EĞİMLİ rafta panelin KALINLIĞI da yatayda yer kaplar: raf θ kadar
        eğilince kesitin yataydaki izdüşümü `derinlik·cosθ + T·sinθ`
        olur. İkinci terim atlanırsa raf, hesapta arkalığın önünde biter
        ama GERÇEKTE arka-üst köşesi arkalığı deler — 18 mm panelde 45°'de
        12.7 mm. (Arkadan bakışta her rafın şerit gibi görünmesinin
        sebebi buydu.)

        Yerleşim: raf ön kenarı gövde ön yüzünden RAF_ON_BOSLUK,
        arka-üst köşesi arkalıktan RAF_ARKA_BOSLUK içeride durur.
        """
        return (self.ic_derinlik - RAF_ON_BOSLUK - RAF_ARKA_BOSLUK
                - self.T * math.sin(math.radians(egim)))

    def on_yuzey(self) -> float:
        """En ÖNDEKİ yüzeyin y'si (mm, gövde ön yüzü 0; kapak/baza öne
        taşıyorsa negatif). Dış ölçü ve render ölçüleri buradan başlar."""
        kapakli = bool(self.tam_kapak or any(b.kapak for b in self.bolgeler))
        return min(0.0, self.baza_icerlek, -self.T if kapakli else 0.0)

    def kot_zinciri(self) -> list[float]:
        """Zincir ölçünün kotları (zeminden mm): kaide üstü, bölge
        sınırları ve RAF kotları. Teknik çizim de render ölçüsü de
        AYNI listeyi kullanır — iki belge birbirinden ayrılamaz."""
        z = [0.0, self.baza]
        for c, b in zip(self.kotlar, self.bolgeler):
            z.append(c + b.yukseklik)
            if b.raf_kotlari:
                z += [c + dz for dz in b.raf_kotlari]
            elif b.raf:
                adim = b.yukseklik / (b.raf + 1)
                z += [c + r * adim for r in range(1, b.raf + 1)]
        return sorted(set(round(v, 2) for v in z))

    def yukleme_acikligi(self, b) -> float | None:
        """Eğimli raflı bölgede EN ÜST rafın ön-ÜST köşesi ile bölge
        tavanı arasında kalan ÖN açıklık (mm). Ayakkabı bu açıklıktan
        içeri sokulur; kapanırsa o raf yüklenemez. Düz raflı bölgede None.

        Rafın en yüksek noktası ön kenarın ÜST köşesidir: nominal kot +
        yukselme + T·cosθ. Kalınlık atlanırsa açıklık olduğundan
        büyük görünür (18 mm panelde 48°'de 12 mm)."""
        if not (b.egim and b.raf):
            return None
        e = egimli_raf(self.raf_derinligi(b.egim), b.egim, 200,
                       tip=self._ayk(b))
        tepe = e["yukselme"] + self.T * math.cos(math.radians(b.egim))
        kotlar = (list(b.raf_kotlari) if b.raf_kotlari else
                  [r * b.yukseklik / (b.raf + 1) for r in range(1, b.raf + 1)])
        return b.yukseklik - (max(kotlar) + tepe)

    def _raf_araliklari(self, b) -> list[float]:
        if b.raf_kotlari:
            s = [0.0] + list(b.raf_kotlari) + [b.yukseklik]
            return [u - a for a, u in zip(s, s[1:])]
        if b.raf:
            adim = b.yukseklik / (b.raf + 1)
            return [adim] * (b.raf + 1)
        return []

    # ---- hesap iskeleti --------------------------------------------------
    def _hesapla(self):
        """Düzen + kontroller → parçalar → yerleşim → kapasite → devrilme.
        Alt sınıflar adımları ezer, sırayı değil."""
        self._duzen_ve_kontroller()
        self._parcalar()
        self._yerlestir()
        self._kapasite()
        kutle = sum(p.agirlik_kg() for p in self.parcalar) + self.cift * 0.8
        self.devrilme = devrilme_kontrolu(self.H, kutle, self.H * 0.45)

    def _duzen_ve_kontroller(self):
        n = len(self.bolgeler)
        # Toplam iç yükseklik = gövde - üst/alt tabla - bölge araları
        kullanilabilir = self.govde_yuksekligi - 2 * self.T - (n - 1) * self.T
        istenen = sum(b.yukseklik for b in self.bolgeler)
        self.bolge_farki = kullanilabilir - istenen
        if abs(self.bolge_farki) > 0.5:
            # Farkı en büyük "raf" bölgesine yedir; yoksa hepsine dağıt
            hedef = max((b for b in self.bolgeler if b.tip in ("raf", "acik")),
                        key=lambda b: b.yukseklik, default=None)
            if hedef is not None:
                hedef.yukseklik += self.bolge_farki
            else:
                for b in self.bolgeler:
                    b.yukseklik += self.bolge_farki / n
        if kullanilabilir < 0:
            self.uyarilar.append(
                f"Bölgeler gövdeye sığmıyor: {istenen:.0f} mm isteniyor, "
                f"{kullanilabilir:.0f} mm var.")

        # Bölge taban kotları (baza üstünden itibaren, alt tabla dahil)
        self.kotlar = []
        z = self.baza + self.T
        for b in self.bolgeler:
            self.kotlar.append(z)
            z += b.yukseklik + self.T

        # ---- kontroller
        self.sehim = raf_sehimi(aciklik=self.ic_genislik,
                                derinlik=self.ic_derinlik,
                                kalinlik=self.T, malzeme=self.malzeme)
        self.max_ack = max_aciklik(self.ic_derinlik, self.T, self.malzeme)
        if not self.sehim["uygun"]:
            self.uyarilar.append(
                f"Raf açıklığı {self.ic_genislik:.0f} mm > "
                f"{self.max_ack:.0f} mm limiti (sehim "
                f"{self.sehim['sehim_sunmeli_mm']} mm = {self.sehim['oran']}). "
                f"Orta dikme veya ön kuşak gerekir.")

        for b in self.bolgeler:
            ayk = self._ayk(b)
            if b.tip == "devrilir":
                mek = DEVRILIR_AYAKKABILIK.get(b.sira)
                if mek and self.ic_derinlik < mek["min_derinlik"]:
                    self.uyarilar.append(
                        f"'{b.ad or b.tip}': {b.sira} sıra devrilir mekanizma "
                        f"{mek['min_derinlik']:.0f} mm iç derinlik ister, "
                        f"{self.ic_derinlik:.0f} mm var "
                        f"(Häfele {mek['art']}).")
                if mek and mek["montaj_yuksekligi"] and \
                        b.yukseklik < mek["montaj_yuksekligi"]:
                    self.uyarilar.append(
                        f"'{b.ad or b.tip}': göz {b.yukseklik:.0f} mm, "
                        f"mekanizma {mek['montaj_yuksekligi']:.0f} mm ister.")
            if b.tip == "aski":
                a = aski_yonu(self.ic_derinlik, self.ic_genislik)
                self.aski = a
                if a["yon"] is None:
                    self.uyarilar.append(
                        f"'{b.ad or 'askı'}': {a['aciklama']}")
                elif a["yon"] == "y" and b.alin <= 0:
                    self.uyarilar.append(
                        f"'{b.ad or 'askı'}': önden arkaya boruda ÖN ALIN "
                        f"PANELİ yok — borunun ön ucu açık, askılar kayıp "
                        f"düşebilir. Bolge(..., alin=150) ekleyin.")
                if a["yon"] == "y":
                    self.uyarilar.append(
                        f"'{b.ad or 'askı'}': {a['aciklama']} "
                        f"Boru {a['boru_boyu']:.0f} mm → yalnız "
                        f"~{aski_kapasitesi(a['boru_boyu'], b.kiyafet)} askı "
                        f"sığar. Öne bakan askı için gövde "
                        f"{ASKI['on_bakan_min_govde']:.0f} mm olmalı.")
                gerek = KIYAFET_BOYU_KONTROL.get(b.kiyafet, 1000.0)
                if b.yukseklik < gerek:
                    self.uyarilar.append(
                        f"'{b.ad or 'askı'}': net {b.yukseklik:.0f} mm — "
                        f"{b.kiyafet} için {gerek:.0f} mm gerekir.")
            if b.tip == "cizme" and b.yukseklik < CIZME_NET_YUKSEKLIK:
                self.uyarilar.append(
                    f"'{b.ad or 'çizme'}': net {b.yukseklik:.0f} mm — dik uzun "
                    f"çizme {CIZME_NET_YUKSEKLIK:.0f} mm ister.")
            if b.tip in ("raf", "acik") and b.raf and b.ayakkabi:
                rd = self.raf_derinligi(b.egim)
                g = egim_gerekli(rd, tip=ayk)
                if b.egim + 1e-6 < g:
                    self.uyarilar.append(
                        f"'{b.ad or b.tip}': {rd:.0f} mm raf derinliğinde "
                        f"{AYAKKABI[ayk]['boy']:.0f} mm ayakkabı için en az "
                        f"{g:.0f}° eğim gerekir; şu an {b.egim:.0f}°. Düz rafta "
                        f"ayakkabı {AYAKKABI[ayk]['boy'] - rd:.0f} mm taşar, "
                        f"kapak kapanmaz.")
                elif b.egim:
                    # Eğimli rafın ÖN kenarı arka kenardan `yukselme` kadar
                    # yukarıdadır. En üstteki rafın ön kenarı bölge tavanını
                    # (üstündeki sabit tablayı) DELMEMELİDİR.
                    ee = egimli_raf(rd, b.egim, 200, tip=ayk)
                    kotlar = (list(b.raf_kotlari) if b.raf_kotlari else
                              [r * b.yukseklik / (b.raf + 1)
                               for r in range(1, b.raf + 1)])
                    for dz in kotlar:
                        on = dz + ee["yukselme"]
                        if on > b.yukseklik + 1e-6:
                            self.uyarilar.append(
                                f"'{b.ad or b.tip}': {dz:.0f} mm kotundaki "
                                f"eğimli rafın ÖN kenarı {on:.0f} mm'ye "
                                f"çıkıyor, bölge tavanı {b.yukseklik:.0f} mm "
                                f"— üstteki sabit tablayı {on - b.yukseklik:.0f} "
                                f"mm deliyor. En üst raf kotu en fazla "
                                f"{b.yukseklik - ee['yukselme']:.0f} mm olabilir.")
                    # İKİ EĞİMLİ RAF ARASINDAKİ gözler: dik açıklık
                    # ayakkabı yüksekliğini karşılamalı. En alttaki göz
                    # (tabanı düz gövde tablası) ve en üstteki göz (tavanı
                    # düz tabla) ayrı değerlendirilir — onlar _goz_kapasitesi
                    # içinde gerekçesiyle raporlanır.
                    ara = self._raf_araliklari(b)[1:-1]
                    ay = [h for h in ara if h < CIZME_NET_YUKSEKLIK]
                    if ay:
                        e = egimli_raf(rd, b.egim, min(ay), tip=ayk)
                        if e["dik_aciklik"] < 120:
                            self.uyarilar.append(
                                f"'{b.ad or b.tip}': eğimli raflar arası dik "
                                f"açıklık {e['dik_aciklik']:.0f} mm — 120 mm "
                                f"altı, ayakkabı üstteki rafa değer.")
                    # En üst rafın YÜKLEME açıklığı: rafın ön kenarı ile
                    # bölge tavanı arasından ayakkabı sokulur.
                    ya = self.yukleme_acikligi(b)
                    if (ya is not None and 0 <= ya
                            < RAF_ARALIGI["duz"] - 1e-6):
                        self.uyarilar.append(
                            f"'{b.ad or b.tip}': en üst eğimli rafın ön "
                            f"kenarı ile tavan arası {ya:.0f} mm — ayakkabı "
                            f"bu açıklıktan sokulamaz "
                            f"({RAF_ARALIGI['duz']:.0f} mm gerekir). O raf "
                            f"kotunu en az {RAF_ARALIGI['duz'] - ya:.0f} mm "
                            f"aşağı al veya rafı kaldır.")
            if (b.tip == "raf" and b.raf and b.ayakkabi
                    and not b.raf_kotlari and not b.egim):
                ara = b.yukseklik / (b.raf + 1)
                if ara < RAF_ARALIGI["karma"]:
                    self.uyarilar.append(
                        f"'{b.ad or 'raf'}': raf aralığı {ara:.0f} mm < "
                        f"{RAF_ARALIGI['karma']:.0f} mm — karma ev "
                        f"ayakkabısı sığmaz.")

    def _goz_kapasitesi(self, b, cm: int) -> int:
        """Bir bölgedeki gözleri TEK TEK değerlendirir.

        Sayılmayan gözler `self.goz_notlari`'na gerekçesiyle yazılır —
        kapasite şişirmek en pahalı yalandır.

          • EN ALT göz: tabanı DÜZ gövde tablasıdır. Eğimli raflı bölgede
            bile ayakkabı orada YATIK duramaz; net iç derinlik ayakkabı
            boyundan kısaysa o göz ayakkabı gözü değildir.
          • EN ÜST göz (eğimli): üstteki rafın ön kenarı ile tavan
            arasındaki ÖN açıklıktan ayakkabı sokulur. Açıklık düz raf
            aralığından (RAF_ARALIGI["duz"]) küçükse göz yüklenemez.
          • Çizme hacmi (400 mm+) yalnız tabanı DÜZ olan gözde anlamlıdır;
            eğimli rafın üstünde çizme dik duramaz.
        """
        boy = AYAKKABI[self._ayk(b)]["boy"]
        sinirlar = [0.0] + list(b.raf_kotlari) + [b.yukseklik]
        goz = list(zip(sinirlar, sinirlar[1:]))
        yuk_ack = self.yukleme_acikligi(b)
        ad = b.ad or b.tip
        c = 0
        for i, (a, ust) in enumerate(goz):
            h = ust - a
            en_alt, en_ust = (i == 0), (i == len(goz) - 1)
            duz_taban = en_alt or not b.egim
            if duz_taban and self.ic_derinlik < boy - 1e-6 and b.egim:
                self.goz_notlari.append(
                    f"{ad} · {i+1}. göz (net {h:.0f} mm): tabanı DÜZ, iç "
                    f"derinlik {self.ic_derinlik:.0f} mm < {boy:.0f} mm "
                    f"ayakkabı boyu — ayakkabı gözü DEĞİL, sayılmadı.")
                continue
            if duz_taban and h >= CIZME_NET_YUKSEKLIK:
                c += int(self.ic_genislik // 200)              # dik çizme
                continue
            if b.egim and en_ust and yuk_ack is not None \
                    and yuk_ack < RAF_ARALIGI["duz"] - 1e-6:
                self.goz_notlari.append(
                    f"{ad} · en üst göz (net {h:.0f} mm): rafın ön kenarı "
                    f"ile tavan arası {yuk_ack:.0f} mm — ayakkabı "
                    f"sokulamaz ({RAF_ARALIGI['duz']:.0f} mm gerekir), "
                    f"sayılmadı.")
                continue
            if h * math.cos(math.radians(b.egim)) >= 120:
                c += cm
            else:
                self.goz_notlari.append(
                    f"{ad} · {i+1}. göz (net {h:.0f} mm): dik açıklık "
                    f"{h * math.cos(math.radians(b.egim)):.0f} mm < 120 mm — "
                    f"ayakkabı gözü değil, sayılmadı.")
        return c

    def _kapasite(self):
        self.cift = 0
        self.detay = []
        self.goz_notlari = []
        for b in self.bolgeler:
            ayk = self._ayk(b)
            if b.tip == "devrilir":
                net = self.ic_genislik - DEVRILIR_GENISLIK_KAYBI
                c = cift_sayisi(net, ayk) * b.sira
            elif b.tip == "cizme":
                c = int(self.ic_genislik // 200)      # çizme çifti ~200 mm
                self.detay.append((b.ad or "çizme", f"{c} çift uzun çizme"))
                self.cift += c
                continue
            elif b.tip == "aski":
                a = self.aski
                n = aski_kapasitesi(a["boru_boyu"], b.kiyafet) if a["yon"] else 0
                self.detay.append((b.ad or "askı", f"{n} askı ({b.kiyafet})"))
                continue
            elif b.tip in ("raf", "acik"):
                if not b.ayakkabi:
                    n = b.raf + 1
                    self.detay.append(
                        (b.ad or b.tip, f"{n} göz (kutu/çanta)"))
                    continue
                cm = cift_sayisi(self.ic_genislik, ayk)
                if b.raf_kotlari:
                    c = self._goz_kapasitesi(b, cm)
                else:
                    c = cm * (b.raf + 1)
            else:
                c = 0
            self.detay.append((b.ad or b.tip, f"{c} çift"))
            self.cift += c

    # ---- ORTAK parça yardımcıları (Dolap + Gardirop) ---------------------
    def _kod_uretici(self):
        """Sıralı parça kodu: <KOD>-P01, -P02, ..."""
        sayac = [0]

        def kod():
            sayac[0] += 1
            return f"{self.kod}-P{sayac[0]:02d}"
        return kod

    @staticmethod
    def _kanat_genisligi(toplam: float, adet: int) -> float:
        """Tam genişlik kapakta kanat eni: iki kenar derzi, çift kanatta
        bir de orta derz düşülür."""
        return (toplam - 2 * DERZ - (DERZ if adet == 2 else 0)) / adet

    @staticmethod
    def _mentese_adedi(govde_yuksekligi: float) -> int:
        """Kanat başına Ø35 gizli menteşe: 1600 mm üstü gövdede 4, altında 3."""
        return 4 if govde_yuksekligi > 1600 else 3

    def _parca_yan(self, kod, ad="Yan panel", boy=None, adet=2,
                   bant=None, not_=None) -> str:
        k = kod()
        self.parcalar.append(Parca(
            k, ad, self.govde_yuksekligi if boy is None else boy, self.D,
            self.T, self.malzeme, adet=adet, desen_kilit=True, grup="gövde",
            bant=dict(bant) if bant else {"W1": 2.0},
            not_=("ön kenar 2 mm bant · desen DİKEY · 32'lik delik sırası "
                  "ön kenardan 37 mm") if not_ is None else not_))
        return k

    def _parca_tabla(self, kod, ad, boy=None, en=None, adet=1,
                     not_="") -> str:
        """Üst/alt tabla ve sabit ara tabla — ön kenarı 2 mm bantlı."""
        k = kod()
        self.parcalar.append(Parca(
            k, ad, self.ic_genislik if boy is None else boy,
            self.D if en is None else en, self.T, self.malzeme, adet=adet,
            grup="gövde", bant={"W1": 2.0}, not_=not_))
        return k

    def _parca_kapak(self, kod, ad, boy, adet, not_, gen=None,
                     toplam=None) -> str:
        """Menteşeli kapak kanadı: 4 kenar 2 mm bant, desen dikey kilitli."""
        k = kod()
        if gen is None:
            gen = self._kanat_genisligi(self.G if toplam is None else toplam,
                                        adet)
        self.parcalar.append(Parca(
            k, ad, boy, gen, self.T, self.malzeme, adet=adet,
            desen_kilit=True, grup="kapak", bant=dict(BANT_KAPAK), not_=not_))
        return k

    def _parca_baza(self, kod):
        """Baza ön + baza yan. `baza_icerlek <= 0` ise kaide gövde ön yüzü
        (veya kapak yüzeyi) ile aynı hizada, tam genişliktedir."""
        if self.baza <= 0:
            self.p_baza_on = self.p_baza_yan = None
            return
        G, D, T, M = self.G, self.D, self.T, self.malzeme
        hizali = self.baza_icerlek <= 0.001
        self.p_baza_on = kod()
        self.parcalar.append(Parca(
            self.p_baza_on, "Baza ön", G if hizali else self.ic_genislik,
            self.baza, T, M, adet=1, grup="gövde", desen_kilit=hizali,
            bant={"L1": 2.0},
            not_=(("KAPAK yüzeyiyle aynı hizada, tam "
                   f"{G:.0f} mm genişlik — kapalıyken kaide "
                   "ve kapaklar tek düzlem"
                   if self.baza_icerlek < -0.001 else
                   "gövde ön yüzüyle aynı hiza, tam genişlik")
                  if hizali else
                  f"ön yüzden {self.baza_icerlek:.0f} mm içeri "
                  f"— süpürgelik payı")))
        self.p_baza_yan = kod()
        self.parcalar.append(Parca(
            self.p_baza_yan, "Baza yan",
            (D - self.baza_icerlek - T) if hizali else (D - 70),
            self.baza, T, M, adet=2, grup="gövde",
            bant={"W1": 2.0} if hizali else {},
            not_="ön kenar 2 mm bantlı (görünür)" if hizali else ""))

    def _parca_arkalik(self, kod, not_, ad="Arkalık", boy=None, en=None,
                       adet=1) -> str:
        """HDF arkalık; kanala girdiği için her kenardan 8 mm büyük."""
        k = kod()
        self.parcalar.append(Parca(
            k, ad,
            (self.govde_yuksekligi - 2 * self.T + ARKALIK_TASMA)
            if boy is None else boy,
            (self.ic_genislik + ARKALIK_TASMA) if en is None else en,
            self.ark, "hdf", adet=adet, grup="gövde", not_=not_))
        return k

    # ---- ORTAK yerleşim yardımcıları -------------------------------------
    def _yerlestir_govde_kutusu(self, ust=True):
        """İki yan panel + alt tabla (+ üst tabla)."""
        T, G, b0, gy = self.T, self.G, self.baza, self.govde_yuksekligi
        Y = self.yerlesim
        Y.append(Yerlestirme(self.p_yan, (0, 0, b0), "x", "z"))
        Y.append(Yerlestirme(self.p_yan, (G - T, 0, b0), "x", "z"))
        Y.append(Yerlestirme(self.p_alt, (T, 0, b0), "z", "x"))
        if ust:
            Y.append(Yerlestirme(self.p_ust, (T, 0, b0 + gy - T), "z", "x"))

    def _yerlestir_kanatlar(self, kod, adet, z, renk="#E8DCC8"):
        """Tam genişlik kapak kanatları: DERZ'den başlar, çift kanatta
        ortada bir DERZ, kapak yüzeyi gövdenin -T önünde."""
        T, G = self.T, self.G
        if adet == 2:
            gen = (G - 3 * DERZ) / 2
            for s in range(2):
                self.yerlesim.append(Yerlestirme(
                    kod, (DERZ + s * (gen + DERZ), -T, z), "y", "z",
                    renk=renk))
        else:
            self.yerlesim.append(Yerlestirme(kod, (DERZ, -T, z), "y", "z",
                                             renk=renk))

    def _yerlestir_baza(self):
        if self.baza <= 0:
            return
        T, G = self.T, self.G
        Y = self.yerlesim
        ic = self.baza_icerlek
        if ic <= 0.001:
            # Tam genişlik kaide. ic<0 ise baza kapak yüzeyine kadar
            # öne taşınır; yan bazalar gövde yanlarının tam altındadır.
            Y.append(Yerlestirme(self.p_baza_on, (0, ic, 0), "y", "x"))
            Y.append(Yerlestirme(self.p_baza_yan, (0, ic + T, 0), "x", "y"))
            Y.append(Yerlestirme(self.p_baza_yan, (G - T, ic + T, 0),
                                 "x", "y"))
        else:
            Y.append(Yerlestirme(self.p_baza_on, (T, ic, 0), "y", "x"))
            Y.append(Yerlestirme(self.p_baza_yan, (T, ic, 0), "x", "y"))
            Y.append(Yerlestirme(self.p_baza_yan, (G - 2 * T, ic, 0),
                                 "x", "y"))

    def _yerlestir_arkalik(self, kod=None, x=None, z=None):
        """Arkalık kanal içinde: arka kenardan 12 mm, kenarlardan 8 mm taşar."""
        T, D, b0 = self.T, self.D, self.baza
        self.yerlesim.append(Yerlestirme(
            kod or self.p_ark,
            (T - 8 if x is None else x, D - 12 - self.ark,
             b0 + T - 8 if z is None else z),
            "y", "z", renk="#8B7355"))

    # ---- parça listesi ---------------------------------------------------
    def _parcalar(self):
        T, G, D, M = self.T, self.G, self.D, self.malzeme
        gy = self.govde_yuksekligi
        P = self.parcalar
        kod = self._kod_uretici()

        self.p_yan = self._parca_yan(kod)
        self.p_ust = self._parca_tabla(kod, "Üst tabla")
        self.p_alt = self._parca_tabla(kod, "Alt tabla")

        ara = len(self.bolgeler) - 1
        self.p_ara = None
        if ara > 0:
            # Derinlik ARKALIĞIN ÖN YÜZÜNDE biter: ön boşluk + derinlik =
            # iç derinlik. D-20 verilirse tabla 3 mm HDF arkalığı delip
            # arkasına 2 mm taşar — arkadan bakışta şerit olarak görünür.
            self.p_ara = self._parca_tabla(
                kod, "Sabit ara tabla", en=self.ic_derinlik - ARA_ON_BOSLUK,
                adet=ara,
                not_="bölge ayırıcı · gövdeyi kareler · arka kenar arkalığa "
                     "dayanır")

        # Bölge içi ayarlanabilir raflar (hepsi aynı ölçü -> tek kalem)
        for b in self.bolgeler:
            if b.raf_kotlari:
                b.raf = len(b.raf_kotlari)
        # Eğim gruplarına göre ayrı raf kalemi (derinlikleri farklı)
        self.p_raf = {}
        gruplar = {}
        for b in self.bolgeler:
            if b.raf:
                gruplar[round(b.egim, 1)] = gruplar.get(round(b.egim, 1), 0) + b.raf
        for egim, adet in sorted(gruplar.items()):
            rd = self.raf_derinligi(egim)
            e = egimli_raf(rd, egim, 200, tip=self.ayk)
            k = kod()
            self.p_raf[egim] = k
            P.append(Parca(k, "Ayarlanabilir raf"
                              + (f" ({egim:g}° eğimli)" if egim else " (düz)"),
                           self.ic_genislik - 2.0, e["raf_egim_boyu"], T, M,
                           adet=adet, grup="raf", bant={"W1": 2.0},
                           not_=("Ø5 pim üzerine · 32'lik sistemde ayarlanır"
                                 if not egim else
                                 f"{egim:g}° arkaya eğimli — ÖN pim sırası arka "
                                 f"sıradan {e['yukselme']:.0f} mm YUKARIDA. "
                                 f"Ayakkabı arkalığa yaslanır, öne kaymaz. "
                                 f"Parça derinliği {e['raf_egim_boyu']:.0f} mm "
                                 f"(eğim boyu, yatay izdüşüm {rd:.0f} mm)")))

        # Kapaklar — bölge bölge
        self.p_kapak = {}
        self.p_mek = {}
        for n, b in enumerate(self.bolgeler):
            if not b.kapak:
                continue
            if b.kapak == "devrilir":
                k = self._parca_kapak(
                    kod, f"Devrilir kapak ({b.ad or n+1})",
                    b.yukseklik + T - DERZ, 1,
                    "4 kenar 2 mm bant · alt derz min 15 mm")
                self.p_kapak[n] = (k, 1)
                ar = kod()
                self.p_mek[n] = ar
                P.append(Parca(ar, f"Mekanizma ara rafı ({b.ad or n+1})",
                               self.ic_genislik - 33.0,
                               self.ic_derinlik - 25,
                               DEVRILIR_ARA_RAF_KALINLIK, M, adet=b.sira,
                               grup="mekanizma", bant={"W1": 0.8},
                               not_=f"KALINLIK {DEVRILIR_ARA_RAF_KALINLIK:g} mm "
                                    f"— mekanizma şartı, 18 mm DEĞİL"))
            else:
                adet = 2 if b.kapak == "cift" else 1
                k = self._parca_kapak(
                    kod, f"Kapak ({b.ad or n+1})" + (" — AYNALI" if b.ayna else ""),
                    b.yukseklik + T - DERZ, adet,
                    "4 kenar 2 mm bant · Ø35 menteşe kabı, kenardan 22 mm eksen"
                    + (" · ön yüz ayna, güvenlik filmli" if b.ayna else ""))
                self.p_kapak[n] = (k, adet)

        # Ön alın paneli (askı bölgesi) — üstteki tabladan aşağı iner
        self.p_alin = {}
        for n, b in enumerate(self.bolgeler):
            if b.tip == "aski" and b.alin > 0:
                k = kod()
                self.p_alin[n] = k
                P.append(Parca(k, f"Ön alın paneli ({b.ad or n+1})",
                               self.ic_genislik, b.alin, T, M, adet=1,
                               desen_kilit=True, grup="gövde",
                               bant={"L1": 2.0},
                               not_="Üstteki sabit tablanın ALTINA, ÖN kenara "
                                    "monte. Alt kenarı 2 mm bantlı (görünür). "
                                    "Askı borusunun ÖN flanşı bu panelin ARKA "
                                    "yüzüne vidalanır; borunun ön ucunu "
                                    "kapatır. Tablayı kirişler."))

        # Askı boruları (levha değil — donanım)
        self.borular = []
        self.donanim = []
        for n, b in enumerate(self.bolgeler):
            if b.tip != "aski":
                continue
            a = self.aski
            if not a["yon"]:
                continue
            cap = ASKI["boru_cap_yuvarlak"]
            z = self.kotlar[n] + b.yukseklik - 55.0     # tavandan 55 mm aşağı
            if a["yon"] == "y":
                on = T + 2.0 if n in self.p_alin else 15.0
                boy = self.ic_derinlik - on - 15.0
                self.borular.append(Boru(
                    f"{self.kod}-D01", "Askı borusu Ø25 (önden arkaya)",
                    cap, boy, (G / 2, on, z), "y"))
            else:
                boy = self.ic_genislik
                self.borular.append(Boru(
                    f"{self.kod}-D01", "Askı borusu Ø25 (soldan sağa)",
                    cap, boy, (T, a["boru_y"], z), "x"))
            self.donanim += [
                (f"{self.kod}-D01", f"Askı borusu Ø{cap:g} krom",
                 f"{boy:.0f} mm", 1,
                 "boy kesilir; uçlar çapaksız" if a["yon"] == "y" else ""),
                (f"{self.kod}-D02", "Askı borusu flanşı Ø25", "-", 2,
                 ("ön flanş ALIN PANELİNİN arka yüzüne, arka flanş sabit "
                  "tablanın alt yüzüne")
                 if a["yon"] == "y" and self.p_alin
                 else ("üstteki sabit tablanın ALT yüzüne vidalanır"
                       if a["yon"] == "y" else "yan panellere vidalanır")),
            ]

        # Tam boy kapak (gardırop düzeni)
        self.p_tam_kapak = None
        if self.tam_kapak:
            adet = 2 if self.tam_kapak == "cift" else 1
            m = self._mentese_adedi(gy)
            k = self._parca_kapak(
                kod, f"Tam boy kapak ({adet} kanat)", gy - 2 * DERZ, adet,
                f"4 kenar 2 mm bant · desen DİKEY · {gy - 2*DERZ:.0f} mm boy "
                f"→ kanat başına {m} adet Ø35 menteşe")
            self.p_tam_kapak = (k, adet)
            self.donanim.append(
                (f"{self.kod}-D03", "Gizli menteşe Ø35 (yavaş kapanan)", "-",
                 adet * m, "kap kenardan 22 mm eksen · Blum vida aralığı 45 mm"))

        self._parca_baza(kod)

        self.p_ark = self._parca_arkalik(
            kod, "4 mm kanal içine, 8 mm derin, arka kenardan 12 mm · "
                 "HAVALANDIRMA delikleri Ø30, bölge başına 4 adet")

    # ---- 3B yerleştirme --------------------------------------------------
    def _yerlestir(self):
        T, G, D = self.T, self.G, self.D
        b0 = self.baza
        Y = self.yerlesim

        self._yerlestir_govde_kutusu()

        # Sabit ara tablalar — bölge sınırlarında
        for n in range(len(self.bolgeler) - 1):
            z = self.kotlar[n] + self.bolgeler[n].yukseklik
            Y.append(Yerlestirme(self.p_ara, (T, ARA_ON_BOSLUK, z),
                                 "z", "x"))

        # Ayarlanabilir raflar
        for n, b in enumerate(self.bolgeler):
            if not b.raf:
                continue
            kod_raf = self.p_raf[round(b.egim, 1)]
            e = egimli_raf(self.raf_derinligi(b.egim), b.egim, 200,
                           tip=self._ayk(b))
            kaldir = e["yukselme"] if b.egim else 0.0   # arka kenar nominal kotta
            if b.raf_kotlari:
                kotlar = list(b.raf_kotlari)
            else:
                adim = b.yukseklik / (b.raf + 1)
                kotlar = [r * adim for r in range(1, b.raf + 1)]
            for dz in kotlar:
                Y.append(Yerlestirme(
                    kod_raf,
                    (T + 1, RAF_ON_BOSLUK, self.kotlar[n] + dz + kaldir),
                    "z", "x", donus_x=-b.egim, renk="#D8C4A0"))

        # Kapaklar
        for n, b in enumerate(self.bolgeler):
            if n not in self.p_kapak:
                continue
            k, adet = self.p_kapak[n]
            z = self.kotlar[n] - T + DERZ / 2
            self._yerlestir_kanatlar(k, adet, z,
                                     renk="#C9D4D8" if b.ayna else "#E8DCC8")

            if b.kapak == "devrilir" and n in self.p_mek:
                kh = b.yukseklik
                for sr in range(b.sira):
                    Y.append(Yerlestirme(
                        self.p_mek[n],
                        (T + 16.5, 25,
                         self.kotlar[n] + 45 + sr * (kh - 110) / max(b.sira, 1)),
                        "z", "x", renk="#B0A090"))

        # Ön alın panelleri
        for n, k in self.p_alin.items():
            b = self.bolgeler[n]
            ust = self.kotlar[n] + b.yukseklik
            Y.append(Yerlestirme(k, (T, 0.0, ust - b.alin), "y", "x",
                                 renk="#D8C4A0"))

        # Tam boy kapak (gardırop düzeni) — gövdenin tamamını kaplar
        if self.p_tam_kapak:
            k, adet = self.p_tam_kapak
            self._yerlestir_kanatlar(k, adet, b0 + DERZ)

        self._yerlestir_baza()
        self._yerlestir_arkalik()

    # ---- çizim / render açıklamaları -------------------------------------
    def cizim_notlari(self) -> list[dict]:
        """Kesit görünüşüne konacak atıf okları.

        Koordinatlar KESİT düzleminin model sistemindedir:
        y = dünya Y (derinlik), z = dünya Z (yükseklik).
        """
        n = []

        # Eğimli raf + çizme gözü atıfları
        for i, b in enumerate(self.bolgeler):
            araliklar = self._raf_araliklari(b)
            if not araliklar:
                continue
            ayk = self._ayk(b)
            rd = self.raf_derinligi(b.egim)
            e = egimli_raf(rd, b.egim, 200, tip=ayk) if b.egim else None
            # Komşularından belirgin yüksek göz = bot / yüksek ayakkabı gözü
            sirali = sorted(araliklar)
            ortanca = sirali[len(sirali) // 2] if sirali else 0.0
            yuksek = max(araliklar) if araliklar else 0.0
            yuksek_esik = (yuksek if yuksek >= ortanca * 1.25
                           and len(araliklar) > 1 else None)
            alt = 0.0
            cizme_yazildi = False
            egim_yazildi = False
            yuksek_yazildi = False
            for j, h in enumerate(araliklar):
                ust = alt + h
                if (yuksek_esik and abs(h - yuksek_esik) < 1e-6
                        and not yuksek_yazildi
                        and (h < CIZME_NET_YUKSEKLIK
                             or (b.egim and j > 0))):
                    n.append({
                        "metin": f"YÜKSEK GÖZ {h:.0f} mm — bot ve kısa çizme "
                                 f"(net raf {ortanca:.0f} mm)",
                        "y": rd * 0.55, "z": self.kotlar[i] + alt + h / 2,
                        "dx": 26.0, "dy": -16.0})
                    yuksek_yazildi = True
                elif (h >= CIZME_NET_YUKSEKLIK and not cizme_yazildi
                        and (j == 0 or not b.egim)):
                    n.append({
                        "metin": f"ÇİZME GÖZÜ {h:.0f} mm · RAF DÜZ",
                        "y": rd * 0.55, "z": self.kotlar[i] + alt + h / 2,
                        "dx": 26.0, "dy": -16.0})
                    cizme_yazildi = True
                elif (j == 0 and b.egim and b.ayakkabi
                        and self.ic_derinlik
                        < AYAKKABI[ayk]["boy"] - 1e-6):
                    n.append({
                        "metin": f"ALT SLOT {h:.0f} mm · TABAN DÜZ — "
                                 f"iç derinlik {self.ic_derinlik:.0f} mm, "
                                 f"{AYAKKABI[ayk]['boy']:.0f} mm "
                                 f"ayakkabı SIĞMAZ (terlik/bakım gereci)",
                        "y": rd * 0.55, "z": self.kotlar[i] + alt + h / 2,
                        "dx": 26.0, "dy": -16.0})
                elif e and not egim_yazildi and j > 0:
                    n.append({
                        "metin": f"{b.egim:g}° EĞİMLİ RAF · parça derinliği "
                                 f"{e['raf_egim_boyu']:.0f} mm · ön pim sırası "
                                 f"arkadan {e['yukselme']:.0f} mm YUKARIDA",
                        "y": rd * 0.5,
                        "z": self.kotlar[i] + alt + e["yukselme"] * 0.5,
                        "dx": 26.0, "dy": 8.0})
                    egim_yazildi = True
                alt = ust

        for i, b in enumerate(self.bolgeler):
            if b.tip != "aski":
                continue
            for br in self.borular:
                z = br.konum[2]
                y = br.konum[1] + (br.boy / 2 if br.eksen == "y" else 0)
                n.append({
                    "metin": f"Ø{br.cap:g} ASKI BORUSU  L={br.boy:.0f}",
                    "y": y, "z": z, "dx": 26.0, "dy": 10.0})
            if i in self.p_alin:
                ust = self.kotlar[i] + b.yukseklik
                n.append({
                    "metin": f"ÖN ALIN PANELİ {b.alin:.0f} mm "
                             f"(ön flanş buraya)",
                    "y": self.T / 2, "z": ust - b.alin / 2,
                    "dx": 26.0, "dy": 34.0})
        if self.baza > 0:
            n.append({
                "metin": f"KAİDE {self.baza:.0f} mm"
                         + (" · kapak yüzeyiyle hizalı"
                            if self.baza_icerlek < -0.001 else ""),
                "y": self.baza_icerlek + self.T / 2, "z": self.baza / 2,
                "dx": 26.0, "dy": 28.0})
        n.append({
            "metin": f"ARKALIK {self.ark:g} mm HDF · 4 mm kanal, 8 mm derin",
            "y": self.D - 12 - self.ark / 2, "z": self.govde_yuksekligi * 0.55,
            "dx": 26.0, "dy": 20.0})
        return n

    def render_olculeri(self) -> list[dict]:
        """Render ÜZERİNE konacak ölçüler — 3B uç noktalarla.

        Ölçü çizgileri 2B'de değil DÜNYA koordinatında tanımlanır; Blender
        kamerasıyla piksele çevrilince perspektife uyar. Ölçü değişince
        çizgi de yazı da kendiliğinden doğru yere düşer.

        Her kalem:  a → b ölçülen doğru,  d → dışa kaçış noktası
        (etiketin hangi yana yazılacağını 2B'de belirler).

        Zincir kotları teknik çizimle AYNI listeden (`kot_zinciri`) gelir.
        """
        G, D, H = self.G, self.D, self.H
        on = self.on_yuzey()
        X_ZINCIR = G + 70.0        # iç zincir düzlemi (gövdenin sağında)
        X_DIS = G + 200.0          # dış ölçü düzlemi
        o = []

        def ek(etiket, a, b, d, sinif="zincir"):
            o.append({"etiket": etiket, "a": list(a), "b": list(b),
                      "d": list(d), "sinif": sinif})

        z = self.kot_zinciri()
        for a, b in zip(z, z[1:]):
            ek(f"{b - a:.0f}", (X_ZINCIR, on, a), (X_ZINCIR, on, b),
               (X_ZINCIR + 60, on, (a + b) / 2))
        ek(f"{H:.0f}", (X_DIS, on, 0.0), (X_DIS, on, H),
           (X_DIS + 60, on, H / 2), "dis")
        ek(f"{G:.0f}", (0.0, on, H), (G, on, H), (G / 2, on, H + 60), "dis")
        ek(f"{D - on:.0f}", (G, on, H), (G, D, H),
           (G + 60, (on + D) / 2, H), "dis")
        return o

    def render_notlari(self) -> list[dict]:
        """Render üzerine oklu açıklama konacak 3B noktalar (mm, dünya).

        Ölçü VERİLMEZ — sadece "bu ne" bilgisi. Ölçüler teknik çizimde.
        """
        G, T, D = self.G, self.T, self.D
        gy, b0 = self.govde_yuksekligi, self.baza
        n = []

        for i, b in enumerate(self.bolgeler):
            kot = self.kotlar[i]
            rd = self.raf_derinligi(b.egim)
            araliklar = self._raf_araliklari(b)
            sirali = sorted(araliklar)
            ortanca = sirali[len(sirali) // 2] if sirali else 0.0
            yuksek = (max(araliklar) if araliklar
                      and max(araliklar) >= ortanca * 1.25
                      and len(araliklar) > 1 else None)
            alt = 0.0
            cizme, egimli, yuk_y, alt_slot = False, False, False, False
            boy = AYAKKABI[self._ayk(b)]["boy"]
            for j, h in enumerate(araliklar):
                orta = kot + alt + h / 2
                duz_taban = (j == 0) or not b.egim
                # En alttaki gözün tabanı DÜZ gövde tablasıdır: eğimli
                # raflı bölgede bile ayakkabı orada yatık duramaz.
                if (j == 0 and b.egim and b.ayakkabi
                        and self.ic_derinlik < boy - 1e-6 and not alt_slot):
                    n.append({"metin": "Alt slot — tabanı düz ve sığ; "
                                       "terlik ve bakım gereci. Ayakkabı "
                                       "eğimli raflara girer",
                              "konum": (G * 0.5, self.ic_derinlik * 0.45,
                                        orta)})
                    alt_slot = True
                    alt += h
                    continue
                if (yuksek and abs(h - yuksek) < 1e-6 and not yuk_y
                        and (h < CIZME_NET_YUKSEKLIK or not duz_taban)):
                    n.append({"metin": "Yüksek göz — bot ve kısa çizme; "
                                       "diğer raflardan daha açık",
                              "konum": (G * 0.5, rd * 0.5, orta)})
                    yuk_y = True
                    alt += h
                    continue
                if duz_taban and h >= CIZME_NET_YUKSEKLIK and not cizme:
                    n.append({"metin": "Çizme gözü — raf düz, dik uzun "
                                       "çizme ayakta durur",
                              "konum": (G * 0.5, D * 0.45, orta)})
                    cizme = True
                elif b.egim and not egimli:
                    n.append({"metin": f"{b.egim:g}° arkaya eğimli raf — "
                                       f"ayakkabı arkalığa yaslanır, "
                                       f"öne kaymaz",
                              "konum": (G * 0.35, rd * 0.5, orta)})
                    egimli = True
                alt += h

            if b.tip == "aski":
                for br in self.borular:
                    if br.eksen == "x":
                        n.append({"metin": "Askı borusu — soldan sağa; "
                                           "kıyafetler öne bakar",
                                  "konum": (br.konum[0] + br.boy * 0.5,
                                            br.konum[1], br.konum[2])})
                        continue
                    n.append({"metin": "Askı borusu — önden arkaya; "
                                       "kıyafetler profilden asılır",
                              # Ön uç alın panelinin arkasında kalır;
                              # etiketi borunun ARKA ucuna al ki açılı
                              # görünüşte panelin yanından görünsün.
                              "konum": (br.konum[0],
                                        br.konum[1] + br.boy * 0.88,
                                        br.konum[2])})
                if i in self.p_alin:
                    n.append({"metin": "Ön alın paneli — boruyu taşır ve "
                                       "ön ucunu kapatır",
                              "konum": (G * 0.5, T / 2,
                                        kot + b.yukseklik - b.alin / 2)})
            if b.tip == "devrilir":
                n.append({"metin": "Devrilir göz — kapak öne devrilir, "
                                   "raf onunla birlikte çıkar",
                          "konum": (G * 0.5, 0.0, kot + b.yukseklik / 2)})
            if b.tip == "acik":
                n.append({"metin": "Açık niş — kapak açmadan bırakma noktası",
                          "konum": (G * 0.5, D * 0.35,
                                    kot + b.yukseklik / 2)})

        if self.tam_kapak or any(b.kapak for b in self.bolgeler):
            n.append({"metin": "Kapak — gizli menteşe, yavaş kapanan; "
                               "çift kanat karşılıklı dışa açılır"
                               if self.tam_kapak == "cift" else
                               "Kapak — gizli menteşe, yavaş kapanan",
                      "konum": (G * 0.22, -T / 2, b0 + gy * 0.62)})
        if self.baza > 0:
            n.append({"metin": "Kaide" + (" — kapak yüzeyiyle aynı hizada"
                                          if self.baza_icerlek < -0.001
                                          else " — süpürgelik boşluğu"),
                      "konum": (G * 0.5, self.baza_icerlek + T / 2,
                                self.baza / 2)})
        n.append({"metin": "Arkalık — HDF, kanal içine; gövdeyi kareler",
                  "konum": (G * 0.5, D - 12.0, b0 + gy * 0.35)})
        return n

    # ---- 32'lik delik tablosu -------------------------------------------
    def raf_delikleri(self) -> list[dict]:
        """Yan paneldeki Ø5 raf pimi delikleri (panelin kendi ekseninde).

        `bolgeler` ve `kotlar` düzleştirilmiş sırayla eşleşir; Gardirop
        her ikisini de sütun sırasıyla düzleştirdiği için aynı kod çalışır.
        """
        s = SISTEM32
        d = []
        y_on, y_arka = s["on_kenar_mesafe"], self.D - s["arka_kenar_mesafe"]
        for b, kot in zip(self.bolgeler, self.kotlar):
            if b.tip not in ("raf", "acik", "cizme") or not b.raf:
                continue
            z0 = kot - self.baza      # yan panelin kendi ekseni
            z = z0 + 64.0
            while z < z0 + b.yukseklik - 50:
                for y in (y_on, y_arka):
                    d.append({"x": z, "y": y, "cap": s["cap"],
                              "derinlik": s["derinlik"], "tip": "raf_pimi"})
                z += s["adim"]
        return d

    # ---- rapor -----------------------------------------------------------
    def _dis_olcu_satiri(self) -> str:
        return (f"Dış ölçü      : {self.G:.0f} G × {self.D:.0f} D × "
                f"{self.H:.0f} Y mm   (baza {self.baza:.0f})")

    def _rapor_duzen(self) -> list[str]:
        r = ["-- BÖLGE DÜZENİ " + "-" * 57]
        for n, b in enumerate(self.bolgeler):
            kot = self.kotlar[n]
            if self.tam_kapak:
                kap = "tam boy kapak arkasında"
            else:
                kap = {"tek": "tek kapak", "cift": "çift kapak",
                       "devrilir": f"devrilir ({b.sira} sıra)"
                       }.get(b.kapak, "AÇIK")
            ek = f" · {b.raf} raf" if b.raf else ""
            r.append(f"  {n+1}. {(b.ad or b.tip):22s} kot {kot:6.0f} → "
                     f"{kot + b.yukseklik:6.0f}  net {b.yukseklik:5.0f} mm  "
                     f"[{kap}{ek}]")
            if b.not_:
                r.append(f"      {b.not_}")
        return r

    def _rapor_kapasite(self) -> list[str]:
        r = ["-- KAPASİTE " + "-" * 61]
        w = max([24] + [len(ad) + 2 for ad, _ in self.detay])
        for ad, c in self.detay:
            r.append(f"  {ad:{w}s} {c}")
        ayk = any(b.ayakkabi and b.tip in ("raf", "acik", "cizme", "devrilir")
                  for b in self.bolgeler)
        if ayk:
            r.append(f"  {'TOPLAM':{w}s} ~{self.cift} çift")
        for n in self.goz_notlari:
            r.append(f"  ! {n}")
        return r

    def _rapor_yapisal(self) -> list[str]:
        s = self.sehim
        r = ["-- YAPISAL KONTROL " + "-" * 54]
        r.append(f"  Raf açıklığı  : {s['aciklik_mm']:.0f} mm → sehim "
                 f"{s['sehim_mm']} mm (sünmeyle {s['sehim_sunmeli_mm']} mm) "
                 f"= {s['oran']}  [limit {s['limit']}]  "
                 f"{'UYGUN' if s['uygun'] else 'AŞIYOR'}")
        r.append(f"  Maks. açıklık : {self.max_ack:.0f} mm "
                 f"({self.T:g} mm {self.malzeme}, 65 kg/m²)")
        r += self._rapor_devrilme()
        return r

    def _rapor_devrilme(self) -> list[str]:
        d = self.devrilme
        return [f"  Devrilme      : h={d['yukseklik_mm']:.0f} mm · "
                f"m={d['kutle_kg']} kg · h_cg×m={d['h_cg_m_x_kg']} (eşik 6) "
                f"→ {'TEST GEREKLİ' if d['stabilite_testi_gerekli'] else 'tetik yok'}",
                f"                  {d['aciklama']}"]

    def rapor(self) -> str:
        """Mühendislik raporu. Uyarılar malzeme özetinden ÖNCE gelir;
        rapor asla uyarı gizlemez."""
        r = [f"{'=' * 74}",
             f"{self.ad}  [{self.kod}]",
             f"{'=' * 74}"]
        if self.aciklama:
            r += [self.aciklama, ""]
        r.append(self._dis_olcu_satiri())
        r.append(f"İç ölçü       : {self.ic_genislik:.0f} × "
                 f"{self.ic_derinlik:.0f} mm")
        r.append(f"Malzeme       : {MALZEMELER[self.malzeme].ad} "
                 f"{self.T:g} mm · arkalık {self.ark:g} mm HDF")
        r.append("")
        r += self._rapor_duzen()
        r.append("")
        r += self._rapor_kapasite()
        r.append("")
        r += self._rapor_yapisal()
        if self.uyarilar:
            r.append("")
            r.append("-- UYARILAR " + "-" * 61)
            for u in self.uyarilar:
                r.append(f"  ! {u}")
        if self.donanim:
            r.append("")
            r.append("-- DONANIM " + "-" * 62)
            for kod, ad, olcu, adet, notu in self.donanim:
                r.append(f"  {kod:12s} {ad:36s} {olcu:>9s} × {adet}"
                         + (f"   {notu}" if notu else ""))
        r.append("")
        r.append(ozet_rapor(self.parcalar))
        return "\n".join(r)


# ---------------------------------------------------------------------------
# ÜRETİM
# ---------------------------------------------------------------------------

def uret(d: Dolap, klasor: str, olcek: float = 15.0, cnc: bool = True,
         sessiz: bool = False) -> dict:
    """Rapor · BOM · donanım listesi · 3B (STEP/GLB/STL) · ölçülü A3 çizim ·
    kesim planı · CNC DXF. Dönen sözlükte `uyarilar` (tasarım) ve
    `yerlesim_hatalari` (nesting) listeleri de bulunur — çağıran gizleyemez.
    """
    import datetime as _dt
    import cizim
    from build123d import Plane

    os.makedirs(klasor, exist_ok=True)
    cikti = {"uyarilar": list(d.uyarilar), "yerlesim_hatalari": []}
    tarih = _dt.date.today().isoformat()
    rapor = d.rapor()
    if not sessiz:
        print(rapor)
    with open(os.path.join(klasor, f"{d.kod}-RAPOR.txt"), "w",
              encoding="utf-8") as f:
        f.write(rapor)
    cikti["bom"] = bom_csv(d.parcalar, os.path.join(klasor, f"{d.kod}-BOM.csv"))
    if d.donanim:
        cikti["donanim"] = donanim_csv(
            d.donanim, os.path.join(klasor, f"{d.kod}-DONANIM.csv"))

    asm = cizim.model_kur(d.parcalar, d.yerlesim, d.ad, borular=d.borular)
    cikti.update(cizim.disa_aktar(asm, klasor, d.kod))
    kati = asm.solids()
    birlesik = kati[0]
    for s in kati[1:]:
        birlesik = birlesik + s

    s = cizim.Sayfa(olcek=olcek, boyut="A3")
    g = s.coklu_gorunus(birlesik, ("on", "sag", "ust"),
                        kesit_duzlemi=Plane.YZ.offset(d.G / 2))
    k = s.k
    on, sag = g["on"], g["sag"]
    # ÖNEMLİ: ölçüler nominal d.G/d.D'den DEĞİL, görünüşün ölçülen
    # model genişliğinden alınır. Aksi halde kapak/baza gövdeden taşınca
    # (ör. kapak yüzeyi +18 mm) çizgi ile yazı birbirini tutmaz.
    s.olcu_yatay(on["x"], on["x"] + on["model_gen"] * k, on["y"], on["y"] - 11)
    s.olcu_dikey(on["y"], on["y"] + on["model_yuk"] * k, on["x"], on["x"] - 11)
    s.olcu_yatay(sag["x"], sag["x"] + sag["model_gen"] * k,
                 sag["y"], sag["y"] - 11)
    # Zincir ölçü: baza + bölge sınırları + RAF kotları.
    # Render üzerindeki ölçüler de AYNI listeyi kullanır (kot_zinciri).
    kotlar = [on["y"] + z * k for z in d.kot_zinciri()]
    s.olcu_zinciri(sorted(set(round(v, 2) for v in kotlar)),
                   on["x"] + d.G * k, on["x"] + d.G * k + 12, dikey=True)
    # Kesit üzerine atıf okları (askı borusu, alın paneli, arkalık)
    for n in d.cizim_notlari():
        try:
            hedef = s.model_kagit(g["kesit"], n["y"], n["z"])
            s.oklu_not(n["metin"], hedef, dx=n.get("dx", 20.0),
                       dy=n.get("dy", 10.0))
        except Exception as e:
            print(f"!! atıf çizilemedi ({n['metin']}): {e}")

    # Üst not: ayakkabılıkta çift, gardıropta askı adedi anlamlıdır
    ayk = any(b.ayakkabi and b.tip in ("raf", "acik", "cizme", "devrilir")
              for b in d.bolgeler)
    aski_b = [b for b in d.bolgeler if b.tip == "aski"]
    if ayk:
        ozet = f"Kapasite ~{d.cift} çift"
    elif aski_b:
        n = sum(int(c.split()[0]) for _, c in d.detay if "askı" in c)
        ozet = f"{n} askı + {len(d.bolgeler) - len(aski_b)} raf bölgesi"
    else:
        ozet = f"{len(d.bolgeler)} bölge"
    s.yazi(f"{ozet}  ·  raf açıklığı {d.ic_genislik:.0f} mm "
           f"({d.sehim['oran']})  ·  {len(d.bolgeler)} bölge",
           26, s.yuk - 22, h=2.5)
    # Antet ölçüsü GÖVDE değil, kapak/baza dahil GERÇEK dış ölçüdür
    s.antet(d.ad,
            f"{on['model_gen']:.0f}×{sag['model_gen']:.0f}×"
            f"{on['model_yuk']:.0f} mm",
            f"{d.kod}-01", tarih, MALZEMELER[d.malzeme].ad, "mobilya-cad")
    cikti.update({f"cizim_{a}": v
                  for a, v in s.kaydet(klasor, f"{d.kod}-CIZIM").items()})

    for mlz, kal in sorted({(p.malzeme, p.kalinlik) for p in d.parcalar}):
        lv = optimize(d.parcalar, mlz, kal)
        h = optimize_dogrula(lv)
        if h:
            print("!! yerleşim hatası:", h)
            cikti["yerlesim_hatalari"] += h
        y = cizim.yerlesim_dxf(lv, klasor, f"{d.kod}-{mlz}{kal:g}",
                               f"{MALZEMELER[mlz].ad} {kal:g} mm")
        cikti[f"kesim_{mlz}_{kal:g}"] = y["pdf"]

    if cnc:
        cnc_kl = os.path.join(klasor, "cnc")
        yan = next(p for p in d.parcalar if p.kod == d.p_yan)
        cikti["cnc_yan"] = cizim.cnc_dxf(yan, d.raf_delikleri(), cnc_kl)
        for p in d.parcalar:
            if p.kod != d.p_yan:
                cizim.cnc_dxf(p, [], cnc_kl)
    return cikti
