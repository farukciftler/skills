# Sanat yönetimi katalogu

Buradaki on yön bir "tema galerisi" değil, **bağlanılacak karar** listesidir.
Birini seç, `DECK.md`'ye token'larını yaz, desteyi baştan sona onunla kur.
İki yönü karıştırmak ikisini de öldürür.

Seçim gerekçesi konudan gelmeli. Bir denetim firması için "Neon Terminal", bir
oyun stüdyosu için "Bilanço" yanlıştır — ve ikisi de teknik olarak "güzel"
görünür. Yönün konuya bağlanmadığı bir deste iyi görünüp hiçbir şey söylemez.

## Yönler

Her satırdaki font anahtarları doğrudan `scripts/setup_fonts.py` ile kurulur.

---

### 1. Editoryal Basılı (Editorial Print)
Dergi mizanpajı: geniş kenar boşlukları, iri serif display, asimetrik ızgara,
tam taşan görsel, kalın alıntılar. 2026'nın en yaygın "pahalı görünen" yönü —
tam da bu yüzden özenli uygulanmazsa moda kurbanı olur.

- **Ne zaman:** strateji, marka, kültür, editoryal içerik, üst yönetim destesi.
- **Renk:** `paper #F4F1EC` · `ink #14140F` · `accent #9E3B1F` · `muted #7C7A6E`
- **Tipografi:** display `fraunces` 700 / body `inter` 400 · sayı: display yüzü
- **Izgara:** 12 kolon, dış boşluk 1.0in, metin bloğu asla 8 kolonu geçmez
- **Motif:** başlığın üstünde ince yatay kural + sayfa numarası; hep aynı yerde
- **Dikkat:** her slaytı ortalamak. Editoryal düzen sola dayalıdır, boşluk
  sağda birikir.

### 2. İsviçre Sistemi (Swiss Grid)
Katı ızgara, tek grotesk yüz, ağırlık kontrastıyla hiyerarşi, süs yok. Renk
neredeyse sadece siyah-beyaz artı tek bir yüksek doygunluklu vurgu.

- **Ne zaman:** mühendislik, altyapı, veri ağırlıklı iç sunum, teknik ürün.
- **Renk:** `paper #FFFFFF` · `ink #111111` · `accent #FF3B00` · `muted #767676`
- **Tipografi:** tek aile `public-sans` — 800 başlık, 400 gövde, 600 etiket
- **Izgara:** 12 kolon sıkı; hizalar mutlak, her şey aynı sol kenardan başlar
- **Motif:** ızgaranın kendisi; blokların arası hep tam bir kolon
- **Dikkat:** vurgu rengini iki yerden fazla kullanmak. Tek slaytta bir kez.

### 3. Gece Yarısı Terminali (Midnight Terminal)
Koyu zemin, mono tipografi vurgusu, ince ışıyan çizgiler, veri odaklı. Ekran
üstünde ve karanlık salonda çok güçlü; basılırsa ölür.

- **Ne zaman:** dev tool, altyapı, güvenlik, AI/ML ürünü, teknik demo.
- **Renk:** `bg #0A0C0B` · `surface #14181A` · `text #E6EDE9` · `accent #4ADE80`
  · `muted #6B7A74`
- **Tipografi:** başlık `space-grotesk` 700 / gövde `inter` 400 / veri
  `jetbrains-mono` 500
- **Izgara:** 12 kolon, kartlar `surface` renginde, kenarlık `#FFFFFF10`
- **Motif:** mono küçük etiketler (sürüm, bölge, metrik adı) — ama ALL CAPS değil
- **Dikkat:** yeşil vurguyu her yere serpmek; bir slaytta tek bir ışıyan öge.

### 4. Bilanço (Ledger)
Kurumsal ciddiyet, sıcak nötrler, kılcal çizgiler, tablo estetiği, ölçülü
serif. Finans ve danışmanlık dilinde güven demek.

- **Ne zaman:** yatırımcı raporu, finansal model, denetim, hukuk, due diligence.
- **Renk:** `paper #FAF8F3` · `ink #1B1D1C` · `accent #1F4B3F` · `rule #DDD8CC`
  · `muted #6E7370`
- **Tipografi:** başlık `source-serif` 600 / gövde `inter` 400 / sayı
  `inter` 600 tabular
- **Izgara:** 12 kolon; sayısal içerik sağa hizalı, etiketler sola
- **Motif:** kılcal yatay kurallar (0.75pt, `rule`), tablo satır ritmi
- **Dikkat:** kural çizgilerini kalınlaştırmak; 1pt'yi geçerse tablo çirkinleşir.

### 5. Malzeme Blok (Material Block)
Doygun, düz renk blokları; tipografi bloğun içinde yaşar; yuvarlama ya çok
büyük ya sıfır. Cesur ve genç.

- **Ne zaman:** tüketici ürünü, lansman, marka kampanyası, işe alım destesi.
- **Renk:** `base #101010` · `block-a #E8FF52` · `block-b #2C5EFF` ·
  `paper #FFFFFF`
- **Tipografi:** başlık `archivo` 800 (dar kesit) / gövde `inter` 400
- **Izgara:** slaytı 2-3 tam yükseklikte bloğa böl; blok kenarları slayta değer
- **Motif:** renkli blok, kenarlıksız, gölgesiz — düzlem üstünde düzlem
- **Dikkat:** blokların arasına gölge koymak. Bu yön düz olmalı.

### 6. Yumuşak Nesne (Soft Object)
Açık zemin, yumuşak 3B benzeri gradyanlı şekiller, geniş yuvarlama, çok
katmanlı yumuşak gölge. Sıcak ve erişilebilir.

- **Ne zaman:** sağlık, eğitim, wellness, aile/çocuk ürünü, İK.
- **Renk:** `paper #FBF7F4` · `ink #2A2320` · `accent #E4795B` ·
  `soft #F2DFD4` · `deep #3F5E56`
- **Tipografi:** başlık `bricolage` 700 / gövde `figtree` 400
- **Izgara:** 12 kolon gevşek; kartlar 24px yuvarlama, gölge iki katmanlı
- **Motif:** organik blob veya yuvarlatılmış kesik görsel çerçeve
- **Dikkat:** mor-mavi degradeye kaymak. Gradyanlar palet içinde kalmalı.

### 7. Arşiv (Archive)
Kağıt dokusu, damgalı görünüm, kırık ızgara, monospace notlar, hafif eskitme.
"İnsan eli değmiş" hissi — 2026'nın imperfect-by-design damarı.

- **Ne zaman:** araştırma, kültür/sanat, gazetecilik, kurucu hikâyesi, retro ürün.
- **Renk:** `paper #EFE9DC` · `ink #23201A` · `accent #B23A28` ·
  `stamp #3A4A3C` · `muted #7A7365`
- **Tipografi:** başlık `instrument-serif` 400 (iri) / gövde `newsreader` 400 /
  not `space-mono` 400
- **Izgara:** kırık ızgara — bloklar bilinçli olarak hizadan kaçar
- **Motif:** grain overlay (illustration.md'deki `feTurbulence` reçetesi) +
  hafif döndürülmüş etiketler
- **Dikkat:** dokuyu metnin altına koymak; okunurluk her zaman kazanır.

### 8. Beyaz Laboratuvar (White Lab)
Neredeyse tamamen beyaz, tek nötr gri kademe, minik tipografi, çok fazla
boşluk, hassas diyagramlar. Ürünün kendisi konuşur.

- **Ne zaman:** donanım, bilimsel ürün, tasarım stüdyosu portföyü, minimal SaaS.
- **Renk:** `paper #FFFFFF` · `ink #0B0B0C` · `line #E7E7E9` · `accent #0B0B0C`
- **Tipografi:** tek aile `instrument-sans` 400/600; boyut kontrastı düşük
- **Izgara:** çok geniş boşluk; içerik slaytın %55'ini geçmez
- **Motif:** ince teknik çizgi/ölçü işaretleri, diyagram etiketleri
- **Dikkat:** boşluğu doldurma dürtüsü. Bu yönde boşluk içeriktir.

### 9. Yüksek Kontrast Poster (Poster)
Dev kondens tipografi slaytın kendisi olur; görsel arkada tam taşar; metin çok
az. Bölüm ayraçları ve kapaklar için.

- **Ne zaman:** manifesto slaytı, bölüm ayracı, tek mesajlı kapanış, etkinlik.
- **Renk:** `bg #101014` · `text #F5F2EC` · `accent #FF4D2E`
- **Tipografi:** `anton` veya `bebas-neue` display / `inter` 400 mikro metin
- **Izgara:** ızgara yok; tipografi optik olarak yerleştirilir
- **Motif:** başlığın slayt kenarından taşması (kırpılmış harf)
- **Dikkat:** bu yönü tüm desteye yaymak. 3-4 slayttan fazlası yorar; diğer bir
  yönle *sandviç* kur (kapak + ayraçlar poster, içerik başka bir yön).

### 10. Anadolu Nötr (Anatolian Neutral)
Türkçe içerik için toprak tonları, geometrik kilim geometrisinden türetilmiş
motif, güçlü serif. Türkiye pazarına dönük destelerde yerli ama folklorik
olmayan bir zemin.

- **Ne zaman:** TR pazarına dönük marka, üretim, gıda, turizm, kültür yatırımı.
- **Renk:** `paper #F3EDE3` · `ink #1E1A16` · `accent #A5482C` ·
  `deep #2F4739` · `muted #7B7266`
- **Tipografi:** başlık `literata` 700 / gövde `figtree` 400 — ikisi de
  Türkçe gliflerde sağlam
- **Izgara:** 12 kolon; asimetrik, ağırlık sola
- **Motif:** tek geometrik birim (eşkenar dörtgen/çengel) — köşede tekrar eder
- **Dikkat:** halı deseni ile slaytı kaplamak. Motif imzadır, arka plan değil.

---

## Kendi yönünü kurarken

Katalogdaki hiçbiri uymuyorsa (marka zaten varsa genelde böyle olur) aynı
disiplini uygula:

**Renk.** 4-6 adlandırılmış hex. Biri %60-70 görsel ağırlığa sahip olmalı;
eşit ağırlıklı palet karar verilmemiş demektir. Vurgu rengi slayt başına en
fazla iki yerde. Kontrastı doğrula: gövde metni zemine karşı en az 4.5:1,
24pt+ başlık en az 3:1.

**Tipografi.** Bir veya iki aile. İki ise açıkça farklı olsunlar (serif +
grotesk gibi) — birbirine yakın iki sans kararsızlık gibi okunur. Tip ölçeği
kur ve ona uy: display / başlık / alt başlık / gövde / etiket, beş kademe
yeter. Gövde satır uzunluğu 80 karakteri geçmesin.

**Motif.** Tek bir tekrar eden öge seç ve her slaytta uygula. Renk şeridi veya
başlık altı vurgu çizgisi **motif değildir** — bunlar AI çıktısının imzasıdır.
İşe yarayanlar: tutarlı görsel çerçeve biçimi, tek bir geometrik birim, kılcal
kural sistemi, numaralı köşe işareti (içerik gerçekten sıralıysa).

## Her yön için geçerli negatif kısıtlar

Bunlar kataloğun hangi satırını seçersen seç yasaktır — hepsi "karar
verilmemiş" sinyali verir:

- Başlık altı vurgu çizgisi; kenar şeridi; slayt genişliğinde dekoratif bant.
- Aynı düzenin arka arkaya tekrarı; her slaytta üç eşit yuvarlak kart.
- Mor→mavi degrade; her karta aynı `rgba(0,0,0,.1)` gri gölge.
- Her başlığın üstünde harf aralığı açılmış ALL-CAPS etiket.
- `A · B · C` biçiminde orta noktayla birleştirilmiş meta dizeleri.
- Buton/link metninin sonuna eklenmiş `→`.
- Gövde metnini ortalamak; başlıkta tek kelimeyi renklendirmek.
- Krem/bej varsayılan zemin (`#F5F5DC`, `#FAF0E6`) — palet kararıysa başka,
  varsayılan olarak asla.
- İçerik gerçekten bir sıra değilken `01 / 02 / 03` numaralandırması.
- El sıkışma, ampul, yapboz parçası türü stok görsel klişeleri.

## Font kataloğu — hızlı eşleşme

`setup_fonts.py` anahtarları. Türkçe glif kapsamı script tarafından doğrulanır.

| Rol | Güvenli seçimler |
|---|---|
| Nötr gövde | `inter` `public-sans` `figtree` `work-sans` `schibsted-grotesk` |
| Karakterli sans | `space-grotesk` `bricolage` `archivo` `epilogue` `geologica` `syne` |
| Serif gövde | `source-serif` `literata` `newsreader` `lora` `crimson-pro` |
| Serif display | `fraunces` `playfair` `instrument-serif` `dm-serif-display` |
| Poster / kondens | `anton` `bebas-neue` `unbounded` |
| Mono / veri | `jetbrains-mono` `space-mono` |

Sisteme kurmadan bir aileyi desteye yazma; yazarsan LibreOffice QA'i başka bir
yüzle render eder ve gördüğün taşma raporu yalan olur.

Özel font kullanmayacaksan pptx skill'inin güvenli listesine düş (Arial,
Calibri, Cambria, Century Schoolbook) — ama bu durumda tipografi ayırt edici
olmayacak, farkı düzen ve renkten çıkarman gerekir.
