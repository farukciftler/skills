# Ekstre biçimleri ve tuzakları

Üç banka, üç ayrı üretici, üç ayrı sayı biçimi. Hepsi 02.09.2026'da bu
makinede `pdftotext -layout` (poppler) ile test edildi.

## Ortak kurallar

- **Bakiye zinciri her belgede doğrulanır:** `bakiye[i-1] + tutar[i] = bakiye[i]`
  (±0,01). Kırık = ayrıştırma hatası; zincir tutana kadar analiz yapılmaz.
  İlk yüklemede zincir 4 kez kırıldı ve dördünde de sebep ayrıştırıcıydı
  (satır ortasında bölünmüş tutar, girintisiz devam satırı, belge içi sıra
  yerine tarihe göre sıralama, `\x03` boşluk glifi).
- **Belge içi sıra korunur** (`sira` sütunu). Aynı gün içindeki hareketleri
  tarihe göre yeniden sıralamak zinciri bozar; Akbank en yeniyi en üste yazar,
  o da olduğu gibi kalır (zincir tersten doğrulanır).
- **Toplamlar başlıkla tutmalı:** Vakıf Katılım "Toplam Çekilen/Yatırılan",
  VakıfBank son bakiye, Akbank son satır bakiyesi.
- Sayı biçimi: Vakıf Katılım `1,234.56` (US); VakıfBank ve Akbank `1.234,56` (TR).

## VakıfBank — "Hesap Hareketleri" (Aspose.Words, 81 sayfa/yıl)

```
TARİH  SAAT  İŞLEM NO  MİKTAR  BAKİYE  İŞLEM ADI
02.09.2025  12:13  2025012390561789  -2.000,00  115.998,82  FAST Anlık Ödeme
(02/09/2025 tarihli … ABDULLAH FARUK ÇİFTLER hesabından Albaraka … DÖNAY YILDIZ ÇİFTLER hesabına giden FAST ödemesi)
```

- İşlem satırı + bir ya da iki **açıklama satırı**; açıklama boş satırla biter.
- Bazı işlem adları **satırın üstüne** taşar ("Kambiyo Muameleleri Vergisi"
  sonraki işlem satırından önce tek başına durur) → ayrıştırıcı "öksüz satır"
  olarak tutar, sonraki satıra ekler.
- Sayfa başlığı her sayfada tekrarlanır (Hesap Hareketleri, VB Müş. No, …,
  `Sf. n / 81`) — atlanır.
- POS satırlarında `Mcc: NNNN`, işyeri adı `ISLEM NO :  -<İŞYERİ>  <ŞEHİR>`;
  yurt dışı POS'ta `Kur ..:48,832420` ile kur.
- Karşı taraf FAST'ta `… hesabından <BANKA> <AD SOYAD> hesabına giden` /
  `<AD> hesabından … gelen`.
- Fatura tahsilatları ayrı işlem adı taşır (Turkcell/Vodafone/İgdaş/İSKİ/
  Clk Boğaziçi Elektrik/Netspeed Tahsilatı) — kategori doğrudan buradan.
- **TCKN başlıkta yazar.** Depo özel; yine de dışarı vermeden önce bil.

## Vakıf Katılım — "HESAP EKSTRESİ" (Reporting Services)

**Font kayması.** Başlıklar ve açıklamaların bir kısmı kaymış bir glif
tablosuyla geliyor:

| Görünen | pdftotext | Kural |
|---|---|---|
| TARİH | `7$5ø+` | ASCII **+29**: `7`→T, `$`→A, `5`→R |
| Günlük Hesap Kapsamında Virman | `*\x81QO\x81N\x03+HVDS…` | `\x03`→boşluk, `\x81`→ü |
| 1351308 | `\x14\x16\x18\x14\x16\x13\x1b` | kontrol karakterleri +29 → rakam |
| ÇİFTLER | `dø)7/(5` | glif: `d`→Ç, `ø`→İ, `Õ`→ı, `ú`→ş, `ù`→Ş, `|`→ö, `h`→Ü, `g`→Ö |

Çözücü `belgeler.py::decode_token`: bir kelime **yalnız** kaymış alfabede
yazılabilecek karakterlerden oluşuyorsa (0x00–0x61 + özel glifler) çevrilir;
gerçek küçük harf (`s`, `p`, `o` …) içeren kelime kaymış olamaz, dokunulmaz.
Bu ayrım olmadan `Hsp.No` → `espKko` oluyordu (ilk sürümün hatası).
Bazı glifler **düşüyor** (`Gnlk` = Günlük): olduğu gibi bırakılır.

**Satır ortasında bölünme.** Uzun açıklamalarda tutar ve bakiye bir **alt
satıra**, bazen **girintisiz** düşer:
```
09-01-2026       A00AI       \x19\x11\x14\x16
,1271 Türk Lirası Kurundan                          2,885.38        2,933.04 Körfez
```
Ayrıştırıcı tutarsız tarih satırını "bekleyen" tutar, ilk tutar+bakiye
taşıyan devam satırından doldurur; sayı bölünmüşse boşluksuz birleştirir
(bir rakam kaybolabilir — `6.13,1271` gibi; kurdan gram×kur ile doğrulanır).

**Şube sütunu** `Körfez` / `Genel` + alt satırda `Müdürlük` / `Fon`.

**Kalıplar** (çözülmüş metin):
- `Amir ABDULLAH FARUK ÇİFTLER Aciklama=` → kendi hesabından gelen (giriş)
- `Lehdar= ABDULLAH FARUK ÇİFTLER Aciklama Fast Anlık Ödeme` → kendi hesabına giden
- `Lehdar BETÜL ÇİFTLER …` → eş
- `Gönderen Hesap: 1351308 - 1 / Alıcı Hesap 1351308 - 4000 / Virman` → yatırım hesabına (fon alımı)
- `Hesaptan ENPRNPMUJNF hesaba ENPRNPMUJQMMMF` → maskeli hesap kodları; `…JNF` = 1351308-1, `…JQMMMF` = 1351308-4000 (yön: tutar işareti)
- `6.133,3267 Türk Lirası Kurundan 1,62 Gr Altın Alımı` / `Satışı`; `BSMV…` aynı işlemin vergisi
- `52,8014 TL Kurundan 2000 Euro Satışı`, `47,6250 TL Kurundan 419,94 Amerikan Doları …`
- `Kar Payı Hsp <tarih> tarihli TL Fonu N günlük` / `Vergi 1351308 - 1000 Hsp …` (günlük katılma kâr payı ve stopajı; **hafta sonu 3 günlük** birikimi Pazartesi yazar — CLAUDE.md K6 ile uyumlu)
- `Günlük Hesap Kapsamında Virman` → 1351308-2 ↔ 1351308-1000 arası

İngilizce başlıklı sürüm (USD hesabı, "ACCOUNT STATEMENT") aynı gövde,
alanlar `Account Number / Account Name / Balance at beginning of the term`.

## Akbank — "HESAP HAREKETLERİ" (iOS Quartz, taranmış görüntü + metin)

```
TARİH  SAAT  VALÖR  FİŞNO  MEBLAĞ  BAKİYE  BIA  AÇIKLAMA
01.09 2026 16-07  02.09.2026  594834  170.000,00  170.005,57   0571/MAAŞ ODEMESI
```
- OCR gürültüsü: `01.09 2026`, `16-07`, `04.082026`, `-0,00`. Regex toleranslı.
- **En yeni işlem en üstte.**
- 2. sayfa bankanın kendi imza sirküleri (şube yetkilileri) — hareket değil.
- Maaş buraya yatıyor (Ağustos'tan beri), ertesi gün Vakıf Katılım'a
  gidiyor → ikinci giriş `ic_transfer/maas_gecisi`.

## Fon pozisyon dökümü (Vakıf Katılım, kaşeli tarama)

Sütunlar: Kıymet Türü · ISIN · Müşteri No · Müşteri Adı · Alış Tarihi · Döviz ·
Nominal Bakiye · Maliyet Değeri · Günlük Getiri Tutar · Piyasa Değeri ·
Ay Bazlı Günlük Ortalama Bakiye · Serbest Depo · Fon Ünvanı · Fon Kodu.
**Lot bazlı**dır (aynı fon birden çok satır). `Serbest Depo` fonun toplam
adedi; lot adetlerinin toplamıyla tutmalı. Piyasa değeri belge tarihinin
NAV'ıyla hesaplanır (02.09 dökümü 02.09 NAV'ını kullanıyordu; TEFAS'tan
doğrulanır). Sayfa **yatay** taranmış: `sips -r 270` ile döndür, üç şeride
kırp, `Read` ile oku.

## Tarama / OCR

```bash
pdftoppm -r 300 -png <pdf> <önek>            # sayfa → PNG
swiftc -O ocr.swift -o ocr && ./ocr <png>…    # macOS Vision, tr-TR + en-US
```
`ocr.swift` (VNRecognizeTextRequest, `.accurate`, `usesLanguageCorrection`)
oturum içinde yazılıp derlenir; çıktı satır başında `[güven]`. **Tablolarda
OCR sırayı korumaz** — sütun sütun okur; tablo taramaları görüntüden elle
okunur. Metin belgeleri (noter sirküleri) OCR ile yeterlidir.
