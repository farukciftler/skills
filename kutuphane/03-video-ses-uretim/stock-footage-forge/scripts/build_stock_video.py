#!/usr/bin/env python3
"""
build_stock_video.py — stok kliplerden + müzik kesitinden dikey Shorts (9:16)
ya da yatay müzik videosu (16:9) kurar. Tek geçişli filter_complex: klip başına
normalize → xfade zinciri → (istenirse) PNG başlık bindirme → iki geçişli
loudnorm'lu ses. Kodlayıcı varsayılanı h264_videotoolbox (Apple Silicon).

Kullanım:
  python3 build_stock_video.py manifest.json [--dry-run]

Manifest şeması (JSON):
{
  "audio": "audio/track.wav",          // müzik master'ı (WAV)
  "audio_start": 114.0,                // kesitin parça içindeki başlangıcı (sn)
  "bpm": 86,                           // verilirse toplam süre TAM BAR sayısına
                                       // yuvarlanır (bar = 4*60/bpm) — döngü için
  "clips": [                           // sırayla; ses yok sayılır (-an)
    {"file": "a.mp4", "in": 0.0, "dur": 6.5},
    {"file": "b.mp4", "in": 2.0, "dur": 6.0, "crop_x": 300}   // crop_x: elle kadraj
  ],
  "xfade": 0.6,                        // çapraz geçiş süresi (0 = sert kesme)
  "fps": 30,
  "width": 1080, "height": 1920,       // 1920x1080 verilirse yatay müzik videosu
  "overlay": "title.png",              // opsiyonel, tuval boyutunda alfa PNG
  "out": "short.mp4",
  "encoder": "h264_videotoolbox",      // koyu/gradyanlı sahnede "libx264" seç
  "bitrate": "12M",
  "audio_fade": 0.3,                   // giriş/çıkış ses fade'i (uzun fade döngüyü öldürür)
  "loudnorm_target": -14.0
}

Süre matematiği: toplam = Σdur − (N−1)·xfade. bpm verildiyse toplam en yakın
tam bara indirilir ve fark SON klibin süresinden düşülür. Klip süreleri ffprobe
ile ölçülür ve manifest'teki dur gerçek süreyi aşarsa kırpılır (uyarıyla).
"""

import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def die(msg):
    sys.exit(f"HATA: {msg}")


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def measure_loudnorm(audio, start, dur, fade, target):
    """1. geçiş: kesitin gerçek ölçümleri. Tam parçada değil kesitte ölçülür."""
    af = (f"atrim=start={start}:duration={dur},asetpts=PTS-STARTPTS,"
          f"afade=t=in:d={fade},afade=t=out:st={max(0.0, dur - fade)}:d={fade},"
          f"loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json")
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(audio),
         "-af", af, "-f", "null", "-"],
        capture_output=True, text=True)
    # loudnorm JSON'u stderr'in sonunda
    tail = r.stderr[r.stderr.rfind("{"):]
    try:
        m = json.loads(tail[:tail.rfind("}") + 1])
    except (ValueError, IndexError):
        die(f"loudnorm ölçümü ayrıştırılamadı:\n{r.stderr[-800:]}")
    return m


def build(manifest_path, dry_run=False):
    mf = json.loads(Path(manifest_path).read_text())
    base = Path(manifest_path).resolve().parent

    def p(rel):
        q = Path(rel)
        return q if q.is_absolute() else base / q

    audio = p(mf["audio"])
    if not audio.is_file():
        die(f"ses yok: {audio}")
    clips = mf["clips"]
    if not clips:
        die("clips boş")
    W, H = int(mf.get("width", 1080)), int(mf.get("height", 1920))
    fps = int(mf.get("fps", 30))
    xf = float(mf.get("xfade", 0.6))
    fade = float(mf.get("audio_fade", 0.3))
    target = float(mf.get("loudnorm_target", -14.0))
    enc = mf.get("encoder", "h264_videotoolbox")
    out = p(mf.get("out", "stock_video.mp4"))

    # --- klipleri ölç, süreleri gerçeğe kırp
    durs = []
    for c in clips:
        f = p(c["file"])
        if not f.is_file():
            die(f"klip yok: {f}")
        real = ffprobe_duration(f)
        start = float(c.get("in", 0.0))
        want = float(c.get("dur", real - start))
        avail = real - start
        if want > avail + 0.01:
            print(f"UYARI: {f.name} {want:.1f} sn istendi, {avail:.1f} sn var — kırpıldı")
            want = avail
        durs.append(want)

    n = len(clips)
    total = sum(durs) - (n - 1) * xf

    # --- bar hizalama: döngü başa döndüğünde vuruş otursun
    if mf.get("bpm"):
        bar = 4 * 60.0 / float(mf["bpm"])
        # 1e-6 payi: 33.100/4.1379 = 7.9992 gibi kayan nokta kirintisi bir tam
        # bari sessizce dusurmesin (WR-040'ta final klibi 4 sn kirpmisti)
        bars = math.floor(total / bar + 1e-3)
        snapped = bars * bar
        trim = total - snapped
        if trim > durs[-1] - 1.0:
            die(f"bar hizalama son klibi {trim:.2f} sn kısaltmak istiyor, klip taşımıyor")
        durs[-1] -= trim
        total = snapped
        print(f"bar hizalama: {bars} bar × {bar:.3f} sn = {total:.3f} sn (son klipten −{trim:.2f})")

    # --- filter_complex
    norm = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={W}:{H}{{cx}},setsar=1,fps={fps},settb=AVTB,format=yuv420p")
    parts, inputs = [], []
    for i, c in enumerate(clips):
        inputs += ["-i", str(p(c["file"]))]
        cx = f":x={int(c['crop_x'])}:y=0" if c.get("crop_x") is not None else ""
        start = float(c.get("in", 0.0))
        parts.append(
            f"[{i}:v]trim=start={start}:duration={durs[i]},"
            f"setpts=PTS-STARTPTS,{norm.format(cx=cx)}[v{i}]")

    if n == 1 or xf <= 0:
        chain = "".join(f"[v{i}]" for i in range(n))
        parts.append(f"{chain}concat=n={n}:v=1:a=0[vraw]")
    else:
        off, prev = 0.0, "v0"
        for i in range(1, n):
            off += durs[i - 1] - xf
            lbl = "vraw" if i == n - 1 else f"x{i}"
            parts.append(f"[{prev}][v{i}]xfade=transition=fade:"
                         f"duration={xf}:offset={off:.3f}[{lbl}]")
            prev = lbl

    # Yayina ozel renk derecelendirmesi. Stok klipler her yerden geliyor; sanatci
    # paletine cekmezsen video "stok gorunuyor". WR-044'te olculmustu: hat sicak
    # bir plakayi magentaya tasiyabiliyor, yani derecelendirme goz kararina
    # birakilamaz — manifest'e YAZILIR ve render sonrasi kanal farki OLCULUR.
    grade = mf.get("grade")
    if grade:
        parts.append(f"[vraw]{grade}[vgr]")
        src = "vgr"
    else:
        src = "vraw"

    a_idx = n
    ov = mf.get("overlay")
    if ov:
        ovp = p(ov)
        if not ovp.is_file():
            die(f"overlay yok: {ovp}")
        inputs += ["-i", str(ovp)]
        a_idx = n + 1
        parts.append(f"[{src}][{n}:v]overlay=0:0:format=auto,format=yuv420p[vo]")
    else:
        parts.append(f"[{src}]null[vo]")
    inputs += ["-i", str(audio)]

    astart = float(mf.get("audio_start", 0.0))
    m = measure_loudnorm(audio, astart, total, fade, target)
    print(f"loudnorm 1. geçiş: I={m['input_i']} TP={m['input_tp']} LRA={m['input_lra']}")
    parts.append(
        f"[{a_idx}:a]atrim=start={astart}:duration={total:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:d={fade},afade=t=out:st={total - fade:.3f}:d={fade},"
        f"loudnorm=I={target}:TP=-1.5:LRA=11:"
        f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
        f"offset={m['target_offset']}:linear=true,aresample=48000[ao]")

    # crf manifest'ten ayarlanabilir. Varsayilan 18 kisa yayinlarda dogru ama
    # UZUN yayinda dosyayi patlatiyor: WR-013'te 40 dakikalik 1080p24 render
    # ~10 Mbit/s ile 2.9 GB'a gidiyordu ve DISK DOLDUGU icin 19. dakikada oldu.
    # Yavas manzara goruntusunde crf 21-22 gozle ayirt edilmiyor, dosya yariya
    # iniyor — ve tarayiciya 3 GB'lik Blob sokmak zaten ayri bir risk (WR-033).
    vcodec = (["-c:v", "libx264", "-preset", "fast",
               "-crf", str(mf.get("crf", 18))]
              if enc == "libx264" else
              ["-c:v", "h264_videotoolbox", "-b:v", mf.get("bitrate", "12M"),
               "-maxrate", "16M", "-bufsize", "24M",
               "-profile:v", "high", "-coder", "cabac", "-spatial_aq", "1"])

    cmd = (["ffmpeg", "-y", "-hide_banner"] + inputs +
           ["-filter_complex", ";".join(parts),
            "-map", "[vo]", "-map", "[ao]"] + vcodec +
           ["-colorspace", "bt709", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-color_range", "tv",
            "-c:a", "aac", "-b:a", "384k", "-ar", "48000", "-ac", "2",
            "-t", f"{total:.3f}", "-movflags", "+faststart", str(out)])

    print(f"plan: {n} klip, xfade {xf} sn, toplam {total:.2f} sn, {W}x{H}@{fps}, {enc}")
    if dry_run:
        print(" ".join(cmd))
        return
    subprocess.run(cmd, check=True)

    # --- doğrulama: dosya var demek iş bitti demek değil (ölç, gözle geçme)
    got = ffprobe_duration(out)
    ok = abs(got - total) < 0.5
    print(f"çıktı: {out}  süre {got:.2f} sn (plan {total:.2f}) "
          f"{'OK' if ok else '!! SAPMA — ek yerlerini kontrol et'}  "
          f"boyut {out.stat().st_size / 1e6:.1f} MB")
    if not ok:
        sys.exit(2)


if __name__ == "__main__":
    if not shutil.which("ffmpeg"):
        die("ffmpeg yok")
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    if len(args) != 1:
        die("kullanım: build_stock_video.py manifest.json [--dry-run]")
    build(args[0], dry_run="--dry-run" in sys.argv)
