# Album system: one identity, many tracks

## How variation is generated

`resolve()` derives `seed = album_seed * 7919 + track * 104729`, then for
`track > 0` perturbs each layer:

- `phase` — randomised over the full circle
- `opacity` — multiplied by 0.82–1.18, clamped to 0.05–0.95
- `pan` — multiplied by 0.8–1.25

What deliberately does **not** change: the layer stack, the plate types, the
grade, the vignette, the grain, the loop length. Those carry the album identity.
The plate *seeds* do change (they follow `seed`), so the actual smoke shapes and
dust distributions differ per track while their character stays constant.

Determinism: `(album_seed, track)` fully determines the output. Re-render in six
months and get the same video. Record the album seed in the release notes.

## Strategies

**Single preset, seed variation (default).** One preset, `--track 1..N`. Strongest
cohesion. Right for a meditation series, a sleep album, a makam cycle.

**Preset pair, alternating.** Two presets that share a grade — e.g.
`candle-meditation` and `sufi-incense` both sit in warm territory. Alternate them
across the tracklist. More variety, still one world.

**Arc.** Change grade progressively across the record while keeping the layer
stack: `rose-dawn` → `warm-amber` → `candle` → `moonlit` reads as dusk falling
across an album. Copy the preset under new names and change only `post.grade`.

**Break identity on purpose.** A single, a bonus track, or the one dark track on
a light album should look different — that is a signal, not an inconsistency.
Switch preset entirely and say so in the handover.

## Practical loop

```bash
SEED=4211
for i in $(seq 1 8); do
  python3 scripts/render_video.py \
    --cover covers/$i.png --audio tracks/$i.flac \
    --preset sufi-incense --album-seed $SEED --track $i \
    --out out/$(printf '%02d' $i).mp4
done
```

Plates are cached per `(seed, size)`, so each track regenerates its own plates
once. On a multi-core host run two or three of these in parallel rather than
raising `-threads` — ffmpeg's filter graph does not scale linearly across cores,
but separate processes do.

## Probe the whole album first

Render a contact sheet per track *before* committing to full renders:

```bash
for i in $(seq 1 8); do
  python3 scripts/render_video.py --cover covers/$i.png --preset sufi-incense \
    --album-seed 4211 --track $i --stage probe --sheet probes/$i.png \
    --res 800x450 --ss 1.0 --out out/$i.mp4
done
```

Then look at all eight sheets together. That is the moment to judge whether the
album reads as one album — and it costs minutes instead of hours.

## Interop

- `retro-record-label` produces the 3000×3000 covers and the release metadata.
  Square covers hit the `pillar` layout here (blurred blown-up background behind
  the intact artwork), which is the standard look for square art on 16:9.
- `suno-composer` produces the audio. Its musical decisions should drive the
  preset choice — instrumentation and tempo, not the cover's colours.
- `post-forge` handles social assets; do not use this skill for Instagram stills.
