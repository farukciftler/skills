# Delivery — Specs, Gates and Handoff

## Contents
1. Platform specs
2. The rejection checklist
3. The thumbnail gate
4. Type-on-plate legibility
5. Deliverable set and folder layout
6. Mockups
7. Physical formats
8. Handoff format

---

## 1. Platform specs

**Design once at 3000 × 3000, sRGB, and submit that file everywhere.** Platforms downscale internally, and standardising is more robust than chasing per-store numbers.

| Target | Spec | Notes |
|---|---|---|
| Distributors (DistroKid, CD Baby, Believe, FUGA) | 3000×3000 min 1400×1400, JPG/PNG, sRGB | most reject under 1400 at upload |
| Spotify | 3000×3000 recommended, min 640×640 | recompresses to JPEG — very high-frequency detail smears, so a fine halftone can turn to noise |
| Apple Music | 3000×3000, sRGB with embedded profile | strictest reviewer; missing colour profile can cause display issues |
| YouTube Music | inherits from the distributor | the art track thumbnail comes from this same square |
| Bandcamp | upload the largest you have | displays art bigger than anyone else |
| SoundCloud | 3000×3000 works; displayed small | plus a 2480×520 banner if wanted |
| File size | keep under 4 MB to satisfy the strictest gate | if rejected for size, re-export JPEG at quality 85–92 rather than reducing dimensions |
| YouTube video thumbnail | 1280×720, under 2 MB | a square cover on a 16:9 field with a colour bar either side beats a stretched crop |
| YouTube Shorts / vertical | 1080×1920 | keep the title inside the central 1080×1420 |

Export both: a PNG master (type stays crisp) and a JPEG at quality 90 with `subsampling=0` for upload. `render.py --jpeg 92` writes both.

## 2. The rejection checklist

Run every line before handoff. These are the actual causes of delayed releases, not hypothetical ones.

- [ ] **No URL, social handle, email or phone number** anywhere on the artwork. Apple in particular rejects on this alone.
- [ ] **No promotional text** — "Out Now", "New Single", "Free Download", "Follow me", a price.
- [ ] **No self-applied Explicit or Parental Advisory badge.** Platforms add it from the metadata flag.
- [ ] **No platform logos** (Spotify, Apple, YouTube) and no distributor marks.
- [ ] **No third-party trademarks, brand logos, or sports/film/TV imagery.**
- [ ] **No copyrighted photograph or artwork without rights** — see `imagery.md` §7.
- [ ] **Artist and title spelled correctly**, matching the metadata sheet exactly. A mismatch between artwork and metadata is a rejection reason and a spelling error in the type is unfixable after release.
- [ ] **Square, 1:1, no letterboxing**, no transparent edges.
- [ ] **sRGB**, not CMYK, for the digital file.
- [ ] **Legible at 110px** (see §3).
- [ ] **Nothing misleading** — artwork should represent the music, not imply a different genre, a compilation, or another artist.
- [ ] **Turkish glyphs rendered**, not fallback boxes or a mid-word font switch.

If a "found record" concept added `ringwear` or heavy `dust`, confirm the wear reads as art direction rather than as a damaged file. It usually does at full size and can look like a corrupt upload at thumbnail — check both.

## 3. The thumbnail gate

```bash
python scripts/contact_sheet.py out/*.png -o review/sheet.png --thumb 110
```

Look at the 110px sheet and answer two questions: **can you read the artist name, and can you tell these alternatives apart?** A playlist row, a search result and a phone lock screen all live between 64 and 160px.

When a cover fails:

- Cut words before shrinking type. A three-word title at 140px beats a six-word title at 70px.
- Increase the contrast between type and ground — a solid band, a crop into a flat area, or a second ink.
- Simplify the plate. Detail that reads as texture at 3000px reads as grey at 110px.
- Never solve it with a drop shadow on every line.

## 4. Type-on-plate legibility

Three period-correct solutions, in order of preference:

1. **Crop the plate so the type lands on a flat area.** What Reid Miles did — the photo is cropped to make room, not the type shrunk to fit.
2. **A solid colour band behind the credits.** Authentic to 70s soul and library sleeves, and it guarantees contrast.
3. **A hard offset in a second ink** (`text-shadow: 6px 6px 0 var(--ink)`). Correct for 70s fat-slab type. Soft/blurred shadows are not period and read as amateur.

Check the mid-tone case specifically: light type on a mid-grey plate is the most common failure and it looks fine on a bright monitor.

## 5. Deliverable set and folder layout

```
release/
├── cover-3000.png            master, type crisp
├── cover-3000.jpg            q90, sRGB, <4MB — the upload file
├── alternatives/
│   ├── 01-<concept>.png      the rejected directions, kept for the record
│   ├── 02-<concept>.png
│   └── 03-<concept>.png
├── youtube/
│   ├── thumbnail-1280x720.png
│   └── vertical-1080x1920.png    (if a Short is planned)
├── work/
│   ├── plate.png             untreated base
│   ├── treated.png           darkroom output
│   ├── cover.html            the typography layer
│   └── recipe.txt            plate command + darkroom chain + seed
└── metadata.md               naming rationale + YouTube pack + DSP sheet
```

`recipe.txt` is not optional. It is what makes the *next* single look like the same artist:

```
plate:    plates.py geo --palette bluenote --size 3000 --seed 11 --set "n:4"
darkroom: square,auto,bw,contrast=1.22,duotone=#0b1a2e/#e9dcbf,
          halftone=lpi:32;angle:15;ink:#0b1a2e;paper:#e9dcbf,grain=0.22,dust=0.15,paper=0.45
seed:     7
fonts:    Archivo Black (display) / Libre Franklin (grotesk) / Space Mono (meta)
signature device: catalogue number block bottom-left, STEREO badge bottom-right
```

## 6. Mockups

Only when the user needs to *sell* the cover — a pitch, a social announcement, a store page. The release itself needs the flat square.

Build them in HTML, not by editing the master:

- **Vinyl sleeve**: the square with a 2–3% inner shadow on two edges, a visible spine line, and a slight perspective. Add `ringwear=0.25` to a *copy* for a used-record look.
- **Cassette J-card**: 4 × 2.625 in at 300 dpi = 1200 × 788 px plus bleed.
- **Crate scene / stack**: two or three covers overlapping at slight rotations.

Hand social-post versions to `post-forge`, which owns that surface.

## 7. Physical formats

If the release is being pressed, the digital master is not enough:

| Format | Size at 300 dpi | Bleed |
|---|---|---|
| 12" LP jacket | 12.375 × 12.375 in → 3713 × 3713 px | 0.125 in each side |
| 7" single sleeve | 7.125 × 7.125 in → 2138 × 2138 px | 0.125 in |
| CD jewel-case front | 4.75 × 4.75 in → 1425 × 1425 px | 0.125 in |
| Cassette J-card | 4 × 2.625 in → 1200 × 788 px | 0.125 in |

Print needs CMYK conversion, and a design built from `duotone`/`riso` ops converts cleanly because it is already ink-limited — one of the practical advantages of working this way. Tell the user the printer will want the file with bleed and crop marks, which is a different export, and that heavy `grain` at 300 dpi can look coarser in print than on screen.

## 8. Handoff format

Present the files, then say in a few lines:

1. **The recommendation** — which alternative, and the one reason.
2. **What the others do differently**, one clause each.
3. **What to change** for a different direction, phrased as a knob: "warmer paper", "coarser screen", "type bigger and the plate cropped tighter".
4. **The name and metadata** are in `metadata.md`, with the search check.

No essay after the link. The user can see the covers.
