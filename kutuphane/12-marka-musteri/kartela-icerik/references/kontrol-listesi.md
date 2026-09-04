# Yayın Öncesi Kontrol Listesi

`denetim.py` bu listenin **makineyle kontrol edilebilen** kısmını otomatik
yapar. Aşağıdaki ★ işaretli maddeler **insan kararı** gerektirir — script
onları kontrol ediyormuş gibi yapmaz.

## Mevzuat — engelleyici

- [ ] **Karekod** görselde var ve okunuyor (ÖÖK Yön. Ek m.4/2) *(otomatik)*
- [ ] Karekod güvenli alanın içinde — hikayede alt 250 px'e girmemiş ★
- [ ] **Ruhsat adı** görünür, önünde "Özel" (m.7/4) *(otomatik)*
- [ ] **Danışan resmi/ismi/başarısı/yorumu yok** (Ek m.4/1) ★
- [ ] **Tanınabilir çocuk yüzü yok** ★
- [ ] Ekip fotoğrafı varsa **yazılı rızası alınmış** ★
- [ ] "terapi, seans, tedavi, tanı, klinik, hasta" geçmiyor *(otomatik)*
- [ ] Tanıtılan program **ruhsat kapsamında** (EK-18 veya TTK onaylı) ★
- [ ] **Kanıtlanamayan iddia yok** — oran, garanti, "en iyi" *(otomatik)*
- [ ] **MEB adı/logosu yok**; olgusal ifade kullanılmış *(otomatik)*
- [ ] Mecra televizyon **değil** *(otomatik)*
- [ ] İşbirliğiyse "Reklam"/"Tanıtım" etiketi ilk görüş alanında *(otomatik)*
- [ ] Hedefleme **velilere** — çocuğa profil bazlı reklam yok ★

## Marka

- [ ] **Fotoğraf var** *(otomatik)*
- [ ] Fotoğraf **dikdörtgen blok değil** — en az iki kenardan taşıyor *(otomatik: yerleşim adı)*
- [ ] Duotone uygulanmış; stok fotoğrafın rengi palete sızmamış ★
- [ ] Gerçek kurum fotoğrafında `yumusak` kullanılmış, duotone değil ★
- [ ] **Kartela şeridi en fazla bir kez** ★
- [ ] Aksan renkleri **metin rengi olarak kullanılmamış** ★
- [ ] Palet dışı renk yok ★
- [ ] En fazla **iki yazı tipi ailesi** ★
- [ ] Logonun el çizimi karakteri **taklit edilmemiş** ★

## Metin ve ton

- [ ] **Ünlem yok** *(otomatik)*
- [ ] **Aciliyet/kıtlık dili yok** *(otomatik)*
- [ ] Emir kipi değil **davet kipi** ★
- [ ] Eşiği düşüren cümle var ★
- [ ] Başlık kelime sınırında *(otomatik)*
- [ ] Hashtag 5–8 arası, yasak etiket yok ★

## Tipografi ve erişilebilirlik

- [ ] Metin/zemin kontrastı **≥4,5:1** ★
- [ ] Başlık ≥48 pt karşılığı, kilit bilgi 32–40, ikincil ≥24 ★
- [ ] Türkçe glifler doğru diziliyor: **ı İ ğ Ğ ş Ş ç Ç ö Ö ü Ü** ★
- [ ] Kesme işareti tipografik: `Kartela'da` (U+2019), düz tırnak değil ★
- [ ] Metin sola dayalı, **iki yana yaslanmamış** ★
- [ ] Görselde metin asgaride — fazlası karusele taşınmış ★

## Hikaye ve Reels

- [ ] Üst **250 px** ve alt **250 px**'e kritik içerik girmemiş ★
- [ ] Reels'te **yakılmış altyazı var** — sessiz izleniyor ★
- [ ] Altyazı alt 480 px'in üstünde (Instagram UI örtmesin) ★
- [ ] Video 15–60 sn arası ★
- [ ] Ses −16 LUFS'a normalize edilmiş *(otomatik)*
- [ ] Çözünürlük 1080×1920, 30 fps, yuv420p *(otomatik: `dogrula`)*
- [ ] Geçişler yumuşak; sert kesme, flaş, hızlı zoom yok ★
- [ ] Otomatik oynatan rahatsız edici içerik yok ★

## Son adım

- [ ] `denetim-raporu.txt` okundu; **"ZORLANDI" damgası yok** ★
- [ ] Yer tutucu (Pexels) görsel notu değerlendirildi — yayında gerçek fotoğraf mı gerekiyor? ★
- [ ] Açıklama metni ve hashtag `aciklama.txt`'ten kopyalandı

---

**Not:** Bu liste mevzuat uyumunun tamamı değildir. İçerik üretimi
`rpdm-mevzuat` skill'inden geçmek zorundadır; tereddütlü noktada il/ilçe MEM
özel öğretim şubesinden yazılı görüş alınır.
