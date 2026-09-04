# Veri Kaynakları ve Fiyat Toplama

Snapshot almadan önce oku. Amaç: her varlık için **bir sayı** bulmak, bulamazsan `null` bırakmak. Yaklaşık değer uydurmak, bu sistemi baştan bozar — çünkü sonraki tüm hata ölçümleri o sayıya dayanır.

## Genel kural

Fiyatı iki bağımsız kaynaktan gördüysen ve %0.5'ten fazla ayrışıyorlarsa, ikisini de not et ve daha resmi olanı (borsa, TEFAS, TCMB) kullan. Ayrışma sebebi genelde alış/satış farkı veya gecikmeli veridir.

Her snapshot'ta fiyatın **hangi ana ait** olduğuna dikkat et. Sabah 09:00'da aldığın gram altın fiyatı ile akşam 18:00'de aldığın karşılaştırılamaz. Tutarlılık için her gün aynı saat diliminde snapshot almaya çalış ve `--notes` alanına saati yaz.

---

## Varlık sınıfına göre

### `spot` — Gram altın, gümüş, döviz

Gram altın TL fiyatı = XAU/USD × USD/TRY ÷ 31.1035 (yaklaşık; TL'de yerel prim/iskonto olabilir, bazen %1-3'e kadar açılır).

Arama kalıpları:
- `gram altın fiyatı` / `gram altın kaç TL`
- `XAU USD spot price`
- `dolar kuru TCMB` veya `USDTRY`

Kaynak tercihi: TCMB (kur için resmî), Bloomberg HT / Reuters / Investing (altın). Kuyumcu sitelerinin "satış" fiyatı portföy değerlemesi için fazla yüksektir — **alış** fiyatı gerçek nakde çevirme değerine daha yakındır, ama tutarlı ol: hep aynısını kullan ve hangisi olduğunu portföyde `price_source` alanına yaz.

Serbest piyasa 7/24 hareket eder ama Türkiye'de kapalıçarşı seansı dışında likidite düşüktür. Hafta sonu fiyatı Cuma kapanışına yakın kalır.

### `fund_tefas` — KTJ, KIK, KUT ve diğer yatırım/katılım fonları

**En kritik tuzak burada.** TEFAS fon fiyatları:

- Sadece **iş günlerinde** açıklanır (hafta sonu ve resmî tatil yok).
- **T+1 gecikmelidir**: bugün gördüğün en güncel fiyat, genelde önceki iş gününün kapanış birim pay değeridir. Yani Pazartesi sabahı baktığında Cuma'nın fiyatını görürsün.
- Alım/satım emirleri de gecikmeli gerçekleşir (fon tipine göre T+1 / T+2), yani "bugün gördüğüm fiyattan alırım" diye bir şey yok.

Bunun tahmin açısından anlamı: bir fon için "1 günlük" tahmin aslında **zaten kısmen gerçekleşmiş** bir hareketi tahmin etmektir. Bu bir avantaj gibi görünür ama değildir — ilgili endeksin (ör. Nasdaq) dünkü kapanışını biliyorsan, fonun bugün açıklanacak fiyatı büyük ölçüde belirlidir. Bunu tahmin olarak sunma; "mekanik olarak beklenen" diye ayrı belirt ve kalibrasyon skorunu bununla şişirme.

`resolve` komutu bu gecikmeyi bilir: hedef günde fiyat yoksa 6 iş gününe kadar ileriye bakar.

Arama kalıpları:
- `TEFAS KTJ fon fiyatı`
- `KT Portföy teknoloji katılım fonu birim pay değeri`
- `tefas.gov.tr <fon kodu>`

Fon kodunun tam adını portföye `label` olarak yaz — arama kalitesi buna bağlı.

### `accrual` — Katılma hesabı, mevduat

Bunlar tahmin edilmez, **projekte edilir**. Kâr payı oranı dönemsel açıklanır ve garanti değildir (katılım bankacılığında kâr/zarar ortaklığı esastır). `accrual_apr` alanına beklenen yıllık oranı yaz; script basit doğrusal birikim uygular.

Gerçek bakiye eline geçtiğinde (banka uygulamasından) `--prices '{"vakif_gunluk": <gerçek bakiye>}'` ile ez. Projeksiyon her zaman gerçek bakiyeye yenilir.

Kâr payı ortaklık oranı (ör. %85 katılımcı / %15 banka) getiriye zaten yansımış olarak açıklanır — net oranı gir, brütü değil.

### `equity` / `crypto`

Hisse: BIST için `<kod> hisse fiyatı`, ABD için ticker. Seans saatleri dışında son kapanış geçerli.
Kripto: 7/24, hafta sonu da snapshot alınabilir.

---

## Tatil ve boşluk yönetimi

- **Hafta sonu**: `spot` ve `crypto` için snapshot al, `fund_tefas` ve `equity` için `null` bırak. Script önceki değeri taşır.
- **Resmî tatil / bayram**: aynısı. Türkiye'de Ramazan ve Kurban Bayramı'nda borsa ve TEFAS birkaç gün kapalıdır; bu dönemde tahmin üretmeye devam et ama hedef tarihi bir sonraki iş gününe kaydır (script otomatik yapar).
- **Bir günü tamamen kaçırdın**: geriye dönük snapshot alma (`--date` ile eski tarih verip fiyat uydurma). Boşluk bırak. Boşluk, uydurulmuş veriden iyidir.

---

## Piyasa bağlamı için sabit takip listesi

Fiyatların yanında bunları da her gün `market_state` içine kaydet — sonradan "hangi makro değişken hangi varlığı sürüklüyordu" analizini ancak bu veri varsa yapabilirsin:

| Değişken | Neden |
|---|---|
| `usdtry` | TL bazlı her şeyin ortak faktörü |
| `xauusd` | Gram altının uluslararası bacağı |
| `dxy` | Dolar endeksi — altınla ters ilişkili |
| `us10y` | ABD 10Y reel faiz — altının en güçlü makro sürücüsü |
| `nasdaq` veya `ndx` | Teknoloji fonları için |
| `bist100` | Yerel risk iştahı |
| `brent` | Enflasyon ve TL üzerinden dolaylı |

Hepsini bulamazsan bulduklarını yaz. Eksik alan boş kalsın.
