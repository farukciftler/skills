---
name: ambient-video-forge
description: Turns a still cover image plus an audio track into a long-form healing/ambient music video with layered procedural effects (rising smoke and incense plumes, drifting fog, dust motes, god rays, bokeh, starfields, water caustics, liquid warping of the artwork, bloom, grain, colour grading) in pure ffmpeg, no stock footage. Renders a short seamless loop and stream-copies it under the full track, so a 60-minute video costs minutes of CPU. Use whenever a video must be made from an album cover or still image, for a music track on YouTube, or with per-track variation across an album — "kapağı videoya çevir", "healing müzik videosu yap", "duman efekti ekle", "youtube için 1 saatlik video", "her parçaya farklı efekt", "ffmpeg ile duman/toz/ışık efekti", "lo-fi görsel yap", "sleep music videosu", "loop video hazırla", "spotify canvas". Trigger even when ffmpeg is never mentioned, if the deliverable is a video whose only footage is a still image plus effects. Pairs with retro-record-label and suno-composer.
---

# Ambient Video Forge

Build the video, don't describe it. The scripts here are tested; the trap list at
the bottom is a record of bugs that were actually hit and fixed, so read it
before hand-rolling a filter chain.

## The architecture, and why it is shaped this way

Long healing tracks are 20–70 minutes. Rendering a 70-minute 1080p video with
six animated effect layers is hours of CPU. So:

1. **Bake textures once.** `make_plates.py` writes still grayscale PNGs (fog,
   smoke plume, curling ink, dust, bokeh, stars, god rays, caustics, warp maps)
   with numpy fBm + domain warping. No per-frame procedural cost, no temporal
   noise flicker.
2. **Animate periodically.** ffmpeg pans, rotates and pulses those plates with
   `sin(2*PI*n*t/L)` where `n` is an integer. Frame 0 and frame L are then
   identical by construction — a perfect loop with no crossfade needed.
3. **Render only L seconds** (20–30 s), then `concat` the loop N times and mux
   the audio with `-c:v copy`. Verified: a 40-minute deliverable re-encodes
   nothing and takes seconds to assemble.

Everything else — the preset library, the album variation system — sits on top
of those three moves.

## Workflow

**Step 1 — check the machine.** `bash scripts/check_env.sh`. It reports the
required built-in filters, plus the optional frei0r/G'MIC extras and the exact
install command. Every preset works without the optional pieces.

**Step 2 — gather inputs.** You need a cover image and (for the final mux) the
audio. If the user has neither yet, `retro-record-label` makes covers at
3000×3000 and `suno-composer` makes the track. Ask what the music *is* before
choosing a look — the preset choice is a musical decision, not a visual one.

**Step 3 — pick a preset** from `assets/presets.json` (12 of them; each carries a
`note` saying what music it is for). Map by instrumentation and function:

| music | preset |
|---|---|
| ney, tanbur, makam, sufi/devotional | `sufi-incense` |
| 8-hour sleep, delta waves | `deep-sleep` |
| forest, birdsong, 432 Hz nature | `forest-mist` |
| space ambient, drone, binaural | `cosmic-drift` |
| water, whale song, flotation | `water-healing` |
| guided meditation, breathwork, yoga nidra | `candle-meditation` |
| lo-fi, tape ambient, study | `lofi-dust` |
| Tibetan bowls, gongs, sound bath | `singing-bowls` |
| rain, thunder, sleep-with-rain | `rain-window` |
| oud, qanun, Levantine/Anatolian | `desert-oud` |
| solo piano, winter, grief/comfort | `piano-snow` |
| dark ambient, dungeon synth | `dark-drone` |

**Step 4 — probe before committing.** Always:

```bash
python3 scripts/render_video.py --cover cover.png --preset sufi-incense \
    --out out/track.mp4 --stage probe --sheet look.png --res 800x450 --ss 1.0
```

That renders 4 frames from across the loop into one PNG in well under a minute.
**Look at it** (`view look.png`) and show it to the user. Iterating on a contact
sheet costs seconds; iterating on a finished render costs many minutes.

**Step 5 — render.**

```bash
python3 scripts/render_video.py --cover cover.png --audio track.flac \
    --preset sufi-incense --out out/01-nefes.mp4
```

**Step 6 — verify, then hand over.** Check duration matches the audio, and
confirm the loop closes: extract frame 0 and the last frame of
`out/_work/loop.mp4` and compare — mean absolute difference under ~3 is grain
only, i.e. seamless. Report the render time and file size.

## Albums: one identity, twelve variations

Fix `--album-seed` for the whole release and increment `--track`:

```bash
for i in 1 2 3; do
  python3 scripts/render_video.py --cover cover$i.png --audio track$i.flac \
    --preset sufi-incense --album-seed 4211 --track $i --out out/0$i.mp4
done
```

Same preset, same palette, same grade — but the plate seeds, oscillator phases,
speeds and opacities all shift inside a narrow band. The result reads as one
album rather than one template. `(album_seed, track)` is deterministic, so a
re-render months later produces the identical video. See
`references/album-system.md` for cross-preset album strategies and for when to
break identity deliberately (singles, a "dark" track in a light album).

## Tuning a look

Edit the preset in `assets/presets.json`, or copy an entry under a new name for
a one-off. The knobs, in order of how much they change the feel:

- `layers[].opacity` — how present the effect is. Smoke reads best at 0.3–0.5.
- `layers[].crush` — where the plate's blacks get clipped before blending. This
  is the single most important dial: see trap 1.
- `post.grade` — one of `warm-amber candle cool-teal moonlit sepia-dust
  monochrome rose-dawn deep-space forest neutral`.
- `post.vignette` (0–1) and `post.grain` (0–16).
- `base.zoom` / `base.drift` — camera breathing and drift. For meditation set
  `zoom_cycles` so the breath lands near 6/min (e.g. `loop: 20`,
  `zoom_cycles: 2`).
- `base.warp` — how much the artwork itself ripples (0.05 subtle, 0.17 aquatic).

Debug flags that save real time: `--layers N` builds only the first N layers,
`--no-post` skips bloom/grade/vignette/grain, `--dry-run` prints the
`filter_complex` without rendering. Bisecting with these is how the two colour
bugs below were found.

The full catalogue of plates, layer parameters, blend modes and hand-written
chains — including effects not wired into presets (heat haze, halation, light
leaks, letterbox, chromatic aberration, Ken Burns variants) — is in
`references/effects.md`. Read it before inventing a new effect.

## Cost, and how to stay inside it

Measured on **one** CPU core, so divide by your core count:

| task | cost |
|---|---|
| plate generation (per plate, 2880×1620) | 5–15 s, cached afterwards |
| 4-frame probe at 800×450 | ~45 s |
| loop render, 640×360, 8 s, `veryfast` | ~20 s |
| 1080p loop, 24 s, `slow`, ss=1.5 | roughly 15–40 min |
| concat + mux to 40 min output | seconds (video is stream-copied) |

Fast path while iterating: `--res 640x360 --ss 1.0 --fps 24 --x264-preset veryfast`.
Final path: default `--ss 1.5`, `--crf 16`, `--x264-preset slow`. `--ss` is
supersampling; it exists because pans move in whole pixels, and rendering above
target resolution then downscaling turns that stepping into sub-pixel motion.
Drop it to 1.0 only for drafts.

Encoding, YouTube delivery specs, banding, loudness, thumbnails and chapters:
`references/production.md`.

## Optional plugins

`frei0r-plugins` (136 filters) and `gmic` are installable with
`sudo apt-get install -y frei0r-plugins gmic` and are auto-detected — presets
degrade gracefully without them. What they actually buy, what they cost, and
which ones were measured to be *worse* than the built-ins is in
`references/plugins.md`. Two hard constraints from that file worth knowing up
front: **frei0r parameters cannot be animated** (ffmpeg exposes no per-frame
commands for them), and frei0r's blur is 3× slower than `gblur`.

## Traps (each of these was a real bug here)

1. **Screen-blending an un-crushed plate turns the artwork into milk.** `screen`
   lifts every non-black pixel, so a plate with mid-gray everywhere becomes
   global haze and eats contrast and saturation. Crush the plate's blacks first
   (`curves=all='0/0 0.4/0 1/1'`). This is the difference between "smoke drifting
   over the cover" and "someone spilled milk on the cover".
2. **`displace` forces one pixel format on all three inputs.** Feed it `gray`
   maps and ffmpeg silently converts your *artwork* to gray too. Keep the maps
   in the same format as the picture.
3. **`eq` and `colorchannelmixer` scramble channels on packed `rgb24`.** An
   orange sky came out magenta. Do the whole graph in planar `gbrp`, and run
   `eq` (a luma filter) inside a `yuv420p` island.
4. **ffmpeg's `vignette` is far stronger than it looks.** The default `PI/5` is
   already heavy. Measured corner luminance: `PI*0.05` keeps ~90%, `PI*0.20`
   keeps ~45%. The preset scale 0–1 maps into exactly that range.
5. **Don't hand-optimise `gblur`.** It is an IIR approximation, so cost barely
   grows with sigma (sigma=45 at 2880×1620 was ~48 ms/frame). Shrink-blur-grow
   saves little and looks blocky.
6. **Non-integer oscillator cycles break the loop.** Any motion period must
   divide L exactly. `sin_expr()` rounds `cycles` to an integer for this reason.
7. **Self-animating filters are not loop-safe.** `distort0r`, `vertigo`, `baltan`
   and friends advance on their own clock, so frame L ≠ frame 0. Use
   `--seamless xfade` for those: it renders L+X seconds and crossfades the tail
   into the head. Same applies to any temporal-feedback effect.
8. **Grain costs bitrate but buys smooth gradients.** Fog and bloom band badly
   in 8-bit; a little luma-only grain dithers it away. Never remove grain to
   shrink the file — lower the resolution instead.
