# Mimari Seçim

Faz 1. Bu dosya, şematiğe başlamadan önce kilitlenmesi gereken kararları kapsar: hangi radyo, hangi MCU, hangi paket (modül mü çip mi), hangi RTOS, hangi pil, ne kadar güç.

## İçindekiler
- [Karar sırası](#karar-sırası)
- [1. Bağlantı teknolojisi](#1-bağlantı-teknolojisi)
- [2. Modül mü çıplak çip mi](#2-modül-mü-çıplak-çip-mi)
- [3. MCU/SoC seçimi](#3-mcusoc-seçimi)
- [4. Güç bütçesi ve pil](#4-güç-bütçesi-ve-pil)
- [5. RTOS ve SDK](#5-rtos-ve-sdk)
- [6. Edge AI / TinyML](#6-edge-ai--tinyml)
- [7. Mimari karar kaydı şablonu](#7-mimari-karar-kaydı-şablonu)

---

## Karar sırası

Sıra önemli — tersine çevirmek pahalıya patlar:

1. **Kullanım senaryosu → veri profili.** Ne kadar veri, ne sıklıkta, hangi yöne, ne gecikmeyle?
2. **Menzil ve topoloji** → bağlantı teknolojisi ailesi
3. **Güç kaynağı** (şebeke / pil / enerji hasadı) → izin verilen ortalama akım
4. **Hedef pazarlar** → regülasyon rejimi → modül vs çip kararı (bkz. `regulasyon.md`)
5. **Bağlantı + güç + regülasyon** → MCU/SoC/modül kısa listesi
6. **MCU** → RTOS/SDK, flash haritası, OTA stratejisi
7. Ancak şimdi şematik

---

## 1. Bağlantı teknolojisi

### Seçim mantığı

Önce **kim ödüyor** sorusunu sor: abonelik ücreti taşıyabilen bir iş modeli var mı? Yoksa lisanssız bant (BLE/Wi-Fi/LoRaWAN) zorunludur.

Sonra **altyapı kimin**: kullanıcının Wi-Fi'ı mı (kurulum sürtünmesi + destek yükü), senin gateway'in mi (donanım maliyeti + kurulum), operatörün mü (abonelik + kapsama riski)?

### Karşılaştırma

| Teknoloji | Menzil | Veri hızı | Pil | Abonelik | Ne zaman |
|-----------|--------|-----------|-----|----------|----------|
| **BLE** | 10-100 m | <2 Mbps | Çok iyi | Yok | Telefonla eşleşen giyilebilir, beacon, yakın alan sensör |
| **Wi-Fi (2.4 GHz)** | 30-50 m iç mekân | Yüksek | Zayıf | Yok | Şebeke beslemeli, yüksek veri, gateway istemeyen |
| **Thread / Zigbee (802.15.4)** | Mesh, ~100 m atlama | <250 kbps | Çok iyi | Yok | Akıllı ev, çok düğümlü, border router var |
| **Matter** | (üstteki üçünün üstünde uygulama katmanı) | — | — | Sertifikasyon ücreti | Apple/Google/Amazon ekosistemine girmek şartsa |
| **LoRaWAN** | 2-15 km | 0.3-50 kbps, ~50 B payload | En iyi | Yok (kendi gateway'in) | Kampüs/tarla/saha, kendi ağını kurabiliyorsan |
| **NB-IoT** | Operatör kapsaması | 20-60 kbps | İyi | Var, düşük | Sabit sayaç, bodrum/iç mekân penetrasyonu kritik |
| **LTE-M (Cat-M1)** | Operatör kapsaması | ~300 kbps | Orta | Var | Hareketli varlık, handover gerekli, daha çok veri |
| **Uydu (LEO)** | Global | 1-5 kbps | Zayıf | Yüksek | Kapsama olmayan yer: denizcilik, boru hattı |

Notlar:
- LoRaWAN'da **duty-cycle limiti** var (EU868'de bant başına). Raporlama sıklığı hesabını buna göre yap, yoksa cihaz susmaya başlar.
- NB-IoT/LTE-M'de pil ömrü **PSM ve eDRX**'in doğru kurulmasına bağlı. Bunlar kapalıysa "yıllarca gider" iddiası çöker; modem attach akımı bütçeyi domine eder.
- 2G/3G üzerine yeni tasarım yapma — çoğu operatörde kapandı veya kapanma takviminde.
- Matter'ın kendisi radyo değil; Wi-Fi, Thread veya Ethernet üzerinde çalışan uygulama katmanı. Matter kararı, altındaki taşıyıcının da ayrıca sertifikalanmasını gerektirir (Bluetooth SIG + Thread Group veya Wi-Fi Alliance). Bu maliyet kalemini baştan bütçele.

### Matter'a girerken bilinmesi gerekenler

- Sürüm hattı hızlı ilerliyor: 1.4 (Kas 2024, enerji/pil/ısı pompası), 1.4.1 (NFC onboarding), 1.4.2 (güvenlik, router'lar için Thread 1.4), 1.5 (Kas 2025 — kamera, kapı zili, kepenk/panjur, toprak sensörü), 1.5.1 (Mar 2026), 1.6 (Haz 2026). **Hangi sürümün hangi cihaz tipini kapsadığını canlı doğrula.**
- CSA üyeliği + Vendor ID gerekir; taşıyıcı teknolojinin ayrı sertifikası (DCP attestation) istenir.
- Ürün başına maliyet + yıllık üyelik maliyetleri toplamı ciddidir; tek ürünlü bir startup için BLE-only yolu çok daha ucuzdur. **Güncel ücretleri CSA'dan doğrula, ezberden verme.**
- CSA'nın platform sertifikasyonu / Rapid Recertification programları türev ürünlerde maliyeti düşürüyor; ürün ailesi planlıyorsan bunu araştır.

---

## 2. Modül mü çıplak çip mi

Bu kararın gerekçesi teknik değil, **regülasyon ve takvim**.

**Ön-sertifikalı modül** (ESP32-WROOM, nRF52840 modülü, Quectel modem vb.):
- Kasıtlı yayıcı (intentional radiator) sertifikası modül üreticisinde. Senin cihazın FCC tarafında yalnız kasıtsız yayıcı testine kalır.
- Tipik olarak günler-haftalar ve 5 haneli dolar tasarrufu.
- Anten tasarımı, RF layout ve eşleme riski ortadan kalkar.
- **Ama koşullar var:** modülün grant'ındaki anten tipi/kazancı ve kullanım koşulları dışına çıkarsan avantaj sıfırlanır ve tam sertifikasyona düşersin. Grant metnini oku, varsayma.

**Çıplak çip:**
- Birim maliyet daha düşük (hacimde anlamlı), kart daha ince, tasarım özgür.
- Karşılığında: RF layout uzmanlığı, anten eşleme (NanoVNA + eşleme ağı iterasyonu), tam radyo sertifikasyonu, daha uzun takvim.
- **Kaba eşik:** ~10.000 adet/yıl altında ve içeride RF mühendisi yoksa modül neredeyse her zaman doğru karar.

Seçimi Faz 1'de yaz ve `regulasyon.md`'deki maliyet/takvim tablosuyla birlikte sun.

---

## 3. MCU/SoC seçimi

### 2.4 GHz bağlantılı SoC ailesi (Eylül 2026 manzarası)

| Aile | Radyo | Güçlü yanı | Zayıf yanı |
|------|-------|-----------|-----------|
| **ESP32-C3** | Wi-Fi 4 + BLE 5.0 | En ucuz Wi-Fi+BLE; devasa ekosistem | Tek çekirdek, uyku akımı yüksek, Wi-Fi 4 |
| **ESP32-C6** | Wi-Fi 6 + BLE 5.3 + 802.15.4 | Matter/Thread/Zigbee için en ucuz yol; 512 KB SRAM; LP core | 2.4 GHz only, 160 MHz, ekran/kamera arayüzü yok |
| **ESP32-C5** | Wi-Fi 6 çift bant | 5 GHz gerekiyorsa | Daha yeni, ekosistem daha ince |
| **ESP32-S3** | Wi-Fi 4 + BLE | Çift çekirdek, USB OTG, kamera/ekran, vektör komutları (ML) | Güç tüketimi yüksek |
| **ESP32-H2** | BLE + 802.15.4 (Wi-Fi yok) | Pilli Thread/Zigbee uç düğüm | Wi-Fi yok |
| **ESP32-P4** | Radyo yok | Yüksek performans uygulama işlemcisi | Ayrı radyo gerekir |
| **nRF52840** | BLE 5, 802.15.4 | Pilli üründe sektör standardı; Bluetooth Mesh olgun | Yeni nesle göre daha yüksek akım |
| **nRF54L15** | BLE, 802.15.4 | Sınıfının en iyi güç profili; Zephyr desteği olgun; OTA için bol flash | Daha yeni |
| **STM32WBA** | BLE 5.4 | Ayrı radyo çekirdeği → çok bağlantı ve yüksek throughput'ta üstün; çok düşük uyku akımı | ST ekosistemi öğrenme eğrisi |
| **STM32U5 / L4** | Radyo yok | Otonom çevre birimleri (LPBAM) ile CPU uyanmadan örnekleme; μA altı uyku | Ayrı radyo gerekir |
| **STM32WL** | LoRa | Tek çipte LoRaWAN | 2.4 GHz yok |

Seçim kısayolları:
- **Matter/Thread + bütçe kısıtlı** → ESP32-C6
- **Pilde 1+ yıl BLE** → nRF54L15 veya STM32WBA (ESP32 ailesi burada zorlanır)
- **Endüstriyel kontrol, deterministik zamanlama, IEC 60730 / AEC-Q100** → STM32
- **Hızlı prototip, geniş kütüphane, tek kişilik ekip** → ESP32
- **Ağır sensör füzyonu + radyo** → STM32U5 (veya nRF) + ayrı radyo, ya da ESP32-P4 + radyo eşlikçisi

Bu tabloyu **kısıt listesiyle** kullan; kullanıcı bütçe/pil/hacim vermemişse önce onu sor.

### Yaygın hata

MCU'yu "hangisini biliyorum" diye seçmek. Doğru sorular: uyku akımı hedefi tutuyor mu, flash OTA için iki slot + bootloader'a yetiyor mu, çevre birimleri (ADC çözünürlüğü, timer, DMA) gerçekten yetiyor mu, 5 yıl sonra hâlâ üretimde mi (longevity programı var mı), ikinci kaynak var mı.

**Flash bütçesi kuralı:** OTA'lı bir üründe uygulama görüntüsü flash'ın yarısından fazlasını kaplıyorsa MCU küçük seçilmiş demektir. Bootloader + slot0 + slot1 + ayarlar/NVS + (varsa) kalibrasyon alanı sığmalı.

---

## 4. Güç bütçesi ve pil

### Hesap

```
Q_döngü = Σ (I_durum × t_durum)        [her durum: uyku, sensör, MCU işlem, TX, RX, retry, join]
I_ort    = Q_döngü / T_döngü
Ömür     = (C_nominal × η_derating) / I_ort
```

`η_derating` tipik değerleri (planlama için; hücre datasheet'i esastır):
- CR2032 / CR2450 lityum coin: 0.60-0.75
- Alkalin AA/AAA: 0.55-0.70
- Lityum primary AA (LiSOCl2 / LiFeS2): 0.75-0.90
- Li-ion / LiPo: 0.75-0.90

### Sık atlanan kalemler — bunlar bütçeyi ikiye böler

- Regülatör **quiescent** akımı (LDO'nun I_q'su μA seviyesinde olmalı; 50 μA'lık bir LDO tek başına coin cell'i öldürür)
- Sensör **standby** akımı ve ısınma/settling süresi
- Pull-up dirençleri, LED'ler, voltaj bölücüler (bölücüyü FET ile kes)
- Flash/EEPROM standby
- Radyo **retry** ve yeniden bağlanma; NB-IoT'de **attach** enerjisi
- LoRaWAN'da RX1/RX2 pencereleri
- Sızıntı akımları ve pilin **kendi kendine deşarjı** (çok uzun ömürlerde baskın hale gelir)

### Coin cell'in gizli tuzağı: darbe akımı

CR2032'nin iç direnci yüksektir ve ömür boyunca artar. Radyo TX'in 15-20 mA'lık darbesi gerilimi MCU'nun brown-out eşiğinin altına düşürebilir — **kapasite bitmeden cihaz ölür**. Çözüm: hücrenin yanına yeterli bulk kapasite (tipik 47-220 µF, düşük ESR) koy ve **soğukta test et** (0 °C'de iç direnç ciddi artar).

### Duyarlılık kuralı

Uyku akımı 24 saat çalışır; aktif darbe saniyeler sürer. Bu yüzden **10 µA → 2 µA** iyileştirmesi genelde aktif darbeyi kısaltmaktan daha fazla ömür kazandırır. Bütçeyi çıkarınca hangi kalemin baskın olduğunu göster ve optimizasyonu oraya yönlendir.

### Ölçüm zorunlu

Hesap tahmindir. Faz 4'te **gerçek akım profilini** ölç (Nordic PPK2, Joulescope, Otii veya shunt + osiloskop). Hesapla ölçümü yan yana koy; sapma %30'u geçiyorsa modelde eksik durum vardır — bul.

### Enerji hasadı

Güneş/termal/kinetik hasat, ortalama akım **onlarca µA altına** indiğinde anlamlıdır. Karar üçlüsü: hasat gücü (en kötü koşulda, en kötü mevsimde), depolama (süper kapasitör vs Li-ion), soğuk başlatma davranışı. Süper kapasitör sızıntısı bütçeye girer.

---

## 5. RTOS ve SDK

| Seçenek | Ne zaman | Uyarı |
|---------|----------|-------|
| **Bare metal** | Tek işli, ultra düşük güç sensör; <32 KB flash | Büyüdükçe yönetilemez; OTA/TLS'i kendin yazarsın |
| **FreeRTOS** | Ekstrem bellek kısıtı, AWS IoT ekosistemi zorunlu, ESP-IDF üzerinde | Yapı sana bırakılmış; çok alt sistemli üründe dağılır |
| **Zephyr** | Yeni proje, uzun ömürlü ürün, çok kartlı ürün ailesi, gelişmiş BLE, CI/CD | Devicetree + Kconfig öğrenme eğrisi 2-4 hafta |
| **ESP-IDF** | ESP32 ailesi (altında FreeRTOS) | Espressif'e bağımlılık; başka MCU'ya taşıma maliyeti yüksek |
| **Embedded Linux** | Cortex-A sınıfı, dosya sistemi/konteyner/ağır ağ ihtiyacı | Boot süresi, güç, BOM ve güvenlik yüzeyi büyür |

Pratik kural: **FreeRTOS "merhaba dünya"ya daha hızlı götürür; Zephyr "CI/CD'li, çok kartlı, test edilebilir üretim firmware"ine daha hızlı götürür.** Kesişim projenin 2-3. haftası civarındadır.

Yaygın hibrit desen: Cortex-A üzerinde Linux (UI, bulut, genel yazılım) + aynı SoC'nin Cortex-M çekirdeğinde Zephyr/FreeRTOS (zamanlama kritik iş) — RPMsg/OpenAMP ile haberleşme.

Karar verirken **LTS penceresini** sor: ürün 5-7 yıl sahada kalacaksa, seçtiğin RTOS sürümünün güvenlik yaması ne kadar süre gelecek? CRA'nın destek süresi yükümlülüğüyle doğrudan bağlantılı (bkz. `regulasyon.md`).

---

## 6. Edge AI / TinyML

Cihazda çıkarım, üç sebepten seçilir: gecikme, gizlilik (veri cihazdan çıkmaz), bant genişliği/enerji (ham veri yerine olay gönder). "Havalı olduğu için" değil.

### Ne zaman gerçekten gerekir

- Titreşimden anomali tespiti, akustik olay tespiti, anahtar kelime yakalama, jest tanıma, düşük çözünürlüklü görüntüde varlık tespiti
- Ham sensör verisini sürekli göndermek pil bütçesini yiyorsa (çoğu zaman gönderdiğin veriyi işlemek göndermekten ucuzdur)

### Ekosistem (2026)

- **LiteRT** (eski TensorFlow Lite Micro): en yaygın MCU çalışma zamanı. TF, PyTorch (`ai_edge_torch`), JAX'ten dönüşüm. Basit modeller çok küçük belleğe sığar.
- **ExecuTorch**: PyTorch'tan doğrudan edge yolu; ONNX→TFLite dolambacını ortadan kaldırır.
- **Edge Impulse**: veri toplama → etiketleme → DSP bloğu (FFT/MFCC) → eğitim → int8 quantization → C++ kütüphanesi. MCU üreticileriyle geniş ortaklık. Tek kişilik ekip için en hızlı yol.
- **CMSIS-NN**: Cortex-M'de optimize kernel katmanı.
- **NPU'lu MCU'lar**: Arm Ethos-U mikroNPU, TI TinyEngine NPU, Syntiant, GreenWaves GAP9. Sürekli çalışan çıkarımda enerji/gecikme kazancı büyük — sürekli dinleyen/izleyen üründe ciddi ciddi değerlendir.
- **MLPerf Tiny**: karşılaştırma için referans.

### Bütçeleme kuralı

Modeli seçmeden önce üç sayıyı yaz: **flash bütçesi (model + arena), RAM bütçesi (tensor arena), çıkarım başına enerji (mJ)**. Çıkarım enerjisi × çıkarım sıklığı, güç bütçesi tablosuna yeni bir satır olarak girer. Bu satır yazılmadan "cihazda AI olsun" kararı verilmez.

Quantization (int8) neredeyse her zaman zorunludur; float model MCU'ya sığsa bile enerjisi sığmaz.

---

## 7. Mimari karar kaydı şablonu

```markdown
# Mimari Karar Kaydı — <ürün adı> v<n>
Tarih: <GG.AA.YYYY>

## Kısıtlar (kullanıcıdan)
- Hedef pazarlar: 
- Pil / güç kaynağı ve ömür hedefi:
- Menzil ve konuşlanma ortamı:
- Hedef BOM maliyeti @ <adet>:
- Hacim/boyut kısıtı:
- İlk sevkiyat tarihi:

## Kararlar
| Katman | Seçim | Gerekçe | Kilitlediği |
|---|---|---|---|
| Bağlantı | | | |
| Paket (modül/çip) | | | |
| MCU/SoC | | | |
| Pil/güç | | | |
| RTOS/SDK | | | |
| OTA stratejisi | | | |
| Sertifikasyon yolu | | | |

## Güç bütçesi
| Durum | Akım | Süre/döngü | Yük (µA·h) |
|---|---|---|---|
| ... | | | |
| **Ortalama** | | | |
Derating: ___ · Hesaplanan ömür: ___ · **Ölçümle doğrulanacak: Faz 4**

## Açık riskler
| Risk | Etki | Ne zaman kapanır |
|---|---|---|

## Doğrulanmamış varsayımlar
- (regülasyon tarihleri, parça fiyatları, lab ücretleri buraya — canlı doğrulanacak)
```
