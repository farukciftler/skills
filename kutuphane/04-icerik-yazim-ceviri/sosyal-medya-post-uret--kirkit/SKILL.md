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

---

## ✍️ 4. METİN (CAPTION) ÜRETİM STANDARTLARI

Her gönderi paketi TR, EN ve AR olarak şu katmanları içerir:

1. **Başlık & Künye:** `[Başlık] · [Şehir / Yüzyıl]`
2. **Kanca (Hook):** İlk 2 cümle somut gerçek, yapım yılı veya mimari olgu. (*"Büyüleyici", "cennet gibi" klişeleri kesinlikle yasaktır.*)
3. **Gövde:** Mekanın hikayesi, mimari ayrıntıları ve ne görüleceği.
4. **Ziyaret / Lezzet Kutusu:**
   - ⏰ Saatler: Net saatler (Örn: `08:00–20:00 (Namaz dışı)`)
   - 🎟️ Giriş / Fiyat: `500 SYP` veya `Değişken — girişte teyit edin`
   - 💡 İpucu: En iyi ışık, çorap/giyim kuralı, tezgâh arkası izleme tavsiyesi
5. **CTA:** `Suriye rehberleri ve rotalar profildeki linkte. ↗ comesyria.com`
6. **Hashtags:** `marketing/captions/hashtags.md`'den seçilen 8-12 adet odaklı etiket.
