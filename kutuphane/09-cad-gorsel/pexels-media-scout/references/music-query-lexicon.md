# Query lexicon for music-studio briefs

Pexels search is a keyword match over contributor-supplied titles and tags. It is not
semantic. This is the single biggest reason searches fail: a brief that describes a
*feeling* returns nothing, while a brief that describes an *object in a lighting
condition* returns hundreds of usable frames.

## The translation rule

Rewrite every brief into `[concrete object] + [material/texture] + [light or colour]`.
Drop mood words unless they are also visual words.

| Brief (as received) | Weak query | Query that works |
|---|---|---|
| "makam esintili, hüzünlü kapak" | sad turkish music | `oud instrument close up`, `brass tray bazaar light`, `ottoman tile pattern` |
| "lo-fi çalışma müziği" | lofi vibe | `desk lamp rain window night`, `cassette tape macro`, `bedroom desk warm light` |
| "gece kulübü techno" | techno energy | `dark smoke laser beam`, `concrete wall neon light`, `strobe light silhouette` |
| "sıcak analog stüdyo" | analog warmth | `mixing console faders macro`, `vacuum tube amplifier glow`, `reel to reel tape machine` |
| "çöl / world fusion" | world music | `sand dune wind long shadow`, `desert road heat haze` |
| "ambient / drone" | ambient soundscape | `fog forest morning slow`, `clouds time lapse grey`, `deep water surface light` |

## Turkish and locale handling

Search in **English**. `locale=tr-TR` biases toward Turkish contributor tags, which are
sparse — it usually shrinks a good result set rather than localising it. The exception is
place-specific work: `locale=tr-TR` with `istanbul bosphorus` or `mosque interior` can
surface frames that the English index buries.

Culturally specific instruments are thinly covered. `oud` and `darbuka` return a handful
of frames; `ney`, `kanun`, `bağlama`, `zurna` return almost nothing usable. When the brief
needs one of these, stop searching for the instrument and search for the *world around*
it: textiles, brass, tile, coffee, low warm light, aged paper. Say this out loud rather
than quietly shipping a generic guitar photo.

## Query variant strategy

Always run 3–5 variants in one pass, not one query. Vary along one axis at a time:

1. **Literal subject** — `recording studio microphone`
2. **Detail / macro** — `condenser microphone mesh macro`
3. **Environment without subject** — `acoustic foam wall dark`
4. **Abstract texture as fallback** — `black paper texture grain`
5. **Adjacent object** — `headphones on desk low light`

Variants 3 and 4 matter most for commercial covers: no people means no model-release
problem, and texture frames leave room for typography.

## Terms that reliably improve a music-visual result set

`macro`, `close up`, `low light`, `dark background`, `moody`, `silhouette`, `bokeh`,
`neon`, `smoke`, `dust particles`, `grain`, `film`, `analog`, `vintage`, `overhead`,
`flat lay`, `minimal`, `negative space`, `gradient`, `long exposure`, `slow motion`
(video), `aerial`, `top down`.

## Terms to avoid

`music` alone (returns sheet-music and headphone clip-art), `singer`, `band`, `concert`
(crowds of identifiable faces, near-useless commercially), `dj` (heavily branded gear),
`success`, `creative`, `inspiration` (business-stock sludge).

## The overused-frame problem

Some Pexels frames appear on thousands of covers. If a candidate has a very high
`total_results` rank on a broad one-word query, assume it is over-circulated. Prefer
results from pages 2–3 of a *specific* query over page 1 of a generic one, and prefer
macro/texture over a composed "scene". A cover that looks like everyone else's cover has
failed even if the licence is clean.

## Negative space for typography

The API does not report where the empty area is. Use the proxies:

- `avg_color` luminance below 0.30 or above 0.78 → likely a frame where overlaid text
  survives. Midtones are the danger zone.
- Macro and texture shots almost always beat composed scenes for text overlay.
- For a square cover from a landscape original, check crop retention: below ~70% means
  the subject will be cut. Prefer a portrait or square original.
- Always open the full frame before committing. Score narrows the field to a handful;
  the eye makes the final call.

## Video-specific selection

- **Loopability**: a clip loops cleanly when the first and last frames are similar —
  drifting fog, water surface, dust, slow push on a static object. Anything with a person
  entering or leaving frame will not loop.
- **Motion budget**: for a 1-hour mix background, low motion is a feature and also keeps
  the render small. Search `slow motion`, `time lapse clouds`, `static shot`.
- **Frame rate**: mixed fps across a multi-clip edit causes judder. Prefer clips whose
  files share one fps, or conform everything in the edit.
- **Audio**: Pexels clips often carry an audio track that is *not* covered by the licence.
  Strip it: `ffmpeg -i in.mp4 -an -c:v copy out.mp4`.
