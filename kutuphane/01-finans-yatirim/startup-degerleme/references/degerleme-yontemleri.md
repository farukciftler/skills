# Değer Tespiti Yöntemleri

## İçindekiler
1. Hangi durumda hangi yöntem
2. Türetme formülleri (indirme, kullanıcı, gelir)
3. Yöntemler tek tek
4. Türkiye erken aşama çarpan bandları
5. Üç değer katmanı ve senaryolar
6. Büyüme Potansiyeli skoru
7. Sık yapılan hatalar

---

## 1. Hangi durumda hangi yöntem

| Şirketin durumu | Birincil yöntem | Destekleyici |
|---|---|---|
| Gelir yok, kullanıcı az, ürün var | Yeniden Yapım Maliyeti + Acquihire | Berkus |
| Gelir yok, kullanıcı çok | Kullanıcı Başı Değer (per-MAU) | Stratejik alıcı primi |
| Gelir var, kârlı değil | Gelir Çarpanı (ARR ×) | SDE, per-MAU |
| Gelir var, kârlı, küçük | SDE Çarpanı (sahibe kalan kâr ×) | Gelir çarpanı |
| Yatırım turu var | Son tur post-money + ilerleme/gerileme düzeltmesi | Scorecard |
| Zorunlu satış / para bitiyor | Tasfiye + Yakım Baskısı iskontosu | Rebuild cost |

**Her zaman en az üç yöntem koştur ve sonuçları yan yana koy.** Yöntemler birbirinden
çok uzaklaşıyorsa (ör. 10 kat fark), bu bir bulgudur: şirketin değeri hangi hikâyeye
inandığına bağlıdır ve raporda bunu açıkça söyle.

## 2. Türetme formülleri

Ham veriden eksik metriği çıkarmak. Hepsi `[T]` etiketiyle girer.

**Play indirme bandı → nokta tahmin**
`1 B+` → 1.000–5.000 (orta: ~2.000)
`5 B+` → 5.000–10.000 · `10 B+` → 10.000–50.000 · `50 B+` → 50.000–100.000
`100 B+` → 100.000–500.000. Bandın alt ucuna yakın say; Google bandı geçer geçmez yükseltir,
yani çoğu uygulama bandın alt üçte birindedir.

**iOS puan sayısı → iOS indirme**
Puanlama oranı tipik olarak indirmelerin **%0,5–2**'si. Sosyal/ücretsiz uygulamalarda
alt uca, oyun ve prompt kullanan uygulamalarda üst uca yakın.
`iOS indirme ≈ puan sayısı ÷ 0,01` (bant: ÷0,02 ile ÷0,005 arası)
Örnek: 27 puan → ~1.350 (bant 1.350–5.400).

**TR platform dağılımı**
Türkiye'de Android ≈ %75-80, iOS ≈ %20-25 kurulu taban. Ama iOS kullanıcısı ödeme
yapma eğiliminde 3-5 kat daha değerlidir. Toplam indirme ≈ Play + iOS.

**İndirme → MAU**
Kurulum→aktif dönüşümü sosyal uygulamalarda acımasızdır. Kaba bant:
- İyi ürün: toplam indirmenin %15-25'i MAU
- Ortalama: %5-10
- Terk edilmiş: %1-3
Hangi bandı seçtiğini review temalarına ve son içerik tarihine dayandır, keyfi seçme.

**MAU → DAU**: sosyal üründe DAU/MAU %10 (zayıf) – %25 (iyi) – %50+ (çok iyi).

**Gelir yoksa gelir potansiyeli**: TR'de reklam destekli gençlik uygulamasında yıllık
kullanıcı başı reklam geliri kabaca 0,3–1,5 USD; abonelik dönüşümü %1-3, ay başı 30-80 TL.
Bunlar **potansiyel** hesabıdır, bugünkü değere doğrudan yazılmaz.

## 3. Yöntemler

### A. Yeniden Yapım Maliyeti (Rebuild Cost) — tabanı belirler
"Bu ürünü sıfırdan yeniden yapmak kaça mal olur, ne kadar sürer?"
```
Rebuild = (geliştirici ay sayısı × aylık maliyet) + tasarım + altyapı kurulum
```
TR piyasası referansı (rapor tarihinde güncelle): orta seviye mobil geliştirici tam maliyeti
aylık 90.000–160.000 TL; senior backend 130.000–250.000 TL; freelance ajans ay/adam 100.000–200.000 TL.

Sonra **zaman iskontosu** uygula: alıcı 6 ay kazanıyorsa bu bir değerdir; ama kod devralınabilir
ve bakımı yapılabilir durumda değilse rebuild değerinin %30-50'si silinir.
**Kritik nüans:** rebuild cost bir taban değildir eğer kimse o ürünü yeniden yapmak istemiyorsa.
Talep yoksa taban tasfiye değerine (domain + marka) düşer.

### B. Acquihire (Ekip Değeri)
Alıcı ürünü değil ekibi alıyor. TR'de kişi başı 30.000–120.000 USD; senior/nadir yetkinlikte
üst banda çıkar. Sadece **ekip birlikte geçiyorsa** geçerlidir; kurucular kalmıyorsa bu yöntem düşer.

### C. Kullanıcı Başı Değer (per-MAU / per-user)
```
Değer = Aktif kullanıcı × kullanıcı başı değer
```
Gelirsiz TR sosyal ürünlerinde kaba bant: 0,5–3 USD/MAU. Niş ve yüksek değerli kitlede
(doğrulanmış üniversite öğrencisi, doktor, KOBİ sahibi) 3–15 USD/MAU'ya çıkabilir —
ama bu ancak **kitle gerçekten erişilebilir ve doğrulanmışsa**. Kayıtlı ama ölü kullanıcı 0 eder.

### D. Gelir Çarpanı
```
Değer = ARR × çarpan
```
TR erken aşama SaaS/uygulama, 2025-2026 bandı: **1,5× – 4× ARR**. Büyüme %100+/yıl ve
net retention iyiyse 5-8×'e çıkar. Küçülen gelirde 0,5-1×. Global SaaS çarpanlarını TR'ye
doğrudan taşıma — likidite ve alıcı havuzu çok daha dar, bu tek başına %30-50 iskonto demektir.

### E. SDE Çarpanı (küçük, kârlı işlerde en gerçekçi)
SDE = Sahibe Kalan Kazanç = net kâr + sahibin maaşı + tek seferlik giderler.
```
Değer = Yıllık SDE × 2,0–4,0
```
Küçük mobil/web işleri global marketplace'lerde (Flippa, Acquire.com, MicroAcquire)
tipik olarak **aylık kârın 24-40 katına** işlem görür. TR'de alıcı havuzu dar olduğu için alt uç.
**Kâr yoksa bu yöntem uygulanmaz — çarpan negatif sayıyla çarpılmaz.**

### F. Berkus (gelirsiz erken aşama)
Beş kaleme en fazla belirli bir tavan (klasik olarak her biri 500.000 USD, TR için
gerçekçi tavan 50.000–150.000 USD) atanır:
sağlam fikir · prototip/ürün (teknoloji riskini azaltma) · kaliteli ekip (uygulama riski) ·
stratejik ilişkiler (pazar riski) · ürünün satışı/traksiyon.
Kaba ama gelirsiz şirkette hızlı bir üst sınır verir.

### G. Scorecard (benzer turlarla kıyas)
Bölgedeki benzer aşama ortalama pre-money'yi al, sonra ağırlıklı katsayılarla çarp:
ekip %30, fırsat büyüklüğü %25, ürün/teknoloji %15, rekabet ortamı %10,
pazarlama/satış/kanallar %10, ek yatırım ihtiyacı %5, diğer %5.

### H. Yakım Baskısı İskontosu (satış zorunluysa)
Bu, Türkiye'deki gerçek durumları en iyi açıklayan düzeltmedir ve çoğu rapor atlar.
```
Pist (ay) = Nakit ÷ Aylık net yakım
```
- Pist > 12 ay → iskonto yok
- Pist 6-12 ay → %10-20 iskonto
- Pist 3-6 ay → %25-40 iskonto
- Pist < 3 ay → %40-70 iskonto; fiilen fiyat tasfiye değerine yakınsar

Alıcı bunu bilir. Satıcı tarafındaysan raporun en önemli tavsiyesi budur:
**pisti uzatmadan satışa çıkmak, fiyatı yarıya indirir.**

### I. VC Yöntemi (potansiyel değer için)
```
Bugünkü değer = (Çıkış değeri × başarı olasılığı) ÷ (1 + hedef getiri)^yıl
```
Erken aşamada hedef getiri %40-70/yıl. Bu yöntem **Potansiyel Değer** katmanında kullanılır,
bugünkü fiyat olarak sunulmaz.

## 4. Türkiye erken aşama çarpan bandları (2026 · rapor tarihinde doğrula)

| Aşama | Tipik pre-money |
|---|---|
| Fikir / MVP öncesi | 150.000 – 500.000 USD |
| MVP + ilk kullanıcılar, gelir yok | 300.000 – 1.000.000 USD |
| Erken gelir (<50k USD ARR) | 700.000 – 2.000.000 USD |
| Anlamlı gelir + büyüme | 2.000.000 – 6.000.000 USD |

**Bu bantlar yatırım turu bantlarıdır, satış (M&A) bantları değildir.** Bir startup'ı satın
alan taraf, yatırımcının verdiği değerlemeyi ödemez — genelde onun %30-60'ını öder, çünkü
yatırımcı gelecekteki opsiyonu satın alır, alıcı ise bugünkü varlığı. Bu ayrımı raporda
mutlaka açıkla; kurucular en çok burada hayal kırıklığına uğrar.

## 5. Üç değer katmanı ve senaryolar

Her raporda üçü de çıkar (`SKILL.md` Aşama 8):

1. **Tasfiye/Varlık** — taban
2. **Yürüyen İşletme** — bugün gerçekçi satış fiyatı; **alıcı tipini isimlendir**
3. **Potansiyel (24 ay)** — olasılıkla birlikte

Senaryo tablosu (her senaryoda: varsayım · sonuç değer · olasılık %):

| Senaryo | Ne olursa | Değer | Olasılık |
|---|---|---|---|
| Kötü | Traksiyon durur, para biter | ... | %.. |
| Baz | Bugünkü eğilim devam eder | ... | %.. |
| İyi | Dağıtım kanalı çalışır / gelir başlar | ... | %.. |

Olasılıklar toplamı %100 olmalı. **Beklenen değer** = Σ(değer × olasılık) — bu sayı, tek
bir "net değer" istendiğinde en savunulabilir cevaptır.

## 6. Büyüme Potansiyeli Skoru (1-10, her raporda aynı tanım)

Altı boyut, her biri 1-10, ağırlıklı ortalama:

| Boyut | Ağırlık | 1-3 | 4-6 | 7-10 |
|---|---|---|---|---|
| Pazar büyüklüğü ve erişilebilirliği | %20 | Niş ve doygun | Orta, rekabetli | Büyük ve açık |
| Dağıtım avantajı (kullanıcıya ulaşma yolu) | %25 | Ücretli reklama mahkûm | Karma | Sahip olunan kanal / viral döngü / dağıtım ortaklığı |
| Ürün farkı ve giriş bariyeri | %15 | 3 ayda kopyalanır | Kısmi fark | Ağ etkisi, veri, regülasyon, entegrasyon kilidi |
| Gelir modeli netliği | %15 | Model yok | Test ediliyor | Ödeyen müşteri var, birim ekonomi pozitif |
| Ekip yürütme kapasitesi | %20 | Deneyimsiz, tek kişi | Karma | Alan deneyimi + önceki çıkış + tam kadro |
| Sermaye/pist durumu | %5 | 3 aydan az | 6-12 ay | 12+ ay veya kârlı |

**Dağıtımın en yüksek ağırlıkta olması bilinçlidir.** 2026'da ürün yapmak ucuzladı;
belirleyici olan kullanıcıya sahip olunan bir kanaldan ulaşabilmek.

Skoru raporda **gerekçesiyle** ver, yalın sayı yazma.

## 7. Sık yapılan hatalar

- Yatırım değerlemesini satış fiyatı sanmak (bkz. bölüm 4)
- Kayıtlı kullanıcıyı aktif kullanıcı gibi çarpmak
- Rebuild cost'u talep yokken taban saymak
- TL rakamı tarihsiz yazmak
- Negatif kârı çarpanla çarpmaya çalışmak
- Tek yöntemle tek sayı vermek — aralık ve yöntem çeşitliliği olmadan rapor savunulamaz
- Yakım baskısını fiyata yansıtmamak
- Rakip tablosunu farklı metriklerle doldurup kıyaslanamaz hale getirmek
