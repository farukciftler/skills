# Emlak ve İnşaat Sorgu Sözlüğü

Pexels'te sorgu yazmak çeviri işidir. Brief bir *duygu* söyler ("prestijli",
"huzurlu", "yatırım"); arama motoru *nesne* arar. Aradaki köprüyü sen kurarsın.

## Temel dönüşüm

Her sorguyu şu üçlüye indirge:

```
[somut nesne] + [malzeme/doku] + [ışık koşulu]
```

| Brief der ki | Sorgu şu olur |
|---|---|
| "prestijli yaşam" | `marble surface soft shadow` · `brass detail dark background` |
| "huzur" | `linen curtain morning light` · `empty room warm sunlight` |
| "sağlam yapı" | `concrete texture close up` · `steel rebar construction site` |
| "yatırım" | `house keys wooden table` · `financial documents pen desk` |
| "modern mimari" | `glass facade abstract reflection` · `geometric concrete pattern` |
| "aile" | `dining table set daylight` · `hands holding keys` (yüz olmadan) |
| "şehir hayatı" | `city street evening bokeh` · `cafe counter warm light` |

**Kural:** Soyut kelimeyi tek başına aratma. `luxury`, `dream home`, `elegant`
gibi kelimeler Pexels'te en klişe ve en çok kullanılmış kareleri getirir.

## Tek eksen kuralı

Beş sorgu yaz, her birinde **tek bir ekseni** değiştir. Böylece sonuç kümesi
çeşitlenir; beş benzer sorgu aynı 40 fotoğrafı getirir.

| Eksen | Örnek (konu: "kredi ve satın alma" blog kapağı) |
|---|---|
| Birebir konu | `house keys on contract paper` |
| Makro detay | `pen signing document close up` |
| Konusuz ortam | `empty modern office desk morning` |
| Soyut doku | `paper texture neutral background` |
| Komşu nesne | `calculator notebook wooden desk` |

## Sorgu bankaları

### İnşaat ve yapı
```
concrete texture close up · steel rebar construction · scaffolding against sky
crane silhouette dusk · architectural blueprint desk · hard hat on table
construction site aerial · formwork concrete pour · welding sparks dark
```
Not: Şantiye görselinde **Moonstone'un kendi sahası** kullanılır. Stok şantiye
yalnızca blog ve rehber içeriğinde, konu anlatımı olarak kullanılabilir.

### Mimari doku ve malzeme (`doku` preset'i)
```
polished concrete surface · white marble veining macro · oak wood grain
brushed brass plate · frosted glass texture · terrazzo floor detail
raw plaster wall · dark stone surface · linen fabric texture
```
Bunlar en güvenli kategoridir: tanınabilir yer yok, insan yok, marka yok.
Site bölüm zeminleri ve sosyal medya arka planlarının çoğu buradan gelmeli.

### İç mekân atmosferi (dikkatli)
```
minimal interior morning light · sheer curtain sunlight · empty living room neutral
kitchen counter detail warm · reading chair corner daylight · plant shadow wall
```
**Uyarı:** Bunlar asla bir daire tipini temsil ediyormuş gibi sunulamaz.
Yalnızca blog ve yaşam tarzı içeriğinde, açıkça genel bağlam olarak.

### Yatırım, finans, süreç
```
house keys wooden table · contract signature pen · calculator documents desk
handshake close up hands · model house on blueprint · savings jar coins
```
`model house` (maket ev) klişedir ama emlak içeriğinde çalışır; ölçülü kullan.

### Yaşam ve sosyal alanlar (bağlam için)
```
indoor swimming pool empty · sauna wood interior · gym equipment dark room
towels folded spa · steam room detail · yoga mat morning light
```
**Uyarı:** Moonstone'un havuzu/sporu/spa'sı için kullanılmaz. Yalnızca
"rezidansta sosyal alan ne işe yarar" tarzı rehber içeriğinde.

### İstanbul ve Tuzla çevresi
```
istanbul skyline evening · bosphorus ferry morning · marmara sea coastline
istanbul street cafe · anatolian side coastline · marina boats sunset
```
Tuzla'ya özgü karşılık Pexels'te yok denecek kadar az. **Tuzla'yı temsil eden
görsel gerekiyorsa gerçek fotoğraf çekilmeli** — İstanbul'un başka bir yerini
Tuzla diye kullanmak, kırmızı çizginin ihlalidir.

### Soyut ve zemin
```
dark navy gradient background · gold bokeh dark · night sky stars minimal
moon crescent dark sky · smooth gradient neutral · light rays dark room
```
`moon`, `moonstone`, `crescent` sorguları marka anlatısıyla örtüşür — hilal ve
ay taşı motifi logo ile uyumlu içerik üretmek için kullanışlı.

## Sessiz alan vekilleri

Üzerine metin gelecek görselde "negative space" doğrudan aranmaz. Bunun yerine
sessiz alan üreten koşulları ara:

```
minimal · empty · negative space · copy space · flat lay top view
overhead shot white background · gradient background · out of focus bokeh
fog mist · dark low key · plain wall
```

Puanlayıcı zaten üzerine metin gelecek preset'lerde ton uygunluğunu ölçüyor;
ama sorgu düzeyinde bunu beslemek sonuç kalitesini belirgin artırır.

## Video (`reels-bstok`, `yt-longform-bg`)

Aranan şey **döngülenebilirlik**: başı ve sonu birbirine yakın, sert kesme
içermeyen, tek yönlü yavaş hareket.

```
slow pan concrete wall · drifting fog dark · water surface ripple slow
dust particles light beam · curtain moving breeze · clouds timelapse slow
abstract ink water · candle flame dark
```

Kaçın: hızlı kamera hareketi, sert kesme, ekranda yazı, tanınabilir yüz,
tanınabilir bina, marka logosu, araç plakası.

Süre: Reels ara kesiti için 5–30 sn yeterli; klibin tamamı kullanılmayacak.
İndirdikten sonra sesi at — `ffmpeg -i in.mp4 -an -c:v copy out.mp4`.

## Türkçe brief'ten sorguya — çalışılmış örnekler

**Brief:** "Net-brüt m² farkı blog yazısı için kapak."
```
-q "architectural floor plan drawing close up"
-q "measuring tape on wooden floor"
-q "blueprint rolled paper desk"
-q "empty room corner daylight"
-q "grid paper texture neutral"
```

**Brief:** "Sitede 'Ayhanlar güvencesi' bölümünün arka planı, üzerine koyu
katman gelecek."
```
-q "concrete texture close up"        --preset web-bolum --color "#040C1D"
-q "steel structure abstract dark"
-q "dark stone surface macro"
-q "scaffolding silhouette dusk"
-q "brushed metal plate dark"
```

**Brief:** "Konut kredisi rehberi için Instagram carousel zeminleri."
```
-q "paper texture neutral background"  --preset ig-feed-45
-q "wooden desk overhead minimal"
-q "calculator pen documents flat lay"
-q "soft gradient beige background"
-q "linen fabric texture light"
```

**Brief:** "Ay taşı / hilal temalı marka içeriği."
```
-q "crescent moon dark sky"            --preset ig-story --color "#040C1D"
-q "moonstone gemstone macro"
-q "gold light streak dark background"
-q "night sky stars minimal"
-q "iridescent stone surface"
```

## Sorgu yazarken son kontrol

- [ ] Sorgu bir nesne içeriyor mu, yoksa sadece duygu mu?
- [ ] Beş sorgu birbirinden gerçekten farklı ekseni mi deniyor?
- [ ] `luxury`, `dream`, `elegant`, `beautiful` gibi klişe sıfatlar var mı?
- [ ] Sonuç Moonstone'un kendisiymiş gibi okunabilir mi? (öyleyse iptal)
- [ ] Marka rengi `--color` olarak verildi mi?
- [ ] Ticari kullanım için `--exclude-people` açık mı?
