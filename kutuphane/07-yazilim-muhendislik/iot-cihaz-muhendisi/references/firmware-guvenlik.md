# Firmware ve Güvenlik

Faz 1'de kararı, Faz 4'te ilk sürümü, Faz 8'de üretim akışı. OTA ve güvenlik burada "sonra ekleriz" denilemeyecek şeyler — flash haritasını ve MCU seçimini geri dönülmez biçimde etkilerler.

## İçindekiler
- [1. Firmware mimarisi](#1-firmware-mimarisi)
- [2. Flash haritası](#2-flash-haritası)
- [3. Secure boot ve zincir](#3-secure-boot-ve-zincir)
- [4. OTA](#4-ota)
- [5. Provisioning ve cihaz kimliği](#5-provisioning-ve-cihaz-kimliği)
- [6. Bağlantı, telemetri ve bulut](#6-bağlantı-telemetri-ve-bulut)
- [7. Güvenlik gereksinimleri haritası](#7-güvenlik-gereksinimleri-haritası)
- [8. Filo yönetimi ve gözlemlenebilirlik](#8-filo-yönetimi-ve-gözlemlenebilirlik)

---

## 1. Firmware mimarisi

**Katmanlar:** HAL/BSP → sürücüler → servisler (bağlantı, depolama, OTA, güç yönetimi) → uygulama mantığı. Uygulama mantığı doğrudan register'a dokunmaz; test edilebilirlik bununla başlar.

**Durum makinesi disiplini.** IoT cihazı esasen bir durum makinesidir: boot → provision kontrolü → bağlan → çalış → uyu → uyan → raporla. Bunu açıkça modelle; if/else yığınına bırakma. Her durumun timeout'u ve hata çıkışı olmalı — özellikle "bağlanmaya çalışıyor" durumunun, çünkü orada sonsuza dek kalan bir cihaz pilini bir gecede bitirir.

**Zaman aşımı ve geri çekilme:** her ağ işleminde timeout + exponential backoff + jitter. Jitter olmadan, elektrik kesintisi sonrası 2000 cihaz aynı saniyede sunucuya vurur.

**Kalıcı durum:** ayarlar ve sayaçlar için yıpranma dengeli (wear-levelled) depolama (NVS, LittleFS, ZMS). Ham flash'a doğrudan struct yazmak, güç kesildiğinde bozuk yapılandırma bırakır. Şema versiyonu ve CRC koy.

**Host tarafında test:** Zephyr'ın `native_sim` hedefi ya da HAL'i mock'layan bir katman, iş mantığını donanımsız CI'da test etmenizi sağlar. Bu, uzun ömürlü ürünlerde en yüksek getirili yatırımdır.

**Loglama:** derleme zamanında seviye ayarlanabilen, üretimde kapatılabilen bir log altyapısı. Üretim firmware'inde açık UART logu = açık debug arayüzü = güvenlik açığı (bkz. EN 303 645 saldırı yüzeyi maddesi).

---

## 2. Flash haritası

OTA'lı bir cihazda tipik bölümleme:

```
bootloader   (immutable, yazma korumalı)
slot0        (birincil — çalışan görüntü)
slot1        (ikincil — indirilen görüntü)
settings/NVS (yapılandırma, kimlik bilgileri)
factory      (kalibrasyon, seri no, üretim verisi — yazma korumalı)
[scratch]    (yalnız swap-scratch stratejisinde)
```

**Boyutlandırma kuralı:** uygulama görüntüsü flash'ın ~%40'ını aşıyorsa iki slot sığmaz. MCU seçimi bu hesapla yapılır (`mimari-secim.md`).

**Alternatif:** flash dar ise harici SPI flash'a staging (indirilen görüntü orada bekler, bootloader oradan iç flash'a yazar). Ek BOM maliyeti ama MCU'yu büyütmekten ucuz olabilir.

---

## 3. Secure boot ve zincir

**Amaç:** cihazda yalnızca senin imzaladığın kodun çalışması ve firmware'in okunup klonlanamaması.

**Bileşenler:**
- **Secure boot**: bootloader, açılışta görüntünün imzasını doğrular. ESP32'de Secure Boot v2, ARM'de MCUboot + (varsa) TrustZone/immutable ROM bootloader.
- **Flash encryption**: fiziksel erişimi olan birinin flash'ı okuyup firmware'i çıkarmasını engeller.
- **Anti-rollback**: eski (açığı bilinen) bir sürüme geri dönülmesini engeller. Yazılım tarafında MCUboot'un confirm/revert mekanizması vardır; **donanım destekli** anti-rollback için monotonik sayaç veya eFuse gerekir — bu ikisi farklı güvence seviyeleridir, karıştırma.
- **Debug arayüzü kilidi**: üretimde SWD/JTAG kalıcı olarak kapatılır veya parola korumalı hale getirilir.

**Anahtar yönetimi — en sık yapılan ölümcül hata:**
- MCUboot ve benzeri projeler **örnek anahtarlarla** gelir ve bu anahtarların özel kısmı herkese açıktır. Üretimde kullanılırsa secure boot hiçbir şey yapmaz.
- İmzalama anahtarı bir HSM'de veya en azından donanım anahtarında tutulur, CI'da düz metin olarak durmaz.
- Anahtar kaybolursa **hiçbir cihaza bir daha güncelleme gönderemezsin**. Yedekleme ve kurtarma prosedürü yazılı olmalı.
- İmzalama, geliştirici makinesinde değil, kontrollü bir imzalama servisinde/CI aşamasında yapılır.

**Sıralama uyarısı:** flash encryption ve secure boot'u etkinleştirmek çoğu MCU'da **geri dönülemez** (eFuse yakma). Geliştirme kartlarında değil, sadece üretim akışında ve doğrulanmış bir prosedürle yapılır. Yanlış sırayla yakılan bir eFuse kartı tuğlalaştırır.

---

## 4. OTA

### Neden pazarlık konusu değil

- Sahadaki bir bug'ı düzeltmenin tek yolu.
- CRA ve RED siber güvenlik gereklilikleri **güvenlik güncellemesi dağıtabilmeyi** zorunlu kılıyor (bkz. `regulasyon.md`). Güncellenemeyen bir bağlantılı cihaz artık AB pazarına konulamaz.
- Destek süresi taahhüdü (CRA'da beş yıldan kısa olamaz, ürün ömrü daha kısa değilse) OTA olmadan yerine getirilemez.

### A/B (çift slot) akışı — standart yaklaşım

1. Yeni görüntü slot1'e indirilir (HTTP(S), MQTT, BLE DFU — taşıyıcı fark etmez).
2. İmza ve bütünlük doğrulanır; donanım/sürüm uyumluluğu kontrol edilir.
3. Yükseltme bayrağı yazılır, cihaz yeniden başlar.
4. Bootloader slot'ları takas eder ve yeni görüntüyü **test (unconfirmed)** durumunda başlatır.
5. Uygulama kendini doğrular (ağ bağlandı mı, sensör okunuyor mu, temel işlev çalışıyor mu) ve **kendini onaylar**.
6. Onay gelmezse bir sonraki reset'te bootloader eski görüntüye döner.

**Adım 5 tüm işin özüdür.** Onaylama çağrısını "boot eder etmez" yapmak, mekanizmayı süs haline getirir. Gerçek bir sağlık kontrolü — en azından buluta başarılı bağlantı — geçilmeden onaylanmaz.

### Strateji seçimi (MCUboot terminolojisiyle)

| Strateji | Rollback | Scratch gerekir | Not |
|---|---|---|---|
| overwrite-only | Yok | Hayır | En küçük, en basit. Kötü görüntü kalıcı olur — üretim için önerilmez |
| swap-scratch | Var | Evet | Klasik; ayrı scratch bölümü, daha çok flash yıpranması |
| **swap-move** | Var | Hayır | Makul varsayılan: flash verimli, scratch istemez |
| direct-xip | Var | Hayır | Yerinde çalışır; iki slot da XIP ve kendi adresine linklenmiş olmalı |
| ram-load | Var | Hayır | Görüntüyü RAM'e kopyalar |

ESP-IDF tarafında karşılığı: çift OTA bölümü + `otadata` + `esp_ota_mark_app_valid_cancel_rollback()` ile self-test deseni.

### Pratik detaylar

- **Delta/diferansiyel güncelleme**: hücresel bağlantıda veri maliyetini ve enerjiyi düşürür; karmaşıklık ekler. Pilli hücresel üründe ciddi ciddi değerlendir.
- **Aşamalı dağıtım (staged rollout)**: %1 → %10 → %100. Tek seferde tüm filoya basmak, tek bir hatayı toplu felakete çevirir.
- **Kill switch**: dağıtımı durdurma mekanizması sunucu tarafında hazır olmalı.
- **Güç kesintisi dayanıklılığı**: indirme ve yazma sırasında güç kesilirse cihaz bootable kalmalı. Bunu **kasten test et** (bkz. `test-dogrulama.md`).
- **Bootloader güncellemesi** ayrı ve çok daha riskli bir problemdir. Mümkünse bootloader'ı değişmez (immutable) tut ve güncelleme ihtiyacı doğurmayacak kadar basit yaz.
- **Pil eşiği**: pil seviyesi eşiğin altındaysa OTA başlatma. Yarıda kalan güncelleme, boş pilden kötüdür.

### Kullanılabilir altyapılar

Zephyr tarafında MCUboot + MCUmgr, Mender (mender-mcu), RDFM gibi seçenekler; ESP tarafında ESP RainMaker veya kendi HTTPS OTA'n; AWS IoT kullanıyorsan FreeRTOS + IoT Jobs bütünleşik bir yol. Seçerken sunucu tarafını da (dağıtım kampanyası yönetimi, sürüm takibi, başarısızlık raporu) değerlendir — cihaz tarafı işin yarısı.

---

## 5. Provisioning ve cihaz kimliği

Her cihazın **benzersiz** kimliği ve sırrı olmalı. Ortak paylaşılan sır kullanan bir filoda tek cihazın sökülmesi tüm filoyu düşürür — ve bu, hem EN 303 645'in hem RED siber güvenlik gerekliliklerinin doğrudan ihlalidir.

**Seçenekler (artan güvence):**
1. Üretimde MCU flash'ına yazılan benzersiz anahtar — basit, ama flash okunabiliyorsa kırılır (flash encryption şart).
2. MCU'nun donanım kimliği + türetilmiş anahtar (PUF/eFuse tabanlı).
3. **Ayrı secure element / secure MCU** (ATECC608, SE050, NXP EdgeLock vb.): özel anahtar çipten hiç çıkmaz, sertifika tabanlı mTLS mümkün. BOM'a ~0.5-1.5 USD ekler; güvenlik iddiası olan üründe doğru karar.

**Üretim akışı (Faz 8'de test jig'ine gömülür):**
```
kart jig'e → güç → temel test → seri no ata → sertifika/anahtar enjekte
→ kalibrasyon verisi yaz → factory bölümünü kilitle → debug arayüzünü kapat
→ fonksiyonel test → sonucu üretim veritabanına logla → etiket/QR bas
```

Her ünitenin **kaydı tutulur**: seri no, MAC, firmware sürümü, test sonuçları, tarih, jig ID. Sahada bir problem çıktığında "hangi partiden" sorusunun cevabı burada. Bu kayıt aynı zamanda geri çağırma (recall) kapsamını daraltır.

**Kullanıcı tarafı onboarding:** varsayılan evrensel parola **yasak**. Ya cihaz başına benzersiz parola (etikette/QR'da), ya ilk kurulumda kullanıcıya zorunlu parola oluşturtma, ya da sertifika tabanlı eşleştirme (BLE provisioning, Matter onboarding kodu, NFC). Bu, `regulasyon.md`'deki en sık takılan maddedir.

---

## 6. Bağlantı, telemetri ve bulut

**Protokol:** MQTT (üzerinde TLS) IoT'nin varsayılanı; kısıtlı/kayıplı ağlarda CoAP+DTLS; LoRaWAN'da zaten kendi çerçevesi var. HTTP(S) sadece seyrek/büyük transferler için (OTA indirme gibi).

**TLS pratiği:**
- Sunucu sertifikası doğrulanır. `insecure_skip_verify` benzeri her şey üretimde yasak.
- Kök sertifika (CA) **güncellenebilir** olmalı; CA'lar süresi dolar ve cihazın hepsi aynı gün buluta bağlanamaz hale gelir. Bu, sahadaki en sık toplu arıza sebeplerinden biridir.
- Cihazın gerçek zaman kaynağı yoksa sertifika geçerlilik kontrolü yanlış sonuç verir (NTP öncesi TLS problemi). Boot sırasında zamanı almadan doğrulama yapma veya bunu bilinçli bir tasarım kararı olarak belgele.
- mTLS (cihaz sertifikası) tercih edilir; secure element ile birlikte en sağlam kurulum.

**Telemetri tasarımı:**
- Veri sözleşmesini (şema) baştan sürümle. `schema_version` alanı olmayan telemetri, ikinci firmware sürümünde bulut tarafını kırar.
- Payload'ı küçült: JSON yerine CBOR/protobuf; alan adlarını kısalt. Hücresel/LoRaWAN'da her bayt para ve enerji.
- **Store-and-forward**: bağlantı yokken veriyi yerel halka tamponda tut, bağlanınca gönder. Kaç örnek saklanacağı bir tasarım kararıdır, kaza değil.
- Zaman damgası cihazda üretilir (RTC veya ilk senkron sonrası ofset), sunucuda değil.

**Bulut tarafı asgari:** cihaz kayıt/kimlik, telemetri alımı, komut gönderimi, OTA kampanya yönetimi, sürüm envanteri, uyarı/alarm. Kendi yazmadan önce yönetilen bir platform (AWS IoT Core, Azure IoT, ThingsBoard, EMQX vb.) değerlendir — bu katmanı yazmak çoğu ekibin sandığından uzun sürer.

---

## 7. Güvenlik gereksinimleri haritası

AB'ye satılacak bağlantılı bir radyo cihazında bu maddeler artık **hukuki zorunluluk**. Firmware tarafında karşılıkları:

| Gereklilik | Firmware'de karşılığı |
|---|---|
| Evrensel varsayılan parola yok | Cihaz başına benzersiz sır veya zorunlu kullanıcı parolası |
| Zafiyet bildirim politikası | Ürün tarafında değil ama süreçte: yayımlanmış CVD politikası, iletişim kanalı |
| Güvenli yazılım güncellemesi + destek süresi | İmzalı OTA + rollback + ilan edilmiş destek penceresi |
| Kimlik bilgilerinin güvenli saklanması | Secure element veya şifreli flash; düz metin sır yok |
| Güvenli haberleşme | TLS/DTLS, sertifika doğrulaması, güncellenebilir CA |
| Saldırı yüzeyinin küçültülmesi | Kullanılmayan servis/port kapalı, **fiziksel debug arayüzü kapalı**, sürüm bilgisi sızdırılmıyor, en az ayrıcalık |
| Yazılım bütünlüğü | Secure boot, imza doğrulama |
| Kişisel verinin korunması | Yerinde şifreleme, veri minimizasyonu, GDPR uyumu |
| Kesinti dayanıklılığı | Ağ yokken temel işlevin sürmesi, backoff, güvenli varsayılan durum |
| Kullanıcı verisinin silinmesi | Fabrika ayarlarına dönüş **ve** ilişkili buluttan silme |
| Girdi doğrulama | Her harici girdi (payload, komut, konfig) sınırlandırılmış ve doğrulanmış |
| SBOM | Derleme çıktısı olarak makine okunabilir SBOM üretimi ve ürün ömrü boyunca güncel tutulması |

**SBOM üretimi CI'a gömülür.** Zephyr'ın SPDX üretimi, `syft`, CycloneDX araçları kullanılabilir. Elle tutulan bir SBOM, ikinci sürümde bayatlar.

Detaylar, hangi standardın hangi maddesi ve hangi tarihler için `regulasyon.md`.

---

## 8. Filo yönetimi ve gözlemlenebilirlik

Sahaya çıktıktan sonra cevaplaman gereken sorular ve bunları mümkün kılan tasarım:

| Soru | Gerekli mekanizma |
|---|---|
| Kaç cihaz online, hangi sürümde? | Periyodik heartbeat + sürüm raporu |
| Hangi cihazlar sık yeniden başlıyor? | Reset sebebi (watchdog/brown-out/panik) telemetriye eklenir |
| Pil ne durumda? | Pil gerilimi + tahmini kalan ömür raporu |
| Bağlantı kalitesi nasıl? | RSSI/SNR, yeniden bağlanma sayacı |
| Crash oldu mu, nerede? | Coredump/panic handler → kalıcı depolama → sonraki bağlantıda yükleme |
| Güncelleme başarılı mıydı? | OTA sonuç raporu (başarı/rollback/sebep) |

**Reset sebebi ve reboot sayacı**, sahadaki en değerli iki telemetri alanıdır ve ikisi de neredeyse bedavadır. Baştan koy.

**Uyarı eşikleri:** filonun %X'i aynı anda rollback ettiyse, offline oranı eşiği geçtiyse, pil raporları anormal hızlanıyorsa — otomatik alarm. Bunu ilk saha pilotu öncesinde kur, sonra değil.
