---
name: gorsel-uretim
description: >
  Moonstone Residence için sosyal medya ve web görseli üretir — Instagram
  story/Reels karesi, feed ve carousel slaytı, OG görseli, sayı kartı, alıntı
  kartı, plan/veri kartı, web bölüm arka planı ve site için AVIF/WebP/JPEG
  varyantları. Markalı çerçeveyi, okunabilirlik katmanını, tipografiyi, altın
  ayracı, logoyu ve "Temsili görseldir" notunu doğru güvenli alan içinde
  yerleştirir; renk düzeltmesini Apple Silicon GPU'sunda Core Image ile yapar.
  Şu ifadeler geçtiğinde kullan: "görsel hazırla", "post tasarla", "story
  görseli", "kapak yap", "bu fotoğrafı markaya uyarla", "kırp", "boyutlandır",
  "renk düzelt", "logo bas", "carousel slaytı", "web için optimize et",
  "AVIF üret", "güvenli alanı kontrol et". Bir görsel dosyası üretilecek ya da
  var olan bir görsel Moonstone kimliğine uyarlanacaksa, araç adı hiç geçmese
  bile devreye gir. Görsel *bulmak* için `pexels-gorsel-bulucu`, hangi ölçü ve
  içeriğin gerektiği için `post-uretimi.md` / `story-uretimi.md`.
---

# Görsel Üretim

Bu skill bir tasarım aracı değil, **markalı bir üretim hattıdır**. Aynı girdiyle
aynı çıktıyı verir, güvenli alanı ihlal etmez, marka renklerinin dışına çıkmaz
ve elle ölçü hesaplamayı ortadan kaldırır.

Bu makine bir **MacBook Pro / Apple M4 Pro** — 14 CPU çekirdeği (10 performans +
4 verim), 20 çekirdekli GPU, 24 GB birleşik bellek, Metal 4. Araç seçimi buna
göre yapıldı: ağır piksel işi GPU'ya (Core Image), toplu iş 10 performans
çekirdeğine, kodlama donanım kodlayıcısına (VideoToolbox) gider.
Ayrıntı ve gerekçe: `references/donanim-ve-araclar.md`.

## Hangi iş hangi araçla

| İş | Araç | Neden |
|---|---|---|
| Markalı kare kurmak (tipografi, logo, katman) | `scripts/frame.py` (Pillow) | Metin yerleşiminde tam denetim gerekiyor |
| Renk düzeltmesi, ton, netlik | `scripts/grade.swift` (Core Image) | GPU'da çalışır, sistemde hazır, kurulum yok |
| Ölçekleme, format çevirme, ICC | `sips` | Apple ImageIO — hızlı, **AVIF yazabiliyor** |
| Site varyantları (AVIF/WebP/JPEG) | `scripts/webexport.sh` | 10 çekirdeğe dağıtır |
| SVG → PNG (logo, ikonlar) | `rsvg-convert` | Vektörden istenen boyutta keskin çıktı |
| Video kesme, kodlama, ses atma | `ffmpeg` | `hevc_videotoolbox` / `h264_videotoolbox` donanım kodlayıcı |
| WebP | `cwebp` | sips WebP'yi yalnızca okuyor |

**Kurulu değil:** ImageMagick, libvips, exiftool, pngquant. Yukarıdaki set bu
işlerin tamamını karşılıyor; toplu iş binlerce dosyaya çıkarsa `brew install
vips` düşünülebilir, ondan önce gerek yok.

## 1. Markalı kare üretmek

```bash
python3 scripts/frame.py --preset ig-story --out cikti.png \
  --bg foto.jpg --bg-focus center --scrim bottom --scrim-strength 0.9 \
  --eyebrow "MOONSTONE RESIDENCE" --rule \
  --title "Ay taşının zarafeti" \
  --body "Tuzla Aydıntepe · 1+1 – 3+1 · 3.000 m² ticari alan" \
  --note "Temsili görseldir"
```

**Preset'ler ve güvenli alanları** (üst/alt/sol/sağ piksel):

| Preset | Ölçü | Güvenli alan |
|---|---|---|
| `ig-story` | 1080×1920 | 250 / 250 / 65 / 65 |
| `reels` | 1080×1920 | 108 / 320 / 60 / 120 |
| `tiktok` | 1080×1920 | 140 / 400 / 60 / 180 |
| `cross-9x16` | 1080×1920 | 140 / 400 / 60 / 180 — **Instagram + TikTok ortak**, tek sürümle ikisi |
| `ig-45` | 1080×1350 | 60 / 60 / 60 / 60 |
| `ig-kare` | 1080×1080 | 56 / 56 / 56 / 56 |
| `og` | 1200×630 | 48 / 48 / 56 / 56 |
| `web-hero` | 2560×1440 | 80 / 80 / 120 / 120 |

Aynı videoyu hem Instagram'a hem TikTok'a basacaksan `cross-9x16` kullan —
alttan 400 px boş kalır, ikisinde de metin kesilmez.

**Kullanışlı bayraklar**

- `--guides` — güvenli alan kılavuzunu üstüne basar. **Denetim içindir, yayına
  gitmez.** Yeni bir düzen kurarken önce bununla bak.
- `--number "3.000 m²" --number-size 210` — sayı kartı modu.
- `--kicker "Detaylı tablo profildeki bağlantıda"` — altın ikinci satır.
- `--scrim none|bottom|top|both|full` ve `--scrim-strength 0..1` —
  okunabilirlik katmanı. Fotoğraf üstüne metin gelecekse **en az 0.85**.
- `--bg-gradient "navy700,ink"` — fotoğrafsız marka zemini.
- `--logo dark|dark-mark|light|light-mark|none`, `--logo-pos`, `--logo-width`.
- `--align top|center|bottom`, `--offset`, `--safe-pad`.
- `--bg-blur 18` — arka planı bulanıklaştırıp metni öne çıkarır.

Renkler `ink · navy800 · navy700 · gold · goldlight · bronze · cream · white`
adlarıyla ya da hex olarak verilir. Palet `marka-kimligi.md`'den gelir; yeni
renk uydurma.

**Fontlar.** Marka fontları Cormorant Garamond ve Lora bu makinede kurulu
değil. Betik en yakın karşılığa düşüyor: display için **Didot**, gövde için
**Georgia** — ikisi de sistemde var ve markaya yakın duruyor. Gerçek marka
fontu için:

```bash
mkdir -p ~/Library/Fonts && cd ~/Library/Fonts && \
curl -sL "https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf" -o CormorantGaramond-Regular.ttf && \
curl -sL "https://github.com/google/fonts/raw/main/ofl/lora/Lora%5Bwght%5D.ttf" -o Lora-Regular.ttf
```

Kurulunca betik kendiliğinden onları kullanır, komut değişmez.

## 1b. Özel düzenler — `scripts/layouts.py`

`frame.py` tek sütunlu, metin-bloğu-altta bir kalıbı çok iyi yapıyor. O kalıbın
dışında kalan beş düzen ayrı dosyada; marka altyapısını `frame.py`'den ithal
ediyorlar, yani renk/font/logo/kontrast tek yerden yönetiliyor.

| Düzen | Ne işe yarar |
|---|---|
| `diptik` | İki planı **aynı ölçekte** yan yana — karşılaştırma. Ölçek net alana orantılı, kareye not düşülür. |
| `oran` | Plansız veri görseli: net m² orantılı yatay çubuklar. Altı tipi tek karede gösteren tek format. |
| `kanama` | Plan tam kanama + koyu bilgi paneli. Dergi serimi hissi. |
| `cerceve` | İnce altın çerçeve içinde ortalanmış plan. Davetiye/baskı hissi. |
| `daire` | Dairesel maske — logodaki ay/hilal motifiyle konuşur. |

```bash
python3 scripts/layouts.py     # hepsini üretir
```

Başka bir tip için ilgili fonksiyondaki plan dosyasını ve rakamları değiştir.
**Akışta ritim:** koyu kareler art arda gelince profil ızgarası tek lekeye
dönüşüyor; `cerceve` ve krem varyantlar bu yüzden var, süs değil.

## 2. Renk düzeltmesi

```bash
swift scripts/grade.swift girdi.jpg cikti.jpg gece 1.0
```

Görünümler: `gece` (doygunluk düşer, gölgeler laciverte kayar — koyu içerik
için), `gunduz` (hafif sıcak, kontrast az), `doku` (yüksek kontrast, düşük
doygunluk — malzeme plakaları için), `notr`. Son parametre yoğunluk (0–1).

Tek kare için `swift` yeterli (~0.8 sn). Onlarca dosya işlenecekse önce derle,
başlatma maliyeti kalkar:

```bash
swiftc -O scripts/grade.swift -o /tmp/msgrade
ls *.jpg | xargs -P 10 -I{} /tmp/msgrade {} graded/{} gece 0.8
```

`-P 10` performans çekirdeği sayısıdır; verim çekirdeklerini de zorlamak
toplam süreyi iyileştirmiyor.

## 3. Site için varyant üretmek

```bash
./scripts/webexport.sh cephe.jpg ./web moonstone-cephe 640 1280 1920
```

Her genişlik için AVIF + WebP + JPEG üretir, `srcset` satırlarını basar.
AVIF'i `sips` yazıyor — bu makinede `public.avif` yazılabilir formatlar
arasında, ayrı kodlayıcı kurmaya gerek yok.

## 3b. Motion içerik — Reels · Story · TikTok

Dikey video üretimi ayrı bir hat: `scripts/reels.py` (tarif → bitmiş video),
`scripts/vo.py` (ElevenLabs seslendirme + Türkçe okunuş düzeltmesi),
`scripts/music.py` (yedek prosedürel müzik).

```bash
python3 scripts/vo.py --text "..." --out vo.mp3 --voice george
python3 scripts/reels.py --recipe tarif.json --out cikti.mp4
```

**Bu makinedeki ffmpeg'de `drawtext` ve `subtitles` YOK** (libass/freetype/
fontconfig olmadan derlenmiş). Bütün tipografi Pillow'da rasterlenir, ffmpeg
yalnız `overlay` yapar — tercih edilen yol, geçici çözüm değil.

**Müzik ve Türkçe okunuş `reelsindustry` deposundan ödünç alınır**
(`~/Documents/GitHub/reelsindustry`). Gerekçesi ve ölçümleri
`references/motion-hatti.md` bölüm 3–4'te. Kısaca: onların müzik motoru
konuşma bandında %0,5 enerji bırakıyor (benimki %2,3–14), ve Türkçe TTS
tuzakları orada ölçülmüş.

**Seslendirme ölçülerek ayarlandı.** Varsayılan `eleven_v3 · hız 0,88 ·
kararlılık 0,50` — bu üçlü aynı metinde kelime hatasını %11'den %4'e,
düşen cümle konturunu %67'den %100'e çıkardı. Kararlılığı 0,75'e almak Türkçe
düşüş konturunu kırıyor. Üretilen sesi ölçmek için:

```bash
python3 scripts/vo.py --out vo.mp3 --denetle --text "…"       # üret + denetle
python3 scripts/vo.py --senaryo senaryo.json --out vo.mp3     # parçalı, dinamik
python3 scripts/soz_olcum.py --ses vo.mp3 --metin "…"          # yalnız ölç
```

**Tek düze ton için `--senaryo`.** Tek çağrıda bütün cümleler aynı perdede
kalıyor; metni parçalayıp her parçaya ayrı hız/stil/etiket/boşluk/kazanç
vermek ton çeşitliliğini 1,5'ten 3,2 yarıtona çıkardı. v3 ses etiketleri
(`[warmly]`, `[slowly][emphasizes]`) Türkçede sesli okunmuyor, ölçüldü.

Fonetik, prozodi kuralları, ölçüm eşikleri ve aracın sınırları:
`references/turkce-seslendirme.md`

**Kural:** seslendirme yuvarlar, ekran tam sayıyı gösterir. `96,54 m²` sese
girmez ("doksan altı metrekare" der), plakada yazılı durur.

**Karaoke altyazı** (`scripts/altyazi.py`): tarife `"altyazi": {...}` ekle,
kelime kelime yanan altyazı gelir. Kelime zamanlaması ElevenLabs Scribe'dan —
ayrı Whisper gerekmiyor. Sosyal videoların çoğu sessiz izlendiği için bu tek
başına en yüksek getirili ekleme.

Tam hat, tarif biçimi, ölçülmüş süreler ve tuzaklar:
`references/motion-hatti.md`
Sektörün nasıl kurduğu ve bizim nerede durduğumuz (Remotion kararı dahil):
`references/sektor-hatti.md`

## 4. Video

Reels/Story kesiti hazırlamak:

```bash
# 9:16'ya kırp, sesi at, donanım kodlayıcıyla yaz
ffmpeg -i kaynak.mp4 -t 8 -an \
  -vf "scale=1080:-2,crop=1080:1920" \
  -c:v hevc_videotoolbox -q:v 60 -tag:v hvc1 cikti.mp4
```

`hevc_videotoolbox` M4 Pro'nun medya motorunu kullanır; `libx264` ile aynı işi
yapmak birkaç kat daha uzun sürer ve CPU'yu doldurur. Kalite kritikse
`libx264 -crf 18` tercih edilebilir, ama sosyal medya yeniden kodladığı için
fark görünmez.

## Çalışma kuralları

**Her karede geçerli:**
- Metin ve logo güvenli alanın içinde. Yeni düzende `--guides` ile doğrula.
- Fotoğraf üstünde metin varsa scrim ≥ 0.85. Kontrastı gözle değil, gerçekten
  bak — bu segmentte okuyucu yaş ortalaması yüksek.
- Altın (`#B8992F`) açık zeminde gövde metni **olamaz** (2,45:1). Koyu zeminde
  serbest (7,1:1). Bkz. `marka-kimligi.md` kontrast tablosu.
- Render ya da proje görseli kullanıldıysa **"Temsili görseldir"** notu.
- Stok görsel kullanıldıysa `pexels-gorsel-bulucu` kırmızı çizgisi geçerli:
  görsel Moonstone'un kendisi sanılamaz.
- Doğrulanmamış veri yazma — fiyat, teslim, mesafe, daire sayısı.

**Bir seri üretirken:** aynı `--title-size`, `--scrim-strength` ve `--logo-pos`
değerlerini koru. Seri hissi ayrıntıların tekrarından doğar; her kareyi ayrı
ayarlarsan altı iyi kare çıkar ama bir set çıkmaz.

## Devir teslim

- **pexels-gorsel-bulucu** — arka plan fotoğrafını oradan al; `avg_color`
  değerini `--scrim-color` ya da `--accent` seçerken kullan.
- **post-uretimi.md / story-uretimi.md** — hangi preset, hangi metin uzunluğu,
  hangi kanca. Görsel üretmeden önce oradaki şablona bak.
- **marka-kimligi.md** — renk, tipografi, logo kuralları. Çakışma olursa o dosya
  kazanır.

## Referans

- `scripts/layouts.py` — frame.py'nin kalıbı dışındaki beş özel düzen.
- `references/motion-hatti.md` — dikey video hattı: reels.py, vo.py, ses karışımı, tuzaklar.
- `references/turkce-seslendirme.md` — Türkçe fonetik/prozodi, ölçülmüş TTS ayarları, denetim eşikleri.
- `references/sektor-hatti.md` — sektör hattı karşılaştırması, Remotion kararı, uyarlananlar.
- `references/donanim-ve-araclar.md` — bu makinenin profili, araç seçim
  gerekçeleri, ölçülmüş süreler, isteğe bağlı kurulumlar, paralel iş kalıpları.
