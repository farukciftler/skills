#!/usr/bin/env python3
"""
pt.py - Portfoy Tahmin Gunlugu defteri.

Deterministik kayit katmani. Internete CIKMAZ, fiyat CEKMEZ, tahmin URETMEZ.
Fiyatlari ve tahminleri Claude web search ile toplayip buraya besler;
bu script sadece saklar, eslestirir ve olcer.

Alt komutlar:
  init         Veri kokunu olustur
  add-asset    Portfoye varlik ekle / guncelle
  list-assets  Portfoyu goster
  snapshot     Gunun fiyatlarini ve portfoy degerini kaydet
  forecast     Tahmin kaydi ekle
  resolve      Vadesi gelen tahminleri gerceklesenle eslestir
  report       Sabah raporu icin baglam paketi (JSON)
  calibrate    Kalibrasyon metrikleri
  note         Gunun gundem notunu evidence/ altina yaz
  flow         Var olan snapshot'a nakit akisi (yatirma/cekme) isle
  holdings     Fonlarin ic varlik dagilimini (look-through) kaydet
  lookthrough  Fon iclerini acarak portfoy geneli gercek maruziyeti hesapla
"""

import argparse
import json
import math
import os
import signal
import statistics
import sys

try:  # `| head` gibi kullanimlarda BrokenPipeError gurultusu olmasin
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass
from datetime import date, datetime, timedelta
from pathlib import Path

ASSET_CLASSES = ("spot", "fund_tefas", "accrual", "equity", "crypto")
FORECASTABLE = ("spot", "fund_tefas", "equity", "crypto")

# Piyasanin KAPALI oldugu gune tahmin hedeflenemez.
#
# Kapali gunun snapshot'i yeni fiyat tasimaz, onceki gunun fiyatini TASIR.
# Boyle bir gune hedeflenmis tahmin garantili %0,000 degisimle cozulur: bant
# her zaman tutar, yon her zaman "yatay" olur, MAE yapay olarak kucuk cikar.
# Bu bir kayip gozlem degil, KIRLI gozlemdir - ve rastgele dagilmaz, sistematik
# olarak Cuma/tatil oncesi tahminlere carpar.
#
# Ilk ornek: 01.08 (Cmt) -> 02.08 (Paz) gram_altin 1g, gerceklesen %0,000
# (6174,455 -> 6174,460, yani sifir). reviews/2026-08.md -> K17.
#
# Kural (kullanici talimati, 07.08.2026): hedef tarih, o varligin GERCEKTEN
# FIYATLANDIGI ilk gune kaydirilir. Cuma gunu uretilen 1g tahmini Pazartesi'yi
# hedefler; hedef bir resmi tatile denk gelirse tatil sonrasi ilk seansa kayar.
ALWAYS_OPEN_CLASSES = ("crypto",)  # 7/24 islem gorur, kaydirma yok

# Borsa Istanbul Pay Piyasasi tatil tablosu - SEANS YAPILMAYAN gunler.
# KAYNAK: borsaistanbul.com/files/pay-piyasasi-<YIL>-yili-tatil-tablosu.pdf
# (birincil kaynak, PDF'ten okundu 07.08.2026).
#
# Arife gunleri (19.03, 26.05, 28.10) YARIM GUN seans yapilir -> ACIK sayilir,
# fiyat olusur, listeye girmez.
#
# Neden tek takvim: portfoydeki her kalem TL cinsinden ve Turkiye'de sakli
# (fonlar TEFAS, ZPE BIST, gram altin Kapalicarsi, doviz katilim banka).
# Resmi tatilde TL bacagi hepsinde kapali. USD/TRY offshore islem gorse bile
# serbest piyasa kotasyonu tatilde bayattir - kaydirmak, bayat fiyata karsi
# cozumlemekten her durumda iyidir.
MARKET_HOLIDAYS = {
    "2026-01-01",  # Yilbasi
    "2026-03-20", "2026-03-21", "2026-03-22",  # Ramazan Bayrami
    "2026-04-23",  # Ulusal Egemenlik ve Cocuk Bayrami
    "2026-05-01",  # Emek ve Dayanisma Gunu
    "2026-05-19",  # Ataturk'u Anma, Genclik ve Spor Bayrami
    "2026-05-27", "2026-05-28", "2026-05-29", "2026-05-30",  # Kurban Bayrami
    "2026-07-15",  # Demokrasi ve Milli Birlik Gunu
    "2026-08-30",  # Zafer Bayrami
    "2026-10-29",  # Cumhuriyet Bayrami
}
# Takvimin kapsadigi son gun. Bunun otesine tasan bir hedef tarih icin motor
# UYARIR - sessizce "acik" varsaymaz. Yeni yilin tablosu yayinlaninca
# MARKET_HOLIDAYS'e ekle ve bu tarihi ilerlet.
MARKET_CALENDAR_THROUGH = "2026-12-31"

HORIZON_DAYS = {"1d": 1, "1w": 7, "1m": 30}
RESOLVE_GRACE_DAYS = 6  # bu kadar gun sonra hala snapshot yoksa veri_yok
# |gerceklesen %| bunun altindaysa hareket "yatay" sayilir ve YON skorlamasina
# girmez (MAE/bant hesabina girer). Tipik gunluk oynaklik %0,8-2,0 oldugundan
# %0,05 gurultu tabanidir. 2026-08-02'de eklendi, gerekce: reviews/2026-08.md K5
DIRECTION_DEADZONE_PCT = 0.05

# Protokol surumu. Bant genisligi tablosu, tahmin modeli veya skorlama kurali
# degisirse BURAYI ARTIR ve degisikligi reviews/ altina yaz. Sebep: kalibrasyon
# ancak sabit protokol altinda havuzlanabilir; 4 gunde 3 revizyon yasandi
# (K7/K9/K10) ve surum alani olmadan hangi satirin hangi kurala gore uretildigi
# geriye donuk ayirt edilemiyordu. Farkli surumler AYNI havuzda toplanmaz.
#
# v2 (07.08.2026): hedef tarih artik varligin fiyatlandigi ILK acik gune
# kaydiriliyor (next_open_day). v1'de bu yalnizca fund_tefas/equity icin
# yapiliyordu; `spot` varliklar hafta sonuna hedeflenebiliyor ve garantili %0
# degisimle cozuluyordu. Ufkun TANIMI degisti (Cuma 1g = Pazartesi, 3 takvim
# gunu), dolayisiyla v1 ve v2 satirlari ayni havuzda toplanamaz. -> K17
# v3 (10.08.2026): TEFAS fon degerleme modeli degisti. "Model A" (NAV(D) <- ABD
#   seansi D-1) 10.08'de dort fonda birden REDDEDILDI; dogru model NAV(D) <- D
#   gununun KENDI seansi, T+1 yayin. Sonuc: fon 1g tahminleri artik kapanmis bir
#   seansin muhasebesi degil, ACIK bir seansin tahmini -> bantlar genisledi,
#   p_up 0,50'ye dondu. v2 ve oncesi fon satirlari bu havuza KATILAMAZ.
#   Ayrica 1h bantlari genisletildi (v1-v2'de 1h bant kapsamasi 5/9 basarisiz,
#   tamami yukari yonlu). Ayrinti: data/reviews/2026-08.md -> K22.
# v4 (13.08.2026): NOKTA URETME KURALI DEGISTI - "disaridan iceriye".
#   Sebep: v3'te belirleyici kanit yoksa nokta SIFIR yaziliyordu. 12.08'de bu
#   politika alti satirin ALTISINDA da uc baseline'i birden kaybetti - cunku
#   sifir tahmin, varligin KENDI gozlenen dagilimini (referans sinif) yok
#   sayiyor. Superforecasting literaturunun en guclu tek teknigi bunun tersi:
#   once disarisi (base rate), sonra ic goru duzeltmesi.
#   Yeni kural:  point = SHRINK * referans_sinif_ortalamasi + ic_goru
#   SHRINK = 0,3 (kucuk orneklem + rejim yanliligi icin agir kirpma).
#   p_up    = 0,50 + 0,3 * (referans_p_up - 0,50), 1g icin [0,40; 0,60] sinirli.
#   Tahmin dosyalarina `reference_class`, `base_rate_pct`, `base_rate_p_up` ve
#   `inside_view_adjustment` alanlari eklendi - ic goru duzeltmesinin kendisi
#   ayrica olculebilsin diye (Brier'i iyilestiriyor mu, yoksa gurultu mu).
#   MALIYET: havuz yeniden bolunuyor ve v3'te yalnizca ~12 satir vardi. Guc
#   kaybi kabul edildi cunku nokta uretme kurali skorun DOGRUDAN belirleyicisi.
PROTOCOL_VERSION = 4
# --- MODEL DAMGASI (02.09.2026, K78) ---
# Tahmini ureten Anthropic modelinin kimligi. PROTOCOL_VERSION bant/skor
# kurallarini ayirir ama MODELI ayirmiyordu: 01.08-01.09 arasi tum tahminler
# Opus 5 ile uretildi, 02.09'da oturum Fable 5.1'e gecti ve dosyada bunu
# ayirt edecek hicbir alan yoktu. "LLM sinyali deger katiyor mu" sorusu
# hangi LLM'in olculdugu bilinmeden cevaplanamaz; alan geriye donuk
# doldurulamaz (market_state ile ayni sinif). Motor bu alani ZORUNLU tutar:
# her tahmin kaleminde `model_id` olmali (payload ust duzeyinde verilirse
# tum kalemlere yayilir; --model-id de kabul edilir). Motor modeli KENDISI
# BILEMEZ - onu calistiran oturum bildirmek zorunda; bu yuzden sorulur.
MODEL_ID_REQUIRED = True

# Gun tipi. Kalibrasyonu ayirmak icin: veri gunu ile sakin gunun oynakligi ayni
# degildir, ikisini tek havuzda olcmek hem bant kapsamasini hem yon isabetini
# bulaniklastirir. `veri` = onceden takvimi belli, sayisal, fiyat hareket
# ettiren bir aciklama var (TUFE, istihdam, FOMC, TCMB).
DAY_TYPES = ("veri", "sakin", "tatil", "hafta_sonu")

# Ufka gore cikti etiketi. 1 aylik ufukta ortusmeyen gozlem yilda ~12 tanedir;
# %55'lik bir edge'i olcmek 21 yil surer. Yani 1a ciktisi OLCULEBILIR bir tahmin
# degildir - projeksiyondur ve rapor dilinde oyle anilir.
HORIZON_KIND = {"1d": "tahmin", "1w": "tahmin", "1m": "projeksiyon"}

# --------------------------------------------------------------- baseline'lar
# "Degismez" (%0) baseline TEK BASINA yaniltici: tek yonlu bir piyasada kucuk
# pozitif bir nokta tahmini onu MEKANIK olarak yener. 12.08.2026'da olculdu:
# 1h gerceklesmelerin %100'u pozitif, ortalama +%5,8; tahminlerin %77,9'u
# pozitif. Yani "baseline yenildi" sonucunun ne kadari beceri, ne kadari rejim
# belli degildi. Iki ZOR baseline eklendi (13.08.2026):
#
#   naif     : %0 degisim              - hareketsizlik
#   drift    : son K gozlenen degisimin ORTALAMASI x adim  - trend takibi
#   momentum : son 1 gozlenen degisim x adim               - dun ne olduysa o
#
# Ucu de YALNIZCA as_of anindaki bilgiyi kullanir (sizinti yok); adim sayisi
# cozumleme aninda gozlenen fiyat degisimi sayisidir, fiyatin kendisi degil.
# Birincil metrik artik "UC baseline'i da yenmek". Sadece naifi yenmek,
# trend rejiminde bilgi tasimaz.
BASELINE_DRIFT_LOOKBACK = 5
BASELINE_KINDS = ("naif", "drift", "momentum")

# Her gun doldurulmasi beklenen makro degiskenler. Eksikse `forecast` uyarir.
# Bunlar GERIYE DONUK DOLDURULAMAZ (gun ici seviyeler kaynaklarda kalmaz);
# "hangi makro degisken neyi surukluyordu" sorusu tamamen bu alana bagli.
MARKET_STATE_REQUIRED = ("usdtry", "xauusd", "dxy", "us10y", "nasdaq", "bist100", "brent")

# Tahmin DOSYASININ ust duzeyinde motorun tanidigi alanlar (acik is #26, K52).
# Tahmin ICINDEKI alanlar icin beyaz liste zaten vardi; dosya duzeyinde yoktu
# ve 20.08'de `band_shadow_notu` sessizce kayboldu. Kural: tanimadigi alani
# motor DUSURMEZ, dosyaya aynen yazar ve UYARIR - kayip sessiz olmamali.
FORECAST_FILE_FIELDS = ("as_of", "forecasts", "evidence", "evidence_patch",
                        "market_state", "day_type", "scheduled_events",
                        "protocol_version", "reason", "superseded",
                        "kontroller", "created_at", "updated_at",
                        "model_id")   # K78: payload ust duzeyi, kalemlere yayilir

# H8 PAYDASI (on-kayit 13.08.2026; 01.09'a kadar HIC yazilmadi -> K77).
# "Mekanizma X hatalari iyi yakaliyor" demek icin X'in kac gun CALISTIRILDIGI
# bilinmeli. Her gun tahmin dosyasina `kontroller: [...]` yazilir; sozluk
# hata_gunlugu.csv'nin `mekanizma_k` sutunuyla AYNIDIR ki pay/payda eslesin.
# Payda sayimi H8_PAYDA_BASLANGIC'tan baslar - geriye donuk doldurulmaz,
# cunku "o gun mutabakat yapildi mi" dosyalardan cikarsanabilir ama
# cikarsama tespit degildir.
KONTROL_MEKANIZMALARI = ("capraz_kontrol", "mutabakat", "banka_ekrani", "kullanici",
                         "motor_uyarisi", "ertesi_gozlem", "akil_yurutme",
                         "rutin_akis", "on_kayitli_test",
                         # K80 (03.09.2026): `tahmin-savcisi` skill'i - commit
                         # oncesi adversaryal denetim. AYRI bir mekanizma olarak
                         # eklendi cunku H8'in sordugu sey "hangi mekanizma verimli
                         # yakaliyor"; `rutin_akis` icine gomulurse savcinin kendi
                         # verimi HIC olculemez. Paydasi da ayni sozlukten sayilir:
                         # `kontroller` listesine yazildigi gun sayisi.
                         "savci")
H8_PAYDA_BASLANGIC = "2026-09-01"

# H4 PAYDASI (K79, 03.09.2026). `scheduled` bir kanit `consensus` ile aciliyor
# ve veri gelince `actual` ile kapaniyor - ama KAPANMAYI HATIRLATAN HICBIR SEY
# YOKTU. 03.09'da olculdu: 41 takvimli kayittan 21'i kapanmis, **20'si acik**;
# acik olanlarin 17'sinin olay tarihi coktan gecmisti (NVDA bilancosu, cekirdek
# PCE, Philly Fed, flash PMI'lar...). Surpriz hesaplanamayan olay H4'un
# paydasina GIREMIYOR ve eksiklik gorunmuyordu.
# Kayip RASTGELE DEGIL: kapanan kayitlar "o gun hatirlanan" olaylardir.
# `event_date` alani da burada dogdu: olayin tarihi yalnizca `claim` metninde
# duruyordu, yani makineyle takip edilemiyordu. Yeni kayitlarda ZORUNLU DEGIL
# ama yokken takip sezgisele dusuyor (as_of + ACIK_KANIT_GRACE).
ACIK_KANIT_GRACE_GUN = 3

# Bir tahminin PUANLANAN alanlari. Ayni (asset, horizon) yeniden gonderildiginde
# bunlardan biri degismisse bu bir REVIZYONDUR (acik is #13): eski kayit
# `superseded` altina tasinir ve gerekce zorunludur. Degismemisse (or. sadece
# band_shadow eklendi) sessiz guncellemedir. Cozulmus tahmin ASLA revize edilmez.
FORECAST_SCORED_FIELDS = ("target_date", "point_pct", "low_pct", "high_pct", "p_up")


# ------------------------------------------------------- istatistik yardimcilari
# scipy yok; gereken testler standart kutuphaneyle tam (exact) hesaplaniyor.

def _binom_cdf(k, n, p):
    """P(X <= k), X ~ Binom(n, p). Tam toplam."""
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(0, k + 1))


def binom_test_greater(k, n, p0=0.5):
    """Tek yonlu tam binom testi: H0 p=p0, H1 p>p0. P(X >= k)."""
    if n == 0:
        return None
    # 6 hane: 4 hanede p<0,00005 "0.0" gorunuyordu; README bunu "<0,0001"
    # diye basar ama JSON'da sifir yanlistir (K76 ile birlikte, 01.09.2026).
    return round(1.0 - _binom_cdf(k - 1, n, p0) if k > 0 else 1.0, 6)


def binom_test_two_sided(k, n, p0=0.5):
    """Cift yonlu tam binom testi (esit-veya-daha-az-olasi kuyruklar)."""
    if n == 0:
        return None
    obs = math.comb(n, k) * p0**k * (1 - p0)**(n - k)
    tot = 0.0
    for i in range(n + 1):
        pi = math.comb(n, i) * p0**i * (1 - p0)**(n - i)
        if pi <= obs * (1 + 1e-9):
            tot += pi
    return round(min(1.0, tot), 6)


def wilson_ci(k, n, z=1.96):
    """Oran icin Wilson skor guven araligi. Kucuk n'de normal yaklasimdan cok
    daha durust - n=9'da normal CI araligi [0,1] disina tasar."""
    if n == 0:
        return None
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 3), round(min(1.0, c + h), 3)]


def mean_ci(xs, z=1.96):
    """Ortalama icin normal yaklasimla CI. n<8 ise None - yaklasim tutmaz."""
    n = len(xs)
    if n < 8:
        return None
    sd = statistics.stdev(xs)
    h = z * sd / math.sqrt(n)
    return [round(statistics.fmean(xs) - h, 4), round(statistics.fmean(xs) + h, 4)]

# Look-through kanonik varlik siniflari. Fonlarin TEFAS'ta gosterdigi satir
# adlari fondan fona degisir ("BIST Taahhutlu Islem Pazari Satim", "Katilma
# Hesabi TL", "Mevduat" hepsi nakit benzeridir); ESLEME CLAUDE'UN ISIDIR ve
# holdings dosyasina kanonik anahtarlarla yazilir. Motor sadece toplar.
# Ham TEFAS satirlari `allocation_raw` altinda aynen saklanir - esleme yanlissa
# geriye donuk duzeltilebilsin diye.
LOOKTHROUGH_CLASSES = (
    "yabanci_hisse",     # ABD/global hisse ve hisse BYF'leri
    "yurtici_hisse",     # BIST hissesi
    "kiymetli_maden",    # altin/gumus, kiymetli maden BYF'leri
    "sukuk_tl",          # TL kira sertifikasi
    "sukuk_altin",       # kiymetli maden cinsinden kira sertifikasi
    "nakit_tl",          # katilma hesabi, mevduat, BIST taahhutlu islem
    "nakit_doviz",       # USD/EUR bakiye
    "belirsiz",          # fon icinde fon - icerigi acilmadi
)


def _blank_exposure():
    return {c: 0.0 for c in LOOKTHROUGH_CLASSES}


# ---------------------------------------------------------------- yardimcilar

def parse_date(s):
    if s is None:
        return date.today()
    return datetime.strptime(s, "%Y-%m-%d").date()


def is_market_open(d):
    """TR piyasasi o gun fiyat uretiyor mu? (hafta ici + tatil disi)"""
    return d.weekday() < 5 and d.isoformat() not in MARKET_HOLIDAYS


def next_open_day(d, cls=None):
    """Hedef tarihi, varligin fiyatlandigi ILK gune kaydirir.

    `crypto` 7/24 islem gorur -> kaydirma yok. Diger her sinif TR piyasa
    takvimine bagli: Cuma + 1 gun = Cumartesi degil PAZARTESI; tatile denk
    gelen hedef tatil sonrasi ilk seansa kayar.
    """
    if cls in ALWAYS_OPEN_CLASSES:
        return d
    guard = 0
    while not is_market_open(d):
        d += timedelta(days=1)
        guard += 1
        if guard > 14:  # 4 gunluk bayram + hafta sonu bile 14'u gecmez
            raise SystemExit(f"takvim dongusu: {d} icin acik gun bulunamadi")
    return d


def next_business_day(d):  # geriye donuk uyumluluk
    return next_open_day(d)


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(p)


def write_jsonl(path, rows):
    """JSONL dosyasini ATOMIK yeniden yaz (tmp + replace).

    `write_json` bastan beri atomikti ama JSONL yeniden yazmalari duz
    `open(..., "w")` kullaniyordu. Bu, deponun EN DEGERLI dosyasini
    (`resolutions.jsonl`, 425 muhurlenmis gozlem) her `resolve`/`baselines`
    /`model-stamp` cagrisinda risk altina sokuyordu: yazma sirasinda kesinti
    (Ctrl-C, disk dolmasi, surec olumu) dosyayi YARIM birakir.

    `resolve` cogunu yeniden uretebilir ama `resolved_at` damgalari ve
    append-only garantisi geri gelmez - ve garanti bu deponun temel iddiasi.
    07.09.2026'da bulundu (teknik denetim).
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(p)


def append_jsonl(path, row):
    """Tek satir ekle. Ekleme zaten atomik sayilir (kucuk, tek write)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def die(msg):
    print(f"HATA: {msg}", file=sys.stderr)
    sys.exit(1)


class Store:
    def __init__(self, root):
        self.root = Path(os.path.expanduser(root))
        self.portfolio_path = self.root / "portfolio.json"
        self.snapshots = self.root / "snapshots"
        self.forecasts = self.root / "forecasts"
        self.evidence = self.root / "evidence"
        self.reviews = self.root / "reviews"
        self.holdings = self.root / "holdings"
        self.resolutions = self.root / "resolutions.jsonl"
        # K92 (07.09.2026): karar defteri. Tahminler olculuyordu, KARARLAR
        # olculmuyordu - oysa para kararla hareket ediyor.
        self.decisions = self.root / "decisions.jsonl"

    def ensure(self):
        for d in (self.snapshots, self.forecasts, self.evidence, self.reviews,
                  self.holdings):
            d.mkdir(parents=True, exist_ok=True)

    def holdings_path(self, d):
        return self.holdings / f"{d.isoformat()}.json"

    def latest_holdings(self, on_or_before=None):
        """En guncel look-through kaydi. Fon dagilimlari gunluk degismez -
        aylik cekilir - bu yuzden 'o gune ait dosya' degil 'o gune kadarki en
        yeni dosya' dogru olandir."""
        files = sorted(self.holdings.glob("*.json"))
        for f in reversed(files):
            d = date.fromisoformat(f.stem)
            if on_or_before is None or d <= on_or_before:
                return d, read_json(f)
        return None, None

    def portfolio(self):
        p = read_json(self.portfolio_path)
        if p is None:
            die(f"portfolio.json yok. Once: pt.py init --root {self.root}")
        return p

    def save_portfolio(self, p):
        write_json(self.portfolio_path, p)

    def snapshot_path(self, d):
        return self.snapshots / f"{d.isoformat()}.json"

    def snapshot(self, d):
        return read_json(self.snapshot_path(d))

    def latest_snapshot(self, on_or_before=None):
        files = sorted(self.snapshots.glob("*.json"))
        for f in reversed(files):
            d = date.fromisoformat(f.stem)
            if on_or_before is None or d <= on_or_before:
                return d, read_json(f)
        return None, None

    def price_series(self, asset, cls=None):
        """[(date, fiyat)] - GERCEK gozlemler, tarihe gore sirali.

        Iki eleme yapilir, ikisi de ayni sebeple: bir "gozlem" yalnizca piyasa
        o gun fiyat urettiyse gozlemdir.

        1. `prices[asset] is None` -> deger tasinmis, fiyat yok (hafta sonu fon).
        2. Piyasanin KAPALI oldugu gun -> gram altin ve USD/TRY icin hafta sonu
           snapshot'ina donmus Cuma kotasyonu YAZILIYOR, yani fiyat None degil
           ama YENI bilgi de degil. Bunlari seriye almak %0'lik sahte gunler
           uretir ve drift/momentum baseline'larini sifira dogru cekerdi -
           yani baseline'i KOLAYLASTIRIR, LLM'in isini haksiz yere kolaylastirir.
           13.08.2026'da tam bu kusur bulundu: gram altin serisinde 08-08 -> 08-09
           gecisi %0,0 olarak drift ortalamasina giriyordu.
        `crypto` 7/24 islem gorur, onda 2. eleme uygulanmaz.
        """
        out = []
        for f in sorted(self.snapshots.glob("*.json")):
            snap = read_json(f)
            px = (snap or {}).get("prices", {}).get(asset)
            if px is None:
                continue
            d = date.fromisoformat(f.stem)
            if cls not in ALWAYS_OPEN_CLASSES and not is_market_open(d):
                continue
            out.append((d, float(px)))
        return out

    def all_forecast_files(self):
        return sorted(self.forecasts.glob("*.json"))

    def all_decisions(self):
        if not self.decisions.exists():
            return []
        return [json.loads(l) for l in
                self.decisions.read_text(encoding="utf-8").splitlines() if l.strip()]

    def all_resolutions(self):
        if not self.resolutions.exists():
            return []
        rows = []
        with self.resolutions.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows

    def append_resolutions(self, rows):
        self.resolutions.parent.mkdir(parents=True, exist_ok=True)
        with self.resolutions.open("a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- komutlar

def cmd_init(args):
    st = Store(args.root)
    st.ensure()
    if st.portfolio_path.exists():
        out({"ok": True, "mesaj": "zaten var", "root": str(st.root)})
        return
    st.save_portfolio({
        "base_currency": args.currency,
        "created_at": now_iso(),
        "assets": {},
    })
    out({"ok": True, "root": str(st.root), "olusturuldu": True})


def cmd_add_asset(args):
    st = Store(args.root)
    st.ensure()
    p = st.portfolio()
    if args.asset_class not in ASSET_CLASSES:
        die(f"gecersiz class. Secenekler: {', '.join(ASSET_CLASSES)}")
    if args.quantity is None and args.value is None and args.id not in p["assets"]:
        # YENI varlik icin miktar/deger zorunlu. MEVCUT varlikta degilse:
        # add-asset ayni zamanda GUNCELLEME komutu ve `accrual` varliklarin
        # (katilma/cari hesap) ne miktari ne degeri vardir - bakiye
        # snapshot'tan gelir. Zorunluluk korunursa `accrual_apr` gibi bir
        # parametre CLI uzerinden HIC guncellenemez ve JSON elle duzenlenmek
        # zorunda kalinir; CLAUDE.md'nin acikca yasakladigi sey budur.
        # 22.08.2026, K56.
        die("--quantity veya --value verilmeli (yeni varlik)")

    existing = p["assets"].get(args.id, {})
    asset = {
        "label": args.label or existing.get("label") or args.id,
        "class": args.asset_class,
        "unit": args.unit or existing.get("unit"),
        "quantity": args.quantity if args.quantity is not None else existing.get("quantity"),
        "value_try": args.value if args.value is not None else existing.get("value_try"),
        "price_source": args.price_source or existing.get("price_source"),
        "custodian": args.custodian or existing.get("custodian"),
        "since": args.since or existing.get("since"),
        "accrual_apr": args.accrual_apr if args.accrual_apr is not None else existing.get("accrual_apr"),
        "lookthrough": existing.get("lookthrough"),
        "notes": args.notes or existing.get("notes", ""),
        "updated_at": now_iso(),
    }
    if args.lookthrough:
        lt = json.loads(args.lookthrough)
        bad = [k for k in lt if k not in LOOKTHROUGH_CLASSES]
        if bad:
            die(f"taninmayan look-through sinifi {bad}. "
                f"Gecerli olanlar: {', '.join(LOOKTHROUGH_CLASSES)}")
        asset["lookthrough"] = lt
    if args.quantity is not None:
        asset["value_try"] = None  # miktar otoriter
    p["assets"][args.id] = asset
    st.save_portfolio(p)
    out({"ok": True, "asset": args.id, "kayit": asset})


def cmd_remove_asset(args):
    st = Store(args.root)
    p = st.portfolio()
    if args.id not in p["assets"]:
        die(f"{args.id} portfoyde yok")
    removed = p["assets"].pop(args.id)
    st.save_portfolio(p)
    out({"ok": True, "silindi": args.id, "kayit": removed})


def cmd_list_assets(args):
    st = Store(args.root)
    p = st.portfolio()
    d, snap = st.latest_snapshot()
    rows = []
    total = 0.0
    for aid, a in p["assets"].items():
        val = (snap or {}).get("values", {}).get(aid)
        if val is None:
            val = a.get("value_try")
        if val:
            total += val
        rows.append({
            "id": aid, "label": a["label"], "class": a["class"],
            "quantity": a.get("quantity"), "deger_try": val,
            "tahmin_edilebilir": a["class"] in FORECASTABLE,
        })
    for r in rows:
        r["agirlik_pct"] = round(100 * r["deger_try"] / total, 1) if (total and r["deger_try"]) else None
    rows.sort(key=lambda r: r["deger_try"] or 0, reverse=True)
    out({"toplam_try": round(total, 2), "son_snapshot": d.isoformat() if d else None, "varliklar": rows})


def _parse_flows(raw, assets):
    """--flows JSON'unu dogrula. Isaret kurali: + para yatirma, - para cekme.

    Nakit akisi fiyat hareketi DEGILDIR; kaydedilmezse "28k cektim" gunu
    portfoy -%2,4 dusmus gibi gorunur ve getiri serisi kirlenir. Akislar
    snapshot'a yazilir, akistan arindirilmis gunluk getiri ayrica hesaplanir.
    """
    if not raw:
        return {}
    flows = json.loads(raw) if isinstance(raw, str) else raw
    for aid, amt in flows.items():
        if aid not in assets:
            die(f"flow icin bilinmeyen varlik: {aid}")
        if not isinstance(amt, (int, float)) or amt == 0:
            die(f"{aid} icin flow sifir olmayan sayi olmali (+yatirma/-cekme), gelen: {amt!r}")
    return flows


def _flow_fields(total, prev_total, flows):
    """Akis alanlarini hesapla. Getiri formulu (gun sonu akis varsayimi):
    r = ((total - net_flow) - prev_total) / prev_total"""
    net = round(sum(flows.values()), 2) if flows else 0.0
    adj = (round(100 * ((total - net) - prev_total) / prev_total, 4)
           if prev_total else None)
    return {"flows": flows or {}, "net_flow_try": net, "delta_flow_adj_pct": adj}


def cmd_snapshot(args):
    st = Store(args.root)
    st.ensure()
    p = st.portfolio()
    d = parse_date(args.date)

    prices = json.loads(args.prices) if args.prices else {}
    if args.prices_file:
        prices.update(read_json(args.prices_file, {}))
    flows = _parse_flows(args.flows, p["assets"])

    prev_date, prev = st.latest_snapshot(on_or_before=d - timedelta(days=1))
    prev_values = (prev or {}).get("values", {})
    prev_prices = (prev or {}).get("prices", {})

    values, used_prices, warnings = {}, {}, []
    dirty_portfolio = False

    for aid, a in p["assets"].items():
        # Varlik henuz edinilmemisse gecmis snapshot'ta hic bulunmamali. Yoksa
        # value_try fallback'i onu geriye dogru tasir ve portfoy degeri de,
        # getiri serisi de sisar.
        since = a.get("since")
        if since and d < date.fromisoformat(since):
            continue

        price = prices.get(aid)
        if price is not None and not isinstance(price, (int, float)):
            die(f"{aid} icin fiyat sayi olmali, gelen: {price!r}")
        used_prices[aid] = price
        cls = a["class"]

        if cls == "accrual":
            base = prev_values.get(aid, a.get("value_try") or 0.0)
            apr = a.get("accrual_apr")
            if prices.get(aid) is not None:
                # Gercek bakiye her seyi ezer. Projeksiyon ona yenilenir.
                values[aid] = round(prices[aid], 2)
                continue
            if apr and prev_date:
                if d.weekday() >= 5:
                    # Hafta sonu: katilma hesabina kar payi YAZILMAZ. Birikim
                    # takvim gunu uzerinden hesaplanir ama ilk is gunu kredilenir
                    # (Cuma -> Pazartesi = 3 gun, Pazartesi'de yazilir).
                    # Bu yapilmazsa veri setine "hafta sonu = her zaman pozitif"
                    # diye sahte bir duzenlilik girer ve model onu ogrenir.
                    warnings.append(f"{aid}: hafta sonu - kar payi yazilmadi, "
                                    f"onceki deger tasindi (birikim Pazartesi kredilenir)")
                    values[aid] = round(base, 2)
                    continue
                # Son IS GUNU snapshot'ini bul; hafta sonu gunleri atlanir ki
                # Pazartesi'de birikmis takvim gunlerinin tamami yazilsin.
                #
                # ⚠ BURADAN SADECE **GUN SAYISI** ALINIR, **BAZ ALINMAZ.**
                # Baz daima EN GUNCEL bakiyedir (`prev_values`), cunku hafta sonu
                # snapshot'i gercek bakiye guncellemesi VEYA para cekimi tasiyabilir.
                # Cuma'nin bakiyesine donmek o hareketi SESSIZCE SILER.
                # K45 (17.08.2026): motor 16.08 Paz (33.565,08) yerine 14.08 Cum
                # (42.046,24) bazini aldi; hafta sonu cekilen 8.481 TL yok oldu ve
                # portfoy 8.623 TL sisti. Gecmiste tetiklenmemisti cunku 03.08 ve
                # 10.08 Pazartesilerinde elle GERCEK BAKIYE verilmis, accrual dali
                # hic calismamisti - yani hata 16 gun boyunca sessizce bekledi.
                credit_date = prev_date
                probe = prev_date
                while probe and probe.weekday() >= 5:
                    probe, _ = st.latest_snapshot(on_or_before=probe - timedelta(days=1))
                    if probe is None:
                        break
                    credit_date = probe
                if credit_date is None or credit_date.weekday() >= 5:
                    # Hic is gunu snapshot'i yok (sistem hafta sonu baslamis).
                    first = sorted(st.snapshots.glob("*.json"))
                    if first:
                        credit_date = date.fromisoformat(first[0].stem)
                        warnings.append(f"{aid}: hic is gunu snapshot'i yok, birikim ilk "
                                        f"snapshot'tan ({credit_date}) itibaren sayiliyor")
                    else:
                        credit_date = prev_date
                days = (d - credit_date).days
                base = base * (1 + (apr / 100.0) * days / 365.0)
                warnings.append(f"{aid}: birikim projeksiyonu ({days} takvim gunu "
                                f"{credit_date} -> {d}, %{apr} yillik) - gercek bakiye degil")
            values[aid] = round(base, 2)
            continue

        qty = a.get("quantity")
        if qty is None and a.get("value_try") is not None and price:
            qty = a["value_try"] / price
            p["assets"][aid]["quantity"] = round(qty, 6)
            p["assets"][aid]["implied_from"] = {"value_try": a["value_try"], "price": price, "date": d.isoformat()}
            p["assets"][aid]["value_try"] = None
            dirty_portfolio = True
            warnings.append(f"{aid}: {round(qty, 4)} birim olarak turetildi (fiyat {price})")

        if qty is not None and price:
            values[aid] = round(qty * price, 2)
        elif aid in prev_values:
            values[aid] = prev_values[aid]
            warnings.append(f"{aid}: fiyat yok, onceki deger tasindi ({prev_date})")
        elif a.get("value_try"):
            values[aid] = a["value_try"]
            warnings.append(f"{aid}: fiyat yok, tanimdaki deger kullanildi")
        else:
            values[aid] = None
            warnings.append(f"{aid}: deger hesaplanamadi")

    if dirty_portfolio:
        st.save_portfolio(p)

    # K84: `accrual` bir varliga akis yazilip AYNI snapshot'ta bakiyesi
    # verilmezse, motor onceki degeri oldugu gibi tasir -> portfoy degeri
    # cekilen/yatirilan parayi hic gormez, ustelik delta_flow_adj_pct akisi
    # bir kez daha duselterek getiriyi TERS YONDE duzeltir. `_flow_fields`
    # yalnizca kaydeder, deger hesabina dokunmaz (tasarim); bu yuzden eksigi
    # motorun SOYLEMESI gerekir.
    for aid, amt in (flows or {}).items():
        a = p["assets"].get(aid) or {}
        if a.get("class") == "accrual" and aid not in prices:
            warnings.append(
                f"{aid}: akis yazildi ({amt:+,.2f}) ama ayni snapshot'ta bakiye VERILMEDI. "
                f"`accrual` varlikta akis bakiyeyi otomatik dusurmez/artirmaz - "
                f"deger onceki gunden tasindi ve portfoy toplami akisi GORMUYOR. "
                f"Gercek bakiyeyi --prices ile de gir (K84)."
            )

    total = round(sum(v for v in values.values() if v), 2)
    prev_total = (prev or {}).get("total")
    snap = {
        "date": d.isoformat(),
        "created_at": now_iso(),
        "prices": used_prices,
        "values": values,
        "total": total,
        "prev_date": prev_date.isoformat() if prev_date else None,
        "prev_total": prev_total,
        "delta_pct": round(100 * (total - prev_total) / prev_total, 2) if prev_total else None,
        **_flow_fields(total, prev_total, flows),
        "notes": args.notes or "",
    }
    write_json(st.snapshot_path(d), snap)
    eksik = [k for k, v in used_prices.items() if v is None and p["assets"][k]["class"] != "accrual"]
    out({"ok": True, "snapshot": snap, "fiyati_eksik": eksik, "uyarilar": warnings,
         "onceki_fiyatlar": prev_prices if eksik else {}})


def cmd_forecast(args):
    st = Store(args.root)
    st.ensure()
    p = st.portfolio()
    payload = read_json(args.file) if args.file else json.loads(sys.stdin.read())

    as_of = parse_date(payload.get("as_of") or args.date)
    snap = st.snapshot(as_of)
    if snap is None:
        _, snap = st.latest_snapshot(on_or_before=as_of)
    base_prices = dict((snap or {}).get("prices", {}))
    # Hafta sonu/tatil snapshot'inda fon fiyatlari `null`dur (TEFAS islem gunu
    # disinda NAV yayinlamaz). base_price null kalirsa tahmin SONRADAN
    # COZUMLENEMEZ, `baz_fiyat_yok` ile kaydedilir ve gozlem KAYBEDILIR.
    # 17.08.2026 denetimi: 142 cozumlemenin 30'u (%21) bu yuzden kayipti -
    # KUT 8 · KTJ 8 · KIK 8 · ZPE 6, hepsi hafta sonu as_of'lu.
    # Kayip RASTGELE DEGIL: yalniz hafta sonu uretilen FON tahminlerine vuruyor,
    # yani K17 ailesinden sistematik bir secilim yanliligi (K46).
    # Cozum: fiyat null ise o varlik icin en son NULL-OLMAYAN fiyata geri yurunur.
    # Bu as_of aninda BILINEN bilgidir, gelecege bakmaz; fon zaten sadece is gunu
    # fiyatlandigi icin "Cuma baz -> Pazartesi hedef" dogru sekilde 1 ISLEM GUNUDUR.
    eksik_baz = [aid for aid, v in base_prices.items() if v is None]
    probe_date, tasinan = as_of, {}
    while eksik_baz and probe_date:
        probe_date, probe = st.latest_snapshot(on_or_before=probe_date - timedelta(days=1))
        if probe is None:
            break
        pp = (probe or {}).get("prices", {})
        for aid in list(eksik_baz):
            if pp.get(aid) is not None:
                base_prices[aid] = pp[aid]
                tasinan[aid] = probe_date.isoformat()
                eksik_baz.remove(aid)

    items, problems, skipped = [], [], []
    model_id_default = payload.get("model_id") or getattr(args, "model_id", None)
    for fc in payload.get("forecasts", []):
        aid = fc.get("asset")
        if aid not in p["assets"]:
            problems.append(f"bilinmeyen varlik: {aid}")
            continue
        cls = p["assets"][aid]["class"]
        if cls not in FORECASTABLE:
            skipped.append(f"{aid} ({cls}) tahmin edilmeyen sinifta, atlandi")
            continue
        h = fc.get("horizon")
        if h not in HORIZON_DAYS:
            problems.append(f"{aid}: gecersiz horizon {h}")
            continue
        for k in ("point_pct", "low_pct", "high_pct", "p_up"):
            if fc.get(k) is None:
                problems.append(f"{aid}/{h}: {k} eksik")
        mid = fc.get("model_id") or model_id_default
        if MODEL_ID_REQUIRED and not mid:
            problems.append(f"{aid}/{h}: model_id eksik - tahmini hangi model uretti? "
                            f"(payload'a \"model_id\" ekle ya da --model-id ver; "
                            f"or. claude-opus-5, claude-fable-5-1)")
        if fc.get("low_pct") is not None and fc.get("high_pct") is not None:
            if not (fc["low_pct"] <= fc.get("point_pct", 0) <= fc["high_pct"]):
                problems.append(f"{aid}/{h}: nokta tahmin bandin disinda")
        if fc.get("p_up") is not None and not (0 <= fc["p_up"] <= 1):
            problems.append(f"{aid}/{h}: p_up 0-1 arasinda olmali")

        tgt = fc.get("target_date")
        tgt = parse_date(tgt) if tgt else as_of + timedelta(days=HORIZON_DAYS[h])
        tgt_ham = tgt
        tgt = next_open_day(tgt, cls)
        if tgt > date.fromisoformat(MARKET_CALENDAR_THROUGH):
            problems.append(
                f"{aid}/{h}: hedef tarih {tgt} tatil takviminin disinda "
                f"(kapsam {MARKET_CALENDAR_THROUGH}) - MARKET_HOLIDAYS guncellenmeli")
        if tgt != tgt_ham:
            skipped.append(f"{aid}/{h}: hedef {tgt_ham} kapali gun -> {tgt}'a kaydirildi")

        items.append({
            "asset": aid, "class": cls, "horizon": h,
            "target_date": tgt.isoformat(),
            "base_price": base_prices.get(aid),
            "point_pct": fc.get("point_pct"),
            "low_pct": fc.get("low_pct"),
            "high_pct": fc.get("high_pct"),
            "interval": fc.get("interval", 80),
            "p_up": fc.get("p_up"),
            "confidence": fc.get("confidence", "dusuk"),
            "kind": HORIZON_KIND.get(h, "tahmin"),
            "drivers": fc.get("drivers", []),
            "rationale": fc.get("rationale", ""),
            "invalidator": fc.get("invalidator", ""),
            # --- GOLGE BANT (20.08.2026) ---
            # Alternatif bir bant kuralinin kapsamasini, YURURLUKTEKI havuzu
            # bolmeden olcmek icin saklanir. Motor bunu HICBIR YERDE SKORLAMAZ;
            # cozumleme, kalibrasyon ve baseline hesaplari yalnizca low_pct /
            # high_pct kullanir. Amac: PROTOCOL_VERSION artirmadan once yeni
            # kuralin gercek kapsamasini bilmek. Olcum: scripts/golge_bant.py
            "band_shadow": fc.get("band_shadow"),
            "band_shadow_rule": fc.get("band_shadow_rule"),
            # --- MODEL DAMGASI (K78) --- tahmini ureten LLM; kalibrasyonda
            # ayri havuz anahtari. Geriye donuk: `pt.py model-stamp`.
            "model_id": mid,
        })

    # --- kanit semasi: surpriz alanlari ---
    # Fiyati OLAY degil SURPRIZ oynatir. Takvimi belli sayisal bir aciklama
    # (TUFE, istihdam, faiz) kanit olarak yaziliyorsa beklenti ve gerceklesen
    # ayri alanlarda durmali; metne gomulurse sonradan analiz edilemez.
    for e in payload.get("evidence", []):
        # `consensus` tek basina MESRUDUR: aciklama oncesi kaydedilen beklenti
        # capasidir (surpriz, veri gelince ayni kanit patch'lenerek hesaplanir).
        # Tersi mesru degil: gerceklesen varken beklenti yoksa surpriz olculemez
        # ve olay "fiyatlanmis miydi" sorusu cevapsiz kalir.
        if e.get("actual") is not None and e.get("consensus") is None:
            problems.append(f"kanit {e.get('id')}: actual var ama consensus yok - "
                            f"surpriz hesaplanamaz, olayin fiyatlanmisligi olculemez")
        if e.get("scheduled") and e.get("consensus") is None:
            problems.append(f"kanit {e.get('id')}: scheduled=true ama consensus yok - "
                            f"takvimi belli veri icin beklenti zorunlu")

    if problems and not args.force:
        die("tahmin dosyasi gecersiz:\n  - " + "\n  - ".join(problems))

    path = st.forecasts / f"{as_of.isoformat()}.json"
    existing = read_json(path, {"as_of": as_of.isoformat(), "forecasts": [], "evidence": []})
    keys = {(i["asset"], i["horizon"]) for i in items}
    # --- REVIZYON IZI (acik is #13, 01.09.2026) ---
    # Eskiden ayni (asset, horizon) sessizce EZILIYORDU; "tahmin sonradan mi
    # degistirildi" sorusu cevaplanamiyordu ve `superseded` alani 03.08'den
    # beri elle korunuyordu. Artik motor yapar:
    #   * puanlanan alanlardan biri degismisse -> revizyon: gerekce zorunlu,
    #     eski kayit `superseded`a tasinir (elle yazilan formatla ayni)
    #   * hicbiri degismemisse -> sessiz guncelleme (band_shadow eklemek gibi)
    #   * cozulmus tahmin revize EDILEMEZ, --force ile bile
    yeni_idx = {(i["asset"], i["horizon"]): i for i in items}
    cozulmus = {(r["as_of"], r["asset"], r["horizon"]) for r in st.all_resolutions()
                if r.get("durum") == "cozuldu"}
    degisen = []
    for f in existing.get("forecasts", []):
        k = (f["asset"], f["horizon"])
        if k not in yeni_idx:
            continue
        y = yeni_idx[k]
        if all(f.get(a) == y.get(a) for a in FORECAST_SCORED_FIELDS):
            # sessiz guncelleme: puanlanmayan alanlar eklenmis/duzeltilmis
            continue
        if (as_of.isoformat(),) + k in cozulmus:
            die(f"{k[0]}/{k[1]}: bu tahmin COZULMUS, revize edilemez. "
                f"Cozulmus tahmin defterde muhurludur (acik is #13).")
        degisen.append(f)
    reason = payload.get("reason") or getattr(args, "reason", None)
    if degisen and not reason:
        die("revizyon gerekce ister: " +
            ", ".join(f"{f['asset']}/{f['horizon']}" for f in degisen) +
            " puanlanan alanlari degisiyor. `--reason \"...\"` ver "
            "(veya payload'a \"reason\"). Gerekce SONUC GORULMEDEN yazilir (H9).")
    if degisen:
        existing.setdefault("superseded", []).append({
            "revised_at": now_iso(),
            "reason": reason,
            "protocol_version": existing.get("protocol_version"),
            "forecasts": degisen,
        })
    existing["forecasts"] = [f for f in existing.get("forecasts", [])
                             if (f["asset"], f["horizon"]) not in keys] + items
    # --- kontroller: H8 paydasi ---
    if "kontroller" in payload:
        kont = payload["kontroller"]
        if not isinstance(kont, list):
            die("kontroller bir liste olmali, or. [\"capraz_kontrol\", \"rutin_akis\"]")
        kotu = [k for k in kont if k not in KONTROL_MEKANIZMALARI]
        if kotu:
            die(f"kontroller sozluk disi: {kotu}. Gecerli: {', '.join(KONTROL_MEKANIZMALARI)}")
        existing["kontroller"] = sorted(set(kont))
    # --- bilinmeyen ust duzey alanlar (acik is #26) ---
    bilinmeyen = [k for k in payload if k not in FORECAST_FILE_FIELDS]
    for k in bilinmeyen:
        existing[k] = payload[k]
    # --- var olan kanitlara alan ekle (geriye donuk surpriz doldurma) ---
    # Yeni kanit eklemek yerine mevcut olani gunceller; id eslesmezse hata verir
    # ki sessizce yeni kayit olusmasin.
    patch = payload.get("evidence_patch") or {}
    if patch:
        idx = {e.get("id"): e for e in existing.get("evidence", [])}
        for eid, fields in patch.items():
            if eid not in idx:
                die(f"evidence_patch: {as_of} dosyasinda '{eid}' adli kanit yok")
            idx[eid].update(fields)

    ev = payload.get("evidence", [])
    if ev:
        for e in ev:
            if e.get("consensus") is not None and e.get("actual") is not None:
                try:
                    e["surprise"] = round(float(e["actual"]) - float(e["consensus"]), 6)
                    e["surprise_yon"] = ("yukari" if e["surprise"] > 0
                                         else "asagi" if e["surprise"] < 0 else "yok")
                except (TypeError, ValueError):
                    pass
        # K52 (20.08.2026): burasi KOSULSUZ EKLIYORDU. Ayni tahmin dosyasi
        # yeniden gonderilince (or. bir alan eklemek icin) tum kanitlar IKINCI
        # KEZ yaziliyordu - 9 kanit 18 oluyor, hicbir uyari cikmiyor. Tehlike
        # sessizligi: kanit sayisi H4'un (surpriz -> fiyat) paydasidir ve
        # ikilenmis kanit o paydayi bozar. Artik `id` ile ESLESTIRILIR:
        # ayni id varsa GUNCELLENIR, yoksa eklenir. `id`siz kanit eklenmeye
        # devam eder (geriye donuk uyum).
        mevcut = existing.get("evidence", [])
        idx_ev = {e.get("id"): i for i, e in enumerate(mevcut) if e.get("id")}
        for e in ev:
            eid = e.get("id")
            if eid is not None and eid in idx_ev:
                mevcut[idx_ev[eid]] = e
            else:
                if eid is not None:
                    idx_ev[eid] = len(mevcut)
                mevcut.append(e)
        existing["evidence"] = mevcut
    # surpriz turetmesi patch'lenen kanitlar icin de calissin
    for e in existing.get("evidence", []):
        if e.get("consensus") is not None and e.get("actual") is not None and "surprise" not in e:
            try:
                e["surprise"] = round(float(e["actual"]) - float(e["consensus"]), 6)
                e["surprise_yon"] = ("yukari" if e["surprise"] > 0
                                     else "asagi" if e["surprise"] < 0 else "yok")
            except (TypeError, ValueError):
                pass
    # --- market_state BIRLESTIRILIR, EZILMEZ (K49 -> K53) ---
    # K49 kismi yamanin 62 alani 5 alana ezdigini bulmus ve cozumu KURALA
    # birakmisti ("daima tam blok gonder"). 21.08'de ayni hata TEKRARLANDI:
    # tek bir alani (xauusd) doldurmak icin kismi yama gonderildi, 62 alan
    # 2'ye dustu. Kural yeterli olmadi -> motor duzeltiliyor.
    #   * gelen blok mevcudun UZERINE yazilir (deep-merge degil, tek seviye)
    #   * acikca null gonderilen alan SILINMEZ, mevcut deger korunur
    #   * bir alani gercekten temizlemek gerekirse dosya elle duzeltilir -
    #     market_state geriye donuk doldurulamaz, kayip sessiz olmamali
    _ms_yeni = payload.get("market_state")
    _ms_var = dict(existing.get("market_state") or {})
    if isinstance(_ms_yeni, dict):
        _ms_var.update({k: v for k, v in _ms_yeni.items() if v is not None})
    existing["market_state"] = _ms_var
    # --- market_state eksikleri (ACIK IS #20 / K40) ---
    # Kontrol PAYLOAD'a degil BIRLESMIS sonuca bakar. Eskiden payload'a
    # bakiyordu: yalnizca `evidence` ya da `scheduled_events` gondermek icin
    # yapilan bir cagri, dosyadaki 45 alan yerinde dururken "market_state
    # eksik: usdtry, xauusd, ..." diye uyariyordu. Yanlis alarmin tehlikesi
    # kendisi degil, ALISKANLIK: her cagride goruleni gormezden gelen bir
    # oturum, GERCEK eksigi de gormezden gelir.
    ms = existing.get("market_state") or {}
    eksik_ms = [k for k in MARKET_STATE_REQUIRED if ms.get(k) is None]
    dt = payload.get("day_type", existing.get("day_type"))
    if dt and dt not in DAY_TYPES:
        die(f"gecersiz day_type: {dt}. Secenekler: {', '.join(DAY_TYPES)}")
    existing["day_type"] = dt
    existing["scheduled_events"] = payload.get("scheduled_events",
                                              existing.get("scheduled_events", []))
    existing["protocol_version"] = payload.get("protocol_version", PROTOCOL_VERSION)
    existing["created_at"] = existing.get("created_at") or now_iso()
    existing["updated_at"] = now_iso()
    write_json(path, existing)
    uy = list(problems)
    if not dt:
        uy.append("day_type yok - kalibrasyonda gun tipi kirilimi yapilamaz "
                  f"({'/'.join(DAY_TYPES)})")
    if eksik_ms:
        uy.append(f"market_state eksik: {', '.join(eksik_ms)} - geriye donuk doldurulamaz")
    # --- GOLGE BANT UYARISI (acik is #30 -> K91, 07.09.2026) ---
    # #30 "motor tarafi degismez, gunluk.sh'a girsin" diyordu. Ikisi de yapildi
    # ve sebebi su: gunluk.sh SONRADAN bakar, motor YAZARKEN yakalar. Alternatif
    # bandin o gunku degeri geriye donuk uretilemez, yani gecikme = kayip.
    # `model_id` da skorlanmiyor ama zorunlu - "skorlanmayan alan" uyarmamak
    # icin gerekce degil. Burada HATA degil UYARI: golge bant deneysel bir
    # olcumdur, tahminin gecerliligi ona bagli degil.
    _1g_eksik = [f["asset"] for f in existing.get("forecasts", [])
                 if f.get("horizon") == "1d" and not f.get("band_shadow")]
    if _1g_eksik:
        uy.append(f"band_shadow eksik ({len(_1g_eksik)} adet 1g): "
                  f"{', '.join(_1g_eksik[:6])}{' ...' if len(_1g_eksik) > 6 else ''} - "
                  f"H14'un havuzu; geriye donuk doldurulamaz "
                  f"(scripts/vol_uncond.py --json)")
    # --- DUSEN ALAN UYARISI (K80, 03.09.2026) ---
    # K49/K53 gun ICINDEKI ezmeyi cozdu. Gorunmeyen sey GUNLER ARASI kayipti:
    # market_state her gun sifirdan kuruluyor ve bir oturumun elle ekledigi
    # alanlar (us2y, TCMB politika oranlari, Fed olasiliklari, gun ici
    # kotasyonlar) ertesi gun yazilmazsa SESSIZCE yok oluyor.
    # 03.09'da olculdu: 88 -> 73 alan, 20 alan dustu, hicbir uyari cikmadi.
    # MARKET_STATE_REQUIRED yalnizca 7 alani koruyor; geri kalan denetimsizdi.
    # Otomatik TASIMA yapilmiyor: bayat degeri sessizce guncel gostermek K18'in
    # ta kendisi olurdu. Yapilan sey UYARMAK - tasinacaksa `_asof` damgasina
    # "tasindi" yazmak oturumun isi.
    _onceki_gun, _onceki_rec = None, None
    for _f in sorted(st.forecasts.glob("*.json")):
        _g = _f.stem
        if _g < as_of.isoformat() and (_onceki_gun is None or _g > _onceki_gun):
            _onceki_gun, _onceki_rec = _g, read_json(_f)
    if _onceki_rec:
        _dusen = sorted(set(_onceki_rec.get("market_state") or {}) - set(_ms_var))
        if _dusen:
            uy.append(f"market_state alan DUSTU ({_onceki_gun}: "
                      f"{len(_onceki_rec.get('market_state') or {})} -> {len(_ms_var)}): "
                      f"{', '.join(_dusen[:12])}{' ...' if len(_dusen) > 12 else ''} - "
                      f"yavas degisen alan taşınacaksa `_asof` damgasina 'tasindi' yaz; "
                      f"gercekten gerekmiyorsa yoksay")

    # --- ENDEKS SICRAMASI (acik is #19 -> K93) ---
    # Bir onceki GUNUN dosyasindaki degerle karsilastirir. Hatali kotasyon
    # ya da yanlis endeks, gunluk esigi asan bir sicrama olarak gorunur.
    if _onceki_rec:
        _onc_ms = _onceki_rec.get("market_state") or {}
        for _k, _esik in MARKET_STATE_SICRAMA.items():
            _a, _b = _onc_ms.get(_k), _ms_var.get(_k)
            try:
                if _a and _b and abs(100 * (float(_b) / float(_a) - 1)) > _esik:
                    uy.append(
                        f"{_k} bir gunde %{100 * (float(_b) / float(_a) - 1):+.2f} "
                        f"({_a} -> {_b}, esik %{_esik}) - K19: hatali kotasyon ya da "
                        f"YANLIS ENDEKS olabilir, ikinci kaynakla dogrula")
            except (TypeError, ValueError, ZeroDivisionError):
                pass

    if existing.get("forecasts") and not existing.get("kontroller") \
            and as_of.isoformat() >= H8_PAYDA_BASLANGIC:
        uy.append("kontroller yok - H8 paydasi bu gun icin eksik kalir. Bugun hangi "
                  "mekanizmalar calistiysa yaz: {\"as_of\": ..., \"kontroller\": [...]}")
    if bilinmeyen:
        uy.append(f"taninmayan ust duzey alan(lar) dosyaya AYNEN yazildi, motor kullanmaz: "
                  f"{', '.join(bilinmeyen)} - kasitli degilse FORECAST_FILE_FIELDS'a bak")
    out({"ok": True, "as_of": as_of.isoformat(), "kaydedilen": len(items),
         "toplam": len(existing["forecasts"]), "atlanan": skipped,
         "revize_edilen": [f"{f['asset']}/{f['horizon']}" for f in degisen],
         "protokol_surumu": existing["protocol_version"], "day_type": dt,
         "model_ids": sorted({f.get("model_id") or "kayitsiz" for f in existing["forecasts"]}),
         "uyarilar": uy, "dosya": str(path)})


# --- KARAR DEFTERI (K92, 07.09.2026) --------------------------------------
# Defter 1 GUNLUK FIYAT TAHMINLERINI titizlikle puanliyordu ve kendi olcumune
# gore o tahminlerin becerisi YOK (uc baseline birden p=1,00). Ama paranin
# gercekten hareket ettigi yer tahmin degil KARAR: "20.000 nereye?" sorusu.
# 07.09'da bes farkli tahsis onerisi uretildi, biri secildi, digerleri
# HICBIR YERDE KAYITLI DEGILDI - bir ay sonra "ben zaten altin diyordum"
# demek serbest olacakti. Deponun tum varlik sebebi bu cumleyi imkansiz
# kilmak.
#
# ISTATISTIK IDDIASI DEGILDIR: yilda ~12 karar olur, hicbir sey "anlamli"
# cikmaz. Amac guc degil KAYIT - geriye donuk revizyonu engellemek.
#
# Skorlama mekanigi: her alternatif {varlik_id: TL} sozlugudur. Karar gunundeki
# fiyattan adet turetilir, hedef gundeki fiyatla degerlenir. Fiyati olmayan
# (accrual) kalemler icin snapshot degeri kullanilir. Ifade edilemeyen
# alternatifler (or. "dort aya yay") `skorlanmaz` + gerekce ile kaydedilir -
# kaydedilir ama puanlanmaz, cunku kaydetmemek onu yok saymaktir.
DECISION_HORIZONS = {"1m": 30, "3m": 91, "6m": 182}
# Karar skorlamasinda bir fiyat en fazla bu kadar eski olabilir. Uzun tatil
# (9 gunu asan) haric her donemde bir snapshot bulunur; asilirsa fiyat
# uydurmak yerine `eksik` yazilir.
FIYAT_BAYATLIK_GUN = 10

# ENDEKS SICRAMA ESIGI (acik is #19, 03.08 -> K93 07.09.2026).
# 03.08'de BIST 100 "14.085" diye kaydedildi, gercegi 13.410,54 idi - 675 puan,
# %5,0. Ders 04.08'de YAZILDI ("endeks degerleri bir onceki kapanisla capraz
# kontrol edilmeli") ama MEKANIZMASI KURULMADI, yani 13 ay boyunca yine
# hatirlamaya bagliydi (K53 kalibi). Artik motor bakiyor.
# Esik varlik sinifina gore: endeksler icin %5 bir gunde nadirdir; kur icin
# %3; oynak olanlarda (altin vadeli, VIX ailesi) kontrol EDILMEZ - orada
# %5'lik gun gercekten olur ve yanlis alarm, alarmı oldururdu (K40).
MARKET_STATE_SICRAMA = {
    "nasdaq": 5.0, "sp500": 5.0, "bist100": 5.0, "ndx": 5.0,
    "usdtry": 3.0, "usdtry_spot": 3.0, "dxy": 3.0,
}


def _fiyat_veya_deger(st, asset, d, ref=None):
    """Karar skorlamasi icin fiyat. accrual'da fiyat yoktur -> snapshot degeri.

    FIYAT REFERANSI IKI DEFTERDE ORTAKTIR (CLAUDE.md "iki defter kurali").
    Bir karsi-olgusal alternatif, o defterde SAHIP OLUNMAYAN bir varliga
    isaret edebilir - panel esin 20.000'i icin "hepsi gram altina" dedi ama
    es defterinde gram_altin yok. Bu bir sahiplik iddiasi degil FIYAT SORUSU:
    "o gun alsaydi bugun ne ederdi". Bu yuzden varlik bu defterde yoksa
    `ref` kokune (varsayilan `data`) dusulur. Sahiplik yine kokle belirlenir;
    buradan hicbir varlik es defterine EKLENMEZ.

    Donus: (deger, tur) - tur "fiyat" | "deger" | None.
    """
    # GERCEK fiyata kadar geri yurunur. `values`a DUSULMEZ - ilk yazimda
    # oyleydi ve mekanik testi (07.09) yakaladi: hedef gun Pazar oldugunda
    # fonun `prices` alani None, `values` ise TUTULAN pozisyonun tasinan TL
    # degeri. Karsi-olgusal bir ALIM icin bu tamamen alakasiz sayidir ve
    # sessizce "getiri = %0" uretiyordu (uc alternatif de tam 10.000,00
    # donmustu). Fiyati olan varlikta yalniz FIYAT kullanilir.
    # BAYATLIK KORUMASI: `latest_snapshot(on_or_before=...)` istenen gunde
    # snapshot yoksa SESSIZCE cok daha eskisini dondurur. Karar skorlamasinda
    # bu, aylik bir fiyati "hedef gunun fiyati" sanmak demektir ve fark
    # hesabini sessizce bozar. En fazla FIYAT_BAYATLIK_GUN geri gidilir;
    # asilirsa fiyat YOK sayilir ve `eksik`e yazilir (yarim hesap, hic
    # hesaptan kotudur - K18 ailesi).
    for kaynak in (st, ref):
        if kaynak is None:
            continue
        probe = d
        for _ in range(FIYAT_BAYATLIK_GUN + 1):
            pd_, snap = kaynak.latest_snapshot(on_or_before=probe)
            if snap is None or (d - pd_).days > FIYAT_BAYATLIK_GUN:
                break
            px = (snap.get("prices") or {}).get(asset)
            if px is not None and float(px) > 0:
                return float(px), "fiyat"
            probe = pd_ - timedelta(days=1)
    return None, None


def _dagilim_degeri(st, dagilim, karar_gun, hedef_gun, ref=None):
    """Bir {varlik: TL} dagiliminin hedef gundeki TL degeri.

    Eksik fiyat SESSIZCE ATLANMAZ - `eksik` listesine yazilir ve toplam
    `kismi` isaretlenir. Yarim hesaplanmis bir karsilastirma, hic
    hesaplanmamistan kotudur (K18 ailesi).
    """
    gun = (hedef_gun - karar_gun).days
    varliklar = {}
    for kaynak in (ref, st):
        if kaynak is not None:
            varliklar.update(kaynak.portfolio().get("assets", {}))
    toplam, eksik = 0.0, []
    for aid, tl in dagilim.items():
        meta = varliklar.get(aid) or {}
        if meta.get("class") == "accrual":
            # Fiyati yok; karsi-olgusal "bu hesaba koysaydi" birikim oraniyla
            # BILESIKLENIR. `values` kullanilamaz - o, GERCEK bakiyedir ve
            # nakit akislarini icerir, karsi-olgusalla ilgisi yoktur.
            apr = float(meta.get("accrual_apr") or 0.0)
            toplam += float(tl) * (1 + apr / 100.0) ** (gun / 365.0)
            continue
        p0, _ = _fiyat_veya_deger(st, aid, karar_gun, ref)
        p1, _ = _fiyat_veya_deger(st, aid, hedef_gun, ref)
        if not p0 or p1 is None:
            eksik.append(aid)
            continue
        toplam += float(tl) * (p1 / p0)
    return round(toplam, 2), eksik


def cmd_decision(args):
    """Karar kaydet. Alternatifler SONUC GORULMEDEN yazilir - sart budur."""
    st = Store(args.root)
    st.ensure()
    payload = read_json(args.file) if args.file else json.loads(sys.stdin.read())
    d = parse_date(payload.get("date") or args.date)
    ref = Store(args.price_root) if args.price_root and Path(args.price_root) != Path(args.root) else None
    p_assets = dict(st.portfolio().get("assets", {}))
    if ref is not None:
        # karsi-olgusal alternatif bu defterde sahip olunmayan varliga isaret
        # edebilir; gecerlilik FIYATIN varligina bakar, sahiplige degil
        p_assets.update({k: v for k, v in ref.portfolio().get("assets", {}).items()
                         if k not in p_assets})

    problems = []
    secilen = payload.get("secilen") or {}
    if not secilen:
        problems.append("`secilen` bos - hangi dagilim uygulandi?")
    alts = payload.get("alternatifler") or []
    if not alts:
        problems.append("`alternatifler` bos - karsilastirmasiz karar puanlanamaz")
    for ad, dag in [("secilen", secilen)] + [(a.get("kaynak", "?"), a.get("dagilim") or {})
                                             for a in alts if not a.get("skorlanmaz")]:
        for aid in dag:
            if aid not in p_assets:
                problems.append(f"{ad}: bilinmeyen varlik '{aid}'")
    for a in alts:
        if a.get("skorlanmaz") and not a.get("skorlanmaz_gerekce"):
            problems.append(f"{a.get('kaynak')}: skorlanmaz var ama gerekce YOK")
    if not payload.get("gerekce"):
        problems.append("`gerekce` yok - karar sonucu gorulmeden yazilmali")
    if problems and not args.force:
        die("karar dosyasi gecersiz:\n  - " + "\n  - ".join(problems))

    rec = {
        "id": payload.get("id") or f"{d.isoformat()}-{len(st.all_decisions()) + 1}",
        "date": d.isoformat(),
        "defter": payload.get("defter") or Path(args.root).name,
        "tutar": payload.get("tutar"),
        "secilen": secilen,
        "alternatifler": alts,
        "gerekce": payload.get("gerekce"),
        "kaynak": payload.get("kaynak"),
        "ufuklar": payload.get("ufuklar") or list(DECISION_HORIZONS),
        "model_id": payload.get("model_id") or getattr(args, "model_id", None),
        "created_at": now_iso(),
        "skorlar": {},
    }
    append_jsonl(st.decisions, rec)
    out({"ok": True, "id": rec["id"], "alternatif_sayisi": len(alts),
         "skorlanacak": sum(1 for a in alts if not a.get("skorlanmaz")),
         "ufuklar": rec["ufuklar"], "dosya": str(st.decisions),
         "not": "Alternatifler SONUC GORULMEDEN kaydedildi. Puanlama: pt.py decisions"})


def cmd_decisions(args):
    """Kararlari listele ve vadesi gelenleri puanla (idempotent).

    GELECEK TARIHLE PUANLAMA YASAK (K95, 07.09.2026). Olgunluk kontrolu
    (`hedef > today`) GECIRILEN tarihe bakiyor; `--date 2026-12-07` verilince
    henuz olusmamis ufuklar "vadesi gelmis" sayiliyor ve MEVCUT (bayat)
    fiyatlarla puanlaniyordu. Bulunma sekli ogretici: bu komutu bir
    PERFORMANS OLCUMU icin gelecek tarihle calistirdim ve karar defterine
    sahte skorlar yazdi - test komutu olcum defterini kirletti.
    Diger komutlarda `--date` gecmise gitmek icin mesrudur; burada degil,
    cunku puanlama GELECEGE bakar.
    """
    st = Store(args.root)
    ref = Store(args.price_root) if args.price_root and Path(args.price_root) != Path(args.root) else None
    today = parse_date(args.date)
    if today > date.today() and not args.force:
        die(f"--date {today} GELECEKTE (bugun {date.today()}). Karar puanlamasi "
            f"gelecege bakar; olgunlasmamis ufuklar bayat fiyatlarla puanlanir "
            f"ve defter kirlenir (K95). Gercekten gerekiyorsa --force.")
    rows = st.all_decisions()
    guncellenen = 0
    for r in rows:
        kd = date.fromisoformat(r["date"])
        for h in r.get("ufuklar", []):
            if h in (r.get("skorlar") or {}) and not args.force:
                continue
            hedef = kd + timedelta(days=DECISION_HORIZONS[h])
            if hedef > today:
                continue
            sec_v, sec_eksik = _dagilim_degeri(st, r["secilen"], kd, hedef, ref)
            alt_sk = []
            for a in r.get("alternatifler", []):
                if a.get("skorlanmaz"):
                    alt_sk.append({"kaynak": a.get("kaynak"), "skorlanmaz": True,
                                   "gerekce": a.get("skorlanmaz_gerekce")})
                    continue
                v, eksik = _dagilim_degeri(st, a.get("dagilim") or {}, kd, hedef, ref)
                alt_sk.append({"kaynak": a.get("kaynak"), "deger_try": v,
                               "fark_try": round(v - sec_v, 2),
                               "fark_pct": round(100 * (v / sec_v - 1), 3) if sec_v else None,
                               "eksik_fiyat": eksik})
            puanli = [a for a in alt_sk if not a.get("skorlanmaz")]
            yenen = sum(1 for a in puanli if a["deger_try"] < sec_v)
            r.setdefault("skorlar", {})[h] = {
                "hedef_tarih": hedef.isoformat(),
                "secilen_deger_try": sec_v, "secilen_eksik_fiyat": sec_eksik,
                "alternatifler": alt_sk,
                "secilen_kacini_yendi": f"{yenen}/{len(puanli)}",
                "puanlandi_at": now_iso(),
            }
            guncellenen += 1
    if guncellenen:
        write_jsonl(st.decisions, rows)
    bekleyen = []
    for r in rows:
        for h in r.get("ufuklar", []):
            if h not in (r.get("skorlar") or {}):
                bekleyen.append({"id": r["id"], "ufuk": h,
                                 "hedef": (date.fromisoformat(r["date"])
                                           + timedelta(days=DECISION_HORIZONS[h])).isoformat()})
    out({"ok": True, "karar_sayisi": len(rows), "puanlanan": guncellenen,
         "bekleyen": bekleyen,
         "kararlar": [{"id": r["id"], "date": r["date"], "defter": r.get("defter"),
                       "tutar": r.get("tutar"), "skorlar": r.get("skorlar")} for r in rows],
         "not": "n kucuk (yilda ~12 karar) - bu bir ISTATISTIK degil KAYITTIR. "
                "Amac geriye donuk 'ben sunu demistim'i imkansiz kilmak."})


def acik_kanitlar(st, today, hepsi=False):
    """`consensus` yazilmis ama `actual` girilmemis takvimli kanitlari dondurur.

    H4'un paydasi bunlarla eksiliyor (K79). Olay tarihi `event_date` alanindan
    okunur; yoksa `as_of + ACIK_KANIT_GRACE_GUN` SEZGISEL siniri kullanilir ve
    satir `tarih_kaynagi: "sezgisel"` ile isaretlenir - kesin olmayan bir
    gecikmenin kesin gorunmesi, K18 ailesinden bir hata olurdu.

    Ayni olay birkac gun ust uste capa olarak kaydedilmis olabilir (or. 07.08
    NFP'si uc ayri dosyada); `olay_anahtari` ile gruplanir ki ayni olay bir kez
    kovalansin ve H4'un paydasinda BIR kez sayilsin.
    """
    out_rows = []
    for f in st.all_forecast_files():
        rec = read_json(f)
        as_of = rec.get("as_of")
        for e in rec.get("evidence", []):
            if not e.get("scheduled") or e.get("consensus") is None:
                continue
            if e.get("actual") is not None:
                continue
            # OLCULEMEZ olarak kapatilmis kayit kovalanmaz. Bu, sayi UYDURMADAN
            # listeden cikmanin tek mesru yolu: gerekce YAZILI olmak zorunda,
            # yoksa "unutuldu" ile "olculemedi" ayirt edilemez ve H4'un paydasi
            # sessizce sisirilir.
            if e.get("actual_unavailable"):
                if not e.get("actual_unavailable_reason"):
                    e["_uyari"] = "actual_unavailable var ama gerekce YOK"
                else:
                    continue
            ed, kaynak = e.get("event_date"), "kayitli"
            if not ed:
                ed = (date.fromisoformat(as_of)
                      + timedelta(days=ACIK_KANIT_GRACE_GUN)).isoformat()
                kaynak = "sezgisel"
            gecti = date.fromisoformat(ed) <= today
            if not gecti and not hepsi:
                continue
            out_rows.append({
                "as_of": as_of, "id": e.get("id"),
                "indicator": e.get("indicator"), "consensus": e.get("consensus"),
                "unit": e.get("unit"), "event_date": ed, "tarih_kaynagi": kaynak,
                "olay_tarihi_gecti": gecti,
                "olay_anahtari": f"{e.get('indicator')}|{ed if kaynak == 'kayitli' else '?'}",
                "dosya": str(f),
            })
    return out_rows


def cmd_evidence_acik(args):
    st = Store(args.root)
    today = parse_date(args.date)
    rows = acik_kanitlar(st, today, hepsi=args.all)
    gecmis = [r for r in rows if r["olay_tarihi_gecti"]]
    gruplar = {}
    for r in gecmis:
        gruplar.setdefault(r["olay_anahtari"], []).append(r)
    # H4 paydasi: kapanmis kayitlar OLAY bazinda tekillestirilir.
    # DIKKAT (K79): tekillestirme (indicator, event_date) ciftine dayanir. Ikisi de
    # serbest metindi - ayni olay farkli adla (US_CORE_PCE_YOY / US_PCE_CORE_YOY) ya
    # da event_date'siz yazildiysa IKI OLAY gorunur ve payda SISER. Bu yuzden
    # tutarsizliklar ayrica raporlanir; sayiyi degil, SAYIYA GUVENI belirler.
    kapali_olay, kapali_satir = set(), 0
    aktueller, tarihsiz = {}, []
    for f in st.all_forecast_files():
        rec = read_json(f)
        for e in rec.get("evidence", []):
            if not (e.get("scheduled") and e.get("consensus") is not None):
                continue
            if e.get("actual") is None:
                continue
            kapali_satir += 1
            ed = e.get("event_date")
            kapali_olay.add(f"{e.get('indicator')}|{ed or rec.get('as_of')}")
            aktueller.setdefault(e.get("indicator"), set()).add(e["actual"])
            if not ed:
                tarihsiz.append(f"{rec.get('as_of')}/{e.get('id')} {e.get('indicator')}")
    catisan = {k: sorted(v) for k, v in aktueller.items() if len(v) > 1}
    out({"ok": True, "tarih": today.isoformat(),
         "acik_toplam": len(rows), "olay_tarihi_gecmis": len(gecmis),
         "gecmis_tekil_olay": len(gruplar),
         "h4_paydasi": {"kapali_satir": kapali_satir,
                        "kapali_tekil_olay": len(kapali_olay),
                        "hedef_olay": 30,
                        "not": "H4 hedefi OLAY sayisidir, satir degil - ayni olay "
                               "birkac gun capa olarak yazilmis olabilir (K79)."},
         "tutarsizlik": {
             "ayni_gosterge_farkli_actual": catisan,
             "event_date_yok": tarihsiz,
             "not": "Catisan gosterge, ayni olayin iki kez ve farkli degerle kapanmis "
                    "olabilecegini soyler (ya da mesru sekilde iki DONEMIN ayni "
                    "gostergesidir - elle bakilir). event_date'siz kayit "
                    "tekillestirilemez, payda sisebilir."},
         "olculemez_kapatilan": sum(
             1 for f in st.all_forecast_files() for e in read_json(f).get("evidence", [])
             if e.get("actual_unavailable")),
         "kovalanacaklar": sorted(gruplar.items()),
         "uyari": ("Bu kayitlarin `actual`i girilmezse surpriz hesaplanamaz ve olay "
                   "H4'un paydasina GIREMEZ. Doldurma: pt.py forecast --file <patch> "
                   "ile {\"as_of\": \"...\", \"evidence_patch\": {\"<id>\": {\"actual\": X}}}")
         if gecmis else "acik kayit yok"})


def alt_baselines(st, asset, as_of, target, actual_pct, point_pct, cls=None):
    """naif / drift / momentum baseline'larini hesapla.

    SIZINTI KURALI: oran (drift, momentum) yalnizca as_of'a KADARKI fiyatlardan
    turetilir. Adim sayisi (kac gozlenen fiyat degisimi) cozumleme aninda
    sayilir - bu bir takvim olgusu, fiyat bilgisi degil.

    Kapali gunler ve tasinan degerler seriye girmez (bkz. price_series).
    """
    seri = st.price_series(asset, cls)
    gecmis = [(d, p) for d, p in seri if d <= as_of]
    ileri = [(d, p) for d, p in seri if as_of < d <= target]
    adim = len(ileri)

    out = {
        "baseline_naif_pct": 0.0,
        "baseline_drift_pct": None,
        "baseline_momentum_pct": None,
        "baseline_adim": adim,
        "baseline_drift_lookback": None,
    }
    # DEFTERIN ILK GUNLERINDE drift/momentum HESAPLANAMAZ ve bu dogru
    # davranistir: gecmis fiyat degisimi yoksa "son 5 degisimin ortalamasi"
    # diye bir sey de yoktur. 07.09 denetimi: 383 cozumlemenin 31'inde
    # `baseline_drift_pct is None` ve HEPSI 01-05.08 arasindan (defterin ilk
    # bes gunu; 01.08 ayrica Cumartesi, yani spot varliklarda gozlem 0).
    # `tum_baselineler_yenildi` bu satirlarda None doner ve baseline ailesi
    # istatistiklerinden DISLANIR - uydurulmus bir drift'le doldurmak
    # baseline'i yapay olarak kolaylastirirdi.
    if len(gecmis) >= 2 and adim >= 1:
        degisimler = [100.0 * (gecmis[i][1] - gecmis[i - 1][1]) / gecmis[i - 1][1]
                      for i in range(1, len(gecmis))]
        son = degisimler[-BASELINE_DRIFT_LOOKBACK:]
        out["baseline_drift_pct"] = round(sum(son) / len(son) * adim, 3)
        out["baseline_drift_lookback"] = len(son)
        out["baseline_momentum_pct"] = round(degisimler[-1] * adim, 3)

    err = abs(point_pct - actual_pct)
    for kind in BASELINE_KINDS:
        tahmin = out[f"baseline_{kind}_pct"]
        if tahmin is None:
            out[f"baseline_{kind}_abs_err"] = None
            out[f"baseline_{kind}_yenildi"] = None
        else:
            b = abs(tahmin - actual_pct)
            out[f"baseline_{kind}_abs_err"] = round(b, 3)
            out[f"baseline_{kind}_yenildi"] = bool(err < b)
    hepsi = [out[f"baseline_{k}_yenildi"] for k in BASELINE_KINDS]
    out["tum_baselineler_yenildi"] = (None if any(v is None for v in hepsi)
                                      else bool(all(hepsi)))
    return out


def cmd_baselines(args):
    """Mevcut cozumlemelere alternatif baseline alanlarini GERIYE DONUK ekler.

    Bu bir yeniden puanlama degil: tahminler, gerceklesenler ve LLM hatasi
    aynen kalir. Yalnizca 'neye karsi olculdugu' zenginlesir. Idempotent -
    tekrar calistirmak ayni sonucu verir.
    """
    st = Store(args.root)
    varliklar = st.portfolio().get("assets", {})
    rows = st.all_resolutions()
    guncellenen = 0
    for r in rows:
        if r.get("durum") != "cozuldu":
            continue
        if r.get("baseline_drift_pct") is not None and not args.force:
            continue
        cls = (varliklar.get(r["asset"]) or {}).get("class")
        alt = alt_baselines(st, r["asset"], date.fromisoformat(r["as_of"]),
                            date.fromisoformat(r["target_date"]),
                            r["actual_pct"], r["point_pct"], cls)
        r.update(alt)
        guncellenen += 1
    write_jsonl(st.resolutions, rows)
    out({"ok": True, "guncellenen": guncellenen, "toplam": len(rows),
         "not": "Tahminler ve gerceklesenler DEGISMEDI; yalnizca baseline alanlari eklendi."})


def cmd_model_stamp(args):
    """`model_id` alanini GERIYE DONUK doldurur (K78).

    Yalnizca alani BOS olan kayitlara yazar; dolu olani --force olmadan ezmez.
    Hem forecasts/*.json kalemlerine hem resolutions.jsonl satirlarina.
    --through verilirse yalnizca as_of <= through olanlar damgalanir - model
    degisim gunu sinir olarak verilir ki yeni modelin tahmini eski damgayi
    almasin. Idempotent.
    """
    st = Store(args.root)
    through = parse_date(args.through) if args.through else None
    mid = args.model_id
    fc_yazilan, fc_dosya = 0, 0
    for f in st.all_forecast_files():
        rec = read_json(f)
        as_of = date.fromisoformat(rec["as_of"])
        if through and as_of > through:
            continue
        degisti = False
        for fc in rec.get("forecasts", []):
            if fc.get("model_id") and not args.force:
                continue
            if fc.get("model_id") != mid:
                fc["model_id"] = mid
                fc_yazilan += 1
                degisti = True
        if degisti:
            rec["updated_at"] = now_iso()
            write_json(f, rec)
            fc_dosya += 1
    rows = st.all_resolutions()
    res_yazilan = 0
    for r in rows:
        if through and date.fromisoformat(r["as_of"]) > through:
            continue
        if r.get("model_id") and not args.force:
            continue
        if r.get("model_id") != mid:
            r["model_id"] = mid
            res_yazilan += 1
    if res_yazilan:
        write_jsonl(st.resolutions, rows)
    out({"ok": True, "model_id": mid, "through": through.isoformat() if through else None,
         "tahmin_kalemi": fc_yazilan, "tahmin_dosyasi": fc_dosya,
         "cozumleme_satiri": res_yazilan,
         "not": "Tahminler, gerceklesenler ve skorlar DEGISMEDI; yalnizca model_id eklendi."})


def cmd_resolve(args):
    st = Store(args.root)
    st.ensure()
    today = parse_date(args.date)
    p_assets = st.portfolio().get("assets", {})
    done = {(r["as_of"], r["asset"], r["horizon"]) for r in st.all_resolutions()}

    new_rows, pending = [], []
    for f in st.all_forecast_files():
        rec = read_json(f)
        as_of = rec["as_of"]
        # Alt kume analizleri join gerektirmesin diye tahmin dosyasindaki baglam
        # her cozumleme satirina damgalanir.
        ctx = {
            "protocol_version": rec.get("protocol_version"),
            "day_type": rec.get("day_type"),
        }
        for fc in rec.get("forecasts", []):
            key = (as_of, fc["asset"], fc["horizon"])
            if key in done:
                continue
            tgt = date.fromisoformat(fc["target_date"])
            if tgt > today:
                pending.append({"as_of": as_of, "asset": fc["asset"], "horizon": fc["horizon"],
                                "target_date": fc["target_date"]})
                continue

            snap = st.snapshot(tgt)
            actual = (snap or {}).get("prices", {}).get(fc["asset"]) if snap else None
            if actual is None:
                # hedef gunde veri yoksa sonraki gunlere bak (tatil / TEFAS gecikmesi)
                for k in range(1, RESOLVE_GRACE_DAYS + 1):
                    s2 = st.snapshot(tgt + timedelta(days=k))
                    if s2 and s2.get("prices", {}).get(fc["asset"]) is not None:
                        actual = s2["prices"][fc["asset"]]
                        break
            if actual is None:
                if (today - tgt).days >= RESOLVE_GRACE_DAYS:
                    new_rows.append({**_res_stub(as_of, fc), "durum": "veri_yok"})
                else:
                    pending.append({"as_of": as_of, "asset": fc["asset"], "horizon": fc["horizon"],
                                    "target_date": fc["target_date"], "not": "snapshot bekleniyor"})
                continue

            base = fc.get("base_price")
            if not base:
                new_rows.append({**_res_stub(as_of, fc), "durum": "baz_fiyat_yok"})
                continue

            actual_pct = 100.0 * (actual - base) / base
            err = abs(fc["point_pct"] - actual_pct)
            baseline_err = abs(actual_pct)  # naif: "degismez"
            # Olu bolge: gurultu seviyesindeki hareketin yonu bilgi degildir.
            # Fiyat yuvarlamasi bile |actual_pct| > 0 yapabilir; bunu "yon
            # tutturuldu/tutturulamadi" diye skorlamak kalibrasyonu kirletir.
            yatay = abs(actual_pct) < DIRECTION_DEADZONE_PCT
            row = {
                **_res_stub(as_of, fc),
                **ctx,
                "confidence": fc.get("confidence"),
                "horizon_kind": HORIZON_KIND.get(fc["horizon"], "tahmin"),
                "durum": "cozuldu",
                "base_price": base,
                "actual_price": actual,
                "actual_pct": round(actual_pct, 3),
                "point_pct": fc["point_pct"],
                "abs_err": round(err, 3),
                "signed_err": round(fc["point_pct"] - actual_pct, 3),
                "baseline_abs_err": round(baseline_err, 3),
                "baseline_yenildi": bool(err < baseline_err),
                "bantta": bool(fc["low_pct"] <= actual_pct <= fc["high_pct"]),
                "band": [fc["low_pct"], fc["high_pct"]],
                "p_up": fc.get("p_up"),
                "yatay": bool(yatay),
                "deadzone_pct": DIRECTION_DEADZONE_PCT,
                "yon_dogru": None if yatay or fc.get("p_up") is None
                             else bool((fc["p_up"] > 0.5) == (actual_pct > 0)),
                "brier": None if yatay or fc.get("p_up") is None
                         else round((fc["p_up"] - (1.0 if actual_pct > 0 else 0.0)) ** 2, 4),
                **alt_baselines(st, fc["asset"], date.fromisoformat(as_of), tgt,
                                actual_pct, fc["point_pct"],
                                (p_assets.get(fc["asset"]) or {}).get("class")),
                "resolved_at": now_iso(),
            }
            new_rows.append(row)

    if new_rows:
        st.append_resolutions(new_rows)
    out({"ok": True, "cozulen": len([r for r in new_rows if r["durum"] == "cozuldu"]),
         "veri_yok": len([r for r in new_rows if r["durum"] != "cozuldu"]),
         "bekleyen": len(pending), "yeni": new_rows, "bekleyenler": pending[:20]})


def _res_stub(as_of, fc):
    return {"as_of": as_of, "asset": fc["asset"], "horizon": fc["horizon"],
            "target_date": fc["target_date"],
            # K78: tahmini ureten model, alt kume anahtari (protocol_version gibi)
            "model_id": fc.get("model_id")}


def _calib(rows):
    """Kalibrasyon metrikleri.

    BIRINCIL TEST: `eslestirilmis` blogu. Ayni gun, ayni varlik icin LLM hatasi
    ile baseline hatasi karsilastirilir; ortak varyans dusurulur. Isaret testi
    (baseline_yenildi orani vs 0,50) TAM binom testidir, yaklasim degil.

    TESHIS: `yon_isabeti`. Ikili siniflama p_up'in tasidigi bilgiyi atar
    (0,54 ile 0,80 ayni sayilir) ve ayni edge'i gostermek icin ~3-6 kat daha
    fazla gozlem ister. Raporda birincil sayi olarak kullanma.
    """
    solved = [r for r in rows if r.get("durum") == "cozuldu"]
    if not solved:
        # Sekil sabit kalsin: downstream kod her zaman ayni anahtarlari bulsun.
        return {"n": 0, "eslestirilmis": None, "bant_kapsama": None,
                "yon_isabeti": None, "skill_score": None, "brier": None}
    errs = [r["abs_err"] for r in solved]
    base = [r["baseline_abs_err"] for r in solved]
    dirs = [r["yon_dogru"] for r in solved if r.get("yon_dogru") is not None]
    briers = [r["brier"] for r in solved if r.get("brier") is not None]
    mae, bmae = statistics.fmean(errs), statistics.fmean(base)

    # --- birincil: eslestirilmis fark (baseline hatasi - LLM hatasi) ---
    diffs = [b - e for e, b in zip(errs, base)]
    wins = sum(1 for d in diffs if d > 0)
    ties = sum(1 for d in diffs if d == 0)
    n_eff = len(diffs) - ties          # isaret testinde beraberlikler atilir
    paired = {
        "n": len(diffs),
        "beraberlik": ties,
        "ortalama_kazanc_puan": round(statistics.fmean(diffs), 4),
        "ortalama_kazanc_ci95": mean_ci(diffs),
        "isaret_testi_kazanan": wins,
        "isaret_testi_n": n_eff,
        "isaret_testi_p_tek_yonlu": binom_test_greater(wins, n_eff) if n_eff else None,
        "kazanma_orani_ci95": wilson_ci(wins, n_eff) if n_eff else None,
        "sonuc": None,
    }
    if n_eff:
        p = paired["isaret_testi_p_tek_yonlu"]
        paired["sonuc"] = ("baseline'dan iyi (p<0,05)" if p is not None and p < 0.05
                           else "baseline'dan iyi oldugu GOSTERILEMEDI")

    # --- ZOR BASELINE'LAR: drift ve momentum -------------------------------
    # "%0 degisim" tek yonlu bir piyasada kolay lokmadir. Asagidaki blok, ayni
    # eslestirilmis isaret testini drift ve momentum baseline'larina karsi da
    # kurar. `hepsi_yenildi` = ucunu birden yenen satirlarin orani; asil sayi
    # budur, cunku bir tahminin bilgi tasidigini soylemek icin hem
    # hareketsizligi hem trendi hem de dunku hareketi yenmesi gerekir.
    baslar = {}
    for kind in BASELINE_KINDS:
        alan = f"baseline_{kind}_abs_err"
        cift = [(r["abs_err"], r[alan]) for r in solved if r.get(alan) is not None]
        if not cift:
            baslar[kind] = {"n": 0, "sonuc": "veri yok"}
            continue
        d = [b - e for e, b in cift]
        w = sum(1 for x in d if x > 0)
        t = sum(1 for x in d if x == 0)
        ne = len(d) - t
        p = binom_test_greater(w, ne) if ne else None
        baslar[kind] = {
            "n": len(d),
            "baseline_mae_pct": round(statistics.fmean(b for _, b in cift), 3),
            "ortalama_kazanc_puan": round(statistics.fmean(d), 4),
            "ortalama_kazanc_ci95": mean_ci(d),
            "isaret_testi_kazanan": w,
            "isaret_testi_n": ne,
            "isaret_testi_p_tek_yonlu": p,
            "kazanma_orani_ci95": wilson_ci(w, ne) if ne else None,
            "sonuc": ("yenildi (p<0,05)" if p is not None and p < 0.05
                      else "yenildigi GOSTERILEMEDI"),
        }
    hepsi_alan = [r.get("tum_baselineler_yenildi") for r in solved]
    hepsi = [v for v in hepsi_alan if v is not None]
    baslar["hepsi_yenildi"] = {
        "n": len(hepsi),
        "kazanan": sum(hepsi),
        "oran": round(sum(hepsi) / len(hepsi), 3) if hepsi else None,
        "oran_ci95": wilson_ci(sum(hepsi), len(hepsi)) if hepsi else None,
        "p_tek_yonlu": binom_test_greater(sum(hepsi), len(hepsi)) if hepsi else None,
        "not": "Uc baseline'i (naif+drift+momentum) BIRDEN yenen satirlarin orani. "
               "Sans esigi 0,50 DEGIL - uc bagimli testin ortak yenilme olasiligi "
               "daha dusuktur, bu yuzden p degeri muhafazakar (gercek anlamlilik "
               "bundan daha guclu olabilir). Asil bakilacak sayi budur.",
    }

    # --- GUN KUMELI ISARET TESTI (K76, 01.09.2026) ---
    # on-kayit.md havuzlama kurali 5: "ayni gunun varliklari bagimsiz degildir,
    # gunde ~2,5 etkin gozlem." Kural 04.08'den beri yaziliydi ama HESAPLANMIYORDU;
    # yukaridaki satir-bazli testler her (gun, varlik, ufuk) satirini bagimsiz
    # sayiyor. Olculdu: 1h signed_err'in ayni gun varliklar arasi korelasyonu
    # gram-KUT +0,80, KTJ-KIK +0,68. Kume = as_of gunu (en muhafazakar birim):
    # gun icinde cogunluk kazandiysa gun "kazanildi", 50/50 gunler atilir,
    # tam binom testi gun sayisi uzerinde. Satir-bazli p ile BIRLIKTE raporlanir;
    # ikisi ayrisiyorsa (01.09: drift 0,0005 -> 0,054) bagimsizlik varsayimi
    # kirilmistir ve baglayici olan kumeli sonuctur.
    def _kumeli(kazandi_mi):
        gunler = {}
        for r in solved:
            v = kazandi_mi(r)
            if v is not None:
                gunler.setdefault(r["as_of"], []).append(v)
        fr = [sum(v) / len(v) for v in gunler.values()]
        w = sum(1 for f in fr if f > 0.5)
        t = sum(1 for f in fr if f == 0.5)
        ne = len(fr) - t
        p = binom_test_greater(w, ne) if ne else None
        return {"gun": len(fr), "kazanilan_gun": w, "berabere_gun": t,
                "p_tek_yonlu": p,
                "sonuc": ("yenildi (p<0,05)" if p is not None and p < 0.05
                          else "yenildigi GOSTERILEMEDI")}

    def _kazandi(alan):
        def f(r):
            b = r.get(alan)
            if b is None:
                return None
            d = b - r["abs_err"]
            return None if d == 0 else d > 0
        return f
    kumeli = {"naif": _kumeli(_kazandi("baseline_abs_err"))}
    for kind in BASELINE_KINDS:
        if kind != "naif":
            kumeli[kind] = _kumeli(_kazandi(f"baseline_{kind}_abs_err"))
    kumeli["hepsi_yenildi"] = _kumeli(lambda r: r.get("tum_baselineler_yenildi"))
    kumeli["not"] = ("Kume = as_of gunu. on-kayit havuzlama kurali 5'in hesabi. "
                     "Satir-bazli p ile ayrisiyorsa BAGLAYICI OLAN BUDUR.")

    # --- EN IYI ADAY: dort adayli yarista hangisi en kucuk hatayi verdi ---
    # `hepsi_yenildi`nin hesaplanabilir sifir hipotezi yoktu ("0,50 esigi
    # yanlis" notu vardi ama dogrusu yoktu). Simetrik kurgu: {LLM, naif, drift,
    # momentum} dort aday, her satirda tek kazanan (en kucuk abs_err; esitlik
    # -> kimseye). Sans = 0,25. LLM'in payi 0,25'e karsi tek yonlu binom.
    # Baseline'larin kendi paylari da yazilir - "drift %30, LLM %32" gibi bir
    # tablo, "%32 iyi mi" sorusunu olcekli hale getirir. Satir-bazli, ayni
    # bagimsizlik uyarisi gecerli; gun-kumeli surumu de verilir.
    adaylar = ("llm", "naif", "drift", "momentum")
    yaris = [r for r in solved if all(r.get(f"baseline_{k}_abs_err") is not None
                                      for k in BASELINE_KINDS)]
    en_iyi = None
    if yaris:
        sayac = {a: 0 for a in adaylar}
        esit = 0
        gun_llm = {}
        for r in yaris:
            hata = {"llm": r["abs_err"], "naif": r["baseline_naif_abs_err"],
                    "drift": r["baseline_drift_abs_err"],
                    "momentum": r["baseline_momentum_abs_err"]}
            m = min(hata.values())
            kaz = [a for a in adaylar if hata[a] == m]
            if len(kaz) == 1:
                sayac[kaz[0]] += 1
                gun_llm.setdefault(r["as_of"], []).append(kaz[0] == "llm")
            else:
                esit += 1
        n_y = len(yaris)
        fr = [sum(v) / len(v) for v in gun_llm.values()]
        g_w = sum(1 for f in fr if f > 0.25)
        en_iyi = {
            "n": n_y, "esitlik": esit,
            "pay": {a: round(sayac[a] / n_y, 3) for a in adaylar},
            "sans_payi": 0.25,
            "llm_p_tek_yonlu": binom_test_greater(sayac["llm"], n_y, 0.25),
            "llm_gun_kumeli": {"gun": len(fr), "llm_payi_0.25_ustu_gun": g_w,
                               "p_tek_yonlu": binom_test_greater(g_w, len(fr)) if fr else None},
            "not": "Dort adayli yaris, satir basina tek kazanan. Sans payi 0,25. "
                   "hepsi_yenildi'nin olcekli karsiligi; baseline paylari referanstir.",
        }

    n_dir = len(dirs)
    k_dir = sum(dirs)
    n_band = len(solved)
    k_band = sum(r["bantta"] for r in solved)
    return {
        "n": len(solved),
        # --- birincil ---
        "eslestirilmis": paired,
        "baseline_ailesi": baslar,
        "gun_kumeli": kumeli,
        "en_iyi_aday": en_iyi,
        # --- ozet ---
        "mae_pct": round(mae, 3),
        "baseline_mae_pct": round(bmae, 3),
        "skill_score": round(1 - mae / bmae, 3) if bmae else None,
        "baseline_yenme_orani": round(wins / len(solved), 3),
        # --- bant (en hizli yakinsayan metrik) ---
        "bant_kapsama": round(k_band / n_band, 3),
        "bant_kapsama_ci95": wilson_ci(k_band, n_band),
        "bant_hedefi": 0.80,
        "bant_sapma_p": binom_test_two_sided(k_band, n_band, 0.80),
        # --- teshis (birincil degil) ---
        "yon_isabeti": round(k_dir / n_dir, 3) if dirs else None,
        "yon_n": n_dir,
        "yon_isabeti_ci95": wilson_ci(k_dir, n_dir) if dirs else None,
        "yon_p_tek_yonlu": binom_test_greater(k_dir, n_dir) if dirs else None,
        "bias_pct": round(statistics.fmean(r["signed_err"] for r in solved), 3),
        "brier": round(statistics.fmean(briers), 4) if briers else None,
        "brier_baseline_050": 0.25,
        **_skorlama(solved),
    }


def _skorlama(solved):
    """Ek skorlar (13.08.2026, derin arastirma sonrasi). Hepsi mevcut alanlardan
    hesaplanir, hicbir sey saklanmaz - idempotent ve geriye donuk.

    1) IKLIMSEL BRIER + BSS: 0,25 referansi ("yazi tura") tek yonlu rejimde
       yaniltici - cozulen kayitlarda "yukari" taban orani ~%88. Dogru referans
       yuruyen taban oran; SIZINTISIZ olmasi icin her satirin p_bar'i yalniz
       DAHA ONCEKI hedef tarihli satirlardan gelir (min 10 gecmis gozlem).
       BSS = 1 - Brier_LLM / Brier_iklimsel. Negatif = taban orana kaybediyor.
    2) INTERVAL SCORE + WIS (Gneiting-Raftery 2007; Bracher 2021): tek %80
       bant icin IS = genislik + (2/a)*alt_kacis + (2/a)*ust_kacis, a=0,2.
       WIS = (0,5*|nokta hatasi| + (a/2)*IS) / 1,5 - MAE ile ayni birim,
       baseline MAE'siyle DOGRUDAN kiyaslanabilir (H13-a).
    3) PIT 4-KUTU: [<alt, alt-nokta, nokta-ust, >ust]; beklenen oranlar
       [0,10, 0,40, 0,40, 0,10]. Sekil TESHISTIR - ayni gunun varliklari
       korelasyonlu oldugu icin chi-kare p'si kanit sayilmaz.
    4) KESKINLIK: ortalama bant genisligi - kapsamanin maliyeti.
    5) KOMBINASYON (H13-b on testi, KESIFSEL): ort4/medyan4 =
       {LLM, naif(0), drift, momentum} esit agirlikli. n<150'de agirlik
       TAHMIN ETMEK YASAK (kombinasyon bilmecesi, Bates-Granger literaturu).
    """
    a = 0.2
    out = {}

    bandli = [r for r in solved if r.get("band") and r.get("actual_pct") is not None]
    if bandli:
        is_l, wis_l, gen_l, pit = [], [], [], [0, 0, 0, 0]
        for r in bandli:
            lo, hi = r["band"]; y = r["actual_pct"]; m = r["point_pct"]
            gen = hi - lo
            isc = gen + (2 / a) * max(0.0, lo - y) + (2 / a) * max(0.0, y - hi)
            is_l.append(isc)
            wis_l.append((0.5 * abs(m - y) + (a / 2) * isc) / 1.5)
            gen_l.append(gen)
            pit[0 if y < lo else 1 if y < m else 2 if y <= hi else 3] += 1
        out["interval_score_ort"] = round(statistics.fmean(is_l), 3)
        out["wis_ort"] = round(statistics.fmean(wis_l), 3)
        out["keskinlik_ort_bant_genisligi"] = round(statistics.fmean(gen_l), 3)
        out["pit_kutulari"] = {"alt_kacis": pit[0], "alt_yarim": pit[1],
                              "ust_yarim": pit[2], "ust_kacis": pit[3],
                              "beklenen_oran": [0.10, 0.40, 0.40, 0.10],
                              "not": "sekil teshistir; ayni gunun varliklari korelasyonlu, test kanit degil"}

    # --- iklimsel Brier / BSS (sizintisiz yuruyen taban oran) ---
    sirali = sorted((r for r in solved if r.get("brier") is not None),
                    key=lambda r: r["target_date"])
    gecmis, katilan = [], []
    for r in sirali:
        onceki = [o for d, o in gecmis if d < r["target_date"]]
        if len(onceki) >= 10:
            pbar = sum(onceki) / len(onceki)
            y = 1.0 if r["actual_pct"] > 0 else 0.0
            katilan.append(((pbar - y) ** 2, r["brier"]))
        gecmis.append((r["target_date"], 1.0 if r["actual_pct"] > 0 else 0.0))
    if katilan:
        b_iklim = statistics.fmean(c for c, _ in katilan)
        b_llm = statistics.fmean(b for _, b in katilan)
        out["brier_iklimsel"] = {
            "n": len(katilan),
            "iklimsel": round(b_iklim, 4), "llm": round(b_llm, 4),
            "bss": round(1 - b_llm / b_iklim, 3) if b_iklim else None,
            "not": "BSS<0 = p_up yuruyen taban orana KAYBEDIYOR. 0,25 referansi degil bu satir basliktir.",
        }

    # --- kombinasyon: ort4 / medyan4 (KESIFSEL - H13-b bunun uzerine on kayitli) ---
    komb = [r for r in solved if r.get("baseline_drift_pct") is not None
            and r.get("baseline_momentum_pct") is not None]
    if komb:
        for ad, fn in (("ort4", lambda v: sum(v) / 4.0),
                       ("medyan4", lambda v: statistics.median(v))):
            e_k, e_l, e_d = [], [], []
            for r in komb:
                tahmin = fn([r["point_pct"], 0.0, r["baseline_drift_pct"],
                             r["baseline_momentum_pct"]])
                e_k.append(abs(tahmin - r["actual_pct"]))
                e_l.append(r["abs_err"])
                e_d.append(r["baseline_drift_abs_err"])
            w_l = sum(1 for k, l in zip(e_k, e_l) if k < l)
            n_l = sum(1 for k, l in zip(e_k, e_l) if k != l)
            w_d = sum(1 for k, d in zip(e_k, e_d) if k < d)
            n_d = sum(1 for k, d in zip(e_k, e_d) if k != d)
            out[f"komb_{ad}"] = {
                "n": len(komb), "mae": round(statistics.fmean(e_k), 3),
                "vs_llm": f"{w_l}/{n_l}", "vs_llm_p": binom_test_greater(w_l, n_l) if n_l else None,
                "vs_drift": f"{w_d}/{n_d}", "vs_drift_p": binom_test_greater(w_d, n_d) if n_d else None,
            }
        out["komb_not"] = ("KESIFSEL - kanit degil, H13-b hipotez ureteci. KURAL: n<150'de "
                           "agirlik tahmini YASAK (esit ortalama/medyan disinda kural denenmez).")
    return out


def cmd_calibrate(args):
    st = Store(args.root)
    today = parse_date(args.date)
    cutoff = today - timedelta(days=args.window)
    rows = [r for r in st.all_resolutions()
            if date.fromisoformat(r["target_date"]) >= cutoff]

    # Protokol v1'de `spot` varliklarin hedef tarihi hafta sonuna dusebiliyordu;
    # kapali gun snapshot'i onceki fiyati tasidigi icin bu satirlar garantili
    # %0 degisimle cozuldu ve metrikleri yapay olarak iyilestirdi. resolutions
    # append-only oldugu icin satir SILINMEZ - havuza alinmaz ve sayisi
    # raporlanir. Kaynak kural: next_open_day(), reviews/2026-08.md -> K17.
    assets = st.portfolio().get("assets", {})

    def _kapali_gun_hedefi(r):
        cls = assets.get(r["asset"], {}).get("class")
        if cls in ALWAYS_OPEN_CLASSES:
            return False
        return not is_market_open(date.fromisoformat(r["target_date"]))

    kapali = [r for r in rows if _kapali_gun_hedefi(r)]
    rows = [r for r in rows if not _kapali_gun_hedefi(r)]

    # --- MUKERRER GOZLEM (K86, 07.09.2026) ---
    # K17 hedef tarihini duzeltti: kapali gune tahmin yazilmiyor artik. Kalan
    # sorun HEDEFTE degil KAYNAKTA: Cuma/Cmt/Paz gunlerinde uretilen fon
    # tahminlerinin UCU DE ayni Pazartesi NAV'ini, ayni baz fiyattan hedefler
    # (TEFAS hafta sonu fiyat vermez, motor onceki degeri tasir). Ucu de ayni
    # gerceklesmeyle cozulur -> tek bir piyasa hareketi havuza UC KEZ girer.
    # 07.09'da olculdu: 383 cozumlemenin 45'i (%11,7) boyle; 1g'de 31, 1h'de 14.
    # Rastgele DEGIL - yalniz fund_tefas'a ve yalniz hafta sonu cevresine vurur.
    # SATIR SILINMEZ (append-only) ve tekil skorlari degismez; yalnizca
    # `mukerrer_arindirilmis` blogu ayrica hesaplanir.
    # Hangi satir tutulur: EN ERKEN as_of. Sebep tasarim degil olcum: sonraki
    # gunun tahmini ayni sonucu daha COK bilgiyle yapiyor (Cuma ABD kapanisi
    # Pazar sabahi bellidir), yani ic ice gecmis bilgi kumeleri. En erkeni
    # tutmak muhafazakar olandir - defterin lehine olan satiri secmez.
    _grup = {}
    for r in rows:
        _grup.setdefault((r["asset"], r["horizon"], r["target_date"],
                          r.get("base_price")), []).append(r)
    tekil_rows, mukerrer_n = [], 0
    for _k, _v in _grup.items():
        _v = sorted(_v, key=lambda x: x["as_of"])
        tekil_rows.append(_v[0])
        mukerrer_n += len(_v) - 1

    if args.asset:
        rows = [r for r in rows if r["asset"] == args.asset]

    by_horizon, by_asset = {}, {}
    by_version, by_daytype, by_conf, by_model = {}, {}, {}, {}
    for r in rows:
        by_horizon.setdefault(r["horizon"], []).append(r)
        by_asset.setdefault(r["asset"], []).append(r)
        by_version.setdefault(str(r.get("protocol_version", "kayitsiz")), []).append(r)
        by_daytype.setdefault(r.get("day_type") or "etiketsiz", []).append(r)
        by_model.setdefault(r.get("model_id") or "kayitsiz", []).append(r)
        by_conf.setdefault(r.get("confidence") or "etiketsiz", []).append(r)

    # ON KAYITLI ALT KUME (reviews/on-kayit.md, H3): dusuk kanaatli tahminler
    # cogunlukla "yonlu sinyalim yok" kaydidir ve varsa edge'i seyreltir.
    # Ayrimin veriye BAKILMADAN once yazilmis olmasi bu testi gecerli kilar.
    yuksek_kanaat = [r for r in rows if r.get("confidence") in ("orta", "yuksek")]

    surumler = sorted(by_version)
    res = {
        "pencere_gun": args.window,
        "tarih": today.isoformat(),
        "protokol_surumu": PROTOCOL_VERSION,
        "haric_kapali_gun_hedefi": {
            "adet": len(kapali),
            "satirlar": [f"{r['as_of']} {r['asset']} {r['horizon']} -> {r['target_date']}"
                         for r in kapali],
            "neden": "hedef gun piyasa kapali; snapshot onceki fiyati tasir, "
                     "cozumleme garantili %0 verir. Protokol v1 artigi (K17).",
        } if kapali else None,
        "genel": _calib(rows),
        "on_kayitli_yuksek_kanaat": _calib(yuksek_kanaat),
        "horizon_bazli": {k: _calib(v) for k, v in sorted(by_horizon.items())},
        "varlik_bazli": {k: _calib(v) for k, v in sorted(by_asset.items())},
        "gun_tipi_bazli": {k: _calib(v) for k, v in sorted(by_daytype.items())},
        "kanaat_bazli": {k: _calib(v) for k, v in sorted(by_conf.items())},
        "surum_bazli": {k: _calib(v) for k, v in sorted(by_version.items())},
        # K86: ayni (varlik, ufuk, hedef, baz) uzerindeki fazladan satirlar
        # atilarak. BIRINCIL degil TESHIS - hangi metrigin bagimli gozlemden
        # ne kadar etkilendigini gosterir.
        "mukerrer_arindirilmis": {
            "n": len(tekil_rows), "atilan_satir": mukerrer_n,
            "atilan_oran": round(mukerrer_n / len(rows), 4) if rows else None,
            "tutulan": "en erken as_of",
            "metrikler": _calib(tekil_rows),
            "not": "Cuma/Cmt/Paz'da uretilen fon tahminleri ayni Pazartesi NAV'ini "
                   "ayni bazdan hedefler; tek hareket havuza birkac kez girer. "
                   "Satirlar SILINMEDI, tekil skorlari degismedi."},
        # K78: farkli LLM'ler ayni havuzda toplanmaz - protocol_version'in model karsiligi
        "model_bazli": {k: _calib(v) for k, v in sorted(by_model.items())},
        "yorum_kilavuzu": {
            "BIRINCIL": "eslestirilmis.isaret_testi_p_tek_yonlu < 0,05 ise baseline yenilmistir. "
                        "Diger her sey teshis amaclidir.",
            "gun_kumeli": "Ayni gunun satirlari bagimsiz DEGIL (on-kayit kural 5). Satir-bazli "
                          "p ile kumeli p ayrisiyorsa baglayici olan kumelidir (K76).",
            "en_iyi_aday": "Dort adayli yaris; LLM payi 0,25'e karsi. hepsi_yenildi'nin "
                           "hesaplanabilir sifir hipotezli karsiligi.",
            "eslestirilmis": "ayni gun ayni varlik, LLM hatasi vs baseline hatasi. "
                             "Ortak varyansi dusurur, yon isabetinden 3-6 kat verimli.",
            "skill_score": ">0 baseline'dan iyi, <=0 tahminlerin degeri yok. "
                           "Guven araligi YOK - tek basina karar verme, eslestirilmis bloga bak.",
            "bant_kapsama": "0,80 civari ideal; en HIZLI yakinsayan metrik, "
                            "bant_sapma_p<0,05 ise bant genisligi gercekten yanlistir.",
            "yon_isabeti": "TESHIS. Ikili siniflama p_up bilgisini atar. "
                           "%52'lik gercek bir edge icin ~3.900 bagimsiz gozlem gerekir "
                           "(bugunku hizla ~6 yil). CI sifiri kapsiyorsa 'sans' de.",
            "brier": "0,25 sans seviyesi; dusuk daha iyi. p_up'i kullandigi icin "
                     "yon isabetinden bilgilendirici.",
            "bias_pct": "pozitif = sistematik olarak fazla iyimser",
            "1m_uyarisi": "1 aylik satirlar ORTUSEN gozlemlerdir; yilda ~12 bagimsiz ay "
                          "vardir. Bu ufuktaki n'i bagimsiz sayma, sonucu yorumlama - "
                          "1a bir PROJEKSIYONDUR (HORIZON_KIND).",
        },
    }
    if len(surumler) > 1:
        res["UYARI_SURUM"] = (
            f"Bu pencerede {len(surumler)} farkli protokol surumu var: {surumler}. "
            f"Farkli surumler AYNI havuzda yorumlanmaz - `surum_bazli` kirilimina bak.")
    out(res)


def cmd_report(args):
    st = Store(args.root)
    st.ensure()
    today = parse_date(args.date)
    p = st.portfolio()

    snap_date, snap = st.latest_snapshot(on_or_before=today)
    prev_date, prev = (None, None)
    if snap_date:
        prev_date, prev = st.latest_snapshot(on_or_before=snap_date - timedelta(days=1))

    # bugunu hedefleyen tum tahminler (horizon'a gore gruplanir)
    targeting_today = {"1d": [], "1w": [], "1m": []}
    for f in st.all_forecast_files():
        rec = read_json(f)
        for fc in rec.get("forecasts", []):
            if fc["target_date"] == today.isoformat():
                targeting_today.setdefault(fc["horizon"], []).append({**fc, "as_of": rec["as_of"]})

    res_index = {(r["as_of"], r["asset"], r["horizon"]): r for r in st.all_resolutions()}
    for h, lst in targeting_today.items():
        for fc in lst:
            fc["sonuc"] = res_index.get((fc["as_of"], fc["asset"], fc["horizon"]))

    # bugun uretilmis, hala acik tahminler
    acik = []
    for f in st.all_forecast_files():
        rec = read_json(f)
        for fc in rec.get("forecasts", []):
            if date.fromisoformat(fc["target_date"]) > today:
                acik.append({"as_of": rec["as_of"], "asset": fc["asset"],
                             "horizon": fc["horizon"], "target_date": fc["target_date"]})

    all_res = st.all_resolutions()
    c30 = [r for r in all_res if date.fromisoformat(r["target_date"]) >= today - timedelta(days=30)]

    varliklar = []
    for aid, a in p["assets"].items():
        v = (snap or {}).get("values", {}).get(aid)
        pv = (prev or {}).get("values", {}).get(aid)
        varliklar.append({
            "id": aid, "label": a["label"], "class": a["class"],
            "tahmin_edilebilir": a["class"] in FORECASTABLE,
            "quantity": a.get("quantity"),
            "deger_try": v,
            "onceki_deger_try": pv,
            "gunluk_pct": round(100 * (v - pv) / pv, 2) if (v and pv) else None,
            "son_fiyat": (snap or {}).get("prices", {}).get(aid),
            "price_source": a.get("price_source"),
        })
    total = (snap or {}).get("total")
    for v in varliklar:
        v["agirlik_pct"] = round(100 * v["deger_try"] / total, 1) if (total and v["deger_try"]) else None
    varliklar.sort(key=lambda r: r["deger_try"] or 0, reverse=True)

    ev_path = st.evidence / f"{today.isoformat()}.md"
    out({
        "tarih": today.isoformat(),
        "sistem_yasi_gun": _system_age(st),
        "portfoy": {
            "toplam_try": total,
            "onceki_toplam_try": (prev or {}).get("total"),
            "delta_pct": (snap or {}).get("delta_pct"),
            "net_flow_try": (snap or {}).get("net_flow_try", 0.0),
            "delta_flow_adj_pct": (snap or {}).get("delta_flow_adj_pct",
                                                   (snap or {}).get("delta_pct")),
            "snapshot_tarihi": snap_date.isoformat() if snap_date else None,
            "bugun_snapshot_var_mi": st.snapshot(today) is not None,
            "varliklar": varliklar,
        },
        "bugunu_hedefleyen_tahminler": targeting_today,
        "acik_tahminler": sorted(acik, key=lambda r: r["target_date"])[:40],
        "kalibrasyon_30g": _calib(c30),
        "bugun_gundem_notu_var_mi": ev_path.exists(),
        "sonraki_adim": _next_step(st, today),
    })


def _system_age(st):
    files = sorted(st.snapshots.glob("*.json")) + sorted(st.forecasts.glob("*.json"))
    if not files:
        return 0
    first = min(date.fromisoformat(f.stem) for f in files)
    return (date.today() - first).days


def _next_step(st, today):
    if not st.portfolio_path.exists():
        return "init + add-asset"
    if st.snapshot(today) is None:
        return "fiyatlari topla ve snapshot al"
    if not (st.forecasts / f"{today.isoformat()}.json").exists():
        return "gundemi tara ve forecast kaydet"
    return "rapor yazilabilir"


def cmd_flow(args):
    """Var olan snapshot'a nakit akisi isle (unutulmus/geriye donuk kayit).

    Snapshot'in kendisini yeniden hesaplamaz; sadece flows + akistan
    arindirilmis getiri alanlarini gunceller. Ayni gun tekrar cagrilirsa
    flows TAMAMEN verilenle degistirilir (birlestirme yok - idempotent).
    """
    st = Store(args.root)
    p = st.portfolio()
    d = parse_date(args.date)
    snap = st.snapshot(d)
    if snap is None:
        die(f"{d} icin snapshot yok - once snapshot al, flow sonra islenir")
    flows = _parse_flows(args.flows, p["assets"])
    if not flows:
        die("--flows bos olamaz")
    snap.update(_flow_fields(snap.get("total"), snap.get("prev_total"), flows))
    snap["flow_updated_at"] = now_iso()
    write_json(st.snapshot_path(d), snap)
    out({"ok": True, "date": d.isoformat(), "flows": snap["flows"],
         "net_flow_try": snap["net_flow_try"],
         "delta_pct": snap.get("delta_pct"),
         "delta_flow_adj_pct": snap["delta_flow_adj_pct"]})


def cmd_note(args):
    st = Store(args.root)
    st.ensure()
    d = parse_date(args.date)
    path = st.evidence / f"{d.isoformat()}.md"
    text = args.text if args.text else sys.stdin.read()
    mode = "a" if path.exists() else "w"
    with path.open(mode, encoding="utf-8") as f:
        if mode == "w":
            f.write(f"# Gundem · {d.isoformat()}\n\n")
        f.write(text.rstrip() + "\n")
    out({"ok": True, "dosya": str(path)})


def cmd_holdings(args):
    """Fonlarin ic varlik dagilimini kaydet.

    Girdi JSON:
      {"date": "2026-08-04",
       "funds": {
         "KTJ": {"source": "...", "source_date": "2026-08-04",
                 "fund_size_try": 1.475e9, "investors": 18984,
                 "allocation": {"yabanci_hisse": 76.85, ...},   # KANONIK, %
                 "allocation_raw": {"Yabanci Hisse Senedi": 76.85, ...},
                 "positions": [{"ticker": "AVPGY", "name": "...",
                                "weight_pct": 3.1, "isin": "TREAVRK..."}],
                 "positions_as_of": "2026-02-28",   # tekil kalemler GECIKMELI
                 "notes": "..."}}}
    """
    st = Store(args.root)
    st.ensure()
    p = st.portfolio()
    payload = read_json(args.file) if args.file else json.loads(sys.stdin.read())
    d = parse_date(payload.get("date") or args.date)

    funds = payload.get("funds") or {}
    if not funds:
        die("funds bos - kaydedilecek bir sey yok")

    existing = read_json(st.holdings_path(d), {}) or {}
    merged = dict(existing.get("funds") or {})
    warnings, saved = [], []

    # --- ONCEKI TARIHLI KAYITTAN DEVRAL (K67, 27.08.2026) ---
    # `holdings` TARIHLI dosya yazar, `lookthrough` ise yalnizca EN GUNCEL
    # dosyayi okur. Tek bir fonun dagilimini kaydetmek (or. yeni fon eklendi)
    # o gun icin YENI bir dosya acar ve digerlerinin dagilimi o dosyada
    # OLMADIGI icin lookthrough onlari "belirsiz" sayar.
    # 27.08'de tam bu oldu: KTN kaydedildi, KTJ/KIK/KUT/ZPE'nin 541.752 TL'si
    # (portfoyun %55,4'u) bir anda "belirsiz" cikti - hicbir hata mesaji yok,
    # yalnizca lookthrough ciktisina bakan fark eder.
    # AILE: K49/K52/K53 ile ayni sinif - "kismi gonderim mevcudu ezer".
    # Cozum de aynisi: EZME, BIRLESTIR. Gelen fon kaydi ust yazar; gonderilmeyen
    # fonlar en guncel onceki dosyadan DEVRALINIR ve yaslari uyarilir, cunku
    # devralinan dagilim eskimis olabilir ve bu SESSIZ kalmamali.
    if not existing:
        prev_d, prev_doc = None, None
        for f in sorted(st.holdings.glob("*.json"), reverse=True):
            try:
                cand = date.fromisoformat(f.stem)
            except ValueError:
                continue
            if cand < d:
                prev_d, prev_doc = cand, read_json(f, {}) or {}
                break
        for fid, rec in (prev_doc or {}).get("funds", {}).items():
            if fid not in funds:
                merged[fid] = rec
                yas = (d - prev_d).days
                warnings.append(f"{fid}: dagilim {prev_d} kaydindan devralindi "
                                f"({yas} gun eski) - gonderilmedigi icin ezilmedi")

    for fid, rec in funds.items():
        if fid not in p["assets"]:
            warnings.append(f"{fid}: portfoyde boyle bir varlik yok - yine de kaydedildi")
        alloc = rec.get("allocation") or {}
        bad = [k for k in alloc if k not in LOOKTHROUGH_CLASSES]
        if bad:
            die(f"{fid}: taninmayan look-through sinifi {bad}. "
                f"Gecerli olanlar: {', '.join(LOOKTHROUGH_CLASSES)}")
        total = round(sum(alloc.values()), 2)
        if alloc and abs(total - 100.0) > 1.0:
            # TEFAS satirlari bazen %100'e tam toplanmaz (yuvarlama, eksi
            # bakiyeli taahhutlu islem). %1'e kadar sessiz, ustu uyari.
            warnings.append(f"{fid}: dagilim toplami %{total} - %100'den {abs(total-100):.2f} puan sapiyor")
        rec = dict(rec)
        rec["allocation_sum_pct"] = total
        rec.setdefault("source_date", d.isoformat())
        rec["recorded_at"] = now_iso()
        pos = rec.get("positions") or []
        if pos and not rec.get("positions_as_of"):
            warnings.append(f"{fid}: positions var ama positions_as_of yok - "
                            f"tekil kalemler gecikmeli veridir, tarihi zorunlu")
        merged[fid] = rec
        saved.append(fid)

    doc = {
        "date": d.isoformat(),
        "created_at": existing.get("created_at") or now_iso(),
        "updated_at": now_iso(),
        "funds": merged,
        "notes": payload.get("notes") or existing.get("notes") or "",
    }
    write_json(st.holdings_path(d), doc)
    out({"ok": True, "dosya": str(st.holdings_path(d)), "kaydedilen": saved,
         "toplam_fon": len(merged), "uyarilar": warnings})


def cmd_lookthrough(args):
    """Fon iclerini acarak portfoy geneli gercek varlik maruziyeti.

    Fon olmayan varliklarin maruziyeti portfolio.json'daki `lookthrough`
    alanindan gelir (ornek: gram_altin -> {"kiymetli_maden": 100}). Tanimsizsa
    varlik 'belirsiz' sayilir ve uyari verilir - sessizce sifirlanmaz.
    """
    st = Store(args.root)
    p = st.portfolio()
    d = parse_date(args.date)

    snap_date, snap = st.latest_snapshot(on_or_before=d)
    if not snap:
        die("snapshot yok - once pt.py snapshot calistir")
    hold_date, hold = st.latest_holdings(on_or_before=d)
    funds = (hold or {}).get("funds", {})

    values = {k: v for k, v in (snap.get("values") or {}).items() if v}
    total = round(sum(values.values()), 2)

    exposure = _blank_exposure()
    per_asset, warnings, uncovered = {}, [], []

    for aid, val in values.items():
        a = p["assets"].get(aid, {})
        alloc = None
        src = None
        if aid in funds and funds[aid].get("allocation"):
            alloc, src = funds[aid]["allocation"], "holdings"
        elif a.get("lookthrough"):
            alloc, src = a["lookthrough"], "portfolio.json"

        if not alloc:
            exposure["belirsiz"] += val
            per_asset[aid] = {"deger_try": val, "kaynak": None, "acilmadi": True}
            uncovered.append(aid)
            warnings.append(f"{aid}: look-through tanimi yok - 'belirsiz' sayildi "
                            f"({val:,.0f} TL)".replace(",", "."))
            continue

        s = sum(alloc.values()) or 100.0
        breakdown = {}
        for cls, pct in alloc.items():
            share = val * pct / s          # %100'e normalize et
            exposure[cls] = exposure.get(cls, 0.0) + share
            breakdown[cls] = round(share, 2)
        per_asset[aid] = {"deger_try": val, "kaynak": src, "dagilim_try": breakdown}

    rows = []
    for cls in LOOKTHROUGH_CLASSES:
        v = round(exposure.get(cls, 0.0), 2)
        if v:
            rows.append({"sinif": cls, "deger_try": v,
                         "agirlik_pct": round(100 * v / total, 2) if total else None})
    rows.sort(key=lambda r: -r["deger_try"])

    res = {
        "tarih": d.isoformat(),
        "snapshot_tarihi": snap_date.isoformat() if snap_date else None,
        "holdings_tarihi": hold_date.isoformat() if hold_date else None,
        "holdings_yasi_gun": (d - hold_date).days if hold_date else None,
        "portfoy_toplami_try": total,
        "maruziyet": rows,
        "varlik_bazli": per_asset,
        "acilmayan_varliklar": uncovered,
        "uyarilar": warnings,
    }
    if args.json_only:
        out(res)
        return res
    out(res)
    return res


# ---------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default="~/portfoy-takip", help="veri kokü (varsayilan ~/portfoy-takip)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="veri kokunu olustur")
    s.add_argument("--currency", default="TRY")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("add-asset", help="varlik ekle/guncelle")
    s.add_argument("--id", required=True)
    s.add_argument("--label")
    s.add_argument("--class", dest="asset_class", required=True,
                   help=f"{'|'.join(ASSET_CLASSES)}")
    s.add_argument("--unit")
    s.add_argument("--quantity", type=float, help="birim adedi (biliniyorsa tercih edilir)")
    s.add_argument("--value", type=float, help="TL degeri (miktar bilinmiyorsa)")
    s.add_argument("--price-source")
    s.add_argument("--custodian", help="varligi tutan kurum (banka/aracilik) - README'de kurum kirilimi icin")
    s.add_argument("--since", help="edinim tarihi YYYY-MM-DD; bu tarihten onceki snapshot'larda varlik yok sayilir")
    s.add_argument("--accrual-apr", type=float, help="sadece accrual: yillik %% getiri projeksiyonu")
    s.add_argument("--lookthrough",
                   help='fon OLMAYAN varliklar icin gercek maruziyet, JSON: '
                        '{"kiymetli_maden": 100}. Fonlarinki `holdings` komutuyla girilir.')
    s.add_argument("--notes")
    s.set_defaults(func=cmd_add_asset)

    s = sub.add_parser("remove-asset")
    s.add_argument("--id", required=True)
    s.set_defaults(func=cmd_remove_asset)

    s = sub.add_parser("list-assets", help="portfoyu goster")
    s.set_defaults(func=cmd_list_assets)

    s = sub.add_parser("snapshot", help="gunun fiyatlarini kaydet")
    s.add_argument("--date")
    s.add_argument("--prices", help='JSON: {"gram_altin": 6187.5, "KTJ": 12.34}')
    s.add_argument("--prices-file")
    s.add_argument("--flows", help='nakit akisi JSON: {"vakif_gunluk": -28000} (+yatirma/-cekme)')
    s.add_argument("--notes")
    s.set_defaults(func=cmd_snapshot)

    s = sub.add_parser("forecast", help="tahmin kaydet (JSON dosya veya stdin)")
    s.add_argument("--file")
    s.add_argument("--date")
    s.add_argument("--model-id", help="tahmini ureten model (payload'daki model_id yoksa); "
                                      "or. claude-opus-5, claude-fable-5-1")
    s.add_argument("--force", action="store_true", help="dogrulama uyarilarina ragmen kaydet")
    s.add_argument("--reason", help="revizyon gerekcesi - puanlanan alan degisiyorsa ZORUNLU, "
                                    "eski kayit `superseded`a tasinir")
    s.set_defaults(func=cmd_forecast)

    s = sub.add_parser("model-stamp",
                       help="model_id alanini geriye donuk doldur (yalniz bos olanlara)")
    s.add_argument("--model-id", required=True)
    s.add_argument("--through", help="yalniz as_of <= bu tarih olanlar (model degisim gunu siniri)")
    s.add_argument("--force", action="store_true", help="dolu olanlari da ez")
    s.set_defaults(func=cmd_model_stamp)

    s = sub.add_parser("resolve", help="vadesi gelen tahminleri eslestir")
    s.add_argument("--date")
    s.set_defaults(func=cmd_resolve)

    s = sub.add_parser("report", help="sabah raporu baglam paketi")
    s.add_argument("--date")
    s.set_defaults(func=cmd_report)

    s = sub.add_parser("decision", help="karar kaydet (alternatifleriyle, sonuc gorulmeden)")
    s.add_argument("--file")
    s.add_argument("--date")
    s.add_argument("--model-id")
    s.add_argument("--price-root", default="data",
                   help="fiyat referansi olarak kullanilacak kok (iki defter kurali: "
                        "fiyatlar ortaktir). Sahiplik DEGISMEZ.")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_decision)

    s = sub.add_parser("decisions", help="kararlari listele ve vadesi gelenleri puanla")
    s.add_argument("--date")
    s.add_argument("--price-root", default="data")
    s.add_argument("--force", action="store_true", help="puanlanmis ufuklari da yeniden hesapla")
    s.set_defaults(func=cmd_decisions)

    s = sub.add_parser("evidence-acik",
                       help="consensus yazilmis ama actual girilmemis takvimli kanitlar (H4 paydasi)")
    s.add_argument("--date")
    s.add_argument("--all", action="store_true",
                   help="olay tarihi gelmemis olanlari da listele")
    s.set_defaults(func=cmd_evidence_acik)

    s = sub.add_parser("baselines",
                       help="mevcut cozumlemelere drift/momentum baseline'larini geriye donuk ekle")
    s.add_argument("--force", action="store_true",
                   help="zaten hesaplanmis satirlari da yeniden hesapla")
    s.set_defaults(func=cmd_baselines)

    s = sub.add_parser("calibrate", help="kalibrasyon metrikleri")
    s.add_argument("--date")
    s.add_argument("--window", type=int, default=30)
    s.add_argument("--asset")
    s.set_defaults(func=cmd_calibrate)

    s = sub.add_parser("note", help="gundem notu yaz")
    s.add_argument("--date")
    s.add_argument("--text")
    s.set_defaults(func=cmd_note)

    s = sub.add_parser("flow", help="var olan snapshot'a nakit akisi isle")
    s.add_argument("--date")
    s.add_argument("--flows", required=True,
                   help='JSON: {"vakif_gunluk": -28000} (+yatirma/-cekme)')
    s.set_defaults(func=cmd_flow)

    s = sub.add_parser("holdings", help="fonlarin ic varlik dagilimini kaydet")
    s.add_argument("--file", help="JSON dosya (yoksa stdin)")
    s.add_argument("--date")
    s.set_defaults(func=cmd_holdings)

    s = sub.add_parser("lookthrough", help="fon iclerini acarak gercek maruziyet")
    s.add_argument("--date")
    s.add_argument("--json-only", action="store_true")
    s.set_defaults(func=cmd_lookthrough)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
