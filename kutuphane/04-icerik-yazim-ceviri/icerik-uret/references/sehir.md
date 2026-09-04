# Şehir sayfası

**Rolü: hub.** Bir şehrin giriş kapısı. Kendi başına okunur bir yazı, ama asıl
işi okuru o şehirdeki mekanlara ve rotalara dağıtmak.

Şehir sayfası **derinlemesine tek konu anlatmaz** — onu mekan sayfası yapıyor.
Burada iş, şehri kavratmak ve nereden başlanacağını söylemek.

## Arama niyeti

Okur bu sayfaya "gitsem mi, gidersem neresi" diye geliyor. İlham ve araştırma
aşaması; henüz hiçbir şey ayırtmıyor.

| Dil | Tipik sorgular |
| --- | --- |
| tr | `halep gezilecek yerler` · `şam'da ne yapılır` · `lazkiye nerede` · `halep'e ne zaman gidilir` |
| en | `things to do in Aleppo` · `is Damascus worth visiting` · `best time to visit Latakia` |
| ar | `أماكن سياحية في حلب` · `ماذا أزور في دمشق` · `أفضل وقت لزيارة اللاذقية` |

Başlık **şehrin adıdır**, uzun bir tamlama değil. "Halep" — "Halep Gezi
Rehberi: Görülecek 15 Yer" değil. Ön yüz zaten `%s · ComeSyria` ekliyor ve
şişkin başlık hem markayı hem tıklanmayı düşürüyor.

## İskelet

```
<p>  Giriş: şehri bir paragrafta kavrat. Ön yüz bunu serif ve büyük basıyor.
     Klişe değil, karakter: "Ticaretin şehri. Kalesi bir tepenin üstünde
     değil, tepenin kendisi."

<h2> Nereden başlamalı        ← ilk gün / ilk yarım gün somut olarak
<h2> Şehirde                  ← merkezde ne var, yürüme mesafeleri
<h2> Çevresinde               ← günübirlik mesafedeki yerler
<h2> Ne zaman gidilir         ← mevsim, ay, neden
<h2> Nasıl gidilir            ← hangi şehirden kaç saat (varsa)
```

Beş H2 zorunlu değil; şehir hakkında söyleyecek gerçek şeyin varsa yaz. **Boş
bir H2, hiç olmayan H2'den kötü.**

## Alanlar

| Alan | Not |
| --- | --- |
| `subtitle` | Şehrin karakterini iki kelimede veren künye: "Yasemin şehri", "Sabun ve taş". Sıfat yığını değil, imge. |
| `lat` / `lng` | Dört ondalık. `City` şemasını bunlar üretiyor. |
| `founded` | Serbest metin: "MÖ 3. binyıl". Kesin tarih uydurma. |
| `population` | Yaklaşık güncel. Bilmiyorsan boş bırak — yanlış sayı, eksik sayıdan kötü. |
| `best_season` | Ay adıyla: "Nisan–Mayıs, Eylül–Ekim". "İlkbahar" tek başına zayıf. |
| `highlights` | 3–5 madde. **Mekan adı listesi değil** — her madde bir sebep taşısın: "Hamidiye Çarşısı'nın kurşun delikli çatısı". |
| `gallery` | Varsa. Kapak zaten ayrı. |

## Hub görevini yerine getir

Şehir sayfasının altındaki "Bu şehirde", "Bu şehirdeki rotalar" bölümlerini ön
yüz **otomatik** dolduruyor — o şehre `city` alanıyla bağlanmış mekan ve
rotalardan.

Yani şehri yayımladıktan sonra iş bitmiyor: **en az iki mekan ve bir rota**
o şehre bağlanana kadar hub boş bir hub. Yeni şehir eklerken bunu peşine
planla.

## Üç dilde

- Başlık şehrin o dildeki **yerleşik adı**: Halep / Aleppo / حلب. Sözlük:
  `ceviri/references/adlar.md`.
- Türk okur Suriye coğrafyasını kabaca biliyor; İngiliz okur ülkeyi bilir ama
  şehirlerin birbirine uzaklığını bilmez — **mesafe ve ulaşım İngilizcede daha
  çok açıklama ister.**
- Arap okur şehri zaten biliyor. Ona "burası neresi" anlatmak yersiz; sorusu
  **"bugün nasıl"**. Arapça sürüm bu yüzden çoğu zaman en çok yeniden yazılan
  sürüm oluyor.

## Örnek: iyi ve kötü giriş

> ✗ Halep, zengin tarihi ve kültürel dokusuyla ziyaretçilerini büyüleyen,
> Suriye'nin en önemli şehirlerinden biridir.

Hiçbir sorguya cevap vermiyor, hiçbir şey öğretmiyor, yapay zekâ da
alıntılamaz.

> ✓ Ticaretin şehri. Kalesi bir tepenin üstünde değil, tepenin kendisi; altında
> binlerce yıllık katman var. Çarşıları yeniden açılıyor, sabun atölyeleri
> yeniden çalışıyor.

Üç somut olgu, bir imge, sıfır klişe.
