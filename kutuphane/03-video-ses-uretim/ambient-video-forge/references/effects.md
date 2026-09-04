# Effect cookbook

Contents: [Plates](#plates) · [Layer parameters](#layer-parameters) ·
[Blend modes](#blend-modes) · [Base motion](#base-motion) ·
[Warping the artwork](#warping-the-artwork) · [Post chain](#post-chain) ·
[Effects not in presets](#effects-not-wired-into-presets) ·
[Adding a new plate](#adding-a-new-plate) · [Format rules](#format-rules)

Every snippet here is written the way `render_video.py` emits it, so you can
paste one into a preset or into a hand-rolled `-filter_complex` and it will run.

## Plates

`scripts/make_plates.py` bakes these as grayscale PNGs. All are deterministic in
`(type, seed, size)` and cached by filename, so re-running a stage is free.

| plate | what it is | reads as |
|---|---|---|
| `fog` | wide, horizontally-stretched fBm with a vertical falloff | low-lying haze, ground mist |
| `plume` | tall fBm with strong domain warp, tapered sides | rising smoke, incense, a censer |
| `ink` | dense fBm, warped twice for tighter curls | full-frame curling smoke, ritual smoke |
| `dust` | ~520 small + ~90 medium soft blobs | dust motes, snow, pollen, fireflies |
| `bokeh` | 34 large discs, ~45% drawn as rings | out-of-focus lens bokeh, orbs |
| `stars` | 900 pinpoints + 25 bright + faint nebula fBm | starfield |
| `rays` | angular noise from a point above frame, radial falloff | god rays, light shafts through canopy |
| `caustics` | six interfering sine gratings | water light, heat shimmer; also a displace map |
| `warpmap` | smooth fBm centred on mid-gray | displacement map for liquid warping |
| `grain` | fine static noise | paper/print texture (prefer the temporal `noise` filter for dithering) |

Why smoke works: plain fBm looks like clouds, not smoke. The curl comes from
**domain warping** — sampling the noise field at coordinates pushed around by two
other noise fields. `plume` warps once with strength `w*0.11`, `ink` warps twice.
Raising the strength gives more turbulence; past ~0.2 it smears into mush.

Soft plates (`fog`, `plume`, `ink`, `rays`, `caustics`, `warpmap`) are computed at
half resolution and upscaled — 4× faster, no visible difference. Detail plates
(`dust`, `bokeh`, `stars`, `grain`) are computed at full size because upscaled
dots turn to mush.

## Layer parameters

```json
{ "plate": "plume", "blend": "screen", "opacity": 0.46, "crush": 0.30,
  "scale": 1.45, "pan": [70, -120], "cycles": 1, "phase": 0.0,
  "rotate": 1.2, "blur": 3, "tint": [1.0, 0.93, 0.82],
  "gamma": 1.0, "pulse": 0.05, "pulse_cycles": 3 }
```

- `opacity` — blend strength. Smoke 0.3–0.5, fog 0.2–0.35, dust 0.15–0.4,
  rays 0.14–0.25, bokeh 0.1–0.2, stars 0.3–0.5.
- `crush` — clip the plate's blacks below this value before blending. Defaults per
  plate live in `CRUSH` in `render_video.py`. Raise it when the frame goes milky,
  lower it when the effect disappears. This is the first dial to reach for.
- `scale` — plate size relative to frame. Anything above 1.0 gives pan headroom;
  above ~1.35 the plate gets upscaled, which is fine only if `blur >= 5`.
- `pan` — `[x, y]` pixel amplitude of the oscillation. Negative y drifts upward,
  which is what makes smoke rise. Values are in internal render pixels.
- `cycles` — how many full oscillations fit in the loop. **Must be an integer**
  or the loop point jumps. Use different `cycles` and `phase` per layer so the
  composite never appears to reverse direction.
- `rotate` — degrees of oscillating rotation. Small values (0.8–1.5°) add
  sub-pixel life and mask the pan reversal; `rotate` interpolates bilinearly, so
  it is the smoothest motion available.
- `blur` — gaussian sigma at output scale (multiplied by `--ss` internally).
- `tint` — `[r, g, b]` multipliers. Warm smoke `[1.0, 0.93, 0.82]`, cold mist
  `[0.85, 0.92, 1.0]`.
- `pulse` / `pulse_cycles` — brightness oscillation; makes dust twinkle and rays
  breathe. Run in a `yuv420p` island because `eq` is a luma filter.

## Blend modes

- `screen` — the default for anything luminous: smoke, fog, dust, rays, stars.
  Never darkens.
- `softlight` — for haze that should sit *in* the image rather than on top; gentler
  but desaturates, so keep opacity ≤ 0.35.
- `multiply` — darkening smoke (see `dark-drone`); needs `gamma` under 1.0 or it
  crushes the picture.
- `lighten` — harder-edged alternative to screen; good for sharp starfields.
- `overlay` — contrast texture, used for the `grain` plate in `lofi-dust`.
- `addition` — almost always too hot; use `screen`.

## Base motion

Breathing zoom plus drift, via `zoompan` with periodic expressions:

```
zoompan=z='1.0350+0.0315*sin(2*PI*1*on/780)'
       :x='iw/2-(iw/zoom/2)+18.0*sin(2*PI*1*on/30/26.0)'
       :y='ih/2-(ih/zoom/2)+10.0*sin(2*PI*1*on/30/26.0+1.5700)'
       :d=1:s=2880x1620:fps=30
```

`on` is the output frame index, so the zoom period is expressed in frames
(`loop*fps`) while x/y use `on/fps` = seconds. `d=1` means one output frame per
input frame, which is what you want with a `-loop 1` still.

Pan offsets land on whole pixels, so very slow motion can step visibly. Two
mitigations, both used here: render above target resolution and downscale
(`--ss 1.5`), and add a small oscillating `rotate` to a layer or two.

For meditation content, tie the zoom to breath: 6 breaths/min = one cycle per
10 s, so `loop: 20` with `zoom_cycles: 2`.

## Warping the artwork

`displace` shifts each pixel by `(map - 128)`, so a mid-gray map means no shift.
`eq=contrast` compresses the map around mid-gray to set the strength:

```
[warpmap]scale=...,crop=W:H:x='...sin...':y='...sin...',
         format=gbrp,eq=contrast=0.14,split=2[wx][wy];
[base][wx][wy]displace=edge=smear
```

`contrast=0.05` is a barely-there shimmer, `0.14` is water, `0.17` is a rainy
window. Use `caustics` instead of `warpmap` as the map for a more rhythmic,
grating-like ripple.

**Format warning:** all three inputs are forced to one pixel format. Gray maps
turn the artwork gray. Keep the maps in `gbrp`.

## Post chain

Order matters, and this order is deliberate:

1. **Bloom** — either frei0r `glow` (one filter, stable) or the built-in
   `split` → `curves=all='0/0 0.62/0 1/1'` → `gblur=sigma=34` → `blend=screen`.
   Threshold controls what glows; radius controls how dreamy.
2. **`colorbalance`** — the grade's shadow/mid/highlight push, RGB-native.
3. **`format=yuv420p`** — switch here, because everything below is a YUV filter.
4. **`eq`** — saturation and contrast.
5. **`vignette`** — mapped from 0–1 to `PI*0.05 … PI*0.20`. Measured corner
   luminance: `0.05` keeps ~90%, `0.13` ~70%, `0.17` ~55%, `0.20` ~45%.
6. **`scale` down from supersample** with `flags=lanczos`.
7. **`noise=c0s=N:c0f=t+u`** — luma-only temporal grain, last so it stays 1:1 with
   output pixels. Doubles as gradient dithering.

Grades available: `warm-amber candle cool-teal moonlit sepia-dust monochrome
rose-dawn deep-space forest neutral`. Each is a `colorbalance` + `eq` pair in
`GRADES`; add new ones there rather than inline in presets.

## Effects not wired into presets

Paste-ready fragments. Insert into the post chain at the position noted.

**Chromatic aberration** (after bloom, before grade) — `post.chroma` already
exposes this: `rgbashift=rh=2:bh=-2`.

**Halation** (warm bleed around highlights, after bloom):
```
split=2[h1][h2];[h2]curves=all='0/0 0.7/0 1/1',gblur=sigma=50,
colorchannelmixer=rr=1.0:gg=0.55:bb=0.35[hal];[h1][hal]blend=all_mode=screen:all_opacity=0.3
```

**Light leak** (a drifting warm wash from one corner; needs a `rays` plate):
```
[rays]scale=...,crop=W:H:x='...',rotate=a='0.4*sin(2*PI*t/L)',
gblur=sigma=60,format=gbrp,colorchannelmixer=rr=1.0:gg=0.7:bb=0.4[leak];
[base][leak]blend=all_mode=screen:all_opacity=0.18
```

**Heat haze without plates** (self-animating, needs `--seamless xfade`):
```
format=rgb24,frei0r=filter_name=distort0r:filter_params=0.05|0.35|y,format=gbrp
```

**Letterbox / cinematic bars** (very last, after grain):
```
pad=W:H+2*B:0:B:black
```
Better: render 1920×800 and pad to 1080 — you keep the pixels you paid for.

**Slow Ken Burns push instead of breathing** — drop `zoom` oscillation, set
`z='1.0+0.06*on/NF'` and use `--seamless xfade`. One-directional motion cannot
be sine-looped.

**Text overlay** (track title, for a single-track upload):
```
drawtext=fontfile=/path/font.ttf:text='Nefes':fontsize=48:fontcolor=white@0.75
:x=(w-tw)/2:y=h-160:alpha='0.75*min(1,max(0,(t-2)/2))'
```

## Adding a new plate

1. Write `plate_yourname(h, w, rng) -> float array in 0..1` in `make_plates.py`.
   Build from `fbm()`, `domain_warp()`, `_blobs()`, `norm01()`, `contrast()`,
   `vgrad()` — they compose well.
2. Register it in `PLATES` and add a `POLICY` entry (`blur` applied on save,
   `half` = safe to compute at half resolution).
3. Add a `CRUSH` default in `render_video.py`.
4. Generate it alone and *look* at it before wiring a preset:
   `python3 scripts/make_plates.py --out /tmp/p --seed 1 --size 1200x675 --types yourname`

## Format rules

Three rules, learned the hard way (see SKILL.md traps 2 and 3):

- Composite in **planar RGB (`gbrp`)**. Packed `rgb24` makes `eq` and
  `colorchannelmixer` scramble channels.
- Run **luma filters (`eq`, `vignette`, `noise`) inside a `yuv420p` island.**
- `displace` and `blend` unify formats across inputs — set the format you want
  *before* them, on every input, rather than trusting negotiation.
