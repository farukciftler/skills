# Story Architecture for 2D Platformers

## Contents
1. Verb → meaning method
2. Premise formula and theme
3. Story spines (pick one)
4. Character design for platformers
5. The antagonist problem
6. Reveals, mystery and information budget
7. Death, failure and the respawn loop
8. Optional depth vs. critical path
9. Endings that use the controller
10. Common failure patterns

---

## 1. Verb → meaning method

In a platformer the player spends 90%+ of their time doing a handful of verbs. That is what the game is *about*, whatever the cutscenes say. Ludonarrative harmony means the mechanics and story point in the same direction; dissonance is when the story says one thing and the play says another (the classic example: a charming everyman in cutscenes who kills hundreds in gameplay).

Build a table before writing any plot:

| Verb | Literal | Emotional meaning | Where it peaks | Story beat it carries |
|---|---|---|---|---|
| climb | go up a wall, stamina limited | effort, stubbornness, "I can do hard things" | final chapter | refusing to quit |
| dash (1 charge) | burst, then must land to recharge | a risk you can only take once before resting | mid-game | trusting yourself |
| double dash (late) | two bursts | two parts of you cooperating | climax | self-acceptance |

The Celeste example above is real: the last power-up is just a double dash, born from Madeline and Badeline merging. The ability *is* the resolution.

**Questions to interrogate each verb**
- What does it feel like when this verb fails? (That failure feeling is your theme's dark side.)
- What changes if the verb gets stronger? Weaker? Taken away?
- Can the verb be done *with* or *to* another character? (That's where relationships live.)
- What would it mean to finally *not* need this verb?

**Mechanic-as-metaphor patterns**
- **Gain** — abilities return as the character heals (Gris: she can barely walk at the start; running, jumping, gliding, singing come back stage by stage).
- **Constraint** — a limit on a verb mirrors an inner limit (stamina = energy you don't have; one dash = one leap of faith).
- **Transformation** — a verb that looks negative becomes a tool (Gris: an awkward, tantrum-like block form introduced in the red/anger stage is later used to smash through obstacles).
- **Cooperation** — two inputs, two characters (Brothers: A Tale of Two Sons makes the control scheme the relationship).
- **Inversion** — the verb you used all game is refused or reversed at the end for meaning.

## 2. Premise formula and theme

Two sentences, no adjectives allowed except one:

> **[Character] wants [external, climbable goal] because [wrong belief about themselves or the world]. [Place] forces them to [learn the truth] through [core verb].**

Example: *Madeline wants to reach the summit because she believes finishing it will prove she's not broken. The mountain forces her to accept the part of her she's been running from, through climbing that she can only finish with that part's help.*

Theme = the gap between the wrong belief and the truth. State it privately in one line. **Never let a character say the theme out loud.** If the theme is spoken, it's a poster, not a story.

External goal must be *spatial* in a platformer: a summit, a bottom, an exit, a signal, a lost person, a place. The map is the plot.

## 3. Story spines

Pick one and justify it by the verbs.

### 3a. Three-act ascent (default)
- Act I (≈20%): ordinary world → arrival → first refusal/doubt. Tutorial chapters.
- Act II-a (≈30%): new places, new mechanics, allies met, the inner problem shows through the outer one.
- Midpoint: a false victory or a revelation that reframes the goal.
- Act II-b (≈25%): pressure rises, relationships strain, **the fall** (literal in a platformer: fall to the bottom, lose abilities, lose the ally).
- Act III (≈25%): the character changes, the verbs recombine, the final climb uses everything.
Celeste follows this with a literal fall to the mountain's base before the final ascent.

### 3b. Kishōtenketsu (no villain required)
Ki (introduce) → Shō (develop, deepen familiarity, no big change) → Ten (twist: something that doesn't fit enters) → Ketsu (reconcile the twist with everything before; a new understanding, not a victory).
Good for gentle, melancholic, curious games where "defeat the enemy" would feel false. Nintendo uses the same four-step shape at the level scale (see `flow-and-pacing.md`); using it at *both* scales makes the game feel coherent.

### 3c. Hub-and-return
A central space the player keeps returning to, changed each time by what they learned. Gris returns to a temple that grows more complete as each stage is passed. Great for games about recovery, grief, rebuilding. The hub is your progress bar made emotional.

### 3d. Descent-and-return
Go down into something (a city, a memory, a body, a machine), find the truth at the bottom, carry it back up. The return trip through changed versions of earlier rooms is where the payoff lives. Reuse art, recontextualize meaning.

### 3e. The loop
Death/reset is diegetic. Each run reveals more; characters remember. Hades is not a platformer, but its principle ports cleanly: if the whole game is dying and restarting, make the moment of death a narrative reward rather than a rage-quit moment.

## 4. Character design for platformers

Every named character gets a card:

```
NAME:
Want (external):
Fear (internal):
Wrong belief:
Verbal habit (one):
Physical habit / idle animation (one):
Gameplay touchpoint: what the player does with/against them
Arc in one line: from ___ to ___
Last line they say in the game (write it early):
```

Rules:
- **Protagonist:** give them a reason to move forward that the player shares. The player wants to explore and progress; the character should want something that requires the same.
- **Silent protagonist** works when the world is loud (Hollow Knight, Inside). If the protagonist talks, they need opinions, not just questions.
- **Characters revealed by action.** Hornet is introduced through battle; her movement tells you her agility and resolve before any backstory. A boss's attack pattern is characterization. Write the fight like a scene: what does this character want during the fight, and how do their moves show it?
- **Side characters are mirrors.** Each should reflect one version of the protagonist's problem (Celeste: a hotel owner whose anxiety literally fills his hotel; a friend who hides behind a camera). The protagonist learns by seeing someone else fail or succeed at the same thing.
- **Cap the cast.** 3–5 named characters for a 3–6 hour game. Every extra named character dilutes the others.

## 5. The antagonist problem

Platformers usually have environmental danger, not a speaking villain. Options:
- **The place is the antagonist** (the mountain, the facility, the dark). Give it rules and moods, not dialogue.
- **The inner antagonist made physical** (a shadow self, a pursuer). Must have a real argument; if it's just evil, it's a boss, not a character. Its best lines are things the protagonist secretly believes.
- **The system** (Inside: a world of controlled crowds and faceless authority). Show it; never name it.
- **No antagonist** — kishōtenketsu. The tension is curiosity and wonder.

Chases are the antagonist's best scenes. A pursuer that is always *one step* behind creates dread no cutscene can.

## 6. Reveals and information budget

- **Question ledger.** Keep a list: every question the game raises, the room where it's raised, the room where it's answered (or deliberately left open). No question left unanswered by accident.
- **Two-plus-two rule.** Give the player 2 + 2, not 4. The satisfying moment is when *they* do the sum.
- **Plant early, pay late.** Every major reveal needs at least two earlier plants the player can re-read in hindsight: a background object, a line that meant something else, a room layout.
- **Reveal in valleys.** Reveals land better when the player's hands are free (a safe room after a hard section).
- **Mystery vs. confusion.** Mystery = the player knows what they don't know and wants it. Confusion = they don't know what they're supposed to wonder about. Ambiguous endings (Inside) work because every scene before them was concrete and legible even when unexplained.

## 7. Death, failure and the respawn loop

Decide the fiction of dying:
- **Not diegetic, but acknowledged in tone** — a death counter framed as progress ("every death teaches you"). Celeste treats deaths as part of climbing.
- **Diegetic loop** — characters notice. Even one NPC remarking on how many times you've tried makes the retry feel seen.
- **Death as information** — each failure reveals something (a new angle, a hidden path, a line of dialogue).

Never punish retries with re-watching dialogue. Checkpoint **after** unskippable text, or make it skippable on repeat.

## 8. Optional depth vs. critical path

- Critical path: clear, concrete, understandable with zero optional content.
- Optional conversations: deepen side characters and theme. In Celeste you can miss a lot of backstory about side characters entirely if you skip the optional chats; the main story still stands.
- Collectibles: tie them to meaning if you can (a memory, a letter, a sketch). A collectible that is just a number is fine for challenge but adds nothing to story.
- Put the best optional content one step *off* the critical path, visibly (a side door, a campfire, a character sitting somewhere odd).

## 9. Endings that use the controller

- The final sequence should require the *combined* verbs of the whole game.
- Music, mechanics and story should converge on the same beat (Celeste's summit: the new double dash, the merged musical theme, and the reconciliation arrive together).
- After the climax, give a **quiet playable epilogue**: walking, looking, a last conversation. The player needs to come down from the peak with their hands still on the controls.
- Last line: short, specific, callback to something small from Act I. Not a summary of the theme.

## 10. Common failure patterns

| Symptom | Cause | Fix |
|---|---|---|
| "Story is fine but I skipped it" | Story lives only in cutscenes | Move beats into mechanics, rooms, bark lines |
| New ability feels random | No story reason for it at that moment | Tie each ability to a beat in the same chapter |
| Villain monologue | Antagonist has no gameplay presence | Replace with a chase or a fight that says it |
| Ending feels unearned | Final challenge doesn't use all verbs | Rebuild the last level as a remix of every chapter |
| Characters feel like signposts | They exist only to give directions | Give each a want that conflicts with the player's |
| Theme stated in dialogue | Writer doesn't trust the player | Delete the line; add a visual plant instead |
| Lore dump at the start | Fear the player won't understand | Start in motion; explain nothing for the first 10 minutes |
