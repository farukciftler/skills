# Marka Kimliği

Bu dosya Moonstone Residence'ın görsel kurallarını tanımlar. Buradaki değerler
depodaki gerçek dosyalardan (SVG kaynak kodu ve piksel örneklemesi) çıkarılmıştır,
tahmin değildir. Bir renk veya font gerektiğinde buradan al; yeni bir tane üretme.

## İçindekiler
1. Logo
2. Renk paleti ve tasarım token'ları
3. Tipografi
4. İkon seti
5. Grafik dil ve fotoğraf yönü
6. Basılı kimlik parçaları
7. Dijital varlık üretimi (favicon, OG görsel, avatar)

---

## 1. Logo

**Yapısı:** Hilal (ay taşı / "moon") + hilalin içine yerleşmiş çizgisel gökdelen
siluetleri ("stone" — yapı) + sağ üstte küçük altın ışıltı. Altında iki satır
kelime markası: `MOONSTONE` (büyük, geniş harf aralıklı) ve `RESIDENCE` (küçük,
çok geniş harf aralıklı).

**Üç ana varyant var, üçünün de yeri farklıdır:**

| Varyant | Dosya | Nerede kullanılır |
|---|---|---|
| Koyu zemin (2D) | `Moonstone Logo 2D/Dark Background/` | Lacivert/siyah zemin. Marka beyaz, ışıltı altın. Web'in varsayılanı. |
| Açık zemin (2D) | `Moonstone Logo 2D/Light Background/` | Beyaz/krem zemin. Marka mavi→lacivert degrade, ışıltı altın. |
| 3D altın rölyef | `Moonstone Logo 2D/Moonstone Logo 3D - HR/` | Katalog kapağı, kartvizit, prestij baskı, sunum kapağı. 4096×4096 PNG. |

Her varyantın 6 kombinasyonu var (dikey kilitli, yatay kilitli, sadece sembol,
sadece kelime markası vb.). Web ve ekran için **SVG** kullan, PNG'yi sadece
SVG'nin çalışmadığı yerde (e-posta imzası, sosyal medya avatarı) kullan.

**3D versiyonu ekranda küçük boyutta kullanma.** Rölyef ve degradeler 200px
altında çamura döner; o boyutlarda 2D SVG'ye geç.

### Kullanım kuralları

- **Koruma alanı:** Logonun her yanında en az, kelime markasındaki "M" harfinin
  yüksekliği kadar boşluk bırak. Bu boşluğa metin, buton ya da fotoğraf girmez.
- **Minimum boyut:** Kilitli logo (sembol + yazı) ekranda 120px genişliğin,
  baskıda 30mm'nin altına inmesin — "RESIDENCE" satırı okunmaz hale gelir. Daha
  küçük gerekiyorsa sadece sembolü kullan.
- **Yapılmaz:** Oranını bozma, döndürme, gölge/kontur ekleme, renklerini
  değiştirme, kelime markasını başka fontla yeniden dizme, kalabalık fotoğrafın
  üstüne doğrudan koyma (önce koyu bir katman ekle), sembolü ve yazıyı kendi
  kafana göre yeniden konumlandırma.
- **Fotoğraf üstünde:** Koyu zemin varyantını kullan ve altına en az %45
  opaklıkta lacivert bir katman (`#040C1D`) koy. Kontrast düşükse logo prestijli
  değil, ucuz görünür.

---

## 2. Renk paleti ve tasarım token'ları

Palet üç eksende çalışır: **derin lacivert** (güven, gece, gökyüzü), **altın**
(değer, ay taşı ışıltısı, prestij) ve **krem/bej** (sıcaklık, nefes alanı).
Lacivert hakim renktir, altın vurgudur — altını zemin rengi yapma, ışıltısı
kaybolur.

### Çekirdek renkler

| Rol | Hex | Nerede |
|---|---|---|
| Ink / marka laciverti | `#040C1D` | Logo koyu zemini, site koyu bölümleri, birincil metin |
| Navy 800 | `#13162A` | Katalog koyu sayfa zeminleri |
| Navy 700 | `#14233F` | Kart ve bölüm zeminleri |
| Navy 500 | `#35446E` | Metin kutusu zemini, ikincil yüzey |
| Blue 300 | `#7B9FEE` | Açık zemin logosundaki degradenin üst ucu, vurgu çizgileri |
| Sky | `#6A9ACA` | Render'lardaki gökyüzü tonu, dekoratif |
| **Gold** | `#B8992F` | **Birincil altın** — ikonlar, çizgiler, vurgu |
| Gold light | `#FDD835` | Altın degradenin ortası |
| Gold highlight | `#FFFF8D` | Altın degradenin en açık ucu (ışıltı) |
| Gold deep | `#F4B400` | Altın degradenin koyu ucu |
| Bronze / bej | `#9C8A5D` | Katalog bant rengi, ikinci metalik, ikon "bej" seti |
| Cream | `#F5F1EC` | Açık bölüm zemini — saf beyaz yerine bunu tercih et |
| White | `#FFFFFF` | Koyu zemin üstü metin, logo |

### Altın degrade (logodaki ışıltının orijinal tanımı)

```css
background: linear-gradient(180deg, #FFFF8D 0%, #FDD835 46.6%, #F4B400 100%);
```

Bu tam değerler logonun SVG'sinden gelir. Altın bir yüzey ya da metin gerektiğinde
bu degradeyi kullan; düz `#B8992F` ise ince çizgi, ikon ve küçük vurgular için.

### CSS token'ları (web projesinde bunu kopyala)

```css
:root {
  --ms-ink:        #040C1D;
  --ms-navy-800:   #13162A;
  --ms-navy-700:   #14233F;
  --ms-navy-500:   #35446E;
  --ms-blue-300:   #7B9FEE;
  --ms-gold:       #B8992F;
  --ms-gold-light: #FDD835;
  --ms-gold-hi:    #FFFF8D;
  --ms-gold-deep:  #F4B400;
  --ms-bronze:     #9C8A5D;
  --ms-cream:      #F5F1EC;
  --ms-white:      #FFFFFF;

  --ms-gold-gradient: linear-gradient(180deg, #FFFF8D 0%, #FDD835 46.6%, #F4B400 100%);
}
```

### Kontrast — bu paletteki tek gerçek tuzak

Ölçülmüş kontrast oranları (WCAG 2.1; normal metin için eşik 4,5:1, 24px+
büyük metin için 3:1):

| Ön plan | Zemin | Oran | Sonuç |
|---|---|---|---|
| `#B8992F` altın | `#F5F1EC` krem | **2,45:1** | ✗ metin olamaz |
| `#B8992F` altın | `#FFFFFF` beyaz | **2,75:1** | ✗ metin olamaz |
| `#9C8A5D` bej | `#F5F1EC` krem | **3,01:1** | sadece büyük başlık |
| `#B8992F` altın | `#040C1D` ink | **7,10:1** | ✓ her boyutta |
| `#B8992F` altın | `#13162A` navy | **6,49:1** | ✓ her boyutta |
| `#7B9FEE` mavi | `#040C1D` ink | **7,47:1** | ✓ her boyutta |
| `#FFFFFF` beyaz | `#040C1D` ink | **19,53:1** | ✓ |
| `#040C1D` ink | `#F5F1EC` krem | **17,36:1** | ✓ |

Pratikte:

- Altın, açık zeminde **gövde metni rengi olamaz** — 2,45:1 eşiğin çok altında.
  Açık zeminde altını yalnızca ikon, ince ayraç çizgisi ve dekoratif öğelerde
  kullan; başlıkta bile kullanacaksan 24px+ ve kalın olsun, yine de tercih etme.
- Açık zeminde okunacak metin `#040C1D` veya `#13162A` olsun (17:1 üzeri).
- **Altın-üstü-lacivert markanın hem en güçlü hem en erişilebilir eşleşmesi.**
  Vurgu gerektiren her yerde koyu zemine geç, altını orada kullan.

---

## 3. Tipografi

Marka iki serif üzerine kurulu. Sans-serif kullanma — kimliğe yabancıdır.

| Rol | Font | Not |
|---|---|---|
| Kelime markası / display başlık | **Cormorant Garamond** | Logonun yazı tipi. Katalog kapak başlıkları da bu. Google Fonts'ta var, `latin-ext` alt kümesi Türkçe karakterleri kapsar. |
| Gövde metni ve kurumsal evrak | **Lora** | Kartvizit ve cepli dosyada gömülü olan font (Lora-Regular / Lora-Bold). Ekranda küçük boyutta okunaklı. Google Fonts'ta var. |

### Kullanım kuralları

- **Cormorant Garamond'u 28px altında kullanma.** İnce kontrastlı bir Garamond
  yorumudur; küçük boyutta ve düşük çözünürlükte kırılır. Başlıklar için
  `font-weight: 300–400` yeterli; kalın ağırlıklar zarafeti bozar.
- **Başlıklarda harf aralığını aç.** Logo dilini sürdürmek için display
  başlıklarda `letter-spacing: 0.04em–0.12em`, tümü büyük harf yazılan küçük
  etiketlerde `0.18em–0.24em` kullan. "MOONSTONE / RESIDENCE" kilidi bu ritmi
  kurar.
- **Gövde metni Lora, 17–19px, satır yüksekliği 1.7.** Serif gövde metni uzun
  paragrafta yorucu olabilir; satır uzunluğunu 60–75 karakterle sınırla.
- **Rakamlar** (m², kat, oda sayısı) Lora ile, tabular hizalı yaz. Plan
  tablolarında sayı sütunlarını sağa yasla.

### Web font yükleme

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Lora:wght@400;500;600;700&display=swap&subset=latin,latin-ext" rel="stylesheet">
```

`display=swap` şart — aksi halde ilk boyamada metin görünmez ve LCP çöker.
Yedek yığın: `'Cormorant Garamond', 'Times New Roman', Georgia, serif` ve
`'Lora', Georgia, 'Times New Roman', serif`.

---

## 4. İkon seti

`Kurumsal Kimlik/Kurumsal Kimlik Parçaları /Icon Çalışması/` altında **8 ikon,
4 renk versiyonunda**:

`Hakkımızda` · `İletişim` · `İnşaat Süreci` · `Lokasyon` · `Proje Detayları` ·
`Projelerimiz` · `Satış Bilgi` · `Yaşam Tarzı`

| Klasör | Format | Renk | Kullanım |
|---|---|---|---|
| `Icon-black-svg/` | SVG | siyah `currentColor`'a çevrilebilir | **Web için bunu kullan** — istediğin rengi CSS'ten ver |
| `Icon-gold/` | PNG | `#B89A2E` çizgi, `#040C1D` zemin | Koyu zeminli sunum, sosyal medya |
| `Icon-bej/` | PNG | `#9B8A5E` çizgi, `#040C1D` zemin | Yumuşak vurgu gereken yerler |
| `Icon-lacivert/` | PNG | `#040C1D` çizgi, `#B89A2E` zemin | Altın rozet/madalyon görünümü |

**Stil:** 544×544 viewBox, dolgu yok, sadece kontur, `stroke-width: 12.75`,
yuvarlatılmış uçlar. Yeni bir ikon gerekiyorsa **bu stile birebir uy** — aynı
viewBox, aynı stroke kalınlığı, aynı yuvarlatma. Farklı bir ikon kütüphanesinden
(Font Awesome, Material, Lucide) ikon karıştırma; set anında dağılır.

SVG'yi web'de renklendirmek için `stroke="black"` değerlerini `stroke="currentColor"`
ile değiştir, sonra CSS'ten `color: var(--ms-gold)` ver.

Bu 8 ikonun isimleri aynı zamanda **sitenin doğal navigasyon iskeletidir** —
kimlik çalışması bunu zaten önermiş durumda, ondan sapmak için sebep gerekir.

---

## 5. Grafik dil ve fotoğraf yönü

**Tekrar eden grafik motif:** logodaki gökdelen siluetinin ince altın/bej
çizgilerle büyütülmüş, sayfa kenarından taşan hali. Kartvizitte, katalog
sayfalarında ve antetli kağıtta bu motif var. Web'de de bölüm arkalarında
düşük opaklıkla (%6–12) filigran olarak kullan — markayı bedava taşır.

**Katalog düzeninin dili:** geniş beyaz/krem alanlar, tam kanama (full-bleed)
render fotoğrafları, koyu lacivert metin kutuları, altın bant ayraçlar,
sayfanın üçte birini kaplayan büyük Cormorant başlıklar. Web tasarımı bu ritmi
sürdürmeli: **çok boşluk, az öğe, büyük görsel.**

**Fotoğraf/render yönü:** Elimizdeki görseller mimari render — gündüz mavi
gökyüzü ve gece mavisi akşam sahneleri olmak üzere iki ton. Kullanırken:

- Gece render'ları koyu bölümlerde, gündüz render'ları krem bölümlerde kullan.
- Render'ı kırparken binanın dikey hatlarını koru — proje kimliği dikeylikte.
- Görsel üstüne metin gelecekse `linear-gradient(to top, rgba(4,12,29,.85), transparent)`
  tipi bir okunabilirlik katmanı ekle.
- Stok fotoğraf kullanma. Gerekiyorsa mockup klasöründeki gerçek kimlik
  görsellerini kullan — onlar markanın kendi malı.
- **Her render'ın altına "temsili görseldir" notu koy.** Hem dürüstlük hem
  reklam mevzuatı açısından gerekli.

---

## 6. Basılı kimlik parçaları

Hepsi baskıya hazır PDF olarak `Kurumsal Kimlik/Kurumsal Kimlik Parçaları /`
altında; mockup görselleri `Kurumsal Kimlik/Mockuplar/` altında.

antetli kağıt (13 varyant) · kartvizit · cepli dosya (4) · diplomat zarf (2) ·
flama (4) · kupa (4) · kalem (beyaz/lacivert) · duvar saati (dark/light)

Yeni bir basılı iş isteniyorsa (roll-up, saha bariyeri, satış ofisi tabelası,
davetiye) mevcut parçaların düzenini referans al: 3D altın logo üstte ortalı,
altında ince altın ayraç, iletişim bilgileri Lora ile küçük ve sakin, arka
planda çizgisel gökdelen filigranı. Mockuplar sunum ve sosyal medya paylaşımı
için doğrudan kullanılabilir.

---

## 7. Dijital varlık üretimi

Bunlar depoda yok, ilk web/sosyal medya işinde üretilmesi gerekir:

| Varlık | Ölçü | Kaynak |
|---|---|---|
| favicon.ico + PNG | 16, 32, 48, 180 (apple-touch), 192, 512 | Sadece **sembol** (hilal + bina), kelime markası olmadan; koyu zemin varyantı |
| OG / Twitter kartı | 1200×630 | Gece render + koyu katman + koyu zemin logosu + proje adı |
| Sosyal medya avatarı | 1080×1080 | Sadece sembol, lacivert zemin, kenarda nefes payı |
| Kapak görselleri | LinkedIn 1128×191, YouTube 2560×1440 | Yatay render + logo sol/orta |
| E-posta imzası | 320px genişlik PNG | Yatay kilitli logo, açık zemin varyantı |
| Watermark | şeffaf PNG | Beyaz logo %40 opaklık, sosyal medya render'larının köşesine |

Sembolü kelime markasından ayırırken hazır dosyalardan uygun varyantı seç —
SVG'yi elle kırpma, setin içinde zaten sembol-only versiyonlar var (dosya
adlarındaki `-1`, `-2` … ekleri farklı kilitleri gösterir; PNG'lere bakarak
doğru olanı seç).
