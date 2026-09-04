# Teknoloji, SaaS, E-ticaret, Telekom — Suriye Regülasyon Katmanı

Son güncelleme: 28 Ağustos 2026. Bu alan Suriye'de en hızlı değişen katman: 2026'da yeni mobil operatör lisansı verildi, dijital dönüşüm programı yürüyor, vergi reformu dijital hizmetleri de kapsıyor. Her lisans/kural iddiasını canlı doğrula.

## Sektörel giriş kapıları

| Faaliyet | Yabancı mülkiyet | Lisans/izin |
|---|---|---|
| Yazılım geliştirme, IT hizmetleri, SaaS, web/uygulama, danışmanlık | %100 serbest | Normal şirket tescili + faaliyet konusu yeterli (özel lisans bilinmiyor — DOĞRULA) |
| E-ticaret platformu işletme | %100 serbest | Şirket tescili; tüketici/mesafeli satış kuralları için İç Ticaret tarafını doğrula |
| ISP / internet servis | Sınırlı | SY-TPRA lisansı; telekom altyapısında ~%49 yabancı tavanı — DOĞRULA |
| Mobil operatörlük | Devlet ortaklı imtiyaz | MoCT ihalesi (2026: Zain, 747M USD, 25 yıl, %25 Suriye Varlık Fonu ortaklığı; Zain Syria lansmanı 2027 başı hedefli; Syriatel diğer operatör) |
| Fintech / ödeme hizmeti | Belirsiz/gelişiyor | Merkez Bankası (CBS) izni; PSP/e-para çerçevesi yeni oluşuyor — DOĞRULA, bu bir mevzuat boşluğu |

## Sınır ötesi SaaS satışı (Suriye'de şirket kurmadan)

- Suriye'de yerleşik olmayan bir TR şirketinin Suriye'deki müşterilere SaaS satması için Suriye'de lisans şartı bilinmiyor; asıl engeller **ödeme tahsilatı** ve **yerel güven**dir.
- Yeni **satış vergisi** taslağı yurt içine sunulan hizmetleri kapsıyor; sınır ötesi dijital hizmetlere ters yükümlülük (reverse charge) veya kayıt şartı getirilip getirilmediğini doğrula — "Syria sales tax digital services non-resident".
- TR tarafı: Suriye'ye hizmet ihracı → KDV istisnası (hizmet ihracı şartlarıyla) + kazancın TR'de vergilenmesi; `turkiye-katmani.md`.

## Ödeme ve tahsilat gerçekliği

- 2025-26 normalleşmesi: **SWIFT restore**, CBS'nin NY Fed hesabı, **Visa/Mastercard** Suriye kartları için onaylandı; QNB Mayıs 2026'da ülke içinde uluslararası kart kabulünü başlatan ilk yabancı banka oldu. Kart kabul altyapısı (POS/sanal POS) hâlâ emekleme — hangi bankalar e-ticaret sanal POS veriyor, canlı doğrula.
- Stripe/PayPal gibi global PSP'lerin Suriye desteği: geçmişte tamamen kapalıydı; yaptırım sonrası durumunu her seferinde doğrula ("Stripe supported countries Syria", "PayPal Syria [yıl]") — muhtemelen hâlâ yok, alternatif: yerel banka sanal POS, bölgesel PSP'ler, havale/ödeme noktası ağları, mobil bakiye.
- Nakit ve havale ağları (ör. Al-Haram, Fouad benzeri sarraf/transfer ofisleri) fiilen yaygın; kurumsal tahsilatta belgelendirme riskine dikkat çek.
- Ekonomi fiilen dolarize: fiyatlama USD, tahsilat SYP/USD karışık — sözleşmede kur maddesi şart.

## Elektronik işlem / veri / içerik mevzuatı (çıpalar — hepsi Esad dönemi, statüsünü doğrula)

- **E-imza ve Şebeke Hizmetleri Kanunu 4/2009** — e-imza altyapısı; NANS yetkili.
- **Elektronik İşlemler Kanunu 3/2014** — elektronik sözleşme/belge geçerliliği.
- **Siber Suç Kanunu 20/2022** — Esad döneminin tartışmalı kanunu (ifade suçları dâhil); geçiş hükûmetinde revizyon/uygulama durumu DOĞRULA — içerik barındıran ürünlerde (sosyal özellik, UGC) risk kalemi.
- **Kişisel veri koruma:** Kapsamlı bir KVK/GDPR muadili **yok** (boşluk). Veri lokalizasyonu genel şartı bilinmiyor; kamu ihaleleri/telekom için yerel barındırma şartları çıkabilir — proje bazında doğrula.
- **Hosting:** yerel veri merkezi kapasitesi zayıf; SaaS fiilen yurt dışı bulutta barındırılıyor. Elektrik/internet kesintileri son kullanıcı deneyimi için tasarım kısıtı (offline-first düşün).

## Fikri mülkiyet

- Marka/patent: Ticari ve Sınai Mülkiyet Koruma Müdürlüğü'nde **ulusal tescil**; Suriye Paris Sözleşmesi tarafı, Madrid Protokolü üyesi değil (DOĞRULA) → TR/WIPO tesciliniz Suriye'yi otomatik kapsamaz.
- Yazılımda telif koruması mevcut mevzuatta zayıf/eski; sözleşmesel koruma (lisans sözleşmesi, NDA) esas alınmalı.

## Pazar bağlamı (ürün kararlarını etkileyen)

- Mobil: Syriatel + (2027'den itibaren) Zain Syria; 2G/3G kapatma yol haritası → akıllı telefon penetrasyonu artacak; SMS OTP maliyet/erişimini operatörle doğrula.
- Meta reklamları Suriye'de tekrar çalışıyor (2025+) → dijital pazarlama kanalı açık; Google Ads durumunu ayrıca doğrula.
- Devlet dijitalleşme programı (MoCT) e-devlet/e-fatura projeleri üretiyor → B2G entegrasyon fırsatları; Syria HiTech fuarı (Nisan, Şam) sektör buluşması.
- İnternet altyapısı: sabit genişbant zayıf, mobil veri esas; Starlink/uydu internetin hukuki durumu belirsiz — DOĞRULA.

## Hazır doğrulama sorguları

- "Syria ISP license SY-TPRA requirements" · "Syria telecom foreign ownership cap"
- "Syria e-commerce regulation consumer [yıl]" · "Syria fintech payment license central bank"
- "Syria virtual POS online payment gateway [yıl]" · "Stripe/PayPal availability Syria"
- "Syria data protection law [yıl]" · "Syria cybercrime law 20 2022 status"
- "Syria trademark registration foreigner" · "WIPO Syria membership"
- "Zain Syria launch" · "Syriatel corporate services"
