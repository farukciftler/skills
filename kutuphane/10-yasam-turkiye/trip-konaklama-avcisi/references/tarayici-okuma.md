# Tarayıcıyla okuma (Seviye 2/3)

Trip.com liste ve detay sayfaları React ile render edilir. `web_fetch` fiyat da politika da
döndürmez. Bu dosya, sayfayı gerçekten okumanın tarifi.

## 1. Açılış

1. Filtreli liste URL'ini kur (`url-grameri.md`).
2. Tarayıcıda aç.
3. **Yüklenmeyi bekle** — kartlar asenkron gelir. 2–3 saniye bekle, sonra
   `X konaklama yeri bulundu` / `X properties found` metni ekranda mı diye bak.
   Yoksa 2 saniye daha bekle. Beklemeden okumak boş liste döndürür ve "sonuç yok" yanlışına
   götürür.
4. **Filtre çiplerini doğrula.** Sonuç sayısının hemen üstünde uygulanan filtreler çip olarak
   yazar (`Ücretsiz İptal`, `Otel`, `Özel banyo`, `The British Museum`). Kurduğun her kısıt
   burada görünmüyorsa token biçimi bozulmuştur — okumaya devam etme, URL'i düzelt.

## 2. Veri çekme — metin kazıma değil, fiber okuma

Sayfanın görünen metnini regex'lemek kırılgandır (dil değişince, düzen değişince kırılır).
Bunun yerine React'in bileşen prop'larından yapılandırılmış veriyi al: her otel kartının
altında `card.hotelInfo` ve `card.roomInfo` nesneleri duruyor — otel adı, id, yıldız, puan,
yorum sayısı, koordinat, landmark'a mesafe, oda adı, yatak, fiyat, etiketler hepsi orada.

`scripts/liste_oku.js` bunu yapar. Sayfa yüklendikten sonra içeriğini çalıştır, JSON döner.

Çalışma mantığı (kırılırsa buradan onar):
- Kartlar `.hotel-list .list-item` altında.
- Her kartın **içindeki** bir düğümden başlayıp `__reactFiber$...` üzerinden **yukarı** yürü;
  `memoizedProps.card.hotelInfo` taşıyan ilk fiber kartın verisidir.
  (Kartın kendi kök elemanından yukarı yürümek işe yaramaz — prop'lar iç düğümlerde.)
- Landmark mesafesi: `hotelInfo.positionInfo.positionDesc` →
  `"The British Museum 210 m uzaklıkta"` / `"210m walk from The British Museum"`.
- Koordinat: `positionInfo.mapCoordinate[0]` (WGS84).
- Oda/fiyat: `roomInfo[0]` → `summary.physicsName`, `bedInfo.contentList`,
  `priceInfo.displayPrice`, `priceInfo.priceExplanation`, `payInfo.payType`,
  `roomTags.advantageTags[].tagTitle` (burada `Ücretsiz İptal` rozeti gelir).

Sayı ayrıştırırken **Türkçe biçime dikkat**: `5.788 TL` beş bin yedi yüz seksen sekiz,
`6,3` puan altı virgül üç. `parseFloat("5.788")` sana 5,788 verir — script bunu ele alıyor,
elle yazarsan aynı tuzağa düşme.

## 3. Sayfalama: 10 kart tavanı — "10 sonuç var" deme

Liste **her seferinde 10 kart** basar. Daha fazlası sonsuz kaydırma (infinite scroll) ile gelir.
Doğrulanmış iki gerçek:

**`page=2` gibi bir URL parametresi YOK.** Denendi: URL'e `page=2` eklemek aynı ilk 10 kartı
döndürüyor, sessizce yok sayılıyor. Sayfalamayı URL'den zorlamaya çalışma.

**Kaydırma yalnızca gerçek bir viewport'ta çalışır.** Sonsuz kaydırma bir IntersectionObserver'a
bağlı; görünür alan yüksekliği 0 olan otomasyon yüzeylerinde (bazı başsız/panel tarayıcılar)
`window.scrollBy` `scrollY`'yi hiç oynatmaz ve **yeni kart hiç yüklenmez**. Okumaya başlamadan
önce kontrol et:

```js
document.documentElement.clientHeight   // 0 ise kaydırma calismaz, 10 kartla sinirlisin
```

### 10 kart tavanına takıldığında — üç çıkış yolu

1. **Sıralamayı kısıtına göre seç, tavanı sorun olmaktan çıkar.** `17|12` (yürüme mesafesi)
   ile sıraladığında ilk 10 kart zaten **landmark'a en yakın 10 tesistir**. Yakınlık sorusunda
   tavan neredeyse hiç zarar vermez — istediğin şey listenin başında. Aynısı `17|3` (en ucuz)
   için bütçe sorusunda geçerli.
2. **Aramayı dilimlere böl.** Aynı filtrelerle ayrı ayrı çalıştır: 3 yıldız / 4 yıldız / 5 yıldız,
   ya da fiyat bandı bandı (`15~Range*15*...`). Her dilim kendi ilk 10'unu verir; birleştir.
   Dilimlerin çakışmadığından emin ol, aynı oteli iki kez sayma.
3. **Gerçek viewport'lu bir tarayıcı yüzeyi kullan** (Chrome eklentisi, başlıklı Playwright).
   Orada kaydırma çalışır:
   ```js
   window.scrollBy(0, 1200);   // 1,5 sn bekle, kart sayisi artti mi bak, tekrarla
   ```
   İki ardışık kaydırmada kart sayısı artmıyorsa listenin sonundasın.

### Her durumda: ne okuduğunu dürüst yaz

"610 tesis filtreden geçti, **yürüme mesafesine göre en yakın 10 kart okundu**" doğru cümledir.
"10 otel bulundu" yanlıştır ve kullanıcıyı listenin tamamını gördüğüne inandırır.

## 4. Detay sayfası okuma

`url-grameri.md` §3'teki minimal URL ile aç. Sonra:

1. **Tarihi doğrula.** camelCase tuzağı yüzünden yanlış tarihle açılmış olabilir. Sayfada
   check-in/check-out tarihleri istediğin tarih mi, bak. Değilse okuma, URL'i düzelt.
2. Sayfa metnini al, `Ücretsiz İptal` / `Free Cancellation` geçen satırı ve çevresini oku
   (`iptal-ve-oda.md` §1).
3. Oda adını ve `Ortak Banyolu` / `Shared` geçip geçmediğini kontrol et.
4. `Toplam fiyat` satırını al.

Detay sayfası liste sayfasından yavaş yüklenir; 4 saniye bekle.

Aday sayısını 5–8'de tut. Her detay sayfası bir sayfa yüklemesi demek; 30 otelin detayını
açmak hem yavaş hem bloklanma riski.

## 5. Yeni bir filtre kodunu keşfetme

`filtre-kodlari.md`'de olmayan bir filtreye ihtiyacın olursa:

1. Liste sayfasını aç.
2. `listFilters` değerini not et (baz).
3. İstediğin filtreyi **tıkla** (sol paneldeki `label` öğesini).
4. 1,5 sn bekle, `listFilters`'ı tekrar oku.
5. Farkı al — eklenen token o filtredir.

Toplu hasat için `scripts/filtre_hasadi.js`: tüm "Daha Fazla Göster" düğmelerini açar, her
filtre öğesinin başlığını ve `filterID`'sini fiber'dan okur, bölüm bölüm döker.

## 6. Bloklanma hijyeni

Trip.com agresif bir bot koruması çalıştırmıyor ama sınırsız da değil.

- **Hacim:** tek oturumda 20–30 sayfa yüklemesini geçme. Sürdürülebilir izleme günde
  ~15 istektir, yüzlerce değil.
- **Hız:** sayfa yüklemeleri arasına 1,5–3 sn koy. Paralel 10 sekme açma.
- **Aynı sekme:** yeni sekme açmak yerine aynı sekmede gezin.
- **CAPTCHA/engel çıkarsa:** dur. CAPTCHA çözmeye çalışma, farklı IP denemeye kalkma.
  Kullanıcıya "Trip.com bu oturumda okumayı engelledi, link aşağıda, kendin 20 saniyede
  doğrulayabilirsin" de. Bu doğru cevaptır.
- **Giriş yapma, hesap açma, ödeme bilgisi girme.** Fiyatı bul, oranı seç, ödeme ekranına
  kadar getir — orada dur.

## 7. Sessiz bozulma korumaları

Şunlardan biri olursa **veri okunmamış demektir**, boş sonucu "sonuç yok" diye sunma:

| Belirti | Anlamı |
|---|---|
| Kart sayısı 0 ama "X tesis bulundu" yazıyor | Sayfa henüz render etmedi — bekle, tekrar oku |
| Filtre çipleri eksik | Token biçimi bozuk — URL'i düzelt |
| Tüm fiyatlar `null` | Fiber yapısı değişmiş — `liste_oku.js`'i §2'ye göre onar |
| Mesafe alanı boş | Landmark çapası uygulanmamış — `50\|...` token'ını kontrol et |
| Detayda tarih bugüne düşmüş | camelCase tuzağı — `checkIn`/`checkOut` |

## 8. Dolgu sonuç tuzağı — en tehlikeli sessiz hata

Filtreleri geçen tesis sayısı azsa, Trip.com listenin altına **filtreleri yok sayan "benzer
öneri" kartları** ekler. Bunlar görsel olarak normal sonuçlardan ayırt edilemez.

Doğrulanmış örnek: 3 gece / 2 yetişkin / otel / özel banyo / puan 8+ / gecelik ≤ 7.000 TL
filtresiyle sayfa **"4 konaklama yeri bulundu"** diyor — ama DOM'da 14 kart var. 5. karttan
itibarenkiler dolgu: aralarında gecelik 19.164 TL'lik Radisson Blu ve 6,3 puanlı bir tesis var,
yani hem fiyat hem puan filtresini ihlal ediyorlar.

**Kural: kaç kart okuduğuna değil, "X konaklama yeri bulundu" sayısına güven.**

```js
const n = +(document.body.innerText.match(/([\d.]+) konaklama yeri bulundu|([\d,]+) properties found/)||[])[1]
  ?.replace(/[.,]/g,'');
// gercek sonuclar = ilk n kart. Gerisi dolgu.
```

Dolguyu ayıklamanın ikinci yolu: her adayı kendi kısıtlarına karşı **tekrar sına** (fiyat ≤ tavan,
puan ≥ eşik). Filtreyi ihlal eden bir kart dolgudur, sonuç değil.

Bu tuzağa düşmek "işte 10 uygun otel" demeye ve altısının şartları hiç karşılamamasına yol açar.

## 9. Kart fiyatı ile detay fiyatı tutmayabilir

Liste kartındaki oran, detay sayfasında görünen en ucuz orandan farklı olabilir — oran tükenmiş,
başka bir oda tipi öne çıkmış ya da kart farklı bir doluluk varsayımıyla fiyatlanmış olabilir.

Doğrulanmış örnek: Dolphin Hotel, 1–4 Ekim 2026 / 2 yetişkin — kartta toplam **22.750 TL**,
detay sayfasında görünen oranlar **30.548 TL**'den başlıyor.

**Bütçe kısıtı varsa detay sayfasındaki rakamı esas al** ve kullanıcıya hangisini okuduğunu söyle.
İkisi çelişiyorsa çelişkiyi raporla, ortalama alma, düşük olanı seçip geçme.
