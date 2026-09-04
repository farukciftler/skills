# ffmpeg dikey kurgu hattı — bu makinede doğrulanmış (ffmpeg 8.1.2, Apple Silicon, 2026-08-13)

`scripts/build_stock_video.py` bu bulguların kodlanmış hâli. Script'i değiştirmeden önce burayı oku;
elle filter_complex yazacaksan da buradan başla.

## Klip normalizasyonu — her kaynağa aynı zincir

```
scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,
crop=1080:1920, setsar=1, fps=30, settb=AVTB, format=yuv420p
```

- `force_original_aspect_ratio=increase` + `crop` çifti yatay/dikey/kare HER kaynağı tek zincirle
  merkez-kırpar. Klasik `crop=ih*9/16:ih` yalnız yatay kaynakta çalışır — kullanma.
- `setsar=1` **atlanamaz**: SAR uyuşmazlığı concat filtresinde açık hata, demuxer'da **sessiz bozulma**.
- `fps=30` **filtre olarak** (çıkış `-r` değil): xfade/concat CFR ister. `-vsync` ffmpeg 8'de kalktı,
  tek dosya işlerde karşılığı `-fps_mode cfr`.
- `settb=AVTB` xfade'in "timebase do not match" hatasının kanonik ilacı.
- `format=yuv420p` zincirin SONUNDA: Pexels 4K bazen yuvj420p/4:2:2 geliyor; videotoolbox H.264 yalnız
  `nv12, yuv420p` kabul ediyor (yerelde doğrulandı).
- Konu merkezde değilse kırpmayı elle kaydır: `crop=1080:1920:x=<px>:0`.

## Birleştirme — üç yol, seçim tablosu

| Yol | Yeniden encode | Ne zaman |
|---|---|---|
| concat demuxer + `-c copy` | yok | sert kesme + kendi ürettiğin TEK TİP ara dosyalar. Yabancı dosyaları asla doğrudan verme: hata VERMEDEN donuk kare/kayma üretir |
| concat filtresi | var | sert kesme, tek komut, karışık kaynak |
| xfade zinciri | var | çapraz geçiş. ≤60 sn işte maliyet saniyeler — Shorts'ta varsayılan bu |

**xfade offset matematiği** (yerelde doğrulandı: 3×4 sn, f=0.5 → offset 3.5 ve 7.0, çıkış tam 11.000 sn):

```
offset_1 = d1 − f
offset_k = offset_{k−1} + d_k − f
toplam   = Σd − (N−1)·f
```

Süreleri **ffprobe ile ölç**, plandan alma — yanlış offset önceki klibi son karesinde sessizce dondurur.
Stok kliplerin sesi hiç haritalanmaz (`-an`); müzik ayrı girdi olarak sona eklenir — `acrossfade` derdi böylece hiç doğmaz.

## h264_videotoolbox

- **CRF yok.** `-b:v` (öngörülebilir, yükleme hedefi için doğru) ya da `-q:v 1–100` (yalnız Apple Silicon,
  eğrisi belgesiz — deneysel say).
- Hedef: `-b:v 12M -maxrate 16M -bufsize 24M -profile:v high -coder cabac -spatial_aq 1`.
  YouTube resmî tablosu 1080p için 8 Mbps (30fps) / 12 Mbps (60fps) der, dikeye özel rakam yayımlamaz;
  VT aynı kalite için x264'ten fazla bit ister, YouTube zaten yeniden kodlar — bol bit ucuz sigorta.
- **Karanlık/yavaş gradyanlı sahnede VT bantlar.** Çare sırayla: bitrate yükselt → `libx264 -crf 18 -preset fast`
  (60 sn'lik işte hâlâ <1 dk) → 10-bit HEVC (`hevc_videotoolbox -profile:v main10 -pix_fmt p010le -tag:v hvc1`,
  Apple donanımında 8-bit ile aynı hızda).
- Renk etiketle: `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv` — etiketsiz
  çıktı YouTube transkodunda ton kaydırır.
- Donanım decode serbest: `-hwaccel videotoolbox` (system-memory çıkışlı) CPU filtreleriyle uyumlu.
  **Tam-GPU yolu KAPALI: `scale_vt` kırpamıyor** (yalnız w/h/renk parametreleri var, yerelde doğrulandı) —
  esnetir, merkez-kırpma yapamaz. Doğru düzen: HW decode → CPU crop/scale/fps → HW encode.

## Ses

```
atrim=start=SS:duration=D, asetpts=PTS-STARTPTS,
afade=t=in:d=0.3, afade=t=out:st=D-0.3:d=0.3,
loudnorm=I=-14:TP=-1.5:LRA=11:measured_...:linear=true, aresample=48000
```

- `asetpts=PTS-STARTPTS` atlanırsa mux sesi geciktirir.
- **loudnorm İKİ geçişli** çalıştırılır: 1. geçiş `print_format=json -f null -` → `input_i/tp/lra/thresh` +
  `target_offset` oku → 2. geçişte `measured_*` + `linear=true`. Tek geçiş dinamik kompresör gibi davranır
  ve müzikte pompalar. Ölçüm **kesitin üstünde** yapılır, tam parçada değil — 45 sn'lik dilimin integrated
  değeri farklıdır.
- `loudnorm` içerde 192 kHz'e çıkar — ardına `aresample=48000` koy.
- `aac -b:a 384k -ar 48000 -ac 2` YouTube önerisinin aynısı.

## Dikişsiz döngü (Shorts otomatik başa sarar)

- Video: kurulan zaman çizelgesinin kuyruğunu başına xfade'le ("self-crossfade") → son kare = ilk kare.
  Ucuz alternatif: ilk ve son klip AYNI klip olsun, iki sınır da benzer hareket fazında kesilsin.
- Ses: kesiti parçanın BPM'inde **tam bar sayısına** kes (bar = 4×60/BPM sn) → döngü başa döndüğünde
  vuruş oturur. 0.3 sn'lik eşit fade'ler nefes gibi okunur; uzun fade-out döngüyü öldürür.

## Tuzak listesi

| Tuzak | Belirti | Çare |
|---|---|---|
| SAR uyuşmazlığı | concat hatası ya da mobilde bozuk oynatma | her zincirde `setsar=1` |
| Timebase uyuşmazlığı | "Non-monotonous DTS", ek yerinde takılma | ara dosyalara `-video_track_timescale 15360`; filtre yolunda `settb=AVTB` |
| VFR kaynak | büyüyen A/V kayması, yanlış offset | `fps=30` filtresi; sonra süreyi yeniden ÖLÇ |
| Piksel format karışımı | concat reddi, soluk/ezik ton | zincir sonunda `format=yuv420p`; full-range kaynağa `scale=in_range=pc:out_range=tv` |
| Etiketsiz renk | transkod sonrası ton kayması | çıktıya dört bt709/tv bayrağı |
| Ses akışı sayısı | biri sesli biri sessiz klip concat'i patlatır | yalnız `:v` haritala, müzik ayrı girdi |
| moov sonda | oynatıcı geç açılır | `-movflags +faststart` |
