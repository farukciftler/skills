---
name: sosyal-medya-post-uret
description: ComeSyria için görsel odaklı, marka kimliğine tam uyumlu, üç dilli (TR/EN/AR) Instagram postları, kaydırmalı (carousel) rehberler ve story/reels kapakları üretir. Görsel manipülasyonu, arşiv taramasını, editoryal perdeleme ve tipografik şablonlamayı otomatik uygular. "sosyal medya postu", "instagram postu üret", "görselli post", "carousel oluştur", "story hazırla", "reels kapağı", "sosyal medya içeriği", "post şablonu" dendiğinde kullan.
---

# ComeSyria — Sosyal Medya & Görselli Post Üretim Becerisi

Bu beceri; ComeSyria'nın zengin içerik arşivini (`content/` dizini) kullanarak **yalnızca görselli, editoryal kalitede ve üç dilli (TR/EN/AR)** Instagram gönderileri üretir.

---

## 🛑 1. GÖRSEL ZORUNLULUĞU (PAZARLIKSIZ)

* **Görselsiz post KESİNLİKLE üretilmez.** Her gönderi mutlaka yüksek kaliteli, gerçek ve doğrulanmış bir Suriye görseli veya görsel kolajı taşımalıdır.
* Görsel yerleşimi şu 3 moddan birinde uygulanır:
  1. **Tam Boy Arka Plan (Full Hero + Scrim):** 4:5 veya 9:16 tuvalin tamamını kaplayan fotoğraf, üzerine binen editoryal koyu yeşil perde (`photo-scrim`) ve tipografi.
  2. **Editoryal Fotoğraf Kutusu (Card + Media Box):** Açık/taş zeminli kartın üst yarısında %45–55 oranında geniş fotoğraf, alt yarısında başlık ve 3'lü bilgi kutusu.
  3. **Çoklu Görsel / Kaydırmalı Akış (Carousel Multi-Photo):** Her slaytta farklı bir durak veya detayı (iç avlu, mozaik, kapı, lezzet) gösteren sıralı fotoğraflar.

---

## 🎨 2. GÖRSEL MANİPÜLASYON VE TASARIM YETENEKLERİ

### A. Görsel Arama & Doğrulama Pipeline'ı
Doğrulanmış ticari arşivi taramak için:
```bash
node .claude/skills/icerik-uret/scripts/gorsel-ara.mjs "Umayyad Mosque Damascus" --strict umayyad
node .claude/skills/icerik-uret/scripts/gorsel-ara.mjs "Aleppo Citadel" --count 4
```
* **Kural:** Yalnızca CC0, CC BY, CC BY-SA ve Kamu Malı fotoğraflar kullanılır.
* **Yasak:** Pexels veya sahte stok sitelerinden başka ülkeye ait (Örn: Şam Kapısı diye Kudüs fotoğrafı) kareler kesinlikle kullanılamaz.

### B. Akıllı Kırpma & Odak Noktası (Smart Crop & Aspect Ratio)
* **4:5 Portre (`1080 x 1350 px`):** Feed gönderileri ve Carousel slaytları için standart. Dikey kadrajda ana mimari öge veya avlu dikey eksenin ortasında tutulur (`object-position: center 35%`).
* **9:16 Dikey (`1080 x 1920 px`):** Story ve Reels kapakları için. Metinler ve rozetler Instagram ve Reels kırpma güvenli alanı (Safe Zone: ortadaki 1080x1350 alan) içine yerleştirilir.
* **1:1 Kare (`1080 x 1080 px`):** Tekli anıt kartları ve kültürel detaylar.

### C. Editoryal Perdeleme (Photo-Scrim Overlay)
Yapay gri/siyah sis yerine 2025 Suriye bayrağının koyu yeşili (`#002B07` / `#001600`) kullanılır:
```css
background: linear-gradient(
  to top,
  rgba(0, 22, 0, 0.96) 0%,
  rgba(0, 22, 0, 0.85) 35%,
  rgba(0, 22, 0, 0.40) 65%,
  rgba(0, 22, 0, 0.15) 100%
);
```

### D. Renk & Kontrast Derecelendirme
* Fotoğraflarda taş dokusu ve mozaik renkleri belirginleştirilir (`contrast: 1.05`, `saturate: 1.08`).
* Aşırı sıcak/soğuk filtreler yerine belgesel fotoğrafı doğallığı korunur.

### E. Marka İmzaları (Kompozisyon Kuralları)
1. **Tricolor Üst Şerit (14px):** Üst %33.3 Yeşil (`#007A3D`) | Orta %33.3 Beyaz (`#FFFFFF`) | Alt %33.3 Siyah (`#000000`).
2. **Üç Kırmızı Yıldız (`★ ★ ★`):** Rozet sol üstte `#CE1126` renginde. Kırmızı başka hiçbir geniş alanda kullanılmaz.
3. **Alt Watermark:** `comesyria.` (kırmızı noktalı) + `comesyria.com`.

---

## 📐 3. KULLANILACAK ŞABLONLAR

| Şablon Dosyası | Tür & Format | Ne Zaman Kullanılır |
| :--- | :--- | :--- |
| `marketing/templates/html/01-place-spotlight.html` | 4:5 Tekli Mekan | Cami, kale, çarşı, saray ve anıt yapılar |
| `marketing/templates/html/02-carousel-city-guide.html` | 4:5 Carousel (5 Slayt) | Çok duraklı şehir ve yürüyüş rehberleri |
| `marketing/templates/html/03-food-highlight.html` | 4:5 Yeme-İçme | Asırlık tatlıcılar, dondurmacılar, kahvehaneler |
| `marketing/templates/html/04-quote-history.html` | 4:5 & 1:1 Tarihi Not | Seyyah alıntıları ve arşiv fotoğraflı tarihi kartlar |
| `marketing/templates/html/05-route-itinerary.html` | 4:5 Gezi Güzergâhı | Adım adım duraklar, yürüyüş mesafesi ve süre |
| `marketing/templates/html/06-story-reel-cover.html` | 9:16 Story / Reel | Hikâyeler ve Reels video kapakları |
| `marketing/templates/html/07-launch-announcement.html` | 4:5 Duyuru | Lansman, yeni bölüm ve büyük güncelleme duyuruları |

---

## ✍️ 4. METİN (CAPTION) VE INSTAGRAM SEO

> **Bu bölümün tamamı `marketing/captions/instagram-seo.md`'de.** Aşağıdakiler
> özet; bir gönderi yazmadan önce o dosya okunur.

### A. 2026'da neyin işe yaradığı

Instagram artık etiket eşleştiren bir dizin değil, **içeriği okuyan bir arama
motoru**: caption metni, alt metin, **görselin üstündeki yazı** ve Reels sesi
taranıyor. Hashtag erişim getirmiyor — yalnızca sınıflandırıyor.

Ayrıca 10 Temmuz 2025'ten beri profesyonel hesapların herkese açık gönderileri
**Google ve Bing tarafından dizine alınıyor.** Yani bir caption, sitenin kendi
sayfasıyla aynı sorguda yarışıyor.

### B. Anahtar kelime beş yuvaya konur

İlk üçü her gönderide **zorunlu**:

| # | Yuva | Kural |
| :-- | :--- | :--- |
| 1 | **Caption'ın ilk 125 karakteri** | Instagram burada kesiyor. Birincil anahtar kelime bu sınırın içinde ve **doğal bir cümlede** geçmeli — liste değil |
| 2 | **Alt metin** | Karede fiilen ne görünüyor, ~110 karakter. `content/media.json`'daki `alt` değeri çoğu zaman doğrudan kullanılır. Anahtar kelime dizisi yazmak ters teper |
| 3 | **Görselin üstündeki yazı** | Şablon başlığı yer adını **tam** yazar; kısaltma ya da ikon değil |
| 4 | Konum etiketi | Yer araması ayrı bir giriş kapısı, rekabeti düşük |
| 5 | Hashtag | **3-5 adet**, bkz. `captions/hashtags.md` |

### C. Anahtar kelime üç dilde ayrı bulunur

Sitenin kuralı burada da geçerli: **çevrilmez, yeniden yazılır.**
`şam gezilecek yerler` / `things to do in Damascus` / `أماكن سياحية في دمشق`
üç ayrı aramadır. Kalıp: **özel ad + niyet ifadesi.**

### D. Caption mimarisi (5 katman, 600-900 karakter)

1. **Kanca** — ilk 125 karakter: birincil anahtar kelime + somut olgu (tarih, ölçü, saat).
2. **Gövde** — 2-3 kısa paragraf; ikincil kelimeler doğal olarak geçer.
3. **Pratik kutu** — 📍 konum · ⏰ saat · 🎟️ giriş · 💡 ipucu. **Kaydettiren katman burası.**
4. **Çağrı** — kaydetmeyi **sebebiyle birlikte** iste, beğeni isteme. Bağlantı o dilin adresine gider.
5. **Hashtag** — 3-5.

### E. Kaydetme sinyali

2026 sıralamasında beğeni en zayıf, **kaydetme ve DM'de paylaşma en güçlü**
sinyal. Bu hesabın doğal avantajı içeriğin zaten pratik olması: sıralı liste,
zamanlama bilgisi, yanlış yapılabilecek şey ve doğrulanmış sayı kaydettirir.
"Muhteşem manzara" kaydettirmez.

### F. Yayın öncesi denetim listesi

`captions/instagram-seo.md` §10'daki liste **her gönderide** geçilir. Öne
çıkanlar: ilk 125 karakter denetimi, alt metnin yazılmış olması, üç dilin
hiçbirinin çeviri olmaması, fiyat ve saatin doğrulanmış ya da "değişken"
işaretlenmiş olması.

## ⚡ 5. ÜRETİM KOMUTLARI

```bash
# JSON kaydından tam Instagram paketini (TR/EN/AR + Şablon Önerisi) üret:
node marketing/scripts/generate-post.mjs content/places/halep-kalesi.json

# Görsel galerisini tarayıcıda aç:
open marketing/templates/html/gallery.html

# Kancanın ilk 125 karakterini denetle (Instagram kesme noktası):
node marketing/scripts/kanca-denetle.mjs "CAPTION METNİ"
```

---

## 📚 6. OKUMA SIRASI

| Dosya | Ne için |
| :--- | :--- |
| `marketing/captions/instagram-seo.md` | **Önce bu.** Bulunabilirlik, anahtar kelime, alt metin, kaydetme sinyali |
| `marketing/captions/voice-and-tone.md` | Klişe yasakları ve üç dilde yazım |
| `marketing/captions/templates.md` | Doldurulacak caption iskeletleri (TR/EN/AR) |
| `marketing/captions/hashtags.md` | 3-5 etiketin nasıl seçileceği |
| `marketing/BRAND_GUIDELINES.md` | Renk, tipografi, bayrak oranı |
| `marketing/INSTAGRAM_PROFILE_SETUP.md` | Profil adı ve biyografi — gönderi SEO'su bunun üstüne kuruluyor |
