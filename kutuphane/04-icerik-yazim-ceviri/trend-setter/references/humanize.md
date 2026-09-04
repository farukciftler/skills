# Humanize — Removing Every AI Tell

This file is the quality gate. Run it on every piece of copy before delivery, in every language. Detection in 2026 is mostly *human* detection: readers pattern-match AI style within two lines and stop reading. The lists below are current as of mid-2026; language models' tells drift, so when writing high-stakes content, spot-check with a quick web search for "AI writing tells [current month/year]" and fold in anything new.

## Contents
1. Why AI text is detectable
2. Layer 1 — Banned and red-flag vocabulary (English)
3. Layer 2 — Banned and red-flag vocabulary (Turkish)
4. Layer 3 — Structural tells
5. Layer 4 — What humans do (add these in)
6. The rewrite procedure
7. Calibration examples (before/after)

---

## 1. Why AI text is detectable

Language models regress to the statistical mean: the most likely word, the most balanced take, the most average rhythm. Human writing has two properties AI text lacks by default:

- **Perplexity** — surprising word choices, specific nouns, opinions that could be wrong
- **Burstiness** — wildly uneven sentence lengths and paragraph shapes

Everything below is a technique for restoring those two properties without making the text worse.

---

## 2. Layer 1 — Banned and red-flag vocabulary (English)

### Hard bans (classic tells — still checked by every editor and detector)
delve, tapestry, landscape (metaphorical), testament, elevate, unlock, unleash, leverage (verb), robust, seamless, game-changer, "in today's fast-paced world", journey (metaphorical), empower, foster, "navigate the complexities", realm, vibrant, bustling, "dive in / let's dive in", "buckle up", "look no further", "at the end of the day", "it's important to note", "in conclusion", "furthermore/moreover" chains, comprehensive, crucial (repeated), "a treasure trove", boasts, "nestled", "whether you're a X or a Y"

### 2026-era tells (newer patterns flagged by editors this year)
- **"quiet" as a weight-adder** — quiet confidence, quiet rebellion, quietly powerful, "the quiet truth". One use max; usually delete.
- **Unsolicited validation** — "You're not imagining it", "You're not alone", "You're not broken", "It's okay to feel...". Therapy-speak grafted onto business content. Delete.
- **"earn" + abstraction** — earn trust, earn attention, "earn the right to". The verb fakes rigor. Say what actually happens.
- **Reverence for "the work"** — "do the work", "trust the work", "the work itself". Vague effort-worship. Name the actual task.
- **Metaphorical "hold"** — hold space, hold the line, "the grip it holds". Max one, prefer zero.
- **"the pull of / feel the pull"** — names a force without naming the motivation. Name the motivation.
- **Insight-announcing** — "Here's the thing:", "Let me be clear:", "The truth is...", "Read that again." State the insight; don't introduce it.
- **Contrast reframes** — "It's not about X. It's about Y." / "X isn't just Y — it's Z." One of the strongest current tells. Zero per post.
- **Fake-empathy openers** — "Picture this:", "We've all been there", "As a founder, you know...". Replace with a specific, gritty scene.

### Soft flags (fine once, tell in bulk)
honestly, actually, genuinely, "the reality is", truly, ultimately, "at its core", powerful, transformative, "double-edged sword", "silver lining"

---

## 3. Layer 2 — Banned and red-flag vocabulary (Turkish)

Turkish AI output has its own fingerprint: it reads like a translation from English, over-formal suffixes, and TV-ad CTAs. Ban list:

### Hard bans
- "Günümüzün hızlı tempolu dünyasında", "dijital çağda", "teknolojinin hızla geliştiği bu dönemde"
- "Keşfedin", "Hemen keşfet", "Kaçırmayın!", "Hemen tıklayın", "Sizler için derledik"
- "İşte karşınızda", "Haydi başlayalım", "Gelin birlikte bakalım", "Hazırsanız başlıyoruz"
- "Unutmayın ki...", "Şunu belirtmek gerekir ki", "önem arz etmektedir", "büyük önem taşımaktadır"
- Aşırı resmî ek yığını sosyal içerikte: "bulunmaktadır", "gerçekleştirilmektedir", "sağlanmaktadır" — konuşur gibi yaz: "var", "yapılıyor", "sağlıyor"
- Çeviri kokan kalıplar: "Bu, ... anlamına geliyor", "... olduğunu unutmayın", "işte bu yüzden", gereksiz "bir" ("harika bir deneyim sunuyor")
- "Sonuç olarak", "Özetle", "Kısacası" ile kapanış paragrafı
- "-manın 5 yolu" tarzı jenerik başlıklar (sayı + "yolu/ipucu/sırrı" üçlemesi arka arkaya)

### Yapısal Türkçe teller
- Her cümlenin sonunda ünlem. Ünlem bütçesi: kısa postta en fazla bir.
- Her satır başında emoji. Emoji süs değil noktalama gibi kullanılır — bir postta 0–2, konuya oturuyorsa.
- "Siz de ... değil mi?" tarzı zorlama katılım soruları.
- Kusursuz paralel maddeler ("Hızlı. Güvenli. Kolay." üçlemesi) — İngilizce rule-of-three'nin Türkçesi, aynı şekilde yasak.
- Devrik cümle hiç yoksa metin makine kokar. Türkçenin doğal konuşma ritmi devrik yapıyı sever: "Denedim ben bunu geçen ay." Yer yer kullan.
- "Yani", "ya", "bir de", "hani", "işin kötüsü", "neyse" gibi bağlaçlar konuşma dokusudur — platform tonuna göre serpiştir.

---

## 4. Layer 3 — Structural tells

These matter more than vocabulary. A post can use clean words and still scream AI through shape.

1. **Rule of three** — "adjective, adjective, adjective" or three parallel phrases. Humans occasionally use it; AI defaults to it. Budget: zero to one per piece, never in the hook.
2. **Em dash density** — cap at ONE per short post, roughly one per 300 words long-form. If the draft has three, that alone outs it. Replace with periods, commas, or parentheses.
3. **Uniform sentence length** — the strongest statistical tell. If most sentences land 15–22 words, break the pattern hard: a three-word fragment, then a 30-word run-on that would annoy an English teacher slightly.
4. **Essay skeleton on a social post** — intro, three body paragraphs, summary conclusion. Social posts start mid-thought and stop when the point lands.
5. **Summary endings** — any closing paragraph that restates what was said. Delete the last paragraph; the post is almost always better.
6. **Diplomatic both-sidesing** — "there are pros and cons", careful neutrality on everything. Humans take sides. If the piece contains no claim someone could disagree with, it isn't finished.
7. **Abstract hypotheticals** — "a marketing team might use this to improve engagement". Replace with a concrete scene: "when the POS dies at 7pm on a Friday and the kitchen's understaffed".
8. **Bold-term-colon bullets** — "**Consistency:** posting daily builds trust". A formatting tic. Rewrite bullets as natural sentences or cut the bullets entirely.
9. **Perfectly parallel bullet grammar** — every bullet starting with the same verb form. Vary or prune.
10. **Over-signposting** — "In this post, I'll cover...", "Now let's look at...". Just say the thing.
11. **Emoji as line-item decoration** — 🚀 at the start of every bullet, the ✨💡🔥 cluster. Emojis are punctuation, not wallpaper.
12. **Hashtag dumps** — a wall of 15 hashtags reads bot. Platform-correct counts live in `platforms.md` (short version: LinkedIn ~0, Instagram 3–5, TikTok 2–4, X 0–1).
13. **Title Case On Every Header** and headers on content too short to need headers.
14. **Hedging stacks** — "may potentially help to somewhat improve". One qualifier max per claim.
15. **Generic praise inflation** — "revolutionary", "iconic", "renowned" attached to ordinary things. Specific beats superlative: "the first tool that reconciles AWS CUR line items nightly" outranks "a revolutionary FinOps platform".

---

## 5. Layer 4 — What humans do (add these in)

Removing tells produces sterile text. Add the positive signals back:

- **A stance.** At least one sentence someone could argue with. Mild spice is memorable; balance is forgettable.
- **Numbers with texture.** 37%, not "about 40%". 4.300 TL, 11 days, v2.3. Round numbers read invented.
- **Named specifics.** Tools, cities, error messages, line items. Proper nouns are perplexity.
- **Human uncertainty.** "no idea why this works, but it does" builds more trust than confident vagueness.
- **Rhythm breaks.** Fragments. One-word sentences. A sentence starting with And or But (Türkçede: Ama, Yani, Bir de).
- **A small imperfection.** A parenthetical aside, a self-correction ("wait, that's not quite right — it was Tuesday"), a tangent that earns its place. One per piece, not three.
- **Contractions and platform register.** don't/won't/it's everywhere in casual contexts; lowercase openers are native on X in many niches.
- **A real ending.** Humans stop on the point, a question, or a punchline — never on a recap.
- **First-person texture — within the integrity rule.** Personal detail humanizes fastest, but only from material the user actually gave. Invented experiences presented as true are forbidden (see SKILL.md non-negotiables). When no real anecdote exists, write honest observation instead of fake memoir.

---

## 6. The rewrite procedure

Run in order on every draft:

1. **Banlist scan** — search the draft for every Layer 1/2 term. Replace with plain verbs and concrete nouns.
2. **Structure scan** — count em dashes (≤1), contrast reframes (0), triads (≤1), bold-colon bullets (0). Fix.
3. **Rhythm pass** — eyeball sentence lengths. If they cluster, split one sentence into a fragment and merge two others.
4. **Concreteness pass** — every claim gets a number, name, or scene, or gets cut.
5. **Stance check** — find the sentence someone could disagree with. If absent, sharpen one.
6. **Ending check** — if the last paragraph summarizes, delete it. Test whether the piece is better. (It is.)
7. **Read-aloud test** — anything you wouldn't say out loud to a colleague at lunch gets rewritten in the words you *would* say.
8. **Squint test** — visually: varied line lengths, white space, no bullet wall, no emoji rail.

If steps 1–2 triggered more than ~5 fixes, don't patch — redraft from the voice fingerprint. Patched AI text reads like patched AI text.

---

## 7. Calibration examples

### English — LinkedIn post

**Before (AI-flavored):**
> In today's fast-paced world, consistency is the key to unlocking growth on LinkedIn. It's not about posting more — it's about posting smarter. Here's the thing: engagement, authenticity, and value are the three pillars of a robust content strategy. Whether you're a founder or a marketer, remember: the algorithm rewards those who show up. In conclusion, start posting consistently today!

**After (human):**
> I posted daily on LinkedIn for 60 days. Reach went down.
>
> Then I cut to twice a week and spent the saved time replying to comments within the hour. Reach tripled in three weeks.
>
> The feed reads your post semantically now and watches what happens in the first 90 minutes. Volume isn't a strategy. Conversation is.
>
> Anyone else seen posting less work better?

### Turkish — X/LinkedIn post

**Önce (AI kokan):**
> Günümüzün hızlı tempolu iş dünyasında bulut maliyetlerini yönetmek büyük önem arz etmektedir. FinOps sadece bir araç değil, bir kültürdür. Doğru strateji ile maliyetlerinizi düşürebilir, verimliliğinizi artırabilir ve rekabet avantajı elde edebilirsiniz. Unutmayın: Görünürlük, optimizasyon ve raporlama başarının anahtarıdır! 🚀

**Sonra (insan):**
> Geçen ay bir müşterinin AWS faturasında 11 aydır kimsenin bakmadığı bir NAT Gateway bulduk. Aylık 840 dolar. Boşta.
>
> FinOps'un yarısı zaten bu: kimsenin sahiplenmediği kaynağı bulup kapatmak. Dashboard sonra geliyor.
>
> Sizin faturada da vardır. Bakın bi.

Note what changed in both: a specific scene with a non-round number, shorter and uneven sentences, a stance, a native ending, zero banned phrases, zero em dashes, and the summary paragraph is gone.
