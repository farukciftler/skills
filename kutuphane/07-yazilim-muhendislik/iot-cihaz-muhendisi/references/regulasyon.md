# Regülasyon ve Belgelendirme

Faz 0'da kararı, Faz 7'de icrası. Bu dosyanın tüm sayıları ve tarihleri **son doğrulama anındaki** durumu yansıtır.

> ## ⚠️ Bu dosyanın birinci kuralı
> Buradaki hiçbir tarih, ücret, eşik veya standart sürümü kullanıcıya **doğrudan** aktarılmaz.
> Her kullanımda canlı doğrula, kaynağı adıyla söyle, **[doğrulandı: GG.AA.YYYY]** damgası koy.
> Bu dosya bir **harita**dır: nereye bakılacağını, hangi soruların sorulacağını ve tuzakların
> nerede olduğunu söyler. Güncel değeri kaynaktan alırsın.
>
> Bu alan gerçekten hızlı hareket ediyor: harmonize standart listeleri kısıtlanabiliyor,
> geçiş takvimleri kayabiliyor, delegated regulation'lar yürürlükten kaldırılabiliyor.
> Bir standardın Official Journal'daki durumu, self-declaration ile Notified Body arasındaki
> farkı belirler — yani projenin takvimini ve bütçesini.

## İçindekiler
- [1. İlk soru: hangi pazarlar](#1-i̇lk-soru-hangi-pazarlar)
- [2. AB — CE ve RED](#2-ab--ce-ve-red)
- [3. AB siber güvenlik: RED 3.3 + EN 18031](#3-ab-siber-güvenlik-red-33--en-18031)
- [4. AB siber güvenlik: Cyber Resilience Act](#4-ab-siber-güvenlik-cyber-resilience-act)
- [5. ABD — FCC](#5-abd--fcc)
- [6. Türkiye](#6-türkiye)
- [7. Diğer pazarlar](#7-diğer-pazarlar)
- [8. Madde/atık/pil mevzuatı](#8-maddeatıkpil-mevzuatı)
- [9. Teknik dosya ve DoC](#9-teknik-dosya-ve-doc)
- [10. Bütçe ve takvim](#10-bütçe-ve-takvim)

---

## 1. İlk soru: hangi pazarlar

Bu, Faz 0 kapısının kriteridir. Cevap yoksa mimari kararlar verilemez.

Her pazar farklı bir rejim: AB (CE + RED), Birleşik Krallık (UKCA + PSTI), ABD (FCC), Kanada (ISED), Türkiye (BTK/TEY + CE), Japonya (MIC/Giteki), Avustralya (RCM), Hindistan (WPC/BIS), Kore (KC), Çin (SRRC/CCC), Brezilya (ANATEL).

**Sonuç, tasarımı doğrudan etkiler:** kullanılabilir frekans bantları, izinli çıkış gücü, kanal planı, duty-cycle limiti ve — en önemlisi — **ön-sertifikalı modül seçimi** (modülün hangi ülkelerde grant'ı var?).

Modül seçerken **modülün hangi pazarlarda sertifikalı olduğunu** kontrol et. Sadece FCC'si olan bir modülle AB'ye çıkmak, avantajın yarısını kaybettirir.

---

## 2. AB — CE ve RED

Kablosuz bir cihaz AB'de **Telsiz Ekipmanları Direktifi (RED, 2014/53/EU)** kapsamındadır. RED, kablosuz ürünlerde EMC ve alçak gerilim direktiflerini de kendi içine alır — ayrıca EMC/LVD CE işareti almazsın, RED'in ilgili maddeleri üzerinden karşılarsın.

### Temel gereklilikler (Madde 3)

| Madde | Konu | Tipik harmonize standart |
|---|---|---|
| 3.1(a) | Sağlık ve güvenlik | EN 62368-1 (elektriksel güvenlik), EN 62479 / EN 62311 (RF maruziyeti) |
| 3.1(b) | Elektromanyetik uyumluluk | EN 301 489-1 + teknolojiye özel parça |
| 3.2 | Spektrumun etkin kullanımı | Radyoya özel standart (aşağıda) |
| 3.3(d)(e)(f) | Siber güvenlik, gizlilik, dolandırıcılığa karşı koruma | EN 18031-1/-2/-3 — bkz. §3 |

### Radyo teknolojisine göre standart (tipik eşleştirme — sürümleri doğrula)

| Teknoloji | Radyo standardı | EMC standardı |
|---|---|---|
| Wi-Fi 2.4 GHz / BLE / Zigbee / Thread | EN 300 328 | EN 301 489-1 + -17 |
| Wi-Fi 5 GHz | EN 301 893 | EN 301 489-1 + -17 |
| Wi-Fi 6 GHz | EN 303 687 | EN 301 489-1 + -17 |
| Sub-GHz SRD (LoRa 868, Z-Wave) | EN 300 220 | EN 301 489-1 + -3 |
| NFC / 13.56 MHz | EN 300 330 | EN 301 489-1 + -3 |
| 1-40 GHz SRD | EN 300 440 | EN 301 489-1 + -3 |
| Hücresel (LTE-M/NB-IoT/4G/5G) | EN 301 908 serisi / ilgili ETSI | EN 301 489-1 + -52 |
| GNSS alıcı | EN 303 413 | — |

**Her birinin sürüm numarasını ve Official Journal'daki güncel alıntı durumunu doğrula.** Standart sürümleri güncellenir ve eski sürümün presumption of conformity'si sona erer.

### Uygunluk değerlendirme modülleri

- **Modül A (iç üretim kontrolü)**: harmonize standartlar tam olarak uygulandıysa üretici kendi beyan eder. IoT ürünlerinin çoğunun yolu budur — ama yine de **akredite laboratuvarda test** ve teknik dosya gerekir. "Kendim beyan ederim, test gerekmez" yanlıştır.
- **Modül B + C (AB tip incelemesi)**: harmonize standart uygulanmıyorsa veya kısıtlar tetiklendiyse **Onaylanmış Kuruluş** (Notified Body) devreye girer. CE işaretinin yanına 4 haneli NB numarası eklenir.
- **Modül H (tam kalite güvencesi)**: onaylı kalite sistemi üzerinden.

Kısıtların hangi durumda modül B+C'yi zorunlu kıldığını §3'te göreceksin — bu, projeyi haftalar ve on binlerce lira etkileyen tek maddedir.

---

## 3. AB siber güvenlik: RED 3.3 + EN 18031

**Durum (bu dosya yazılırken):** Delegated Regulation (EU) 2022/30, RED'in 3.3(d), (e), (f) maddelerini internete bağlanan telsiz ekipmanı için **1 Ağustos 2025'ten itibaren zorunlu** hale getirdi. Bu tarih daha önce bir kez ertelendi (2024'ten 2025'e), harmonize standartların yayımlanması için.

**Harmonize standart: EN 18031 serisi** (CEN-CENELEC JTC 13), Official Journal'da **kısıtlarla** listelendi:

| Parça | Karşıladığı madde | Konu |
|---|---|---|
| EN 18031-1 | 3.3(d) | Ağın korunması / ağ dayanıklılığı |
| EN 18031-2 | 3.3(e) | Kişisel veri ve mahremiyet (çocuk oyuncakları/bakım cihazlarında ebeveyn erişim kontrolü dahil) |
| EN 18031-3 | 3.3(f) | Parasal değer taşıyan cihazlarda dolandırıcılığa karşı koruma |

### Kısıtlar — projeyi belirleyen kısım

Standartlar **koşulsuz** harmonize değil. Bilinen kısıt temaları:
- Kullanıcının **parola oluşturmadan** ve kullanmadan cihazı çalıştırabildiği durumlar (ilgili maddeler tüm parçalarda)
- Oyuncak/çocuk bakım cihazlarında ebeveyn/vasi erişim kontrolünün sağlanmadığı durumlar (EN 18031-2)
- Finansal varlıklarla ilgili güvenli güncelleme kriterleri (EN 18031-3)

**Kısıt senin ürününe uygulanıyorsa, harmonize standardın verdiği uygunluk karinesi geçersiz olur ve Onaylanmış Kuruluş üzerinden belgelendirme gerekir.**

Pratik sonuç: **ürünü kısıt tetiklemeyecek şekilde tasarla.** Yani kullanıcıya benzersiz parola oluşturmayı zorunlu kıl veya cihaz başına benzersiz kimlik bilgisi kullan. Bu, `firmware-guvenlik.md` §5'teki provisioning kararıyla aynı karardır — ve bir yazılım tercihi olarak görünse de aslında **belgelendirme yolunu** seçen karardır.

**Doğrulanacaklar:** EN 18031 parçalarının güncel sürümleri, Official Journal'daki alıntı durumu ve kısıtların tam metni, Komisyon'un yayımladığı kısıt uygulama rehberi.

### Kapsam: "internete bağlı" ne demek

Doğrudan internete bağlanan cihazlar kadar, **bir ara cihaz (telefon, hub, gateway) üzerinden dolaylı bağlananlar** da kapsamda. Telefona bağlanan bir BLE cihazı, telefon üzerinden internete veri gönderiyorsa kapsamdadır. "Sadece BLE, internet yok" savunması genelde çalışmaz — kontrol et.

### ETSI EN 303 645

Tüketici IoT için uluslararası taban güvenlik standardı (13 hüküm ailesi + kişisel veri koruma). RED'in harmonize standardı **değil** ama:
- EN 18031 gereksinimlerinin büyük kısmıyla örtüşür
- UK PSTI, Singapur CLS, Finlandiya etiketi, Avustralya ve Hindistan programlarının dayanağı
- Test spesifikasyonu: ETSI TS 103 701

Tek bir güvenlik tasarımıyla birden çok pazarı karşılamak istiyorsan, EN 303 645'i **tasarım kontrol listesi** olarak kullan. Hüküm başlıkları `firmware-guvenlik.md` §7'de firmware karşılıklarıyla eşlenmiş durumda.

---

## 4. AB siber güvenlik: Cyber Resilience Act

**Regulation (EU) 2024/2847.** RED'in siber güvenlik delegated act'inin yerini alacak yatay düzenleme — ve kapsamı çok daha geniş: **dijital unsur taşıyan tüm ürünler** (donanım + yazılım + uzaktan veri işleme çözümleri), sadece telsiz değil.

### Takvim (doğrula — bu dosya bu tarihlere göre yazıldı)

| Tarih | Ne olur |
|---|---|
| 10 Aralık 2024 | Yürürlüğe girdi |
| 11 Haziran 2026 | Üye devletlerin uygunluk değerlendirme kuruluşlarını bildirmesi |
| **11 Eylül 2026** | **Raporlama yükümlülükleri başlar** — piyasadaki mevcut ürünler dahil |
| 11 Aralık 2027 | Tam uygulama; CE işareti için CRA uygunluğu şart |

> **Bugüne göre kritik not:** 11 Eylül 2026 raporlama tarihi **çok yakın veya geçmiş** olabilir. Kullanıcının piyasada ürünü varsa bunu ilk gündeme getirilecek madde yap ve tarihi mutlaka canlı doğrula.

### Raporlama yükümlülüğü (11 Eylül 2026'dan itibaren)

Aktif olarak **istismar edilen** bir zafiyet veya ciddi güvenlik olayı için ENISA'nın tek raporlama platformu üzerinden:
- **24 saat** içinde erken uyarı
- **72 saat** içinde tam bildirim
- **14 gün** içinde nihai rapor

Bu, **halihazırda piyasada olan ürünler için de** geçerli. Yani 2027'yi beklemek bir strateji değil. Ön koşul: yayımlanmış **koordineli zafiyet açıklama (CVD) politikası** ve ENISA platformuna erişim hazır olmalı.

### Ürün ve süreç yükümlülükleri (11 Aralık 2027'den itibaren)

- Tasarımdan güvenli (secure by design), bilinen istismar edilebilir zafiyet olmadan piyasaya sürme
- Güvenli varsayılan yapılandırma, şifreli haberleşme, tüm arayüzlerde erişim kontrolü, yazılım bütünlüğü doğrulama, DoS dayanıklılığı
- **SBOM**: en azından üst düzey bağımlılıkları kapsayan, makine okunabilir formatta, ürün ömrü boyunca güncel. Kamuya açık olması gerekmez; piyasa gözetim otoritesi isterse verilir.
- **Zafiyet yönetimi süreci** ve ücretsiz güvenlik güncellemeleri
- **Destek süresi beyanı** — satış noktasında ilan edilir; ürünün daha kısa kullanılması beklenmiyorsa **beş yıldan kısa olamaz**
- Ürün sınıfına göre uygunluk değerlendirme yolu: varsayılan sınıf öz-değerlendirme; "önemli" (Annex III) ve "kritik" (Annex IV) ürünlerde üçüncü taraf değerlendirme

**Ürün sınıfını erken belirle.** Sınıflandırma, öz-beyan ile Notified Body arasındaki farktır.

### Geçiş

11 Aralık 2027'den önce piyasaya sürülen ürünler, o tarihten sonra **esaslı değişiklik (substantial modification)** geçirmedikçe tam gerekliliklere tabi olmaz — ama **raporlama yükümlülüğü her hâlükârda geçerlidir**.

RED'in siber güvenlik delegated regulation'ı CRA lehine kaldırılıyor; Komisyon 16 Şubat 2026'da 11 Aralık 2027 itibarıyla yürürlükten kaldıran bir delegated regulation kabul etti. **Yani Eylül 2026 – Aralık 2027 arasında iki rejim paralel işliyor.** Bu geçiş dönemindeki durumu her seferinde doğrula.

---

## 5. ABD — FCC

### Üç yol

| Yol | Ne zaman | Tipik maliyet | Tipik süre |
|---|---|---|---|
| **SDoC** (öz-beyan) | Kasıtsız yayıcı — radyosuz dijital cihaz | Düşük | Haftalar |
| **SDoC + modül grant'ı** | Ön-sertifikalı radyo modülü kullanan cihaz | Düşük-orta | Birkaç hafta |
| **Certification (FCC ID)** | Kendi radyo tasarımın | Yüksek | Aylar |

Ön-sertifikalı modül yolunda: modülün FCC ID'si kasıtlı yayıcı kısmını karşılar, senin ürünün **Part 15 Subpart B** (kasıtsız yayıcı) testine kalır. Bu, tipik olarak beş haneli dolar ve haftalarca zaman tasarrufudur.

**Modüler onayın sınırları (KDB 996369 çerçevesi):**
- **Full modular approval**: modül kendi kendine yeter (kendi ekranlaması, kendi anteni/anten listesi).
- **Limited modular approval**: koşullara bağlı; host tasarımı belirli şartları sağlamalı.
- **Grant'ın anten listesi ve kazanç sınırı dışına çıkarsan** avantaj biter. Anteni değiştirmek, kazancı artırmak veya modülü grant'ın öngörmediği bir kullanımda çalıştırmak tam sertifikasyona düşürür.
- Modülün grant metnini **oku**; varsayma.

**Süreç:** akredite laboratuvarda test → teknik dosya → TCB (Telecommunication Certification Body) incelemesi → grant. SDoC'de TCB yok, raporu dosyanda tutarsın ve FCC isterse sunarsın.

**Ek kalemler:** RF maruziyeti değerlendirmesi (SAR veya muafiyet hesabı — vücuda yakın kullanılan cihazlarda), etiketleme kuralları (FCC ID görünür olmalı; küçük cihazda e-labeling), kullanım kılavuzunda zorunlu uyarı metni.

**Kanada (ISED)** genelde FCC ile paralel yürütülür ve marjinal ek maliyetle eklenir; ABD'ye gidiyorsan aynı lab ziyaretinde sor.

**Hücresel varsa:** operatör sertifikasyonu (AT&T, Verizon vb.) + PTCRB ayrı ve çok daha pahalı/uzun bir süreçtir. Bunu ayrı bir proje gibi planla.

---

## 6. Türkiye

**Yetkili kurum: BTK (Bilgi Teknolojileri ve İletişim Kurumu).** Telsiz Ekipmanları Yönetmeliği (TEY), 05.11.2020 tarihli ve 31295 sayılı Resmî Gazete'de yayımlandı ve AB'nin RED'i (2014/53/AB) ile uyumludur.

**Ana hatlar:**
- Telsiz ekipmanının piyasaya arzı için **CE işareti zorunlu** ("CE İşareti Yönetmeliği" çerçevesinde).
- Uygunluk değerlendirme modülleri RED ile aynı: **Modül A** (iç üretim kontrolü), **Modül B+C**, **Modül H**.
- Onaylanmış Kuruluşlar rejimi mevcut; ilgili yönetmelik usul ve esasları belirler.
- BTK piyasa gözetimi ve denetimi (PGD) yapar; uygun olmayan cihazın arzını yasaklama, toplatma ve bertaraf yetkisi vardır.
- İthalat denetimi tarafında Ticaret Bakanlığı süreçleri devrededir.

**Pratik sonuç:** AB için hazırladığın teknik dosya ve test raporları Türkiye için de büyük ölçüde kullanılabilir. Tekrar test genelde gerekmez, ama **belge dili, yetkili temsilci ve etiketleme** gereklerini doğrula.

**Yerel test altyapısı:** TÜRKAK akreditasyonlu EMC/LVD laboratuvarları Türkiye'de mevcut ve fiyatlar Batı Avrupa'nın belirgin altında olabiliyor. Laboratuvar seçerken:
- TÜRKAK akreditasyon kapsamının **senin standardını** içerdiğini akreditasyon belgesinden doğrula (her lab her standardı kapsamaz)
- Radyo (EN 300 328 / EN 300 220) testlerini yapıp yapmadığını sor — EMC yapan her lab radyo yapmaz
- Raporun AB'de kabul göreceğinden emin ol (özellikle FCC/TCB süreci hedefliyorsan lab'ın FCC tanınırlığını sor)
- Ön-uyum (pre-compliance) hizmeti verip vermediğini sor — bu, tam testten önce ucuz bir güvence

**Fiyat sorulursa:** güncel teklif al, ezberden rakam verme. Ürün karmaşıklığı, standart sayısı ve tekrar testi ihtimali fiyatı belirler.

**Türkiye'ye özgü ek konular** — ürün türüne göre doğrula: TSE belgelendirme gereklilikleri, enerji verimliliği etiketi, Türkçe kullanım kılavuzu zorunluluğu, garanti belgesi ve satış sonrası hizmet yeterlilik belgesi, AEEE (atık elektrikli ekipman) kaydı, pil ve akümülatör mevzuatı.

---

## 7. Diğer pazarlar

| Pazar | Rejim | Not |
|---|---|---|
| Birleşik Krallık | UKCA + **PSTI Act** | PSTI 29 Nisan 2024'te yürürlükte: evrensel varsayılan parola yasağı, zafiyet bildirim politikası, güncelleme destek süresi beyanı. Uygunluk beyanı gerekir. Dayanağı EN 303 645. |
| Kanada | ISED | FCC ile paralel yürür |
| Japonya | MIC / Giteki | Ayrı işaret; modül seçerken Giteki'si olanı tercih et |
| Avustralya/YZ | RCM | ACMA |
| Hindistan | WPC (ETA) + BIS | Yerel süreç uzun |
| Kore | KC | |
| Çin | SRRC + (kapsamdaysa) CCC | |
| Brezilya | ANATEL | |

**Modül seçerken çoklu sertifikasyonu olan modülü tercih etmek**, uzun vadede her pazar için ayrı ayrı ödemekten çok ucuzdur.

---

## 8. Madde/atık/pil mevzuatı

Bunlar radyo testinden bağımsız ve unutulduğunda sevkiyatı durdurur:

- **RoHS**: tehlikeli madde kısıtlaması. Tedarikçilerden uygunluk beyanı toplanır; teknik dosyaya girer.
- **REACH / SVHC**: yüksek önem arz eden maddeler; bildirim yükümlülükleri.
- **WEEE**: atık elektrikli ekipman — üretici kaydı, geri dönüşüm katkı payı, üzeri çizili çöp kutusu sembolü. Ülke bazında kayıt gerekir.
- **Pil mevzuatı**: AB Pil Regülasyonu kapsamında işaretleme, kayıt, geri toplama; ürüne gömülü pilin **sökülebilirliği** konusunda gelişen gereklilikler var — **canlı doğrula**, bu alan hareketli.
- **UN 38.3**: lityum hücre/pil taşıma testi. Numune bile göndersen gerekir. Hücre üreticisinden test özetini iste.
- **IEC 62133**: lityum hücre/pil güvenliği.
- **Ambalaj mevzuatı** ve ülke bazlı ambalaj atığı kayıtları.
- **GPSR** (AB Genel Ürün Güvenliği Regülasyonu): tüketici ürünlerinde ek bilgi/izlenebilirlik gereklilikleri.

---

## 9. Teknik dosya ve DoC

### Teknik dosya içeriği (RED için)

- Ürün tanımı, model/tip, fotoğraflar
- Blok şema, devre şeması, PCB layout, **RF bölümünün açıkça işaretlenmesi**
- Parça listesi ve kritik bileşen bilgileri
- Firmware sürümü ve radyoyla ilgili yazılım açıklaması
- Uygulanan harmonize standartların listesi (sürüm numaralarıyla)
- **Tüm test raporları** (akredite lab)
- Risk değerlendirmesi (Madde 3.1(a) için)
- Radyo yapılandırmalarının tablosu: bant, modülasyon, maksimum güç (iletken ve EIRP), anten tipi ve kazancı, uygulanan standart
- Siber güvenlik değerlendirmesi (EN 18031 karşılama kanıtı)
- Kullanım kılavuzu ve güvenlik bilgileri (bant ve güç bilgisi dahil)
- Etiket tasarımı ve yerleşimi
- Notified Body kullanıldıysa AB tip inceleme sertifikası
- Üretim kontrol prosedürleri

**Saklama süresi:** ürünün piyasaya arzından itibaren belirli bir süre (RED için 10 yıl) — güncel süreyi doğrula.

### AB Uygunluk Beyanı (DoC) — asgari yapı

```
AB UYGUNLUK BEYANI
No: <benzersiz numara>

1. Ürün: <tanım, model, tip>
2. Üretici: <ad, tam adres>
3. Bu beyan üreticinin tek sorumluluğu altında düzenlenmiştir.
4. Beyanın konusu: <ürün tanımı; gerekirse izlenebilirlik için renkli görsel>
5. Yukarıda tanımlanan beyan konusu, 2014/53/AB sayılı Direktife ve
   ilgili diğer AB mevzuatına uygundur.
6. Çalışılan frekans bantları ve maksimum güç (EIRP):
   <bant> : <dBm>
7. Uygulanan harmonize standartlar (sürüm ve tarihiyle):
   EN 62368-1 ...            (madde 3.1(a))
   EN 62311 / EN 62479 ...   (madde 3.1(a) — RF maruziyeti)
   EN 301 489-1 ...          (madde 3.1(b))
   EN 301 489-17 ...         (madde 3.1(b))
   EN 300 328 ...            (madde 3.2)
   EN 18031-1 / -2 [/-3] ... (madde 3.3(d)(e)[(f)])
8. Onaylanmış Kuruluş: <ad, numara, sertifika no> — varsa
9. Ek bilgiler:
   İmzalayan: <ad, unvan>  Yer/Tarih:  İmza:
```

**Sık yapılan hatalar:** eski direktife (1999/5/EC) atıf, standart sürüm numarasının yazılmaması, EIRP yerine sadece iletken gücün yazılması, siber güvenlik standardının unutulması, DoC'nin kullanıcı tarafından erişilebilir kılınmaması.

---

## 10. Bütçe ve takvim

**Aşağıdaki aralıklar kaba planlama içindir. Gerçek rakam için teklif al ve tarih damgası koy.**

| Kalem | Etki |
|---|---|
| Ön-sertifikalı modül vs kendi radyo tasarımın | En büyük tek kalem: modül yolu maliyeti ve süreyi büyük oranda düşürür |
| Radyo sayısı | Her ek radyo (Wi-Fi + BLE + LoRa) ayrı radyo standardı = ayrı test |
| Şebeke gerilimi var mı | Elektriksel güvenlik testi ekler, süreyi uzatır |
| Vücuda yakın kullanım | RF maruziyeti / SAR değerlendirmesi ekler |
| Kısıt tetiklenmesi (EN 18031) | Öz-beyandan Notified Body'ye geçiş = ciddi maliyet + süre |
| Hücresel | Operatör + PTCRB sertifikasyonu; ayrı bir proje ölçeğinde |
| Matter/Thread/Wi-Fi Alliance | CSA + taşıyıcı alyans üyeliği ve ürün başına sertifikasyon |
| İlk seferde geçememe | Tekrar testi + respin + lab kuyruğu = haftalar |

**Takvimi geriye doğru planla:**

```
Sevkiyat tarihi
  ← ambalaj/etiket üretimi           (2-4 hafta)
  ← seri üretim + üretim testi        (4-8 hafta)
  ← sertifikasyon (lab kuyruğu dahil) (6-16 hafta, hücreselse çok daha uzun)
  ← EMC ön-uyum + düzeltme + respin   (4-8 hafta)
  ← saha pilotu                       (4-8 hafta)
  ← Rev B bring-up                    (3-5 hafta)
  ← Rev A bring-up + düzeltme         (4-6 hafta)
  ← layout + fab + dizgi              (4-6 hafta)
  ← şematik + parça tedariki          (3-6 hafta)
  ← mimari kararı
```

**Lab kuyruğunu erken rezerve et.** Test slotu genelde haftalar öncesinden dolar; "ürün hazır olunca ararım" yaklaşımı takvimi 4-6 hafta uzatır.

### Sertifikasyon öncesi son kontrol

- [ ] Test edilecek numune **üretim niyetli** (production-intent) — Rev A prototip değil
- [ ] Firmware **sürüm kilitli**; test sonrası RF'i etkileyecek değişiklik yapılmayacak
- [ ] Muhafaza nihai (malzeme, renk, montaj dahil) — kutu değişikliği anteni etkiler
- [ ] Tüm kablolar nihai uzunluk ve tipte
- [ ] Ön-uyum marjı ≥ 6 dB
- [ ] Test modu firmware'i hazır (sürekli TX, kanal sabitleme, güç ayarı) — lab bunu isteyecek
- [ ] Etiket tasarımı ve kılavuz metni hazır
- [ ] Modül kullanılıyorsa grant metni ve modül test raporu dosyada
- [ ] Siber güvenlik kanıtları toplanmış (parola politikası, OTA, CVD politikası, SBOM)
- [ ] Yedek numune var (lab genelde 2-3 ünite ister, biri hasar görebilir)
