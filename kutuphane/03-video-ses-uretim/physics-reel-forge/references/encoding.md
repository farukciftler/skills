# Encoding on Apple Silicon

## The two-encoder strategy

Apple Silicon has a dedicated media engine exposed through VideoToolbox. It is fast and nearly free in CPU terms, but its quality per bit is worse than a good software encoder. Both facts matter, in different places:

| Use | Encoder | Why |
|---|---|---|
| Preview / seed sweep | `h264_videotoolbox` | Roughly 4–8× faster than software, ~20% CPU instead of 100%. When rendering 30 variants to decide which is worth keeping, quality is irrelevant and speed is everything. |
| Final master | `libx264 -crf 17 -preset veryfast` | Instagram re-encodes every upload. Feeding its encoder a cleaner source is what survives to the viewer. For a 15 s 1080×1920 clip this takes seconds on Apple Silicon, so the quality costs nothing worth counting. |

The trap worth naming: VideoToolbox **does not support CRF**. Passing `-crf` either errors or is silently ignored. It takes `-b:v` (bitrate, the predictable control) or `-q:v` (0–100, behaviour varies by ffmpeg version and chip generation). Starving its bitrate produces visible blocking, which is why a bitrate that would be generous for x264 can still look bad here. When using VideoToolbox for anything that ships, budget roughly 1.5–2× the bitrate x264 would need.

Do not use `hevc_videotoolbox` for Instagram. HEVC forces an extra transcode on ingest and that is where most quality loss happens. H.264 High profile, yuv420p.

## Platform targets

| Setting | Value |
|---|---|
| Container | MP4 |
| Video codec | H.264, High profile |
| Pixel format | yuv420p |
| Resolution | 1080×1920 (9:16) |
| Frame rate | 30 fps default; 60 only if motion needs it — above 60 gets dropped to 30 on ingest anyway |
| Bitrate | 8–12 Mbps |
| Audio | AAC, 128–256 kbps, 48 kHz, stereo |
| Colour | sRGB / Rec.709, no wide-gamut tags — they get stripped and can shift hues |
| Length | 7–25 s for this genre |
| File size | well under any cap at these settings |

Same master works for YouTube Shorts and TikTok. Render once.

Note on frame rate: capturing at 60 and delivering at 30 is often better than capturing at 30, because dropping every second frame from a 60 fps capture gives cleaner motion sampling than a 30 fps capture with no motion blur. Better still, capture at 120 and blend down to 30 for accumulation motion blur — see below.

## Recipes

**Preview (fast, disposable):**

```bash
ffmpeg -y -i take.avi \
  -c:v h264_videotoolbox -b:v 6M \
  -vf "scale=1080:1920:flags=lanczos" \
  -pix_fmt yuv420p -c:a aac -b:a 128k \
  preview.mp4
```

**Master (ships):**

```bash
ffmpeg -y -i take.avi \
  -c:v libx264 -crf 17 -preset veryfast -profile:v high -level 4.2 \
  -vf "scale=1080:1920:flags=lanczos" \
  -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -movflags +faststart \
  master.mp4
```

**From a PNG sequence plus WAV** (the full-resolution path):

```bash
ffmpeg -y -framerate 60 -i frames/frame_%05d.png -i audio.wav \
  -c:v libx264 -crf 17 -preset veryfast -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest \
  -movflags +faststart master.mp4
```

**Accumulation motion blur** — render at 4× the target rate, blend down. Genuinely photographic, and the clearest single upgrade available for fast-moving physics:

```bash
# 240 fps capture → 60 fps output with 4-frame blend
ffmpeg -y -i take_240.avi \
  -vf "tmix=frames=4:weights='1 1 1 1',fps=60" \
  -c:v libx264 -crf 17 -preset veryfast -pix_fmt yuv420p \
  blurred.mp4
```

Costs 4× render time. Reserve for clips already known to be good.

**Loop seam check** — concatenate the clip to itself and watch the join:

```bash
printf "file '%s'\nfile '%s'\n" "$PWD/clip.mp4" "$PWD/clip.mp4" > /tmp/loop.txt
ffmpeg -y -f concat -safe 0 -i /tmp/loop.txt -c copy /tmp/loop_check.mp4
```

**Safe-zone overlay** for checking framing (throwaway file, never publish):

```bash
ffmpeg -y -i master.mp4 -vf "
  drawbox=x=0:y=0:w=1080:h=250:color=red@0.3:t=fill,
  drawbox=x=0:y=1520:w=1080:h=400:color=red@0.3:t=fill
" -c:v h264_videotoolbox -b:v 4M safezone_check.mp4
```

**Verify what was actually produced** — do this on the first render of any new setup, because silently wrong dimensions from Retina scaling is a real failure mode:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,pix_fmt,nb_frames \
  -of default=noprint_wrappers=1 master.mp4
```

## Audio mastering

Physics audio is extremely peaky. Mobile playback is loudness-normalised, so an uncompressed mix gets turned down and loses all body.

```bash
ffmpeg -y -i master.mp4 \
  -af "acompressor=threshold=-18dB:ratio=4:attack=5:release=120,
       loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v copy -c:a aac -b:a 192k mastered.mp4
```

`loudnorm` in single-pass mode is approximate. For a series where consistency matters, run it in two-pass mode (measure, then apply the measured values) so every clip in the series lands at the same perceived loudness.

## Intermediate file hygiene

MJPEG AVI at `mjpeg_quality=0.95` runs to hundreds of MB for 15 seconds. A 30-variant sweep is tens of gigabytes. Transcode immediately after each render and delete the intermediate — `batch_render.py` does this by default. Losing a morning to a full disk mid-sweep is an avoidable and annoying way to lose a morning.
