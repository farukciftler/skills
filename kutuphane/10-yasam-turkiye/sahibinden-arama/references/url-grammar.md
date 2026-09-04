# URL Dilbilgisi

## Genel biçim

```
https://www.sahibinden.com/{kategori-slug}[/{konum-yolu}][?{sorgu}]
```

- Şema her zaman `https`, host her zaman `www.sahibinden.com`
  (`sahibinden.com` → `www.` redirect; `m.sahibinden.com` mobil sürüm, markup farklı,
  parser desteklemez).
- `{kategori-slug}` zorunlu. Tek başına da geçerli: `/satilik-daire` = tüm Türkiye.
- `{konum-yolu}` opsiyonel, tek segment, tirelerle birleşik: `istanbul-kadikoy-moda`.
- Sorgu parametreleri sırası önemsiz; ancak paylaşılan URL'lerin dengi olması için
  `emlakarama` deterministik sıra kullanır (aşağıdaki tablo sırası).

## İlan detay URL'i

```
https://www.sahibinden.com/ilan/{kategori-yolu}-{başlık-slug}-{ilanNo}/detay
```

- `{ilanNo}` 9–10 haneli sayı ve **kalıcı birincil anahtardır**. Başlık slug'ı
  ilan düzenlenince değişir; ID değişmez. Tekilleştirmeyi her zaman ID ile yap.
- Sadece ID varsa şu kısa biçim de detay sayfasına gider:
  `https://www.sahibinden.com/ilan/{ilanNo}/detay` — ancak bazı kategorilerde 404
  döner, güvenilir yol tam slug'ı saklamaktır.

## Sabit (kategoriden bağımsız) sorgu parametreleri

| Parametre | Değer | Anlamı | Güven |
|---|---|---|---|
| `pagingOffset` | `0`, `20`, `40`, … (pagingSize katı) | Atlanacak ilan sayısı | ✅ doğrulanmış |
| `pagingSize` | `20` \| `50` | Sayfa başı ilan | ✅ |
| `sorting` | aşağıdaki tablo | Sıralama | ✅ |
| `price_min` | tam sayı | Alt fiyat (para birimi filtreye bağlı) | ✅ |
| `price_max` | tam sayı | Üst fiyat | ✅ |
| `price_currency` | `1`=TL, `2`=USD, `3`=EUR | Fiyat filtresinin para birimi | ⚠️ olası |
| `query_text` | serbest metin | Anahtar kelime | ✅ |
| `query_text_mf` | `query_text` ile aynı | Site ikisini birlikte gönderir | ✅ |
| `date` | `1`,`3`,`7`,`15`,`30` | Son N gün içindeki ilanlar | ⚠️ olası |
| `address_country` | `1` = Türkiye | Ülke | ⚠️ olası |
| `address_city` | il ID | Konum yolu yerine ID ile il | ⚠️ olası |
| `address_town` | ilçe ID | Çoklu ilçe seçiminde tekrarlanır | ⚠️ olası |
| `address_quarter` | mahalle ID | Çoklu mahalle seçiminde tekrarlanır | ⚠️ olası |
| `m:{ad}` | — | Bazı sayfalarda kampanya/segment işareti | ⚠️ yoksay |
| `viewType` | `List` \| `Gallery` \| `Table` | Görünüm; markup'ı değiştirir | ⚠️ olası |

> ⚠️ işaretli olanlar gözlemlenmiş ama her kategoride doğrulanmamıştır.
> Kritik bir işte kullanmadan önce `emlakarama learn <gerçek-url>` ile teyit et.
> Konum için **her zaman önce yol tabanlı biçimi** (`/satilik-daire/istanbul-kadikoy`)
> dene — en kararlı olan odur.

## `sorting` değerleri

| Değer | Anlamı |
|---|---|
| `date_desc` | Tarihe göre en yeni (yeni ilan avında varsayılan seçim) |
| `date_asc` | Tarihe göre en eski |
| `price_asc` | Fiyata göre artan |
| `price_desc` | Fiyata göre azalan |
| `a{ID}_asc` / `a{ID}_desc` | Attribute'a göre (ör. m² için `a4_asc`) — ID kategoriye bağlı |

Parametre hiç verilmezse site kendi varsayılan sıralamasını (genelde "gelişmiş"
karma sıralama) uygular ve **sayfalar arası tutarlılık garanti değildir**. Toplu
çekimde her zaman açık bir `sorting` ver; aksi halde sayfa 3'te sayfa 1'deki ilanı
tekrar görebilirsin.

## Sayfalama

```
sayfa 1 → pagingOffset=0
sayfa 2 → pagingOffset=pagingSize
sayfa n → pagingOffset=(n-1)*pagingSize
```

- `pagingSize=50` kullan: aynı veri için 2.5× daha az istek.
- Pratik tavan: `pagingOffset` ~950–1000'i geçince site ya boş sonuç ya da ilk
  sayfaya dönüş yapar. Toplam sonuç 1000'i aşıyorsa bölmek zorundasın
  (bkz. `search-playbook.md`).
- Toplam sonuç sayısı sayfada `.result-text` / `#searchResultsSearchForm` civarında
  "1.234 ilan" biçiminde yazar; parser bunu `total_results` olarak okur.

## Kanonikleştirme

Aynı aramanın farklı yazımları tekilleştirilmeli. `emlakarama` kuralları:

1. Host `www.sahibinden.com`, şema `https`, yol sonundaki `/` atılır.
2. Boş değerli parametreler (`price_min=`) atılır.
3. `pagingOffset=0` atılır (varsayılan).
4. `query_text_mf` `query_text`'e eşitse tek kopya saklanır ama URL üretilirken
   ikisi de yazılır (site böyle bekliyor).
5. Kalan parametreler ada göre sıralanır; çok değerli olanlar (`address_town`)
   değerine göre sıralı tekrar eder.
6. Sonuç `canonical_key` olarak SQLite'ta arama kimliğidir.

## Örnekler

```
# Kadıköy, satılık daire, 5–8 M TL, en yeni önce, 50'lik sayfa
https://www.sahibinden.com/satilik-daire/istanbul-kadikoy?price_max=8000000&price_min=5000000&pagingSize=50&sorting=date_desc

# Tüm Türkiye kiralık işyeri, son 3 gün
https://www.sahibinden.com/kiralik-isyeri?date=3&sorting=date_desc

# Muğla Bodrum satılık villa, "havuzlu" kelimesi geçen
https://www.sahibinden.com/satilik-villa/mugla-bodrum?query_text=havuzlu&query_text_mf=havuzlu

# Ankara Çankaya satılık arsa, 500–2000 m² (a4 = m², doğrulanması gereken ID)
https://www.sahibinden.com/satilik-arsa/ankara-cankaya?a4_min=500&a4_max=2000
```
