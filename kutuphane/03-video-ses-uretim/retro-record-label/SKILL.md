---
name: retro-record-label
description: A full retro record label in one skill — names the release, art-directs and RENDERS period-accurate album covers at 3000×3000 (procedural plates or the user's own photo, run through halftone/duotone/riso/VHS/xerox treatments), then writes the globally optimised English release metadata — YouTube title, description, tags, hashtags and chapters, plus DSP-legal track and album titles. Use whenever someone needs cover art, an album or song name, or release copy — "albüm kapağı yap", "retro kapak tasarla", "şarkı ismi bul", "albüm ismi öner", "youtube açıklaması yaz", "single çıkaracağım", "kapak alternatifleri üret", "plak kapağı", "70ler tarzı kapak", "spotify kapak boyutu", "bu şarkıyı nasıl adlandırayım", "keyword'leri optimize et". Trigger even when the request covers only one department (just the name, just the cover, just the description), and whenever a track from suno-composer needs packaging for release.
---

# Retro Record Label

A label has three departments and this skill is all three: **A&R** names the record, **art** designs and prints the sleeve, **marketing** writes the metadata that makes it findable in English-speaking markets. A request that touches one department usually needs a nod to the others — a cover with no title decision is a mockup, a name with no search check is a guess.

The output is never a description of a design. It is files on disk that have been rendered, looked at, and gated at thumbnail size.

## Division of labor

| Need | Where it belongs |
|---|---|
| The music itself, Suno prompts, lyrics | `suno-composer` |
| Instagram/LinkedIn posts, Reels scripts, captions | `post-forge` (pixels), `trend-setter` (copy) |
| App Store / Play listing | `aso-expert` |
| Naming, cover art, release metadata, YouTube copy | here |

When a track came out of `suno-composer`, take the key/tempo/genre/mood decisions from that session as the brief — they are better art direction input than anything a user types.

## Reference map

Read what the job needs. Do not preload everything.

| File | Read when |
|---|---|
| `references/era-playbook.md` | ALWAYS before designing. 13 era systems: palette hexes, type, layout logic, plate + preset pairing, and the clichés that mark a fake. |
| `references/naming.md` | Any naming work — album, EP, single, track list. Generation methods, the scoring rubric, collision checks, DSP title legality. |
| `references/youtube-metadata.md` | Any release copy: YouTube title/description/tags/hashtags/chapters, keyword research method, Shorts, DSP metadata sheet, localisation. |
| `references/imagery.md` | Deciding what the base image is: user photo, procedural plate, or public-domain source. Licence hygiene and network reality. |
| `references/darkroom.md` | Building or debugging a treatment chain. Full op reference + recipe cookbook. |
| `references/delivery.md` | Before export and handoff: platform specs, the rejection checklist, folder layout, mockups. |

`assets/cover.css` is the canvas stylesheet — copy it next to the HTML. `assets/starter.html` shows the plumbing (how `.cover`, `.plate`, `.pad` and the ink variables fit together) and is a reference for mechanics only, never a layout to reuse with the words swapped.

## Scripts

```bash
python scripts/fetch_fonts.py --era 1970s          # install real period faces first
python scripts/plates.py sungrid --palette neon84 -o work/plate.png
python scripts/darkroom.py work/plate.png --preset neon-1984 -o work/treated.png --size 3000
python scripts/darkroom.py photo.jpg --alternatives bluenote-1958,riso-1990,punk-xerox-1977 --out-dir work/
python scripts/render.py cover.html --out out/ --size 3000
python scripts/contact_sheet.py out/*.png -o review/sheet.png
```

`plates.py --list` and `darkroom.py --list-presets` print what is available. Everything is seeded: same seed, same result; change `--seed` to reroll noise without touching the recipe.

## Workflow

### 1 — Brief, inferred not interrogated

Settle these before anything else, pulling from the conversation, uploaded files, and the track itself: **genre and tempo**, **mood in three adjectives**, **artist name**, **release type** (single / EP / album), **era target**, **market** (Turkish-language release, English-language, or instrumental-and-therefore-global), and **whether a photograph exists**.

If two or three are genuinely unknown, ask once, in one message, with options — then proceed. Do not stall a design job on a questionnaire. An instrumental lo-fi track needs no lyrics discussion; a Turkish-language single needs an early decision about whether the title stays Turkish.

State the resolved brief in three lines before starting, so the user can correct one word instead of rejecting a finished cover.

### 2 — A&R: name it, then check the name

Read `references/naming.md`. Produce a shortlist, score it, and **verify the winners with web_search** — a title that collides with a charting song is a discoverability trap, and a title that violates DSP style rules gets the release rejected days before launch. Deliver the name with the collision evidence, not just the vibe.

### 3 — Art direction in writing, before pixels

Read `references/era-playbook.md` and commit, in writing:

- **Era** and why it fits the music (not just "retro").
- **Palette**: 3–4 hexes, with which colour carries 70% / 25% / 5%.
- **Type pair**: display + secondary, from faces `fetch_fonts.py` can actually install.
- **Layout archetype**: where the type sits and what the image does.
- **Signature device**: the one repeatable element — a rule, a catalogue number block, a corner notch, a duotone crop, a badge. This is what makes a second single look like the same artist.

Then the **variation plan**: the alternatives must differ in *concept* — a type-dominant sleeve, an image-dominant sleeve, a graphic-abstract sleeve — not in filter. Three treatments of one layout is one cover with three moods, and users can feel the difference.

### 4 — Base imagery

Read `references/imagery.md`. Three honest routes: the user's own photo (best), a procedural plate from `plates.py` (fast, no licence risk, and genuinely period-correct for graphic-abstract eras), or a public-domain image the user downloads themselves — **this container cannot reach image hosts, so never claim to have "found" a photo online**. Prepare the base to square and tonally open before treatment.

### 5 — Darkroom

Read `references/darkroom.md`. Use `--alternatives` to run several era presets over one base in a single pass, then tune the chain of the ones worth keeping. Presets are starting points; a brief-specific chain almost always beats a preset.

### 6 — Type on top, in HTML

Install fonts first (`fetch_fonts.py`), copy `cover.css`, design at 1000×1000 CSS px, one `.cover` element per alternative in one file. `render.py` rasterises type at final resolution rather than upscaling it, and reports overflow plus the fonts that actually resolved — a silent fallback to DejaVu is the most common invisible failure.

### 7 — The gates. Nothing ships unseen.

Run `contact_sheet.py` and **look at both sheets**:

- **Thumbnail gate**: at 110px, can you read the artist and the title? A playlist row is 64–160px. If it turns to mud, cut words or grow the type — do not shrink the type to fit.
- **Compliance gate**: run the checklist in `references/delivery.md`. URLs, social handles, "Out Now!", explicit badges, and platform logos on the artwork are the most common rejection causes, and a rejection moves a release date by days.
- **Glyph gate**: if any Turkish text appears, confirm `ı ğ ş İ Ğ Ş` rendered rather than falling back mid-word. `fetch_fonts.py --check` reports coverage per face.
- **Contrast gate**: type over a busy plate needs a band, a scrim, or a crop — not a drop shadow on every line.

### 8 — Marketing: the global metadata pack

Read `references/youtube-metadata.md`. Deliver, in English for the international market: YouTube title, the full description (above-fold hook, credits, chapters, links, keyword paragraph, hashtags), tags, and the DSP metadata sheet. Search for the actual keyword landscape before writing — genre and use-case language shifts fast, and 2026 phrasing is not 2022 phrasing.

### 9 — Handoff

Deliver the file set from `references/delivery.md`, present the files, and say in two lines what to change if they want a different direction. No essay after the link.

## What makes this fail

- **The filter parade.** Same layout, three treatments, presented as three concepts.
- **Canva retro.** A sunburst plus a chunky sans plus a grain overlay. Period accuracy lives in the *constraints* — two ink colours because the label was cheap, type crushed into a corner because the photo was cropped badly on purpose, a catalogue number nobody needed. Read the era file.
- **Thumbnail mud.** Beautiful at 3000px, unreadable at 100px, which is where it lives.
- **Keyword stuffing in English.** A description written for a crawler reads as spam to the listener who actually clicked. Every line earns its place.
- **An unsearchable name.** A one-word common noun the artist loves and nobody can find.
- **Invented facts.** Never fabricate stream counts, chart positions, press quotes, or a label that does not exist — unless the user asks for a fictional label as part of the concept, in which case label it as fiction.

## Rights and honesty

Do not pastiche a specific famous sleeve closely enough to be recognisable, reproduce band logos or trademarks, or build a cover around a photo of an identifiable living person the user has no rights to. Do not depict real musicians. When imagery comes from a public-domain source, record the source and licence in the handoff so the user can defend it. When a treatment leans on a label's visual identity, say "in the tradition of" rather than passing it off as that label's work.
