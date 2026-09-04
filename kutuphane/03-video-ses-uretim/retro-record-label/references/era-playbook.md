# Era Playbook

Thirteen sleeve systems. Each one is a set of *constraints*, because that is what dates a design — not a filter. A 1958 Blue Note sleeve looks like that because two-colour offset was cheap, the photographer shot the session on tungsten film, and the designer had one photo and had to make a headline out of it. Reproduce the constraint and the era arrives on its own.

## Contents

1. How to use an era entry
2. 1955–1962 · Hard bop / modernist jazz
3. 1958–1965 · Exotica, lounge, easy listening
4. 1965–1969 · Psychedelia
5. 1968–1975 · Prog and concept surrealism
6. 1970–1978 · Soul, funk, disco
7. 1968–1976 · Library / production music
8. 1976–1980 · Punk and xerox
9. 1979–1984 · Post-punk and the design sleeve
10. 1982–1989 · Synth, neon, airbrush
11. 1985–1992 · VHS, late-night, cheap video
12. 1988–1996 · Riso, zine, indie two-colour
13. 1991–1997 · Grunge and found-object
14. 1993–1999 · Early digital / proto-vaporwave
15. Choosing between eras
16. Era tells that read as fake

---

## 1. How to use an era entry

Each entry gives: the **constraint** that produced the look, **palette** hexes, **type** (faces `fetch_fonts.py` installs), **layout logic**, the **plate + preset** pairing to start from, and **tells** — the clichés that mark a pastiche made by someone who only saw thumbnails.

Take the palette as a starting temperature, not a law. Shift one hue toward the music's mood and the cover stops looking like a template.

---

## 2. 1955–1962 · Hard bop / modernist jazz

**Constraint.** Two or three ink colours, one session photograph, a printer with visible screen dots. The designer's whole job was to make typography carry the drama the budget could not.

**Palette.** Deep navy `#0b1a2e`, warm cream `#e9dcbf`, brick `#c9552f`, grey-green `#7c8b91`. One dominant ink, cream as the field, accent used once.

**Type.** Grotesque only — Libre Franklin, Archivo Black, Oswald condensed. Set the title huge and tight, break lines where the meaning breaks, and let a word run off the edge if the crop is better for it. Never centre everything.

**Layout logic.** The photograph is cropped brutally — a hand, half a face, a horn — and the type is crushed into the space left over. Title in one corner, artist smaller and often in the accent colour, personnel list in tiny type at the bottom like a legal notice. Asymmetry throughout. Massive negative space is period-correct and reads as confidence.

**Plate + preset.** `plates.py geo --palette bluenote` (for graphic sleeves) or a real portrait; `darkroom.py --preset bluenote-1958`. The halftone at `lpi:30–36` is the signature — the dots must be visible at full size.

**Tells.** A trumpet silhouette clip-art. Perfectly centred type. Four colours. Drop shadows. A "jazz" script font — there were none.

---

## 3. 1958–1965 · Exotica, lounge, easy listening

**Constraint.** Stereo was new and the sleeve had to sell the *technology* as much as the music. Hence badges, boasts, and unreal colour.

**Palette.** Cream `#f0e3c8`, burnt orange `#d9772b`, teal `#2f6f6b`, ink `#231f20`. Saturated, flat, slightly wrong — like colour separation done by eye.

**Type.** A modern serif or a fat wood-type display (Bodoni Moda, Abril Fatface, Alfa Slab One) over widely-tracked caps for the subtitle.

**Layout logic.** Centred and symmetrical, unlike jazz. A decorative frame or rule. A **badge** is mandatory: "STEREO", "HIGH FIDELITY", "FULL DIMENSIONAL SOUND". Illustration over photography.

**Plate + preset.** `plates.py sunburst` or `rings` with `--palette lounge62`; `--preset verve-1962`.

**Tells.** Tiki clip art. Modern gradients. Anything with a soft shadow.

---

## 4. 1965–1969 · Psychedelia

**Constraint.** Art Nouveau revival plus poster printing, plus the deliberate refusal to be legible. Type was drawn, not set.

**Palette.** Violet `#2b0a4a`, hot red `#e0344f`, acid yellow `#f7d84a`, viridian `#1f7a5c`. Vibrating complementaries — the point is that adjacent colours fight.

**Type.** Rye, Sancreek, Bungee, Monoton. Letters must warp to fill their container, not sit on a baseline. If the display face cannot warp, set it in HTML and distort the *plate* underneath instead.

**Layout logic.** No hierarchy. The type is the image. Mirror symmetry, concentric fills, every gap filled. Illegibility up to about 70% is authentic — the artist name should still resolve at thumbnail, or the cover fails commercially.

**Plate + preset.** `plates.py blobs` or `rings --palette psych68`; `--preset psych-1968` (posterize + warp + tritone is the core).

**Tells.** A peace sign. Rainbow gradients. Legible, evenly-spaced type. Modern neon glow.

---

## 5. 1968–1975 · Prog and concept surrealism

**Constraint.** Real photography, real objects, in-camera tricks, no compositing tools — so the strangeness had to be *staged*, and printing was good enough to show grain and subtle colour.

**Palette.** Muted and desaturated: forest `#1a2b1f`, bone `#d8cbb0`, tobacco `#8a5a2b`, sage `#4a6b52`. Sun-faded, never punchy.

**Type.** Small, quiet, sometimes absent from the front entirely. Josefin Sans, Poiret One, a light grotesque. Restraint is the statement.

**Layout logic.** One uncanny image, full bleed, no frame. An object where it should not be — a horizon indoors, a scale error, a figure facing away. The title lives on the spine or the back, not fighting the picture.

**Plate + preset.** A real photograph is strongly preferred here; failing that `plates.py clouds --palette prog73` or `mountains`; `--preset hipgnosis-1973` (fade + bloom + grain + vignette).

**Tells.** Type over the middle of the image. High saturation. Obvious digital compositing. Lens flare.

---

## 6. 1970–1978 · Soul, funk, disco

**Constraint.** Warm film stock, airbrush illustration, and typography that had to feel like the groove — heavy, rounded, confident.

**Palette.** Chocolate `#3a1408`, terracotta `#c8622a`, cream-gold `#f2d9a0`, deep red `#7a1f1f`. Add a metallic-adjacent gold for disco.

**Type.** Fat and round — Alfa Slab One, Bevan, Righteous, Abril Fatface. Custom-feeling ligatures, tight tracking, offset outlines or hard drop shadows in a second ink (a real 70s device, unlike soft shadows).

**Layout logic.** Big centred title, artist below in tracked caps, sunburst or airbrushed sky behind. A solid colour band behind the credits — that band is how the era got contrast over busy art, and it still works.

**Plate + preset.** `plates.py sunburst` or `mesh --palette soul75`; `--preset soul-1975`.

**Tells.** Cool colours. Thin type. Gradients with modern smoothness instead of airbrush banding.

---

## 7. 1968–1976 · Library / production music

**Constraint.** These sleeves were never sold in shops — they were catalogues sent to TV editors. So they are pure information design, and that is exactly why they look so good now.

**Palette.** Two inks on stock: paper `#e8e3d3`, black `#1f1f1f`, one signal colour (`#d94f2b` or `#3b6ea5`).

**Type.** A single grotesque at two sizes. Libre Franklin, Archivo Narrow, Oswald. All caps, tight, no exceptions.

**Layout logic.** A visible grid. A colour field or geometric diagram occupying an exact fraction of the square. Track titles listed on the front with durations and mood keywords ("DRAMATIC · TENSION · 2:14"). A catalogue number set as large as the title. It should look like a filing system.

**Plate + preset.** `plates.py stripes`, `dots`, or `geo --palette library70`; `--preset print-cmyk` at low `lpi`, or no photographic treatment at all — just paper texture and grain.

**Tells.** Any photograph of a musician. Decoration. Centred type.

---

## 8. 1976–1980 · Punk and xerox

**Constraint.** A photocopier, scissors, a typewriter, and no money. Every visual property follows from generation loss.

**Palette.** Paper `#f1eee6`, black `#141414`, one screaming red `#e5202e`. Never more.

**Type.** Special Elite (typewriter), Anton, Archivo Black — or ransom-note mixing where each word is a different face and size, set at slight rotations.

**Layout logic.** Collage. Hard-edged rectangles of pasted-in image with visible cut lines. Tape marks, hand-drawn arrows, over-inked blacks blown out to solid. Deliberate misalignment: rotate elements 1–3°, never 0.

**Plate + preset.** Any base; `--preset punk-xerox-1977` (adaptive threshold + coarse halftone + heavy dust). Push `xerox` to 0.85 and `dust` to 0.6 for third-generation copies.

**Tells.** Clean edges. Smooth greys — xerox has no midtones. Distressed-texture overlays from a stock pack; the damage must come from the process.

---

## 9. 1979–1984 · Post-punk and the design sleeve

**Constraint.** Art-school rigour and expensive print on a small budget: the money went into one idea executed exactly.

**Palette.** Near-black `#0e0e10`, cold grey `#d8d8d2`, slate blue `#8c9aa6`. Monochrome with one desaturated accent, or no accent at all.

**Type.** Small. Oswald, Libre Franklin, Space Mono. Extreme tracking, lowercase where the era would have gone uppercase. Sometimes the artist name is absent from the front and that is the boldest choice available.

**Layout logic.** A boxed image with generous white margins — the frame is the design. A line-screen or half-tone photographic plate, abstract and unreadable as a subject. Hairline rules. Precise, ungenerous, cold.

**Plate + preset.** `plates.py mountains` or `clouds --palette postpunk81`; `--preset postpunk-1981` (line-screen halftone at `lpi:18–22`).

**Tells.** Warmth. Big type. A recognisable subject.

---

## 10. 1982–1989 · Synth, neon, airbrush

**Constraint.** Airbrush and early photo-typesetting, chrome, and grids that stood for "computer" before anyone had one.

**Palette.** Near-black violet `#0a0518`, magenta `#ff2d95`, cyan `#00e5ff`, yellow `#ffd400`. Dark ground, two glowing accents, and a hard horizon.

**Type.** Orbitron, Audiowide, Michroma, Bebas Neue. Wide tracking, chrome or gradient fills, hard outline strokes rather than soft glows.

**Layout logic.** Horizon at 55–65%. Sun, grid, or mountain silhouette. Title on the horizon line or straddling it. Everything symmetrical around the vertical axis.

**Plate + preset.** `plates.py sungrid --palette neon84` (this is what it exists for); `--preset neon-1984`.

**Tells.** Modern glassmorphism. Blur used as glow. Lowercase type. Palm trees so generic they read as a stock template — if a palm appears, it should be a silhouette on the horizon, not the subject.

---

## 11. 1985–1992 · VHS, late-night, cheap video

**Constraint.** Composite video, tape dropouts, chroma bandwidth a quarter of luma — so colours smear sideways and never align with edges.

**Palette.** Ink blue `#101426`, hot pink `#f24b6a`, mint `#35d0c8`, ivory `#f5e9c8`.

**Type.** Bebas Neue, VT323, Chakra Petch. Broadcast-style: a timecode strip, "PLAY ▶", a channel bug in a corner, tracking text at the bottom.

**Layout logic.** The whole square behaves like a frame grab: bars, scanlines, a subtitle strip. Type sits in the safe area with obvious margins, as if a titler generated it.

**Plate + preset.** Any base; `--preset vhs-1987`. Push `vhs` to 0.9 and add `misreg=offset:8` for a worse-generation tape.

**Tells.** Sharp type over a degraded plate — the *type* must degrade too. A modern glitch-art effect with random RGB blocks; tape damage is horizontal, never blocky.

---

## 12. 1988–1996 · Riso, zine, indie two-colour

**Constraint.** Two spot inks on a duplicator that never registers perfectly, on absorbent paper.

**Palette.** Newsprint `#f6efdd`, riso red `#ff4a3d`, riso blue `#1b3fa0`, yellow `#ffd23f`. Exactly two or three inks, and where they overlap they must genuinely multiply into a third colour.

**Type.** Archivo Narrow, Space Mono, Courier Prime. Small, functional, slightly crooked.

**Layout logic.** Flat illustration or a heavily-screened photo, hand-drawn elements, generous paper showing. One ink deliberately offset 4–8px so you can see the misregistration — that offset *is* the aesthetic.

**Plate + preset.** `plates.py geo` or `blobs --palette riso90`; `--preset riso-1990`. Tune `offset` up for a worse machine.

**Tells.** Perfect registration. More than three inks. A "riso texture" overlay on top of a full-colour photo — the colour reduction has to happen first.

---

## 13. 1991–1997 · Grunge and found-object

**Constraint.** A cheap camera, a flatbed scanner, and an aesthetic that treats damage as honesty.

**Palette.** Bitumen `#1b1a17`, dirty bone `#cfc7b3`, army green `#6b7b4a`, oxide `#a8412a`. Desaturated and muddy on purpose.

**Type.** Special Elite, Courier Prime, a condensed sans set slightly too small. Hand-written annotation. Type that looks photocopied and re-scanned.

**Layout logic.** A found object photographed flat — a medical diagram, a doll, a tag, a page. Off-centre, badly cropped, plenty of dead space. Ring wear and scuffs as if the sleeve has been in a crate for years.

**Plate + preset.** Any base; `--preset grunge-1993` (xerox + heavy dust + paper + ringwear).

**Tells.** Symmetry. Clean type. Saturated colour. A grunge-brush font, which is a 2004 idea, not a 1993 one.

---

## 14. 1993–1999 · Early digital / proto-vaporwave

**Constraint.** 8-bit palettes, early 3D, JPEG artefacts, and clip art from a CD-ROM.

**Palette.** Deep violet `#2a1240`, pale pink `#f7c8dc`, aqua `#2de1c2`, pale yellow `#fdf6a0`.

**Type.** Monoton, VT323, Press Start 2P, Space Mono. System-font energy. A caption box. Japanese-katakana-style secondary text is period-authentic but overused — if used, it must actually say something relevant.

**Layout logic.** Perspective checkerboard floor, a floating object, a bust or column, and a horizon. Deliberate visual non-sequitur.

**Plate + preset.** `plates.py checker --palette vapor95`; `--preset vaporwave-1995`.

**Tells.** The exact same bust-plus-grid composition every other vaporwave cover uses. If the brief lands here, find a different object.

---

## 15. Choosing between eras

Match the *production* of the music, not its genre label:

- Acoustic, live-tracked, small ensemble → 1955–1962 or 1968–1976 library.
- Dense, layered, studio-as-instrument → 1968–1975 prog.
- Groove-led with real bass → 1970–1978 soul.
- Drum machine and synth bass → 1982–1989 neon, or 1985–1992 VHS if it is lo-fi.
- Fuzzy, DIY, recorded in a room → 1976–1980 punk, 1988–1996 riso, or 1991–1997 grunge.
- Sample-based, nostalgic, slowed → 1993–1999 digital.

When two eras fit, use them as the axis of variation: give the user one cover from each and let the choice make itself.

---

## 16. Era tells that read as fake

These break the illusion faster than anything else, regardless of era:

- **Soft drop shadows and blurs.** Offset print has no soft shadows. Hard offsets in a second ink are correct; Gaussian glow is not.
- **Even, modern letter-spacing.** Pre-digital type had optical spacing — tighten display type more than feels comfortable.
- **Too many colours.** Almost every era above was limited by ink cost. Four is generous. Two is often better.
- **Grain and texture applied last over a clean modern design.** The degradation has to affect the *whole* image including type, or it looks like a filter, which it is.
- **Sharp 4K clarity underneath the texture.** Real sleeves lose detail. `fade` and slight `blur` before `grain` help.
- **A perfectly square, perfectly centred layout in an era that never did that.** Check the layout logic above before centring anything.
