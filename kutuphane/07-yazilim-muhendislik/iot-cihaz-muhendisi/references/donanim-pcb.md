# Donanım ve PCB

Faz 2-3. Şematikten Gerber'e, oradan fab ve dizgi siparişine.

## İçindekiler
- [1. Şematik disiplini](#1-şematik-disiplini)
- [2. Güç ağacı](#2-güç-ağacı)
- [3. Koruma ve dayanıklılık](#3-koruma-ve-dayanıklılık)
- [4. Stackup](#4-stackup)
- [5. RF ve anten](#5-rf-ve-anten)
- [6. Layout disiplini](#6-layout-disiplini)
- [7. DFM ve üretici kısıtları](#7-dfm-ve-üretici-kısıtları)
- [8. BOM, tedarik ve maliyet](#8-bom-tedarik-ve-maliyet)
- [9. EDA aracı](#9-eda-aracı)

---

## 1. Şematik disiplini

Şematikteki her hata layout'a, layout'taki her hata bakıra, bakırdaki her hata 2-4 haftaya dönüşür. Şematik en ucuz düzeltme yeridir — burada acele etmek en pahalı acele.

**Zorunlu alışkanlıklar:**
- Her IC'nin datasheet'indeki **tipik uygulama devresi** yanına açık tutulur; kopyalanan her değer işaretlenir.
- Her besleme pinine decoupling: yakın 100 nF + rayda bulk. Çok pinli IC'de pin başına.
- Kullanılmayan pinler açıkta bırakılmaz; datasheet ne diyorsa (NC / GND / pull) o yapılır.
- Reset ve boot pinleri: pull direnci + test noktası + (gerekiyorsa) buton.
- **Programlama/debug arayüzü** (SWD/JTAG/UART) her zaman konur ve üretim jig'inden erişilebilir olur — pogo pin pad'i olarak. Üretimde bunu unutmak, her kartı elle programlamak demektir.
- Kritik rayların ve sinyallerin **test noktaları**. Kural: bring-up sırasında osiloskop probu değecek her yer bir pad olmalı.
- 0 Ω link ve DNP (do-not-populate) pad'leri: alternatif eşleme ağı, akım ölçüm shunt'ı, izolasyon noktası. Rev A'da cömert ol; Rev B'de temizle.
- **Akım ölçüm noktası**: pil hattına seri 0 Ω / jumper. Bu olmadan güç bütçesini doğrulayamazsın.
- Referans tanımlayıcılar ve değerler baskıda okunabilir; kutup işaretleri (diyot, elektrolitik, konnektör pin-1) silkscreen'de net.

**Review'a girmeden önce:** ERC temiz, tüm net'ler adlandırılmış, güç ağacı çizilmiş, BOM'daki her satırın stok linki var.

---

## 2. Güç ağacı

Bir sayfa çiz: kaynak → koruma → dönüştürücü(ler) → yükler. Her düğümde gerilim, en kötü durum akımı, verim.

**Topoloji seçimi:**

| Durum | Seçim | Neden |
|---|---|---|
| Küçük düşüm (ör. 3.7 V → 3.3 V), düşük akım | LDO | Basit, ucuz, gürültüsüz — RF için iyi |
| Büyük düşüm veya yüksek akım | Buck | LDO'da kayıp ısı olur; 5 V→3.3 V @ 500 mA'da LDO 0.85 W yakar |
| Pil gerilimi hedefin altına düşüyor | Buck-boost | Alkalin/coin cell ömrünün son yarısı |
| Batarya şarjı | Ayrı şarj IC + koruma IC | Li-ion'da pazarlık konusu değil |

**Kritik detaylar:**
- Pilli üründe LDO'nun **I_q**'su seçim kriteridir; datasheet'te "ultra-low quiescent" arayın (< 1-2 µA).
- Buck'ın anahtarlama frekansı ve harmonikleri EMC'de en sık başarısızlık kaynağıdır. Anahtarlama düğümü (SW node) küçük tutulur, giriş kapasitörü IC'ye **mümkün olan en yakın** yerleştirilir, yüksek di/dt döngüsü minimize edilir. Ön-uyum taramasında en çok bu döngü konuşur.
- Ray sıralaması (power sequencing): datasheet ne sırada istiyorsa o. Sıra ihlali latch-up yapar.
- Her rayda **en kötü durum** akımı hesaplanır ve iz genişliği buna göre (IPC-2152 mantığı; sıcaklık artışı hedefiyle) seçilir.

---

## 3. Koruma ve dayanıklılık

Sahaya çıkan cihazda bunlar isteğe bağlı değil:

- **ESD**: kullanıcı erişimli her hatta (USB, konnektörler, butonlar, harici kablolar) TVS diyot. EMC immunity testinde (EN 61000-4-2, kontak ve hava deşarjı) ilk düşen yer burasıdır.
- **Ters polarite**: pil/besleme girişinde P-kanal MOSFET (diyottan verimli) veya ideal diyot.
- **Aşırı akım**: PTC/polyfuse veya eSwitch.
- **Surge/EFT**: kablolu uzun hatlarda (RS-485, güç) EN 61000-4-4/-4-5 için ek koruma.
- **Brown-out**: MCU'nun BOR seviyesi doğru ayarlanır; pil gerilimi düşerken yarım yazılmış flash bırakmaması için.
- **Watchdog**: donanım watchdog aktif; firmware'de "watchdog'u besleyen ayrı task" antipattern'inden kaçın (asıl işi yapan yol beslemeli).

---

## 4. Stackup

| Katman | Ne zaman | Not |
|---|---|---|
| 2 katman | Basit, düşük hız, RF yok veya modül üstünde anten var | Ucuz ama sürekli GND düzlemi zor; EMC riski yüksek |
| **4 katman** | IoT cihazlarının varsayılanı | Sinyal / GND / GÜÇ / Sinyal. Kesintisiz GND düzlemi RF ve EMC'nin yarısını çözer |
| 6+ katman | Yoğun BGA, çok raylı, yüksek hız | Maliyet ve tedarik süresi artar |

4 katman kural: **Katman 2 kesintisiz zemin.** Güç yollarını katman 2'den geçirmek için düzlemi bölmek, tasarımı 2 katmana geri döndürür. Hızlı/hassas sinyalin altında dönüş yolu kırılmamalı.

**Kontrollü empedans:** 50 Ω tek uçlu (RF besleme), 90 Ω (USB), 100 Ω (Ethernet, diferansiyel) gerekiyorsa üreticinin **yayımlanmış stackup'ına göre** iz genişliği hesaplanır — genel formülle değil. Üretici hesaplayıcısını kullan ve stackup'ı fab notunda kilitle. Standart tolerans ±%10; daha sıkısı özel istek ve ek maliyet.

---

## 5. RF ve anten

Menzil şikâyetlerinin ezici çoğunluğu radyo çipinden değil, buradan gelir.

### Anten tipi

| Tip | Alan | Kazanç | Maliyet | Ne zaman |
|---|---|---|---|---|
| Modül üstü anten | 0 (modülde) | İyi | Modül fiyatında | Varsayılan; modül kart kenarından taşar |
| PCB anten (IFA/MIFA) | 15-25 × 5-10 mm | İyi-çok iyi | 0 | Hacim varsa, referans tasarım birebir kopyalanırsa |
| Chip anten | Küçük | Orta | ~0.15-0.60 USD | Yer yoksa; eşleme ağı genelde gerekir |
| Harici (U.FL/SMA) | — | En iyi | Konnektör + anten | Menzil kritik, metal kutu, endüstriyel |

### Değişmez yerleşim kuralları (2.4 GHz)

1. **Anten kart kenarında veya köşede.** Kart ortasında anten, zemin düzlemi tarafından kısa devre edilir.
2. **Keepout: hiçbir katmanda bakır yok.** Anten elemanının altında ve çevresinde tüm katmanlarda boş. İç katmanda "unutulmuş" bir GND dökümü anteni radyatör olmaktan çıkarıp kayıplı iletim hattına çevirir.
3. **Keepout mesafesi**: iç bölgedeyse 2.4 GHz için ~15 mm'den başla; kenardaysa üreticinin referans değerini uygula. Sub-GHz'de (433/868 MHz) 20-25 mm'ye çıkar — dalga boyu büyüdükçe her şey büyür.
4. **Referans tasarımı birebir kopyala.** Espressif/Nordic/SiLabs/Infineon'un Gerber veya DXF'ini al; iz uzunluğunu, genişliğini, boşluk yüksekliğini 0.1 mm hassasiyetle koru. Datasheet resmine bakıp göz kararı çizmek çalışmaz.
5. **Besleme izi**: 50 Ω kontrollü empedans, mümkün olduğunca kısa ve düz, via yok, 90° dönüş yok (45° veya yay).
6. **Zemin düzlemi kenarı** antene en yakın yerde düz ve temiz; çentik/düzensizlik yok. Zemin düzlemi antenin ikinci yarısıdır — yeterli büyüklükte kesintisiz alan bırak.
7. **Via stitching**: zemin kenarı boyunca dikiş vialar, aralık λ/20 mertebesinde (2.4 GHz'de ~6 mm altı).
8. **Eşleme ağı yeri**: π ağı için 3 adet DNP pad (seri + iki şönt) koy. Rev A'da 0 Ω/DNP bırak, ölçüp doldur. Bu pad'ler olmadan detuning'i düzeltemezsin ve respin'e mahkûm olursun.
9. **Mekanik komşuluk**: pil ≥ 8 mm, metal ekran ≥ 6 mm, kutu duvarı ≥ 5 mm uzakta. Kaçınılmazsa yerel zemin moat'ı ekle.
10. **Keepout'u silkscreen'e ve fab notuna yaz.** Altı ay sonra dosyaya dokunan kişi bunu bilmiyor olacak.

### Kutu etkisi ve ölçüm

Plastik muhafaza anteni **aşağı** kaydırır (dielektrik yükleme). Bu yüzden serbest alanda hedefin biraz üstüne (ör. 2.50-2.55 GHz) ayarlamak, kutuda 2.44 GHz'e oturmasını sağlar.

Doğrulama zinciri:
1. NanoVNA ile **S11** ölç — serbest alanda, sonra kutu içinde, sonra pil takılıyken, sonra el/insan yakınken.
2. Rezonans kaydıysa eşleme ağını ayarla (kabaca: seri küçük indüktans frekansı aşağı, şönt küçük kapasitans da aşağı kaydırır).
3. Menzil testi: aynı ortamda referans bir cihazla karşılaştırmalı RSSI. Mutlak sayıdan çok **fark** anlamlıdır.

`test-dogrulama.md`'de ölçüm protokolü var.

---

## 6. Layout disiplini

- **Yerleşim sırası**: önce anten ve konnektörler (mekanik kısıtlı), sonra güç dönüştürücüler, sonra MCU ve çevresi, en son pasifler.
- **Bölgelendirme**: RF bölgesi / analog bölge / dijital bölge / güç anahtarlama bölgesi ayrı; aralarına gürültülü sinyal geçirme.
- **Kristal/osilatör**: MCU'ya en yakın, altında sürekli zemin, çevresinde koruma zemini, altından sinyal geçmez.
- **Dönüş yolu**: her hızlı sinyalin altında kesintisiz referans düzlemi. Düzlem bölünmesini geçmesi gerekiyorsa dikiş kapasitörü/via ile köprü kur.
- **Termal**: güç bileşenlerinin altına termal via dizisi ve bakır döküm. Kapalı kutu içinde konveksiyon yoktur — hesaba kat (`muhafaza-mekanik.md`).
- **Montaj delikleri**: 3D modelde kutuyla birlikte kontrol et; PCB'yi kutuya sığdırmak Rev A'daki en sık mekanik hata.
- **Fiducial** işaretler: dizgi yaptıracaksan zorunlu (kart köşelerinde 3 adet asimetrik).
- **Panelizasyon**: küçük kartta v-cut/mouse-bite paneli dizgi maliyetini ciddi düşürür; üreticiden panel kurallarını al.
- **3D kontrol**: layout bitince kartı 3D'de kutu modeliyle birleştir ve çarpışma kontrolü yap. KiCad 10 varsayılan olarak STEP modelleriyle geliyor — kullan.

---

## 7. DFM ve üretici kısıtları

**Kural: kendi tasarım kurallarını, sipariş vereceğin üreticinin yayımlanmış yeteneklerine göre ayarla ve sipariş öncesi o sayfayı yeniden oku.** Yetenekler ve fiyatlandırma eşikleri değişiyor.

Tipik prototip/orta hacim fab (JLCPCB sınıfı) referans değerler — **sipariş öncesi doğrula**:

| Parametre | Tipik değer |
|---|---|
| Min iz/boşluk, 1 oz, 1-2 katman | 0.10-0.127 mm (4-5 mil) |
| Min iz/boşluk, 1 oz, çok katman | 0.09 mm (3.5 mil), BGA fan-out'ta 3 mil |
| Min iz/boşluk, 2 oz | ~0.16 mm (6.5 mil) |
| Min via deliği | 0.2 mm (çok katmanda daha küçüğü özel) |
| Min annular ring (via) | ~0.13 mm |
| Empedans toleransı | ±%10 standart, ±%5 özel istek |
| Katman-katman kayıt | ~±0.13 mm |
| Kenar-özellik kaydı | ~±0.25 mm |

**Sınırda tasarlama.** Min değer "üretilebilir" demektir, "yüksek verimle üretilebilir" demek değil. 3.5 mil yerine 5 mil kullanmak, aşındırma sırasında iz incelmesi (necking) riskini ve tarama sonrası ret oranını düşürür.

**Ne zaman butik üreticiye geçilir:** ±%5'ten sıkı empedans (TDR kuponuyla), HDI/mikrovia, Rogers/PTFE, rigid-flex, via-in-pad, IPC Class 3, 6+ katman, yüksek hacimde tutarlı verim ihtiyacı.

**Dizgi (assembly) için:**
- Üreticinin parça kütüphanesinden (basic/extended) seçmek kurulum ücretini düşürür; extended parça başına ek ücret alınır.
- BOM + CPL (pick and place) dosyalarını üreticinin şablonuna göre üret; dönüş açısı (rotation) hatası en sık dizgi hatasıdır — ilk seride kutup kontrolü yap.
- Elle dizilecek/hassas parçaları (konnektör, pil tutucu) ayır.
- Stencil: 0.4 mm pitch altı için step stencil veya azaltılmış açıklık gerekebilir.

**Rev A için sipariş adedi:** 5-10 kart, en az 5 dizili. Tek kartla bring-up yapmak, tek bir yanlış lehimin günlerini yakmasına davetiye.

---

## 8. BOM, tedarik ve maliyet

**BOM hijyeni:** her satırda üretici parça numarası (MPN), üretici, tedarikçi, hedef hacimde fiyat, stok durumu, **ikinci kaynak**, ömür durumu (NRND/EOL kontrolü), paket, tolerans/gerilim/sıcaklık sınıfı.

**Risk sınıflandırması:**
- 🔴 Tek kaynak + uzun tedarik süresi + yüksek fiyat → tasarım riski. Alternatif ayak izi (dual footprint) düşün.
- 🟡 Tek kaynak ama ikame kolay
- 🟢 Çoklu kaynak, geniş stok

**Maliyet modeli (birim, hacme göre):**

```
Birim maliyet = PCB + bileşenler + dizgi + muhafaza + montaj işçiliği
              + test süresi + ambalaj + fire payı (%2-5)
NRE (tek seferlik) = tasarım + prototip iterasyonları + stencil
              + kalıp (varsa) + test jig'i + sertifikasyon
```

Sertifikasyon NRE'si küçük hacimde birim maliyeti domine eder — 1000 adette 15.000 USD sertifikasyon = adet başına 15 USD. Fiyatlandırma konuşulacaksa bunu hesaba kat.

**Hacim eşikleri (kaba):**
- < 100 adet: elle/az sayıda dizgi, prototip fab, 3D baskı muhafaza
- 100-1.000: panelize fab + otomatik dizgi, 3D baskı veya poliüretan döküm muhafaza
- 1.000-10.000: enjeksiyon kalıbı ekonomik olmaya başlar, üretim test jig'i şart
- 10.000+: sertleştirilmiş kalıp, tam otomatik test, ikinci kaynak zorunlu

---

## 9. EDA aracı

**KiCad 10** (ilk sürüm Mart 2026; 10.0.x bakım sürümleri devam ediyor) IoT cihaz sınıfı işlerin tamamı için yeterli ve ücretsiz:
- Grafik DRC kuralı editörü (özel kuralları elle yazmadan)
- Zaman alanında iz ayarlama (time-domain tuning) ve katman başına tuning profilleri
- Component Classes — referans/kütüphane/yön/alan içeriğine göre dinamik sınıflandırma; RF veya güç izlerine otomatik kural uygulamak için kullanışlı
- PCB Design Blocks — tekrar kullanılabilir yerleşim blokları (ör. standart güç bölümü, standart RF ön ucu)
- İç katman nesneleri footprint içinde — **anten keepout'unu footprint'e gömmek için** birebir bunu kullan
- STEP varsayılan 3D formatı; mekanikle çakışma kontrolü daha doğru
- Altium, CADSTAR, EasyEDA (JLCEDA), Allegro, PADS, Eagle, gEDA içe aktarma

Ticari araca geçme sebebi genelde takım işbirliği, gelişmiş SI/PI simülasyonu veya kurumsal kütüphane yönetimidir — tek kişilik/küçük ekipte gerek yok.

**Sürüm kontrolü:** KiCad dosyaları metin tabanlı; git kullan. `.kicad_pcb`, `.kicad_sch`, `.kicad_pro` versiyonlanır; üretim çıktıları (`gerbers/`, `bom/`) etiketli sürüm klasörlerinde tutulur. Her fab siparişi bir git tag'ine karşılık gelmeli — hangi kartın hangi dosyadan çıktığını 6 ay sonra bilmenin tek yolu bu.
