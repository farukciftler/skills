# Rakip ve Sektör Analizi

24 Ağustos 2026'da yapılan saha araştırmasının bulguları. On iki alan adı DNS
düzeyinde tarandı, altı site tarayıcıda 375×812 mobil görünümde tek tek açıldı.

**Kanıt seviyeleri** — bir bulguyu aktarırken seviyesini de aktar:
`SAHA` = kendi incelemem, tarihli · `RESMÎ` = TÜİK/kurumsal kaynak ·
`SEKTÖR` = ajans/sektör yayını, bağımsız doğrulanmadı.

Tam rapor (paylaşılabilir sürüm): https://claude.ai/code/artifact/1ee555a1-b962-4454-8339-7f99360ceb15

## İçindekiler
1. İncelenen siteler ve bulgular
2. Türk konut projesi sitesinin ortak anatomisi
3. Sektörün kronik hataları
4. Türkiye'nin dijital zemini (rakamlar)
5. Karar tablosu: zorunlu / ayrıştırır / sonra
6. Boşluk: kimsenin yapmadığı şey

---

## 1. İncelenen siteler ve bulgular

İki ayrı tür var: **kurumsal firma sitesi** (Nef, Sinpaş, DKY, Emlak Konut —
çok proje, kurumsal anlatı) ve **tek proje mikrositesi** (Uplife Kadıköy,
Yenişehir Evleri). Moonstone ikincisidir; kurumsal siteleri örnek almak
gereksiz ağırlık getirir.

**Uplife Kadıköy** (uplifekadikoy.com, Teknik Yapı) `SAHA`
- Mobilde **sabit alt aksiyon çubuğu, dört düğme**: Hemen Ara · Yol Tarifi ·
  Biz Sizi Arayalım · WhatsApp. Ekranda sürekli görünür. **Kopyalanacak fikir.**
- Kahraman alanı doğrudan 360° sanal tura davet ediyor.
- Hata: telefon bağlantısı `tel:444 10 08` — boşluklu, bazı cihazlarda çalışmaz.
- Hata: KVKK metninin tamamı ana sayfa HTML'ine gömülü.
- 94 KB HTML, ilk yanıt ~2,9 sn.

**Nef** (nef.com.tr) `SAHA`
- Kalıcı **"Sizi Arayalım"** düğmesi — Türkiye'de baskın lead kalıbı. Form
  doldurtmak yerine geri arama sözü veriyor; sürtünmeyi kullanıcıdan alıp
  satış ekibine veriyor.
- Ama form ağır: telefon, il, ad, soyad, e-posta, proje + 3 KVKK onayı +
  reCAPTCHA. Bu kadar alan dönüşümü keser.
- Çerez izni mobilde ekranın yarısından fazlasını kaplıyor.

**Avrupa Konutları** (avrupakonutlari.com, Artaş) `SAHA`
- Çerez uyarısında **sadece "Kabul Et" var, reddetme yok.** KVKK açısından
  savunulabilir değil. Moonstone bunu asla kopyalamamalı.
- Ana sayfada 74 görsel, tek H1, 30 maddelik hamburger menü.

**DKY İnşaat** (dkyinsaat.com.tr) `SAHA`
- Kahraman alanının doğru anatomisi: tam kanama render + büyük başlık + tek
  cümle + **iki düğme (dolu birincil, kontur ikincil)** + aşağı kaydırma işareti.

**Yenişehir Evleri Arnavutköy** (emlakkonut.com.tr alt alan adı) `SAHA`
- **Moonstone'un birebir muadili.** Mikrositenin asgari iskeleti: Proje
  Hakkında · Örnek Daire Planı · Lokasyon · İletişim Formu.
- Mesafeleri **dakika/km cinsinden** veriyor ("İstanbul Havalimanı 10 dakika",
  "Kuzey Marmara Otoyolu 4 km"). En güçlü hamleleri bu.
- Form: ad, soyad, telefon, e-posta, mesaj + KVKK onayı.

**nidapark.com** `SAHA`
- Tanınmış rezidans markasının alan adı bugün GoDaddy'de satılık; site yok.
  Proje siteleri satış bitince terk ediliyor. **Alan adı yenileme ve arşiv
  planı baştan konuşulmalı** — marka arama trafiği yıllarca sürüyor.

## 2. Türk konut projesi sitesinin ortak anatomisi

Altı sitede tekrar eden yapı. Klişe değil, alıcının beklediği sıra. Moonstone
bu iskeleti kullanmalı, farkı içerik kalitesinde yaratmalı.

| Katman | Sektörde standart |
|---|---|
| Kahraman | Tam ekran render, büyük proje adı, bir cümle, iki düğme |
| Sabit iletişim | Başlıkta 444'lü hat; mobilde alt çubuk (ara / yol tarifi / geri arama / WhatsApp) |
| Lead kancası | "Sizi Arayalım" — form yerine geri arama sözü |
| Ürün | Daire tipleri, kat planı görselleri, m² listesi |
| Yaşam | Sosyal alanlar, peyzaj, çevre |
| Konum | Harita + dakika/km cinsinden mesafeler |
| Güven | Kurumsal geçmiş, tamamlanan projeler, "sayılarla biz" |
| Hukuk | KVKK aydınlatma, çerez izni |

## 3. Sektörün kronik hataları

Bunlar rakiplerde gördüğüm gerçek hatalar — Moonstone'da tekrarlanmamalı, ve
bir kullanıcı "rakip böyle yapmış" dediğinde bunları hatırlat:

1. **Reddetme düğmesi olmayan çerez izni.** Yaygın ve KVKK açısından savunması zor.
2. **Bozuk `tel:` bağlantıları.** Mobilin en önemli dönüşüm eylemi, en özensiz
   bırakılan detay. Yayına almadan önce gerçek telefonla test et.
3. **Sayfaya gömülü hukuk metni.** KVKK politikası ayrı sayfa olmalı.
4. **Çerez izninin ilk ekranı yutması.** Alt şerit biçiminde olmalı.
5. **Ana sayfada onlarca ağır görsel.** Bir sitede 74 görsel saydım.

## 4. Türkiye'nin dijital zemini

`RESMÎ` TÜİK 2026 Hanehalkı Bilişim Teknolojileri araştırması:
- 16–74 yaş internet kullanımı **%92,3** (2025: %90,9)
- En çok kullanılan uygulamalar: **WhatsApp %90** · YouTube %77,6 · Instagram %71,1

**Bu sıralama stratejiyi belirliyor: WhatsApp Türkiye'nin bir numaralı
uygulaması.** Bir konut projesinde en değerli iletişim kanalı bir sosyal medya
hesabı değil, çalışan bir WhatsApp hattıdır. Sitede, ilanlarda, sosyal medyada
ve basılı işte birinci sınıf kanal olarak kurulmalı.

`SEKTÖR` Platform büyüklükleri: Instagram ~54,7 milyon kullanıcı; TikTok 31,2
milyon 18+ kullanıcı, kişi başı günde ~37 dakika. TikTok'un boyutu artık göz
ardı edilecek düzeyde değil — Türk ajanslarının standart paketi (Instagram,
YouTube, LinkedIn, Facebook) TikTok'u çoğu zaman atlıyor.

`SEKTÖR` Alıcı davranışı: konut alıcısı karar öncesi **önce portallara** gidiyor
(sahibinden, emlakjet, hepsiemlak, zingat). Proje sitesi ikinci durak. Kararda
öne çıkan iki faktör **fiyat ve ödeme koşulları**; ikinci elde **deprem
dayanıklılığı** öncelikli kriter olarak raporlanıyor.

`SEKTÖR` Alıcıların "çok faydalı" bulduğu site özellikleri (ABD verisi, birebir
alınmamalı ama sıralama öğretici): fotoğraf %83 · detaylı bilgi %79 · kat planı
%57 · satış temsilcisi iletişimi %47 · **sanal tur %41**. Sanal tur listenin en
altında ve en pahalısı — önceliklendirmede bunu hatırla.

`SEKTÖR` Sayfa hızı: yüklenmenin ilk beş saniyesinde her ek saniye dönüşümü
ortalama **%4,42** düşürüyor.

`SEKTÖR` Sosyal medya formatı: inşaat ilerleme videoları statik görsele göre
3–4 kat erişim; Reels genel olarak statik gönderinin iki katı erişim, carousel'e
göre %22 daha fazla etkileşim. İdeal uzunluk 15–30 sn. Bu rakamlar doğrulanmadı
ama mekanizma mantıklı: **şantiye ilerlemesi, projeyi aramayan insanı bile
ilgilendiriyor.** Bitmiş render herkesin gördüğü şey; 7. katın dökülmesi gerçek.

## 5. Karar tablosu

| Özellik | Sınıf | Gerekçe |
|---|---|---|
| Çalışan WhatsApp hattı | **Zorunlu** | Türkiye'nin 1 numaralı uygulaması (%90) |
| Mobil sabit aksiyon çubuğu | **Zorunlu** | Sektörde kanıtlanmış; mobil dönüşümün ana kaynağı |
| Üç alanlı lead formu + teşekkür sayfası | **Zorunlu** | 7 alanlı form dönüşümü kesiyor; ayrı URL olmadan ölçüm yok |
| Daire tipi sayfaları (net/brüt + mahal listesi) | **Zorunlu** | En çok bakılan sayfa; veri elimizde |
| Google Business Profile | **Zorunlu** | İlçe aramasında siteden çok lead; doğrulama 1–2 hafta |
| Portal ilanları (4 portal) | **Zorunlu** | Alıcının ilk durağı; site beklemeden açılır |
| KVKK + gerçek reddetmeli çerez izni | **Zorunlu** | Form açılmadan şart; rakiplerin çoğu yanlış yapıyor |
| Tip karşılaştırma tablosu (süzülebilir) | **Ayrıştırır** | Altı sitenin hiçbirinde yok |
| Tarihli inşaat ilerleme sayfası | **Ayrıştırır** | Güvenin en ucuz kanıtı; içeriği besliyor |
| Ölçülebilir mesafeler (dk/km) | **Ayrıştırır** | Katalogda yok; satış + yerel SEO argümanı |
| İndirilebilir tip föyü (PDF) | **Ayrıştırır** | Meşru lead kapısı |
| Ticari alanlar için ayrı sayfa ve ilan seti | **Ayrıştırır** | Ayrı ürün, ayrı alıcı |
| 360° sanal tur | **Sonra** | Faydalı bulunma en düşük (%41), maliyet yüksek |
| Tam interaktif 3D daire seçici | **Sonra** | Fiyat/stok verisi olmadan çalışmaz |
| Çok dilli site | **Sonra** | Yabancı yatırımcı kararı verilmeden boşa maliyet |
| Otomatik oynayan arka plan videosu | **Yapma** | Mobil hızını bozuyor, ölçülebilir faydası yok |

**Önerilen sıra:** (1) bu hafta — GBP başvurusu + WhatsApp hattı + portal
ilanları; (2) 2–3 hafta — tek sayfalık açılış sitesi, çalışan form, mobil
aksiyon çubuğu, KVKK; (3) 1–2 ay — tam site; (4) paralel — sosyal medya
hesapları ve ilk saha çekim günü.

## 6. Boşluk: kimsenin yapmadığı şey

İncelediğim altı sitenin hiçbirinde **daire tiplerini yan yana karşılaştırma**
imkânı yoktu. Alıcı tam olarak bunu yapmaya çalışıyor: "65 m² mi 75 m² mi,
hangi katta, farkı ne?"

Moonstone'un altı net tipi ve eksiksiz mahal listesi zaten var. Tam interaktif
daire seçici birinci sürüm için fazla; ama **işin %80'i basit bir süzülebilir
karşılaştırma tablosuyla** alınabilir. Maliyeti düşük, rakiplerde yok, ve
alıcının gerçekte yapmak istediği iş bu. Bu proje için en yüksek getirili tek
tasarım kararı budur.

Bunu besleyen altyapı Türkiye'de mevcut: Konutmatik, PirCloud KonutCRM, YapıCRM
gibi sistemler kat planı üzerinden daire durumu, stok ve lead takibini birlikte
yönetiyor. Fiyat ve stok verisi netleştiğinde bu yöne geçilebilir.
