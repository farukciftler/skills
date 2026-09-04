# Mesafe ve konum

"British Museum'a max 30 dakika yürüme mesafesinde" gibi bir kısıtı çalışır hale getirmenin
tam yöntemi.

## 1. `cityId` ve POI id keşfi — uydurma, keşfet

Yanlış `cityId` hata vermez; **başka bir şehrin sonuçlarını sessizce döndürür.** Bu, bu skill'in
en sinsi hata modu. Bilmiyorsan üç yoldan biriyle öğren.

### Yol A — SEO açılış sayfası (en hızlı, Seviye 1'de de çalışır)
`https://www.trip.com/hotels/` sayfasındaki şehir linkleri `.../{sehir}-hotels-list-{cityId}/`
biçimindedir. `web_fetch` ile alınabilir, çünkü bu linkler statik HTML'de.

Doğrulanmış id'ler:

| Şehir | cityId | Şehir | cityId |
|---|---|---|---|
| Londra | 338 | İstanbul | 532 |
| Paris | 192 | Tokyo | 228 |
| Bangkok | 359 | Şangay | 2 |
| Pekin | 1 | Guangzhou | 32 |
| Sidney | 501 | Melbourne | 358 |
| Chicago | 549 | Miami | 25773 |
| Las Vegas | 26282 | Gold Coast | 1210 |
| Indianapolis | 1291 | | |

Listede olmayan şehir için: `web_search` ile `trip.com "hotels-list" <şehir adı>` ara,
ya da Yol B.

### Yol B — Arama kutusu (Seviye 2)
Liste sayfasını herhangi bir şehirle aç, hedef adı arama kutusuna **gerçek klavye girdisiyle**
yaz (JS ile `value` atamak React'te öneri listesini açmaz — `computer` aracıyla tıkla ve yaz),
öneriden seç, "Ara"ya bas. `cityId` URL'e düşer.

### Yol C — POI (landmark) id'si
Landmark id'leri şehre özeldir ve `50|50|{poiId}` biçiminde taşınır, değer kısmı
`{lat}|{lon}|{ad}|{poiId}|1`. İki kaynaktan alınır:

1. **Liste sayfasının "Konum" filtre bölümü** — o şehrin popüler landmark'larını
   koordinatlarıyla listeler. `scripts/filtre_hasadi.js` bunları da çeker.
2. **Arama kutusuna landmark adını yazıp öneriden seçmek** — filtre otomatik uygulanır,
   URL'den token'ı kopyalarsın.

Doğrulanmış örnekler (Londra):

| Landmark | filterID | Değer |
|---|---|---|
| The British Museum | `50\|50\|6789940` | `51.5194133\|-0.1269566\|The British Museum\|6789940\|1` |
| London Eye | `50\|50\|6789972` | `51.5031864\|-0.1195192\|London Eye\|6789972\|1` |
| Hyde Park (semt tipi) | `50\|8\|10788` | `10788\|51.50736\|-0.16411\|1` |

Dikkat: Hyde Park **tip 8** (bölge/semt), diğer ikisi **tip 50** (POI). Değer sırası farklı.
Hangisi olduğunu hasat ederek öğren, kalıba güvenme.

## 2. Metre → dakika

Trip.com landmark seçiliyken kartta **yürüme rotası mesafesini** yazar, kuş uçuşu değil.
Bu, sayfanın kendi verisinde `trafficType: "walking"` olarak doğrulandı. Yani metreyi
doğrudan süreye çevirebilirsin; sapma payı yalnızca yürüme hızından gelir.

Kullanılacak hız: **4,8 km/sa ≈ 80 m/dakika** (yetişkin, düz zemin, bagajsız).

| Süre | Mesafe eşiği |
|---|---|
| 10 dk | 800 m |
| 15 dk | 1.200 m |
| 20 dk | 1.600 m |
| **30 dk** | **2.400 m** |
| 40 dk | 3.200 m |
| 45 dk | 3.600 m |

Yavaşlatan durumlar — kullanıcının bağlamı bunlardan birini ima ediyorsa hızı 4,0 km/sa
(67 m/dk) al ve bunu çıktıda tek satırla belirt:
- bavul/valizle yürüyecekse (varış/çıkış günü)
- küçük çocuk, yaşlı ya da hareket kısıtı varsa
- yokuşlu şehir (Lizbon, San Francisco, İstanbul'un yamaçları)
- gece geç saat ya da sağanak sezonu

**Sınır bölgesi kuralı:** eşiğin ±%10'una düşen adayları (30 dk için 2.160–2.640 m) listeden
atma, "sınırda" diye işaretle. Kullanıcı 2 dakika için iyi bir oteli kaçırmasın.

## 3. Kuş uçuşu ile karışırsa

Landmark seçmeden, "şehir merkezine mesafe" filtresi kullanılırsa Trip.com **kuş uçuşu**
mesafe verir (`Straight-line distance`, 500 m / 1 km / 2 km / 3 km / 5 km seçenekleri).
Kuş uçuşunu yürüme mesafesine çevirmek için **1,3 katsayısı** kullan (şehir içi ortalama
dolambaç payı):

```
yürüme_metre ≈ kuş_uçuşu_metre × 1,3
30 dk hedefi için kuş uçuşu eşiği ≈ 2.400 / 1,3 ≈ 1.850 m
```

Bu bir tahmindir; nehir, demiryolu ya da park gibi kesintiler varsa (Londra'da Thames,
İstanbul'da Boğaz) katsayı 2'yi aşabilir. Mümkünse landmark çapası kullan ve bu hesabı hiç yapma.

## 4. Birden fazla landmark

Trip.com **aynı anda tek bir konum çapası** kabul eder (Konum bölümü radio davranır).
Kullanıcı iki landmark verirse:

1. Daha kısıtlayıcı olanı (daha kısa süre isteneni) çapa yap.
2. Sonuçları oku.
3. İkinci landmark'a mesafeyi **ikinci bir aramayla** ya da otelin koordinatından haversine
   ile hesapla — otel koordinatları `liste_oku.js` çıktısında var (`lat`/`lon`).
4. Çıktıda ikinci mesafenin **hesaplanmış** olduğunu belirt: kuş uçuşudur, yürüme değil.

İkisinin ortasında kalmak isteniyorsa iki koordinatın orta noktasına en yakın semti bul ve
o semti çapa yap — ama bunu bir öneri olarak sun, kullanıcı adına karar verme.

## 5. Semt bilgisi

`liste_oku.js` her otel için `semt` (Bloomsbury, Theatreland, Paddington...) döndürür.
Kısa listede semt sütunu tutmak, mesafe sayısının anlatmadığı şeyi anlatır: 2.000 m'lik iki
otelden biri sakin bir müze mahallesinde, diğeri gece kulüpleri sokağında olabilir.
Semtler hakkında kesin iddia üretme — kullanıcı sorarsa `web_search` ile doğrula.

## 6. POI çapası ile bölge çapası aynı şey değil

İki farklı mekanizma; karıştırmak yanlış sonuç verir.

| | POI (tip 50) | Bölge/semt (tip 8) |
|---|---|---|
| Örnek | The British Museum | Hyde Park, Bayswater, Bloomsbury |
| Token | `50~50~{poiId}*50*{lat}~{lon}~{ad}~{poiId}~1` | `50~8~{zoneId}*8*{zoneId}~{lat}~{lon}~1` |
| Ne yapar | Noktaya göre **mesafe** hesaplar, uzaklığa göre sıralar | O semte **üye olan** tesisleri filtreler |
| Kartta yazan | `The British Museum 210 m uzaklıkta` | `Bölge merkezine 1,5 km yürüyüş mesafesinde` |

**İkinci segment tuzağı.** POI'de token'ın ortası `*50*`, bölgede `*8*` — yani grup numarası
değil, **alt tip**. `50~8~10788*50*...` yazarsan filtre çipi sayfada görünür ama sonuçlar
tamamen alakasız gelir (doğrulandı: Hyde Park çapasıyla ilk sonuç Stratford çıktı).
Sessiz hatadır, çip göründüğü için fark etmesi zor.

**Asıl önemli fark: bölge çapası bir yarıçap değil, üyelik filtresidir.**
Doğrulanmış örnek: Wedgewood Hotel, Kensington Gardens'a 530 m mesafede ama semti "Bayswater"
olduğu için "Hyde Park" bölge filtresinde **hiç çıkmıyor**. Fiziksel olarak yakın bir tesis,
idari olarak başka semtte diye eleniyor.

Sonuç: "şu parka/semte yakın" isteklerinde bölge filtresine tek başına güvenme. Komşu semtleri
de ayrı ayrı tara, ya da adayların detay sayfasındaki **"Çevre"** bölümünden gerçek mesafeyi oku
(`Cazibe merkezi: Kensington Gardens (230 m)` gibi). Bu bölüm her tesiste var ve çapadan bağımsızdır.
