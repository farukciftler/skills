# Akış Denetimi Yöntemi

## Yöntem

1. **Akışları envanterle.** Her işi giriş → adımlar → başarı hâli olarak numaralandır.
   Gösterişsiz olanları da dahil et: ikinci ziyaret, hata kurtarma, boş liste, mesai dışı,
   yavaş bağlantı.
2. **Her akışı iki kez yürü.** Bir kez yeni gelen olarak (hiçbir bilgi yok, kaygılı, mobil),
   bir kez mevcut danışan olarak (sadece adres ve saat lazım).
3. **Her adımı kontrol listesine göre notla.** Akışın notu, en kötü adımının notudur.
4. **Bulguları raporla:** `[önem] akış / adım — ne bozuluyor — neden önemli — en ucuz düzeltme`
5. **Önem sırasına göre düzelt**, sonra akışı baştan sona tekrar yürü — komşu adımı bozan
   düzeltme, düzeltme değildir.

**Önem düzeyleri:** `blocker` (kullanıcı bitiremiyor) · `friction` (bitiriyor ama bedel
ödüyor) · `polish` (güven ve his)

## Kartela'nın akışları

| # | Akış | Giriş | Başarı |
|---|---|---|---|
| A1 | Bireysel başvuru | Ana sayfa / hizmet / blog | Talep iletildi + ne zaman dönüleceği söylendi |
| A2 | WhatsApp'tan başvuru | Her sayfa | Mesaj gönderildi |
| A3 | Telefonla başvuru | Mobil header / lokasyon | Arama başladı |
| A4 | Kurumsal talep | "Kurumlar için" | Kurumsal form iletildi |
| A5 | Oyun grubu / etkinlik kaydı | Etkinlikler / oyun grupları | Kayıt talebi iletildi |
| A6 | Yer bulma | Lokasyon / footer | Yol tarifi açıldı |
| A7 | Bilgi arama | Arama motoru → blog | Okundu veya A1'e geçti |
| A8 | İkinci ziyaret | Doğrudan | 10 saniyede saat/adres/telefon bulundu |
| A9 | Hata ve boş durum | Her yer | Kullanıcı kaybolmadan devam etti |

## Kontrol listesi — her adımı bununla notla

### Süreklilik
- [ ] Navigasyon kaybolmuyor, yeri değişmiyor; kullanıcı nerede olduğunu görüyor
- [ ] Geri/ileri, yenileme, derin bağlantı, yeni sekmede açma çalışıyor
- [ ] Sekme başlığı doğruyu söylüyor
- [ ] Form yarıda kalırsa yazılanlar duruyor

### 100 ms içinde geri bildirim
- [ ] Her tıklama anında bir şey boyuyor (basılı hâli, iskelet, iyimser durum)
- [ ] Uzun işlem gerçek birimle ilerleme gösteriyor
- [ ] Gönderim sonrası **ne olacağı** söyleniyor ("1 iş günü içinde ararız")

### Beş hâl
- [ ] Yükleniyor (iskelet, spinner değil)
- [ ] Boş (tek fiille sonraki adımı söylüyor)
- [ ] Hata (ne oldu **ve** şimdi ne yapılacak)
- [ ] Kısmi (bir kısım veri + sorun)
- [ ] Dolu

### Giriş ve klavye
- [ ] Yazılan metin hiçbir koşulda kaybolmuyor
- [ ] Tek alanlı formda Enter gönderiyor; Escape yalnızca en üst katmanı kapatıyor
- [ ] Odak her açılma/kapanma sonrası mantıklı bir yere iniyor ve **görünür**

### Sükunet (bu projeye özel)
- [ ] Sayfa yüklenirken mizanpaj kaymıyor (CLS < 0,1)
- [ ] İstenmeden başlayan hareket yok (video, karusel, animasyon)
- [ ] `prefers-reduced-motion` açıkken tüm zorunsuz hareket duruyor
- [ ] Hiçbir yerde aciliyet/kıtlık dili yok
- [ ] Pop-up yok, otomatik açılan sohbet yok
- [ ] Metin kontrastı ≥ 4,5:1; aksan renkleri metin olarak kullanılmamış
- [ ] Kullanıcı her adımda vazgeçebiliyor ve bu açıkça söyleniyor

### Mobil
- [ ] Telefon numarası tıkla-ara
- [ ] Dokunma hedefleri ≥ 44×44 px
- [ ] Alt bardaki birincil eylemler klavye açılınca içeriği kapatmıyor
- [ ] WhatsApp butonu gerçek telefonda test edildi, sağ altta, her sayfada değil

### Yoğunluk ve ölçek
- [ ] Ekip 3 kişiyken de 15 kişiyken de çalışıyor
- [ ] Etkinlik listesi 0, 1 ve 40 kayıtta çalışıyor
- [ ] Uzun Türkçe başlıklar taşmıyor, düzgün kırpılıyor

## Rapor biçimi

```
# kartelapsikoloji.com akış denetimi — <tarih>
## Envanterlenen akışlar
## Bulgular (önem sırasına göre tablo: # / akış / bulgu / düzeltme)
## Bu turda düzeltilenler (doğrulama notlarıyla)
## Ertelenenler (ne kaldı, neden, önerilen sıra)
```

Her düzeltmeyi akışı gerçekten yeniden yürüyerek doğrula. Diff'e bakarak "düzeldi"
işaretlenmez.
