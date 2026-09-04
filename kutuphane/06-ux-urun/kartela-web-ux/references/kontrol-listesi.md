# Yayın Öncesi Kontrol Listesi

## A. Sükunet

- [ ] Sayfa yüklenirken mizanpaj kaymıyor (CLS < 0,1)
- [ ] İstenmeden başlayan hiçbir hareket yok — video, karusel, animasyon
- [ ] `prefers-reduced-motion: reduce` tüm zorunsuz hareketi durduruyor
- [ ] Pop-up, çıkış-niyeti modalı, otomatik sohbet yok
- [ ] Aciliyet ve kıtlık dili yok ("son 3 kontenjan", ünlem işareti)
- [ ] Bölüm ayrımı beyaz ↔ nane zemin ritmiyle; çizgi/kutu/gölge yok
- [ ] Boşluk cömert; hiçbir bölüm sıkışmış görünmüyor
- [ ] Kartela şeridi sayfada en fazla bir kez
- [ ] Kullanıcı her adımda vazgeçebiliyor ve bu açıkça söyleniyor

## B. Renk ve tipografi

- [ ] Metin yalnızca `--ink`, `--ink-soft`, `--brand` veya `-ink` türevleri
- [ ] Gül kurusu, sarı, açık mavi, nane **hiçbir yerde `color` değeri değil**
- [ ] Metin kontrastı ≥ 4,5:1 (normal), ≥ 3:1 (büyük)
- [ ] Petrol zemin üzerinde: beyaz/nane/sarı serbest; açık mavi ve gül kurusu yalnızca
      büyük metin ve UI öğeleri
- [ ] En fazla iki yazı tipi ailesi
- [ ] Türkçe glifler doğru görünüyor: **ı İ ğ Ğ ş Ş ç Ç ö Ö ü Ü**
- [ ] Gövde ≥ 16 px, satır yüksekliği ~1,7, satır 60–75 karakter
- [ ] All-caps yalnızca logoda
- [ ] Renk tek başına bilgi taşımıyor; her ayrım etiket/ikonla destekli

## C. Akış ve etkileşim

- [ ] Her tıklama 100 ms içinde bir şey boyuyor
- [ ] Her görünümün beş hâli var: yükleniyor, boş, hata, kısmi, dolu
- [ ] Yazılan metin hiçbir koşulda kaybolmuyor
- [ ] Odak halkası görünür; klavyeyle tüm site gezilebiliyor
- [ ] Geri/ileri/yenileme/derin bağlantı çalışıyor
- [ ] 404 sayfası yol gösteriyor
- [ ] Hata mesajları suçlamıyor, yol gösteriyor

## D. Mobil

- [ ] Mobilde tasarlandı, masaüstünde genişletildi
- [ ] Telefon tıkla-ara
- [ ] Dokunma hedefleri ≥ 44×44 px
- [ ] Alt bardaki eylemler klavye açılınca içeriği kapatmıyor
- [ ] WhatsApp butonu gerçek telefonda test edildi; sağ altta; her sayfada değil
- [ ] WhatsApp'a cevap verecek biri var; mesai dışı durumu belirtiliyor

## E. Performans

- [ ] LCP < 2,5 sn
- [ ] INP < 200 ms
- [ ] CLS < 0,1
- [ ] İlk yükleme < 1 MB
- [ ] Tüm görsellere boyut verilmiş; modern format kullanılmış
- [ ] Yazı tipleri `font-display: swap` ile ve preload edilerek yükleniyor

## F. İçerik ve güven

- [ ] Mekân ve ekip fotoğrafları **gerçek** — stok görsel yok
- [ ] Bina girişi fotoğrafı var
- [ ] "Nasıl başlıyoruz" sayfası her adımda süre ve kim bilgisi veriyor
- [ ] Ücret, iptal ve gizlilik soruları cevaplanmış
- [ ] Ekip unvanları ruhsattaki kadro unvanları
- [ ] Blogda yazar kutusu ve güncelleme tarihi var; gelecek tarihli yazı yok
- [ ] Çalışma saatleri **her sayfada aynı**

## G. Mevzuat *(ayrıca `rpdm-mevzuat` skill'i)*

- [ ] Karekod tanıtım sayfasında
- [ ] Kilitli logo (ruhsat adı) header ve footer'da; adın önünde "Özel"
- [ ] 5651 tanıtıcı bilgi: tam ad, adres, telefon, e-posta — erişilebilir ve güncel
- [ ] KVKK aydınlatma metni, gizlilik ve çerez politikası yayında
- [ ] Formda ayrı onay kutuları; ticari ileti önceden işaretsiz ve koşul değil
- [ ] **Danışan yorumu / referansı / fotoğrafı / başarı hikâyesi yok**
- [ ] "Terapi, tedavi, tanı, klinik, hasta, seans" kelimeleri yok
- [ ] Yalnızca ruhsat kapsamındaki programlar tanıtılıyor
- [ ] Kanıtlanamayan iddia ve sayaç yok
- [ ] MEB logosu yok
- [ ] Profillemeye dayalı yeniden pazarlama etiketi yok
- [ ] Online ödeme varsa ETBİS + mesafeli sözleşme + cayma hakkı
