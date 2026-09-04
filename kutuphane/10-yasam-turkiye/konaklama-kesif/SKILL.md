---
name: konaklama-kesif
description: Global konaklama keşif uzmanı — herhangi bir ülke/şehir için HER SORGUDA üç kanalı birden — otel, Airbnb/apart/daire ve hostel-private/pansiyon — ve yerel kiralık seçeneklerini SADECE OTA'larla sınırlı kalmadan (yerel forumlar, Facebook grupları, Telegram kanalları, Reddit, yerel rezervasyon siteleri) tarar; en merkezi ve ulaşımı kolay bölgelerde, özel banyolu seçenekleri, TL bazında fiyatlarla, misafir yorumları + WiFi kalitesi + çevre bilgisiyle sunar. Paralel (karaborsa) döviz kuru olan ülkelerde resmi kur ve karaborsa kurunu ayrı ayrı gösterir ve fiyatı her iki kurla TL'ye çevirir. Kullanıcı "X ülkesinde Y şehrinde şu kadar gün kalacağım", "nerede kalayım", "otel bul", "Airbnb bak", "konaklama araştır", "ucuz pansiyon", "aylık kiralık daire", "where to stay in..." dediğinde ya da herhangi bir seyahat planında konaklama ayağı gündeme geldiğinde bu skill'i kullan — kullanıcı "skill" veya "detaylı araştır" demese bile. Otel/kur bilgisini asla ezberden verme; her seferinde canlı web araştırması yap.
---

# Konaklama Keşif Uzmanı

Global konaklama araştırması yapan uzman. Amaç: kullanıcıya belirli bir şehirde, belirli bir süre için **en merkezi, ulaşımı kolay, özel banyolu** konaklama seçeneklerini **TL bazında**, güvenilir ve güncel verilerle sunmak.

## Temel İlkeler

1. **Asla ezberden fiyat/kur verme.** Fiyatlar ve kurlar her konuşmada web_search ile canlı doğrulanır. Eğitim verisindeki fiyat bilgisi kesinlikle kullanılmaz.
2. **OTA'lar başlangıç noktasıdır, son nokta değil.** Booking/Airbnb fiyatı referans alınır; ardından yerel kanallar (forumlar, FB grupları, yerel siteler, doğrudan otel sitesi) taranır. Yerel kanal çoğu ülkede %15-40 daha ucuz olabilir. Bkz. `references/yerel-kaynaklar.md`.
3. **Özel banyo varsayılan filtredir.** Hosteller ancak "private room + private bathroom" ise listelenir. Shared bathroom seçenekleri elenmeli; belirsizse "banyo bilgisi doğrulanamadı" notu düşülür.
4. **Paralel kur şeffaflığı.** Hedef ülkede karaborsa/paralel kur varsa (bkz. `references/paralel-kur.md`) her fiyat İKİ kurla gösterilir. Nakit götürüp karaborsada bozdurmanın pratik etkisi açıklanır.
5. **Merkeziyet > mutlak ucuzluk.** Varsayılan öncelik: şehir merkezine/ana gezilecek yerlere yürüme veya kısa toplu taşıma mesafesi. Kullanıcı aksini söylemedikçe banliyö/uzak ucuz seçenekler ancak "bütçe alternatifi" olarak eklenir.

## İş Akışı

### Adım 0 — Girdiyi netleştir (gerekirse tek soruda)
Gereken: ülke + şehir + gün sayısı. Varsa: tarih aralığı, kişi sayısı, bütçe tavanı, tercih (otel mi daire mi). Eksikler tek bir kısa soruyla toplanır; tarih yoksa "önümüzdeki 30 gün içinde" varsayılır ve bu varsayım belirtilir. 7+ gün konaklamalarda haftalık/aylık indirimler (Airbnb weekly/monthly discount, apart aylık fiyat) mutlaka kontrol edilir.

### Adım 1 — Şehir haritasını çıkar (1-2 arama)
- "best area to stay in [city]" + "[city] city center where to stay reddit"
- Çıktı: 2-3 aday bölge; her biri için merkeziyet, ulaşım (metro/tramvay/havalimanı bağlantısı), güvenlik notu.

### Adım 2 — Üç zorunlu kanal taraması (3-5 arama)
Her sorguda ÜÇ konaklama türü de ayrı ayrı taranır — süre kısa olsa bile. Birini atlamak skill ihlalidir; sonuç bulunamazsa "tarandı, uygun sonuç yok" diye raporlanır.

**2a. Otel (OTA):** "[city] hotels [dates/month] price" — Booking/Agoda/Hotels.com/Kayak sonuçları.

**2b. Airbnb / apart / kısa dönem daire (ZORUNLU):** "[city] airbnb [month] price per night", "[city] serviced apartment / aparthotel price", "[neighborhood] entire flat airbnb". Vrbo, Plum Guide, yerel kısa-dönem siteleri de sayılır. 7+ gecede weekly/monthly indirim; kısa kalışta da studio/özel-girişli oda seçeneği mutlaka sunulur. Airbnb fiyatlarında temizlik + servis ücretinin gecelik fiyatı %15-30 şişirdiği hesaba katılır ve toplam fiyat üzerinden karşılaştırılır.

**2c. Hostel private / az kişili dorm:** "[city] best hostels private room / 4-bed dorm price". Özel banyo kuralı gereği varsayılan öneri hostel PRIVATE oda; kullanıcı bütçe sinyali verirse ("ucuz", "en ucuzu", "dorm olur") 4-6 yataklı, tercihen ensuite dorm'lar da eklenir ve ortak banyo açıkça etiketlenir.

- Her aday için topla: **tesis adı, gecelik/dönemlik fiyat (yerel para + USD), puan ve yorum sayısı, yorumların özü (2-3 cümle: ne övülüyor, ne şikayet ediliyor)**.

### Adım 3 — Yerel kanal taraması (2-4 arama)
`references/yerel-kaynaklar.md` dosyasını oku, ülkeye uygun kanalları seç:
- "[city] guesthouse/pension direct booking price forum"
- Reddit: "[city] cheap accommodation reddit 2026"
- Bölgeye özgü site/grup adlarıyla arama (ör. Japonya→Rakuten Travel, Rusya/BDT→Ostrovok, Arap ülkeleri→Almosafer, Latam→FB grupları)
- Uzun kalışta: "furnished apartment [city] monthly rent [local site name]"
- Bulunan yerel fiyat OTA fiyatından belirgin düşükse, farkı ve rezervasyon yöntemini (WhatsApp, e-posta, kapıdan pazarlık) açıkça yaz.

### Adım 4 — WiFi ve çevre doğrulaması (1-2 arama, önerilen tesisler için)
- "[hotel name] wifi speed review" / yorumlarda "wifi" geçen bölümler
- WiFi bilgisi yoksa: dürüstçe "yorumlarda WiFi verisi yok" de; şehir geneli mobil internet alternatifi (eSIM/yerel hat fiyatı) tek cümleyle ekle. Uzaktan çalışacak kullanıcı sinyali varsa WiFi araştırmasını derinleştir.
- Yakın çevre: her tesis için 3-5 madde — yürüme mesafesindeki önemli noktalar (meydan, çarşı, metro istasyonu, market, hastane/eczane).

### Adım 5 — Kur hesabı
1. `references/paralel-kur.md` listesine bak. Ülke listede mi?
2. **Listede değilse:** "yerel para → TRY" güncel resmi kur webden çekilir, tek kurla TL hesabı yapılır. USD/TRY kuru da mutlaka canlı çekilir.
3. **Listedeyse:** hem resmi kur hem paralel kur canlı aranır ("[currency] black market rate today", ülkeye özel kaynaklar referans dosyasında). Her fiyat şu formatta sunulur:

```
Gecelik: 45 USD
  → Resmi kur (1 USD = X yerel): ~Y.YYY TL
  → Karaborsa kuru (1 USD = Z yerel): ~W.WWW TL
```

4. Pratik tavsiye eklenir: ödemeyi hangi para/yöntemle yapmak avantajlı (nakit USD/EUR götür, kartla ödeme resmi kurdan geçer, vb.).

## Çıktı Formatı

Kısa bir bölge özeti + tesis kartları. Her tesis kartı:

```
### 1. [Tesis Adı] — [Bölge] · [tür: otel/apart/Airbnb/pansiyon]
- Fiyat: [gecelik yerel + USD] → toplam [N gece]: ~X TL [paralel kur varsa iki satır]
- Özel banyo: ✓ (doğrulandı / ilana göre)
- Puan: 8.7/10 (1.240 yorum) — "temizlik ve konum övülüyor, kahvaltı zayıf bulunuyor"
- WiFi: yorumlarda hızlı/stabil deniyor · veya: veri yok
- Konum & çevre: [merkeze mesafe, metro, yürünebilecek 3-5 nokta]
- Rezervasyon: [OTA linki bilgisi / doğrudan kanal — hangisi ucuzsa belirt]
```

- 4-6 tesis: en az 1 otel + en az 1 Airbnb/apart/daire + en az 1 bütçe seçeneği (hostel private veya yerel kanal). Bir kanalda uygun sonuç yoksa bu açıkça yazılır, sessizce atlanmaz.
- Sonda tek paragraf "Karar özeti": hangi seçenek hangi profile uygun + kur/ödeme taktiği.
- Uygunsa places_search + places_map_display_v0 ile harita göster.
- Toplam maliyet her zaman **kalınan gün sayısı üzerinden toplam TL** olarak da verilir.

## Dürüstlük Kuralları

- Fiyatlar tarih/sezona göre oynar; bulunan fiyatın hangi tarih/kaynağa ait olduğu belirtilir, "±%20 oynayabilir" uyarısı eklenir.
- Doğrulanamayan iddia (WiFi, banyo, güncel fiyat) tahminle doldurulmaz; "doğrulanamadı" yazılır.
- Karaborsa kuru kullanımının bazı ülkelerde hukuken gri/yasak olduğu tek cümleyle not edilir; skill sadece bilgiyi şeffaflaştırır, yönlendirme yapmaz.
- Güvenlik sorunu bilinen bölge/tesis varsa açıkça söylenir.
