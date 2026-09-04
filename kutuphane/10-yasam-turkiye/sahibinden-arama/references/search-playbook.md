# Arama Oyun Kitabı

## 1. Sonuç tavanını aşmak

sahibinden bir sorgu için yalnızca ilk ~1000 ilanı sayfalar. "İstanbul'daki tüm
satılık daireler" (~200.000 ilan) tek sorguyla alınamaz.

**Bölme stratejisi — sırayla uygula, her adımda alt sorgu < 1000 olana kadar:**

```
1. Coğrafya      il → ilçe → mahalle
2. Fiyat bandı   geometrik bölme (aritmetik değil!)
3. Oda sayısı    1+1, 2+1, 3+1, 4+1, 5+
4. m² bandı      0-75, 75-110, 110-150, 150-220, 220+
5. Tarih penceresi  date=1 ile günlük çekim (yalnız takip modunda)
```

Fiyat bölmesi **geometrik** olmalı çünkü ilan yoğunluğu log-normal dağılır.
2M–20M arası 4 banda bölerken 2/4.5/8.5/14/20 değil, `exp(linspace(ln2, ln20, 5))`
→ 2 / 3.8 / 7.1 / 13.4 / 20 kullan. `emlakarama plan` bunu yapar:

```bash
emlakarama plan 'https://www.sahibinden.com/satilik-daire/istanbul' --target 800
```

Çıktı: her biri hedefin altında kalması beklenen alt sorgu URL listesi + toplam
sayfa tahmini.

**Doğrulama:** her alt sorgunun ilk sayfasındaki toplam sayacı oku
(`total_results`). 1000'i aşan varsa o dalı bir kez daha böl. `emlakarama sync`
bunu özyinelemeli olarak, `--max-depth` sınırıyla yapar.

**Sınır bandı hatası:** fiyat bantları `[min, max)` yarı açık olmalı, yoksa
`price_max=3000000` ve `price_min=3000000` iki sorguda da aynı ilanı getirir.
Tekilleştirme ID üzerinden yapıldığı için zararsız ama istek israfıdır.

## 2. Sıralama seçimi

| Amaç | `sorting` | Neden |
|---|---|---|
| Yeni ilan avı | `date_desc` | İlk sayfa = son eklenenler; 1 sayfa yeter |
| Tam kapsama (arşiv) | `price_asc` | Deterministik, sayfalar arası kayma yok |
| Ucuz fırsat taraması | `price_asc` | İlk 2 sayfa çoğu zaman yeter |
| Kesinlikle kullanma | (boş) | Site karma sıralar, sayfalar tekrar eder |

Tam kapsamada **asla `date_desc` kullanma**: çekim sürerken yeni ilan eklenirse
tüm sayfalama bir kayar ve ilan atlarsın. `price_asc` sabit bir eksendir.

## 3. Takip döngüsü (fiyat düşüşü / yeni ilan)

```bash
# Bir kez: aramayı kaydet
emlakarama search add kadikoy-3+1 \
  'https://www.sahibinden.com/satilik-daire/istanbul-kadikoy?price_max=9000000&sorting=date_desc&pagingSize=50'

# Her çalıştırmada (günde 1–2 kez yeterli)
emlakarama sync kadikoy-3+1 --cdp --max-pages 6
emlakarama diff kadikoy-3+1 --since last
emlakarama report kadikoy-3+1 --new --price-drop --format md
```

`diff` sınıfları:

| Sınıf | Tanım |
|---|---|
| `new` | ID önceki snapshot'ta yok |
| `price_drop` | Aynı ID, fiyat düştü (mutlak + % ile) |
| `price_rise` | Aynı ID, fiyat arttı |
| `relisted` | ID kaybolmuştu, geri geldi (genelde "yenileme" — ilan tarihi sıfırlanır) |
| `removed` | ID artık sonuçta yok (satıldı **veya** filtre dışına çıktı **veya** süresi doldu) |
| `updated` | Başlık/m²/oda değişti |

**`removed` yanılgısı:** ilan fiyatı `price_max`'in üstüne çıkarsa "removed"
görünür ama satılmamıştır. Takip aramalarını filtre sınırlarından biraz geniş kur
(`price_max`'i %15 yukarı al), raporda dar sınırı uygula.

**`relisted` sinyali:** sahibinden'de ilan "güncelleme"/"yenileme" ile tarihi
tazelenir. Aynı ID'nin tarihi ileri gidip fiyatı sabitse satıcı ilanı öne
çıkarmaya çalışıyordur → satmakta zorlanıyor → pazarlık payı yüksek.

## 4. Skorlama

`emlakarama report --score` şu sinyalleri 0–100'e normalize edip ağırlıklı toplar:

| Sinyal | Ağırlık | Yön | Not |
|---|---|---|---|
| TL/m² (aynı ilçe medyanına göre z-skoru) | 0.35 | düşük iyi | Ana sinyal |
| Fiyat düşüş yüzdesi (takip geçmişinden) | 0.20 | yüksek iyi | Geçmiş yoksa 0 |
| İlan yaşı (gün) | 0.10 | yüksek iyi | Uzun süredir duran = pazarlık payı |
| Yenileme sayısı | 0.10 | yüksek iyi | `relisted` sayacı |
| Fotoğraf sayısı | 0.05 | yüksek iyi | Ciddiyet göstergesi |
| Satıcı = sahibinden | 0.10 | evet iyi | Komisyon yok |
| Açıklama uzunluğu | 0.05 | yüksek iyi | Bilgi kalitesi |
| Eksik alan cezası | 0.05 | — | m²/oda yoksa düş |

Ağırlıklar `data/scoring.json` içinde; `--weights` ile dosya değiştirilebilir.

**Uyarı:** TL/m² medyanı **aynı ilçe + aynı oda sayısı + benzer bina yaşı**
kohortundan hesaplanmalı. Kadıköy'de 1+1 ile 4+1'in TL/m²'si karşılaştırılamaz.
Kohortta < 8 ilan varsa z-skoru güvenilmezdir; araç o satırda sinyali `null`
bırakır ve ağırlığı diğerlerine dağıtır.

**Bu bir değerleme değildir.** İlan fiyatı, satış fiyatı değildir; Türkiye'de
ilan–satış farkı %5–20 bandındadır ve piyasaya göre değişir. Raporu sunarken
bunu söyle.

## 5. Tipik arama tarifleri

### "Kadıköy'de bütçem 8 milyon, 2+1 veya 3+1, yeni ilanlar"
```bash
emlakarama url satilik-daire istanbul-kadikoy \
  --price-max 8000000 --sort date_desc --page-size 50 \
  --attr "Oda Sayısı=2+1" --attr "Oda Sayısı=3+1"
```
Çoklu enum aynı `aNN`'i tekrar eder.

### "Bodrum'da havuzlu villa, deniz manzaralı"
Serbest metin + filtre birlikte:
```bash
emlakarama url satilik-villa mugla-bodrum --q "havuzlu deniz manzara"
```
`query_text` başlıkta **ve** açıklamada arar; gürültülüdür. Önce filtreleri
daralt, metni son çare olarak ekle.

### "İzmir'in tamamında son 24 saatte eklenen kiralıklar"
```bash
emlakarama plan 'https://www.sahibinden.com/kiralik-daire/izmir?date=1&sorting=date_desc' --target 800
```
`date=1` çoğu ilçede tavanın altında kalır; bölme gerekmeyebilir.

### "Ankara Çankaya, m²'si 120+, bina yaşı 0-5"
Önce keşif (`discover-filters`), sonra:
```bash
emlakarama url satilik-daire ankara-cankaya \
  --attr "m² (Brüt)=120.." --attr "Bina Yaşı=0..5"
```
Aralık sözdizimi: `min..max`, `min..`, `..max`.

### "Elimdeki 40 ilanı tabloya çıkar"
```bash
emlakarama parse samples/*.html --format csv > ilanlar.csv
```

## 6. Etik ve sınırlar

- Kişisel/araştırma amaçlı, düşük hacimli erişim. Toplu yeniden yayın yapma.
- İlan sahiplerinin telefon/isim bilgilerini toplayıp liste üretme.
- Hız sınırına uy; engel sayfası görülürse dur, kullanıcıya bildir, bekle.
- Site markup'ı veya kuralları değiştiyse aracı zorlamak yerine güncelle.
