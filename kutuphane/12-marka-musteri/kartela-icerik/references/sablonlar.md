# Şablonlar, Yerleşim ve Duotone

## Tuval ölçüleri

| Ad | Piksel | Kullanım |
|---|---|---|
| `gonderi` | 1080 × 1350 (4:5) | **Varsayılan.** Akışta en çok yer kaplar. |
| `kare` | 1080 × 1080 | Izgara tutarlılığı gerektiğinde |
| `hikaye` | 1080 × 1920 (9:16) | Hikaye ve Reels kapağı |

**Güvenli alan:** kenar boşluğu her yönde 72 px. Hikayede ayrıca üst ve alt
**250 px** arayüz tarafından örtülebilir — kritik metin ve karekod girmez.

## Beş gönderi şablonu

### `t1-soz` — söz / kısa mesaj
Tek fikir, **≤12 kelime**. Tırnak işareti + display punto + kartela şeridi.
Akışta durdurucu; en çok paylaşılan tip.
**Yerleşim:** `kose` (sağ üstten taşan daire) veya `yan`. Metin nefes almalı.
**Zemin:** `z-nane` veya `z-gul`.

### `t2-bilgi-kapak` — karusel kapağı
Üst etiket + başlık + destek cümlesi + "kaydır" işareti.
Kartela şeridi **yalnızca burada** — iç sayfalarda tekrarlanmaz.
**Yerleşim:** `alt` veya `kemer`. **Zemin:** `z-beyaz`.

### `t3-bilgi-ic` — karusel iç sayfası
Numaralı rozet + tek fikir + açıklama. Kare başına **≤45 kelime**.
`numara_tonu`: `n-gul` · `n-sari` · `n-mavi` (boş bırakılırsa petrol).
**Yerleşim:** `yan`. **Zemin:** `z-beyaz`.

### `t4-duyuru` — program / etkinlik
Etiket + başlık + alt metin + bilgi satırları + kayıt notu. **Karekod zorunlu.**
Bilgi satırları temiz zeminde toplanır, fotoğraf altta erir, logo/karekod
korumalı bantta durur.
**Yerleşim:** `alt`. **Zemin:** `z-nane` veya `z-sari`.

### `t5-mekan` — mekân / ekip / atmosfer
Tam kadraj fotoğraf + perde + altta tek cümle. Metin fotoğrafın üstünde durur.
**Yerleşim:** `tam` (perde otomatik). **Zemin:** önemsiz, fotoğraf örter.
⚠️ Danışan fotoğrafı konulamaz. Yalnızca mekân, nesne, rızası alınmış ekip.

### `h1-hikaye` — hikaye
Tek mesaj. `eylem` alanı yönlendirme cümlesi taşır.

## Beş yerleşim — hiçbiri dikdörtgen blok değildir

| Yerleşim | Ne yapar | Ne zaman |
|---|---|---|
| `tam` | Tuvalin tamamı; koyu perde altında beyaz metin | Mekân, atmosfer, güçlü tek görsel |
| `alt` | Alt %58; **iki uçtan** maskeyle erir, sol/sağdan taşar | Bilgi yoğun duyuru — metin üstte temiz kalır |
| `kemer` | Üstten taşan, altı yuvarlatılmış kemer | Editorial his; kapak sayfası |
| `kose` | Sağ üstten taşan büyük daire parçası | Kısa metin; sol taraf serbest |
| `yan` | Sağ kenardan taşan dikey şerit, sol kenarı erir | Metin sütunu ile fotoğraf yan yana |

**Kural:** fotoğraf her zaman en az iki kenardan taşar ya da maskeyle erir.
Dört kenarı da tuvalin içinde kalan bir fotoğraf **kullanılmaz**.

## Duotone seçimi

Duotone, fotoğrafın parlaklık bilgisini korur, rengini markanın iki tonuna
eşler (Photoshop'taki "Gradient Map"in karşılığı). Böylece hangi stok fotoğraf
gelirse gelsin palet bozulmaz.

| Değer | Renk çifti | Eşleştiği zemin | İçerik |
|---|---|---|---|
| `petrol` | `#0A2A36` → `#E4EFE9` | `z-nane` | Sakin, kurumsal — **varsayılan** |
| `gul` | `#4A2129` → `#F7EAEC` | `z-gul` | Sıcak — aile, ergen, duygu |
| `mavi` | `#0F323E` → `#E6F2F6` | `z-mavi` | Serin — bilgi, süreç, kurumsal |
| `sari` | `#38381A` → `#F6F5DF` | `z-sari` | Toprak — oyun grubu, atölye, çocuk |
| `kartela` | petrol → açık mavi → nane | `z-nane` | **Tri-tone.** Markanın fikrinin fotoğraftaki karşılığı. ⚠️ Aynı tuvalde **kartela şeridi kullanılmaz** — tri-tone zaten o jesttir. |
| `yumusak` | *(duotone değil)* | herhangi | **Gerçek mekân ve ekip fotoğrafı** — renkleri korur, doygunluğu %55'e düşürür, gölgeleri kaldırır |

### En önemli kural: açık uç = zemin rengi

Fotoğrafın "sayfaya yapıştırılmış blok" görünmesini bitiren şey kenar yumuşatmak
**değil**, duotone'un **açık ucunu zemin rengiyle birebir aynı yapmaktır.**
Fotoğrafın en açık pikselleri zeminle aynı renk olunca nerede bittiği gözle
ayırt edilemez; maskeyle birleşince fotoğraf kâğıda basılmış gibi durur.

Filtre uçları bu yüzden zemin token'larıyla birebir eşlenmiştir.
**`duotone` alanını boş bırakırsan `uret.py` onu zeminden otomatik türetir** —
doğru olan da budur. Elle vermek yalnızca bilinçli bir kontrast isteniyorsa
gerekir.

**Kural:** gerçek kurum fotoğrafında `yumusak` kullanılır — mekânın kendi rengi
markanın parçasıdır, duotone onu siler. Duotone stok görsel içindir.

`grain: true` (varsayılan) ince film dokusu ekler; dijital düzlüğü kırar.

## Zemin renkleri

`z-beyaz` · `z-nane` · `z-gul` · `z-sari` · `z-mavi` · `z-petrol`

Dördü de `--ink` metniyle **10:1 üzerinde** kontrast verir (ölçüldü). `z-petrol`
üzerinde metin otomatik beyaza döner.

**Karusel ritmi:** kapak `z-beyaz`, iç sayfalar dönüşümlü `z-nane` → `z-gul` →
`z-mavi` → `z-sari`. Sayfalar kaydırıldıkça bir kartela şeridi gibi okunur.

## Anatomi — her tuvalde sabit olanlar

- **Logo** sol altta, sabit boyut
- **Ruhsat adı** logonun altında, küçük punto (m.7/4)
- **Karekod** sağ altta, 180 × 180 px (Ek m.4/2)
- **Kenar boşluğu** 72 px
- **Kartela şeridi** en fazla bir kez
- Tuvalin **en az %25'i boş**

## Punto tabanı

1080 px tuvalde, University of Maryland erişilebilirlik eşiklerinin üzerinde:

| Rol | Punto |
|---|---|
| Display (söz) | 92 px |
| Başlık | 68 px |
| Ara başlık | 50 px |
| Destek cümlesi | 38 px |
| Gövde | 32 px |
| Meta / bilgi etiketi | 26 px |
| Üst etiket, ruhsat adı | 22 / 19 px |

Metin/zemin kontrastı **≥4,5:1** — istisnasız.
