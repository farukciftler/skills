# İptal politikası ve oda doğrulaması

Adım 5'in tarifi. Bu dosyadaki iki şey yapılmazsa skill yanlış cevap verir.

## 1. İptal son tarihi

### Filtre ne söyler, ne söylemez
`23|10` (Ücretsiz iptal) filtresi: *"bu tesiste ücretsiz iptal edilebilen en az bir oran var."*
Söylemediği: **hangi tarihe kadar.** Kart üzerindeki "Ücretsiz İptal" rozeti de tarihsizdir.

Son tarih yalnızca **detay sayfasında, oran satırında** yazar. Canlı sayfadan alınmış
birebir metin biçimleri (25 Ağustos 2026'da doğrulandı):

```
Ücretsiz İptal 30 Eyl 16:00 öncesi              (tr.trip.com)
Free Cancellation before 16:00, Sep 30          (www.trip.com)
```

Dikkat: iki dilde **alan sırası ters** — Türkçesi gün-ay-saat, İngilizcesi saat-ay-gün.
İkisini de yakalayan, canlı metinde test edilmiş desen:

```js
/(?:Ücretsiz İptal|Free Cancellation)\s*(?:before\s*(?<saatEN>\d{1,2}[:.]\d{2})\s*,\s*(?<ayEN>\p{L}{3,})\s*(?<gunEN>\d{1,2})|(?<gunTR>\d{1,2})\s*(?<ayTR>\p{L}{3,})\.?\s*(?<saatTR>\d{1,2}[:.]\d{2})\s*(?:öncesi|önce))/u
```

Tarihsiz sade `Ücretsiz İptal` rozeti bilerek eşleşmez — o, tarih taşımayan kart rozetidir
ve **son tarih kanıtı değildir**.

Metin biçimi kırılgandır. Eşleşmezse ham satırı çıktıya taşı ve `[OKUNDU]` etiketiyle olduğu
gibi göster. Ayrıştıramadığın bir tarihi tahmin etme.

### Aynı otelde her oranın tarihi farklı olabilir
Doğrulanmış örnek — The Bloomsbury (hotelId 718347), 1–6 Ekim 2026: sayfadaki oranların
çoğu `30 Eyl 16:00 öncesi` derken bir oran `29 Eyl 12:00 öncesi` diyor. **Otelin değil,
seçtiğin oranın tarihini oku ve hangi oranı okuduğunu çıktıda yaz.**

### Karşılaştırma mantığı — ters çevirme
Kullanıcı "**X tarihine kadar** iptal edebileyim" diyor. Aradığın:

```
iptal_son_tarihi  >=  X
```

| Kullanıcı istediği | Oranın son tarihi | Sonuç |
|---|---|---|
| 28 Eylül'e kadar | 30 Eylül 16:00 | ✅ geçer — 28'inde hâlâ ücretsiz iptal edebilir |
| 28 Eylül'e kadar | 28 Eylül 18:00 | ✅ geçer (ama sınırda, saati yaz) |
| 28 Eylül'e kadar | 27 Eylül 18:00 | ❌ kalır |
| 28 Eylül'e kadar | 1 Ekim 12:00 | ✅ geçer, en esnek |

Sık yapılan hata: "son tarih 30 Eylül, kullanıcı 28 dedi, o zaman uymuyor" demek. Uyuyor.
**Geç son tarih iyidir.**

### Saat ve saat dilimi
Son tarih saat içerir ve **otelin yerel saatidir**. Kullanıcı sınıra yakın bir tarihte
karar verecekse (aynı gün), saati ve saat diliminin otel yerel saati olduğunu yaz.
İstanbul'dan Londra'ya bakarken 2 saat fark var; "28 Eylül 16:00 Londra = 18:00 İstanbul".

### Kısmi ve kademeli politikalar
Bazı oranlar kademelidir: *"X tarihine kadar ücretsiz, sonra 1 gece ücreti, sonra tamamı."*
Detay metnini olduğu gibi taşı, "ücretsiz iptal" diye sadeleştirme.

### Ön ödeme + ücretsiz iptal aynı anda olabilir
`payType` ön ödemeliyse para tahsil edilir, iptalde **iade süreci** işler — anında geri gelmez
(kart tipine göre günler alabilir, döviz kurundan da kayıp olabilir). Kullanıcı asıl olarak
esneklik istiyorsa **otelde ödemeli + ücretsiz iptal** oranı daha iyidir. Bunu bir satırla söyle,
karar kullanıcının.

Ödeme tipi kodları (`liste_oku.js` çıktısındaki `odeme` alanı, `payInfo.payType`):
gözlemlenen değerler `1` ve `3` — anlamları site sürümüne göre değişebildiği için
**koda göre iddia üretme**, detay sayfasındaki metni (`Ön ödeme` / `Otelde ödeme`) oku.

## 2. Ortak banyo tuzağı

Trip.com'un `77|92` (özel banyo) ve `77|445` (özel tuvalet) filtreleri **tesis düzeyinde**
çalışır: tesiste özel banyolu bir oda varsa tesis listede kalır. Kartta gösterilen oran ise
**en ucuz** orandır ve ortak banyolu olabilir.

Bu teorik bir risk değil — filtre uygulanmış Londra listesinde gerçekten şu kartlar çıkıyor:
`Basic İki Yataklı Oda - Ortak Banyolu`, `Ortak Banyolu Tek Kişilik Oda`.

**Kural: oda adını oku.**

| Oda adında geçen | Karar |
|---|---|
| "Ortak Banyolu", "Shared bathroom", "Shared facilities" | ❌ o oran elenir |
| "En-suite", "Özel banyo", "Private bathroom" | ✅ geçer |
| Hiçbiri geçmiyor (ör. "Deluxe Queen Room") | Detay sayfasında oda olanaklarına bak; bakamadıysan `[DOĞRULANMADI]` etiketiyle sun |

Otel tipinde (`75|TAG_495`) ortak banyo nadirdir ama Londra/Paris'in eski Bloomsbury tipi
bütçe otellerinde yaygındır — yani tam da bu skill'in aradığı fiyat bandında. Kontrolü atlama.

Aynı mantık her "oda düzeyi" olanağı için geçerli: klima, küvet, mutfak, balkon.
Tesiste var demek, **senin göreceğin oranda var** demek değil.

## 3. Toplam fiyat

Kart iki sayı gösterir: **gecelik** (büyük) ve **toplam** (küçük satır).
`Toplam fiyat: 88.732 TL — 1 oda × 5 gece, vergiler ve ücretler dahil`.

- Kullanıcı bütçe verdiyse **toplam** üzerinden ele.
- Vergi dahil olup olmadığını satırdan oku, varsayma. Trip.com'da fiyat gösterim tercihi
  (gecelik vergi hariç / gecelik vergi dahil / toplam) değiştirilebiliyor; okuduğun sayının
  hangisi olduğunu yaz.
- **Şehir/konaklama vergisi** ayrı bir kalem olabilir ve otelde nakit tahsil edilir
  (Roma, Paris, Amsterdam, Lizbon...). Trip.com toplamına dahil değilse detay sayfasında
  "otelde tahsil edilecek ek ücretler" bölümünde yazar. Kullanıcı bütçeye duyarlıysa bak.
- Promosyon kodu / "üye fiyatı" / "ilk rezervasyon indirimi" giriş yapılmış oturumda farklı
  fiyat gösterir. Okuduğun fiyatın kullanıcıda birebir çıkmayabileceğini bir kez söyle.

## 4. Kahvaltı

"Kahvaltı dahil" (`5|1`) tesis filtresi de aynı tuzağı taşır. Detayda oran satırında
`Kahvaltı dahil` mi yoksa `34 $ karşılığında kahvaltı (opsiyonel)` mi yazdığını oku.
İkisi çok farklı toplam maliyet demek — 5 gece × 2 kişi × 30 $ = 300 $.

## 5. Doğrulama çıktısı

Her aday için şu dört maddeyi ayrı ayrı raporla; hepsini tek "uygun ✅" işaretine indirgeme:

```
The Bloomsbury
  iptal      : 30 Eyl 16:00'a kadar ücretsiz ✅ (28 Eylül şartı karşılanıyor) [OKUNDU 25 Ağu 14:10]
  banyo      : "Classic Queen Room" — en-suite ✅
  mesafe     : 250 m ≈ 3 dk yürüme ✅
  toplam     : 3.302 $ (5 gece, vergi dahil), kahvaltı hariç
```

Doğrulayamadığın maddeyi `[DOĞRULANMADI]` yaz ve neden doğrulanamadığını tek kelimeyle belirt
(sayfa açılmadı / metin bulunamadı / oran tükendi). Boş bırakma.
