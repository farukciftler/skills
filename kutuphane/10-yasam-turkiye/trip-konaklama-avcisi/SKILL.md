---
name: trip-konaklama-avcisi
description: Trip.com üzerinde çok şartlı konaklama araması yapar — tarih, şehir, tesis tipi, ücretsiz iptal (ve iptal son tarihi), özel banyo/tuvalet, yıldız, puan, bütçe, ve "şu landmark'a max N dakika yürüme mesafesi" gibi kısıtları tek bir filtreli arama URL'ine çevirir, sonuçları canlı okur, her adayı şart şart doğrular ve sıralı kısa liste verir. Kullanıcı "1-6 Ekim Londra'da ücretsiz iptal edilebilir, özel banyolu, British Museum'a 30 dk yürüme mesafesinde otel bul", "trip.com'da ara", "şu tarihlerde şu şehirde otel", "iptal edilebilir oda", "müzeye yakın otel", "bu otel iptal edilebilir mi", "toplam ne tutar" gibi bir şey dediğinde kullan. Kullanıcı "trip.com" demese bile, istek çok şartlı bir otel/konaklama aramasıysa devreye gir. Fiyat ve iptal politikası asla uydurmaz — okur ya da "okunamadı" der.
---

# Trip.com Konaklama Avcısı

Belirsiz ya da çok şartlı bir konaklama isteğini, Trip.com'un **gerçek filtre dilbilgisine**
çevirip tek bir derin link üreten; sonra o sayfayı okuyup her adayı **şart şart doğrulayan** skill.

Bu skill'in tüm değeri şurada: kullanıcı "ücretsiz iptal edilebilir" dediğinde, filtreyi
işaretlemekle yetinmeyip **iptal son tarihini oda bazında okumakta**. Filtre kaba eleme yapar,
karar detayda verilir.

## §0. Ortam tespiti — ilk iş bu

Araç listene bak, karar ver, kullanıcıya "hangi ortamdasın" diye sorma.

| Seviye | Elinde ne var | Ne yapabilirsin | Ek olarak hangi dosyayı okursun |
|---|---|---|---|
| **1 — Sohbet** | `web_search` + `web_fetch` | Şartları filtre şartnamesine çevir, **filtreli derin linki üret**, kullanıcıya doğrulama checklist'i ver. Fiyat/iptal tarihi **okuyamazsın** | `url-grameri.md`, `filtre-kodlari.md` |
| **2 — Tarayıcı** | Claude Browser MCP, Chrome eklentisi, Playwright/Puppeteer | Linki aç, **canlı fiyatı ve yürüme mesafesini oku**, adayları çıkar, detay sayfasında **iptal son tarihini oku** | + `tarayici-okuma.md` |
| **3 — Kod + kalıcı depo** | Claude Code: bash, dosya sistemi, cron | Aday havuzunu dosyaya yaz, fiyat/politika değişimini izle, tarih ızgarası tara, bildirim gönder | + `otomasyon.md` |

Seviyeler kümülatif. Emin değilsen bir seviye aşağı davran.

**Bu skill'de Seviye 1 yarım cevaptır ve bunu kullanıcıya açıkça söyle.** Uçak biletinden farklı
olarak burada kritik bilgi (iptal son tarihi, odanın banyosu özel mi, yürüme mesafesi) yalnızca
sayfada var. Seviye 1'de dürüst çıktı şudur: *"Şartlarının tamamını kodlayan arama linki hazır,
şu 4 şeyi açıp doğrulaman gerekiyor: ..."* — uydurulmuş bir kısa liste değil.

## Temel kısıt — uydurma

Trip.com liste ve detay sayfaları JavaScript ile render edilir; `web_fetch` fiyat da iptal
politikası da döndürmez. Bu yüzden bu skill'in tek gerçek başarısızlık modu **fiyat ya da iptal
şartı uydurmaktır.** Uydurulmuş bir iptal tarihine güvenip rezervasyon yapan kullanıcı para kaybeder.

Her sayı ve her politika ifadesi bir etiket taşımak zorunda:

| Etiket | Anlamı | Nereden gelir |
|---|---|---|
| **[OKUNDU]** | Sayfadan canlı okundu | Seviye 2/3. **Yanına okuma zamanını yaz** — Trip.com fiyatları gün içinde değişir |
| **[KANIT]** | Kaynağı ve tarihi olan yazılı bilgi | Otelin kendi sayfası, Trip.com politika metni, `web_fetch` ile alınmış |
| **[KULLANICI]** | Kullanıcının kendisi söyledi | "Booking'de 8.200 TL gördüm" |
| **[DOĞRULANMADI]** | Filtre geçti ama şart tek tek kontrol edilmedi | Aşağıdaki "tesis düzeyi tuzağı"na bak |

Etiketsiz sayı yazma. "Yaklaşık 6.000 TL civarı" gibi cümle kurma. Okuyamadıysan
**"okunamadı, link aşağıda"** doğru cevaptır.

## Akış

```
1. Şartname çıkar     → kullanıcının cümlesi → sert/yumuşak kısıt tablosu
2. URL kur            → sert kısıtlardan filtreli derin link (scripts/trip_url.py)
3. Listeyi oku        → Seviye 2/3: scripts/liste_oku.js ile yapılandırılmış aday listesi
4. Eşikle             → yürüme metresi, puan, bütçe → 5-8 adaya in
5. Detayda doğrula    → her aday için iptal son tarihi + oda banyosu + toplam fiyat
6. Sırala ve sun      → tek tablo + doğrulama linkleri + "neden elendi" notu
```

Adım 5'i atlama. Adım 5 bu skill'in var oluş sebebi.

---

## 1. Şartname çıkar

Kullanıcının cümlesini kısıt tablosuna çevir. Her kısıt için **nerede uygulanacağını** işaretle —
bu, sonradan hangi doğrulamayı yapman gerektiğini belirler.

Örnek: *"1-6 Ekim arası Londra'da, 28 Eylül'e kadar ücretsiz iptal edilebilir, özel banyosu
tuvaleti olan, hotel, British Museum'a max 30 dk yürüme mesafesinde"*

| Kullanıcı ifadesi | Tip | Trip.com karşılığı | Nerede uygulanır |
|---|---|---|---|
| 1–6 Ekim | sert | `checkin=2026-10-01&checkout=2026-10-06` (5 gece) | URL |
| Londra | sert | `cityId=338` | URL |
| hotel (apart/hostel değil) | sert | `75\|TAG_495` | URL |
| ücretsiz iptal | sert | `23\|10` | URL — **kaba eleme** |
| **28 Eylül'e kadar** iptal | sert | *karşılığı yok* | **Detay sayfası, oran bazında** |
| özel banyo | sert | `77\|92` | URL (tesis düzeyi) + **oda adı kontrolü** |
| özel tuvalet | sert | `77\|445` | URL (tesis düzeyi) + **oda adı kontrolü** |
| British Museum'a yakın | sert | `50\|50\|6789940` + sıralama `17\|12` | URL |
| max 30 dk yürüme | sert | *karşılığı yok* | **Okunan metre değerine eşik** (bkz. `mesafe-ve-konum.md`) |

Kural: sağ kolonda "detay sayfası" veya "kontrol" yazan her satır, adım 5'te bir doğrulama
maddesine dönüşür. Bunları çıktıda ayrı ayrı raporla.

**Tarih yılı belirtilmemişse** bugünün tarihine bak; geçmişteki bir tarihe denk geliyorsa
gelecek yıla al ve varsayımı çıktının başında tek satırda belirt.

## 2. URL kur

Tam dilbilgisi ve doğrulanmış parametreler: `references/url-grameri.md`.
Filtre kod tablosu (tesis tipi, oda olanakları, yıldız, puan, ödeme, politika):
`references/filtre-kodlari.md`.

Elle uğraşma, üreteci kullan:

```bash
python3 scripts/trip_url.py --city 338 --city-name London \
  --checkin 2026-10-01 --checkout 2026-10-06 --adults 1 --rooms 1 \
  --tip hotel --ucretsiz-iptal --ozel-banyo --ozel-tuvalet \
  --poi "51.5194133,-0.1269566,The British Museum,6789940" \
  --sirala yurume --curr TRY --locale tr-TR
```

`cityId` veya POI id'sini bilmiyorsan `references/mesafe-ve-konum.md` §1'deki keşif yöntemini
uygula — **uydurma**. Yanlış `cityId` sessizce başka bir şehrin sonuçlarını döndürür ve bu,
bu skill'in en sinsi hata modudur.

## 3–4. Oku ve eşikle

Seviye 2/3: linki aç, sayfa yüklendikten sonra `scripts/liste_oku.js` içeriğini çalıştır.
Otel adı, tip, yıldız, puan, yorum sayısı, **landmark'a yürüme mesafesi (metre)**, oda adı,
yatak, gecelik ve toplam fiyat, ödeme tipi ve etiketleri yapılandırılmış olarak döner.

Sonra eşikle:
- **Yürüme süresi:** metre → dakika dönüşümü ve hangi hızın kullanılacağı `mesafe-ve-konum.md` §2.
  30 dakika ≈ **2.400 m**. Eşiği geçenleri listeden çıkar, kaç tanesinin bu yüzden elendiğini not et.
- **Puan/yorum:** yorum sayısı 20'nin altındaki puan istatistiksel olarak anlamsız; puanı
  yüksek diye öne alma.
- **Bütçe:** kullanıcı bütçe verdiyse **toplam fiyat** üzerinden ele, gecelik üzerinden değil.

**10 kart tavanı.** Liste her seferinde yalnızca 10 kart basar; gerisi sonsuz kaydırmayla gelir
ve `page=2` gibi bir URL parametresi **yoktur** (denendi, yok sayılıyor). Bazı otomasyon
yüzeylerinde kaydırma hiç çalışmaz. Çıkış yolları `tarayici-okuma.md` §3'te — en önemlisi şu:
**sıralamayı kısıtına göre seçersen tavan zarar vermez.** `17|12` ile sıraladığında ilk 10 kart
zaten landmark'a en yakın 10 tesistir; yakınlık sorusunun cevabı listenin başındadır.

Ne okuduğunu dürüst yaz: "610 tesis filtreden geçti, en yakın 10 kart okundu" — "10 otel bulundu" değil.

## 5. Detayda doğrula — atlanamaz adım

Kalan 5–8 aday için her birinin detay sayfasını aç ve şunları oku. Yöntem ve tam metin kalıpları:
`references/iptal-ve-oda.md`.

**a) İptal son tarihi.** Detay sayfasında oran satırında şu biçimde yazar:
`Ücretsiz İptal 30 Eyl 16:00 öncesi` / `Free Cancellation before 16:00, Sep 30`.
Aynı otelde farklı oranların farklı son tarihi olabilir — **otelin değil, oranın** tarihini oku.

Karar mantığı — bunu ters çevirme:

> Kullanıcı "**28 Eylül'e kadar** iptal edebileyim" diyorsa, aradığın şey
> **iptal serbestlik tarihi ≥ 28 Eylül**'dür. Son tarihi 30 Eylül olan oran **geçer**
> (28'inde hâlâ ücretsiz iptal edebilir). Son tarihi 20 Eylül olan **kalır**.

Son tarih saat de içerir; sınıra yakın durumlarda saati de yaz ve saat diliminin **otelin yerel
saati** olduğunu belirt.

**b) Oda gerçekten özel banyolu mu.** Trip.com'un "özel banyo/tuvalet" filtresi **tesis
düzeyindedir**: tesiste özel banyolu *bir* oda varsa tesis listede kalır. Kartta gösterilen
oran ise **en ucuz** orandır ve ortak banyolu olabilir. Doğrulanmış gerçek: filtre uygulanmış
Londra listesinde bile "Ortak Banyolu Tek Kişilik Oda" / "Basic İki Yataklı Oda - Ortak Banyolu"
kartları çıkıyor. **Oda adını oku.** "Ortak Banyolu" / "Shared bathroom" geçiyorsa o oran elenir;
"En-suite" / "Özel banyo" geçiyorsa geçer; hiçbiri geçmiyorsa oda olanakları sekmesinden doğrula
ya da `[DOĞRULANMADI]` etiketiyle sun.

**c) Toplam fiyat.** Kart "gecelik" gösterir; kullanıcı toplamı sorar. `Toplam fiyat: X` satırını
oku ve vergi/ücret dahil olup olmadığını yaz. Şehir vergisi (London'da yok, Roma/Paris'te var)
otelde ayrıca alınabilir — dahil değilse belirt.

**d) Ödeme tipi.** Ön ödemeli mi, otelde ödemeli mi, kredi kartsız tutulabiliyor mu. "Ücretsiz
iptal" ile "ön ödeme" birlikte olabilir: para iade sürecine girer, anında geri gelmez.
Kullanıcı esneklik istiyorsa otelde ödemeli oran daha iyidir; bunu bir satırla söyle.

## 6. Sırala ve sun

Tek tablo. Rapor yazma. Satır sayısı 8'i geçmesin.

```
Varsayımlar: 1–6 Ekim 2026 (5 gece), 1 yetişkin 1 oda, TRY, tr.trip.com.
Filtre: Otel + Ücretsiz iptal + Özel banyo + Özel tuvalet, British Museum'a göre sıralı.
610 tesis filtreden geçti; ilk 30 kart okundu, 30 dk yürüme eşiğinde 12'si kaldı, ilk 6'sı aşağıda.

| Otel | Yürüme | Puan | Oda | Gecelik | Toplam | Ücretsiz iptal son tarih | Not |
|---|---|---|---|---|---|---|---|
| The Bloomsbury | 250 m / 3 dk | 9,4 (116) | Classic Queen | 550 $ [OKUNDU 25 Ağu 14:10] | 3.302 $ | 30 Eyl 16:00 ✅ | En-suite |
| Thistle Holborn | 230 m / 3 dk | 8,5 (103) | Standard Single | 361 $ [OKUNDU] | 2.167 $ | 27 Eyl 18:00 ❌ | 28 Eylül şartını karşılamıyor |

**Elenenler:** 4 tesis 30 dk eşiğini aştı, 2 tesis yalnızca ortak banyolu oran sunuyordu.

**Doğrulama linkleri**
- Filtreli arama: <derin link>
- The Bloomsbury: <detay linki>
```

Kurallar:
- Şartı karşılamayan adayı **tabloda tutabilirsin ama ❌ ile işaretle ve nedenini yaz.** Sessizce
  atmak, kullanıcının "neden bu çıkmadı" sorusunu doğurur.
- Neyin elendiğini say. "12 aday 30 dk eşiğinde kaldı" cümlesi, listenin güvenilirliğini kurar.
- Fiyatın okunma zamanını en az bir kez yaz.

---

## Varsayılanlar — sormadan uygula

Netleşmemiş her şey için makul varsayım yap ve **çıktının başında tek satırda** belirt.

- Yolcu: **1 oda, 2 yetişkin** — kullanıcı tek başına gittiğini ima etmediyse. Tek kişi ima
  ediliyorsa 1 yetişkin. (Trip.com varsayılanı 2'dir; 1 yetişkin fiyatı bazı otellerde farklıdır.)
- Para birimi: **TRY**, site `tr.trip.com`. Kullanıcı başka para birimi/dil isterse `--curr`/`--locale`.
- Sıralama: landmark verilmişse **yürüme mesafesi**, verilmemişse Trip.com önerisi.
- "Ücretsiz iptal" dendiğinde `23|10` filtresi **her zaman** açılır.
- "Otel" dendiğinde apart/hostel/pansiyon hariç tutulur (`75|TAG_495`). Kullanıcı "kalacak yer"
  gibi genel bir kelime kullandıysa tipi kısıtlama.
- Tarih aralığı gece sayısına çevrilir: 1–6 Ekim = **5 gece** (6 Ekim çıkış). Kullanıcı "5 gün"
  dediyse kaç gece kastettiğini varsayımda yaz.

Sadece şu iki durumda sor: (a) yolcu sayısı/kompozisyonu belirsiz ve fiyatı katlıyorsa
(2 yetişkin + 2 çocuk gibi — çocuk yaşları oda fiyatını değiştirir), (b) tarih hiç yoksa.

## Genel davranış kuralları

**Filtre ≠ garanti.** Trip.com'un birçok filtresi tesis düzeyinde çalışır, gösterilen oran ise
en ucuz orandır. Bir tesisi "özel banyolu" diye sunmadan önce **o oranın** oda adına bak.

**Boş sonuç bir cevaptır.** Şartların hepsi birlikte hiçbir sonucu bırakmıyorsa, uydurma —
hangi kısıtı gevşetirsen kaç sonuç açıldığını söyle: *"30 dk yerine 40 dk yaparsan 12 → 31 tesis."*
Hangi kısıtı gevşeteceğine kullanıcı karar verir.

**Yürüme süresi kestirimdir.** Trip.com'un verdiği metre değeri yürüme rotası mesafesidir
(`trafficType: walking`), kuş uçuşu değil — ama süre senin çevirdiğin bir tahmindir. Bagajla,
yokuşta, kalabalıkta yavaşlar. Sınıra yakın adaylarda (28–32 dk) bunu not düş.

**Puanı yorum sayısıyla birlikte oku.** 9,8 puanlı 11 yorumlu tesis, 8,6 puanlı 3.000 yorumlu
tesisten iyi değildir.

**Fiyat okuma zamanı önemlidir.** Trip.com fiyatları gün içinde ve oturuma göre değişir
("üye fiyatı", promosyon kodu, ilk rezervasyon indirimi). Okuduğun fiyatın kullanıcıda birebir
çıkmayabileceğini bir kez söyle, her satırda tekrarlama.

**Son tıklama kullanıcının.** Tarayıcı sürebiliyor olsan bile rezervasyonu tamamlama, ödeme
bilgisi girme, hesap açma. Doğru oteli ve doğru oranı bul, ödeme ekranına kadar getir — kararı
ve ödemeyi kullanıcı verir.

**Konum.** Kullanıcı İstanbul'da; para birimi ve dil varsayımı bu yüzden TRY / tr.trip.com.

## Referans dosyaları

- `references/url-grameri.md` — Trip.com liste ve detay URL'lerinin doğrulanmış parametreleri,
  `listFilters` dilbilgisi, camelCase tuzağı. **URL kurarken her zaman oku.**
- `references/filtre-kodlari.md` — tesis tipi, oda/tesis olanakları, yıldız, misafir puanı,
  yatak, öğün, ödeme, politika, sıralama ve fiyat aralığı kodlarının tam tablosu.
- `references/mesafe-ve-konum.md` — `cityId`/POI id keşfi, landmark filtresi, metre→dakika
  dönüşümü, yürüme eşiği mantığı, harita görünümü. **Landmark/mesafe kısıtı varsa oku.**
- `references/iptal-ve-oda.md` — iptal son tarihini okuma, tarih karşılaştırma mantığı,
  ortak banyo tuzağı, ödeme tipleri, iade süreci. **Adım 5'te her zaman oku.**
- `references/tarayici-okuma.md` — sayfayı okuma tarifi, lazy-load/kaydırma, kırılgan seçici
  tuzağı, React fiber'dan yapılandırılmış veri çekme, bloklanma hijyeni. **Seviye 2/3'te oku.**
- `references/otomasyon.md` — çoklu tarih/şehir tarama, fiyat ve politika izleme, cron.
  **Sadece otomasyon isteniyorsa oku.**
- `scripts/trip_url.py` — filtreli Trip.com arama URL'i üreteci. Bağımlılık yok.
- `scripts/liste_oku.js` — liste sayfasından yapılandırılmış aday listesi çıkarır.
- `scripts/filtre_hasadi.js` — Trip.com filtre kodlarını sayfadan yeniden hasat eder
  (kodlar değişirse `filtre-kodlari.md` bununla tazelenir).
