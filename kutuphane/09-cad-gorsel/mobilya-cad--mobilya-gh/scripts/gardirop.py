"""
gardirop.py — SÜTUNLU (kolonlu) gövde üreteci.

`dolap.Dolap` tek kolonludur: bölgeler yalnızca düşey sıralanır. Gardırop
genişledikçe bu yetmez —

  • 1064 mm iç genişlikte 18 mm suntalam raf L/78 sarkar (limit L/240).
    Orta dikme YAPISAL OLARAK ZORUNLUDUR, tercih değildir.
  • Askılı bölme ile raflı/çekmeceli bölme yan yana durur; her sütunun
    kendi düşey düzeni olur.

Bu modül tam boy düşey dikmelerle gövdeyi sütunlara böler; her sütun
kendi `Bolge` yığınını taşır. Geri kalan her şey (parça modeli, kontroller,
çizim, render, belge) dolap.py ve mobilya.py'den aynen gelir.

    from gardirop import Gardirop, Sutun
    from dolap import Bolge

    g = Gardirop(genislik=1100, derinlik=482, yukseklik=2100,
                 sutunlar=[Sutun([Bolge("aski", 1400, ad="uzun askı")]),
                           Sutun([Bolge("raf", 1400, raf=4, ad="raflar")])],
                 kapak="sutun")
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from mobilya import (
    ASKI, aski_kapasitesi, aski_yonu, AYAKKABI, MALZEMELER, RAF_ARALIGI,
    SISTEM32, Parca, cift_sayisi, devrilme_kontrolu, max_aciklik,
    optimize, ozet_rapor, raf_sehimi,
)
from dolap import Bolge, Dolap, CIZME_NET_YUKSEKLIK, DERZ, KIYAFET_BOYU_KONTROL


@dataclass
class Sutun:
    """Gövdenin düşey bir bölmesi. Kendi bölge yığınını taşır."""
    bolgeler: list
    genislik: float | None = None     # None -> kalan genişliği eşit paylaş
    ad: str = ""
    kapak: str | None = None          # None | "tek" | "cift"; None ise
                                      # Gardirop.kapak kuralı uygulanır
    ayna: bool = False                # KAPAK yüzeyi ayna
    ayna_arkalik: bool = False        # bu sütunun ARKASI ayna
    ust_yukseklik: float | None = None
    # Ortak alt bölmenin ÜSTÜNDE bu sütunun gövde yüksekliği.
    #   None -> kalanı doldur (dikdörtgen gövde)
    #   0    -> bu sütunun üstünde DOLAP YOK. Yan panel, tabla ve raf
    #           konmaz; yalnız ARKALIK devam eder. Gövde L olur.


class Gardirop(Dolap):
    def __init__(self, *, genislik, derinlik, yukseklik, sutunlar,
                 ortak_alt=None, kusak: float = 0.0,
                 kapak: str | None = "sutun", baza=80.0, baza_icerlek=50.0,
                 kalinlik=18.0, malzeme="suntalam", arkalik=3.0,
                 kiyafet="ceket", kod="GRD-01", ad="Gardırop", aciklama=""):
        self.G, self.D, self.H = float(genislik), float(derinlik), float(yukseklik)
        self.baza, self.T = float(baza), float(kalinlik)
        self.malzeme, self.ark = malzeme, float(arkalik)
        self.ayk = "karma"
        self.kiyafet = kiyafet
        self.kod, self.ad, self.aciklama = kod, ad, aciklama
        self.sutunlar = list(sutunlar)
        # ortak_alt: TÜM sütunların altında, dikmesiz, tam genişlik
        # bölme (yorgan/valiz). Tavanı 1064 mm açıklık geçtiği için
        # ÖN KUŞAK zorunludur — kusak=0 ise uyarı verilir.
        self.ortak_alt = ortak_alt
        self.kusak = float(kusak)
        # kapak: "sutun" -> her sütuna bir kanat · "tek"/"cift" -> tam boy
        self.kapak_kurali = kapak
        self.tam_kapak = kapak   # belge.py dış ölçüde kapağı sayabilsin
        if baza_icerlek == "kapak":
            baza_icerlek = -float(kalinlik)
        self.baza_icerlek = float(baza_icerlek)

        self.uyarilar: list[str] = []
        self.parcalar: list[Parca] = []
        self.yerlesim = []
        self.borular = []
        self.donanim = []
        self.detay = []
        self.p_alin = {}
        self._hesapla()

    # ---- sütun geometrisi ------------------------------------------------
    @property
    def dikme_sayisi(self):
        return len(self.sutunlar) - 1

    def _sutun_genislikleri(self):
        """Her sütunun NET iç genişliği (dikmeler düşülmüş)."""
        toplam = self.ic_genislik - self.dikme_sayisi * self.T
        sabit = [s.genislik for s in self.sutunlar if s.genislik]
        serbest = [s for s in self.sutunlar if not s.genislik]
        kalan = toplam - sum(sabit)
        pay = kalan / len(serbest) if serbest else 0.0
        return [s.genislik if s.genislik else pay for s in self.sutunlar]

    def _sutun_x(self):
        """Her sütunun sol kenarının x'i (gövde iç yüzünden)."""
        xs, x = [], self.T
        for g in self._sutun_genislikleri():
            xs.append(x)
            x += g + self.T
        return xs

    # ---- hesap -----------------------------------------------------------
    def _hesapla(self):
        gen = self._sutun_genislikleri()
        self.sutun_gen = gen
        self.sutun_x = self._sutun_x()

        if min(gen) <= 0:
            self.uyarilar.append(
                f"Sütun genişlikleri sığmıyor: iç genişlik "
                f"{self.ic_genislik:.0f} mm, {self.dikme_sayisi} dikme.")

        # Ortak alt bölme varsa sütunlar onun TAVANININ üstünden başlar
        self.sutun_taban = self.baza + self.T
        if self.ortak_alt:
            self.ortak_kot = self.baza + self.T
            self.sutun_taban = self.ortak_kot + self.ortak_alt.yukseklik + self.T
            if self.kusak <= 0:
                self.uyarilar.append(
                    f"Ortak alt bölme {self.ic_genislik:.0f} mm açıklıkta ve "
                    f"ÖN KUŞAK yok — tavan paneli taşımaz. kusak=100 verin.")
            else:
                from mobilya import kusakli_sehim
                r = kusakli_sehim(self.ic_genislik, self.ic_derinlik, self.T,
                                  self.kusak, tekil_yuk_kg=25.0,
                                  malzeme=self.malzeme)
                self.kusak_sehim = r
                if not r["uygun"]:
                    self.uyarilar.append(
                        f"Ortak alt bölme tavanı: {self.kusak:.0f} mm kuşakla "
                        f"sehim {r['sehim_sunmeli_mm']} mm = {r['oran']} — "
                        f"{r['limit']} sınırını aşıyor. Kuşağı büyütün.")

        # Sütun ÜST yükseklikleri (ortak bölmenin üstü)
        tam_ust = self.govde_yuksekligi - 2 * self.T - (
            (self.ortak_alt.yukseklik + self.T) if self.ortak_alt else 0.0)
        self.sutun_ust = [tam_ust if s.ust_yukseklik is None
                          else float(s.ust_yukseklik) for s in self.sutunlar]
        self.L_govde = any(u <= 0.001 for u in self.sutun_ust)
        if self.L_govde:
            self.uyarilar.append(
                "L gövde: üstünde dolap olmayan sütunda arkalık kendi başına "
                "kalır. 3 mm HDF orada duramaz — o alanda arkalık 18 mm "
                "panele çıkarıldı ve DUVARA sabitlenmesi YAPISAL şarttır "
                "(devrilme braketinden ayrı bir gereklilik).")

        # Bölge kotları — her sütun ayrı
        ic_yuk_tam = tam_ust
        self.sutun_kotlar = []
        for si, s in enumerate(self.sutunlar):
            if self.sutun_ust[si] <= 0.001:
                s.bolgeler = []
                self.sutun_kotlar.append([])
                continue
            ic_yuk_tam = self.sutun_ust[si]
            n = len(s.bolgeler)
            kullanilabilir = ic_yuk_tam - (n - 1) * self.T if n else 0.0
            istenen = sum(b.yukseklik for b in s.bolgeler)
            fark = kullanilabilir - istenen if n else 0.0
            if n and abs(fark) > 0.5:
                hedef = max((b for b in s.bolgeler
                             if b.tip in ("raf", "acik")),
                            key=lambda b: b.yukseklik, default=None)
                if hedef is not None:
                    hedef.yukseklik += fark
                else:
                    for b in s.bolgeler:
                        b.yukseklik += fark / n
            kot, z = [], self.sutun_taban
            for b in s.bolgeler:
                kot.append(z)
                z += b.yukseklik + self.T
            self.sutun_kotlar.append(kot)

        # ---- yapısal kontroller (raf açıklığı = SÜTUN genişliği)
        self.sehim = raf_sehimi(aciklik=max(gen), derinlik=self.ic_derinlik,
                                kalinlik=self.T, malzeme=self.malzeme)
        self.max_ack = max_aciklik(self.ic_derinlik, self.T, self.malzeme)
        if not self.sehim["uygun"]:
            self.uyarilar.append(
                f"En geniş sütun {max(gen):.0f} mm > {self.max_ack:.0f} mm "
                f"limiti (sehim {self.sehim['sehim_sunmeli_mm']} mm = "
                f"{self.sehim['oran']}). Dikme ekleyin.")
        if self.ic_genislik > self.max_ack and self.dikme_sayisi == 0:
            self.uyarilar.append(
                f"İç genişlik {self.ic_genislik:.0f} mm dikmesiz — "
                f"{self.max_ack:.0f} mm sınırı aşılıyor.")

        # ---- sütun bazlı bölge kontrolleri
        self.aski = None
        for si, s in enumerate(self.sutunlar):
            sg = gen[si]
            ad_s = s.ad or f"sütun {si+1}"
            for b in s.bolgeler:
                if b.tip == "aski":
                    a = aski_yonu(self.ic_derinlik, sg)
                    self.aski = a
                    if a["yon"] is None:
                        self.uyarilar.append(f"'{ad_s} · {b.ad}': {a['aciklama']}")
                    elif not a.get("rahat", False):
                        self.uyarilar.append(f"'{ad_s} · {b.ad}': {a['aciklama']}")
                    gerek = KIYAFET_BOYU_KONTROL.get(b.kiyafet or self.kiyafet,
                                                     1000.0)
                    if b.yukseklik < gerek:
                        self.uyarilar.append(
                            f"'{ad_s} · {b.ad}': net {b.yukseklik:.0f} mm — "
                            f"{b.kiyafet or self.kiyafet} için {gerek:.0f} mm "
                            f"gerekir.")
                if b.tip == "raf" and b.raf and not b.raf_kotlari:
                    ara = b.yukseklik / (b.raf + 1)
                    if b.ayakkabi is False and ara < 250:
                        self.uyarilar.append(
                            f"'{ad_s} · {b.ad}': raf aralığı {ara:.0f} mm — "
                            f"katlı giysi için 250-380 mm önerilir.")
                if b.tip == "cekmece" and b.raf:
                    # Çekmece ERGONOMİ: en üst çekmecenin üst kenarı ~1300 mm'yi
                    # geçerse içine bakılamaz, kullanılamaz hale gelir.
                    bi = s.bolgeler.index(b)
                    ust = self.sutun_kotlar[si][bi] + b.yukseklik
                    if ust > 1350:
                        self.uyarilar.append(
                            f"'{ad_s} · {b.ad}': çekmece üst kenarı "
                            f"{ust:.0f} mm — 1350 mm üstündeki çekmecenin "
                            f"içine bakılamaz. Çekmece bölgesini sütunun "
                            f"ALTINA alın (bölge listesinde ilk sıraya).")
                    yuk = b.yukseklik / b.raf
                    if not (140 <= yuk <= 260):
                        self.uyarilar.append(
                            f"'{ad_s} · {b.ad}': çekmece yüksekliği "
                            f"{yuk:.0f} mm — 150-230 mm bandı dışında.")

        self._parcalar()
        self._yerlestir()
        self._kapasite()

        kutle = sum(p.agirlik_kg() for p in self.parcalar)
        self.devrilme = devrilme_kontrolu(self.H, kutle, self.H * 0.45)

    # ---- kapasite --------------------------------------------------------
    def _kapasite(self):
        self.cift = 0
        self.detay = []
        for si, s in enumerate(self.sutunlar):
            sg = self.sutun_gen[si]
            ad_s = s.ad or f"sütun {si+1}"
            for b in s.bolgeler:
                if b.tip == "aski":
                    a = aski_yonu(self.ic_derinlik, sg)
                    boy = a["boru_boyu"] if a["yon"] else 0
                    n = aski_kapasitesi(boy, b.kiyafet or self.kiyafet)
                    self.detay.append(
                        (f"{ad_s} · {b.ad or 'askı'}",
                         f"{n} askı ({b.kiyafet or self.kiyafet})"))
                elif b.tip == "cekmece":
                    self.detay.append(
                        (f"{ad_s} · {b.ad or 'çekmece'}", f"{b.raf} çekmece"))
                elif b.tip in ("raf", "acik"):
                    self.detay.append(
                        (f"{ad_s} · {b.ad or b.tip}", f"{b.raf + 1} göz"))

    # ---- parçalar --------------------------------------------------------
    def _parcalar(self):
        T, G, D, M = self.T, self.G, self.D, self.malzeme
        gy = self.govde_yuksekligi
        P = self.parcalar
        i = [0]

        def kod():
            i[0] += 1
            return f"{self.kod}-P{i[0]:02d}"

        # Sütun başına toplam gövde yüksekliği (baza üstünden)
        bant = (self.sutun_taban - self.baza) if self.ortak_alt else 0.0
        self.sutun_toplam = [
            (bant + u + T) if u > 0.001 else bant
            for u in self.sutun_ust] if self.ortak_alt else \
            [gy for _ in self.sutunlar]

        self.p_yan_sol = self.p_yan_sag = None
        if not self.L_govde:
            self.p_yan = kod()
            P.append(Parca(self.p_yan, "Yan panel", gy, D, T, M, adet=2,
                           desen_kilit=True, grup="gövde", bant={"W1": 2.0},
                           not_="ön kenar 2 mm bant · desen DİKEY · 32'lik "
                                "delik sırası ön kenardan 37 mm"))
            self.p_ust = kod()
            P.append(Parca(self.p_ust, "Üst tabla", self.ic_genislik, D, T, M,
                           adet=1, grup="gövde", bant={"W1": 2.0}))
        else:
            # L gövde: sol ve sağ yan panel FARKLI boyda
            hs, hd = self.sutun_toplam[0], self.sutun_toplam[-1]
            self.p_yan_sol = kod()
            P.append(Parca(self.p_yan_sol, "Yan panel — SOL (tam boy)",
                           hs, D, T, M, adet=1, desen_kilit=True,
                           grup="gövde", bant={"W1": 2.0},
                           not_="ön kenar 2 mm bant · desen DİKEY"))
            self.p_yan = self.p_yan_sol   # CNC delik tablosu bunu kullanır
            self.p_yan_sag = kod()
            P.append(Parca(self.p_yan_sag, "Yan panel — SAĞ (alçak)",
                           hd, D, T, M, adet=1, desen_kilit=True,
                           grup="gövde", bant={"W1": 2.0, "L2": 2.0},
                           not_=f"Yalnız {hd:.0f} mm — üstünde dolap yok. "
                                f"ÜST kenarı da görünür, 2 mm bantlı."))
            self.p_ust = kod()
            ust_gen = [self.sutun_gen[i] for i, u in enumerate(self.sutun_ust)
                       if u > 0.001]
            P.append(Parca(self.p_ust, "Üst tabla (yalnız yüksek sütun)",
                           ust_gen[0], D, T, M, adet=len(ust_gen),
                           grup="gövde", bant={"W1": 2.0},
                           not_="Yalnız dolap olan sütunun üstünü kapatır."))
        self.p_alt = kod()
        P.append(Parca(self.p_alt, "Alt tabla", self.ic_genislik, D, T, M,
                       adet=1, grup="gövde", bant={"W1": 2.0}))

        # Ortak alt bölmenin tavanı + ön kuşak
        self.p_ortak_tavan = self.p_kusak = None
        if self.ortak_alt:
            self.p_ortak_tavan = kod()
            P.append(Parca(self.p_ortak_tavan, "Ortak bölme tavanı",
                           self.ic_genislik, D - 20, T, M, adet=1,
                           grup="gövde", bant={"W1": 2.0},
                           not_=f"TAM GENİŞLİK {self.ic_genislik:.0f} mm — "
                                f"altında dikme YOK. Tek başına taşımaz; "
                                f"ön kuşakla birlikte L kesit oluşturur."))
            if self.kusak > 0:
                self.p_kusak = kod()
                P.append(Parca(self.p_kusak, "Ön kuşak",
                               self.ic_genislik, self.kusak, T, M, adet=1,
                               desen_kilit=True, grup="gövde",
                               bant={"L1": 2.0},
                               not_=f"YAPISAL — tavan panelinin ÖN kenarının "
                                    f"altına, boydan boya. Kesit atalet "
                                    f"momentini "
                                    f"{getattr(self,'kusak_sehim',{}).get('kazanc','?')} "
                                    f"kat artırır. Alt kenarı görünür, "
                                    f"2 mm bantlı."))

        self.p_dikme = None
        if self.dikme_sayisi:
            self.p_dikme = kod()
            if self.L_govde:
                dikme_boy = max(self.sutun_ust)
            else:
                dikme_boy = (gy - 2 * T - (self.ortak_alt.yukseklik + T)
                             if self.ortak_alt else gy - 2 * T)
            P.append(Parca(self.p_dikme, "Orta dikme",
                           dikme_boy, D, T, M, adet=self.dikme_sayisi,
                           desen_kilit=True, grup="gövde", bant={"W1": 2.0},
                           not_=f"YAPISAL — {self.ic_genislik:.0f} mm açıklık "
                                f"dikmesiz {self.max_ack:.0f} mm sınırını aşar. "
                                f"Alt ve üst tabla arasına, minifix + kavela."))

        # Sütun içi yatay ayırıcılar ve raflar
        self.p_ara = {}
        self.p_raf = {}
        self.p_cekmece = {}
        for si, s in enumerate(self.sutunlar):
            sg = self.sutun_gen[si]
            ara = len(s.bolgeler) - 1
            if ara > 0:
                k = kod()
                self.p_ara[si] = k
                P.append(Parca(k, f"Sabit ara tabla (S{si+1})", sg, D - 20, T,
                               M, adet=ara, grup="gövde", bant={"W1": 2.0}))
            raf_adet = sum(b.raf for b in s.bolgeler
                           if b.tip in ("raf", "acik"))
            if raf_adet:
                k = kod()
                self.p_raf[si] = k
                P.append(Parca(k, f"Ayarlanabilir raf (S{si+1})", sg - 2.0,
                               self.ic_derinlik - 15, T, M, adet=raf_adet,
                               grup="raf", bant={"W1": 2.0},
                               not_="Ø5 pim üzerine · 32'lik sistemde ayarlanır"))
            cek = sum(b.raf for b in s.bolgeler if b.tip == "cekmece")
            if cek:
                k = kod()
                self.p_cekmece[si] = k
                yuk = next(b.yukseklik / b.raf for b in s.bolgeler
                           if b.tip == "cekmece")
                P.append(Parca(k, f"Çekmece ön paneli (S{si+1})",
                               yuk - 4.0, sg - 4.0, T, M, adet=cek,
                               desen_kilit=True, grup="çekmece",
                               bant={"L1": 2.0, "L2": 2.0,
                                     "W1": 2.0, "W2": 2.0},
                               not_="4 kenar 2 mm bant · teleskopik ray, "
                                    "yanda 13 mm boşluk"))
                self.donanim.append(
                    (f"{self.kod}-D{len(self.donanim)+1:02d}",
                     "Teleskopik çekmece rayı (tam açılım)",
                     f"{int((self.ic_derinlik - 20) // 50 * 50):.0f} mm",
                     cek * 2,
                     "çift başına 2 adet · yanda 13 mm boşluk gerekir"))

        # L gövdede: dolap olmayan sütunun arkasında 18 mm sırt paneli
        self.p_sirt = {}
        for si, u in enumerate(self.sutun_ust):
            if u > 0.001:
                continue
            bosluk = gy - self.sutun_toplam[si]
            if bosluk <= 1:
                continue
            k = kod()
            self.p_sirt[si] = (k, bosluk)
            P.append(Parca(k, f"Sırt paneli — açık alan (S{si+1})",
                           bosluk, self.sutun_gen[si] + T, T, M, adet=1,
                           desen_kilit=True, grup="gövde",
                           bant={"L1": 2.0, "W1": 2.0, "W2": 2.0},
                           not_="YAPISAL. Bu alanda yan panel ve tabla yok; "
                                "3 mm arkalık kendi başına duramaz. 18 mm "
                                "panel dikmeye ve ortak tavana vidalanır, "
                                "üst kenarından DUVARA sabitlenir. Üç kenarı "
                                "görünür, bantlı."))
            self.donanim.append(
                (f"{self.kod}-DB", "Duvar sabitleme braketi (rijit metal)",
                 "-", 2, "sırt panelinin üst kenarı — YAPISAL, devrilme "
                         "braketinden ayrı"))

        # Aynalı arkalık (açık bölmenin arkası)
        self.p_ayna = {}
        for si, s2 in enumerate(self.sutunlar):
            if not s2.ayna_arkalik:
                continue
            if si in self.p_sirt:
                yuk = self.p_sirt[si][1]
            else:
                yuk = sum(b.yukseklik for b in s2.bolgeler) + \
                    (len(s2.bolgeler) - 1) * T
            k = kod()
            self.p_ayna[si] = k
            P.append(Parca(k, f"Aynalı arkalık (S{si+1})", yuk,
                           self.sutun_gen[si], 4.0, "mdf", adet=1,
                           grup="ayna",
                           not_="4 mm AYNA, güvenlik filmli. Arkalığın önüne "
                                "yapıştırılır; açık bölmeyi görsel olarak "
                                "iki katı derin gösterir."))

        # Askı boruları
        from cizim import Boru
        for si, s in enumerate(self.sutunlar):
            sg = self.sutun_gen[si]
            for bi, b in enumerate(s.bolgeler):
                if b.tip != "aski":
                    continue
                a = aski_yonu(self.ic_derinlik, sg)
                if not a["yon"]:
                    continue
                cap = ASKI["boru_cap_yuvarlak"]
                kot = self.sutun_kotlar[si][bi]
                z = kot + b.yukseklik - 55.0
                x0 = self.sutun_x[si]
                if a["yon"] == "x":
                    boy = sg
                    self.borular.append(Boru(
                        f"{self.kod}-A{si+1}{bi+1}",
                        f"Askı borusu Ø{cap:g} (soldan sağa)",
                        cap, boy, (x0, self.ic_derinlik / 2 + 10, z), "x"))
                else:
                    boy = self.ic_derinlik - 35
                    self.borular.append(Boru(
                        f"{self.kod}-A{si+1}{bi+1}",
                        f"Askı borusu Ø{cap:g} (önden arkaya)",
                        cap, boy, (x0 + sg / 2, 20.0, z), "y"))
                self.donanim.append(
                    (f"{self.kod}-A{si+1}{bi+1}",
                     f"Askı borusu Ø{cap:g} krom", f"{boy:.0f} mm", 1,
                     "boy kesilir" if a["yon"] == "y" else
                     "yan panel/dikmeye flanşla"))
                self.donanim.append(
                    (f"{self.kod}-F{si+1}{bi+1}", "Askı borusu flanşı", "-", 2,
                     "üstteki sabit tablanın alt yüzüne"
                     if a["yon"] == "y" else "yan panel ve dikmeye"))

        # Kapaklar
        self.p_kapak = {}
        for si, s in enumerate(self.sutunlar):
            tip = s.kapak or (self.kapak_kurali
                              if self.kapak_kurali == "sutun" else None)
            if tip in (None, "yok"):
                continue
            adet = 2 if tip == "cift" else 1
            sg = self.sutun_gen[si]
            # kanat, sütunun kendi genişliği + payına oturur
            toplam = sg + self.T
            k_gen = (toplam - DERZ - (DERZ if adet == 2 else 0)) / adet
            k = kod()
            self.p_kapak[si] = (k, adet)
            kapak_boy = gy - (self.sutun_taban - self.baza) - 2 * DERZ
            P.append(Parca(k, f"Kapak (S{si+1})"
                              + (" — AYNALI" if s.ayna else ""),
                           kapak_boy, k_gen, T, M, adet=adet,
                           desen_kilit=True, grup="kapak",
                           bant={"L1": 2.0, "L2": 2.0, "W1": 2.0, "W2": 2.0},
                           not_="4 kenar 2 mm bant · Ø35 gizli menteşe"
                                + (" · ön yüz AYNA, güvenlik filmli 4 mm"
                                   if s.ayna else "")))
            self.donanim.append(
                (f"{self.kod}-M{si+1}", "Gizli menteşe Ø35 (yavaş kapanan)",
                 "-", adet * (4 if gy > 1600 else 3),
                 "kap kenardan 22 mm eksen · Blum vida aralığı 45 mm"))

        # Ortak alt bölmenin kendi kapağı — tam genişlik
        self.p_ortak_kapak = None
        if self.ortak_alt and self.ortak_alt.kapak:
            adet = 2 if self.ortak_alt.kapak == "cift" else 1
            kg = (G - 2 * DERZ - (DERZ if adet == 2 else 0)) / adet
            k = kod()
            self.p_ortak_kapak = (k, adet)
            P.append(Parca(k, f"Ortak bölme kapağı ({adet} kanat)",
                           self.ortak_alt.yukseklik + T - DERZ, kg, T, M,
                           adet=adet, desen_kilit=True, grup="kapak",
                           bant={"L1": 2.0, "L2": 2.0, "W1": 2.0, "W2": 2.0},
                           not_="Tam genişlik — yorgan gözünü tümüyle kapatır. "
                                "Üstteki sütun kapağıyla arasında 3 mm derz."))
            self.donanim.append(
                (f"{self.kod}-MO", "Gizli menteşe Ø35 (yavaş kapanan)", "-",
                 adet * 3, "ortak bölme kapağı"))

        if self.baza > 0:
            hizali = self.baza_icerlek <= 0.001
            self.p_baza_on = kod()
            P.append(Parca(self.p_baza_on, "Baza ön",
                           G if hizali else self.ic_genislik,
                           self.baza, T, M, adet=1, grup="gövde",
                           desen_kilit=hizali, bant={"L1": 2.0},
                           not_=("kapak yüzeyiyle hizalı, tam genişlik"
                                 if self.baza_icerlek < -0.001 else
                                 "gövde ön yüzüyle hizalı" if hizali else
                                 f"ön yüzden {self.baza_icerlek:.0f} mm içeri")))
            self.p_baza_yan = kod()
            P.append(Parca(self.p_baza_yan, "Baza yan",
                           (D - self.baza_icerlek - T) if hizali else (D - 70),
                           self.baza, T, M, adet=2, grup="gövde",
                           bant={"W1": 2.0} if hizali else {}))

        # Arkalık — L gövdede İKİ parça: boşlukta 18 mm sırt paneli zaten
        # var, oraya ayrıca 3 mm HDF kesmek malzeme israfı olur.
        self.p_ark2 = None
        if self.L_govde:
            bant_yuk = min(self.sutun_toplam)
            self.p_ark = kod()
            P.append(Parca(self.p_ark, "Arkalık — alt bant",
                           bant_yuk - T + 16.0, self.ic_genislik + 16.0,
                           self.ark, "hdf", adet=1, grup="gövde",
                           not_="Tam genişlik, ortak bölmenin arkası. "
                                "4 mm kanal içine, 8 mm derin."))
            yuksek = [i for i, u in enumerate(self.sutun_ust) if u > 0.001]
            if yuksek:
                self.p_ark2 = kod()
                P.append(Parca(self.p_ark2, "Arkalık — yüksek sütun",
                               max(self.sutun_ust) + 16.0,
                               self.sutun_gen[yuksek[0]] + 16.0,
                               self.ark, "hdf", adet=len(yuksek),
                               grup="gövde",
                               not_="Yalnız dolap olan sütunun arkası. Açık "
                                    "alanın arkasında 3 mm HDF YOK — orada "
                                    "18 mm sırt paneli var."))
        else:
            self.p_ark = kod()
            P.append(Parca(self.p_ark, "Arkalık", gy - 2 * T + 16.0,
                           self.ic_genislik + 16.0, self.ark, "hdf", adet=1,
                           grup="gövde",
                           not_="4 mm kanal içine, 8 mm derin, arka kenardan "
                                "12 mm · dikmeye de vidalanır"))

    # ---- yerleştirme -----------------------------------------------------
    def _yerlestir(self):
        from cizim import Yerlestirme, boru_kati
        T, G, D = self.T, self.G, self.D
        b0, gy = self.baza, self.govde_yuksekligi
        Y = self.yerlesim

        if not self.L_govde:
            Y.append(Yerlestirme(self.p_yan, (0, 0, b0), "x", "z"))
            Y.append(Yerlestirme(self.p_yan, (G - T, 0, b0), "x", "z"))
            Y.append(Yerlestirme(self.p_ust, (T, 0, b0 + gy - T), "z", "x"))
        else:
            Y.append(Yerlestirme(self.p_yan_sol, (0, 0, b0), "x", "z"))
            Y.append(Yerlestirme(self.p_yan_sag, (G - T, 0, b0), "x", "z"))
            for si, u in enumerate(self.sutun_ust):
                if u <= 0.001:
                    continue
                Y.append(Yerlestirme(
                    self.p_ust, (self.sutun_x[si], 0,
                                 b0 + self.sutun_toplam[si] - T), "z", "x"))
        Y.append(Yerlestirme(self.p_alt, (T, 0, b0), "z", "x"))

        # açık alanın sırt paneli
        for si, (k, bosluk) in getattr(self, "p_sirt", {}).items():
            x0 = self.sutun_x[si] - T
            Y.append(Yerlestirme(k, (x0, D - 12 - self.ark - T,
                                     b0 + self.sutun_toplam[si]),
                                 "y", "z", renk="#C8B48C"))

        # ortak alt bölme tavanı + ön kuşak
        if self.p_ortak_tavan:
            zt = self.sutun_taban - T
            Y.append(Yerlestirme(self.p_ortak_tavan, (T, 10, zt), "z", "x"))
            if self.p_kusak:
                Y.append(Yerlestirme(self.p_kusak, (T, 0, zt - self.kusak),
                                     "y", "x", renk="#C8B48C"))

        # dikmeler — ortak bölme varsa onun tavanından başlar
        if self.p_dikme:
            for si in range(1, len(self.sutunlar)):
                x = self.sutun_x[si] - T
                Y.append(Yerlestirme(self.p_dikme, (x, 0, self.sutun_taban),
                                     "x", "z"))

        # aynalı arkalıklar
        for si, k in self.p_ayna.items():
            x0 = self.sutun_x[si]
            if si in getattr(self, "p_sirt", {}):
                z0 = self.baza + self.sutun_toplam[si]
                yy = D - 12 - self.ark - T - 4
            else:
                z0 = self.sutun_kotlar[si][0]
                yy = D - 12 - self.ark - 4
            Y.append(Yerlestirme(k, (x0, yy, z0), "y", "z", renk="#C9D4D8"))

        for si, s in enumerate(self.sutunlar):
            x0 = self.sutun_x[si]
            kotlar = self.sutun_kotlar[si]
            for bi, b in enumerate(s.bolgeler):
                kot = kotlar[bi]
                if bi < len(s.bolgeler) - 1 and si in self.p_ara:
                    Y.append(Yerlestirme(self.p_ara[si],
                                         (x0, 10, kot + b.yukseklik),
                                         "z", "x"))
                if b.tip in ("raf", "acik") and b.raf and si in self.p_raf:
                    if b.raf_kotlari:
                        kl = list(b.raf_kotlari)
                    else:
                        adim = b.yukseklik / (b.raf + 1)
                        kl = [r * adim for r in range(1, b.raf + 1)]
                    for dz in kl:
                        Y.append(Yerlestirme(self.p_raf[si],
                                             (x0 + 1, 12, kot + dz),
                                             "z", "x", renk="#D8C4A0"))
                if b.tip == "cekmece" and si in self.p_cekmece:
                    yuk = b.yukseklik / b.raf
                    for r in range(b.raf):
                        Y.append(Yerlestirme(
                            self.p_cekmece[si],
                            (x0 + 2, -T, kot + r * yuk + 2), "y", "z",
                            renk="#E8DCC8"))

        # kapaklar
        for si, s in enumerate(self.sutunlar):
            if si not in self.p_kapak:
                continue
            k, adet = self.p_kapak[si]
            x0 = self.sutun_x[si] - T + DERZ / 2
            toplam = self.sutun_gen[si] + T
            renk = "#C9D4D8" if s.ayna else "#E8DCC8"
            if adet == 2:
                kg = (toplam - 3 * DERZ / 2) / 2
                for j in range(2):
                    Y.append(Yerlestirme(k, (x0 + j * (kg + DERZ), -T,
                                             self.sutun_taban + DERZ / 2),
                                         "y", "z", renk=renk))
            else:
                Y.append(Yerlestirme(k, (x0, -T, self.sutun_taban + DERZ / 2),
                                     "y", "z", renk=renk))

        if getattr(self, "p_ortak_kapak", None):
            k, adet = self.p_ortak_kapak
            if adet == 2:
                kg = (G - 3 * DERZ) / 2
                for j in range(2):
                    Y.append(Yerlestirme(k, (DERZ + j * (kg + DERZ), -T,
                                             b0 + DERZ / 2), "y", "z",
                                         renk="#E8DCC8"))
            else:
                Y.append(Yerlestirme(k, (DERZ, -T, b0 + DERZ / 2), "y", "z",
                                     renk="#E8DCC8"))

        if self.baza > 0:
            if self.baza_icerlek <= 0.001:
                ic = self.baza_icerlek
                Y.append(Yerlestirme(self.p_baza_on, (0, ic, 0), "y", "x"))
                Y.append(Yerlestirme(self.p_baza_yan, (0, ic + T, 0), "x", "y"))
                Y.append(Yerlestirme(self.p_baza_yan, (G - T, ic + T, 0),
                                     "x", "y"))
            else:
                ic = self.baza_icerlek
                Y.append(Yerlestirme(self.p_baza_on, (T, ic, 0), "y", "x"))
                Y.append(Yerlestirme(self.p_baza_yan, (T, ic, 0), "x", "y"))
                Y.append(Yerlestirme(self.p_baza_yan, (G - 2 * T, ic, 0),
                                     "x", "y"))

        if self.L_govde:
            Y.append(Yerlestirme(self.p_ark, (T - 8, D - 12 - self.ark,
                                              b0 + T - 8), "y", "z",
                                 renk="#8B7355"))
            if self.p_ark2:
                for si, u in enumerate(self.sutun_ust):
                    if u <= 0.001:
                        continue
                    Y.append(Yerlestirme(
                        self.p_ark2,
                        (self.sutun_x[si] - 8, D - 12 - self.ark,
                         b0 + self.sutun_toplam[si] - u - T - 8),
                        "y", "z", renk="#8B7355"))
        else:
            Y.append(Yerlestirme(self.p_ark, (T - 8, D - 12 - self.ark,
                                              b0 + T - 8), "y", "z",
                                 renk="#8B7355"))

    # ---- belge/çizim arayüzü (Dolap ile uyum) ---------------------------
    @property
    def bolgeler(self):
        """belge.py ve uret() için düzleştirilmiş bölge listesi."""
        out = []
        for si, s in enumerate(self.sutunlar):
            for b in s.bolgeler:
                kopya = Bolge(**{f.name: getattr(b, f.name)
                                 for f in b.__dataclass_fields__.values()})
                kopya.ad = f"S{si+1} · {b.ad or b.tip}"
                out.append(kopya)
        return out

    @bolgeler.setter
    def bolgeler(self, v):
        pass

    @property
    def kotlar(self):
        return [k for kl in self.sutun_kotlar for k in kl]

    def raf_delikleri(self):
        s = SISTEM32
        d = []
        y_on, y_arka = s["on_kenar_mesafe"], self.D - s["arka_kenar_mesafe"]
        for si, su in enumerate(self.sutunlar):
            for bi, b in enumerate(su.bolgeler):
                if b.tip not in ("raf", "acik") or not b.raf:
                    continue
                z0 = self.sutun_kotlar[si][bi] - self.baza
                z = z0 + 64.0
                while z < z0 + b.yukseklik - 50:
                    for y in (y_on, y_arka):
                        d.append({"x": z, "y": y, "cap": s["cap"],
                                  "derinlik": s["derinlik"], "tip": "raf_pimi"})
                    z += s["adim"]
        return d

    def cizim_notlari(self):
        n = []
        for br in self.borular:
            y = br.konum[1] + (br.boy / 2 if br.eksen == "y" else 0)
            n.append({"metin": f"Ø{br.cap:g} ASKI BORUSU  L={br.boy:.0f}",
                      "y": y, "z": br.konum[2], "dx": 26.0, "dy": 12.0})
        if self.p_dikme:
            n.append({"metin": f"ORTA DİKME {self.T:g} mm — YAPISAL "
                               f"({self.ic_genislik:.0f} mm açıklık "
                               f"dikmesiz sarkar)",
                      "y": self.D * 0.5, "z": self.govde_yuksekligi * 0.62,
                      "dx": 26.0, "dy": 30.0})
        if self.baza > 0:
            n.append({"metin": f"KAİDE {self.baza:.0f} mm",
                      "y": self.baza_icerlek + self.T / 2, "z": self.baza / 2,
                      "dx": 26.0, "dy": 24.0})
        n.append({"metin": f"ARKALIK {self.ark:g} mm HDF · 4 mm kanal",
                  "y": self.D - 12 - self.ark / 2,
                  "z": self.govde_yuksekligi * 0.3, "dx": 26.0, "dy": 4.0})
        return n

    def render_notlari(self):
        G, T, D = self.G, self.T, self.D
        n = []
        for si, s in enumerate(self.sutunlar):
            x0, sg = self.sutun_x[si], self.sutun_gen[si]
            for bi, b in enumerate(s.bolgeler):
                kot = self.sutun_kotlar[si][bi]
                orta = kot + b.yukseklik / 2
                if b.tip == "aski":
                    a = aski_yonu(self.ic_derinlik, sg)
                    yon = ("kıyafetler öne bakar" if a["yon"] == "x"
                           else "kıyafetler profilden asılır")
                    n.append({"metin": f"{b.ad or 'Askı'} — {yon}",
                              "konum": (x0 + sg / 2, D * 0.45,
                                        kot + b.yukseklik - 55)})
                elif b.tip == "cekmece":
                    n.append({"metin": f"{b.raf} çekmece — teleskopik ray, "
                                       f"tam açılım",
                              "konum": (x0 + sg / 2, 0.0, orta)})
                elif b.tip == "acik":
                    n.append({"metin": f"{b.ad or 'Açık bölme'} — kapaksız",
                              "konum": (x0 + sg / 2, D * 0.4, orta)})
                elif b.tip == "raf" and b.raf:
                    n.append({"metin": f"{b.ad or 'Raflar'} — {b.raf} "
                                       f"ayarlanabilir raf, 32'lik sistem",
                              "konum": (x0 + sg / 2, D * 0.45, orta)})
        if self.p_dikme:
            n.append({"metin": "Orta dikme — yapısal; rafın sarkmasını "
                               "engelleyen şey bu",
                      "konum": (self.sutun_x[1] - T / 2, D * 0.5,
                                self.baza + self.govde_yuksekligi * 0.5)})
        for si, s in enumerate(self.sutunlar):
            if si in self.p_kapak and s.ayna:
                n.append({"metin": "Aynalı kanat — güvenlik filmli 4 mm",
                          "konum": (self.sutun_x[si] + self.sutun_gen[si] / 2,
                                    -T / 2,
                                    self.baza + self.govde_yuksekligi * 0.6)})
        return n

    # ---- rapor -----------------------------------------------------------
    def rapor(self) -> str:
        r = ["=" * 74, f"{self.ad}  [{self.kod}]", "=" * 74]
        if self.aciklama:
            r += [self.aciklama, ""]
        dis_d = self.D + (self.T if self.p_kapak else 0)
        r.append(f"Dış ölçü      : {self.G:.0f} G × {dis_d:.0f} D × "
                 f"{self.H:.0f} Y mm   (gövde {self.D:.0f}, baza {self.baza:.0f})")
        r.append(f"İç ölçü       : {self.ic_genislik:.0f} × "
                 f"{self.ic_derinlik:.0f} mm")
        r.append(f"Malzeme       : {MALZEMELER[self.malzeme].ad} "
                 f"{self.T:g} mm · arkalık {self.ark:g} mm HDF")
        r.append("")
        r.append("-- SÜTUN DÜZENİ " + "-" * 57)
        for si, s in enumerate(self.sutunlar):
            kap = {"tek": "tek kanat", "cift": "çift kanat"}.get(
                s.kapak or (self.kapak_kurali if self.kapak_kurali == "sutun"
                            else None) or "", "KAPAKSIZ")
            if self.kapak_kurali == "sutun" and not s.kapak:
                kap = "tek kanat"
            r.append(f"  S{si+1} · {(s.ad or ''):22s} "
                     f"net {self.sutun_gen[si]:6.0f} mm  [{kap}"
                     + (" · AYNALI" if s.ayna else "") + "]")
            for bi, b in enumerate(s.bolgeler):
                kot = self.sutun_kotlar[si][bi]
                ek = (f" · {b.raf} raf" if b.raf and b.tip != "cekmece"
                      else f" · {b.raf} çekmece" if b.raf else "")
                r.append(f"       {(b.ad or b.tip):24s} kot {kot:6.0f} → "
                         f"{kot + b.yukseklik:6.0f}   net {b.yukseklik:5.0f} mm{ek}")
                if b.not_:
                    r.append(f"         {b.not_}")
        r.append("")
        r.append("-- KAPASİTE " + "-" * 61)
        for ad, c in self.detay:
            r.append(f"  {ad:34s} {c}")
        r.append("")
        r.append("-- YAPISAL KONTROL " + "-" * 54)
        s_ = self.sehim
        r.append(f"  Sütun açıklığı: {s_['aciklik_mm']:.0f} mm → sehim "
                 f"{s_['sehim_mm']} mm (sünmeyle {s_['sehim_sunmeli_mm']} mm) "
                 f"= {s_['oran']}  [limit {s_['limit']}]  "
                 f"{'UYGUN' if s_['uygun'] else 'AŞIYOR'}")
        r.append(f"  Maks. açıklık : {self.max_ack:.0f} mm  ·  dikmesiz iç "
                 f"genişlik {self.ic_genislik:.0f} mm "
                 f"{'AŞARDI' if self.ic_genislik > self.max_ack else ''}")
        d = self.devrilme
        r.append(f"  Devrilme      : h={d['yukseklik_mm']:.0f} mm · "
                 f"m={d['kutle_kg']} kg · h_cg×m={d['h_cg_m_x_kg']} (eşik 6) "
                 f"→ {'TEST GEREKLİ' if d['stabilite_testi_gerekli'] else 'tetik yok'}")
        r.append(f"                  {d['aciklama']}")
        if self.donanim:
            r.append("")
            r.append("-- DONANIM " + "-" * 62)
            for kod, ad, olcu, adet, notu in self.donanim:
                r.append(f"  {kod:12s} {ad:36s} {olcu:>9s} × {adet}"
                         + (f"   {notu}" if notu else ""))
        if self.uyarilar:
            r.append("")
            r.append("-- UYARILAR " + "-" * 61)
            for u in self.uyarilar:
                r.append(f"  ! {u}")
        r.append("")
        r.append(ozet_rapor(self.parcalar))
        return "\n".join(r)
