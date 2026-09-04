# Production: encoding, delivery, long-form

## The loop-and-copy pipeline

`stage_loop` renders L seconds; `stage_mux` writes a concat list repeating that
file `ceil(audio/L)+1` times and muxes with `-c:v copy`:

```
ffmpeg -f concat -safe 0 -i concat.txt -i audio.flac \
  -map 0:v:0 -map 1:a:0 -c:v copy \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=<dur-6>:d=6" \
  -c:a aac -b:a 320k -ar 48000 -t <dur> -shortest \
  -movflags +faststart -fflags +genpts out.mp4
```

Verified: a 40-minute deliverable assembles in seconds and the video is
bit-identical to the loop. `-fflags +genpts` matters — without it concatenated
copies can produce non-monotonic timestamps that some players choke on.

Use the concat demuxer, not `-stream_loop -1`. Both work, but concat gives an
exact repeat count and a duration you can predict and check.

## Loop encoding settings

```
-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p
-g <2*fps> -keyint_min <fps> -x264-params aq-mode=3:deblock=1,1
-movflags +faststart
```

- **CRF 16** for the loop, not 20. The loop is re-shown dozens of times; any
  artefact is seen dozens of times. It costs disk once.
- **`aq-mode=3`** puts bits into flat gradient areas, which is exactly where fog
  and bloom band.
- **`-g 2*fps`** keeps keyframes frequent enough that seeking in a 60-minute
  video is responsive.
- **8-bit is fine** *if* grain is on. Without grain, smooth fog gradients band
  visibly on YouTube. 10-bit (`yuv420p10le`) removes banding without grain but
  loses hardware decode on older devices — only worth it for a premium upload.

## Frame rate

24 fps for slow, contemplative content (deep sleep, dark drone); 30 fps when
anything moves at a moderate pace (dust, caustics, rays). Slow pans at 24 fps can
strobe on high-contrast covers. Never 60 — the content has no fast motion and it
doubles both render time and file size.

## Resolution

1920×1080 is the default and the right answer for almost everything: healing
content is watched on phones and TVs, and 4K quadruples render time to make fog
slightly smoother. Go 2560×1440 only if the cover art is genuinely detailed.

For Spotify Canvas: 1080×1920 vertical, 3–8 s loop, no audio — set
`--res 1080x1920 --loop 8` and mute the mux stage (render only `--stage loop`).

## Loudness

`--loudnorm` normalises to `I=-14 TP=-1.0 LRA=11`, which is the streaming
target. Two cautions: healing and sleep music is often *intentionally* quiet, and
normalising it up can ruin the intent; and `loudnorm` in single-pass mode is
approximate. Ask before applying it, and prefer feeding an already-mastered file.

Fades are on by default (2 s in, 6 s out) because an abrupt cut at the end of a
sleep track is jarring. Set `--fade-out 0` if the master already fades.

## YouTube specifics

- Upload the mp4 as rendered; do not pre-compress to hit a size target.
- Chapters: put `00:00 Title` timestamps in the description. For a multi-track
  hour-long upload, generate them from the track durations — one line per track,
  first line must be `00:00`.
- Thumbnail: render one at 1280×720 from the same graph so it matches the video —
  `--stage probe` then crop a frame, or re-run the loop stage with `--loop 1` and
  grab frame 0. A thumbnail that matches the video's grade materially helps CTR.
- Titles/description/tags for release copy: that is `retro-record-label`'s job,
  not this skill's.
- 8-hour sleep uploads: L stays 24–30 s. The repeat count grows, nothing else.

## File size expectations

Grain and gradients are expensive. Measured: 640×360, CRF 18, grain 9 landed
around 5 Mbps. At 1080p CRF 16 with grain expect roughly 8–14 Mbps, so a
60-minute video is 3.5–6 GB. That is normal for this genre and YouTube re-encodes
it anyway. If you must shrink: drop resolution before dropping grain.

## Checks before handing over

1. `ffprobe -show_entries format=duration` matches the audio length.
2. Loop closes: extract frame 0 and the last frame of `_work/loop.mp4`; mean
   absolute difference under ~3 means seamless (grain accounts for the rest).
3. Play the mux point mentally: video is copied, so the only risk is a stale
   `loop.mp4` from an earlier preset — check the `_work` directory is the one you
   just wrote.
4. Report render time, output size and the preset/seed used, so the user can
   reproduce or iterate.
