# Kampanya Planı — Faz, Ritim ve Karar Disiplini

Bu dosya, tek tek kampanyaları bir **süreç** haline getirir. Emlakta reklam
tek bir lansmanla bitmez; proje satılana kadar süren, stok azaldıkça mesajı
değişen bir akıştır.

## İçindekiler

1. Dört faz
2. Faz 0 — Temel (reklamdan önce)
3. Faz 1 — Sinyal toplama
4. Faz 2 — Ölçekleme
5. Faz 3 — Verim ve stok yönetimi
6. Haftalık ritim
7. Test kuyruğu
8. Karar eşikleri
9. Kriz senaryoları
10. Ajans ve iş bölümü

---

## 1. Dört faz

| Faz | Amaç | Ana metrik | Tipik süre |
|---|---|---|---|
| **0 — Temel** | Ölçüm ve altyapı | Kurulum tamamlanma | 2-4 hafta |
| **1 — Sinyal** | Hangi mesaj/kreatif/kanal tutuyor | Hook rate, CPL, ilk nitelikli lead oranı | 4-6 hafta |
| **2 — Ölçekleme** | Nitelikli lead hacmini büyütmek | Nitelikli lead maliyeti | 2-4 ay |
| **3 — Verim** | Kalan stoka göre hedefli baskı | Randevu → satış oranı | Proje sonuna kadar |

Faz atlamak mümkün ama bedeli var: Faz 0 olmadan Faz 1'e geçmek, altı hafta
sonra "veriye güvenemiyoruz" demektir.

---

## 2. Faz 0 — Temel (reklamdan önce)

Bugün Moonstone burada. Bu fazın çıktısı reklam değil, **hazırlık**.

| İş | Durum | Not |
|---|---|---|
| Site ve açılış sayfaları | **Tamam** | proje / daire-planlari / sosyal-alanlar / ticari-alanlar / lokasyon / iletisim |
| GA4 | **Tamam** | `G-WQDKQHYBHW`, özel olaylar kurulu |
| KVKK metni + rıza kutusu + çerez şeridi | **Tamam** | KVKK zorunlu, ETK ayrı onay — doğru pratik |
| CRM ve lead akışı | **Var** | `[DOĞRULA: hangi CRM, ortalama ilk dönüş süresi]` |
| **Çerez şeridine reklam izni eklenmesi** | **Eksik — 1. öncelik** | `ad_storage` hiç `granted` olmuyor; reklam ölçümünü tamamen kapatıyor |
| **Google Ads dönüşüm etiketi (`AW-`)** | **Eksik** | |
| **Meta Pixel + CAPI** | **Eksik** | |
| **Form gönderimi olayı (`generate_lead`)** | **Eksik** | `/tesekkurler/` sayfası GA4'te dönüşüm mü, kontrol et |
| **Formda gclid / utm gizli alanı** | **Eksik** | Offline dönüşüm aktarımının ön şartı |
| GTM konteyneri | Yok | Etiket yönetimi tema koduna bağlı |
| Reklam hesapları **Moonstone mülkiyetinde** açılır | Yönetim | Ajans hesabı değil |
| Google Business profili | Yerel SEO | `[DOĞRULA: mevcut mu]` |
| Kreatif envanteri: en az 8 varlık | Üretim | `references/kreatif-degerlendirme.md` § 3 |
| Satış ekibi lead karşılama senaryosu ve dönüş süresi hedefi | Satış | 5 dakika hedefi |
| Bilinmeyenlerin kapatılması | Yönetim | Fiyat, teslim, ruhsat, daire sayısı |

**Kullanıcı bu fazda reklam açmak isterse:** hayır deme. En küçük sağlam
kurguyu ver — tek Meta kampanyası, lead formu + WhatsApp, düşük günlük
bütçe — ve bunun **satış kampanyası değil mesaj testi** olduğunu yaz.
Bu aşamada toplanan bilgi (hangi kreatif tutuyor, hangi daire tipi
soruluyor) Faz 1'i haftalarca hızlandırır.

---

## 3. Faz 1 — Sinyal toplama

**Amaç lead değil, öğrenme.** Bu fazda CPL'in yüksek olması sorun değil;
hiçbir şey öğrenmeden ucuz lead toplamak sorundur.

**Kurgu:**
- Meta: tek kampanya, tek reklam seti, **8-15 kreatif** — farklı kanca ve
  formatta. Kitleyi değil kreatifi test ediyorsun.
- Google: marka savunması + dar yüksek niyet kümesi.
- Bütçe: kademeye göre, ama tek kanala yığ. Bölme.

**Bu fazın cevaplaması gereken beş soru:**
1. Hangi kreatif arketipi tutuyor? (hook rate ile)
2. Hangi vaat tıklatıyor? (CTR ile)
3. Lead formu mu WhatsApp mı daha nitelikli lead veriyor?
4. Hangi daire tipi soruluyor? (satış ekibinden geri bildirim)
5. Gerçek CPL ve nitelikli oran ne? (`references/birim-ekonomi.md` tablosu artık ölür)

**Çıktı:** Bir sayfalık "öğrenilenler" notu ve Faz 2 bütçe önerisi.
Faz 1 bu belge yazılmadan kapanmaz.

---

## 4. Faz 2 — Ölçekleme

Faz 1'in kazananları büyütülür, kaybedenler kapatılır.

- Bütçe artışı **3-4 günde bir en fazla %20** (öğrenme sıfırlanmasın).
- Remarketing devreye girer — havuz artık doludur.
- Google'da keşif katmanı ve gerekiyorsa PMax açılır (**ölçüm ve
  nitelikli-lead sinyali koşuluyla**).
- **Kreatif üretim hattı kurulur:** haftada en az 2 yeni kreatif. Bu fazda
  performansı bütçe değil kreatif tazeliği belirler.
- Offline dönüşüm aktarımı çalışır durumda olmalı — değilse ölçekleme,
  çöp lead hacmini ölçekler.

**Ölçekleme durdurma sinyali:** Nitelikli lead maliyeti, hedefin %30
üstüne çıktıysa bütçe artışını durdur. Sorun kreatifte mi, açık artırmada
mı, satış tarafında mı — teşhis koymadan devam etme.

---

## 5. Faz 3 — Verim ve stok yönetimi

Stok azaldıkça reklam mantığı değişir: artık hacim değil **eşleşme** aranır.

- Kalan daire tiplerine göre kampanya ayrıştırılır; stokta olmayan tipin
  reklamı durur (elde olmayanı pazarlamak, en pahalı lead türüdür).
- Bütçe yüksek niyetli katmana kayar; keşif katmanı kısılır.
- Yeniden pazarlama ağırlığı artar — havuz artık büyük ve olgun.
- Ticari alan tarafı ayrı bir kampanya olarak öne çıkabilir; rezidansla
  aynı takvimde bitmez.
- **Aciliyet dili yine yasak.** Stok azaldı diye "son daireler" denmez;
  `references/mevzuat-ve-politika.md`.

---

## 6. Haftalık ritim

| Gün | İş | Süre |
|---|---|---|
| Pazartesi | Hafta özeti, bütçe kontrolü, anomali taraması | 30 dk |
| Salı | Arama terimleri raporu, negatif kelime ekleme | 20 dk |
| Çarşamba | Kreatif performansı: hook rate sıralaması, yorulanları emekliye ayırma | 30 dk |
| Perşembe | Yeni kreatif brief'i / üretim hattı | 45 dk |
| Cuma | Satış ekibiyle lead kalitesi görüşmesi — **bu toplantı atlanmaz** | 30 dk |

Cuma toplantısı en değerlisidir ve ilk kesilen odur. Reklam panelinin
göremediği tek şey lead'in telefonda nasıl davrandığıdır; nitelikli lead
tanımı orada kalibre olur.

**Panel kontrol sıklığı:** Günde bir kereden fazla panele bakma. Reklam
verilerinin günlük gürültüsü, gerçek sinyalden büyüktür; sık bakmak sık
müdahaleye, sık müdahale sürekli öğrenme sıfırlanmasına yol açar.

---

## 7. Test kuyruğu

Aynı anda **tek anlamlı test** çalıştır. Paralel test, küçük bütçede
sonuçları okunamaz kılar.

Test kartı formatı:
```
Hipotez:        Kat planı gösteren kreatif, dış cephe render'ından
                daha nitelikli lead getirir
Değişken:       Yalnızca kreatif (metin, hedefleme, teklif sabit)
Karar metriği:  Nitelikli lead oranı
Minimum hacim:  Her kolda 15 lead
Karar tarihi:   [tarih]
Sonuç:          [doldurulacak]
Öğrenilen:      [doldurulacak]
```

**"Öğrenilen" satırı doldurulmadan test kapanmaz.** Testin değeri sonucunda
değil, bir sonrakini nasıl değiştirdiğindedir.

Test önceliği: kanca → format → vaat → hedef (form/WhatsApp) → detaylar.
Detaydan başlamak en yaygın vakit kaybı.

---

## 8. Karar eşikleri

Bunları kampanya açılmadan yaz; sonra tartışılmaz.

| Karar | Eşik |
|---|---|
| Kreatifi öldür | Hook rate < %15 @ 1.000 gösterim |
| Kreatifi öldür (statik) | CTR eşiğin altında @ 100+ tık |
| CPL kararı ver | En az 15-20 dönüşüm birikince |
| Kampanyayı durdur | Nitelikli lead maliyeti hedefin 2 katına çıktıysa |
| Bütçe artır | Nitelikli lead maliyeti hedefin altındaysa, 3-4 günde %20 |
| Teklif hedefi değiştir | Haftada en fazla 1 kez, %15'ten fazla değil |
| Kanal kapat | 60 gün sonunda nitelikli lead üretmediyse |

---

## 9. Kriz senaryoları

| Durum | İlk kontrol | Sonra |
|---|---|---|
| **CPL bir gecede ikiye katlandı** | Dönüşüm izleme çalışıyor mu? (en sık sebep) | Açık artırma / sezon; kreatif sıklığı |
| **Lead geliyor, hepsi çöp** | Kreatif yanlış vaat mi veriyor? Form çok mu kolay? | Nitelendirici soru ekle, "yüksek niyet" formuna geç |
| **Reklam reddedildi** | Hangi politika? Metin mi görsel mi? | `references/mevzuat-ve-politika.md`; itiraz ve düzeltme |
| **Hesap kısıtlandı** | Politika ihlali geçmişi | Meta/Google destek; **paralel yedek hesap kurma** — ihlal sayılır |
| **Rakip marka aramamıza girdi** | Marka kampanyası açık mı, gösterim payı ne | Marka kampanyası bütçesini artır, marka terimlerini savun |
| **Satış ekibi "reklam kötü" diyor** | İlk dönüş süresi kaç dakika? | Rakamla konuş: lead sayısı, nitelik oranı, dönüş süresi |

Son satır özellikle önemli: "reklam kötü" ile "lead takibi kötü" aynı
belirtiyi verir. Ayırt eden tek şey ölçümdür — bu yüzden Faz 0 pazarlıksızdır.

---

## 10. Ajans ve iş bölümü

Ajansla çalışılacaksa üç şey sözleşmede net olsun:

1. **Mülkiyet.** Google Ads hesabı, Meta Business Manager, piksel, GA4
   mülkü ve domain **Moonstone adına** olmalı. Ajans erişim alır, sahip
   olmaz. Bu tek madde, ilişkinin bittiği gün altı ay kazandırır.
2. **Ücret yapısı.** Medya bütçesi ile ajans ücreti ayrışmalı. Medya
   harcamasının yüzdesi üzerinden ücretlendirme, ajansı bütçe büyütmeye
   teşvik eder — verim değil hacim optimize edilir.
3. **Taahhüt metriği.** Lead sayısı taahhüdü kabul etme; **nitelikli lead**
   taahhüdü iste. Nitelikli tanımı sözleşmede yazılı olsun
   (`references/olcum-ve-crm.md` § 6 skorlaması).

**Aylık ajans raporunda aranacaklar:** kanal kırılımlı nitelikli lead
maliyeti, kreatif kazanan/kaybeden listesi, alınan aksiyonlar ve
gerekçeleri, gelecek ay önerisi. Yalnızca gösterim ve tık raporlayan
rapor, rapor değildir.
