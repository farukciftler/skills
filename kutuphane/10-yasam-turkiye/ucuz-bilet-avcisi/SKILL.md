---
name: ucuz-bilet-avcisi
description: Hunts underpriced flights out of Istanbul and turns a vague travel wish into a ranked, evidence-backed shortlist with ready-to-click search links. Two modes — open-destination deal hunting ("perşembe gidiş pazar dönüş fırsat var mı", "vizesiz nereye ucuz uçarım", "error fare var mı", "bu fiyat indirimli mi") and targeted routing, especially Umrah ("umre için bilet ara", "Cidde mi Medine mi", "aktarmalı mı aktarmasız mı", "kampanyalı bilet var mı", "başka tarihte avantajlı mı"). Also for judging a quoted fare, open-jaw versus return, IST versus SAW, Ramadan/Hajj/holiday price peaks. Adapts to environment — chat gathers campaign evidence and hands over links; a Chrome extension or browser MCP reads live fares off Google Flights date grids and Explore maps; Claude Code builds a price-history store with empirical scoring and cron monitoring ("fiyat takibi kur", "kampanyaları tara", "fırsat çıkınca haber ver", "uçuş fiyatı botu"). Use it even when the person never says "ucuz". Never invents prices.
---

# Ucuz Bilet Avcısı

İstanbul kalkışlı biletlerde "bu fiyat gerçekten fırsat mı?" sorusuna kanıtla cevap veren, ve
belirsiz bir seyahat isteğini sıralı bir kısa listeye çeviren skill.

## §0. Ortam tespiti — ilk iş bu

Bu skill üç farklı yetenek seviyesinde çalışır. **Hangi seviyedeysen ona göre farklı iş yaparsın.**
Elindeki araç listesine bak ve karar ver; kullanıcıya "hangi ortamdasın" diye sorma.

| Seviye | Elinde ne var | Ne yapabilirsin | Hangi dosyayı okursun |
|---|---|---|---|
| **1 — Sohbet** | `web_search` + `web_fetch` | Kampanya kanıtı topla, statik banda göre skorla, kullanıcıya tıklanabilir arama linki ver. Fiyat rakamını **okuyamazsın** | `arama-kaynaklari.md` |
| **2 — Tarayıcı** | Chrome eklentisi, Playwright/Puppeteer MCP, veya tarayıcı süren herhangi bir araç | Google Flights'ı açıp **gerçek fiyatı oku**, tarih ızgarasını tara, Explore haritasından "her yer" fiyatı çek, çok şehirli açık çene fiyatı gör | + `tarayici-otomasyonu.md` |
| **3 — Kod + kalıcı depo** | Claude Code / sunucu: bash, dosya sistemi, cron, `scripts/` | Gözlem geçmişi biriktir, **ampirik** skorla, sürekli izleme borusu kur, bildirim gönder | + `otomasyon-boru-hatti.md` |

Seviyeler kümülatif: 3'teysen 2'nin de 1'in de araçlarını kullanırsın. Emin değilsen bir seviye
aşağı davran — var olmayan aracı kullanmaya çalışmaktan iyidir.

**Seviye 2/3'te statik bantlar ikincil hale gelir.** Gerçek fiyat okuyabiliyorken referans bandına
göre tahmin yürütmek, elindeki daha iyi kanıtı çöpe atmak olur. Bantlar artık sadece **sağlama**
için: okuduğun fiyat banda göre 10 kat sapıyorsa yanlış alanı okumuşsundur.

## Temel kısıt — bunu asla unutma

Seviye 1'de canlı fiyat yok: Google Flights, Skyscanner, Kayak `web_fetch`'e fiyat döndürmez
(JS ile yükleniyor + bot engeli). Bu yüzden **fiyat uydurmak** bu skill'in tek gerçek başarısızlık
modudur. Uydurulmuş bir fiyat, hiç fiyat vermemekten çok daha kötüdür: kullanıcı ona güvenip plan
yapar.

Bu kural Seviye 2 ve 3'te de aynen geçerli — orada okuma **başarısız olduğunda** devreye girer.
Sayfa değişmiş, CAPTCHA çıkmış, fiyat render edilmemiş olabilir. O durumda "okunamadı, link
aşağıda" demek doğru cevaptır; boşluğu makul görünen bir rakamla doldurmak değil.

Her sayı üç etiketten birini taşımak zorunda:

| Etiket | Anlamı | Nereden gelir |
|---|---|---|
| **[KANIT]** | Kaynağı ve tarihi var | Havayolu kampanya sayfası, basın bülteni, fırsat hesabı paylaşımı — `web_fetch` ile alınmış |
| **[OKUNDU]** | Tarayıcıdan canlı okundu | Seviye 2/3. Yanına okuma zamanını yaz: fiyatlar saatler içinde değişir |
| **[BANT]** | Tipik fiyat aralığı, canlı değil | `references/firsat-skorlama.md` referans bantları |
| **[KULLANICI]** | Kullanıcının kendisi söyledi | "Skyscanner'da 4.200 TL gördüm" |

Etiketsiz sayı yazma. "Yaklaşık 3000 TL olur" gibi cümle kurma. Bilmiyorsan bant ver ve
linki ver — kullanıcı 20 saniyede kendi doğrular.

## Hangi mod?

Kullanıcının cümlesinden karar ver, sorma:

- **Destinasyon yoksa** → Mod A (Fırsat Avı). "Perşembe gidiş pazar dönüş, vizesiz nereye
  ucuz var" tipik örnek.
- **Destinasyon veya amaç sabitse** → Mod B (Hedefli Rota). Umre, düğün, konferans, "Tiflis'e
  gideceğim" gibi.
- **Elinde bir fiyat varsa ve "iyi mi?" diye soruyorsa** → Mod C (Fiyat Yargısı). Kısa cevap,
  tek tablo, uzun rapor yazma.

## Varsayılanlar — sormadan uygula

Netleşmemiş her şey için makul varsayım yap, varsayımı çıktının başında tek satırda belirt.
Kullanıcıyı soru yağmuruna tutmak bu skill'in işini yavaşlatır.

- Kalkış: **IST + SAW ikisi birlikte** (Sabiha Gökçen'i atlamak fırsatların yarısını kaçırmak
  demektir). Fiyata SAW ulaşım maliyeti farkını not düş.
- Tarih belirtilmemişse: **önümüzdeki 8 hafta** içindeki tüm uygun gün çiftleri.
- Yolcu: 1 yetişkin, ekonomi.
- Para birimi: TRY göster, karşılaştırma matematiğini EUR üzerinden yap (TL enflasyonu bantları
  bozuyor).
- "Vizesiz" dendiğinde kapıda vize + e-vize de havuza dahil — ama vize ücretini toplam
  maliyete ekle ve ayrı kolonda göster.

Sadece şu iki durumda `ask_user_input` ile sor: (a) bütçe tavanı fırsat tanımını tamamen
değiştirecekse ve hiç ipucu yoksa, (b) yolcu sayısı/kompozisyonu belirsiz ve fiyatı katlıyorsa
(4 kişi + bebek gibi).

---

## Mod A — Fırsat Avı (destinasyon açık)

### A1. Havuzu daralt

`references/vizesiz-destinasyonlar.md` oku. Şu filtreleri sırayla uygula:

1. **Vize durumu** — kullanıcının kısıtına uyanlar (vizesiz / kapıda / e-vize).
2. **Süre mantığı** — gidiş-dönüş uçuş süresi toplamı, seyahatin toplam saatinin %20'sini
   geçmesin. 3 gecelik Perşembe-Pazar için bu **tek yön ≤ 5 saat** demek. Tokyo'yu 3 geceye
   koymak fiyatı ne olursa olsun kötü tavsiyedir; kullanıcı ısrar ederse uyarıyla listele.
3. **Sezon uygunluğu** — Kasım'da Batum, Ağustos'ta Dubai teknik olarak ucuz ama pratikte kötü.
   Tabloda sezon notu var.
4. **Direkt uçuş var mı** — 3 gecelik kaçamakta aktarma, seyahatin yarısını yer. Mod A'da
   aktarmalıları ancak fiyat gerçekten uçuk derecede iyiyse listele.

Bu filtreden 8–15 aday çıkar. Hepsini aramaya kalkma.

### A2. Kanıt topla

**Seviye 2/3'teysen** sıra tersine döner: önce Google Flights **Explore** haritasını aç ve havuzdaki
şehirlerin fiyatını tek ekranda gör, sonra kazananlar için tarih ızgarasıyla en iyi Perşembe–Pazar
çiftini bul. Bu, 15 ayrı arama yerine 2–3 sayfa açmakla aynı kapsamı verir. Ayrıntı:
`references/tarayici-otomasyonu.md` §2. Kampanya taramasını buna ek olarak yine yap — kampanyalar
Explore haritasında görünmez.

**Seviye 1'deysen** `references/arama-kaynaklari.md` oku ve oradaki sıraya göre ilerle. Özet öncelik:

1. **Havayolu kampanya sayfaları** — THY, Pegasus, AJet, Wizz Air, flynas, Air Arabia. Bunlar
   statik HTML, `web_fetch` çalışır. En güvenilir [KANIT] kaynağı burasıdır.
2. **`web_search`** ile güncel fırsat haberleri ve fırsat takip hesaplarının paylaşımları.
   Sorguya mutlaka **ay + yıl** koy ("Pegasus kampanya Ağustos 2026"), yoksa 2023 sonuçları gelir.
3. **Doğrulama** — bir kampanya bulduğunda satış tarihini ve seyahat tarihi penceresini oku.
   Süresi geçmiş kampanyayı fırsat diye sunmak en sık yapılan hata. Bugünün tarihiyle karşılaştır.

Aynı sorguyu farklı kelimelerle tekrarlamak sonucu değiştirmez — sonuç gelmiyorsa açıyı
değiştir (havayolu adı → rota adı → "error fare" → "bilet fiyatı düştü").

### A3. Skorla ve sırala

**Seviye 3'teysen** önce ampirik yolu dene: `scripts/fiyat_deposu.py skor` kendi gözlem geçmişine
göre skor üretir ve bir `guven` alanı döndürür. `guven` değeri `zayif` değilse bu skoru kullan,
statik bandı sadece sağlama için tut. Her okuduğun fiyatı da `kaydet` ile depoya yaz — deponun
ısınması buna bağlı. Ayrıntı: `references/otomasyon-boru-hatti.md` §2.

**Seviye 1/2'de** veya depo soğukken: `references/firsat-skorlama.md` içindeki skorlamayı uygula.
Kısaca: fiyat ÷ referans bant tabanı.

| Skor | Etiket | Anlam |
|---|---|---|
| < 0,40 | 🔴 **Hata fiyatı olabilir** | Hemen al, ama iptal riski var — protokole bak |
| 0,40–0,60 | 🟢 **Gerçek fırsat** | Kullanıcının aradığı şey bu |
| 0,60–0,85 | 🟡 **İyi** | Alınır ama acele gerekmez |
| > 0,85 | ⚪ **Normal** | Listelemeye değmez, listeden çıkar |

Kullanıcı "aşırı indirimli" dediyse **sadece 🔴 ve 🟢 göster**. 🟡'ları "ayrıca" diye tek satırda
geç. Listeyi doldurmak için normal fiyatı fırsat gibi sunmak, skill'in tüm değerini yok eder.

### A4. Çıktı formatı

Kısa giriş cümlesi + tek tablo + linkler. Rapor yazma.

```
Varsayımlar: IST+SAW kalkış, 1 yetişkin, [tarih aralığı], vizesiz+kapıda vize dahil.

| Şehir | Tarih | Fiyat | Skor | Uçuş | Vize | Kaynak |
|---|---|---|---|---|---|---|
| Üsküp (SKP) | 14–17 Ağu | 1.850 TL [KANIT] | 🟢 0,52 | 1s40d direkt | Vizesiz | Pegasus kampanya, 8 Ağu |
| Tiflis (TBS) | 21–24 Ağu | ~2.400 TL [BANT] | 🟡 0,71 | 2s10d direkt | Vizesiz | doğrulanmalı ↓ |

**Doğrulama linkleri** (tıkla, fiyatı 20 saniyede gör)
- Üsküp: <google flights linki>
- Her yer birden: <skyscanner everywhere linki>

**Not:** Perşembe akşam 18:00–21:00 kalkışlar iş trafiği yüzünden en pahalı dilim. Aynı rotada
Perşembe 23:xx veya Cuma 06:xx kalkış sık sık %30–40 daha ucuz çıkıyor.
```

Tablo satırı 8'i geçmesin. Uzun liste seçim yapmayı zorlaştırır, kullanıcı hiçbirini almaz.

### A5. Kuralı esnetme önerisi

Kullanıcının Perşembe-Pazar kuralı fiyatı ciddi şekilde yukarı çekiyorsa, en sonda **tek
paragraf** halinde alternatif sun: "Çarşamba gece – Pazartesi sabah yapsan aynı rotada bant
tabanı %35 düşüyor." Zorlamadan, tek seferde söyle.

---

## Mod B — Hedefli Rota

Destinasyon veya amaç sabit. Sıra:

1. **Havaalanı seçimi.** Şehir ≠ havaalanı. Umre için Cidde/Medine kararı, Londra için
   LHR/LGW/STN, Milano için MXP/BGY. Yanlış havaalanı, kazanılan parayı transferde geri verir.
2. **Rota kalıbı.** Gidiş-dönüş mü, açık çene (open-jaw) mı, iki ayrı tek yön mü? Açık çene çoğu
   zaman hem daha mantıklı hem daha ucuz — özellikle Umre'de.
3. **Aktarmalı/aktarmasız kararı.** Bunu fiyat farkına göre değil, **kullanıcının durumuna** göre
   ver. Karar tablosu:

| Durum | Tercih | Neden |
|---|---|---|
| Yaşlı/çocuklu/hasta yolcu | Aktarmasız, fiyat farkı %40'a kadar tolere edilir | Aktarma yorgunluğu paradan pahalı |
| Tek başına, esnek, bütçe kritik | Aktarmalı sorun değil, ≥3s bağlantı payı bırak | En büyük tasarruf burada |
| Kritik varış saati (nikah, uçuş bağlantısı) | Aktarmasız, ya da aynı bilette tek PNR aktarma | Ayrı biletlerde gecikme senin sorunun |
| Fazla/ağır bagaj | Bagaj dahil taşıyıcı, aktarma sayısı az | Her aktarmada bagaj kayıp riski |
| Umre/hac | `references/umre-rehberi.md` — ihram zamanlaması ayrı bir kısıt | Aşağıda |

4. **Gerçek maliyet hesabı.** Bilet fiyatını asla tek başına karşılaştırma. Şunları ekle:
   bagaj ücreti, koltuk, havaalanı ulaşımı (IST vs SAW farkı), gece konaklaması gerektiren
   aktarma, vize ücreti. `references/firsat-skorlama.md` içinde hesap şablonu var.
5. **Tarih esnekliği analizi.** Kullanıcı "başka tarihte çok avantajlı var mı?" diye sorarsa —
   ki genelde sorar — sabit tarihin etrafında ±3 gün, ±2 hafta ve **sezon dışı** olmak üzere üç
   halka tara. Sezon dışı halkası en büyük kazancı verir ama uygulanabilirliği en düşüktür;
   ikisini birbirinden ayır: "±3 günde %15, Kasım'a alırsan %55."

### Umre / Hac

Kullanıcı umre, hac, Cidde, Medine, Mekke, Nusuk, mikat, ihram kelimelerinden birini
kullanırsa **mutlaka** `references/umre-rehberi.md` oku. Bu rotanın normal turistik uçuştan
farklı beş kısıtı var (ihram/mikat zamanlaması, Ramazan ve hac dönemi fiyat patlaması, açık
çene mantığı, zemzem/bagaj, acente paketiyle kıyas) ve bunları bilmeden verilen tavsiye
yüzeysel kalır.

---

## Mod C — Fiyat Yargısı

Kullanıcı elindeki fiyatın iyi olup olmadığını soruyor. Uzun cevap verme.

1. Rotanın referans bandını bul (`firsat-skorlama.md`).
2. Skoru hesapla, etiketi ver.
3. Tek cümle gerekçe.
4. Daha iyisi mümkünse tek alternatif ver, değilse "bu iyi, al" de.

Örnek: "IST–DXB gidiş-dönüş 5.900 TL → skor 0,62, 🟡 iyi. Ağustos Dubai için makul; ama Kasım'a
kaydırabilirsen aynı rota 3.500–4.000 bandına iniyor. Tarih sabitse alabilirsin."

---

## Genel davranış kuralları

**Yatırım/hukuk tavsiyesi değil, ama para tavsiyesi.** Bilet alma kararı kullanıcının.
Eksik doğrulanmış bir fırsatı "kesin" diye sunma.

**Kampanya tarihini kontrol et.** Her kampanyanın iki tarihi var: satış penceresi ve seyahat
penceresi. İkisini de yaz. Süresi geçmişse listeleme.

**Hata fiyatı bulduysan protokolü uygula** (`firsat-skorlama.md`): bileti al, ama otel/tur gibi
iptal edilemez şeyleri 72 saat beklemeden bağlama, havayoluyla iletişime geçme, sosyal medyada
yayma. Türkiye'de uçak bileti mesafeli satışta cayma hakkı kapsamı dışında — 24 saat iade hakkı
otomatik değil, tarifeye bakılır.

**Vizesiz listesi değişkendir.** `vizesiz-destinasyonlar.md` bir *arama kısa listesi*, hukuki
kaynak değil. Kullanıcı bilet almaya yaklaştığında Dışişleri Bakanlığı sayfasından veya
havayolunun vize aracından doğrulamasını söyle. Pasaport geçerlilik süresi (çoğu ülke 6 ay
ister) ayrı bir tuzak, hatırlat.

**Son tıklama kullanıcının.** Tarayıcı sürebiliyor olsan bile bilet satın alma adımını kendi başına
tamamlama. Fiyatı bul, doğru uçuşu seç, ödeme ekranına kadar getir — kararı ve ödemeyi kullanıcı
verir. Para harcayan adımı devralmak bu skill'in işi değil.

**Otomasyon isteniyorsa** `references/otomasyon-boru-hatti.md` oku. Toplu kazıyıcı kurmaya
girişmeden önce oradaki §5 (API yolu) ve hacim önerisine bak: sürdürülebilir izleme günde ~15
istektir, yüzlerce değil.

**Konum.** Kullanıcı İstanbul'da; kalkış varsayımı bu yüzden IST/SAW. Farklı şehir söylerse
ona göre çalış, tablodaki uçuş süreleri İstanbul referanslı olduğu için yeniden hesapla.

## Referans dosyaları

- `references/vizesiz-destinasyonlar.md` — Türk pasaportuna vizesiz/kapıda/e-vize destinasyon
  havuzu; havaalanı kodu, direkt taşıyıcılar, uçuş süresi, referans fiyat bandı, sezon notu.
  **Mod A'da her zaman oku.**
- `references/firsat-skorlama.md` — fiyat bantları, skor matematiği, gerçek maliyet şablonu,
  hata fiyatı protokolü, Perşembe-Pazar saat mekaniği. **Her modda oku.**
- `references/arama-kaynaklari.md` — hangi kaynak `web_fetch` ile çalışıyor hangisi çalışmıyor,
  hazır link şablonları (Google Flights, Skyscanner everywhere, Azair, havayolu kampanya
  sayfaları), arama sorgusu kalıpları. **Kanıt toplarken oku.**
- `references/umre-rehberi.md` — Umre/hac rota mantığı, sezon takvimi, ihram/mikat kısıtı,
  bagaj, acente kıyası. **Umre/hac geçtiğinde oku.**
- `references/tarayici-otomasyonu.md` — Google Flights'ı tarayıcıyla okuma yöntemi, tarih ızgarası
  ve Explore taktiği, kırılgan seçici tuzağı, bloklanma hijyeni, API alternatifleri.
  **Seviye 2/3'te oku.**
- `references/otomasyon-boru-hatti.md` — sürekli izleme mimarisi, cron, sessiz bozulma
  korumaları, izleme listesi kurma, bildirim. **Sadece otomasyon isteniyorsa oku.**
- `scripts/fiyat_deposu.py` — SQLite gözlem deposu ve ampirik skorlama (`kaydet`, `skor`, `ozet`,
  `firsatlar`). Bağımlılık gerektirmez. **Seviye 3'te kullan.**
