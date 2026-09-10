# Anti-AI Pass + Non-native (Turkish speaker) Polish Pass

Run both passes on every piece of in-game text before delivery. The lint script catches the mechanical part; this file covers judgment.

## Contents
1. Why AI-flavored text kills a story game
2. Word-level kill list
3. Structural tells
4. Dialogue-specific AI tells
5. Turkish-speaker English pitfalls in dialogue
6. Deliberately non-standard English (when it's a character choice)
7. Rewrite drills

---

## 1. Why it matters

Players forgive simple writing. They don't forgive writing that feels generated: it signals nobody cared, and immersion drops. AI-flavored text is usually abstract, symmetrical, over-explained, and emotionally announced. Human dialogue is concrete, lopsided, under-explained, and emotionally leaky.

Caveat: these are *tells*, not laws. Plenty of human writers use em dashes and the word "crucial". The problem is density and pattern. Fix clusters, not single instances.

## 2. Word-level kill list

Wikipedia's "Signs of AI writing" guide lists words that show up disproportionately in AI text. For game dialogue, treat these as near-banned:

**Vocabulary:** delve, tapestry, testament, intricate, pivotal, crucial, vibrant, meticulous, underscore (verb), showcase, foster, bolster, enduring, garner, interplay, landscape (abstract), realm, beacon, symphony, journey (abstract), embark, navigate (abstract), unwavering, multifaceted, myriad, plethora, profound, resonate, ethereal, whispers of…, echoes of…, a sense of…

**Transitions in speech:** additionally, furthermore, moreover, indeed, nevertheless, ultimately, in conclusion, it is important to note. Real people say: also, and, plus, anyway, but, so.

**Fantasy-writing clichés that read as AI now:** "ancient power", "the fate of the world", "darkness spreads", "only you can…", "a light in the darkness", "it's not about the destination", "the real treasure…", "you were the key all along".

## 3. Structural tells

| Pattern | Example | Fix |
|---|---|---|
| **Rule of three everywhere** | "dark, cold, and silent" | Use one precise detail, or two, or four uneven ones |
| **"Not X, but Y" / "It's not just X, it's Y"** | "It's not just a tower. It's a promise." | Say the real thing once, plainly, or cut |
| **Em dash for punchy emphasis** | "The door was open—too open." | Comma, period, or restructure. Keep em dashes for real interruptions |
| **False ranges** | "from the deepest caves to the highest peaks" | Name one specific place |
| **Present-participle significance tails** | "…, highlighting the city's tragic past." | Delete the tail |
| **Symmetrical exchanges** | every line same length, every character equally articulate | Vary length, let someone be bad at talking |
| **Summarizing the scene at the end** | "So we've learned that trust matters." | End on action or a small specific line |
| **Everything resolved warmly** | each conflict closes with mutual understanding | Leave some things unsaid or unresolved |
| **Abstraction trap** | "I've been dealing with a lot of emotions" | "I cried in the elevator yesterday. Twice." |

## 4. Dialogue-specific AI tells

- **Therapy-speak in fantasy worlds:** "I need to set boundaries", "I hear you", "that's valid", "process my trauma". Wrong register, wrong era, and emotionally announced.
- **Characters narrating their own arc:** "I've changed so much since we started this climb."
- **Characters stating the theme:** "Maybe the mountain was never the real challenge… maybe it was me."
- **Perfect listening:** every line directly and helpfully answers the previous one. Real people talk past each other.
- **Uniform politeness:** nobody is rude, petty, awkward or boring. Give someone a bad mood.
- **Exclamation inflation:** "Let's go!" "We did it!" "Amazing!" Cap at one or two per scene.
- **Generic reassurance:** "You've got this!", "I believe in you!" Replace with something only *this* character would say to *this* person.
- **Wise mentor aphorisms:** "The strongest trees grow from the smallest seeds." Replace with a specific memory or a dry practical tip.

## 5. Turkish-speaker English pitfalls in dialogue

These show up even at C1. The lint script flags some; the rest need eyes.

**Grammar**
| Error pattern | Wrong | Right |
|---|---|---|
| Gender for "o" | "My sister? He's up there." | "She's up there." (check every he/she against the character sheet) |
| Dropped subject "it" | "Is very cold here." | "It's freezing." |
| Present continuous for duration | "I'm living here since the flood." | "I've lived here since the flood." |
| Articles | "I saw big bird on roof." / "The life is hard." | "I saw a big bird on the roof." / "Life is hard." |
| "Agree" as adjective | "I am agree." | "I agree." / "Yeah." |
| "Since / for" | "I'm waiting since three hours." | "I've been waiting for three hours." |
| "Until / by" | "Finish it until tomorrow." | "Finish it by tomorrow." |
| Plural "informations/advices" | "Thanks for the informations." | "Thanks for the info." |

**Word choice (literal translations)**
| Turkish | Literal (wrong) | Natural |
|---|---|---|
| ışığı aç / kapat | open/close the light | turn on / turn off the light |
| otobüsü kaçırmak | lose the bus | miss the bus |
| para kazanmak | win money (for wages) | make / earn money |
| sınav vermek | give an exam (as student) | pass an exam |
| telefonu kapatmak | close the phone | hang up |
| kontrol etmek | control it | check it |
| sempatik | sympathetic | likable, nice |
| fotoğraf çekmek | pull a photo | take a photo |
| söz vermek | give a word | promise |
| rüya görmek | see a dream | have a dream |
| hadi | "let's" (everywhere) | come on / let's go / hurry up |
| aynen | "same" | exactly / yep / right |
| kolay gelsin | "may it come easy" | (no equivalent; cut, or "Don't work too hard") |
| geçmiş olsun | "may it pass" | "Hope you feel better" / "That sucks, I'm sorry" |

**Register**
- **Too formal between friends:** "Could you please help me?" → "Help me with this?" / "Gimme a hand."
- **"Of course" overuse** (from "tabii"): → "sure", "yeah", "obviously" (depending on attitude).
- **Textbook exchanges:** "How are you? I'm fine, thank you, and you?" → nobody talks like this. "Hey." / "Hey. You look terrible." / "Thanks."
- **Over-apologizing politeness:** "Sorry, excuse me, I'm sorry to disturb you." → one "sorry" at most.
- **"Very very" / "so so"** → a stronger single word: "freezing", "starving", "exhausted".

## 6. Deliberately non-standard English

Non-standard English can be a character: a foreign traveler, a robot, a child, a rural dialect. If so:
- Write it in the voice bible ("drops articles, never uses contractions, calls everyone 'friend'").
- Keep it **consistent** and **light**; 1–2 features, not a wall of errors.
- Make sure it reads as a choice. One accidental-looking error next to one deliberate feature makes the whole thing look like a mistake.
- Never build humor on mocking a real accent or group.

## 7. Rewrite drills

**AI-flavored mentor**
```
BEFORE
SAGE: Your journey is a testament to your unwavering courage. Remember, it's not about reaching the summit—it's about discovering who you truly are.

AFTER
SAGE: Took me four tries to get past that ridge. You did it in one.
SAGE: Don't let it go to your head. The next bit's worse.
```

**Announced emotion + triplet**
```
BEFORE
MIRA: I feel scared, alone, and lost in this dark, cold, silent place.

AFTER
MIRA: Okay. Okay. Just... keep talking. Anyone. Please.
```
(Better still: no line at all, and a shaky idle animation.)

**Turkish-literal draft from the user**
```
BEFORE
MIRA: Open the light please, I am not seeing anything. My brother, he is waiting us since morning.

AFTER
MIRA: Can someone turn a light on? I can't see a thing.
MIRA: My brother's been waiting since this morning.
```
