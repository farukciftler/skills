# Tarayıcı Otomasyonu — Chrome Eklentisi / MCP ile Canlı Fiyat Okuma

Bu dosya yalnızca **tarayıcıyı sürebildiğin ortamlarda** geçerlidir: Claude in Chrome eklentisi,
bir Playwright/Puppeteer MCP sunucusu, ya da Claude Code içinden çalıştırılan headless tarayıcı.
Ortam tespitini SKILL.md §0'da yaptın; bu dosyayı sadece Seviye 2 veya 3'teysen oku.

Buradaki fark temel: artık fiyat **[KANIT]** olarak toplanabiliyor. Skill'in tahmin modundan
ölçüm moduna geçtiği yer burası.

---

## 1. Doğru araç, doğru iş

| İş | Araç | Neden |
|---|---|---|
| Tek rota, tek tarih fiyatı | Google Flights | En temiz veri, tüm taşıyıcılar |
| Ay boyu en ucuz gün | Google Flights **tarih ızgarası / fiyat grafiği** | Tek sayfada 30 gün, 30 ayrı arama yapma |
| "Her yer" keşfi | Google Flights **Explore** haritası | Fiyatı şehir şehir listeler |
| LCC kombinasyonu | Kiwi.com | Ayrı biletleri birleştirir |
| Kampanya metni | Havayolu kampanya sayfası | `web_fetch` yeterli, tarayıcı gerekmez |
| Açık çene (Medine giriş/Cidde çıkış) | Google Flights **çok şehirli** | Gidiş-dönüş kutusunda bu fiyat görünmez |

**Kural:** Tarayıcıyı en pahalı araç olarak gör. Bir kampanya sayfası `web_fetch` ile okunabiliyorsa
tarayıcı açma. Tarayıcıyı sadece **fiyat rakamı** gerektiğinde kullan.

## 2. Google Flights okuma yöntemi

### Sayfayı aç

Doğal dil `q=` parametresi en dayanıklı giriş noktası:

```
https://www.google.com/travel/flights?q=flights%20from%20IST%20to%20SKP%20on%202026-08-13%20returning%202026-08-16
```

Sayfa yüklendikten sonra fiyatların render edilmesi için **bekle** — hemen okumaya kalkarsan boş
veya "yükleniyor" değeri alırsın. Sonuç listesinde en az bir fiyat görünene kadar bekle, sabit
bir saniye sayısı verme.

### Okumayı DOM seçicisine değil, görünene dayandır

Google Flights sınıf adları obfuscated ve sık değişiyor. Sabit CSS seçicisi yazmak, 3 hafta sonra
sessizce yanlış veri üreten bir boru hattı demektir.

Sağlam yaklaşım sırası:
1. **Erişilebilirlik ağacı / metin içeriği** üzerinden oku — "1.850 TL", "2 sa 10 dk", "Aktarmasız"
   gibi görünür etiketler tarayıcı otomasyon araçlarının metin dökümünde çıkar.
2. **Ekran görüntüsü al ve oku.** Sayfa yapısı değişse de görsel okuma çalışır. Fiyat + taşıyıcı +
   süre + aktarma dörtlüsünü görüntüden çıkarmak, kırılgan seçiciden daha güvenilir.
3. Seçici yazmak zorundaysan, sınıf adı yerine **rol ve metin** üzerinden hedefle.

### Neyi kaydet

Her okuma için şu altı alanı topla, eksik olanı `null` bırak — uydurma:

`fiyat` · `para birimi` · `taşıyıcı` · `aktarma sayısı` · `toplam süre` · `kalkış saati`

Bunları `scripts/fiyat_deposu.py kaydet` ile depoya yaz. Depoya yazmadığın gözlem, bir sonraki
aramada yeniden aranmak zorunda kalır.

### Tarih ızgarası — en yüksek verimli hamle

Kullanıcı "başka tarihte avantajlı var mı?" diye sorduğunda 30 ayrı arama yapmak yerine Google
Flights'ın **tarih ızgarasını** (date grid) veya fiyat grafiğini aç. Tek ekran görüntüsü, bir ay
boyunca hangi Perşembe–Pazar çiftinin en ucuz olduğunu verir. Bu, skill'in Mod A'daki en verimli
tek hareketi.

Aynısı Explore haritası için geçerli: tek sayfada 40 şehrin fiyatı. Havuz filtresini bu ekran
üzerinden uygula, sonra sadece kazananları tek tek doğrula.

## 3. Hijyen — bloklanmamak ve dürüst kalmak

- **Kullanıcının kendi tarayıcı oturumunu kullan.** Chrome eklentisi ile çalışırken zaten
  böyledir; insan hızında, insan oturumunda gezinmek hem daha az bloklanır hem doğru duruştur.
- **İstek hızını sınırla.** Aramalar arasına bekleme koy. 40 rotayı 40 saniyede taramaya çalışmak
  CAPTCHA'ya, ardından o oturumda hiç veri alamamaya götürür.
- **Toplu kazıyıcı kurma.** Google Flights ve Skyscanner kullanım şartları otomatik toplu veri
  çekmeyi yasaklar. Kişisel kullanım için birkaç rotayı kontrol etmek ile binlerce sorgu atan bir
  servis kurmak farklı şeylerdir; ikincisini kullanıcı isterse §5'teki API yoluna yönlendir.
- **CAPTCHA çıkarsa dur.** Aşmaya çalışma. Kullanıcıya söyle, o elle çözsün veya API yoluna geç.
- **Login duvarı arkasına girme.** Kullanıcının hesabıyla bilet satın alma adımını **asla kendi
  başına tamamlama** — fiyatı bul, ödeme ekranına kadar getir, kararı ve son tıklamayı kullanıcıya
  bırak. Para harcayan son adım kullanıcının.

## 4. Doğrulama — kendi okumana da güvenme

Tarayıcıdan okunan fiyatlar için iki sağlama:

1. **Mantık sınırı.** Okunan değer statik banda göre 10 kat sapıyorsa muhtemelen yanlış alanı
   okudun (örn. tek yön yerine kişi başı vergi, ya da başka rotanın satırı). Yeniden oku.
2. **Çapraz kontrol.** 🔴 hata fiyatı iddiası üretecekseniz, aynı fiyatı **ikinci bir kaynakta**
   (havayolunun kendi sitesi) gör. Tek okumaya dayanarak "hata fiyatı buldum, hemen al" demek,
   kullanıcıyı yanlış yönlendirmenin en pahalı biçimi.

Okuma başarısızsa bunu **söyle**. "Google Flights'ta fiyat okunamadı, sayfa değişmiş olabilir;
link aşağıda" cümlesi, uydurulmuş bir rakamdan sonsuz daha değerli.

## 5. Tarayıcı yerine API — sürdürülebilir yol

Kullanıcı düzenli, otomatik tarama istiyorsa (cron, günlük bülten, fiyat alarmı) tarayıcı yanlış
temeldir: kırılgan, yavaş, şartlara aykırı. Bunun yerine resmî erişim:

| Kaynak | Ne verir | Not |
|---|---|---|
| **Amadeus Self-Service API** | Uçuş teklifleri, en ucuz tarih, esnek arama | Ücretsiz test katmanı var; prod için kota satın alınır |
| **Duffel** | Gerçek satılabilir teklifler | Rezervasyona kadar gider |
| **Travelpayouts / Aviasales** | Toplanmış en düşük fiyat verisi, ucuz bilet akışı | Ortaklık programı üzerinden, fiyat takibi için pratik |
| **Kiwi Tequila** | Arama + "anywhere" sorgusu | Kota politikası değişken |
| **Havayolu kampanya sayfaları** | Kampanya metni | Zaten serbest, `web_fetch` yeterli |

Bu API'lerin güncel kota/fiyat koşullarını **her seferinde arat**; bu alan hızlı değişiyor.
Kurulum ve boru hattı için `otomasyon-boru-hatti.md`.
