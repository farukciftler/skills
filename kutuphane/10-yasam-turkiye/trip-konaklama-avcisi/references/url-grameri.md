# Trip.com URL dilbilgisi

Buradaki her parametre 25 Ağustos 2026'da canlı sitede tek tek denenerek doğrulandı.
Doğrulanmamış hiçbir şey yazmadım; bir parametreye ihtiyacın olur da burada yoksa
`tarayici-okuma.md` §5'teki yöntemle **kendin keşfet ve buraya ekle** — uydurma.

## 1. Liste (arama sonuçları) sayfası

```
https://tr.trip.com/hotels/list
  ?cityId=338
  &cityName=London
  &searchType=CT
  &checkin=2026-10-01
  &checkout=2026-10-06
  &crn=1
  &adult=1
  &children=0
  &curr=TRY
  &locale=tr-TR
  &listFilters=<filtre zinciri>
```

| Parametre | Değer | Not |
|---|---|---|
| `cityId` | sayı | **Zorunlu.** Londra 338, İstanbul 532, Paris 192, Tokyo 228, Bangkok 359. Keşif: `mesafe-ve-konum.md` §1 |
| `cityName` | metin | Kozmetik; yanlış olması sonucu değiştirmez, `cityId` belirleyicidir |
| `searchType` | `CT` | Şehir araması |
| `checkin` / `checkout` | `YYYY-MM-DD` | **Küçük harf.** Liste sayfası küçük harf ister |
| `crn` | sayı | Oda sayısı |
| `adult` | sayı | Toplam yetişkin (oda başına değil) |
| `children` | sayı | Çocuk varsa `ages=8,12` gibi yaş listesi de gerekir |
| `curr` | `TRY`, `USD`, `EUR` | Fiyat aralığı filtresi bu para biriminde yorumlanır |
| `locale` | `tr-TR`, `en-XX` | `tr.trip.com` + `tr-TR` Türkçe arayüz verir |

### Alan adı seçimi
- `tr.trip.com` → Türkçe arayüz, TRY varsayılan. Türk kullanıcı için varsayılan bu.
- `www.trip.com` → İngilizce arayüz, USD varsayılan.

Aynı `listFilters` dilbilgisi ikisinde de birebir çalışır (doğrulandı).

### SEO sayfasıyla karıştırma — sık yapılan hata
`https://www.trip.com/hotels/london-hotels-list-338/` bir **SEO açılış sayfasıdır**.
Tarih/filtre parametrelerini **sessizce yok sayar** ve ilgisiz bir "en iyi oteller" listesi
gösterir. Filtreli arama her zaman `/hotels/list?...` yolundadır. Faydası tek şeydir:
şehir adından `cityId` öğrenmek.

## 2. `listFilters` dilbilgisi

Virgülle ayrılmış token zinciri. Her token:

```
{type}~{filterIdKuyruğu}*{type}*{value}
```

- `type` = filtre grubu numarası (23 = rezervasyon politikası, 77 = oda olanağı, ...)
- Sayfa içinde her filtre öğesi `filterID: "type|value"` biçiminde taşınır.
  Token'a çevirirken `|` → `~` olur ve `*type*value` kuyruğu eklenir.

| Kaynak `filterID` | URL token'ı |
|---|---|
| `23\|10` (ücretsiz iptal) | `23~10*23*10` |
| `77\|92` (özel banyo) | `77~92*77*92` |
| `77\|445` (özel tuvalet) | `77~445*77*445` |
| `75\|TAG_495` (otel tipi) | `75~TAG_495*75*495` |
| `16\|4` (4 yıldız) | `16~4*16*4` |
| `6\|9` (puan 8+) | `6~9*6*9` |
| `17\|12` (yürüme mesafesine göre sırala) | `17~12*17*12` |

Kural: `TAG_` önekli değerlerde token'ın ilk yarısı öneki **korur**, ikinci yarısı **atar**.
Diğer hepsinde iki yarı aynıdır.

### Özel biçimli iki token

**Landmark (POI) çapası** — tip 50:
```
50~50~{poiId}*50*{lat}~{lon}~{ad}~{poiId}~1
```
Gerçek örnek (British Museum):
```
50~50~6789940*50*51.5194133~-0.1269566~The%20British%20Museum~6789940~1
```
Semt/bölge çapası ise tip 8 kullanır ve değer sırası farklıdır (`8|{zoneId}` →
`{zoneId}~{lat}~{lon}~1`). İkisini karıştırma; hangisi olduğunu sayfadan hasat ederek öğren.

**Fiyat aralığı** — tip 15:
```
15~Range*15*{min}~{max}
```
Gerçek örnek (5.350–8.250 TL): `15~Range*15*5350~8250`.
Değerler **`curr` ile seçilen para biriminde ve gecelik**tir, toplam değil.

### Sayfanın kendiliğinden eklediği token'lar
Trip.com sayfa içinde gezinirken `29~1*29*1~1*2` ve `80~0~1*80*0` gibi token'lar ekler
(fiyat gösterim tercihi vb.). **Bunlar gerekli değildir** — bu skill'in ürettiği, sadece
gerçek kısıtları içeren URL'ler sorunsuz çalışıyor (doğrulandı).

### Boşluk ve kodlama
`listFilters` içindeki boşluklar `%20` olmalı. Virgül, tilde ve yıldız **kodlanmaz** —
kodlarsan filtre sessizce düşer ve filtresiz sonuç alırsın. Bunu kontrol etmenin yolu:
sayfada filtre çipleri (`Ücretsiz İptal`, `Otel`, `The British Museum`) görünüyor mu.

### Doğrulanmış tam örnek
```
https://www.trip.com/hotels/list?cityId=338&cityName=London&searchType=CT
&checkin=2026-10-01&checkout=2026-10-06&crn=1&adult=1
&listFilters=17~12*17*12,23~10*23*10,75~TAG_495*75*495,77~92*77*92,77~445*77*445,
50~50~6789940*50*51.5194133~-0.1269566~The%20British%20Museum~6789940~1
```
→ 610 tesis, yürüme mesafesine göre sıralı, ilk sonuç "180 m walk from The British Museum".

## 3. Detay (otel) sayfası

Liste kartındaki link devasa bir `hoteluniquekey` blob'u taşır. **Gerek yok.** Minimal biçim
çalışıyor (doğrulandı):

```
https://tr.trip.com/hotels/detail/
  ?cityId=338
  &hotelId=981580
  &checkIn=2026-10-01
  &checkOut=2026-10-06
  &adult=1
  &children=0
  &crn=1
  &curr=TRY
```

**Tuzak:** detay sayfası `checkIn` / `checkOut` — **camelCase**. Liste sayfası `checkin` /
`checkout` — küçük harf. Yanlışını verirsen sayfa açılır ama **bugünün tarihiyle** açılır,
hata vermez. Okuduğun fiyat ve iptal tarihi sessizce yanlış olur. Detay sayfasını okumadan
önce sayfadaki tarihin istediğin tarih olduğunu **her zaman doğrula**.

`hotelId` liste kartından gelir (`liste_oku.js` çıktısındaki `id` alanı).

## 4. Harita görünümü
Liste sayfasındaki "Haritada göster" düğmesi aynı filtreleri harita üzerinde uygular.
Bir landmark'ın etrafındaki dağılımı görmek için faydalıdır ama **veriyi listeden oku** —
harita katmanı daha kırılgan.

## 5. Kırılganlık notu
Bu bir genel API değil, sitenin kendi iç filtre kodlamasıdır. Trip.com bunu haber vermeden
değiştirebilir. Kurduğun URL beklenmedik sonuç veriyorsa:
1. Sayfada filtre çipleri görünüyor mu — görünmüyorsa token biçimi bozulmuş.
2. `scripts/filtre_hasadi.js` ile kodları yeniden hasat et.
3. Elle tek filtre tıklayıp URL'i kopyala, farkı gör.
