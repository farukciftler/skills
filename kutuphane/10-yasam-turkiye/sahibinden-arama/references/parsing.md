# Ayrıştırma (Parsing)

Tüm seçiciler `data/selectors.json` içinde yapılandırma olarak durur. Site markup'ı
değişirse **kodu değil o dosyayı** güncelle; parser her alan için sıralı bir
seçici listesi dener ve ilk tutanı kullanır.

## Arama sonuç sayfası

Kök: `table#searchResultsTable` → satırlar `tr.searchResultsItem`.

| Alan | Seçici (birincil) | Yedek | Notlar |
|---|---|---|---|
| `listing_id` | `tr[data-id]` | detay linkindeki son sayı grubu | **Birincil anahtar** |
| `url` | `a.classifiedTitle@href` | `td a[href*="/detay"]@href` | Göreli → `https://www.sahibinden.com` ile birleştir |
| `title` | `a.classifiedTitle` metni | `a[href*="/detay"]@title` | `strip()` |
| `price_raw` | `td.searchResultsPriceValue` | `div.classified-price-container` | "1.250.000 TL" |
| `attrs[]` | `td.searchResultsAttributeValue` | — | Sırayla m², oda, bina yaşı, kat (kategoriye göre değişir) |
| `date_raw` | `td.searchResultsDateValue` | — | İki `span`: "12 Ağustos" + "2026" |
| `location_raw` | `td.searchResultsLocationValue` | — | `<br>` ile ayrılmış il / ilçe / mahalle |
| `thumbnail` | `td.searchResultsLargeThumbnail img@data-src` | `img@src` | Lazy-load olduğu için `data-src` önce |
| `store` | `td.searchResultsTagValue` | — | Doluysa mağaza/emlak ofisi |
| `is_promoted` | `tr` sınıflarında `nativeAd` / `sponsored` | — | Reklam satırları sayaçtan düşülmeli |
| `total_results` | `.result-text` metnindeki ilk sayı | `#searchResultsSearchForm` civarı | "1.234 ilan" |

**Yedek mod:** tablo bulunamazsa parser sayfadaki tüm
`a[href*="/ilan/"][href$="/detay"]` bağlantılarını toplar, `href`'ten ID ve
başlığı çıkarır, en yakın atadan fiyat/tarih metnini regex ile arar. Eksik alanlı
ama kullanılabilir kayıt üretir; `parse_mode: "fallback"` işaretlenir.

**Reklam satırları:** sonuçların başında/arasında sponsorlu satırlar bulunur.
Bunlar `data-id` taşır ama arama kriterlerine uymayabilir. Parser onları
`is_promoted=true` işaretler; `--no-promoted` ile filtrelenir. Sayfalama
hesabında **asla sayma**.

## İlan detay sayfası

| Alan | Seçici |
|---|---|
| `title` | `.classifiedDetailTitle h1` |
| `price_raw` | `.classifiedInfo h3` |
| `listing_id` | `.classifiedInfoList li` içinde "İlan No" satırı |
| `posted_date` | "İlan Tarihi" satırı |
| `attributes{}` | `.classifiedInfoList li` → `strong` (etiket) + `span` (değer) |
| `features[]` | `.classifiedProperties li.selected` (işaretli özellikler) |
| `description` | `#classifiedDescription` (HTML → düz metin) |
| `location` | `.classifiedInfo h2 a` zinciri (il / ilçe / mahalle) |
| `images[]` | `.classifiedDetailMainPhoto img@src` + galeri `data-src`'leri |
| `seller_type` | `.classifiedUserBox` içinde mağaza kutusu var mı |

`.classifiedInfoList` etiketleri kategoriye göre değişir; sabit bir şema yerine
`Dict[str, str]` olarak sakla, sonra `data/field_map.json` ile normalize et:

```json
{"m² (Brüt)": "gross_m2", "m² (Net)": "net_m2", "Oda Sayısı": "rooms_raw",
 "Bina Yaşı": "building_age", "Bulunduğu Kat": "floor", "Isıtma": "heating",
 "Aidat (TL)": "dues", "Krediye Uygun": "mortgage_eligible"}
```

## Normalizasyon kuralları

### Fiyat
```
"1.250.000 TL"     → {amount: 1250000,   currency: "TRY"}
"1,250,000 TL"     → {amount: 1250000,   currency: "TRY"}
"85.000 USD"       → {amount: 85000,     currency: "USD"}
"12.500 EUR"       → {amount: 12500,     currency: "EUR"}
"Fiyat Belirtilmemiş" / "" → {amount: null}
```
Kural: harf ve para birimi işaretlerini ayır; kalan dizeden `.` ve `,`
**ayırıcı olarak** at (Türkçe binlik ayırıcı `.`); ondalık sahibinden fiyatlarında
kullanılmaz.

### Tarih
Türkçe ay adları: `Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık`
```
"12 Ağustos 2026" → 2026-08-12
"12 Ağustos" (yıl ayrı span'de) → span'leri birleştir
"Bugün" → çekim tarihi
"Dün"  → çekim tarihi - 1
```

### Oda sayısı
```
"3+1"     → {rooms: 3, living: 1, label: "3+1"}
"1+0"     → {rooms: 1, living: 0}
"Stüdyo"  → {rooms: 1, living: 0, studio: true}
"5+ üzeri"→ {rooms: 5, living: null, open_ended: true}
```

### m²
```
"120 m²"      → 120
"120"         → 120
"120 / 100"   → {gross: 120, net: 100}   (bazı satırlarda brüt/net birlikte)
```

### Bina yaşı
```
"0"      → 0          "Sıfır Bina" → 0
"5-10"   → {min: 5, max: 10}
"21 Ve Üzeri" → {min: 21, max: null}
```

### Kat
```
"Zemin" → 0    "Bodrum" → -1    "Bahçe Katı" → 0    "Giriş Katı" → 0
"3"     → 3    "Çatı Katı" → "attic"   "Yüksek Giriş" → 0
```

### Konum
`td.searchResultsLocationValue` metni `<br>` ile bölünür; genelde
`["İstanbul", "Kadıköy", "Caferağa Mah."]` sırasıyla gelir ama bazı kayıtlarda
mahalle yoktur. Uzunluğa göre sondan eşle:
- 3 parça → il, ilçe, mahalle
- 2 parça → il, ilçe
- 1 parça → il

## Kalite kontrolleri

Parser her çalıştırmada şunları raporlar; eşik altına düşerse **uyarır** (sessizce
devam etmez):

| Kontrol | Eşik |
|---|---|
| Satır sayısı vs `total_results`/sayfa | ±%20 |
| `listing_id` dolu oranı | ≥ %99 |
| `price.amount` dolu oranı | ≥ %90 |
| `title` dolu oranı | ≥ %99 |
| Yinelenen ID oranı | ≤ %2 |

Bunlar bozulduysa muhtemelen (a) engel sayfası çekildi, (b) markup değişti,
(c) mobil sürüm kaydedildi. Sırayla kontrol et.

## Kodlama

sahibinden sayfaları UTF-8'dir ama elle kaydedilmiş dosyalarda bazen
`windows-1254` çıkar. Parser BOM ve `<meta charset>` okur, yoksa UTF-8 dener,
başarısız olursa `cp1254`'e düşer. "Kadýköy" gibi bozuk metin görürsen kodlama
düşüşü olmuştur → `--encoding cp1254` ile zorla.
