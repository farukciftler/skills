# Motion Hattı — Reels · Story · TikTok

Dikey kısa video üretimi. Görsel kareler için `frame.py`, özel düzenler için
`layouts.py`; bu dosya **hareketli** içeriğin hattını anlatıyor.

## İçindekiler
1. Bu makinenin kısıtı — ffmpeg'de metin filtresi yok
2. Hattın parçaları
3. Ödünç alınanlar: reelsindustry
4. Türkçe TTS tuzakları — ölçülmüş
5. Ses karışımı
6. Tarif biçimi
7. Ölçülmüş süreler
8. Tuzaklar

---

## 1. Bu makinenin kısıtı

`ffmpeg -filters` çıktısında **`drawtext` ve `subtitles` YOK** — bu ffmpeg
libass, freetype ve fontconfig olmadan derlenmiş. Doğrulandı, filtre sayısı: 0.

Sonuç, hattın en önemli tasarım kararı: **bütün tipografi Pillow'da
rasterlenir**, ffmpeg yalnızca `overlay` yapar. Bu bir geçici çözüm değil:

| ASS yakma | PNG bindirme (bizim yol) |
|---|---|
| Font-config bağımlılığı, makineden makineye kayan render | Font dosyası sabit, çıktı bit-bit aynı |
| ASS sözdizimiyle sınırlı tipografi | Kerning, harf aralığı, satır kırma tam denetim |
| Marka rengi/kontrast denetimi yok | `frame.py` altyapısı aynen çalışır |

## 2. Hattın parçaları

| Betik | İş |
|---|---|
| `reels.py` | Tarif → bitmiş dikey video. Çekim akışı, Ken Burns, plaka bindirme, grade, ses karışımı |
| `vo.py` | ElevenLabs seslendirme + Türkçe okunuş düzeltmesi |
| `music.py` | Kendi prosedürel ambiyans üreticim — **artık yedek**, bkz. bölüm 3 |
| `frame.py` | Metin plakalarının tipografi altyapısı (`reels.py` ithal ediyor) |

```bash
python3 scripts/reels.py --recipe tarif.json --out cikti.mp4
python3 scripts/vo.py --text "..." --out vo.mp3 --voice george
```

## 3. Ödünç alınanlar: reelsindustry

`~/Documents/GitHub/reelsindustry` kullanıcının kendi dikey video üretim
merkezi — ölçülmüş bir hat. İki parçası buraya doğrudan bağlandı:

**`motor/ses/muzik.py` — prosedürel müzik.** Kendi `music.py`'ımı yazdım, sonra
ölçtüm ve onlarınki daha iyi çıktı:

| Motor | Konuşma bandı (300 Hz–4 kHz) enerji payı |
|---|---|
| reelsindustry `notr` / `denizci` / `antik` / `sanayi` | **%0,5 – 0,7** |
| benim `gece` / `acilis` | %2,3 – 2,7 |
| benim `veri` | %14,3 — seslendirmeyi yerdi |

Onların motoru konuşma bandını sentezde oyuyor. Müzikal kararları da markaya
birebir uyuyor: **üçlü yok** (majör "neşeli" / minör "hüzünlü" taahhüdünü
dayatmıyor), **vurmalı yok** (ritim aciliyet üretir, marka aciliyet dilini
yasaklıyor), **pedal ton** (zemin kaymıyor).

Temalar: `notr` `nordik` `antik` `bilim` `kasvet` `dogal` `denizci` `sanayi`.
Moonstone için `notr` (varsayılan), `antik` (marka/atmosfer), `denizci`
(Tuzla sahil bağlamı) denendi.

```python
import sys; sys.path.insert(0, "~/Documents/GitHub/reelsindustry")
from motor.ses import muzik
muzik.uret(16.5, "yatak.wav", tohum=11, tema="notr")
```

**`motor/ses/okunus.py` — Türkçe okunuş.** Bölüm 4.

`music.py` yedek olarak duruyor: reelsindustry erişilemezse hat çalışmaya
devam etsin diye.

## 4. Türkçe TTS tuzakları — ölçülmüş

reelsindustry'de ölçülmüş (ElevenLabs `eleven_multilingual_v2`, 2026-08-23).
Metin TTS'e **söylendiği** gibi gider, ekrana **yazıldığı** gibi:

| Yazım | Sonuç |
|---|---|
| `426 km` | **felaket** — «dört yüz yüzyüz mülandı vatid hilet» |
| `%74'ü` | «%50 kütüğü» |
| `II. Mehmet` | «3. Mehmet» |
| `DSİ` | «DSI» |
| `1453'te`, `3,5 milyon` | doğru, dokunulmaz |

`vo.py` metni önce `okunus.seslendirilebilir()`'den geçirir. `3.000 m²` →
"üç bin metrekare", `10.` → "onuncu" otomatik dönüşüyor.

**Ama ondalıklı sayı + birim dönüşmüyor:** `96,54 m²` olduğu gibi kalıyor ve
`426 km` ile aynı ailedendir. Bu yüzden Moonstone kuralı:

> **Seslendirme yuvarlar, ekran tam sayıyı gösterir.**
> Ses "doksan altı metrekare" der; `96,54 m²` görsel plakada yazılı durur.

Zaten daha doğal: hiç kimse konuşurken "doksan altı virgül elli dört" demez.

## 5. Ses karışımı

Yatak + seslendirme, **yan zincir sıkıştırma (sidechain ducking)** ile:
konuşma varken müzik otomatik geri çekilir.

```
[vo] highpass=90 → acompressor → apad → asplit
[muzik] volume → sidechaincompress(yan zincir = vo) → amix(vo) → alimiter
```

Referans seviyeler: konuşma −6…−12 dB, yatak konuşma altında −20…−30 dB,
boşluklarda −12…−18 dB. Tarifte `vo_gain` ve `music_gain` ile ayarlanır.

## 6. Tarif biçimi

```json
{ "fps":30, "xfade":0.5, "scrim":"bottom", "scrim_strength":0.80,
  "music_file":"yatak.wav", "vo_file":"vo.mp3", "vo_delay":1.1,
  "music_gain":0.5, "vo_gain":1.3, "vignette":0.11, "grain":6,
  "shots":[
    {"src":"klip.mp4","in":1.5,"dur":5.5,"grade":"eq=saturation=0.65"},
    {"kind":"still","src":"kare.jpg","dur":5.5,"z":[1.0,1.15],"focus":[0.5,0.40]}
  ],
  "plates":[
    {"t":0.9,"dur":4.6,"eyebrow":"...","title":"...","logo":true}
  ]}
```

- `shots[].grade` — kare bazlı renk düzeltmesi. Stok b-roll markanın
  lacivert-altın paletine oturmuyorsa burada düzeltilir:
  `eq=saturation=0.52:contrast=1.07,colorbalance=bs=0.12:bm=0.04:rm=-0.05`
- `plates[]` alanları `frame.py` ile aynı (eyebrow, rule, number, title, body,
  logo). Güvenli alan **140/400/70/130** — Instagram ve TikTok'un ortak, en dar
  alanı; tek sürümle ikisi de kurtulur.
- Duruk kareler `z` ve `focus` ile Ken Burns alır.

## 7. Ölçülmüş süreler

Bu makinede (M4 Pro, VideoToolbox):

| İş | Süre |
|---|---|
| 15 sn'lik Reels, 3 çekim, 2 plaka, ses karışımı dahil | **~5,5 sn** |
| 16 sn'lik müzik yatağı (reelsindustry motoru) | ~2 sn |
| Seslendirme (ElevenLabs, 124 karakter) | ~3 sn |
| Toplam: tariften bitmiş videoya | **~11 sn** |

## 7b. Aydınlık (açık) tema

Koyu tema varsayılan, ama akışta ritim ve daha sıcak bir ton için açık tema
sürümü var. Tarifte üç şey değişir:

```json
"scrim_color":"cream", "scrim_strength":0.90, "scrim_ease":0.8,
"vignette":0.07, "grain":4
```
ve plakalarda `"fg":"ink"`, `"accent":"#7A6116"`, `"logo_variant":"light"`.

**Altın açık zeminde `#B8992F` olarak kullanılmaz** — krem üzerinde 2,45:1,
okunmuyor. Açık tema altını `#7A6116` (5,26:1).

**Aydınlık b-roll markaya çekilir:** stok klipler fazla doygun ve yeşile
kaçıyor. `"grade":"eq=saturation=0.58:contrast=1.02:brightness=0.14"` hem
doygunluğu kısıyor hem koyu bölgeleri açıyor — böylece koyu metin okunuyor.

**Kaynak kırpmalarında koyu kenar şeridine dikkat.** Katalog sayfasından
kesilen render'ın üstünde ince bir koyu bant kalmıştı; satır/sütun ortalama
parlaklığına göre otomatik kırpmak temizliyor.

## 7c. Parlak müzik

reelsindustry motorunda `MODLAR`: `dor` `aeol` `lidyen` `miksolidyen`
`pentatonik`. "Mutlu ve heyecanlı" için:

```python
muzik.uret(18.0, "yatak.wav", tohum=21, kok="F2",
           mod="miksolidyen", akor_suresi=5.5, tema="dogal",
           tepe=0.46, islak=0.34)
```

- **`miksolidyen`** majör karakterli, yumuşak yedili — neşeli ama zorlamıyor.
  **`lidyen`** en parlak (yükseltilmiş dörtlü), "hayret" hissi verir.
- **`akor_suresi`** düşürmek hareket katıyor: 11 → 5,5 gözle görülür fark.
- **`tema='dogal'`** parlaklık 0,52 ile en yüksek ikinci; `nordik` 0,58.
- Kök yükseltmek (D2 → F2/G2) toparlıyor.

Ölçüm (18 sn, spektral merkez / konuşma bandı payı):

| Ayar | Merkez | Konuşma bandı |
|---|---|---|
| `miksolidyen` + `dogal` | **152 Hz** | %3,9 |
| `lidyen` + `nordik` | 140 Hz | %3,3 |
| `lidyen` + `dogal` | 115 Hz | %2,5 |
| `pentatonik` + `nordik` | 116 Hz | **%0,6** |

Parlaklık arttıkça konuşma bandı da doluyor. Kadın seslendirmede bu daha
kritik (temel frekans daha yüksek): parlak yatak kullanılıyorsa
`music_gain` 0,40–0,42'ye çekilir, ducking zaten devrede.

**Motorda vurmalı yok** — tasarım kararı. Yani "parlak ve sıcak" olur,
"ritimli ve enerjik" olmaz. Gerçek bir nabız isteniyorsa ayrı bir yol gerekir.

## 8. Tuzaklar

1. **Bir ffmpeg etiketi yalnızca bir kez tüketilir.** `[vo]` hem sidechain'e hem
   amix'e verilemez → `asplit=2[vo1][vo2]`.
2. **`sidechaincompress` yan zincir bitince durur.** Seslendirme videodan
   kısaysa müzik orada kesilir. Çözüm: `apad=whole_dur=<video süresi>`.
3. **`zoompan` tam piksel adımlarla çalışır, titrer.** Kaynağı önce 2× ölçekle,
   sonra zoompan uygula.
4. **Doğrusal zoom mekanik durur.** Kosinüs yumuşatma:
   `z = z0 + (z1-z0)*(1-cos(PI*on/(n-1)))/2`
5. **Plan çizimleri beyaz zeminli ve yatay.** `cover` kırpması onları yer;
   önce lacivert 1080×1920 tuvale `contain` ile yerleştirilip duruk kare
   olarak verilir.
6. **Parlak b-roll üzerinde altın etiket okunmuyor.** Scrim yetmez; klibi
   `brightness=-0.26` ile karart. Kontrast denetimi `frame.py`'de var ama
   video karelerinde otomatik çalışmıyor — gözle bak.
7. **Açık temada koyu metin, koyu b-roll üstünde kaybolur.** Scrim krem olsa
   bile klibin kendisi karanlıksa yetmez; klibi `brightness` ile aç.
8. **Metin plakası çekim geçişine taşmasın.** Plaka `t+dur` değeri xfade
   başlangıcını geçerse metin bir sonraki görüntünün üstünde asılı kalır.
