---
name: kartela-web-ux
description: Kartela Psikoloji'nin (kartelapsikoloji.com, Fatih/İstanbul) web sitesi ve dijital arayüzleri için sükunet-sakinlik-huzur hissi veren, başvuruya yönlendiren kullanıcı deneyimi tasarlar ve denetler. Sayfa tasarımı, bölüm sıralaması, bilgi mimarisi, menü ve navigasyon, ana sayfa kurgusu, başvuru veya iletişim formu, WhatsApp ve telefon akışı, ekip sayfası, mekân galerisi, etkinlik ve oyun grubu listeleme, kurumsal-anaokulu paket sayfası, blog düzeni, lokasyon sayfası, mikro metin ve buton etiketi, boş durum ve hata mesajı, renk-tipografi-boşluk-hareket kararları, erişilebilirlik ve Core Web Vitals konularında kullan. Ayrıca hazır bir sayfanın veya tasarımın UX denetimini yaparken, rakip psikoloji merkezi sitelerini değerlendirirken, "bu bölüm nereye gelmeli / bu form nasıl olmalı / burası sakin hissettiriyor mu / dönüşümü nasıl artırırız" sorularında kullan. Tetikleyiciler - web sitesi tasarla, sayfa kurgusu, landing page, form tasarımı, UX denetimi, kullanıcı akışı, menü yapısı, ana sayfa, mikro kopya, buton metni, renk paleti uygula, erişilebilirlik, site hızı, dönüşüm.
---

# Kartela Psikoloji — Web UX

kartelapsikoloji.com ve tüm dijital arayüzler için kullanıcı deneyimi üretimi ve denetimi.

**Önce oku:**
- `docs/kartelapsikoloji-site-plani.md` — bilgi mimarisi, akışlar, sayfa spesifikasyonları
- `docs/marka-kimligi.md` — renk token'ları, kontrast tablosu, logo kuralları
- `docs/web-ux-arastirmasi.md` — gerekçeler ve kaynaklar

Mevzuat kısıtı için `rpdm-mevzuat` skill'i **ayrıca** geçerlidir.

## Tasarım tezi — her karar buna bağlanır

> Rakipler "bize güvenin, memnun kalanlar var" diyor.
> **Kartela "ne olacağını biliyorsunuz" diyor.**

Danışan yorumu ve başarı hikâyesi mevzuaten yasak (ÖÖK Yön. Ek m.4/1 + KVKK). Bu kısıt
konumlandırmaya çevrildi: güven **süreç şeffaflığı** ve **gerçek mekân** üzerinden kurulur.
Kaygılı ziyaretçinin asıl sorusu zaten "başkaları memnun mu?" değil, **"beni ne bekliyor?"**.

## Sükunet nasıl üretilir

**Sükunet paletle değil, öngörülebilirlikle kurulur.** Palet ve boşluk hissi taşır; asıl işi
"her adımda ne olacağını bilmek" yapar. Altı ilke:

1. **Kademeli açıklama** — bilgiyi adım adım aç, hepsini birden değil
2. **Affedici etkileşim** — geri dönülebilirlik; "hiçbir şey kesin değil"
3. **Tahmin edilebilir geri bildirim** — her tıklama 100 ms içinde bir şey boyasın
4. **İnsan dili** — jargon yok, suçlayıcı hata mesajı yok
5. **Çevresel tutarlılık** — sabit navigasyon, kaymayan mizanpaj (CLS < 0,1)
6. **Mikro-kaygı temizliği** — "Gönder" değil "Talebi gönder"

Travma-bilgili ek: **seçim ve kontrol** ver, **kolay çıkış** bırak, baskı kurma.

## Değişmez kurallar

**Asla yapılmaz:**
- Otomatik oynatan video, kayan karusel, paralaks, sayaç animasyonu
- Çıkış-niyeti pop-up'ı, otomatik açılan sohbet penceresi
- Danışan yorumu, referansı, fotoğrafı, başarı hikâyesi *(mevzuat)*
- "1000+ mutlu danışan" türü sayaç *(hem yasak hem kanıtlanamaz)*
- Stok fotoğraf — mekân ve ekip görselleri **gerçek** olacak
- Gül kurusu, sarı, açık mavi veya naneyi **metin rengi** yapmak *(kontrast 1,2–1,9:1)*
- "Terapi, tedavi, tanı, klinik, hasta, seans" kelimeleri *(1219 s. K. Ek m.13)*
- Placeholder'ı etiket yerine kullanmak

**Daima yapılır:**
- Mobil önce — hedef kullanıcı akşam, yalnız, telefonda ve kaygılı
- WhatsApp ve tıkla-ara, formla **eşdeğer birincil** yol *(TR'de WhatsApp #1 uygulama)*
- Her görünümün beş hâli tasarlanır: yükleniyor, boş, hata, kısmi, dolu
- `prefers-reduced-motion` desteklenir
- Bölüm ayrımı **beyaz ↔ nane zemin ritmiyle**; çizgi ve kutuyla değil
- Karekod tanıtım sayfasında; kilitli logo (ruhsat adı) header ve footer'da
- Yazılan metin kaybolmaz — taslak korunur

## Çalışma akışı

### Üretirken
1. Hangi akışa hizmet ediyor? (`site-plani.md` §2.2 — A1…A9)
2. Kullanıcı bu adımda hangi soruyu soruyor? Bölüm o soruya cevap versin.
3. Sakinlik ilkelerinden geçir, sonra `references/kontrol-listesi.md`.
4. Mikro metni `references/mikro-kopya.md` tonuna göre yaz.

### Denetlerken
`references/akis-denetimi.md` yöntemini uygula: akışları numaralandır → her akışı iki kez
yürü (yeni gelen / mevcut danışan) → adımları kontrol listesine göre notla → bulguları
**[önem] akış / adım — ne bozuluyor — neden önemli — en ucuz düzeltme** biçiminde raporla.

Önem düzeyleri: `blocker` (kullanıcı bitiremiyor) · `friction` (bitiriyor ama bedel ödüyor)
· `polish` (güven/his).

## Referanslar

| Konu | Dosya |
|---|---|
| Akış denetimi yöntemi ve kontrol listesi | `references/akis-denetimi.md` |
| Sakinleştirici mikro metin, buton, hata, boş durum | `references/mikro-kopya.md` |
| Sayfa bazlı desenler ve karar kuralları | `references/sayfa-desenleri.md` |
| Yayın öncesi kontrol listesi | `references/kontrol-listesi.md` |

## Çıktı üslubu

Türkçe yaz. Her tasarım kararını **kullanıcının o anki sorusuna** bağla — "güzel görünür"
gerekçe değildir. Araştırma bulgusu varsa rakamıyla an (`web-ux-arastirmasi.md`). Mevzuat
kısıtına takılan bir fikir çıkarsa **kısıtı söyle ve çalışan alternatifi yaz**; sadece
"olmaz" deme.
