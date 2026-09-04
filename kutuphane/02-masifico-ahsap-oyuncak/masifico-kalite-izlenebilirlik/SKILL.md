---
name: masifico-kalite-izlenebilirlik
description: Masifico'nun kalite kontrol ve izlenebilirlik sistemi — gelen kereste kabul kriterleri (nem, sınıf, ret kusurları), proses içi ve son kontrol listeleri, 25 kodlu kusur sınıflandırması, parti büyüklüğüne göre doğru örnekleme kararı (küçük partide %100 kontrol), EN 71-1 atölye ön-testleri (küçük parça silindiri, 50/90 N çekme, 0,34 Nm tork, 850 mm düşürme, ıslatma testi), NCR/CAPA döngüsü, altın numune pratiği; ve bunların hepsini parti numarasına bağlayan izlenebilirlik zinciri — hammadde lotu → kimyasal lotu → operatör → QC sonucu → hangi müşteriye gitti. Ayrıca şikâyet/kaza sicili ve geri çağırma duyurusu üretimi. Kullanıcı "kalite", "QC", "kontrol", "kusur", "hatalı çıktı", "ret oranı", "zayiat", "fire", "numune kabul", "nem ölçtüm", "kereste geldi", "AQL", "örnekleme", "kaç adet bakayım", "parti no", "izlenebilirlik", "geri çağırma", "şikâyet geldi", "müşteri kırıldı diyor", "kıymık", "çatlak", "altın numune" dediğinde; bir parti üretime girerken veya biterken; fasondan mal geldiğinde; müşteri şikâyeti ulaştığında; veya sevkiyat öncesi son kontrolde bu skill'i kullan. QC geçmeyen parti sevk edilmez; kritik kusurda şartlı kabul verilmez.
---

# Masifico Kalite Kontrol & İzlenebilirlik

İki işi tek sistemde birleştirir: **kaliteyi ölçmek** ve **ölçüleni partiye bağlamak**. İkincisi olmadan birincisi kanıt üretmez — piyasa gözetimi kapıyı çaldığında "biz kontrol ediyoruz" demek yetmez, hangi partide ne ölçtüğünü göstermen gerekir.

Zincirdeki yeri: `masifico-tedarik-rfq` (malzeme gelir) → **bu skill** (kabul eder, üretimi denetler, partiye bağlar) → `masifico-teknik-dosya` (kanıtı dosyaya taşır).

## 0 · Beş kural

1. **QC geçmeyen parti sevk edilmez.** `parti.py` bunu koda gömer — `qc.gecti != True` ise sevk komutu hata verir (numune hariç).
2. **Kritik kusurda şartlı kabul (concession) YOKTUR.** Major/minor kusurda yazılı onayla verilebilir; güvenlik kusurunda asla.
3. **Parti sınırı dört şeye bağlıdır:** hammadde lotu, kimyasal (yağ/tutkal/boya) lotu, fason atölye, operatör. Bunlardan biri değişirse **yeni parti açılır.** Sınır doğru çizilirse bir sürpriz tek partiyle sınırlanır; yanlış çizilirse tüm üretim tarihçesi geri çağrılır.
4. **Örnekleme küçük partide yanlış araçtır.** ISO 2859-1 *sürekli lot serisi* için tasarlandı. 30'luk partide AQL 2,5 planı 5 adet baktırır ve gerçekten %10 hatalı bir partiyi **%57 olasılıkla geçirir**. Masifico kuralı: **N ≤ 50 → %100 kontrol.**
5. **Ölçüm kaydedilmezse yapılmamıştır.** Nem okuması, mastar sonucu, red adedi `partiler.json`'a yazılır; denetçi boş alanı hata sayar.

## 1 · Gelen kereste kabul (IQC)

`qc.py` içindeki sabitler bağlayıcıdır.

| Ölçüm | Kriter |
|---|---|
| **Nem** | Hedef **%8-10**; kabul bandı **%7-12** (dışı RET). Parti içi yayılım (max−min) **≤2 puan** — dağınık nem, partinin farklı parçalarının farklı çalışması demektir |
| **Nem ölçüm yöntemi** | Pinli direnç ölçer, **kayına ve sıcaklığa kalibre**; en az **10 parça × 3 nokta**; uçtan **≥300 mm** içeriden (uçlar hep daha kurudur); pinler kalınlığın ~1/3'üne, lif yönüne paralel. Ortalama + min + max **birlikte** kaydedilir — yalnız ortalama yanıltır |
| **Düzlük** | 1 m'de sapma ≤2 mm |
| **Sınıf** | 1. sınıf: **budaksız ve ARDAKSIZ**, renk uyumlu. Kayında kaliteyi belirleyen budak sayısı değil **renk ve ardaktır** |
| **Kabul edilemez kusurlar (pazarlık yok)** | çürük · mavi renklenme · kırmızı öz (red heart) · **böcek deliği (tek delik bile parti reddi)** · uç çatlağı >50 mm · boy çatlağı · halka ayrılması · reaksiyon odunu · metal kalıntı · kimyasal işlem beyanı olmayan parti |
| **Parti reddi eşiği** | Reddedilen tahta oranı **>%5** → partinin tamamı reddedilir |
| **Teslim sonrası** | Atölyede **≥7 gün iklimlendirme**, sonra nem TEKRAR ölçülür; ikinci ölçüm de bantta olmalı |

**Fırın kurutma doğrulaması:** tedarikçiden kurutma kaydı iste (çıkış nemi, program, kondisyonlama yapıldı mı). Şüphede kesin yöntem EN 13183-1 (fırın kurutma, (103±2) °C, `MC% = (m₁−m₀)/m₀ × 100`).

**Case hardening (kabuk sertleşmesi) testi:** parçadan çatal şeklinde kesit al; dişler içe/dışa kıvrılıyorsa iç gerilim vardır → torna/kesimde parça oynar, sonradan çarpılır. **"Nemi doğru ama kötü kurutulmuş" keresteyi yakalayan tek pratik testtir** ve fason torna hatalarının gizli nedenidir.

## 2 · Kusur sınıflandırması

`qc.py::KUSURLAR` — 25 kod, tek doğruluk kaynağı. Mantık:
- **KRİTİK:** yaralanma riski veya ürünü yasa dışı kılan kusur. Tolerans yok.
- **MAJOR:** işlevi/dayanımı bozan veya müşterinin iade edeceği kusur.
- **MINOR:** standarttan sapma; işlev ve güvenlik etkilenmiyor.

Ahşap oyuncakta **en sık kritik kusur kıymıktır** (DEF-03) ve çoğu zaman QC'de değil müşteride ortaya çıkar — sebebi §3'teki lif kaldırma adımının atlanmasıdır.

Sınıf kayması yaratan üç durum: yüzey zımpara izi normalde MINOR'dır ama **dokunuşta kıymık riski varsa KRİTİK**; tutkal artığı MINOR'dır ama **yağlanacak yüzeydeyse MAJOR** (yağ tutmaz, leke yapar); çarpılma MAJOR'dır ama **denge taşında işlevi bozuyorsa KRİTİK** (üründe işlev = güvenlik).

## 3 · Proses içi kontrol (IPQC)

**Zımpara sırası: 120 → 180 → 220.** Kum atlanmaz — 120'den 220'ye geçilirse P120 izleri yağ altında ortaya çıkar. Yağlanacak yüzeyde son kum 220; kayında **P320 üstü kontrprodüktiftir** (gözenekleri kapatır, yağ emmez, leke yapar).

**Lif kaldırma (grain raising) — atlanırsa müşteride kıymık çıkar:** P180'den sonra yüzey **hafif nemli bezle silinir → 30-60 dk kurutulur → P220 ile hafifçe geçilir.** Bu adım atlanırsa yağ sürüldüğü anda lifler kalkar; ürün QC'yi geçer, müşteride tüylenir. Ahşap oyuncakta 1 numaralı gizli kritik kusur mekanizması budur.

**Kıymık kontrolü — naylon çorap testi:** ince naylon çorabı ele geçirip tüm yüzeylerde, özellikle kenar/köşe/delik ağzında hafif baskıyla gezdir. **Tek bir takılma bile → parça zımparaya geri döner.** İki kez uygulanır: **yağdan önce** (düzeltilebilir) ve **kür sonrası** (kalkan lifi yakalar). Standart hükmü değil, ama elle taramadan daha hassastır.

**Pah/radyüs:** tüm erişilebilir kenar ve köşeler, **%100 parça, istisna yok** (EN 71-1 md. 4.6/4.7). Hedef min **R1,5-2 mm**; pah genişliği sapması ≤±0,3 mm. Üç yüzün birleştiği köşe **nokta kalmaz, küreselleşir**.

**Yağ kürü:** fazlası **10-20 dk içinde** silinir (kalırsa yapış yapış kürlenir). Dokunma kuruluğu 8-12 saat, ikinci kat 12-24 saat, **tam kür 7-14 gün**. Ambalajlama ve **EN 71-3 numunesi bu süreden önce alınmaz** — süreler yağın kendi TDS'inden doğrulanır; atölye 15 °C ise süre katlanır.

**Kuru film kontrolü:** beyaz kâğıt testi (24 saat ağırlıkla bastır, lekelenmemeli) · su damlası (boncuklanmalı, koyu leke bırakmamalı) · beyaz bezle silme (**bezde transfer varsa EN 71-3 riski**) · koku (keskin solvent kokusu = kürlenmemiş).

**Ağırlık kontrolü küçük seride en verimli QC aracıdır:** set ağırlığı nominal ±%5. Tek tartımla eksik parça + yanlış parça + nem sapması + fazla yağ birikimi taranır.

## 4 · Örnekleme kararı

```
~/masifico-venv/bin/python uretim/parti/qc.py plan --adet 30
~/masifico-venv/bin/python uretim/parti/qc.py karar --adet 30 --kritik 0 --major 1 --minor 2
```

| Parti | Yöntem |
|---|---|
| **N ≤ 50** | **%100 kontrol.** Örnekleme yok. Her parça zaten elden geçiyor; ek maliyet ayrı QC istasyonunda 30-60 sn/adet ≈ 15-30 dk/parti |
| **51-150** | %100 görsel/dokunsal **+** ölçü/ağırlık/mastar için AQL 1,0 örneklemesi |
| **N > 150** | ISO 2859-1 Seviye II tam örnekleme + kritikte %100 tarama |

**AQL politikası:** kritik **0** · major **1,0** · minor **2,5**. Sektör standardı 0/2,5/4,0'tır; premium fiyat bandı ve yüksek iade maliyeti nedeniyle sıkılaştırılmıştır.

**%100 kontrolde Ac/Re uygulanmaz** — kusurlu parça ayrılır, parti reddedilmez. Parti ancak **kritik kusur** varsa karantinaya alınır. Örneklemede ise Ac/Re bağlayıcıdır.

**Tablo tuzağı:** AQL sıkılaştıkça örnek küçülebilir (lot 26-50 / Sev. II: AQL 2,5 → n=5, AQL 4,0 → n=13). Hata değil, ok mimarisinin sonucu. Ayrıca ok, örnek büyüklüğünü de değiştirir — okun gösterdiği **harfin** n'i kullanılır; piyasadaki hesaplayıcıların çoğu bunu düzleştirir ve gerçek riski bozar.

## 5 · EN 71-1 atölye ön-testleri

**Lab testinin yerine geçmez.** Amaç: laba giden numunenin ilk denemede geçmesi ve seri üretimde sapmanın yakalanması.

| Test | Parametre |
|---|---|
| Küçük parça silindiri | Ø**31,7** mm · derinlik **25,4-57,1** mm · eğim 45° · **<36 ay** ürünlerde |
| Çekme | en büyük boyut **>6 mm → 90 N**; **≤6 mm → 50 N**. Kuvvet **5 s**'de kademeli, **10 s** tutulur |
| Tork | **0,34 Nm** · 5 s'de rampalanır · **180° dönme VEYA** 0,34 Nm — hangisi önce · 10 s tutulur |
| Düşürme | **(850±50) mm** · **5 düşürme** (≤14 yaş), **10 düşürme** (≤18 ay) · zemin **4 mm çelik + 2 mm Shore A (75±5) kaplama** |
| **Islatma (md. 8.9)** | Ahşap oyuncakta **ZORUNLU ve mekanik testlerden ÖNCE**. Demineralize su **(21±5) °C**, **4 dk** daldır → silkele → **10 dk** bekle → **4 çevrim** → hemen ardından tork/çekme/düşürme |

**Zincir kritik:** test sonrası kopan her parça **silindire sokulur**. Yani silindir testi tek başına değil, çekme/tork/düşürme/ıslatma sonrasında da uygulanır.

**Ekipman:** silindiri torna ile yaptır (~500-1.500 TL) — 3D baskıda delik tipik 0,2-0,4 mm **dar** çıkar ve dar silindir "sığmadı, geçti" diyerek **yanlış GEÇTİ** verir. Kuvvet ölçer olarak 200 N ±%1 pik modlu analog cihaz yeterlidir; 100 N'lik cihaz 90 N'de skalanın sınırındadır. Tork için moment kolu + 347 g ağırlık, dijital torkmetreden hem ucuz hem izlenebilirdir (dijital torkmetrelerin tabanı genelde 1,5 Nm'dir, 0,34'e **inmez**). **Keskin kenar/uç test cihazı ALINMAZ** — EN 71-1 Ek A.8 uyarınca yalnız metal ve cam için geçerlidir.

## 6 · NCR ve CAPA

**NCR (uygunsuzluk raporu) zorunlu alanları:** ncr_no · tarih · tespit aşaması · sku · **parti_no** · lot adedi · kontrol edilen adet · kusurlu adet · **kusur kodu + sınıfı** · **fotoğraf (zorunlu — fotoğrafsız NCR kapanmaz)** · ölçülen/şartname değeri · tedarikçi · sorumluluk · karar (yeniden işle / onar / ikinci kalite / hurda / tedarikçiye iade / şartlı kabul) · maliyet · kök neden · düzeltme · düzeltici faaliyet · etkinlik doğrulama · durum.

**Kural:** kusur sınıfı KRİTİK ise karar asla `şartlı kabul` olamaz ve CAPA zorunludur.

**CAPA yalnızca üç durumda açılır:** (a) kritik kusur, (b) aynı major kusur iki partide üst üste, (c) kalitesizlik maliyeti eşiği aşıldı. Geri kalanı NCR + düzeltme ile kapanır. **Aynı anda 3'ten fazla açık CAPA = hiçbiri bitmez.**

**Kök neden, ahşap atölyesinde neredeyse her zaman şu altıdan biridir:** nem · zımpara sırası/kum atlama · mastar aşınması · fason tolerans kayması · yağ kür süresi · dikkat/eğitim. Ishikawa/FMEA gerekmez; **5-Neden 30 dakikada biter.**

**İyi CAPA fiziksel/prosedürel bir değişikliktir** (yeni mastar, kızak/fikstür, kontrol adımı, tedarikçi şartnamesi). **"Daha dikkatli olunacak" CAPA değildir** — asla işe yaramaz.

**Etkinlik doğrulama:** sonraki **3 partide** aynı kusur kodu tekrar etmediyse CAPA kapanır; ettiyse kök neden yanlıştı, yeniden açılır.

**Metrikler:** FPY ≥%90 · hurda ≤%2 · yeniden işleme ≤%8 · parti reddi ≤%5 · **kritik kusur %0 (hedef ve eşik aynı)** · DPU ≤0,15. Ret oranı %10'u aşarsa maliyet motorundaki `ZAYIAT = 0.08` varsayımı gerçeği tutmuyor demektir — güncelle. **Yeniden işleme dakikaları mesai gölge maliyetine eklenir**, yoksa "nakit kârlı ama mesai yanıyor" hatası tekrarlanır.

## 7 · Altın numune

Her SKU için onaylanmış **fiziksel referans set** — "kabul edilebilir kalite" tartışmasını sözden nesneye taşır. **3 kopya:** atölye QC masası · kilitli arşiv (master, kullanılmaz) · fason tedarikçi (sözleşme ekidir).

**Prototipten değil, ilk SERİ partinin çıktısından** oluşturulur. Etiketi: SKU, sürüm, onay tarihi, onaylayan, **"ALTIN NUMUNE — SATILAMAZ"**.

**Sınır numuneleri (limit samples)** yanında durur: en koyu ve en açık kabul edilebilir renk, kabul edilebilir maksimum budak, ve **reddedilen** bir örnek. Bu, renk/budak gibi MINOR kusurların öznel tartışmasını bitirir.

Yağ zamanla koyulaşır → **altın numune yılda bir yenilenir**, eski master arşivde kalır.

## 8 · İzlenebilirlik zinciri

**Parti no:** `MSF-<SKU>-<YYYY>W<WW>-<NN>` (örn. `MSF-DT10-2026W34-01`).

Her parti kaydında: hammadde lotu (tedarikçi + irsaliye + lot + nem ölçümü) · kimyasal lotlar (ürün, marka, lot, **SDS yolu**, **EN 71-3 rapor no**) · fason atölye · operatör · QC sonucu · AT Uygunluk Beyanı no · teknik dosya sürümü · **sevkiyat[] (kanal, müşteri, sipariş no, tarih, adet)**.

**Saklama:** teknik dosya + beyan **10 yıl** (arz tarihinden); tedarik zinciri kayıtları 10 yıl; şikâyet sicilindeki **kişisel veri en fazla 5 yıl** (otomatik anonimleştirme).

**Kanal ayrımı önemli:** kreşte müşteri faturada bellidir, geri çağırma tek telefonla biter. Trendyol/Etsy'de tüketici verisi platformdadır — **platform sipariş numarası ile parti numarasının eşleşmesini kendi tarafında tut**, yoksa kitlesel duyuruya mecbur kalırsın (pahalı ve marka için yıkıcı).

## 9 · Şikâyet, kaza, geri çağırma

```
sikayet.py ac --kanal etsy --sku DT10 --parti MSF-... --ozet "..." --ciddiyet ...
geri_cagirma.py olaylar/OLAY-....json     # TR + AB duyurusu + müşteri listesi
```

**Ciddiyet "ölüm" veya "ciddi sağlık etkisi" ise:** GPSR Md. 20 kaza bildirimi **Safety Business Gateway**'e "without undue delay" (AB Sorumlu Kişi üzerinden) + Oyuncak Yön. Md. 5(8) uyarınca **hemen Ticaret Bakanlığı ÜGD'ye** bildirim. Bildirim ürün tipini ve **parti numarasını** içerir.

**Geri çağırma duyurusunda yasak dil:** "gönüllü", "tedbiren", "nadiren", "kaza bildirilmedi" — GPSR Md. 36(2)(c) riski küçülten ifadeleri yasaklar. `geri_cagirma.py` bunları reddeder.

**Telafi:** TR (7223 Md. 19/3) en az **bir**, AB (GPSR Md. 37) en az **iki** seçenek ister — AB'ye satıyorsan bağlayıcı taban AB'dir. Tüm masraflar işletmecidedir; tüketici kargo bile ödemez.

**Finansal gerekçe:** 7223 Md. 21(1) — yetkili kuruluş talep etmeden **kendiliğinden** düzeltir ve uygunsuzluğu tamamen giderirsen **idari yaptırım uygulanmaz**. 2026 ceza bandı 60.830 – 4.345.058 TL. İyi parti kaydının parasal karşılığı budur.

## Dosyalar

```
uretim/parti/
├── parti.py            ← parti aç / QC işle / sevk / arz (QC geçmeden sevk YOK)
├── qc.py               ← örnekleme planı · kusur kodları · kabul-ret · eşikler
├── sikayet.py          ← şikâyet ve kaza sicili (5 yıl kişisel veri kuralı)
├── geri_cagirma.py     ← TR (7223) + AB (GPSR) duyurusu + müşteri listesi
├── parti_kontrol.py    ← DENETÇİ: izlenebilirlik zinciri + etiket + DPP hazırlığı
├── partiler.json       ← parti kayıt defteri (tek doğruluk kaynağı)
└── dpp_hazirlik.json   ← 2030 Dijital Ürün Pasaportu veri toplama takibi
```
