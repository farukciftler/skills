---
name: oyuncak-pazar-radari
description: Masifico için oyuncak/SKU düzeyinde pazar araştırması uzmanı — Trendyol, Hepsiburada, Etsy ve Google Trends sinyallerinden talep ölçümü (yorum hızı, "son 3 günde satıldı" etiketi, stok-delta takibi), rekabet yoğunluğu ve masif/MDF ayrıştırması, fiyat bandı çıkarımı, pazar açığı tespiti, ihracat (Etsy) sinyali ve B2B/kamu (EKAP, Yuvamız İstanbul, doğrudan temin) radarı; sonucu 0-20 Fırsat Skoru ve üret/revize/vazgeç kararıyla raporlar. Kullanıcı "pazar araştırması", "talep var mı", "bu ürün satar mı", "satıyor mu", "rekabet nasıl", "pazar açığı/fırsat", "hangi SKU'yu üreteyim", "fiyatı ne olmalı", "rakipler ne yapıyor", "Etsy'de gider mi", "ihale", "kreş alımı", "trend ne", "hangi kategori" dediğinde; yeni bir oyuncak fikri/SKU adayı atıldığında; rakip ürün linki paylaşılıp görüş istendiğinde; sezon/kampanya planı yapılırken; veya seri üretim öncesi ürün seçimi konuşulduğunda bu skill'i kullan. "Araştır" kelimesi geçmese bile bir ürünün pazarına dair karar veriliyorsa devreye gir. Her analiz canlı web aramasıyla yapılır; ezbere pazar verisi asla kullanılmaz.
---

# Oyuncak Pazar Radarı

Masifico'nun (masif kayın, Montessori-tarzı + tasarım oyuncakları, İstanbul) SKU düzeyinde pazar kararlarını veriye bağlayan araştırma sistemi. Çıktı her zaman: ölçülmüş talep + rekabet + fiyat bandı + farklılaşma → **Fırsat Skoru** → net karar.

## Temel kurallar

1. **Asla ezberden pazar verisi verme.** Her analizde canlı web araması yap. Bu dosyadaki taban veriler sadece bağlam içindir ve tarihlidir (Ağustos 2026).
2. **Her tahmin aralık + "tahmin" etiketiyle verilir.** Kesin satış adedi kimsede yok; tüm araçlar kamuya açık sinyalden türetir.
3. **Tek metriğe güvenme; üçgenle.** En az iki bağımsız sinyal aynı yönü göstermeden hüküm verme.
4. **Mevsimsellik notu düş:** oyuncakta Kasım-Aralık (yılbaşı) ve bayram/23 Nisan zirvedir; kreş/kurum alımları Ağustos-Eylül'de yoğunlaşır. Ölçüm ayını rapora yaz.
5. Masifico bağlamı sabittir: premium konum (perakende 450-1.500 TL, vitrin 1.750-2.500 TL), masif kayın, CE/EN 71 süreci, kanallar = kreş toptan + Instagram/site + Etsy ihracat.

## Metodoloji — 6 adım

Basit soruda (tek ürün, tek platform) ilgili adım tek başına çalıştırılabilir.

### Adım 1 — Talep ölçümü (TR)

Trendyol'da kategori/ürün araması ("montessori ahşap [ürün]", "[ürün] ahşap", markasız genel terim). Sinyaller ve okunuşları:

| Sinyal | Nasıl okunur |
|---|---|
| "Son 3 günde X ürün satıldı" etiketi | En değerli canlı sinyal; görünüyorsa günlük hız ≈ X/3. Aralıklı gösterilir — yokluğu "satmıyor" demek değildir |
| Yorum sayısı | **1 yorum ≈ 8-15 satış** (Trendyol uygulama içi yorum teşviki nedeniyle; eski ×50-100 e-ticaret ezberi Trendyol'da GEÇERSİZ). 200 yorumlu ürün ≈ 1.600-3.000 adet |
| Yorum hızı | Son yorum tarihlerinden haftalık yeni yorum sayısı × 8-15 = güncel haftalık satış tahmini. Toplam yorum geçmişi, yorum hızı bugünü gösterir |
| Favori sayısı ve artışı | Niyet göstergesi; birkaç gün arayla değişimi izle |
| Stok-delta | Derin analizde: stok/“sepette azaldı” adedini not et, 2-3 gün sonra tekrar bak; fark ≈ satış hızı. (Sepete yüksek adet ekleme hilesi Trendyol'da çoğunlukla çalışmaz — sepet tavanı var) |
| "Çok Satan" rozeti | Kategori içi satış hızına göre otomatik verilir (favori/yorum saymaz) — rozetli ürün = kategori hız lideri |

Google Trends TR (5 yıl): "montessori oyuncak", "ahşap oyuncak" + ürün terimi — yükselen mi, platoda mı; mevsim desenini not et. Değerler görelidir; nişleri "oyuncak" ana terimiyle kıyasla.

Araçlar (kullanıcı isterse öner; fiyatlar Ağustos 2026): **SatışAnaliz** (ücretsiz plan + ~₺349-799/ay; Trendyol kelime hacmi analizi), **TPro360** (ücretsiz + ~₺500-2.000/ay; stok-delta satış takibi, Buy Box, kâr hesabı), Pazarus "Ne Kadar Sattı" / nekadarsatti.com (ücretsiz hızlı bakış). Çıktıları "karar destek aralığı" olarak oku.

**Talep puanı (0-5):** 0 = arama sonuçları boş/ilgisiz · 3 = ilk sayfada düzenli satan 3-5 ürün · 5 = çok satıcılı, "son 3 günde" etiketli, yorum hızı yüksek canlı kategori.

### Adım 2 — Rekabet yoğunluğu

Aynı aramanın ilk sayfasını (ilk 20-24 sonuç) analiz et:

- **Satıcı/ürün sayısı:** aynı ürün tipinde kaç farklı satıcı? 100+ satıcılı jenerik ürün = fiyat savaşı, marj ölümü.
- **Malzeme dağılımı (kritik):** kaçı gerçek masif, kaçı MDF/kontrplak/lazer-kesim? Başlıkta "ahşap" yazan çoğu ürün MDF'dir — açıklama/yorum/fotoğraf kesitinden doğrula. Masif oranı düşükse Masifico için açık kapı.
- **Fiyat dağılımı:** taban-tavan açıklığı. Tabana sıkışmış dar bant = marj baskısı; geniş dağılım = premium konumlanma alanı.
- **Marka yoğunluğu:** tek güçlü marka mı, dağınık pazar mı? İthal premium (Grimm's, PlanToys tarzı) ilk sayfadaysa fiyatları senin tavanını tanımlar.
- **CE/sertifika söylemi:** kaç rakip CE/EN 71'i açıkça yazıyor? Azsa güven farklılaşması kozu.

**Rekabet puanı (0-5, yüksek = kötü):** 0 = niş boş · 3 = 10-30 ciddi rakip, karışık kalite · 5 = yüzlerce satıcı, dip fiyat savaşı.

### Adım 3 — Fiyat bandı ve marj kontrolü

İlk sayfa fiyatlarından üç nokta: **taban (en ucuz %10), medyan, tavan (en pahalı %10)**. Masifico maliyet modeliyle çarpıştır (hesabı maliyet-fiyat skill'i yapar; buradaki oranlar hızlı eleme içindir):

- Kanal kesintileri (Ağustos 2026 tabanı): Trendyol komisyon **%19** (resmi tablo; panelindeki oran bağlayıcı) + 10,99 TL hizmet bedeli + desi kargo → etkin ~%40-50 · kreş toptan = perakendenin ~%50-60'ı · kendi kanal ~%12-15 · Etsy ~%17-25.
- Soru: pazarın tavan bandında satarken hedef kanalda en az %30 brüt kalıyor mu? Kalmıyorsa ürün yeniden tasarlanır ya da vazgeçilir.

**Marj puanı (0-5):** 0 = tavan fiyatta bile marj yok · 3 = tek kanalda çalışıyor · 5 = üç kanalda da rahat marj.

### Adım 4 — Farklılaşma denetimi

Masifico'nun dört kozunu ilk sayfa rakiplerine karşı test et: (1) masif kayın kaçında var, (2) CE/EN 71 belgesi kaçı gösteriyor, (3) yerli el işçiliği/İstanbul hikâyesi kaçı anlatıyor, (4) tasarım dili — ilk sayfa görsel olarak jenerik mi?

Ek: bu SKU'da bizim versiyonun *ürünsel* farkı ne olurdu? Fark cümlesi tek nefeste söylenemiyorsa farklılaşma zayıftır → farklılaşma skill'ine gönder (o inşa eder, bu skill puanlar).

**Farklılaşma puanı (0-5):** 0 = aynısını herkes yapıyor · 3 = 4 kozdan 2'si ilk sayfada yok · 5 = ilk sayfada bu kombinasyonu sunan kimse yok.

### Adım 5 — İhracat sinyali (Etsy)

Etsy'de İngilizce terimle ara ("wooden montessori [product]", "balance stones", "wood robot toy"):

- İlk sayfa fiyat bandı (USD) ve Bestseller/"Popular now" rozetleri (kategori-görece satış hızıyla verilir, eşik gizli)
- Review sayıları ve mağaza yaşları; **TR zanaatkâr satıcılar Etsy'de var ve yaşıyor** (ör. WoodenDesignTurkiye, MontessoriProducts/İstanbul — Star Seller) — varlıkları kanal fizibilitesinin kanıtı
- Görünürlük gerçekleri (2026): ABD'ye <$6 kargo aramada öne çıkar; her listing'de iade politikası tanımlı olmalı; ≥5 foto/≥2000px; Star Seller eşikleri (%95 24s yanıt, %95 zamanında kargo, ≥4.8 puan)
- Araçlar: **eRank** (~$5.99-29.99/ay — en ucuz ciddi seçenek), **EverBee** (~$29.99+/ay, ciro tahmini), **Alura** (cömert ücretsiz plan). Hedef: yüksek arama hacmi + düşük rekabet kesişimi
- Taban fiyat bantları (Ağustos 2026, spot): denge taşları $30-90 · ahşap robot $20-110 · dizme kule $15+
- **ABD notu:** de-minimis kalktı (2025) + TR'ye %12,5 ek tarife (dava sürüyor) → alıcı tarafında sürpriz maliyet; **AB, düşük sürtünmeli Etsy şeridi.** ABD'ye satış kararı mevzuat skill'iyle birlikte verilir.

**İhracat puanı bonus +0-3:** karara ek bonus; ana skora girmez (Etsy tek başına SKU taşıyabilir ama TR kararını maskelemesin).

### Adım 6 — B2B/kamu radarı (istenirse veya kreş SKU'sunda otomatik)

- **Yuvamız İstanbul:** 127 merkez / 35 ilçe (Haziran 2026), büyümede. İBB alımları EKAP'ta çoğu kez "mefruşat/donatım" başlığı altında — "oyuncak", "kreş", "anaokulu donatım" anahtar kelimeleriyle EKAP taraması yap.
- **Doğrudan temin 22/d (2026):** büyükşehirde 1.021.827 TL'ye kadar tek teklifle alım mümkün — belediye kreşlerine kapı budur; açık ihalede iş deneyim belgesi (~%25) istenebilir.
- İhale şartlarında tipik istekler: CE + EN 71 raporları + Türkçe etiket + fatura; TSE gönüllü ama şartnamede istenebilir.
- Canlı örnek arama: EKAP'ta "oyuncak satın alınacaktır" duyuruları (belediyeler doğrudan oyuncak alıyor).

## Fırsat Skoru ve karar

**Skor = Talep + Farklılaşma + Marj + (5 − Rekabet)** → 0-20

| Skor | Karar |
|---|---|
| 14-20 | **Üret.** Prototipe al, seri planla |
| 9-13 | **Revize.** Ürünü/fiyatı/açıyı değiştir, tek zayıf kalemi düzelt, yeniden ölç |
| 0-8 | **Vazgeç.** Enerjiyi başka SKU'ya taşı |

Etsy bonusu 2-3 ise "TR zayıf ama ihracat SKU'su olabilir" notu düş.

## Rapor şablonu

1. **Tek cümle karar** (skor + üret/revize/vazgeç)
2. Talep: sinyaller + tahmini hacim aralığı ("tahmin" etiketiyle, hangi sinyalden türetildiği yazılı)
3. Rekabet: satıcı sayısı, masif/MDF oranı, fiyat dağılımı
4. Fiyat önerisi: kanal bazında (kreş toptan / kendi kanal / Trendyol / Etsy USD) — kesin hesap maliyet-fiyat skill'ine devredilir
5. Farklılaşma cümlesi: "Bizim versiyonu farklı kılan şey: ..."
6. Riskler + mevsimsellik notu
7. Kaynak tarihi ("ölçüm: [ay yıl]") ve kullanılan sinyaller

## Taban veriler (Ağustos 2026 itibarıyla — bayatlar, önemli kararda yeniden doğrula)

- Küresel ahşap oyuncak pazarı ~28-31 milyar $ (2025), yıllık ~%4-6 büyüme; sert ağaç (kayın dahil) pazarın ~%58'i; **kreş/anaokulu talebi pazarın ~%26'sı** (B2B kanalının gücüne kanıt). Montessori alt pazarı tanıma göre 0,5-2,5 milyar $ (5 kat tanım farkı — dikkat).
- Türkiye oyuncak pazarı 0,8-1,0 milyar $ (Statista ~820 M$ vs sektör derneği ~1 milyar $); ~%75 ithalat payı; bazı kategorilerde ithalat gözetim ücretleri arttı = yerli üreticiye rüzgâr.
- TR premium çapa fiyatları (Trendyol, spot): Grimm's 1.393-4.750 TL (tavan çapası) · Wood&Joy 1.750-6.900 TL · yerli el yapımı premium (denge taşı ~1.500 TL, blok 820-1.450 TL) · seri/MDF bandı 135-450 TL. **~900-3.000 TL bandı yerli masif üretici için görece açık.**
- 2026 tasarım trendi: toprak tonları, soluk pasteller, dokusal yüzeyler, modüler/sistem oyuncaklar; neon dönemi kapandı.
