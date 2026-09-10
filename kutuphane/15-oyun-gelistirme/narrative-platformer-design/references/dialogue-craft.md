# Dialogue Craft (English, human-sounding)

## Contents
1. What game dialogue has to do
2. The ten habits of real-sounding speech
3. Subtext techniques
4. Exposition without "As you know, Bob"
5. Surface constraints: bubbles, boxes, reading speed
6. Voice: making characters distinguishable
7. Barks and ambient lines
8. Reactive and state-based dialogue
9. Walk-and-talk, interrupts, silence
10. Player choices that don't feel like menus
11. Humor timing in text
12. Before/after rewrites

---

## 1. What game dialogue has to do

Each line should do at least two of: characterize, advance the relationship, deliver needed info in a masked way, set mood, foreshadow, or give the player a reason to keep moving. A line doing only one job (usually "deliver info") is a candidate to cut or merge.

Game dialogue is harder than film dialogue because the player is *reading while wanting to play*. That's why the default is short, fast, and skippable without losing the critical path.

## 2. The ten habits of real-sounding speech

1. **Contractions.** "I'm", "don't", "it's", "gonna" (for casual characters). Uncontracted speech ("I do not know") sounds robotic or very formal; use it only as a deliberate trait.
2. **People answer the question they wish they'd been asked.** Direct question → indirect answer is the default in emotionally loaded moments.
3. **Fragments.** "Up there? No way." Real people rarely speak in complete, balanced sentences.
4. **People don't say each other's names.** Outside of calling someone or making a point, names are rare. A name every other line is a strong fake-dialogue signal.
5. **Nobody describes what both people can see.** "Look, a huge door covered in vines!" → cut. The player sees it.
6. **Short turns.** Most lines under 12 words. Long lines only when someone's rambling *is* the character, or the long line is the emotional release of the scene.
7. **Interruption and overlap.** "I just think maybe we—" / "Don't." Em dashes for cut-offs are fine here; that's their honest job.
8. **Specifics beat abstractions.** "I haven't slept since Tuesday" beats "I've been struggling lately."
9. **Emotions leak, they aren't announced.** "I'm scared" is sometimes right (once, at the peak). Most of the time fear shows up as a joke, a complaint about the cold, or a sudden change of subject.
10. **Filler is flavor, used sparingly.** One "uh" or "I mean" can make a nervous character real; ten make the scene unreadable. Page dialogue is cleaner than real speech on purpose.

## 3. Subtext techniques

- **Talk about the object, mean the person.** Two friends arguing about who packed the snacks are arguing about who always takes care of whom.
- **The deflection.** A: "Are you okay?" B: "This wind is insane." (B isn't okay.)
- **The too-quick answer.** A: "Do you miss him?" B: "No." (followed by silence or a jump)
- **The callback.** A phrase from Act I returns in Act III with a new meaning. Nobody points it out.
- **Mismatched energy.** One character is light, the other isn't picking it up. The gap is the scene.
- **Action instead of reply.** In games you have animation: the character turns away, sits down, keeps walking. A line + an action that contradicts it is peak subtext.
- **The question that isn't a question.** "You're really going up there." (not "Are you really going up there?")

Test: cover the line and ask, "What does this character *want* in this moment?" If the line states that want directly, it's on the nose. Keep maybe one on-the-nose line per major scene, at the turning point, where the plainness hits hard because everything around it was indirect.

## 4. Exposition without "As you know, Bob"

"As you know, Bob" = two characters telling each other what both already know, purely for the audience. Fixes, in order of preference:
1. **Put it in the world** (a sign, a ruin, a crowd's behavior). See `environmental-storytelling.md`.
2. **Ask the newcomer.** The protagonist or someone else genuinely doesn't know. Only works once or twice per character.
3. **Argue about it.** Two characters disagree about the fact; the fact slips out as ammunition. "You think the lift still works? Nothing's worked since the flood."
4. **Wrap it in a joke or a complaint.** Shakespeare's clowns and gravediggers deliver backstory while cracking jokes.
5. **Interrupt it.** The reveal gets cut off; the player gets half, and wants the other half.
6. **Delay it.** The player doesn't need backstory until they care. Let them wonder first.

Budget: in the first 10 minutes, the player needs to know *what to do next*, not *why the world is like this*.

## 5. Surface constraints

**Speech bubbles (above heads):** Night in the Woods wrote nearly everything at tweet length and used segmenting, pauses and single-word bubbles for humor and tension. Practical limits:
- ≤ 90 characters per bubble for normal lines; ≤ 50 for walk-and-talk
- Break long thoughts into 2–3 bubbles at natural breath points
- A one-word bubble after a pause is a comedy/tension tool

**Dialogue boxes (bottom of screen):**
- 2–3 lines per box, ~35–45 characters per line
- Never split a sentence across boxes mid-clause
- Portrait + name tag, or name tag only; be consistent

**Reading speed & timing:**
- Auto-advancing text: ~ 3 s base + 0.05 s per character, and never faster than the slowest readers you care about. Better: player-advanced, with a hold-to-fast-forward.
- Typewriter effect: fast by default; tap completes the line instantly; second tap advances.

**Localization headroom:** German commonly runs 20–35% longer than English, and short strings expand the most. Design bubbles and boxes with ≥ 35% extra room or allow wrapping. Never concatenate sentence fragments in code.

## 6. Voice

Fill `assets/voice-bible-template.md` for each speaker. The dimensions that actually differentiate characters:

| Dimension | Example contrast |
|---|---|
| Sentence length | clipped vs. run-on |
| Vocabulary | plain/Anglo-Saxon vs. Latinate/formal |
| What they notice | people vs. objects vs. danger vs. food |
| How they deflect | jokes / facts / anger / silence / changing subject |
| Certainty | hedges ("maybe", "kinda") vs. declarations |
| Questions | asks a lot vs. never asks |
| Swearing | never / mild / creative |
| Verbal tic | one. Only one. Used rarely. |

**Name-removal test:** strip speaker names from a scene. If you can't tell who's talking, the voices are too similar.

**Age and era:** teenagers don't say "indeed"; old people don't say "lowkey". But avoid dated slang that will age badly; favor rhythm and attitude over trendy words.

## 7. Barks and ambient lines

Barks: short, repeatable lines triggered by events (entering an area, taking damage, idling, seeing something). They carry world-building and personality with near-zero momentum cost.
- Think of a bark as the **middle or end of a longer conversation** you overheard. Pick the juiciest line.
- **Start from a verb:** what is this NPC *doing* while talking? Fixing, waiting, hiding, eating? People don't loiter on corners waiting to deliver lore.
- Two natural modes: **thinking aloud** and **overheard banter**.
- Keep quirks subtle; barks repeat, and loud quirks get annoying fast.
- Write 3–5 variants per trigger; never play the same one twice in a row.
- Hint barks: a nudge, not a solution. "That ledge looks crumbly" (not "Dash to the left ledge before it falls").

## 8. Reactive and state-based dialogue

Model from Hades' system (portable to any game with repeated visits): conversations are a **bucket filtered by game state and weighted by importance**. Roughly three tiers:
1. **Generic** — always valid, low priority, lots of variants.
2. **Specific, non-essential** — triggered by something the player did (used a certain ability, died a certain way, found a secret). Some apply only immediately; some stay valid forever after.
3. **Essential story beats** — triggered by milestones; override everything else.

When the player talks to an NPC, pick the highest-priority unplayed valid line. The magic moments are tier 2: a character commenting on how you *just* died makes the game feel like it sees you.

For platformers: react to death count ranges, time spent in a room, collectibles found, ability used last, whether the player skipped the previous conversation, returning to a hub after a hard chapter.

Track with simple flags/counters; see `implementation.md` for the schema.

## 9. Walk-and-talk, interrupts, silence

Oxenfree's design (a "Limbo, but you can talk" pitch): dialogue appears as bubbles while the player keeps moving; choices appear above the protagonist; the player can wait, **interrupt**, or **stay silent**, and silence is itself a choice.

Transferable rules:
- Choices appear as short bubbles (≤ 4 words each, 2–3 options max).
- Timed choices must allow a "say nothing" outcome that is written, not a failure.
- Interrupting should change the next line (the other character reacts to being cut off).
- Conversations must survive room transitions or be sized to the corridor.

## 10. Choices that don't feel like menus

Night in the Woods deliberately avoided Big Moral Choice moments and made branching feel organic and tangent-prone: the game is about exploring who the character *is*, not building who you want her to be. Good choice types for story platformers:
- **Who you spend time with** (whose storyline you see)
- **Tone choices** (same info, different attitude)
- **What you notice** (optional interactions)
- **Silence vs. speaking**

Avoid choices where one option is obviously "good". Label options with what the character would *say*, not a summary like "[Be supportive]".

## 11. Humor timing in text

- The punchline goes **last** in the bubble, and ideally alone in its own bubble.
- Undercut, don't explain. The joke lands in the gap; a follow-up explanation kills it.
- Rule of three works for jokes (setup, setup, twist) — but only for jokes; see the anti-AI file for why triplets elsewhere smell.
- Characters who are funny when scared are more real than characters who are funny all the time.

## 12. Before/after rewrites

**Exposition dump → argument**
```
BEFORE
ELDER: As you know, the Lantern Guild abandoned the city twenty years ago after the Great Flood, and since then the lights have been dying one by one.
MIRA: Yes, and that is why I must climb the tower and relight the first lantern.

AFTER
ELDER: You're climbing the tower. For a lantern.
MIRA: Somebody has to.
ELDER: The Guild said that too. Right before they packed up and left us in the dark.
MIRA: Then I'll do it better than them.
```

**On-the-nose feeling → deflection + action**
```
BEFORE
TEO: I feel very sad that my brother left without saying goodbye, and I am worried he will not come back.

AFTER
TEO: He took the good rope.
MIRA: ...That's what you're mad about?
TEO: It was a really good rope.
[TEO turns away, starts climbing without waiting for her]
```

**Describing the visible → reacting to it**
```
BEFORE
MIRA: Wow! Look at that giant broken bridge in front of us! It seems we cannot cross it.

AFTER
MIRA: Oh, come ON.
```

**Name overuse and symmetry → natural rhythm**
```
BEFORE
KAI: Mira, we need to be careful here.
MIRA: I know, Kai. This place is dangerous, dark, and full of secrets.
KAI: Exactly, Mira. Let us move forward together.

AFTER
KAI: Watch the floor.
MIRA: I'm watching the floor.
KAI: You're watching me watch the floor.
MIRA: Because you're being weird about the floor.
```

**Bark set (idle guard, tired, underpaid)**
```
- "Twelve hours. For a door."
- "If you're a ghost, at least be a quiet one."
- "...I'm not sleeping. I'm resting my eyes. Standing up."
- "Nobody told me there'd be stairs."
```
