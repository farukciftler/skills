# Türkiye E-Ticaret Pazarı — Platformlar ve Güven Sinyalleri

## Platform haritası

| Platform | Güçlü olduğu alan | Not |
|---|---|---|
| Trendyol | Giyim, kozmetik, ev; en geniş satıcı havuzu | Fiyat rekabeti yüksek; satıcı kalitesi çok değişken, sahte ürün riski en çok burada raporlanıyor (özellikle kozmetik/parfüm/ayakkabı). "Yorumlar ürünü satın alanlardan gelir" kuralı var ama satıcı değişimi yorumları yanıltabilir: yorumlar başka satıcı dönemine ait olabilir. |
| Hepsiburada | Elektronik, beyaz eşya | "HepsiExpress/resmi satıcı" rozetleri; ürün puanı ile satıcı puanı ayrı metriklerdir, ikisini de kontrol et. |
| Amazon TR | Elektronik, kitap; iade süreci en pürüzsüz | "Amazon tarafından satılır ve gönderilir" en güvenli seçenek; Buy Box'taki satıcıyı mutlaka kontrol et. Yorumcu profilleri görülebilir (TR pazaryerlerinde görülemez). |
| n11 | Elektronik, genel | Karşılaştırma sitelerinde hâlâ listelenen az sayıda büyük pazaryerinden biri. |
| Pazarama, PTT AVM, İdefix, ÇiçekSepeti | Niş/kampanya | Banka kampanyaları (Pazarama-Ziraat gibi) bazen en düşük fiyatı buradan çıkarır; büyük alımlarda kontrol etmeye değer. |
| Marka resmi siteleri | Giyim, ayakkabı | Sezon sonu indirimlerinde pazaryerinden ucuz olabilir; orijinallik garantisi kesin. |
| İkinci el/yenilenmiş: Letgo, Dolap, yenilenmiş cihaz siteleri | Telefon, konsol | Kullanıcı bütçesi zorluyorsa "yenilenmiş + garanti" seçeneğini öner. |

## Karşılaştırma siteleri ve kör noktaları

- **Akakçe** — en geniş mağaza havuzu, fiyat geçmişi grafiği (sahte indirim tespiti için birincil araç), fiyat alarmı. **Kritik:** Trendyol, Hepsiburada, Amazon TR gibi devler Akakçe listelerinden çekildi; Akakçe'deki "en ucuz" artık piyasanın en ucuzu olmayabilir. Akakçe sonucunu her zaman büyük pazaryerlerinde ayrı aramayla teyit et.
- **Cimri** — kampanya/kupon takibi ve market broşürleri (BİM/A101/Şok aktüel) için iyi; kapsam Akakçe'ye benzer şekilde eksik.
- **Epey** — fiyattan çok **teknik özellik karşılaştırması**; elektronikte iki aday arasında kalınca "fark ödediğin farkı hak ediyor mu" sorusunu burada yanıtla.
- Pratik doğrulama: Akakçe'deki en iyi iki fiyatı Cimri'de de gör; iki kaynakta benzer ise yanlış ürün eşleşmesi riski düşer.
- Karşılaştırma sitelerinde görünen fiyat, pazaryeri içi sepet kuponu/kart kampanyasını içermez — nihai fiyatı platformda doğrula.

## Satıcı güven kontrol listesi (sırayla)

1. Satıcı adı + rozet (resmi/yetkili satıcı mı?)
2. Satıcı puanı ve işlem hacmi — yüksek puan az işlemle anlamsızdır.
3. Ürün puanı ≠ satıcı puanı; ikisini ayrı oku.
4. Soru-cevap bölümü: satıcı yanıt veriyor mu, kaçamak mı?
5. Negatif ve orta yıldızlı (2-4) yorumların içeriği — asıl bilgi buradadır.
6. Şüphede: `"<satıcı adı>" şikayetvar` ve `"<satıcı adı>" technopat` web araması yap; Şikayetvar'da satıcı adına kayıtlı sahte ürün/iade sorunu deseni varsa uyar.
7. Elektronikte garanti tipi: distribütör (Türkiye) garantisi > ithalatçı garantisi. Fiyat farkı bazen sadece budur; kullanıcıya seçimi bırak ama farkı açıkla.

## Sahte yorum tespiti

Şüpheli desenler: aynı gün/kısa aralıkta yığılmış yorumlar; kopyala-yapıştır kalıplar (aynı cümle yapısı, aynı kapanış); yalnız 5 ve 1 yıldızda kutuplaşma; "harika, mükemmel, bayıldım" gibi detaysız genel ifadeler; alakasız/karanlık fotoğraflı zorlama görselli yorumlar.
Güvenilir desenler: artı ve eksiyi birlikte anlatan, kullanım detayı veren ("dikişleri sağlam ama fermuar sert"), zamana yayılmış, gerçek kullanım fotoğraflı yorumlar. Karar için 3-4 yıldızlı yorumları oku; ortalama puanı değil.

## Kampanya takvimi

Kasım (11.11, Black Friday/Efsane Günler), Ocak ve Temmuz sezon sonları (giyim), bayram öncesi kampanyalar, okula dönüş (Ağustos-Eylül, elektronik). Büyük alım + yakın kampanya dönemi = "bekle" önerisi meşrudur; Akakçe fiyat geçmişiyle destekle.

## Canlı doğrulama teknikleri (niş beden/varyant avı)

Site erişilebilirlik haritası (test edilmiş):
- **Boyner: canlı fetch AÇIK** — niş beden aramada birincil silah. Marka+kategori sayfasını fetch et; sayfanın içinde beden filtresi URL'leri hazır gelir (`?beden=38-30` gibi). Filtre URL'sini fetch et: **listelenen her ürün o varyantta gerçekten stokludur** — bu, canlı stok kanıtıdır ve doğrudan önerilebilir. Ürün linkleri `?barcode=` parametresiyle varyantı işaret eder. Boyner ayrıca W/L bedenlemeli çok markayı (Dockers, Levi's, Lee, Wrangler, Mavi, Pierre Cardin...) tek çatıda barındırır — filtre sayfasında marka kombinasyon linkleri de hazırdır.
- **Dockers TR, benzer marka siteleri: robots ENGELLİ** — ürün sayfası fetch edilemez; buradan gelen bilgi asla "stokta" diye sunulmaz.
- **Trendyol/HB: fetch kısmi/önbellek riskli** — arama snippet'lerindeki beden listeleri eski olabilir; stok kanıtı sayılmaz. Kullanıcıya uygulama içi beden filtresi tarifi verilebilir (filtre yalnız stoktakini gösterir).

- **Mavi (mavi.com): canlı fetch AÇIK — kumaş pantolonda W/L bedenlemenin adresi.** Kategori sayfaları (`/erkek/pantolon/gabardin/c/2` gibi) canlı facet sayıları döner (ör. "38 (29)", Boy "30 (31)", "Regular Straight (10)") ve ürün kartında kalıp adı yazar. Filtre URL deseni SAP Hybris `?q=:relevance:fit:Regular%20Straight` — ama beden facet'inin anahtarı sayfada link olarak gelmez, elle kurulamaz. SINIR: ürün sayfasında beden/boy seçici JS ile yüklenir → tek ürünün 38/30 stoğu statik fetch'le DOĞRULANAMAZ; bu yüzden Mavi önerileri her zaman "beden facet'i canlı, varyant stoğu sayfada teyit edilmeli" etiketiyle verilir. Alt kategoriler: gabardin/düz renk/kadife/keten/jogger/kargo; outlet ayrı (`/outlet/...`).
- **Colin's (colins.com.tr): canlı fetch AÇIK — Boyner'den bile iyi.** Kategori sayfası (`/c/erkek-pantolon-201` gibi) fetch edildiğinde her ürün kartında "Beden Seçiniz" satırıyla **stoktaki bedenler doğrudan listelenir** (28-30 ... 38-30 ... 42-34). Filtre URL'sine gerek yok: ürünün altında hedef beden yazıyorsa canlı stok kanıtıdır, yazmıyorsa yok demektir. Beden filtreleri checkbox/JS olduğu için URL'e çevrilemez — bunun yerine kart üstü beden listesi taranır. Kumaş pantolonları çoğunlukla S-XXL bedenler; W/L (38-30 gibi) bedenleme ağırlıkla jean/denim ürünlerde. Fit adları: Regular / Relaxed / Straight / Loose Straight / Slim / Slim Tapered / Baggy. Sayfalama: `/cis/<kategori>?pagenumber=2`.
- **Site erişim haritası (canlı test edilmiş):** Boyner AÇIK (filtre URL yöntemi) · Colin's AÇIK (kart üstü beden listesi yöntemi) · Dockers TR robots-ENGELLİ · Trendyol/Hepsiburada snippet=önbellek, stok kanıtı değil. Diğer adaylar (Mavi, LTB, LC Waikiki, DeFacto, Koton, FLO) ilk kullanımda aynı iki yöntemle test edilir: önce web_search ile kategori sayfası yüzeye çıkarılır (fetch izni için şart), sonra fetch edilip (a) sayfa içi beden-filtre URL'si veya (b) kart üstü beden listesi aranır; hangisi varsa o sitenin yöntemi olarak not edilir.

Yöntem sırası: (1) hedef markaları barındıran, fetch'e açık çok markalı perakendecinin (Boyner önce) kategori sayfasını canlı çek → (2) sayfa içinden gelen beden-filtre URL'sini çek → (3) çıkan ürün linklerini varyant kanıtıyla öner. Filtre URL'si sayfa içinden alınır, elde uydurulmaz. Önemli teknik not: web_fetch yalnızca konuşmada görünmüş URL'leri kabul eder; hedef sayfa reddedilirse önce web_search ile o URL'yi sonuçlarda yüzeye çıkar, sonra fetch et.
Ek kaynaklar: Marks & Spencer TR (çoğunlukla tek standart boy — kısa boyda çözüm değil), marka outlet sayfaları, Boyner "Tek Kalan Bedenler" kampanya sayfası (niş bedenler için indirim avı).
