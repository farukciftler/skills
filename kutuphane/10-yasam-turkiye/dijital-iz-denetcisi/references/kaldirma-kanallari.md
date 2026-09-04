# Kaldırma Kanalları

Her bulgu bir kanala eşlenir. Kanal yoksa bunu açıkça yaz — sahte bir yol göstermek, hiç yol göstermemekten kötüdür.

## Temel ilke: sıralamayı bozma

```
KAYNAK → (hukuki dayanak) → ARAMA MOTORU → TÜREVLER → İZLEME
```

Arama motoru kaldırma talepleri, içerik kaynak sayfada hâlâ canlıyken **büyük çoğunlukla reddedilir.** Bu, tüm kanalın en sık yapılan hatası. Kaynağı önce indir.

---

## 1. Arama motorları

### Google

Dört ayrı araç var ve yanlış aracı seçmek doğrudan ret demek:

| Araç | Ne için | Ne için DEĞİL |
|---|---|---|
| **Results about you** (goo.gle/resultsaboutyou) | Telefon, e-posta, ev adresi, devlet kimlik numaraları (pasaport/ehliyet/SSN — Şubat 2026'dan beri) için izleme + tek panelden kaldırma talebi | Veri simsarı kaldırma servisi değil; kaynak sayfaya dokunmaz |
| **Kişisel içerik kaldırma formu** | Hassas kişisel bilgi, finansal veri, kimlik bilgisi, doxxing, rızasız mahrem görsel | Sadece "hoşuma gitmeyen" içerik |
| **Yasal kaldırma talebi** | Telif, marka, mahkeme kararı, ülke mevzuatı gereği (KVKK/GDPR indeksten çıkarma dahil) | Politika ihlali olmayan içerik |
| **Refresh Outdated Content** (Search Console) | Sayfa **silinmiş veya değişmiş** ama sonuç hâlâ görünüyor | İçerik sayfada duruyorsa çalışmaz — otomatik ret |

**Results about you işleyişi:** Kullanıcı izlenecek bilgileri girer, Google düzenli tarar, eşleşme bulunca bildirim gönderir, panelden "kaldırmayı talep et" denir. Talep durumu aynı panelden izlenir. Ayrıca arama sonucunun yanındaki üç noktadan doğrudan kaldırma talebi gönderilebiliyor (2026 tasarım güncellemesiyle daha az tıkla).

**Ret sebepleri:**
- İçerik kaynak sayfada hâlâ canlı ve değişmemiş → en yaygın sebep
- Sayfa devlet, eğitim veya haber alan adında
- İçerik "geniş kamu yararı" taşıyor (mahkeme kaydı, resmî kayıt)
- Yanlış araç kullanılmış

**Kritik sınır:** Google'dan kaldırma, veriyi internetten silmez. Sadece Google Search'te o sorguyla bulunmasını engeller. Bing, Yandex ve kaynak sitenin kendisi etkilenmez.

### Diğer motorlar

- **Bing** — kendi kaldırma formu var, izleme paneli yok. DuckDuckGo ve Ecosia Bing indeksini kullandığı için Bing'den kaldırma bu ikisini de kapsar.
- **Yandex** — ayrı başvuru gerekir; Türkiye ve Rusça içerikte Google'ın kaçırdığını tuttuğu için atlanmamalı.
- **Brave Search** — kendi indeksi var, ayrı başvuru.

---

## 2. Veri simsarları

**Genel akış:** Sitede kendi kaydını bul → profil URL'sini kopyala → opt-out sayfasına git → URL + e-posta gir → e-posta veya telefonla doğrula.

**Tipik süreler:** 24-72 saat (kolay olanlar), 1-3 iş günü (orta), 30 güne kadar (Acxiom gibi pazarlama agregatörleri).

**Konsolidasyondan yararlan:**
- PeopleConnect ailesi (Intelius, TruthFinder, Instant Checkmate) — tek akış
- BeenVerified — kardeş markaları da bastırıyor
- Whitepages — alt siteler ana suppression üzerinden

**Zorluk kalıpları ve karşı hamleler:**

| Engel | Karşı hamle |
|---|---|
| Opt-out sayfası gizlenmiş (dark pattern), site içi aramada çıkmıyor | `site:broker.com opt out` veya `site:broker.com removal` ile Google'dan gir |
| Kimlik doğrulama için ehliyet/kimlik fotoğrafı isteniyor | Fotoğrafı ve numarayı **karartarak** gönder; yalnızca ad ve doğum yılı görünsün |
| Telefonla otomatik doğrulama araması gerekiyor (Whitepages tipi) | Sırayı bozma, tek oturumda hallet — kod süreli |
| Opt-out ancak hesap açarak yapılabiliyor | Bu tek başına ret sebebi değil; tek kullanımlık e-posta ile aç |

**Yeniden ortaya çıkma — bunu baştan söyle.** Whitepages ve Spokeo gibi büyük siteler kaynak kamu kayıtlarını yeniden çektiğinde profili tipik olarak **3-4 ayda bir** yeniden yayımlıyor. Opt-out kalıcı silme değil, bastırmadır. Bu yüzden Faz 3 (izleme) opsiyonel değil.

**Çoklu kayıt:** Aynı kişi kızlık soyadı, eski şehir ve sabit hat üzerinden 3-4 ayrı kayda bölünmüş olabilir. Tek kaydı kaldırmak yeterli değil; her varyantı ayrı ara.

**Kaliforniya sakinleri için kısayol:** DROP platformu (bkz. `diger-yargi-yetkileri.md`) tek talep ile 500+ kayıtlı broker'a ulaşıyor. Uygunsa manuel turdan önce bunu çalıştır.

---

## 3. Sosyal medya ve platformlar

**Öncelik sırası:** Önce görünürlük ayarı (anında etki), sonra içerik silme (kalıcı), en son hesap kapatma (geri dönüşsüz).

- **Hesabı silmeden önce indir.** Her büyük platform veri dışa aktarma sunuyor. Silme geri alınamaz; kullanıcı iki yıl sonra o fotoğrafı isteyebilir.
- **Terk edilmiş hesaplar:** Erişim varsa içeriği sil → hesabı sil. Erişim yoksa hesap kurtarma; o da olmazsa platformun "sahibi olduğum hesaba erişemiyorum" akışı.
- **Vefat etmiş yakın hesapları:** Ayrı prosedür (Facebook memorialization, Google Inactive Account Manager), ölüm belgesi isteniyor.
- **Arama motoru indekslemesi:** LinkedIn, X ve Instagram'da profilin arama motorlarınca indekslenmesini kapatan ayrı bir ayar var. Profili tamamen silmeden görünürlüğü ciddi biçimde düşürür — düşük maliyetli, yüksek etkili.
- **Etiketlenen içerik:** Kendi hesabını temizlemek, başkalarının paylaşımlarındaki etiketleri temizlemez. Etiket kaldırma ayrı iş.
- **Eski profil fotoğrafları:** Çoğu platformda geçmiş profil fotoğrafları kalıcı olarak herkese açık kalır; ayrıca silinmeleri gerekir.

### Rehber uygulamaları (Türkiye'de kritik)

**Getcontact:** İki ayrı işlem, ikisi de gerekli — sadece hesap silmek numarayı havuzdan çıkarmaz.
1. Uygulama içinden hesabı sil (Ayarlar → Gizlilik/Hakkında → Hesabı Sil)
2. `getcontact.com/tr/unlist` üzerinden numarayı unlist et (numara girilir, SMS doğrulaması yapılır)
Etki tipik olarak 24 saat içinde.

**Truecaller:** Önce uygulamadan hesap devre dışı bırakılır, sonra web üzerindeki unlist formundan numara kaldırılır. Yine ~24 saat.

**Önemli uyarı:** Bu uygulamalar veriyi kullanıcıların rehberlerinden topluyor. Numara unlist edildikten sonra rehberinde numaranız kayıtlı biri uygulamayı yeniden yüklerse numara havuza geri girebilir. Bu, tekrarlanması gereken bir işlem — Faz 3'e yaz.

---

## 4. Görsel ve biyometrik

### PimEyes

Form: `pimeyes.com/en/opt-out-form`. Süreç: net, önden çekilmiş, güncel bir referans fotoğraf + karartılmış kimlik (yüz görünür kalmalı) + hukuki dayanak.

**Mekanizma:** İnsan incelemesi değil — PimEyes referans fotoğrafını kendi yüz tanıma modelinden geçirip aday eşleşmelerle karşılaştırıyor. Benzerlik skoru eşiği geçmezse jenerik ret geliyor. Yani **fotoğraf kalitesi doğrudan başarı oranını belirliyor.**

**Ret sebepleri ve düzeltmeleri:**
| Sebep | Düzeltme |
|---|---|
| Yüz kısmen kapalı (gözlük, şapka, yan açı, düşük çözünürlük) | Tek, net, önden, iyi ışıklı, güncel fotoğraf |
| Kimlikteki yüz görünmüyor | Veri alanlarını karart, fotoğrafı bırak |
| Hukuki dayanak alanı boş veya belirsiz | "GDPR m.17 (silme hakkı)" veya "KVKK m.7 ve m.11" gibi somut madde yaz. "Bunun kaldırılmasını istiyorum" işleme alınmıyor |

**Süre:** Otomatik onay e-postası dakikalar içinde; asıl sonuç 3-7 iş günü, yoğun dönemde 2-6 haftaya kadar.

**Kapsam:** PimEyes birden fazla farklı fotoğrafla (farklı açı, dönem, gözlüklü/gözlüksüz) tekrarlanan başvuru yapılmasını kendisi öneriyor — tek başvuru tüm indekslenmiş görselleri yakalamayabiliyor. Ayrıca tekil bir arama sonucu için "Exclude from public results" akışı da var.

**Sınır:** Opt-out fotoğrafı silmez; kaynak site yayımlamaya devam eder. Yalnızca yüzle arandığında bulunmasını engeller. Blok listesi diğer servislerle paylaşılmaz.

### FaceCheck.ID ve Clearview AI

Ayrı başvurular. FaceCheck.ID'nin kendi kaldırma talebi akışı var, talep sonrası görseller sonraki aramalardan hemen gizleniyor. Clearview tüketiciye kapalı ama bazı yargı yetkilerinde (AB, bazı ABD eyaletleri) veri erişim/silme talebi hakkı işliyor.

### Ters görsel arama

Google Lens/TinEye sonuçları kendi başına bir veritabanı değil — kaynak sayfa indiğinde sonuç da düşer. Bu yüzden bu katmanda hedef kaynak sayfadır.

---

## 5. Arşiv ve önbellek

**Wayback Machine:** Kaldırma isteğe bağlı ve garantisiz; `info@archive.org` adresine gerekçeli talep gönderilir. Kişisel veri ve güvenlik gerekçeleri diğerlerine göre daha çok kabul görüyor. Alan adının sahibiyseniz `robots.txt` ile geçmiş arşivin gizlenmesi bazı durumlarda hâlâ çalışıyor ama Archive.org bu politikayı gevşetti — güvenilir bir yol değil.

**archive.today / archive.ph:** Kaldırma politikası çok daha katı, çoğu talep yanıtsız kalıyor. Raporda gerçekçi ol.

**Google önbelleği:** Kaynak indikten sonra Refresh Outdated Content aracıyla hızlandırılır.

**Common Crawl:** Doğrudan kaldırma mekanizması yok. Yapılabilecek olan, kaynak sitede `robots.txt` ile `CCBot`'u engellemek ve gelecek crawl'larda dışarıda kalmak. Halihazırda çekilmiş arşivler kalır.

---

## 6. LLM / AI yüzeyleri

Üç boru hattı, üç farklı müdahale:

**A. Gelecek eğitimden çıkma (ayar):**
- ChatGPT: Ayarlar → Data Controls → "Improve the model for everyone" kapat. Not: oturum açmadan kullanımda bu ayar geçerli değil, veri yine toplanıyor. Geçici sohbetler zaten eğitime girmiyor. API kullanımı varsayılan olarak eğitime dahil değil.
- Gemini: Google hesabı → "Gemini Apps Activity" (yeni adıyla "Keep Activity") kapat + geçmiş etkinliği sil. Kapatıldıktan sonra da güvenlik amaçlı ~72 saat saklama var.
- Claude: Ayarlardan; Incognito sohbetler ayar ne olursa olsun eğitime girmiyor.
- Kurumsal katmanlar (Team/Enterprise/API) genelde varsayılan olarak eğitim dışı.

**B. Modelin cevaplarından kişisel bilgi çıkarma (talep):**
OpenAI'nin gizlilik portalı (`privacy.openai.com`) üzerinden, eğitimden çıkma talebinden **ayrı** bir talep türü olarak "cevaplarda görünen kişisel bilgilerin kaldırılması" istenebiliyor. Bu ikisi karıştırılıyor: hesap verisi silme talebi otomatik ve hızlı işliyor, cevap içeriğinden kişisel bilgi çıkarma talebi ayrı ve daha yavaş.

**C. Web erişimi katmanı (kaynak temizliği):**
Model canlı web'den çekiyorsa hiçbir eğitim ayarı işe yaramaz. Tek çözüm kaynak sayfayı indirmek. Bu, LLM katmanının aslında **1-5 arası kanalların bir türevi** olduğu anlamına gelir — ve raporda böyle sunulmalı.

**AB'de ek kaldıraç:** GDPR m.21 uyarınca eğitim amaçlı işlemeye **itiraz** edilebiliyor; bu standart opt-out'tan daha güçlü, şirket ya uymak ya da meşru menfaatin üstünlüğünü ispat etmek zorunda.

**Dürüst olunacak sınır:** Bir veri eğitim turuna girdiyse geriye dönük çıkarılamaz. Bunu vaat etme.

---

## 7. Kaynak site / webmaster

Çoğu durumda ilk ve en etkili adım, çoğu denetimde atlanan adım.

**Sıra:**
1. Sitede yayımlanmış iletişim/gizlilik e-postası
2. Alan adı WHOIS kaydındaki abuse adresi
3. Hosting sağlayıcısının abuse kanalı
4. CDN sağlayıcısı (Cloudflare vb.) — kaynağı gizliyorsa

**Metin:** Kısa, kibar, somut. URL, hangi kişisel veri alanı, hangi hukuki dayanak, hangi süre içinde yanıt beklendiği. Şablon için `assets/dilekce-sablonlari.md`.

**Yanıt gelmezse:** KVKK/GDPR resmî başvuru rotasına geç. Türkiye için `turkiye-hukuk.md`, AB/ABD için `diger-yargi-yetkileri.md`.

---

## 8. İzleme rejimi (Faz 3)

Kaldırma bir kerelik iş değil. Kullanıcıya bir ritim ver:

| Sıklık | Ne |
|---|---|
| Sürekli | Google Results about you izlemesi açık; HIBP ihlal bildirimi aboneliği |
| Aylık | Ad-soyad araması, gizli pencerede, ilk 3 sayfa |
| 3 ayda bir | Öncelikli broker listesi yeniden kontrol (yeniden yayımlama döngüsü tam bu aralıkta) |
| 6 ayda bir | Kullanıcı adı yayılımı taraması, yüz arama motoru kontrolü |
| Olay bazlı | İş değişikliği, kamusal bir role geçiş, ihlal bildirimi sonrası tam tekrar tarama |

**Kaynağı kesme (önleme):** Yeni maruziyet üretmeyi durdurmak, mevcut olanı temizlemekten daha kalıcı. Kayıt formlarında takma ad ve yönlendirmeli e-posta (Apple Hide My Email, e-posta alias'ları), telefon için ikincil numara, rehber uygulamalarına rehber erişimi vermeme, sosyal medyada konum etiketi kapalı, yeni hesaplarda arama motoru indekslemesi kapalı.
