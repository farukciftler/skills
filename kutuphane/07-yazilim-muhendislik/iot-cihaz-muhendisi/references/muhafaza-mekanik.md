# Muhafaza ve Mekanik

Faz 5. Kutu, çerçeve, kap — 3D baskıdan seri üretime. Muhafaza bir "kılıf" değil; antenin, termalin, sızdırmazlığın ve ürün algısının parçası.

## İçindekiler
- [1. Muhafaza gereksinim tablosu](#1-muhafaza-gereksinim-tablosu)
- [2. Malzeme seçimi](#2-malzeme-seçimi)
- [3. FDM/SLA tasarım kuralları](#3-fdmsla-tasarım-kuralları)
- [4. Birleştirme: vida, insert, snap-fit](#4-birleştirme-vida-insert-snap-fit)
- [5. Sızdırmazlık ve IP](#5-sızdırmazlık-ve-ip)
- [6. Termal](#6-termal)
- [7. RF ile etkileşim](#7-rf-ile-etkileşim)
- [8. Baskıdan seri üretime geçiş](#8-baskıdan-seri-üretime-geçiş)
- [9. Muhafaza kontrol listesi](#9-muhafaza-kontrol-listesi)

---

## 1. Muhafaza gereksinim tablosu

Modellemeye başlamadan bunları yaz — hepsi geometriyi değiştirir:

| Gereksinim | Soru |
|---|---|
| Ortam | İç mekân / dış mekân / güneş altı / endüstriyel / ıslak? Sıcaklık aralığı? |
| Koruma sınıfı | Toz? Sıçrayan su? Yağmur? Daldırma? (IP hedefi) |
| Erişim | Kaç kez açılacak? Pil değişimi var mı? Servis kim yapacak? |
| Montaj | Duvar / DIN ray / masa / boru kelepçesi / yapıştırma / mıknatıs? |
| Arayüz | Konnektör, buton, LED ışık borusu, ekran penceresi, kablo çıkışı |
| Anten | İçeride mi, dışarıda mı? Metal parça var mı? |
| Termal | Sürekli güç kaybı kaç W? Havalandırma mümkün mü (IP ile çelişir)? |
| Mekanik | Düşme yüksekliği? Titreşim? Basma kuvveti? |
| Görsel | Renk, yüzey, logo, etiket alanı, sertifikasyon işaretleri için yer |
| Hacim | İlk seri kaç adet? 12 ay sonra kaç adet? |

**Sertifikasyon işaretleri için yer ayır.** CE/UKCA/FCC işareti, model adı, seri no, üretici bilgisi ve (kablosuzsa) frekans/güç bilgisi ürüne veya ambalajına gelmek zorunda. Bunu tasarımın sonunda hatırlamak, kalıp değişikliği demektir.

---

## 2. Malzeme seçimi

### FDM filamentleri

| Malzeme | Isı dayanımı | UV/dış mekân | Tokluk | Baskı zorluğu | Nerede |
|---|---|---|---|---|---|
| PLA | Zayıf | Kötü | Kırılgan | Kolay | Sadece görsel prototip. Ürün değil. |
| **PETG** | Orta | Orta | İyi | Kolay-orta | İç mekân muhafazanın varsayılanı |
| ABS | İyi | Orta | İyi | Zor (warp, koku) | PETG'nin ısı sınırını aştığında |
| **ASA** | İyi | **Çok iyi** | İyi | Zor (kapalı hazne + havalandırma şart) | Dış mekân, güneş altı |
| PC | Çok iyi | Orta | Çok iyi | Zor | Yapısal / yüksek sıcaklık |
| Naylon (PA) | İyi | Orta | Mükemmel | Zor (nem emer) | Aşınan/esneyen parça |
| TPU | — | İyi | Elastomer | Orta | **Conta**, tampon, kablo geçidi |

Seçim kuralı: **montajın en zayıf halkasına göre seç.** Duvar malzemesi 100 °C'ye dayansa da içindeki conta, insert veya kablo dayanmıyorsa muhafaza o sınırda çalışır.

ASA'yı "daha endüstriyel duruyor" diye seçme; sadece maruziyet gerektiriyorsa seç — baskısı zordur, ciddi warp yapar, havalandırma gerektirir.

### Reçineler (SLA/DLP)

Yüzey kalitesi ve boyutsal doğruluk üstün; ama çoğu standart reçine kırılgandır ve **UV altında zamanla bozulur**. Görsel prototip ve iç parçalarda iyi; dış kabukta ancak mühendislik reçinesiyle.

### SLS (PA12)

Destek gerektirmez, izotropiye yakın, düşük-orta hacimde (yüzlerce adet) enjeksiyondan önce güçlü bir ara basamak. Yüzey mat/taneli; kozmetik gerekiyorsa post-işlem gerekir.

### Yangın sınıfı uyarısı

Filament üreticisinin ısı deformasyon sıcaklığı, bir **yangın sınıfı (UL 94) beyanı değildir**. Şebeke gerilimiyle çalışan ya da yangın muhafazası gerektiren üründe, muhafaza malzemesinin ilgili sınıfta belgelenmiş olması gerekir; 3D baskı filamentlerinin çoğunda bu belge yoktur. Bu durumda düşük gerilim tarafında kal veya sertifikalı hazır muhafaza kullan.

---

## 3. FDM/SLA tasarım kuralları

**Duvar kalınlığı:** FDM'de nozzle çapının tam katı seçilir (0.4 mm nozzle → 1.6 / 2.0 / 2.4 mm). Küçük muhafazada 2 mm makul varsayılan; conta baskısı taşıyan duvarlarda daha kalın.

**Toleranslar (PCB'yi kutuya oturturken):**
- SLA/SLS: ~0.5 mm boşluk yeterli
- **FDM: 1.0-2.0 mm** boşluk bırak — warp ve ilk katman fil ayağı (elephant foot) yüzünden. Sıkı tasarlanmış FDM kutu, PCB'yi almaz.
- Hareketli/geçmeli parçalarda 0.2-0.5 mm boşluk (esnek malzemede alt sınır, sert malzemede üst sınır).

**Yön (orientation):** katman çizgileri en zayıf düzlemdir. Yükü katmanlara **paralel** değil, dik verecek şekilde yönlendir. Vida bosslarında katman ayrılması en sık kırılma modudur.

**Köşe ve destek:** iç köşelerde radüs (gerilim yığılmasını önler), geniş düz yüzeylerde nervür (rib) — nervür kalınlığı duvarın ~yarısı-üçte ikisi kadar, aksi halde dışarıda çöküntü izi olur. Köşelerde gusset.

**Fil ayağı düzeltmesi:** taban kenarında 0.2-0.4 mm pah (chamfer), oturma yüzeyinin düz kalması için.

**Boss tasarımı:** boss dış çapı ≈ insert dış çapının 2-2.5 katı; tabanına radüs; boss'u duvara nervürle bağla.

**Silkscreen yerine gömme yazı:** model numarası, revizyon ve tarih parçanın içine gömülü yazıyla basılır. Altı ay sonra hangi revizyonun elinde olduğunu bilmenin tek yolu.

---

## 4. Birleştirme: vida, insert, snap-fit

**Sıcak yerleştirmeli pirinç insert (heat-set insert) — servis edilebilir ürünlerde varsayılan.** Doğrudan plastiğe diş açmak veya kendinden kılavuzlu vida kullanmak, 3-5 açma-kapamada dişi sıyırır. Insert, tekrarlı montaja ve tork'a dayanır.

Uygulama:
- Delik çapını insert üreticisinin verdiği ölçüde bırak (genelde insert dış çapından az küçük).
- Havyayı malzemenin akma sıcaklığına uygun ayarla; PETG ve ABS/ASA farklı sıcaklıklar ister.
- Insert yüzeyle aynı hizada veya hafif gömülü otursun; taşarsa kapak oturmaz.
- Konik uçlu özel havya ucu kullan — düz uçla yamuk oturur.

**Snap-fit:** alet gerektirmeyen, sık açılmayan, düşük yük taşıyan kapaklarda iyi. Tasarım parametreleri: kiriş uzunluğu (uzun = düşük gerilim), çıkıntı derinliği (baskıda tipik 0.5-1.0 mm), kiriş kalınlığı. PETG ve naylon esneklik/yorulma açısından uygun; PLA kırılır. FDM'de snap kirişini katmanlara dik yönde bükülecek şekilde konumlandır.

**Vida seçimi:** M2.5/M3 çoğu IoT muhafazası için yeterli. Kapak vidalarını çapraz sırayla ve **eşit** sıkılaştır (özellikle contalı kapakta) — tek taraftan sıkmak conta baskısını dengesizleştirir ve sızdırır.

---

## 5. Sızdırmazlık ve IP

**Önce dürüst ol: 3D basılmış bir muhafazanın IP derecesi yoktur.** IP derecesi, IEC 60529'a göre belirli bir üründe yapılan testin sonucudur; malzemenin veya tasarımın özelliği değil. "IP65 tasarladım" denemez; "IP65 hedefiyle tasarlandı, test edilecek" denir. Ürün iddiası olarak kullanılacaksa akredite testle doğrulanır.

**Sızıntının üç yolu** — üçünü ayrı ayrı çöz:

1. **Kapak dikişi.** TPU veya silikon conta + kanal (groove). Conta kesitinin %15-25 sıkışacağı derinlikte kanal aç. Eşit vida baskısı şart. Basılmış bir yüzeyin katman çizgileri mikro kanal oluşturur — conta bu yüzden düz sızdırmazlık yüzeyine değil, kanala oturmalı.
2. **Kablo girişi — en sık sızıntı noktası.** Kablo rakoru (cable gland) + gerilim azaltma (strain relief). Kabloyu deliğe geçirip silikonla kapatmak sahada 6 ay sonra sızdırır. Sabit kablolarda potting (dolgu) alternatif.
3. **Konnektör, buton, LED penceresi.** Contalı/IP dereceli konnektör kullan; buton için membran veya silikon kapak; pencere için yapıştırma yerine conta + baskı.

**Yoğuşma (condensation) gerçeği:** dış mekânda sızdırmaz bir kutu iç nem yüzünden içeriden ıslanır — gündüz ısınıp gece soğudukça hava içeri çekilir ve nem yoğuşur. Çözümler: nem alıcı paket (kapasitesi sınırlı, servis ister), **basınç dengeleme membranı** (Gore vent tipi — nemi geçirir, suyu geçirmez; doğru cevap), konforlu tarafta koruyucu kaplama (conformal coating) PCB'de.

**Baskı ayarları sızdırmazlığı etkiler:** çevre sayısını (perimeter) artır (4+), katman yüksekliğini düşür, akış oranını kalibre et. Poröz bir duvar, mükemmel bir contayı işe yaramaz hale getirir.

**Test:** su testi öncesi basit bir kaçak testi yap — kutuyu hafif basınçlandırıp suya batır ve kabarcık ara; ya da içine nem indikatörü koyup püskürtme testi uygula.

---

## 6. Termal

Kapalı bir plastik kutunun içinde konveksiyon yoktur. İletim ve ışıma kalır.

**Sıra:**
1. Toplam güç kaybını hesapla (regülatör kaybı + MCU + radyo TX ortalaması + diğer).
2. Kabaca sıcaklık artışını tahmin et (kutu yüzey alanı ve malzeme üzerinden), sonra **ölç** (termokupl veya termal kamera, en kötü senaryoda: maksimum ortam + sürekli TX + kutu kapalı + güneş altındaysa güneş yükü).
3. Sıcak bileşenin izin verilen sıcaklığını datasheet'ten al ve marj bırak.

**Müdahale araçları:** bakır döküm ve termal via (PCB'de), sıcak bileşeni kutu duvarına termal ped ile bağlama, alüminyum plaka/gövde, havalandırma (IP ile çelişir — labirent/membranlı havalandırma dengeler).

**Sık gözden kaçan:** pilin sıcaklık sınırı. Li-ion 45-60 °C üstünde hızla bozulur ve şarj sınırları daralır. Sıcak bileşenin yanına pil koyma.

**ASA/PETG'nin ısı deformasyon sıcaklığı** üründeki gerçek sınır olabilir — özellikle boss'lar, sürünme (creep) yüzünden zamanla vida ön-yükünü kaybeder. Sıcak ortamda uzun süre baskı altında kalan parçalarda buna dikkat.

---

## 7. RF ile etkileşim

Muhafaza antenin bir parçasıdır — mekaniği "sonra tasarlarız" diye bırakmak, RF'i yeniden yapmak demektir.

- **Metal yok** (anten çevresinde). Metalik boya, metalize kaplama, alüminyum plaka, mıknatıslı montaj, metal vida — hepsi anteni etkiler.
- **Plastik dielektrik yükleme** rezonansı aşağı kaydırır. Bu yüzden anteni serbest alanda hedefin biraz üstüne ayarla (2.4 GHz için ~2.50-2.55 GHz), kutuda 2.44 GHz'e otursun.
- **Mesafe**: anten ile kutu duvarı arası ≥ 5 mm hedefle. Duvarın anten üzerine oturması en kötü senaryo.
- **Pil ve ekran** anten yakınında olmaz; pil ≥ 8 mm, metal ekran ≥ 6 mm.
- **Kablolar** antenin yanından geçirilmez; parazitik radyatör olur ve hem menzili hem EMC sonucunu bozar.
- **Doğrulama zinciri**: S11 serbest alanda → kutuda → pil takılı → elle tutulurken. Her adımda kaymayı kaydet.

Detay: `donanim-pcb.md` §5.

---

## 8. Baskıdan seri üretime geçiş

Bu bir "ne zaman" sorusu ve cevabı hacimde.

### Seçenekler ve kaba ekonomi

| Yöntem | Kalıp/kurulum | Birim | Teslim (ilk parça) | Hacim aralığı |
|---|---|---|---|---|
| FDM 3D baskı | 0 | Düşük-orta | Saatler-1 gün | 1-100 |
| SLA/SLS | 0 | Orta | 1-3 gün | 1-300 |
| CNC | 0 (fikstür) | Yüksek | Günler | 1-100 |
| Poliüretan döküm (silikon kalıp) | Düşük (master + silikon) | Orta-yüksek | ~1 hafta | ~20-500 |
| Düşük hacim enjeksiyon (alüminyum kalıp) | Orta | Düşük | 1-4 hafta | 100-10.000 |
| Üretim enjeksiyon (çelik kalıp) | Yüksek | Çok düşük | 4-8 hafta | 10.000+ |

**Kritik nokta: yayımlanmış "başabaş" rakamlarının hepsi parça özelinde değişir.** Genel eşik vermek yerine **hesabı yap**:

```
Başabaş adet = Kalıp maliyeti / (Baskı birim maliyeti − Enjeksiyon birim maliyeti)
```

Örnek: 6.000 USD alüminyum kalıp, baskı 22 USD/parça, enjeksiyon 2 USD/parça
→ 6.000 / 20 = **300 adet**.

Aynı parça 18.000 USD çelik kalıpla → 900 adet. El büyüklüğünde bir muhafazada tipik kırılma noktası birkaç yüz ile birkaç bin adet arasında oynar; yan hareketli (side action), sıkı tolerans veya çok kaviteli kalıp bunu yukarı taşır.

**Karar sadece paradan ibaret değil:**
- **Tasarım kilitlendi mi?** Kalıp açıldıktan sonra değişiklik 500-5.000 USD. Tasarım hâlâ oynuyorsa kalıba geçme.
- **Teslim süresi** — kalıp 1-4 hafta (alüminyum) veya daha uzun; baskı 1 gün.
- **Kozmetik** — enjeksiyon yüzeyi baskıdan çok üstün. Tüketici ürününde bu tek başına belirleyici olabilir.
- **Tutarlılık** — enjeksiyon parçaları birbirinin aynısı; baskıda parça-parça sapma toleransı yönetmelisin.

### DFM: baskıdan kalıba geçerken değişecekler

Enjeksiyon kalıbı bambaşka kurallar ister; baskı modelini olduğu gibi kalıba veremezsin:
- **Tek tip duvar kalınlığı** (çöküntü izi ve çarpılmayı önler)
- **Çıkma açısı (draft)**: her dikey yüzeyde tipik 1-2°, dokulu yüzeyde daha fazla
- **Kalın bölge yok** — kalın yerler nervürlü/oyuk hale getirilir
- **Alttan kesme (undercut) minimizasyonu** — her yan hareket kalıba para ekler
- **Ayrılma çizgisi (parting line)** ve iticinin (ejector pin) izleri kozmetik yüzeye gelmeyecek şekilde konumlandırılır
- **Yolluk (gate) yeri** — akış izi ve birleşme çizgisi (weld line) yerini belirler

Bu geçiş, kalıpçıyla birlikte yapılan bir DFM turudur; tek başına yapılan bir CAD işi değil. Kalıpçıdan **DFM raporu** iste ve T1 (ilk kalıp denemesi) numunelerini geçmeden seri üretime izin verme.

---

## 9. Muhafaza kontrol listesi

Faz 5 kapısı:

- [ ] PCB kutuya **fiziksel olarak** oturdu (3D'de değil, elde)
- [ ] Tüm konnektörler kesitten erişilebilir, kablo bükülme yarıçapı yeterli
- [ ] Butonlar tıklıyor, LED ışık borusu görünür, ekran penceresi hizalı
- [ ] Anten S11'i kutu içinde ölçüldü ve kabul aralığında
- [ ] Pil ve metal parçalar antenden yeterli uzaklıkta
- [ ] En kötü durum termal ölçüldü, tüm bileşenler sınır içinde
- [ ] Insert'ler oturdu, kapak 10 kez açılıp kapandı, diş sağlam
- [ ] Conta baskısı eşit, kaçak testi geçti (IP hedefi varsa)
- [ ] Kablo rakoru + strain relief takılı ve çekme testi yapıldı
- [ ] Düşme testi yapıldı (hedef yükseklikten, en kötü açıyla, 6 yüz)
- [ ] Sertifikasyon işaretleri, model no, seri no için yer ayrılmış
- [ ] Servis/pil değişimi prosedürü denendi ve süresi ölçüldü
- [ ] Montaj sırası belgelendi (fotoğraflı), montaj süresi ölçüldü — birim maliyete girecek
- [ ] Hacim planına göre üretim yöntemi seçildi ve başabaş hesabı yazıldı
