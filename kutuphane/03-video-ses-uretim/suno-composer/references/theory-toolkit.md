# Theory Toolkit

Compositional decisions, and how each one translates into language Suno responds to. Every section ends with the translation, because a decision you can't encode is a decision you didn't make.

## Contents
1. Keys and modes
2. Chord progression archetypes
3. Cadences, harmonic rhythm, and section contrast
4. Colour moves: modal interchange, secondary dominants, pedal points
5. Meter, groove, and tempo
6. Form and bar-count planning
7. Melody and hook construction
8. Vocal ranges, tessitura, and where to put the chorus
9. Arrangement by register
10. Dynamics and the emotional arc
11. Lyric prosody (including Turkish)
12. Non-Western and makam material

---

## 1. Keys and modes

Absolute key matters less than most guides claim — Suno treats it as a bias, not a lock — but **mode** matters enormously, because it changes which scale degrees the melody leans on and that is audible immediately.

The seven diatonic modes, by the one interval that defines each:

| Mode | Defining degree | Emotional colour | Idiom |
|---|---|---|---|
| Ionian (major) | natural 4 & 7 | bright, resolved, uncomplicated | pop, gospel, country |
| Dorian | minor with **natural 6** | melancholy but not defeated; hopeful sadness | funk, Celtic folk, jazz minor, drum & bass |
| Phrygian | **b2** | tense, Spanish/Middle Eastern, ominous | flamenco, metal, Anatolian |
| Lydian | **#4** | wonder, floating, unresolved brightness | film score, dream pop, prog |
| Mixolydian | major with **b7** | rootsy, defiant, bluesy without being sad | rock, blues-rock, Britpop, sea shanty |
| Aeolian (natural minor) | b3 b6 b7 | plain sadness, gravity | ballads, minor-key pop, epic trailer |
| Locrian | b5 | unstable, unusable as a tonic in practice | avoid unless the point is dread |

Beyond diatonic:

- **Harmonic minor** — raised 7 gives a V (major dominant) in a minor key. The augmented second between b6 and 7 is the "exotic" sound in Western ears.
- **Phrygian dominant** (5th mode of harmonic minor: 1 b2 3 4 5 b6 b7) — the single most useful non-diatonic scale for Middle Eastern, Anatolian, flamenco and metal colour. This is Hicaz in makam terms, near enough for a 12-TET model.
- **Melodic minor / jazz minor** — for neo-soul and jazz lines over minor-major 7 chords.
- **Blues scale** (1 b3 4 b5 5 b7) and **major pentatonic** (1 2 3 5 6) — pentatonics have no half-steps, which is why they never sound wrong and also why they can sound bland without rhythmic interest.

**Key choice by practical constraint**, which is the part theory guides skip: guitar-led songs sit well in E, A, D, G (open strings ring). Brass-led jazz sits in Bb, Eb, F (the horns are built there). Piano ballads work anywhere but F, C, G, D and their relative minors sound the most "natural" because of black-key voicing ergonomics. Sub-bass-driven electronic music sits low — F minor, G minor — so the root lands in the 40–60 Hz shelf.

**Translation:** name the key and mode plainly ("A Dorian", "F# Phrygian dominant") *and* add a scale-flavour descriptor Suno definitely understands ("modal, Dorian brightness in a minor key", "Middle Eastern harmonic minor colour"). The descriptor does the real work.

---

## 2. Chord progression archetypes

Suno does not parse chord symbols. Choose the progression for yourself, then describe its **character**.

### Major-key
| Roman numerals | Name | Character | Say this to Suno |
|---|---|---|---|
| I–V–vi–IV | axis / four chords | universal pop lift | "anthemic pop cycle, resolves upward" |
| vi–IV–I–V | sad axis | melancholy that still lifts at the end | "melancholy cycle that opens into hope" |
| I–vi–IV–V | doo-wop / 50s | nostalgic, innocent | "50s doo-wop changes" |
| I–IV–V | blues / rock primary | plain, driving | "three-chord rock changes" |
| I–bVII–IV | Mixolydian rock | defiant, rootsy | "Mixolydian rock changes, flat-seven" |
| I–V–vi–iii–IV–I–IV–V | Pachelbel | descending inevitability | "descending sequence, canon-like" |
| Imaj7–iii7–vi7–ii7 | neo-soul cycle | warm, sophisticated, unhurried | "extended seventh chords, neo-soul harmony" |

### Minor-key
| Roman numerals | Name | Character | Say this to Suno |
|---|---|---|---|
| i–VI–III–VII | epic minor | grand, cinematic, forward-leaning | "epic minor cycle, cinematic lift" |
| i–VII–VI–VII | minor vamp | brooding, static, hypnotic | "brooding minor vamp, no resolution" |
| i–VII–VI–V | Andalusian cadence | Spanish/Middle Eastern descent, tragic | "Andalusian descending cadence, Phrygian" |
| i–iv–i–V | harmonic-minor folk | old, formal, weighty | "harmonic minor, formal cadence" |
| i–iv–VII–III | minor circle | flowing, sorrowful, jazz-adjacent | "circle-of-fifths minor movement" |
| i–bIII–bVII–iv | modern minor pop | dark, contemporary | "dark minor pop changes" |

### Jazz and blues
- **ii–V–I** is the atom of jazz. Chains of them (ii–V of the ii, etc.) create the sense of constant motion.
- **12-bar blues**: I I I I / IV IV I I / V IV I V. The last two bars are the turnaround.
- **Rhythm changes** (I–vi–ii–V, AABA, 32 bars) underpins a huge amount of bebop.
- Translation: "walking bass and 2-5-1 turnarounds", "twelve-bar blues form", "bebop changes".

### Choosing one
Match the progression to the **emotional arc**, not the genre. A song that must end unresolved should not use a progression that lands on I. If the chorus is meant to feel like release, the verse should withhold the tonic — start the verse on vi or IV and only reach I at the chorus downbeat. That single choice does more emotional work than any adjective in the prompt.

---

## 3. Cadences, harmonic rhythm, and section contrast

**Cadences** are how a section says what it means:
- **Authentic (V–I)** — closed, final. Chorus ends.
- **Half (…–V)** — open, question. Pre-chorus ends here to force the chorus.
- **Plagal (IV–I)** — soft landing, "amen". Outros, gospel.
- **Deceptive (V–vi)** — the promised resolution withheld. Use once, at the end of the second chorus, to buy a bridge.
- **Picardy third** — minor song ending on a major tonic. Ambiguous consolation. Overused; earn it.

**Harmonic rhythm** — the rate of chord change — is the most underused contrast tool. Verse: one chord per two bars. Pre-chorus: one per bar. Chorus: back to two bars but with the melody moving faster. That acceleration-then-release is *felt* even by listeners who couldn't name a chord.

**Where contrast actually comes from**, ranked by audibility:
1. Register (the vocal moves up; the bass drops an octave)
2. Arrangement density (a layer enters or leaves)
3. Harmonic rhythm
4. Rhythmic feel (straight → half-time, or the hats double)
5. Actual new chords — least important, and the thing people reach for first

**Translation:** "verse holds one chord for two bars then the pre-chorus doubles the harmonic rhythm", "pre-chorus ends unresolved on the dominant". Suno responds to these because they're arrangement descriptions, not notation.

---

## 4. Colour moves

- **Modal interchange (borrowed chords)** — pull a chord from the parallel mode. In a major key, the borrowed **iv** (minor four) is the single most reliable heartbreak device in pop; bVI and bVII give the "epic" flavour. Say: "borrowed minor four for the ache".
- **Secondary dominants** — V/V, V/vi. A momentary pull toward a chord that isn't the tonic. Say: "secondary dominant pushing into the chorus".
- **Pedal point** — hold one bass note while chords change above. Creates tension without motion. Standard under a build. Say: "sustained bass pedal under shifting chords".
- **Tritone substitution** — bII7 for V7. Jazz. Say: "chromatic tritone-sub turnaround".
- **Modulation** — up a semitone or whole tone for the final chorus is the classic (and now slightly kitsch) lift. Up a minor third is more modern. A *down* modulation for a final verse is rare and devastating. Say: "key change up a whole tone for the last chorus" — Suno honours this inconsistently, so also add "final chorus lifts" as arrangement backup.
- **Suspensions (sus2, sus4)** — delay resolution, create shimmer. Ubiquitous in indie and worship. Say: "suspended chord voicings, unresolved shimmer".

---

## 5. Meter, groove, and tempo

### Meter
- **4/4** — everything, default.
- **3/4** — waltz. Lilting, old-fashioned, or eerie depending on tempo.
- **6/8** — compound. Two big beats each subdivided in three. The ballad meter (doo-wop ballads, Irish folk, power ballads). Feels like rolling rather than stepping.
- **12/8** — slow blues shuffle.
- **5/4, 7/8** — prog, math rock, and Balkan/Anatolian folk. Suno handles these unreliably; reinforce with a groove descriptor ("limping seven-beat groove") rather than trusting the number alone.
- **Aksak (9/8 as 2+2+2+3)** — Turkish karşılama. Also 7/8 (2+2+3) and 10/8. See § 12.

### Groove
Straight vs. **swing** (the off-beat delayed toward a triplet feel) vs. **shuffle** (heavier swing, blues) is a bigger decision than tempo. Related feels worth naming explicitly: four-on-the-floor, backbeat on 2 and 4, **half-time** (backbeat moves to beat 3 only — instantly heavier), double-time hats, dembow (reggaeton), clave (Afro-Cuban), one-drop (reggae), boom-bap swing (slightly late snare), motorik (krautrock's steady eighth pulse).

### Tempo
BPM sets energy, but perception depends on subdivision. 140 with half-time drums reads as 70. 80 with double-time hats reads as 160. Decide both.

| Lane | Range | Common centre |
|---|---|---|
| Ambient / drone | 50–70 | 60 |
| Lo-fi, chill | 65–90 | 75 |
| R&B / neo-soul | 65–90 | 78 |
| Hip-hop (boom bap) | 82–96 | 90 |
| Ballad | 60–80 | 70 |
| Reggaeton | 88–100 | 95 |
| Indie folk | 85–110 | 95 |
| Pop | 100–130 | 118 |
| Disco / funk | 110–125 | 118 |
| House | 118–128 | 124 |
| Rock | 110–150 | 128 |
| Techno | 125–150 | 135 |
| Trap | 130–160 (half-time feel) | 140 |
| Drum & bass | 165–180 | 174 |
| Punk / hardcore | 150–200 | 170 |

**Translation:** give the number *and* the feel — "92 BPM, half-time backbeat, slightly behind the beat". Suno treats the number as approximate guidance; the feel descriptor is what keeps the groove honest.

---

## 6. Form and bar-count planning

Common bar counts (4/4): Intro 4–8 · Verse 16 · Pre-chorus 8 · Chorus 16 · Post-chorus 8 · Bridge 8 · Outro 4–8.

**Duration math:** seconds = (bars × beats-per-bar × 60) / BPM. A 16-bar chorus in 4/4 at 120 BPM is 32 seconds. Use this to hit a target length instead of guessing — and to notice when a plan is 90 seconds too long before generating.

Forms worth knowing:
- **Verse–Chorus** — pop default. Contrast lives between the two.
- **AABA (32-bar)** — standards, older pop. The B section (bridge) is the only contrast, so it must be genuinely different.
- **Verse–Refrain** — folk, singer-songwriter. No big chorus; a repeated final line carries the hook.
- **Through-composed** — no repetition. Cinematic, art song. Hard for Suno; expect it to impose repetition anyway.
- **Loop-based** — game and lo-fi music. 8 or 16 bars designed to seam. See genre blueprints.
- **Drop-based** — EDM. Build → drop is the whole form; energy management replaces harmonic development.

Suno approximates bar counts rather than obeying them, but planning them still pays off: it forces you to decide where contrast goes, and the section *order* is honoured reliably.

---

## 7. Melody and hook construction

A hook is a **motif** — typically 3–7 notes with a distinctive rhythm — that survives repetition. Development techniques: sequence (repeat at a different pitch), inversion, rhythmic displacement, augmentation/diminution, fragmentation (keep the tail, drop the head).

Principles that actually change how a chorus lands:

- **Contour.** The chorus should occupy a different register from the verse — usually a fourth or fifth higher. If the verse and chorus share a tessitura, no arrangement trick will make the chorus feel like a chorus.
- **The peak note.** One highest note in the song, placed on the most important word. Not repeated more than twice. If everything is high, nothing is.
- **Interval character.** A rising perfect fourth or fifth is anthemic. A rising minor sixth is yearning. A descending minor third is plaintive, almost speech-like (it's the "nyah-nyah" interval, and it's everywhere in folk). A rising octave is a shout.
- **Note density.** Sparse verses with long notes make a busy chorus feel urgent, and vice versa. Two sections with the same syllable density feel like one section.
- **Tension tones.** Land on the 7th or 9th and hold, and the melody sounds unresolved regardless of the chord underneath. Land on the root and it closes.
- **Anacrusis.** Starting the chorus phrase a beat *before* the downbeat pushes it forward. Starting on the downbeat plants it. This is a real choice.

**Translation:** Suno won't take a notated contour, but it responds to "chorus melody sits a fourth above the verse", "sparse long-held verse melody opening into a dense chorus hook", "vocal peaks once on the final chorus".

---

## 8. Vocal ranges, tessitura, and where to put the chorus

**Range** is what a singer can hit. **Tessitura** is where they sound good living. Chorus melodies belong in the upper tessitura — high enough that the singer is working, low enough that they aren't screaming.

| Voice | Typical range | Comfortable tessitura | Chorus sweet spot |
|---|---|---|---|
| Soprano | C4–C6 | G4–G5 | E5–A5 |
| Mezzo-soprano | A3–A5 | E4–E5 | C5–F5 |
| Alto / contralto | F3–F5 | C4–C5 | A4–D5 |
| Countertenor | G3–E5 | C4–C5 | — |
| Tenor | C3–C5 | E3–G4 | A4–C5 |
| Baritone | A2–A4 | C3–E4 | F4–A4 |
| Bass | E2–E4 | G2–C4 | D4–F4 |

**Passaggio** — the register break — is where the voice audibly strains, and that strain is expressive. Male voices break roughly around E4–G4; female voices have a lower break around E4–F#4 and an upper one around E5–F5. Contemporary pop belting deliberately parks the chorus right at or just under the break: female pop chorus peaks cluster in E4–C5, male in A4–C5. That's not an accident — it's where the voice sounds like it costs something.

**Practical consequence for key choice:** pick the key so the chorus peak lands in the sweet spot column. If you wrote a great melody in a key that puts the peak at F5 for a baritone, the key is wrong, not the melody.

**Translation:** don't specify pitches. Say "male tenor, chorus sitting at the top of his chest range, straining slightly on the peak" or "smoky female alto, low and close, never belts". Suno reads register descriptions well and reads note names not at all.

Always give all three vocal layers:
- **Character** — raspy female alto, smooth baritone, young androgynous tenor, weathered male voice
- **Delivery** — breathy, belted, conversational, whispered, spoken word, drawled, half-sung, strained
- **Effects** — dry close-mic, reverb-drenched, doubled in octaves, telephone-filtered, lo-fi, no autotune

---

## 9. Arrangement by register

Every element needs its own frequency lane, or the mix turns to mud. Suno ignores EQ instructions, but it responds to *arrangement* choices — which is where register conflicts are actually solved anyway.

| Band | Range | Occupants | Rule |
|---|---|---|---|
| Sub | 20–60 Hz | 808, sub bass, kick fundamental | One occupant only. Ever. |
| Bass | 60–250 Hz | bass guitar, kick body, low toms, left-hand piano | Kick and bass must interlock rhythmically, not overlap |
| Low-mid | 250–500 Hz | guitar body, snare body, male chest voice | The mud zone; thin it by *removing* players, not EQ |
| Mid | 500 Hz–2 kHz | vocal fundamentals, guitars, keys, horns | The crowded lane; the vocal wins, everything else moves |
| Upper-mid | 2–6 kHz | vocal intelligibility, snare crack, pick attack | Presence and harshness live together here |
| Air | 6–20 kHz | cymbals, breath, string sheen, reverb tails | Adds space; too much reads as brittle |

**The one-element rule.** At each section boundary, add or remove exactly one layer. Verse: voice + guitar. Pre: add bass. Chorus: add drums and a pad. Bridge: strip to voice + pad. That is an entire arrangement, and it will out-perform a prompt with fifteen instruments in it.

**Texture types worth naming:** monophonic (single line), homophonic (melody + chords — most pop), polyphonic/contrapuntal (independent lines — Bach, some prog), heterophonic (multiple ornamented versions of one melody — central to Turkish and Arabic classical ensembles).

Also decide: **countermelody** (a second line answering the vocal in the gaps — strings, guitar, horn) and **call-and-response** (gospel, funk, Afrobeat). Both make an arrangement sound composed rather than stacked.

**Translation:** "sparse verse of nylon guitar and voice only, upright bass enters at the pre-chorus, full kit and string pad at the chorus" — this is a Suno prompt *and* an arrangement chart. Register talk stays in your head; layer entries go in the prompt.

---

## 10. Dynamics and the emotional arc

Suno's default is loud-the-whole-way-through, which is the main reason AI tracks sound like AI. Fight it explicitly.

Plan a curve: where the quietest moment is (usually the start of verse 2 or the bridge), where the peak is (last chorus, ~75–85% through the song), and how the track leaves. The **false ending** — strip to almost nothing before the last chorus — is a cheap trick that works every time.

Encode it in two places: arrangement language in the Style field ("quiet verse to explosive chorus dynamic"), and inline cues in the lyrics ((stripped back), (building intensity), (full band, belted)). The lyric cues are the more reliable of the two.

---

## 11. Lyric prosody

Words are rhythm before they're meaning. Suno sings what you give it, so bad prosody produces rushed, crammed, mechanically-stressed vocals — the "AI voice" people complain about is often just a metrical failure.

- **6–10 syllables per line.** Longer lines get rushed or truncated.
- **Stressed syllables on strong beats** (1 and 3 in 4/4). Read the line aloud and tap: if the natural stress fights the beat, rewrite the line, don't fix it with a cue.
- **Open vowels on sustained high notes** — /a/, /o/, /e/ carry; /i/ and /u/ pinch, and consonant clusters on a held note are unsingable.
- **Verses 4–8 lines; choruses 2–4 lines.** Short choruses are catchier and land as hooks.
- **Strongest line first in each section** — Suno gives the opening line the most melodic weight.
- **Rhyme helps.** ABAB or AABB give the model rhythmic anchors. Free verse invites Suno to invent an arbitrary meter.
- **Repetition in choruses works.** One phrase repeated with escalation beats three different clever lines.
- **Concrete images over abstractions.** "The porch light" outperforms "my loneliness" — and it also gives the vocal harder consonants to bite.

### Turkish-specific

- Turkish is agglutinative, so it's trivially easy to rhyme on suffixes (*-yorum / -yordum / -acağım*). It sounds lazy and lands flat. Rhyme on content-word stems instead.
- Turkish word stress is usually final-syllable, which fits phrase endings on strong beats naturally — use it rather than fighting it.
- Vowel harmony makes long runs of the same vowel colour easy to produce accidentally; vary it, or the melody sounds monotone even when the pitches move.
- Turkish syllables are mostly open (CV), so syllable count maps to note count more cleanly than in English. 8–11 syllables per line often works where English wants 6–10.
- Suno's Turkish pronunciation is decent but stumbles on *ğ*, *ı* and long compound words. If a word matters, prefer a shorter synonym. Writing a problem word phonetically sometimes helps, but check it doesn't wreck the line's look.

---

## 12. Non-Western and makam material

Suno is a 12-TET model. It cannot produce koma (comma) intervals, so makams defined by microtonal degrees will be approximated — say this plainly rather than promising something the tool can't do.

| Makam | Nearest 12-TET | Notes |
|---|---|---|
| Hicaz | Phrygian dominant (1 b2 3 4 5 b6 b7) | Approximates well; the most Suno-friendly makam |
| Nihavend | Natural minor (Aeolian) | Maps cleanly |
| Kürdi | Phrygian | Maps cleanly |
| Rast | Mixolydian-ish | Rast's third is a koma flat — expect major-ish |
| Uşşak / Hüseyni | Dorian-ish | Second degree is a koma flat; will come out Dorian |
| Hüzzam / Segah | — | Genuinely microtonal; will not be reproduced. Get the flavour from instrumentation instead |

When the makam won't survive the approximation, carry the identity with **timbre and ornament** instead: ney, kanun, ud, bağlama/saz, kemençe, darbuka, bendir, davul-zurna, plus "glissando-heavy melismatic vocal", "quarter-tone inflected ornaments", "free-tempo taksim intro".

**Aksak meters** — say the grouping, not just the number: "9/8 aksak, grouped 2+2+2+3", "7/8 grouped 2+2+3". Suno's odd-meter reliability is mediocre; a groove descriptor ("limping, uneven pulse") plus the grouping does better than the fraction alone.

Same principle applies elsewhere: Indian raga (add "sitar, tabla, tanpura drone, meend slides"), flamenco (add "palmas, cajón, rasgueado, compás"), Balkan (add "brass band, kaval, uneven meter"), Japanese (add "koto, shakuhachi, in-scale"), West African (add "kora, talking drum, polyrhythmic 12/8"). Instrumentation carries identity more reliably than scale specification in every case.
