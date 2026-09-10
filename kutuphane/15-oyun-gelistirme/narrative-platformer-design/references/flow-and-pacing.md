# Flow, Pacing and Immersion

## Contents
1. Flow channel: what "sürükleyici" actually means
2. Three rhythms to align (difficulty, story, music)
3. Kishōtenketsu per level/chapter
4. Game-feel forgiveness (if the controls feel unfair, the story dies)
5. Beat charts: columns, rules, example
6. Where words go: dialogue placement rules
7. Breathers, checkpoints and the retry loop
8. Chase and escape sequences
9. Momentum-preserving storytelling techniques
10. Playtest signals

---

## 1. Flow channel

Csikszentmihalyi's flow: challenge balanced against skill. Too much challenge → anxiety; too little → boredom; in between there is a fuzzy tolerance zone where the player loses track of time. Jenova Chen's thesis adds the part designers forget: the player also needs a **sense of control**, not just balanced numbers.

For a story platformer, "immersive / sürükleyici" = the player stays in that channel **and** always has a reason to take the next step. Two engines:
- **Mechanical pull:** "I can almost do this."
- **Narrative pull:** "I need to know / I need to get there / I need to see them again."

When one engine idles, the other must be running. A hard section with no story reason feels like a wall; a long story section with no play feels like homework.

Deliberate anxiety is allowed when it *is* the story. Celeste's harder chapters produce panic that mirrors the protagonist's; souls-likes keep players at the anxiety edge on purpose. The rule: anxiety must be followed by release, and the player must believe failure is their mistake, not the game's.

## 2. Three rhythms to align

Draw three lines across the same timeline:
1. **Difficulty/intensity** (1–10 per room)
2. **Story tension** (1–10: how much is at stake emotionally right now)
3. **Music/audio energy** (1–10)

Good pacing: story tension leads slightly, difficulty follows, music confirms. At key moments all three peak together (the climax), and at key moments all three drop together (the epilogue, the campfire). Bad pacing: story peak happens during a trivial room, or a brutal room happens while the story is idle.

## 3. Kishōtenketsu per level

Nintendo's stage design (Koichi Hayashida on Super Mario 3D World): each stage is a four-part showcase where a mechanic is taught, developed, twisted, then retired in a few minutes.

| Step | Level design | Story layer on top |
|---|---|---|
| **Ki** introduce | new mechanic in a safe space, no death risk | an image or line that frames what the mechanic will mean |
| **Shō** develop | same mechanic with real risk, variations | character reaction, a bark, the world reacting |
| **Ten** twist | mechanic used in an unexpected way or combined with a threat | the chapter's story twist lands here or right after |
| **Ketsu** conclude | mastery test | valley afterwards: the chapter's main dialogue/reveal |

Rule of thumb: the story twist should arrive *with* the mechanical twist, and the emotional payoff should arrive *after* the mastery test.

## 4. Game-feel forgiveness

If jumps feel unfair, players blame the game, frustration replaces flow, and nothing you write will land. Maddy Thorson's list of Celeste's invisible helpers (all of them widen timing or positioning windows slightly):

- **Coyote time:** you can still jump briefly after leaving a ledge.
- **Jump buffering:** press jump slightly before landing; the jump fires on the landing frame.
- **Halved gravity at the jump peak** while holding jump: more time to adjust landing.
- **Jump corner correction:** bonking a corner nudges you around it.
- **Dash corner correction:** clipping a ledge while dashing sideways pops you up.
- **Semi-solid popping** when dashing through one-way platforms.
- **Lift momentum storage:** jumping off a moving platform keeps its speed for a few frames after it stops.
- **Wide wall-jump window:** wall jump works a couple of pixels away from the wall; harder variants get an even wider window.

Narrative relevance: forgiveness is what lets you make a game *about* struggle without the struggle being fake. Also consider an **assist/accessibility mode**, framed without shame.

## 5. Beat charts

A beat chart is a spreadsheet that documents the whole game's flow like a music sheet: every beat, when each mechanic appears, where the quiet moments and twists land. Lead designers use it to spot long exhausting stretches or dead lulls that individual level designers can't see.

Columns in `assets/beat-chart-template.csv`:

| Column | Meaning |
|---|---|
| `id` | room/segment id (e.g. 2-04) |
| `chapter` | chapter number |
| `location` | short name |
| `kishotenketsu` | ki / sho / ten / ketsu / none |
| `mechanic` | main mechanic in this segment |
| `new_mechanic` | yes/no — first time the player sees it |
| `intensity` | 1–10 mechanical difficulty/tension |
| `story_tension` | 1–10 emotional stakes |
| `story_beat` | what happens narratively (blank if nothing) |
| `delivery` | none / bark / dialogue / cutscene / environment / collectible |
| `control_loss_sec` | seconds the player can't move (0 if none) |
| `checkpoint` | yes/no — checkpoint at the start of the segment |
| `est_minutes` | estimated play time for an average player |
| `music` | cue name or energy |
| `notes` | anything |

Checker rules (`scripts/beat_chart_check.py`):
- `delivery` in {dialogue, cutscene} with `intensity ≥ 7` → **momentum break**.
- More than 3 consecutive rows with `intensity ≥ 7` → **no breather**.
- A row with `intensity ≥ 8` not followed within 2 rows by `intensity ≤ 4` → **missing release**.
- `new_mechanic = yes` with `intensity ≥ 6` → **no safe introduction (Ki)**.
- `control_loss_sec > 45` → **long control loss**; also sums per chapter.
- Dialogue/cutscene row without `checkpoint = yes` on the next gameplay row → **retry punishes story**.
- Chapter's last row with both `intensity` and `story_tension` ≤ 3 → **flat chapter ending** (unless marked epilogue in notes).
- Story beat with `story_tension ≥ 8` but `delivery = none` → **missing delivery**.

## 6. Where words go

1. **After a spike, before the next one.** Relief + reward.
2. **In rooms with no threats**, ideally ones designed as stages (a bench, a fire, a window, an elevator).
3. **During low-skill traversal** (walk-and-talk): long safe corridors, elevators, rides. Oxenfree's walk-and-talk keeps the player moving while conversations happen, with no cutscenes.
4. **Never** during precision platforming, chases, or boss patterns. Barks of ≤ 5 words are the only exception, and they must not require reading to survive.
5. **Mind the room boundary.** A known walk-and-talk failure: players reach the edge of the screen before the conversation ends, then either cut the conversation off by walking on or pace around waiting. Fixes: size the corridor to the conversation (≈ 2.5–3.5 s per bubble), let conversations continue across room transitions, or queue the rest for the next safe room.
6. **Budget.** Light story platformer: dialogue ≤ 10% of play time, no single stop > 60 s, no more than one full cutscene per chapter.

## 7. Breathers, checkpoints, retry

- **Sawtooth curve**, not a ramp: tension rises across a segment, drops, then rises from a slightly higher floor. The drop is where the story lives.
- **Checkpoint density** scales with the cost of failure. Precision rooms: checkpoint every screen. Unskippable story: checkpoint *after* it.
- **Retry speed** is a pacing tool. Death → control should be under ~1 second in precision platformers. Every second of death animation multiplies across hundreds of deaths.
- **Breather room design:** open space, no hazards, pleasant audio, something to look at, often an optional conversation or collectible.

## 8. Chase and escape sequences

The highest-intensity story moments in platformers are usually chases (Inside's pursuit sequences; Ori's escape sequences such as the Ginso Tree). Rules:
- The pursuer should feel one step behind. Inside tunes escapes to be barely achieved, so each chase demands precision without feeling random.
- **Use only mechanics the player has already mastered.** The chase tests, it doesn't teach.
- **Short.** Under a minute of optimal play per segment. Checkpoint between segments; one-mistake-restart-from-zero over several minutes is a common complaint.
- **Readable at speed:** hazard silhouettes and colors must be unmistakable; no leaps of faith.
- **Music carries the story.** No text. Maybe one bark at the start.
- **Land it:** after the chase, a calm, beautiful release (swimming safely, a sunrise, silence).

## 9. Momentum-preserving storytelling

Ranked from least to most momentum cost:
1. Environment change (color, weather, architecture) — zero cost
2. Animation acting (character stumbles, looks back, hesitates) — zero cost
3. Audio (a motif returns, a voice in the distance) — zero cost
4. Bark (≤ 8 words, no input needed) — near zero
5. Walk-and-talk bubbles — low
6. Optional sit-down conversation — player's choice
7. Camera hold / pan with control kept — low
8. Forced walk / scripted movement — medium
9. Text box requiring input — medium
10. Full cutscene — high

Start from the top of the list. Move down only when the beat truly needs it.

## 10. Playtest signals

| Signal | Likely problem |
|---|---|
| Players skip text on first read | Too long, shown on a peak, or not interesting in the first 5 words |
| Players stop and wait for a bubble to finish | Corridor too short for the conversation |
| Death heatmap spike right after a cutscene | Player not re-oriented; add a safe beat after control returns |
| "Why am I doing this?" | Narrative pull missing in a hard stretch |
| Players can't retell the story | Too much implicit, no concrete anchors |
| Players retell it but feel nothing | Mechanics disconnected from story beats |
