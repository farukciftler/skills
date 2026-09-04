# Darkroom — Treatment Reference and Cookbook

`darkroom.py` runs an ordered chain of ops over a base image. The chain is the recipe, and order is everything: screening a faded image and fading a screened image produce different objects.

```bash
python scripts/darkroom.py in.jpg -o out/cover.png --size 3000 \
  --ops "square,auto,duotone=#101820/#e8dcc0,halftone=lpi:32;angle:15,grain=0.3,dust=0.2"

python scripts/darkroom.py in.jpg --preset riso-1990 -o out/cover.png
python scripts/darkroom.py in.jpg --alternatives bluenote-1958,riso-1990,vhs-1987 --out-dir work/
python scripts/darkroom.py --list-presets
```

Syntax: comma-separated ops. `name`, `name=value`, or `name=key:val;key:val`. `--seed` controls all noise; `-v` prints each step as it runs.

## Contents
1. The canonical order
2. Op reference
3. Presets, and when to leave them
4. Recipe cookbook
5. Debugging a chain that looks wrong

---

## 1. The canonical order

Chains that work almost always follow this sequence. Deviate deliberately, not accidentally.

```
1  geometry      square, resize, border
2  tonal prep    auto, levels, contrast, saturate, bw
3  distortion    warp, blur            ← before ink, so the ink follows the distortion
4  ink mapping   duotone, tritone, posterize, solarize, xerox, riso, halftone, cmyk
5  optics        bloom, misreg, vhs, sharpen
6  material      grain, dust, paper, ringwear
7  framing       vignette, border
```

The two rules that matter most: **tonal prep before ink mapping** (every ink op reads luminance, and a flat source maps to mud), and **material last** (grain and dust are the print and the wear; anything applied after them looks like a filter on top of a photo, which is exactly the tell to avoid).

## 2. Op reference

### Geometry

| Op | Params | Notes |
|---|---|---|
| `square` | `anchor:center\|top\|bottom` | centre-crop to square. The crop is a design decision — `top` on a portrait is a period-correct awkward crop. |
| `resize` | `_` = px | rarely needed; `--size` handles it. |
| `border` | `w:60`, `color:#f2e8d0` | insets the whole image inside a paper border. A real sleeve device for library and lounge. |

### Tonal prep

| Op | Params | Notes |
|---|---|---|
| `auto` | `lo:0.5`, `hi:99.5` | percentile black/white point stretch. **Put this in almost every chain.** Percentile, not min/max, so a single blown pixel doesn't defeat it. |
| `levels` | `lo:0–255`, `hi:0–255`, `gamma:1.0` | manual version when `auto` overshoots. |
| `contrast` | `_` = 1.2 | pivots on mid grey. |
| `saturate` | `_` = 1.0 | 0 = greyscale, >1 = pushed. |
| `bw` | — | luminance only. Do this before `duotone` when you want pure tonal mapping. |
| `posterize` | `_` = 6 | levels per channel. 4–8 for psych, 8–12 for early-digital banding. |
| `solarize` | `_` = 0.55 | inverts above threshold — Sabattier effect, authentic to 60s–70s darkroom experiments. |
| `fade` | `_` = 0.35 | sun-bleached: lifts blacks, compresses whites, drifts warm/yellow, drops saturation. The single most effective "this sleeve is fifty years old" op. Sits in tonal prep when you want the ink to inherit the fade, or at the end when you want the print faded. |

### Ink mapping

| Op | Params | Notes |
|---|---|---|
| `duotone` | `_` = `#dark/#light`, `gamma:1.0` | two-ink mapping across luminance. The workhorse of two-colour eras. `gamma` shifts where the midpoint lands. |
| `tritone` | `_` = `#dark/#mid/#light` | three-ink. The mid colour does the emotional work — pick it, then the ends. |
| `halftone` | `lpi:34`, `angle:15`, `shape:circle\|square\|line\|diamond`, `ink:#hex`, `paper:#hex`, `mono:1`, `soft:1.0` | AM dot screen. **`lpi` is resolution-relative** (dots across the canvas ÷ 10), so a recipe looks the same at 900px preview and 3000px delivery. 18–26 = chunky pop-art, 30–40 = visible newsprint, 55+ = disappears at thumbnail size. `angle:15` is the classic single-screen angle; `shape:line` gives a line screen for post-punk. `mono:0` screens each RGB channel instead. |
| `cmyk` | `lpi:38`, `gcr:0.7`, `shape`, `soft` | four-colour process at real separation angles (15/75/0/45), producing genuine rosettes. `gcr` controls how much black replaces CMY overlap. |
| `riso` | `colors:#a/#b/#c`, `offset:5`, `lpi:26`, `ink:0.95`, `paper:#f6efdd` | quantises to N spot inks, screens each, misregisters each independently, multiplies onto paper. `offset` is the whole point — 4–8px reads as a duplicator, 12+ as broken. |
| `xerox` | `_` = 0.6, `threshold:auto`, `ink:#hex`, `paper:#hex` | high-contrast threshold with edge chatter. Threshold defaults to the image median, so it never blacks out. Xerox has no midtones — that is correct. |

### Optics

| Op | Params | Notes |
|---|---|---|
| `bloom` | `_` = 0.35, `radius:` | halation off the highlights. Film and early video both do this; digital does not. |
| `misreg` | `_`/`offset:6`, `angle:20` | shifts red and blue in opposite directions. Press misregistration, and at small offsets it is the single most convincing "this was printed" cue. |
| `vhs` | `_` = 0.5, `scanline:` | chroma smear, chroma offset, tracking bands, scanlines. 0.3 = a good tape, 0.9 = a third-generation dub. |
| `warp` | `amp:10`, `freq:3` | sine displacement. Put it *before* ink mapping. Destroys fine detail, which is why psych bases should be graphic. |
| `blur` | `_` = 2 | mostly a preparation tool — a touch before `grain` sells "this lost detail in reproduction". |
| `sharpen` | `_` = 0.6 | unsharp mask. Use sparingly; sharpening a retro cover fights the whole premise. |

### Material

| Op | Params | Notes |
|---|---|---|
| `grain` | `_` = 0.28, `size:1.0` | luminance-weighted film grain — bites the midtones, spares blacks and whites, like real emulsion. `size:2–3` for pushed high-ISO clumping. |
| `dust` | `_` = 0.3 | specks plus a few thin emulsion scratches, alpha-blended rather than stamped. 0.15 = clean archive, 0.5+ = damaged. |
| `paper` | `_` = 0.6, `tone:#f4ecd6`, `texture:0.35` | multiplies the art onto a paper stock with a fibre field. The difference between "image" and "printed thing". |
| `ringwear` | `_` = 0.35 | vinyl ring wear plus corner scuff. Only for a "found record" concept or a mockup — do not ship it on a new release's cover art unless that is the concept. |
| `vignette` | `_` = 0.35 | lens falloff. Keep under 0.4 or it reads as a 2010 Instagram filter. |

## 3. Presets, and when to leave them

`--list-presets` prints all thirteen with their full chains. They are calibrated starting points, one per era in `era-playbook.md`:

`bluenote-1958` · `verve-1962` · `psych-1968` · `hipgnosis-1973` · `soul-1975` · `punk-xerox-1977` · `postpunk-1981` · `neon-1984` · `vhs-1987` · `riso-1990` · `grunge-1993` · `vaporwave-1995` · `print-cmyk`

Use a preset directly when generating alternatives to find a direction. Then **fork it**: copy the chain from `--list-presets`, change the inks to the brief's palette, and tune two or three numbers. A preset with the brief's actual colours in it beats a preset every time, and the palette is usually the only thing that needs to change.

`--alternatives a,b,c` runs several presets over one base in one pass and writes numbered files. It accepts raw chains too, so this works:

```bash
python scripts/darkroom.py photo.jpg --out-dir work/ --size 1500 --alternatives \
  "bluenote-1958,riso-1990,square,auto,bw,contrast=1.4,halftone=lpi:20;angle:0;shape:line,grain=0.3"
```

## 4. Recipe cookbook

**Two-colour jazz sleeve, brief palette.**
```
square,auto,bw,contrast=1.22,duotone=#0b1a2e/#e9dcbf,
halftone=lpi:32;angle:15;ink:#0b1a2e;paper:#e9dcbf,grain=0.22,dust=0.15,paper=0.45
```
Why: `bw` first so the duotone maps pure tone; the halftone inks match the duotone so the screen reads as the same press run.

**Newsprint press ad, three inks.**
```
square,auto,contrast=1.1,cmyk=lpi:30;gcr:0.8,misreg=offset:5;angle:18,
grain=0.16,paper=amount:0.55;tone:#efe6cf
```

**Riso two-colour, hand-made.**
```
square,auto,posterize=5,riso=colors:#ff4a3d/#1b3fa0;offset:7;lpi:24,
grain=0.18,paper=amount:0.6;tone:#f6efdd
```
Push `offset` to 10 and it becomes a jammed machine; drop `lpi` to 18 for a coarser stencil.

**Photocopied gig flyer, third generation.**
```
square,auto,contrast=1.3,xerox=0.85,halftone=lpi:20;angle:45;ink:#141414;paper:#f1eee6,
dust=0.6,grain=0.28
```

**Sun-bleached prog sleeve found in a crate.**
```
square,auto,fade=0.45,contrast=1.05,saturate=0.8,bloom=0.28,blur=1.2,
grain=0.36,dust=0.3,paper=0.3,vignette=0.32
```

**Late-night cable broadcast.**
```
square,auto,saturate=1.2,vhs=0.85,bloom=0.3,misreg=offset:6;angle:0,grain=0.3,vignette=0.3
```

**Solarised art-school sleeve.**
```
square,auto,bw,solarize=0.5,contrast=1.25,duotone=#141018/#c9c4b4,
halftone=lpi:26;angle:75,grain=0.25
```

**Psychedelic liquid poster.**
```
square,auto,saturate=1.5,warp=amp:20;freq:3,posterize=5,
tritone=#2b0a4a/#e0344f/#f7d84a,bloom=0.42,grain=0.28,dust=0.22
```

**Clean but printed** — when the brief wants restraint and only one cue that it is a physical object:
```
square,auto,contrast=1.06,misreg=offset:3;angle:25,grain=0.14,paper=amount:0.3
```
This chain is worth remembering. Three subtle ops do more for credibility than a stack of ten.

## 5. Debugging a chain that looks wrong

| Symptom | Cause | Fix |
|---|---|---|
| Everything is mud | ink mapping on a flat source | add `auto` (or `levels`) before the ink ops |
| Halftone invisible | `lpi` too high for the final size | drop to 20–34; check you are viewing at 100%, not in a contact sheet cell |
| Halftone looks like a moiré mesh | two screens at close angles | separate angles by ≥30°, or use `cmyk` which sets them correctly |
| Riso colours look muddy instead of overprinting | too many inks, or `posterize` missing | reduce to two inks, add `posterize=4–6` first |
| Xerox output is a black rectangle | source median very dark | `auto` first; or set `threshold:` explicitly |
| Grain looks like TV static | applied to a flat or already-noisy image | lower to 0.15–0.25, add `size:2` for clumping, and make sure it is last |
| Reads as "photo with a filter" | material ops applied before ink mapping | reorder per §1 |
| Looks AI-generated | full-frame symmetrical plate, untreated, no crop | crop into it, let type cover two-thirds, add `misreg` |
| Beautiful at full size, mud at 110px | too much detail, too little contrast between title and ground | coarser screen, fewer tones, bigger type |
| Noise changes every run | expected — it is seeded per run | pin `--seed` once you like a result, and record it |

Preview at `--size 900` or `1500` while iterating; run the keeper at `3000`. `lpi` is resolution-relative so the look transfers, but anti-aliasing and grain quality improve at full size.
