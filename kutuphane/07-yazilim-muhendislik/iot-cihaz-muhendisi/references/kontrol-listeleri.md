# Kapı Kontrol Listeleri

Kopyala, doldur, kullanıcıya sun. Her madde için ✅ / ⚠️ / ❌ ve **tek satır kanıt**.
❌ varsa kapı geçmez — bunu yumuşatma, geçici çözüm önerme; ne yapılması gerektiğini söyle.

---

## Kapı 0 → 1: Ürün tanımı

- [ ] Kullanım senaryosu bir paragrafla yazılı, kullanıcı kim belli
- [ ] **Hedef pazarlar** listelendi (regülasyon rejimini bu belirler)
- [ ] Pil ömrü / güç kaynağı hedefi **sayı** olarak var
- [ ] Menzil ve konuşlanma ortamı tanımlı (iç/dış, engel, mesafe)
- [ ] Çevre koşulları: sıcaklık aralığı, nem, IP hedefi
- [ ] Hedef birim maliyet **ve hangi adette** olduğu yazılı
- [ ] İlk seri adedi ve 12 aylık hacim tahmini var
- [ ] Boyut/ağırlık kısıtı var
- [ ] Veri profili: ne kadar, ne sıklıkta, hangi yöne
- [ ] Sevkiyat hedef tarihi var ve geriye doğru takvimle çelişmiyor

---

## Kapı 1 → 2: Mimari

- [ ] Bağlantı teknolojisi seçildi ve gerekçesi yazılı
- [ ] **Sertifikasyon yolu seçildi**: ön-sertifikalı modül mü, çıplak çip mi
- [ ] Seçilen modülün **hedef pazarların hepsinde** grant'ı var (veya olmaması kabul edildi)
- [ ] MCU/SoC seçildi; flash bütçesi OTA'nın iki slotu + bootloader + NVS'i alıyor
- [ ] Kritik bileşenlerde stok var, ikinci kaynak belirlendi, EOL/NRND kontrolü yapıldı
- [ ] **Güç bütçesi tablosu hesaplandı** ve pil hedefini karşılıyor
- [ ] Coin cell varsa darbe akımı ve iç direnç riski değerlendirildi
- [ ] RTOS/SDK seçildi; LTS penceresi ürün ömrünü karşılıyor
- [ ] OTA stratejisi (slot yapısı, taşıyıcı, rollback) belirlendi
- [ ] Cihaz kimliği/provisioning yaklaşımı belirlendi (evrensel parola **yok**)
- [ ] Edge AI varsa flash/RAM/enerji bütçesine satır olarak eklendi
- [ ] Mimari karar kaydı yazıldı, kilitlediği kararlar listelendi

---

## Kapı 2 → 3: Şematik

- [ ] ERC temiz, tüm net'ler adlandırılmış
- [ ] Güç ağacı çizildi; her rayda en kötü durum akımı hesaplandı
- [ ] LDO'ların quiescent akımı pil bütçesiyle uyumlu
- [ ] Her IC'de decoupling ve datasheet'e uygun pin bağlantıları
- [ ] Ray sıralaması (power sequencing) datasheet'e uygun
- [ ] Kullanıcı erişimli tüm hatlarda **ESD koruması**
- [ ] Ters polarite ve aşırı akım koruması var
- [ ] Watchdog ve brown-out yapılandırması planlandı
- [ ] **Programlama/debug arayüzü** var ve üretim jig'inden erişilebilir olacak
- [ ] Kritik rayların ve sinyallerin **test noktaları** var
- [ ] Pil hattında **akım ölçüm noktası** (seri jumper/0 Ω) var
- [ ] Anten eşleme ağı için **π ağı DNP pad'leri** kondu
- [ ] BOM v1: her satırda MPN, tedarikçi, fiyat, stok, ikinci kaynak
- [ ] Risk listesi: tek kaynak / uzun tedarik / EOL riski işaretlendi

---

## Kapı 3 → 4: Layout (tape-out öncesi — geri dönülemez)

**Genel**
- [ ] DRC temiz, seçilen üreticinin **güncel** kural setine göre
- [ ] Stackup seçildi ve fab notunda kilitlendi
- [ ] Katman 2 kesintisiz zemin; hızlı sinyallerin dönüş yolu kırılmıyor
- [ ] İz genişlikleri akım ve sıcaklık artışına göre hesaplandı
- [ ] Kontrollü empedans gerekiyorsa üreticinin stackup'ına göre hesaplandı
- [ ] Kristal MCU'ya yakın, altında zemin, altından sinyal geçmiyor
- [ ] Anahtarlama düğümü (SW node) küçük, giriş kapasitörü IC'ye çok yakın
- [ ] Termal via/bakır döküm güç bileşenlerinin altında
- [ ] Fiducial'lar var (dizgi yapılacaksa)
- [ ] Panelizasyon kuralları üreticiye soruldu

**RF/anten**
- [ ] Anten kart kenarında veya köşede
- [ ] Keepout **tüm katmanlarda** temiz — iç katman dökümü dahil kontrol edildi
- [ ] Anten geometrisi referans tasarımdan birebir kopyalandı (0.1 mm hassasiyet)
- [ ] Besleme izi 50 Ω, kısa, düz, via yok, 90° dönüş yok
- [ ] Zemin düzlemi kenarı anten yakınında düz ve temiz
- [ ] Zemin kenarında via stitching, aralık ≤ ~6 mm
- [ ] Anten ile pil ≥ 8 mm, ekran ≥ 6 mm, kutu duvarı ≥ 5 mm
- [ ] **Keepout silkscreen'e ve fab notuna yazıldı**

**Mekanik ve test**
- [ ] Montaj delikleri kutu modeliyle 3D'de doğrulandı, çarpışma yok
- [ ] Konnektörler kutu kesitleriyle hizalı
- [ ] Test pad'leri tek yüzde toplandı, pogo pin boyutunda
- [ ] Fikstür hizalama delikleri/fiducial'ları var

**Çıktı**
- [ ] Gerber + delik dosyaları + BOM + CPL üretici şablonunda
- [ ] Dizgi dönüş açıları (rotation) kontrol edildi
- [ ] Git'te etiketli sürüm; sipariş bu tag'e karşılık geliyor
- [ ] Rev A için ≥5 kart, ≥5 dizili sipariş edildi

---

## Kapı 4 → 5: Bring-up

- [ ] Güç öncesi kısa devre kontrolü yapıldı
- [ ] Tüm raylar nominal ± tolerans içinde; ripple ölçüldü
- [ ] Debug arayüzü bağlanıyor, firmware yükleniyor
- [ ] Tüm çevre birimleri tek tek doğrulandı
- [ ] Radyo çalışıyor, temel bağlantı kuruluyor
- [ ] **Uyku akımı ölçüldü** ve hesaba yakın (sapma < %30)
- [ ] Aktif durumların akım ve süreleri ölçüldü, güç bütçesi güncellendi
- [ ] Anten S11 ölçüldü (çıplak kart)
- [ ] Bring-up defteri ve rework listesi yazıldı → Rev B girdisi hazır
- [ ] Sapma varsa kök nedeni bulundu (semptom değil)

---

## Kapı 5 → 6: Muhafaza

`muhafaza-mekanik.md` §9'daki listeyi kullan. Özet kritik maddeler:

- [ ] PCB kutuya fiziksel olarak oturdu
- [ ] **Anten S11 kutu içinde** (+ pil takılı + elle tutulurken) ölçüldü, kabul aralığında
- [ ] En kötü durum termal ölçüldü, tüm bileşenler sınır içinde
- [ ] Insert'ler oturdu, kapak 10 kez açılıp kapandı
- [ ] Conta baskısı eşit, kaçak testi geçti (IP hedefi varsa)
- [ ] Kablo rakoru + strain relief takılı, çekme testi yapıldı
- [ ] Düşme testi yapıldı
- [ ] Sertifikasyon işaretleri, model/seri no için yer ayrıldı
- [ ] Montaj sırası belgelendi ve süresi ölçüldü

---

## Kapı 6 → 7: Doğrulama

**EMC**
- [ ] Ortam gürültüsü ölçüldü ve kaydedildi
- [ ] Yakın alan taramasıyla emisyon kaynakları haritalandı
- [ ] Işıyan emisyon ön-taraması yapıldı (tüm kablolar takılı, gerçek uzunlukta)
- [ ] İletilen emisyon ön-taraması yapıldı (şebeke beslemeliyse)
- [ ] **Marj ≥ 6 dB**
- [ ] ESD ön-kontrolü: cihaz kilitlenmiyor, veri kaybetmiyor

**Çevresel**
- [ ] Sıcaklık uç noktaları test edildi
- [ ] Hedef ortama uygun testler (nem/titreşim/UV/IP) yapıldı veya atlanma gerekçesi yazıldı
- [ ] Güç kesintisi dayanıklılığı: 200+ rastgele kesinti, tuğlalaşma yok

**Yazılım**
- [ ] OTA end-to-end çalıştı
- [ ] OTA **rollback** denendi ve çalıştı
- [ ] OTA indirme ortasında kesinti denendi, cihaz kurtardı
- [ ] Bulut erişilemezken temel işlev sürüyor
- [ ] Yeniden bağlanma fırtınası testi (backoff + jitter) geçti
- [ ] Fabrika ayarlarına dönüş cihazdaki **ve** buluttaki veriyi siliyor
- [ ] 7+ gün soak testi: bellek sızıntısı yok
- [ ] Üretim firmware'inde debug arayüzü kapalı, log kapalı
- [ ] Reset sebebi telemetrisi doğru raporluyor

**Saha**
- [ ] 10-50 cihazla 4-8 haftalık pilot tamamlandı
- [ ] Gerçek pil tüketimi hesabı doğruladı
- [ ] Pilot bulguları sınıflandırıldı: Rev B / firmware / kabul edildi

---

## Kapı 7 → 8: Sertifikasyon

- [ ] Numune **üretim niyetli**, firmware sürüm kilitli, muhafaza nihai
- [ ] Test modu firmware'i hazır (sürekli TX, kanal sabitleme, güç ayarı)
- [ ] Yedek numune var
- [ ] Lab akreditasyon kapsamı **senin standartlarını** içeriyor (belgeden doğrulandı)
- [ ] Lab slotu rezerve edildi
- [ ] Uygulanacak harmonize standartların **güncel sürümleri ve OJ durumu** doğrulandı [tarih damgalı]
- [ ] Siber güvenlik yolunun **kısıt tetiklemediği** doğrulandı (yoksa NB planlandı)
- [ ] CVD politikası yayımlandı, iletişim kanalı çalışıyor
- [ ] SBOM üretimi CI'a gömüldü
- [ ] Destek süresi beyanı belirlendi ve satış materyaline girecek
- [ ] Teknik dosya iskeleti hazır, eksikler listelendi
- [ ] Etiket tasarımı ve kılavuz metni hazır
- [ ] Modül kullanılıyorsa grant metni ve modül raporu dosyada
- [ ] RoHS/REACH tedarikçi beyanları toplandı
- [ ] Pil varsa UN 38.3 / IEC 62133 belgeleri alındı
- [ ] WEEE / ambalaj / AEEE kayıtları planlandı

---

## Kapı 8: Üretim

- [ ] Üretim test jig'i çalışıyor, test dizisi tanımlı
- [ ] Test süresi ölçüldü ve hedefin altında
- [ ] Jig "altın numune" ile doğrulandı, periyodik doğrulama planı var
- [ ] Her ünitenin sonucu **veritabanına loglanıyor** (seri no, MAC, FW sürümü, test sonuçları, tarih, jig ID)
- [ ] Provisioning otomatik: seri no + anahtar/sertifika enjeksiyonu + factory kilit + debug kapatma
- [ ] İmzalama anahtarı güvenli saklanıyor; kurtarma prosedürü yazılı
- [ ] Yield hedefi ve fire payı tanımlı, takip ediliyor
- [ ] Kalma sebeplerinin sınıflandırması yapılıyor (kart / dizgi / jig ayrımı mümkün)
- [ ] İlk seri (pilot run) yapıldı ve tam denetlendi
- [ ] OTA aşamalı dağıtım altyapısı hazır (%1 → %10 → %100 + kill switch)
- [ ] Filo gözlemlenebilirliği ve alarm eşikleri kurulu
- [ ] Ambalaj, etiket, kılavuz üretimde
- [ ] Servis/RMA prosedürü yazılı
