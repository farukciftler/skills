# Ölçüm, CRM ve KVKK

Reklam tavsiyelerinin tamamı bu dosyadaki altyapının üstünde duruyor.
Ölçüm yoksa geri kalan her şey tahmindir — ve tahminle harcanan bütçe,
harcanmamış sayılmaz, kaybedilmiş sayılır.

## İçindekiler

1. Ölçüm katmanları
2. Dönüşüm eylemleri ve değerleri
3. Google tarafı: Enhanced Conversions ve offline aktarım (2026 değişikliği)
4. Meta tarafı: Piksel, CAPI, EMQ
5. UTM ve kaynak disiplini
6. Lead skorlama
7. KVKK ve rıza altyapısı
8. Raporlama: haftalık ve aylık
9. Atıf (attribution) tuzakları

---

## 1. Ölçüm katmanları

Beş katman var; birinden birinde kopukluk varsa üstündeki her şey yanlış okur.

| Katman | Ne yapar | Araç |
|---|---|---|
| 1. Etiketleme | Site olaylarını yakalar | GTM (Google Tag Manager) |
| 2. Analitik | Davranışı ölçer | GA4 |
| 3. Reklam dönüşümü | Platforma sinyal gönderir | Google Ads dönüşümleri, Meta Piksel + CAPI |
| 4. CRM | Lead'in gerçek hikâyesini tutar | `[DOĞRULA: hangi CRM kullanılacak]` |
| 5. Geri besleme | CRM sonucunu platforma geri gönderir | Offline dönüşüm aktarımı / CAPI |

**Katman 5 emlakta olmazsa olmazdır ve en çok atlanandır.** Satış döngüsü
haftalar-aylar sürdüğü için platform, kendi gördüğü son olayı (form gönderimi)
başarı sayar. CRM'den "bu lead randevuya döndü / bu lead çöp" bilgisi geri
gitmezse, akıllı teklif sistemi **çöp lead üretmekte uzmanlaşır.**

---

## 2. Dönüşüm eylemleri ve değerleri

Hepsini aynı ağırlıkta saymak, sistemin en kolay olanı çoğaltmasına yol açar.
Değerler göreli önem sırasını anlatır; para birimi olması şart değil ama
tutarlı olmalı.

| Dönüşüm | Öneri değer [MUHAKEME] | Not |
|---|---|---|
| Randevu talebi (tarih seçilmiş) | 100 | Ana dönüşüm |
| İletişim formu gönderimi | 60 | |
| WhatsApp sohbeti başlatma | 50 | Sohbet başlaması, sohbetin sürmesi değil |
| Telefon araması (60 sn+) | 70 | 60 sn altı sayılmaz |
| Katalog / kat planı indirme | 25 | İkincil |
| Sanal tur 30 sn+ izleme | 15 | İkincil, niyet sinyali |
| Sayfa görüntüleme, kaydırma | 0 | **Dönüşüm sayma.** En sık hata |

**Yalnızca birincil dönüşümler teklif optimizasyonuna verilir**; ikincil
olanlar gözlem ve remarketing için tutulur. Hepsini optimizasyona açmak,
sisteme "en ucuzunu getir" demektir — o da katalog indirmedir.

Nitelikli lead ölçülmeye başladığında **asıl optimizasyon hedefi o olur.**

---

## 3. Google tarafı: Enhanced Conversions ve offline aktarım

**2026'nın iki önemli değişikliği — kurulum yaparken kontrol et:**

- **15 Haziran 2026'dan itibaren** offline dönüşüm aktarımı ve lead için
  gelişmiş dönüşüm yüklemeleri **Data Manager API'ye taşındı** ve Google Ads
  API üzerinden bloklandı. Eski entegrasyonu olan ajans/yazılım varsa bu
  tarihte kırılmıştır — **kontrol et.** [KIYAS: Google Ads duyurusu]
- **Nisan 2026'dan itibaren** Google Ads; site etiketi, Data Manager ve API
  bağlantılarından gelen kullanıcı verisini eşzamanlı kabul ediyor; artık
  yöntemler arasında seçim yapmak gerekmiyor.

**Lead için gelişmiş dönüşümler (Enhanced conversions for leads):** Form
gönderiminde toplanan hashlenmiş e-posta/telefonu kullanarak, GCLID izi
koptuğunda bile eşleştirme yapar. Google, standart offline aktarıma göre
medyan **%10 dönüşüm artışı** bildiriyor [KIYAS: Google kaynaklı].

**Emlak için akış:**
```
Form gönderimi → hashlenmiş e-posta/telefon + GCLID CRM'e yazılır
CRM'de lead durumu güncellenir (nitelikli / randevu / satış)
Durum değişimi Data Manager üzerinden Google Ads'e geri gönderilir
Akıllı teklif artık "form dolduran"a değil "randevuya gelen"e optimize eder
```

Bu döngü kurulmadan Google Ads'te emlak reklamı, gerçek hedefe değil
vekil hedefe optimize edilir.

---

## 4. Meta tarafı: Piksel, CAPI, EMQ

- **Piksel + Conversions API birlikte.** Tarayıcı tarafı çerez ve izleme
  kısıtlarıyla eriyor; sunucu tarafı bunu telafi ediyor. İkisi birden.
- **Tekilleştirme (deduplication):** Aynı olay iki kanaldan geldiğinde
  `event_id` ile tekilleştirilmeli. Kurulmazsa dönüşüm şişer, teklif motoru
  yanlış öğrenir, raporlar gerçekdışı görünür.
- **Event Match Quality (EMQ) 7 üstü** hedef. Altındaysa eşleşme parametresi
  ekle: hashlenmiş e-posta, telefon, ad-soyad, şehir, IP, kullanıcı aracısı.
- **Offline Conversions / CAPI ile CRM geri beslemesi**: randevu ve satış
  olayları Meta'ya geri gönderilmeli — Google tarafındaki mantığın aynısı.

---

## 5. UTM ve kaynak disiplini

Tek bir şema, istisnasız. Şema bozulduğunda raporlar sessizce yanlışlaşır
ve bu genelde aylar sonra fark edilir.

```
utm_source   = google | meta | tiktok | sahibinden | emlakjet | eposta
utm_medium   = cpc | paidsocial | display | organic | referral | email
utm_campaign = moonstone_rezidans_2026q4
utm_content  = kreatif_adi_veya_id
utm_term     = anahtar_kelime (yalnız arama)
```

Kurallar: hepsi küçük harf, Türkçe karakter yok, boşluk yerine alt çizgi.
Google Ads'te otomatik etiketleme (auto-tagging) açık kalsın — GCLID
gelişmiş dönüşümler için gerekli. Meta'da URL parametreleri kampanya
düzeyinde şablonlansın, reklam reklam elle yazılmasın.

**WhatsApp ve telefon trafiği UTM taşımaz** — kaynağı kaybolur. Çözüm:
kampanya bazında ayrı WhatsApp ön-doldurulmuş mesaj metni ("Moonstone
Instagram ilanınız için yazıyorum") ya da ayrı numara. Kaba ama işe yarar.

---

## 6. Lead skorlama

Reklamın optimize edeceği hedef budur. Basit ve satış ekibinin gerçekten
dolduracağı kadar kısa tut — doldurulmayan alan, olmayan alandır.

| Kriter | Puan |
|---|---|
| Ulaşılabildi (telefon açıldı / mesaj yanıtlandı) | +2 |
| Bütçe projeye uygun | +3 |
| Aradığı daire tipi stokta var | +2 |
| 6 ay içinde alma niyeti | +2 |
| Randevu kabul etti | +3 |
| Yanlış/eksik numara | −5 |
| Kiralık arıyor, ticari alan arıyor (kampanya uyumsuz) | −3 |

**Nitelikli lead eşiği: 7+ puan** [MUHAKEME — ilk 60 gün verisiyle kalibre
edilecek başlangıç değeri]. Bu etiket CRM'den platformlara geri gönderilen
sinyal olur.

**Kritik operasyon kuralı:** Lead'e ilk dönüş süresi, reklam bütçesinden
daha çok satış belirler. 5 dakika ile 1 saat arasındaki fark, hiçbir
kampanya optimizasyonuyla kapatılamaz. Ölç ve raporla: **ortalama ilk dönüş
süresi**, haftalık rapordaki ilk satırlardan biri olmalı.

---

## 7. KVKK ve rıza altyapısı

**Form açmadan önce hazır olması gerekenler:**
1. Aydınlatma metni (veri sorumlusu, işleme amacı, saklama süresi, haklar)
2. Açık rıza kutusu — **ön işaretli olamaz**, ticari elektronik ileti için
   ayrı rıza gerekir
3. Çerez politikası ve çerez banner'ı
4. VERBİS kaydı gerekliliği kontrolü `[DOĞRULA: Ayhanlar VERBİS kaydı]`
5. İYS (İleti Yönetim Sistemi) kaydı — SMS/e-posta gönderilecekse zorunlu

**Consent Mode v2:** KVKK, Consent Mode'u doğrudan zorunlu kılmıyor; ancak
çerez rızası olmadan ölçüm ciddi biçimde eriyor ve Consent Mode reddedilen
rıza durumunda modellenmiş veri sağlıyor. Yani **uyum için değil, ölçüm
sürekliliği için** kurulur. AB'den trafik alınacaksa GDPR tarafında zaten
gerekli hale gelir.

**Pratik kurulum:** GTM üzerinden rıza banner'ı → Consent Mode v2 sinyalleri
→ GA4 ve Google Ads etiketleri rızaya göre davranır. Türkiye ve AB
ziyaretçileri için farklı rıza politikası uygulanabilmeli.

**Müşteri listesi yüklemesi (Customer Match / Meta müşteri listesi) yalnızca
açık rıza varsa yapılır.** Rızasız liste yüklemek hem KVKK ihlali hem
platform politikası ihlalidir. Bu konuda esneme yok.

---

## 8. Raporlama

**Haftalık (operasyon — kısa, tek ekran):**
| Metrik | Neden |
|---|---|
| Harcama, gösterim, tık | Temel |
| Lead sayısı ve CPL | Kanal kırılımıyla |
| **Nitelikli lead ve maliyeti** | Asıl karar metriği |
| **Ortalama ilk dönüş süresi** | Satışın gizli kaldıracı |
| En iyi 3 / en kötü 3 kreatif (hook rate) | Kreatif hattını besler |
| Bu hafta alınan aksiyonlar | Karar izi |

**Aylık (yönetim):**
- Kanal bazında lead → nitelikli → randevu → satış hunisi, tam sayılarla
- Kohort görünümü: "Temmuz lead'lerinden bugüne kaç satış" — emlakta ay
  içi ROAS anlamsızdır, kohort anlamlıdır
- Kreatif kazanan/kaybeden özeti ve öğrenilenler
- Gelecek ay bütçe önerisi ve **gerekçesi**
- Kapanmamış bilinmeyenler listesi (fiyat, teslim tarihi vb.)

---

## 9. Atıf (attribution) tuzakları

1. **Platformların topladığı dönüşüm, gerçeğin üstündedir.** Google ve Meta
   aynı lead'i ikisi de kendine yazar. Toplama güvenme; **CRM'deki tekil lead
   sayısı tek gerçek kaynaktır.**
2. **Son tık atfı Meta'yı cezalandırır.** Meta talebi yaratır, kullanıcı sonra
   markayı Google'da arar, satış Google'a yazılır. Marka araması hacmindeki
   artış, Meta'nın gizli katkısıdır — bunu ayrı izle.
3. **Emlakta atıf penceresi kısa kalır.** Varsayılan pencereler haftalar süren
   karar süreçlerini kaçırır. Pencereyi uzat ve raporda hangi pencerede
   bakıldığını yaz.
4. **Artımsallık (incrementality) testi**, atıf tartışmasının tek gerçek
   cevabıdır: bir kanalı iki hafta kapat, toplam lead ne oldu. Pahalı ve
   rahatsız edici ama tek dürüst yöntem. 300.000 TL üstü bütçelerde yılda
   bir kez yapılmaya değer.
