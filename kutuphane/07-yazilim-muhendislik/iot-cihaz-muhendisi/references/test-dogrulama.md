# Test ve Doğrulama

Faz 4, 6, 8. Kartın ilk nefesinden, akredite laboratuvara girmeye hazır hale gelmesine ve her ünitenin hatta test edilmesine kadar.

## İçindekiler
- [1. Bring-up](#1-bring-up)
- [2. Güç ve pil doğrulaması](#2-güç-ve-pil-doğrulaması)
- [3. RF doğrulaması](#3-rf-doğrulaması)
- [4. EMC ön-uyum](#4-emc-ön-uyum)
- [5. Çevresel ve ömür testleri](#5-çevresel-ve-ömür-testleri)
- [6. Yazılım/sistem doğrulaması](#6-yazılımsistem-doğrulaması)
- [7. DFT ve üretim testi](#7-dft-ve-üretim-testi)
- [8. Saha pilotu](#8-saha-pilotu)

---

## 1. Bring-up

Kart geldi. **Güç vermeden önce** yapılacaklar:

1. Görsel muayene: yanlış yönlü bileşen (kutup!), köprü, eksik parça, yanlış değer. Büyüteç veya mikroskop.
2. Ohmmetre ile **her güç rayı ile GND arası** direnç ölçümü. Kısa devre varsa güç vermek karta zarar verir.
3. Enerji verme sırası: **akım limitli laboratuvar güç kaynağıyla** ve düşük limitle (ör. 50 mA) başla. Limit hemen doluyorsa kapat, ara.

Sonra sırayla:

4. Rayların gerilimini ölç (nominal ±tolerans), dalgalanmayı (ripple) osiloskopla bak.
5. Reset/boot pinlerinin seviyelerini doğrula.
6. Kristal osilasyonu (osiloskop, düşük kapasiteli prob veya MCU'nun clock-out pini).
7. Debug arayüzü bağlanıyor mu (SWD/JTAG). Bağlanmıyorsa: reset, güç, SWDIO/SWCLK pull, boot pin durumu.
8. En basit firmware: LED toggle. Bu geçmeden karmaşık kod yükleme.
9. Çevre birimleri tek tek: I2C tarama, SPI loopback, ADC referans ölçümü, sensör kimlik register'ı.
10. En son radyo.

**Bring-up defteri tut.** Her adım, ölçülen değer, beklenen değer, sapma. Rev B'nin değişiklik listesi bu defterden çıkar. Beş kart varsa hepsini ayrı ayrı defterle — kartlar arası fark bir üretim problemine işaret eder.

**Rework kaydı:** Rev A'da yapılan her tel/kesim/parça değişimi fotoğraflanır ve Rev B'ye taşınacak liste olarak tutulur. Aksi halde Rev B'de aynı hata tekrarlanır.

---

## 2. Güç ve pil doğrulaması

Hesabı doğrulamanın tek yolu ölçmek.

**Araç:** Nordic PPK2, Joulescope, Otii Arc gibi bir güç profil cihazı; yoksa shunt direnç + fark yükselteci + osiloskop. Multimetre **yetmez** — μA uykuyla mA darbeleri arasındaki dinamik aralığı ve darbe sürelerini göremezsin.

**Ölçülecekler:**
- Derin uyku akımı (tüm çevre birimleri kapalıyken)
- Her aktif durumun akımı ve süresi (sensör okuma, işlem, TX, RX, retry)
- Bir tam döngünün ortalama akımı
- Açılış (boot) ve ilk bağlantı enerjisi (özellikle hücreselde attach maliyeti)

**Hesapla karşılaştır.** %30'dan büyük sapma varsa modelde eksik bir durum vardır. En sık suçlular: unutulmuş pull-up, uyanık kalan sensör, LDO quiescent'ı, kapanmayan LED, radyonun beklenenden uzun retry'ı.

**Pil ömrü doğrulaması:** hızlandırılmış test için raporlama periyodunu kısalt (ör. 1 saatte 100 döngü) ve tüketilen yükü ölç; sonra gerçek periyoda ölçekle. Ek olarak **soğukta** (0 °C ve altı) darbe altında gerilim çökmesini test et — coin cell'li ürünlerde en sık saha arızası budur.

---

## 3. RF doğrulaması

| Ölçüm | Araç | Kabul |
|---|---|---|
| S11 / dönüş kaybı | NanoVNA (kalibre edilmiş) | Bant içinde tipik hedef ≤ −10 dB |
| Rezonans frekansı | NanoVNA | Serbest alanda hedefin biraz üstünde, kutuda hedefte |
| Çıkış gücü / spektrum | Spektrum analizör + kuplör/anten | Beyan edilen güce ve bant sınırlarına uygun |
| Alıcı hassasiyeti | Zayıflatıcı + paket kayıp oranı | Datasheet'e yakın |
| Menzil | Karşılaştırmalı RSSI | Referans cihaza göre kabul edilebilir fark |

**S11 ölçüm sırası** (her adımı kaydet): çıplak kart → kutu içinde → pil takılı → el/vücut yakınında → gerçek montaj konumunda (duvarda/metal yüzeyde).

**Menzil testi protokolü:** aynı gün, aynı ortam, aynı yükseklik, aynı yön; referans bir ticari cihazla yan yana. Mutlak metre sayısı ortamdan çok etkilenir; **fark** anlamlıdır. Her ölçümde en az 100 paket üzerinden paket kayıp oranı raporla.

**Not:** anten eşleme değişikliği (π ağı bileşenleri) yaptıysan, radyo çıkış gücü de değişmiş olabilir. Sertifikasyona giden nihai donanımda ölçümü tekrarla.

---

## 4. EMC ön-uyum

Ön-uyum, akredite laboratuvara gitmeden önce **başarısızlığı ucuz bulmaktır**. Laboratuvarda takılmak: 2.000-4.000 USD tekrar testi + haftalar + muhtemelen PCB respin.

### Neden başarısız olunur

Sırayla en sık sebepler: anahtarlamalı regülatörün harmonikleri, kablolar (anten gibi ışır), kesintili zemin düzlemi/dönüş yolu, ekranlama boşlukları, hızlı saat sinyalleri.

### Asgari ön-uyum kiti

- Spektrum analizörü (en azından temel sinyalin 3-5. harmoniğini kapsayan bant)
- **Yakın alan probu seti** (H-alan ve E-alan) + ön yükselteç
- **LISN** (iletilen emisyon için, 150 kHz-30 MHz)
- Akım probu (kablolardaki ortak mod akımı için)
- Kalibre edilmiş EMI anteni (ışıyan emisyon için, 30 MHz üstü) ve metalik olmayan sehpa

### Pratik yöntem

1. **Önce ortam gürültüsünü ölç** (DUT kapalı). Yayın vericileri, floresan, komşu ekipman — bunları bilmeden ölçüm okunmaz.
2. **Yakın alan taraması** ile kaynak bul. H-probu akım döngülerini (güç dağıtımı, topraklama) gösterir; E-probu yüksek empedanslı düğümleri ve ekran boşluklarını. Kartı sistematik tara, emisyon haritası çıkar.
3. **Işıyan emisyon ön-taraması**: kalibre anten 1 m veya (daha iyi) 3 m mesafede, DUT normal çalışma modunda, tüm kabloları takılı ve gerçek uzunlukta.
4. **İletilen emisyon**: LISN üzerinden, 150 kHz-30 MHz.
5. **Karşılaştırmalı test**: bir değişiklik yap (ferrit, kondansatör, kablo yönü), önce/sonra ölç. Gürültülü ortamda mutlak seviye güvenilmez ama **fark** güvenilirdir.

**Marj hedefi: limitin en az 6 dB altı.** Ön-uyum ortamı ile akredite oda arasındaki fark, ölçüm belirsizliği ve üretim varyasyonu bu marjı yer. Sınırda geçen bir ön-uyum, laboratuvarda kalır.

### Yakın alan uyarısı

Yakın alan ölçümü **teşhis** aracıdır, uygunluk kararı aracı değil. Yakın alandaki bir tepe, uzak alanda limit aşımına dönüşür diye bir garanti yoktur ve tersi de doğrudur. Karar için kalibre uzak alan ölçümü veya laboratuvar gerekir.

### Bağışıklık (immunity) tarafı

Emisyon kadar konuşulmaz ama takılma sebebidir. Odak: **ESD** (kontak ve hava deşarjı — kullanıcı erişimli her yüzey ve konnektör), ışıyan RF bağışıklığı, hızlı geçici rejim (EFT), surge ve gerilim düşmeleri (şebeke beslemeliyse). Basit ön-kontrol: bir ESD tabancası ile kritik noktalara deşarj ve cihazın kilitlenip kilitlenmediğine bakmak. Cihaz reset atıyorsa bile **kendini toparlaması** ve veri kaybetmemesi beklenir.

### Profesyonel ön-uyum

Bazı laboratuvarlar akredite ekipmanlarıyla ön-uyum hizmeti verir — tam sertifikasyonun bir kısmı fiyatına, aynı odada, mühendis eşliğinde. Karmaşık ürünlerde bu, kendi kitini kurmaktan hızlı ve ucuz olabilir.

---

## 5. Çevresel ve ömür testleri

Hedef ortama göre seç; hepsini yapmak gerekmez ama **hangisini neden atladığını yaz**.

| Test | Ne bulur |
|---|---|
| Sıcaklık uç noktaları (çalışma + depolama) | Kristal kayması, LCD, pil, plastik deformasyonu, saat hatası |
| Sıcaklık çevrimi | Lehim yorulması, conta sızıntısı, insert gevşemesi |
| Nem / sıcaklık-nem çevrimi | Yoğuşma, korozyon, kaçak akım |
| Titreşim / şok | Konnektör oturması, ağır bileşen gövdeleri, vida gevşemesi |
| Düşme | Kutu kırılması, snap kopması, pil temas kaybı |
| IP (toz/su) | Sızdırmazlık tasarımı |
| UV / hava koşulu | Dış mekân plastik renk ve tokluk kaybı |
| HALT (yıkıcı sınır bulma) | Tasarım marjı — sınırı bulup nerede kırıldığını görmek |
| Yaşlandırma (burn-in) | Erken ömür arızaları (infant mortality) |

**HALT mantığı:** amaç geçmek değil, **kırmak**. Sıcaklığı ve titreşimi kademeli artırıp ilk arızayı bul, sebebini anla, gerekiyorsa düzelt. Bu, "spesifikasyonda geçti" bilgisinden çok daha değerlidir çünkü marjı gösterir.

**Güç kesintisi dayanıklılığı** ayrı bir test kalemidir ve genelde unutulur: cihazı yazma sırasında, OTA sırasında, boot sırasında rastgele 200+ kez enerjisiz bırak. Bozuk yapılandırma veya tuğlalaşma varsa burada çıkar.

---

## 6. Yazılım/sistem doğrulaması

Faz 6 kapısı için asgari senaryolar:

- [ ] **OTA end-to-end**: yeni sürüm dağıtıldı, indi, doğrulandı, takas oldu, kendini onayladı
- [ ] **OTA rollback**: kasten bozuk/başarısız bir görüntü gönderildi, cihaz eski sürüme döndü ve online kaldı
- [ ] **OTA kesintisi**: indirme ortasında güç kesildi / ağ koptu → cihaz bootable ve tekrar denedi
- [ ] **Düşük pilde OTA reddi** çalışıyor
- [ ] **Ağ kesintisi**: bulut erişilemezken temel işlev sürüyor; store-and-forward tamponu doldu ve taştığında en eskiyi düşürdü
- [ ] **Yeniden bağlanma fırtınası**: 50+ cihaz aynı anda açıldığında backoff+jitter çalıştı, sunucu boğulmadı
- [ ] **Saat/zaman**: RTC yokken, NTP gelmeden TLS davranışı tanımlı
- [ ] **Sertifika süresi**: CA rotasyonu senaryosu denendi
- [ ] **Fabrika ayarlarına dönüş**: cihazdaki ve buluttaki kullanıcı verisi silindi
- [ ] **Provisioning tekrarı**: cihaz ikinci bir kullanıcıya devredilebiliyor
- [ ] **Uzun süre çalışma (soak)**: 7+ gün kesintisiz, bellek sızıntısı yok, heap parçalanması yok
- [ ] **Reset sebebi telemetrisi** doğru raporluyor
- [ ] **Debug arayüzü** üretim firmware'inde kapalı, üretim logu kapalı

---

## 7. DFT ve üretim testi

### Design for Test — layout aşamasında yapılır

- Her güç rayı, kritik sinyal ve programlama pini için **pogo pin pad'i** (tipik 1.0-1.5 mm, tel geçmeyecek şekilde açık)
- Test pad'leri kartın **tek yüzünde** toplansın (tek taraflı fikstür ucuz)
- Fikstür hizalaması için delik/fiducial
- Programlama arayüzü fikstürden erişilebilir
- Kart bükülmesini önlemek için destek noktaları planlanmış (pogo pin kuvveti × pin sayısı ciddi yük yaratır)
- Kart üzerinde **test modu** girişi (belirli pin kombinasyonu veya UART komutu) — üretim firmware'i bu moda girip kendi kendini test edebilmeli

### Test stratejisi seçimi

| Yöntem | Ne bulur | Hacim |
|---|---|---|
| AOI (dizgi evinde) | Lehim/yerleşim hatası | Her zaman iste |
| Uçan prob (flying probe) | Kısa/açık devre | Düşük hacim, fikstür yok |
| ICT (bed-of-nails) | Bileşen düzeyi hata, kısa/açık | Yüzlerce adet üstü |
| **FCT (fonksiyonel test)** | Ürün gerçekten çalışıyor mu | Neredeyse her zaman gerekir |

**Kaba eşik:** özel fikstür yatırımı tipik olarak birkaç yüz adetlik seriden itibaren geri döner. Altında, basit bir programlama + fonksiyonel test tezgâhı yeterli.

### Fonksiyonel test jig'i — asgari içerik

```
Mekanik: hizalama pimleri, pogo pin plakası, kaldıraç/pnömatik bastırma, kart eğilmesini önleyen destek
Elektrik: güç besleme + akım ölçümü, programlama arayüzü, test edilecek çevre birimlerine bağlantı
Test yazılımı: sıralı test adımları, geçti/kaldı kriteri, sonuç loglama
```

**Tipik test dizisi:**
1. Kısa devre kontrolü (güç vermeden)
2. Güç ver, ray gerilimlerini ölç
3. Uyku akımını ölç (bu **çok** önemli — yanlış bileşen veya lehim köprüsü burada yakalanır)
4. Firmware yükle
5. Çevre birimlerini test et (sensör kimliği, ADC referansı, I2C/SPI cevabı)
6. RF: verici gücünü ve alıcı hassasiyetini kontrollü bir ortamda ölç (kutu içinde veya ekranlanmış hücrede)
7. Seri no ata, anahtar/sertifika enjekte et, kalibrasyon yaz
8. Factory bölümünü kilitle, debug arayüzünü kapat
9. Son fonksiyonel doğrulama
10. **Sonucu veritabanına logla**, etiket/QR bas

**Test süresi birim maliyettir.** Hedef koy (ör. < 60 s/ünite) ve ölç. 5 dakikalık bir test, 10.000 adette 833 saat operatör zamanı demektir.

**Yield takibi:** geçme oranı, kalma sebeplerinin dağılımı, jig başına sapma. Yield düşerse sebebi kartta mı, dizgide mi, jig'de mi ayırt edebilmelisin — bu yüzden jig'in kendisi de periyodik olarak "altın numune" (known-good unit) ile doğrulanır.

---

## 8. Saha pilotu

Sertifikasyondan önce veya paralelinde, **gerçek kullanıcıda 10-50 cihazla** 4-8 hafta.

Ölçülecekler:
- Gerçek pil tüketimi (hesabı doğruluyor mu?)
- Bağlantı kesintisi sıklığı ve süresi
- Yeniden başlama sayısı ve sebepleri
- Kurulum/onboarding başarı oranı ve süresi (kullanıcı desteğe kaç kez yazdı?)
- Menzil şikâyetleri
- Mekanik: takılıyor mu, düşüyor mu, ıslanıyor mu

**Pilot çıkışı bir belgedir:** hangi bulgu Rev B'ye giriyor, hangisi firmware ile çözülüyor, hangisi kabul edilip dokümana yazılıyor. Bu ayrım yapılmadan seri üretime geçilmez.
