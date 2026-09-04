# Post-Prodüksiyon, Alternatif Modeller ve Hukuk

## 1. 5 sn Kling klibinden yayın Reels'ine — zincir

```
hazirla.py  →  kling_video.py (2 varyant)  →  seçim  →  [upscale/60fps]  →
katman.py (başlık/logo/not)  →  bitir.py (birleştir, kapanış kartı, müzik)  →  yayın
```

1. **Seçim.** Her çekimin varyantlarını yan yana izle; ölçütler
   `prompt-rehberi.md` §7. Reddedilen klip silinmez, `red/` altına taşınır —
   künyesiyle. Aynı prompt'un neden çalışmadığını bir dahaki sefer orada görürsün.
2. **Upscale / 60 fps — çoğu zaman gereksiz.** Kling pro katmanı 1080p verir;
   1080×1920 Reels için yeter. Instagram çoğu izleyiciye 30 fps'e yeniden
   kodlar. Yalnızca: kaynak görsel küçüktü ve klip yumuşak çıktıysa
   `fal-ai/topaz/upscale/video` (2×, Proteus; `target_fps` 60 isteğe bağlı,
   fiyatı ikiye katlar). Ucuz alternatif `fal-ai/seedvr/upscale/video`.
   Yerelde `minterpolate` kenarları bulanıklaştırır; RIFE (`fal-ai/rife/video`) temiz.
3. **Döngü.** `bitir.py --dongu` ileri+geri (boomerang) yapar; push-in'in tersi
   pull-out okunur, ambiyans için iyi, "içeri girme" anlatısı için garip.
   Kesintisiz döngü: başlangıç görselini bitiş görseli olarak da ver.
4. **Uzatma.** fal'da Kling extend yok. Yol: `bitir.py klip.mp4 --son-kare son.png`
   → `son.png` yeni çekimin başlangıç görseli → `--gecis 0.6` ile çapraz geçiş.
   v3'te `multi_prompt` ile tek istekte 15 sn'ye kadar çok plan da mümkün.
5. **Birleştirme.** `bitir.py` xfade (varsayılan 0,6 sn `fade`; `fadeblack`
   kapanışta), son karede bekleme (`--bekle`), kapanış kartı (`katman.py
   --sadece-logo`), açılış karartması. Kodlayıcı `h264_videotoolbox` 12 Mb/s,
   yuv420p, faststart — Instagram/TikTok yükleme için en sorunsuz.
   Arşiv kalitesi için `--kodlayici libx264` (crf 18).
6. **Müzik.** Kling'in yerel sesi kapalı (mimari klipte gereksiz, ücreti
   artırır). İş hesapları Instagram'ın ticari müzik kütüphanesini
   **kullanamaz**; Meta Sound Collection ya da lisanslı parça. Üretmek
   gerekirse `fal-ai/stable-audio-25/text-to-audio` (~$0,20, ticari kullanım)
   ya da `fal-ai/elevenlabs/sound-effects/v2` (ambiyans). `bitir.py --muzik`
   −14 LUFS'a normalize eder, son 1,5 sn'de kısar. Brief: "sessiz-derin
   ambiyans, tek düşük vuruş, trend ses yok".
7. **Marka katmanı.** Metin ve logo **asla AI karesine girmez**; `katman.py`
   ile post'ta biner. Güvenli alan `cross-9x16` (üst 140 / alt 400 / sol 60 /
   sağ 180) — tek sürüm Instagram + TikTok. K4: en fazla üç öğe.

## 1b. Devralınan kalıplar — weftrecords ve reelsindustry (2 Eylül 2026)

İki kardeş projeden (`~/Documents/GitHub/weftrecords`, `~/projects/reelsindustry`
+ `~/projects/instagram-reels`) ölçülmüş kararlar. `bitir.py` bunları uyguluyor;
buradaki liste "neden böyle" cevabıdır. Kaynak yolları parantezde.

**Bu makinede drawtext ve subtitles filtresi yok** (`ffmpeg -buildconf`: libfreetype/libass
yok; 2 Eylül 2026'da doğrulandı). Yazı yalnızca Pillow PNG + `overlay`. reelsindustry bunu
geri dönmeyeceği tercih olarak kaydetmiş: font depoda, çıktı bit-bit aynı, güvenli alan
mürekkep kutusundan ölçülebiliyor (`docs/ffmpeg-hatti.md:28-38`).

### Normalizasyon zinciri — her klipte, sırası değişmez
```
scale=W:H:force_original_aspect_ratio=increase:flags=lanczos,crop=W:H,setsar=1,fps=30,settb=AVTB,format=yuv420p
```
- `force_original_aspect_ratio=increase`+`crop`: yatay/dikey/kare her kaynağı tek zincirle
  ortalar; `crop=ih*9/16:ih` yalnızca yatayda çalışır, kullanma.
- `setsar=1` şart: SAR uyuşmazlığı concat filtresinde hata, concat demuxer'da **sessiz bozulma**.
- `fps=30` **filtre** olarak: xfade/concat CFR ister; ffmpeg 8'de `-vsync` yok.
- `settb=AVTB`: xfade "timebase do not match" hatasının kanonik çözümü.
- `format=yuv420p` zincir **sonunda**: 4:2:2/yuvj kaynaklar; VideoToolbox yalnızca nv12/yuv420p alır.
- `scale_vt` kırpamaz → tam GPU yolu kapalı; doğru düzen HW decode → CPU kırp/ölçek → HW encode.
(`reelsindustry/motor/kurgu/ffmpeg_serit.py:23`, `docs/ffmpeg-hatti.md:170-179`)

### xfade ofset matematiği
`offset_1 = d1 − f` · `offset_k = offset_{k−1} + d_k − f` · `toplam = Σd − (N−1)·f`.
Ofset **zincir uzunluğu** üzerinden birikir, kaynak zaman çizgisinden değil. Geçişten
kısa klip = dur, sessiz kısaltma yok. Geçiş tipi üretimde yalnızca `fade`; çeşitlilik
süreden gelir (0,3–0,55 sn). (`ffmpeg_serit.py:193-203`, `weftrecords/scripts/build_soc_video.py:121-133`)

### Kapanış kartı gövdeden SONRA
Kart zincire "süreyi sese çek" adımından önce eklenirse o adım kartı yer ve **hata vermez**
(reelsindustry'de 2,5 sn kart hiç görünmedi). `bitir.py` kartı en sona ekler ve `-t toplam`
ile mühürler. (`docs/ffmpeg-hatti.md:104-120`)

### Sabit görselden hareket (Ken Burns) — `durgun.py` kalıbı
- `zoompan` büyük kaynağa doğrudan uygulanınca zoom adımı tam piksele yuvarlanır → titreme.
  Çözüm: kaynağı önce **2× hedefe** (2160×3840) getir, zoompan'ı orada çalıştır, 1080×1920'ye in.
- Marka hızı: **en fazla %6 zoom / 9 sn**, kısa klipte orantılı az. Altı hareket: yakınlaş,
  uzaklaş, yukarı, aşağı, yakınlaş-sol, uzaklaş-sağ; art arda aynı hareket yok.
- Kat planı gibi çizgisel görsellerde AI değil bu yol. (`reelsindustry/motor/goruntu/durgun.py:7-71`)
- weftrecords: tek yönlü Ken Burns sinüsle döngülenemez; `--dongu-xfade` (kuyruk→baş çapraz
  geçiş) ile kapatılır. Sinüs salınımı kullanılacaksa **döngü sayısı tam sayı** olmalı
  (`render_video.py:100-107`).

### Oran değiştirirken siyah bant yerine bulanık kendi-dolgu
Yatay render'ı 9:16'ya kırpınca %65 kaybediyoruz. Alternatif: arkaya aynı karenin bulanık,
%18 karartılmış büyütülmüşü, öne tam kare (`--doldur bulanik`). weftrecords kapak
videosunda tipografiyi kırpmamak için bu yolu seçmiş. (`render_video.py:244-255`,
`build_cover_video_mlx.py:45-65`)

### Katman (overlay) kuralları
- PNG **tuval boyutunda** üretilir; videodan geniş overlay **hiç görünmez** (`race_overlay.py:181`).
- Zamanlama `enable='between(t,a,b)'`, yumuşatma alfa `fade`.
- Metin kutusu font metriğinden değil **mürekkepten** (alfa bbox) ölçülür; güvenli alan
  yüzdeyle değil kutuyla denetlenir — %2 eşik taşan başlığı "temiz" geçirmişti
  (`kart.py:124-142`, `docs/ffmpeg-hatti.md:60-94`). `katman.py` aynı yöntemle uyarır.
- Türkçe büyük harf: `"Prestij".upper()` → `PRESTIJ`; doğrusu `PRESTİJ` (`kart.py:35-46`).
  `katman.py` düzeltiyor. `"İ".lower()` de birleşik nokta üretir; karşılaştırmada dikkat.
- Instagram güvenli alan: üst 250 / alt 400 (`instagram-reels/pipeline/encode_reel.sh:97`);
  YouTube Shorts resmî reklam spesifikasyonu üst %10 / alt %25 / sağ %10.

### Ses
- **Tek geçişli loudnorm kompresör gibi pompalar.** Önce ölç (`print_format=json`), sonra
  `measured_*` + `linear=true` ile uygula; loudnorm içeride 192 kHz'e çıkar, ardından
  `aresample=48000` zorunlu. (`ffmpeg_serit.py:84-96, 245-249`)
- Platform hedefi: **Instagram −16 · YouTube/TikTok −14 LUFS**, TP −1,5. İki platforma
  giden takenin sesi yeniden ölçülür, görüntü `-c:v copy` (2 sn) (`motor/yayin/paket.py:23-45`).
- Seslendirme gelirse: müzik yatağı 1–3 kHz'de −7 dB oyulur (ünsüz anlaşılırlığı), sidechain
  `threshold=0.03:ratio=8:attack=15:release=350`; konuşma bandı SNR kapısı 14–30 dB
  (altı yatak yarışıyor, üstü yatak yok) (`ffmpeg_serit.py:34-81`, `denetim/preflight.py:61-90`).
- Müzik **videonun tamamı** kadar; kapanış kartı sessiz kalmasın. Bar hizası: toplam süreyi
  tam bar sayısına yuvarla, `floor(total/bar + 1e-3)` — kayan nokta bir barı sessizce
  düşürmüştü (`build_stock_video.py:115-127`).
- İş hesabı Instagram ticari müzik kütüphanesini kullanamaz (§1).

### Kodlama
- **Yayın: libx264 crf 17 veryfast High 4.2.** Instagram her yüklemeyi yeniden kodlar;
  temiz kaynak veren kazanır. 15 sn klip Apple Silicon'da saniyeler. VideoToolbox aynı
  algısal kalite için ~1,5–2× bit hızı ister ve koyu yavaş degradelerde bantlanır
  (`instagram-reels/pipeline/encode_reel.sh:136-140`, `encoding.md:5-14`).
- **Önizleme: h264_videotoolbox 12M** (`--hizli`), 4–8× hızlı; 30 varyant arasından seçerken
  kalite önemsiz.
- **Instagram/TikTok'a HEVC verme** — ingest'te ek transcode, kayıp orada. H.264 High, yuv420p.
- `-colorspace/-color_primaries/-color_trc bt709 -color_range tv`: etiketsiz çıktı
  transcode'da ton kaydırır. **Ölçüldü (2 Eyl 2026):** filter_complex'li çıktıda yalnızca
  CLI bayrağı primaries/trc yazmıyor; zincir sonuna `setparams=…` şart. Geniş gamut etiketi
  koyma, platform siler ve ton kayar.
- Instagram transcode rengi düzleştirir; master'ı hafif sıcak gönder
  (`eq=contrast=1.04:saturation=1.08` gibi, `--derece` ile; kimlik dosyasından, göz kararı değil).
- GOP 2 sn (`-g 60 -keyint_min 30`), `+faststart`, `-t toplam` (`-shortest` `-loop 1`
  görselle 4–5 sn sessizlik bırakır; süreyi ffprobe'dan al, `-t` ile mühürle — `build_video.py:11-17`).
- 60 fps'in üstü ingest'te 30'a düşer; yavaş hareket zaten 30'da akar.
- weftrecords ölçümü: filtre grafiği darboğazken **kodlayıcı seçimi hız kazandırmaz**
  (libx264 / VT / crf 22 aynı 41 sn); VT ancak hazır kareler gelince öder.

### QC — "dosyanın var olması işin bittiği anlamına gelmez"
1. `ffmpeg -v error -i out.mp4 -f null -` **sessiz** olmalı (pkill ile kesilen render bozuk
   dosya bırakır, ffprobe süreyi doğru okur ama akış çöker).
2. `ffprobe` süre = plan ±0,3 sn; ölçü 1080×1920; `yuv420p`; H.264; ses izi var; ≤ 60 sn.
3. `<out>.qc.json` raporu (plan/ölçülen süre, MB, Mb/s, kodlayıcı, LUFS girişi, sorunlar).
4. `--guvenli-alan`: UI bantlarını kırmızı basıp **gözle bak**. `--dongu-kontrol`: klibi
   kendine ekle, dikişe bak; sıçrama varsa çapraz geçişle örtme — kurgu hatası gibi okunur.
5. Kapak karesi 1. saniyeden (`--kapak 1.0`); ilk kare sık karanlık açılır. `-ss` girişten
   önce: arar, çözmez.
6. **Ölçümü süreç bittikten sonra yap.** Yazılırken okunan boyut üç yanlış karar verdirmiş
   (2,9 MB görünen 8,9 MB bitti). CRF eğrisini var olan encode'u yeniden kodlayarak ölçme
   (%65 sapma). Kıyaslamada üç koşu, ilkini at; meşgul makinede alınan ölçüm yanlı.
7. `pgrep -f` ile bekleme yapma: kabuk kendi komut satırını eşler, sonsuza kadar bekler;
   dosyayı bekle: `until [ -s out.mp4 ]`.

### Süreç
- **Skor seçmez, göz seçer.** Kontakt sayfası + ölçüm üretilir, klibi insan seçer;
  otomatik seçilen take yayına çıkmaz (`reelsindustry/docs/mimari.md:291-297`).
- Render'dan önce prob: 4 kare (%2/%27/%52/%77) tek PNG'de; "prob olmadan render yok".
- Take değişmez: aynı tohum (FNV-1a, `hash()` değil) aynı kurgu; reddedilen take
  benzerlik geçmişine girmez.
- Simülasyon %2, render %90: değmeyecek take'i hiç render etme — Kling'de karşılığı:
  önce `taslak` katmanı, sonra v3-pro.
- Paralel render: instagram-reels'te 3 iş → 2×, ötesi GPU doygun; "pahalı olan her aşama
  kritik yolda değildir, iki ölçümle maliyet modeli kur".
- Bulut video API'si reelsindustry'de bilinçli kapalı (30 sn avatar Reels $1,8–9); Moonstone'da
  kabul: klip başına $0,56, ay başına 12–16 klip.

## 2. Alternatif image-to-video modelleri (fal, Eylül 2026)

Kling varsayılan; A/B için aynı üç render'ı (cephe, iç mekân, drone) şu
ikisinde de dene ve **düz çizgi kararlılığını** puanla:

| Model | Uç nokta | $/sn | Not |
|---|---|---|---|
| Veo 3.1 Fast | `fal-ai/veo3.1/fast/image-to-video` | 0,10 (ses kapalı) | En iyi prompt takibi ve kare tutarlılığı; 4/6/8 sn; `aspect_ratio` 9:16 var |
| Seedance 2.0 Fast | `bytedance/seedance-2.0/fast/image-to-video` | 0,24 | I2V liderlik tablosunda 1.; `camera_fixed` anahtarı; 1080p pahalı |
| Hailuo 2.3 Fast | `fal-ai/minimax/hailuo-2.3-fast/standard/image-to-video` | ~0,03 | `[Push in]`, `[Static shot]` köşeli komutları deterministik; ucuz keşif |
| Wan 2.6 | `wan/v2.6/image-to-video` | 0,10–0,15 | Hızlı, ucuz; mimaride az test edilmiş |
| Luma Ray 3.2 | `luma/agent/ray/v3.2/image-to-video` | 0,06–0,24 | "akıcı dış mekân reveal" için övülüyor; Ray 2'de `loop` bayrağı |
| Pika 2.2 | `fal-ai/pika/v2.2/image-to-video` | — | Mimaride en zayıf geometri — kullanma |
| Sora 2 | — | — | fal'da kullanımdan kaldırıldı — kullanma |
| Runway Gen-4 | fal'da yok | — | Dış cephe çizgi kararlılığında saha kazananı, ama başka platform |

Topluluk özeti: Kling iç mekân derinliği ve fotogerçekçilikte iyi ama
istenmeyen hareket ekler; Veo kamera hareketinde; Runway/Luma dış cephe
kararlılığında. **Kesin kamera yolu gerekiyorsa 3D'den gerçek animasyon
her AI modelini geçer** — `gorsel-yon-referans.md` §7 Rota A.

## 3. Hukuk ve etik — kısa

- **Türkiye.** Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği
  değişikliği (RG 1 Temmuz 2026, yürürlük **1 Ağustos 2026**): yapay zekâ
  kullanımı tüketicinin ekonomik davranışını önemli ölçüde etkileyecekse
  **açık, anlaşılır ve ayırt edilebilir** biçimde belirtilir (Madde 18);
  gerçek kişi replikası yasak (Madde 27). Henüz yapılmamış binanın AI
  videosu bu eşiği büyük olasılıkla geçer → **etiketle.** Reklam Kurulu
  Ocak–Ağustos 2026'da yanıltıcı reklama 218,5 milyon TL ceza kesti.
- **AB Yapay Zekâ Yasası Madde 50** (2 Ağustos 2026'dan itibaren): gerçek
  gibi görünen AI görsel/video için görünür etiket; metadata tek başına
  yetmez, platformlar siler. Moonstone AB satıcısı değil ama içerik AB'de
  görünür; etiket bedava.
- **Meta.** Fotogerçekçi AI video için "Yapay zekâ ile üretildi" beyanı;
  reklamda zorunlu. Sonradan otomatik etiketlenmek, baştan beyan etmekten kötü.
- **Uygulama (K7).** Karede okunur "Temsili görseldir"; açıklamada
  `Görseller temsilidir; yapay zekâ desteğiyle hareketlendirilmiştir.`;
  Instagram "Made with AI" anahtarı açık.
- **Etik sınır.** Teslim edilemeyecek detayı hareketlendirme (malzeme,
  peyzaj, olmayan manzara); yaşandığı izlenimi veren insan/araba ekleme;
  inşaat başlamadan "yükseliyor" deme; her klibin künyesini sakla.

## Kaynaklar
fal.ai/models/fal-ai/topaz/upscale/video · fal.ai/models/fal-ai/seedvr/upscale/video ·
fal.ai/models/fal-ai/rife/video · fal.ai/learn/tools/best-image-to-video-apis-2026 ·
pixo.video/blog/seedance-vs-veo-vs-kling · visiomake.com/en/blog/best-ai-tools-for-architectural-animation-2026 ·
tripepismith.com/insights/music-in-reels-business-accounts ·
gun.av.tr (dijital reklamcılıkta yeni dönem, yapay zekâ düzenlemeleri) ·
celikhukuk.av.tr/reklamlarda-yapay-zeka-kullanimi-1-agustos-2026-yonetmeligi ·
artificialintelligenceact.eu/transparency-rules-article-50 · dezeen.com (10 Ağu 2026, AI render ve AB yasası) ·
trendekonomi.com (19 Ağu 2026, Reklam Kurulu cezaları).
