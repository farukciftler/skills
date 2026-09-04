# Imagery — Where the Base Picture Comes From

Every treatment in `darkroom.md` needs something underneath it. There are exactly three honest routes, and being straight about which one is in play protects the user from a takedown and from being told a photo was "found" when it was not.

## Contents
1. The network reality
2. Route A — the user's own photograph
3. Route B — a procedural plate
4. Route C — public domain and open licence, fetched by the user
5. What makes a good base image per era
6. Preparing a base image before treatment
7. Licence hygiene in the handoff
8. Never do these

---

## 1. The network reality

In this environment, `bash` can reach a short allow-list (GitHub, PyPI, npm) and **cannot reach image hosts** — Wikimedia, Unsplash, Openverse, museum APIs all return 403 through the proxy. Font files work because the Google Fonts repository lives on GitHub.

So:

- **Never say a photo was downloaded or found.** If a URL was not fetched, it was not fetched.
- `image_search`, when available, is a **moodboard tool**: it shows reference so art direction can be discussed. Those images cannot be saved to disk or treated.
- If the skill runs somewhere with open network access (a user's own machine, a server session), Route C becomes a real download step. Test with one `curl` before assuming.

State the route being used in one line, early. "No photo was supplied, so these covers are built from procedural plates" is information the user needs, not an apology.

## 2. Route A — the user's own photograph

Best outcome, always. A real photograph carries texture, accident and specificity that no generator invents, and the rights question disappears.

Ask for it once, concretely, and make it easy to say yes: **"A phone photo works — a wall, a window, a hand, a street at night, an object on a table. It does not need to be good; the darkroom does the work."** That framing gets a usable image far more often than "do you have artwork?".

What actually works from a phone:

- **Texture over subject.** Concrete, rust, a curtain, water, paint, fabric.
- **A single object on a plain surface**, lit from one side.
- **Night street** with one light source, motion blur welcome.
- **A hand, a shoulder, a silhouette** — a person without an identifiable face solves both composition and rights.
- **Something shot through glass**, a screen, a fence.

What does not: group photos, selfies, wide landscapes with a busy horizon, anything already filtered.

Files arrive at `/mnt/user-data/uploads`. Read them from there, never write there.

## 3. Route B — a procedural plate

`plates.py` builds the under-layer from geometry and noise. This is not a fallback for the graphic eras — it is the *correct* method for them. A 1968 library sleeve or a 1958 Blue Note graphic cover was made from flat shapes and screens, and that is exactly what these generators produce.

| Generator | What it gives | Strongest for |
|---|---|---|
| `geo` | 3–5 confident flat shapes | jazz modernist, library, riso |
| `stripes` / `dots` | rhythmic fields, size gradients | library, pop art, post-punk |
| `rings` | concentric target | lounge, psych, mod |
| `sunburst` | radiating rays | soul, disco, lounge |
| `sungrid` | horizon, slatted sun, perspective grid | synth 80s |
| `checker` | perspective floor | vaporwave, 80s stage |
| `mountains` | layered ridge silhouettes | prog, post-punk, ambient |
| `clouds` | fractal sky / marble (`marble:1`) | prog, ambient, sleeve texture |
| `mesh` | soft multi-point gradient | soul airbrush, 70s ground |
| `blobs` | liquid organic masses | psychedelia |
| `starfield` | stars plus one body | space rock, cosmic jazz |

Palettes are named per era (`--palette` — see `plates.py --list`), or pass explicit hexes as `#dark/#light/#accent/#second`. `--set` passes generator params: `--set "rays:32;cy:0.4"`, `--set "horizon:0.58;sun:0.26"`, `--set "marble:1;veins:4"`.

Two things make procedural plates stop looking generated:

1. **Treat them.** A raw plate is flat vector; a plate through `darkroom` has ink, dot, grain and misregistration. Never ship an untreated plate.
2. **Crop into them.** Generate at 3000 and use a 60% crop, or build the plate then let the type cover two thirds of it. Full-frame symmetrical plates are what "AI cover" looks like.

Combining plates is legitimate: render two, and composite them in the HTML with `mix-blend-mode: multiply` on a second `.plate` layer.

## 4. Route C — public domain and open licence, fetched by the user

When the brief genuinely needs photography and the user has none, hand them a **sourcing brief**: exact search terms, the two or three collections most likely to have it, and the licence note. Then they drop one file in and the pipeline runs.

Collections worth naming, in rough order of usefulness for sleeve art:

| Source | What it holds | Licence note |
|---|---|---|
| **Library of Congress** (loc.gov) | US documentary photography, FSA archive, portraits | much is public domain; per-item rights statement |
| **Wikimedia Commons** | everything, variable quality | per-file licence; many need attribution (CC BY-SA) |
| **The Met** / **Rijksmuseum** open access | paintings, prints, objects at very high resolution | CC0 for flagged items |
| **NASA image library** | space, earth, technical | generally free to use, no endorsement implied |
| **Public Domain Review** | curated pre-1930 oddities | links to sources with rights stated |
| **Flickr Commons** | institutional archives | per-image licence, check each |
| **Unsplash / Pexels** | modern photography | permissive licence, but *not* public domain — read the current terms, and note these images appear on thousands of other projects |
| **Internet Archive** | scans, ephemera | rights vary wildly, verify per item |

The sourcing brief should read like this:

```
Looking for: a single object on a plain background, tungsten light, 1960s.
Try: Library of Congress → "still life 1965", "shop window night"
     Rijksmuseum open access → "vanitas", "glass vessel"
Need: ≥2000px on the short edge, no visible faces, no logos.
Save it anywhere and send it back — I'll square it and treat it.
```

Public-domain paintings and prints are underused and excellent bases: a detail from a 17th-century still life, screened to two inks and misregistered, is indistinguishable from a real 1970s art-house sleeve.

## 5. What makes a good base image per era

| Era | Base that works | Base that fights the treatment |
|---|---|---|
| Jazz modernist | one figure or object, hard side light, lots of dark | busy midtones, evenly lit |
| Lounge / exotica | saturated illustration, flat colour | documentary photography |
| Psychedelia | high-contrast graphic shapes | fine detail, which the warp destroys |
| Prog surrealism | a real place with one wrong element | anything already strange, which becomes noise |
| Soul / funk | warm skin tones, a sky, an airbrush ground | cold blue, high-key white |
| Library | pure geometry, no photograph | any photograph |
| Punk xerox | strong silhouettes, near-black and near-white | subtle gradients — xerox has no midtones |
| Post-punk | abstract texture, unreadable subject | a face |
| Synth 80s | horizon, chrome, one glow source | daylight, clutter |
| VHS | anything with a light source | flat lighting, since the bleed needs edges |
| Riso | flat areas that survive 2–3 colour reduction | photographs with wide tonal range |
| Grunge | found object, flat-scanned | wide landscape |

## 6. Preparing a base image before treatment

`darkroom.py` does the mechanics — `prepare()` centre-crops to square and resizes to `--size` — but decide these first:

- **The crop is a design decision.** `--anchor top|center|bottom` picks the band. For a portrait, anchoring `top` and letting the chin leave the frame is a period-correct, deliberately awkward crop.
- **Open the tonal range.** Every preset starts `square,auto` for a reason: the ink-mapping ops read luminance, and a flat source turns to mud. If a source is very dark or very flat, add `levels=lo:15;hi:240` before the ink ops.
- **Kill colour you are about to replace.** Going to duotone or riso? The source's hue is irrelevant — judge the base on *tonal structure* only. Squint at it in greyscale.
- **Downscale, never upscale.** A 900px phone photo can make a fine 3000px cover after heavy screening — halftone and grain hide softness. But `auto` plus `sharpen` on an upscaled file just amplifies mush; if the source is small, lean into a coarse screen (`lpi:18–26`) which turns low resolution into a deliberate look.
- **Work at final size for the final pass.** `lpi` is resolution-relative so recipes transfer, but anti-aliasing quality is not. Preview at 900–1500 while iterating, then run the keeper at 3000.

## 7. Licence hygiene in the handoff

Include a short block with the deliverables whenever a base image was not generated:

```
Cover base: user-supplied photograph (IMG_4821.jpg), rights held by the artist.
```
```
Cover base: "Still Life with Glass", Rijksmuseum, CC0 public domain.
Treatment and typography original. Safe for commercial release; no attribution required.
```

Fonts too, briefly: all faces `fetch_fonts.py` installs are OFL/Apache/UFL and safe on commercial artwork, but the licence file ships next to each font if the artwork is going to be trademarked.

## 8. Never do these

- Claim an image was fetched when it was not.
- Build a cover around a recognisable photograph of a living person without rights — including the artist's own photo of someone else.
- Reproduce a famous sleeve closely enough to be identified as that sleeve, or place a real band's logo or a label's trademark on artwork.
- Depict real, identifiable musicians.
- Use an AI-image-generator watermark, a stock-photo watermark, or a visibly cropped watermark. If it has a watermark, it is not licensed.
- Pass a CC BY image off as public domain. If attribution is required, it goes in the release credits, and the user has to be told.
