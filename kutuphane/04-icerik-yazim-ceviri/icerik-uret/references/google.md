# Google yorumları ve harita bağlantıları

Mekan sayfasının en değerli kısmı resmî kaynaklarda **olmayan** bilgi: kapının
gerçekte kaçta açıldığı, hangi girişin kullanıldığı, kalabalığın ne zaman
bastığı, kadın ziyaretçiye örtü verilip verilmediği. Bunlar hiçbir turizm
sitesinde yok — Google yorumlarında var.

## Kural: yorum girdidir, içerik değildir

**Yorum metni siteye kopyalanmaz.** İki sebep var ve ikisi de bağlayıcı:

1. **Şartlar.** Google Places API şartları yorum metninin, puanların ve
   fotoğrafların saklanmasını ve yeniden yayımlanmasını kısıtlıyor. Kalıcı
   olarak saklanmasına izin verilen tek alan **`place_id`**. Puanı sayfaya
   basmak da atıf yükümlülüğü getiriyor.
2. **İçerik kalitesi.** Yorum alıntısı zaten Google'da duruyor; kopyalayan sayfa
   arama motoruna yeni hiçbir şey vermiyor. Değer, on yorumdan çıkan **ortak
   örüntüyü** kendi cümlemizle yazmakta.

Yani akış şu:

```
yorumları oku  →  tekrar eden somut olguyu çıkar  →  kendi cümlenle yaz
```

> ✗ Bir ziyaretçi "sabah gittik çok sakin ve güzeldi" diyor.
> ✓ Öğle namazından önce avlu boş; kalabalık öğleden sonra başlıyor.

## Ne aranır

Yorumları tararken şunları ara — hepsi doğrudan bir alana ya da bir ipucuna
dönüşüyor:

| Yorumda geçen | Nereye gider |
| --- | --- |
| "kapı 9'da açılıyor ama gişe 9.30'da" | `opening_hours` |
| "giriş X lira oldu" (birden çok yorumda aynı) | `entry_fee` |
| "iki saat yetti / yarım günümüzü aldı" | `duration` |
| "sabah ışık çok güzeldi" | `best_time` |
| "kadınlara girişte örtü veriliyor" | `tips` |
| "yan sokaktaki girişten girdik, ana kapı kapalıydı" | `tips` |
| "merdivenler kaygan" | `tips` |
| "kartla ödeme yok, nakit lazım" | `tips` |
| "restorasyon var, bir bölüm kapalı" | gövde metni |

## Doğrulama eşiği

Tek yorum kanıt değil. Kural:

- **Bir yorum → yazma.** Kişisel deneyim ya da eski bilgi olabilir.
- **Aynı şeyi söyleyen üç yorum → yaz.**
- **Fiyat ve saatte tarih kontrol et.** İki yıl önceki yorumdaki fiyat bugün
  yanlış. Enflasyon yüksekken bu özellikle geçerli — emin değilsen
  `entry_fee` alanına "Değişken — girişte teyit et" yaz. Uydurmaktansa dürüst
  belirsizlik.
- **Çelişki varsa en yenisine bak**, ama çelişkiyi gövdede belirt: "bazı
  kaynaklar pazartesi kapalı diyor, girişte teyit et".

## Diller

Yorumlar üç dilde de okunur ve **farklı şeyler söylerler**:

- **Arapça yorumlar** yerel gerçekliği veriyor: gerçek fiyat, hangi kapı açık,
  namaz saatlerinde ne oluyor.
- **İngilizce yorumlar** yabancı ziyaretçinin takıldığı yeri gösteriyor: vize,
  rehber, kıyafet, kart/nakit.
- **Türkçe yorumlar** Türkiye'den gidenin sorusunu yansıtıyor: ulaşım, sınır,
  konaklama mesafesi.

Üçünü de tara. Bu, tek dilli rakiplerin yapmadığı şey ve içeriği gerçekten
ayıran nokta.

## Place ID nasıl alınır

`google_place_id` alanı doldurulunca harita ve yol tarifi bağlantıları ona göre
kuruluyor — ad değişse, koordinat birkaç metre kaysa bile doğru kaydı açıyor.

Google Maps'te yeri aç → **Paylaş** → bağlantıda `ChIJ…` ile başlayan dizi.
Ya da Google'ın Place ID Finder aracı.

Boş bırakılırsa bağlantılar `lat`/`lng` üzerinden kuruluyor; çalışıyor ama
kayıt eşleşmesi zayıf.

## API entegrasyonu (şu an kapalı)

Sunucuda Google API anahtarı **yok**, dolayısıyla yorum çekme otomatik değil —
araştırma elle yapılıyor.

Otomatikleştirmek istenirse gereken: bir Places API anahtarı, `.env`'de
`GOOGLE_PLACES_API_KEY`. Ama otomatikleşse bile yukarıdaki kural değişmiyor:
**çekilen yorum saklanmaz, yalnızca yazarken okunur.** Saklanabilecek tek şey
`place_id`.
