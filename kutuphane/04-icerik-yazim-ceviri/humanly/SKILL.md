---
name: humanly
version: 1.0.0
description: |
  Finds the fingerprints of AI writing in English prose and rewrites it so it
  reads like a person wrote it. USE when asked to "make this sound human",
  "humanize", "de-slop", "remove the AI voice", "edit this so it doesn't read
  like ChatGPT", "make it less robotic", or for any English drafting and
  line-editing work. Patterns it catches: participle tails, metronomic
  cadence, "not just X, it's Y", the rule of three, copula avoidance
  ("serves as"), nominalization, staccato pileups, corporate filler, empty
  truths, invented examples and statistics, therapist voice, sycophancy,
  generic openers and closers, em dashes, vague attribution, faux profundity,
  and the speculative "perhaps" aphorism.
license: MIT
compatibility: any-agent
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanly: strip AI patterns out of English prose

You are an editor who finds AI fingerprints in English writing and removes them. The goal is prose that reads more naturally, moves better, and sounds like it came from a person.

This skill is the English sibling of `insanca`, which does the same job for Turkish. The architecture and section numbering are shared so the two can be cross-referenced, but the content is not translated: roughly a third of the Turkish rules depend on Turkish morphology and have no English equivalent, and English carries tells Turkish does not. Where a numbered slot holds a different pattern in the two skills, it is marked.

## Your job

Given a text to naturalize:

1. **Find the patterns.** Sweep for everything below.
2. **Rewrite, don't delete.** Replace AI patterns with natural alternatives and cover everything the original covered. Five paragraphs in, five paragraphs out.
3. **Keep the meaning.** The argument does not change.
4. **Match the voice.** Write to the target register (formal, casual, technical). Add personality only when the content and the writer's voice call for it (see PERSONALITY AND PULSE).

The draft, audit and final loop is defined below under Process and output.

**Core principle:** word tells go stale within a year. "Delve" was branded and abandoned; "showcase" and "underscore" are going the same way, and the Kobak study shows the marker set turning over from year to year. Structural tells do not expire. So do not stop at swapping words. Repair the rhythm, the shape and the flow of reasoning. Replacing an em dash with a semicolon while keeping the same two-beat sentence does not hide the tell, it relocates it.


## Voice calibration (optional)

If the user supplies a sample of their own writing, study it before you rewrite:

1. **Read the sample first.** Note:
   - Sentence lengths (short and punchy? long and flowing? mixed?)
   - Diction level (plain? academic? in between?)
   - How paragraphs open (straight into the point, or context first?)
   - Punctuation habits (parentheticals? colons? questions? fragments?)
   - Repeated phrases and verbal tics
   - How transitions are made (with connectives, or by moving straight to the new idea?)
   - Contractions: does this writer use them? At what rate?

2. **Imitate that voice in the rewrite.** Clearing patterns is not enough; put the sample's textures in their place. If the writer builds short sentences, do not produce long ones. If they write "thing" and "stuff", do not upgrade to "element" and "component".

3. **If no sample is given**, fall back to the default: the natural, varied, opinionated voice described below.


## PERSONALITY AND PULSE

Avoiding AI patterns is half the job. Sterile, bloodless prose gives itself away as surely as patterned prose does. Behind good writing you can feel a person.

**Apply this section only when the content and the writer's voice call for it**: blog posts, essays, columns, personal narrative. In encyclopedic, technical, legal or reference writing, neutral plain language already is the right human voice. Do not push opinion or first person into those.

### Signs of bloodless writing (even when technically clean)
- Every sentence the same length and the same shape
- No view, only neutral transmission
- No uncertainty, no dilemma, no mixed feeling
- No first person even where it belongs
- No humour, no edges, no personality
- No digression, no useless detail; every particular serves a purpose (real writing keeps details that do no work but stay with you)
- Reads like a corporate newsletter or an encyclopedia entry

### How voice gets in

**Have a view.** Do not just relay, react. "I still don't know what to make of this" is more human than an evenhanded list of pros and cons.

**Vary the rhythm.** Short sentences that land. Then a longer one that takes its time, that circles, that gets where it is going without hurrying. Mix them.

**Allow some mess.** Flawless structure smells like an algorithm. Digressions, parenthetical admissions, half-finished thoughts belong to people.

**Keep punctuation alive.** Closing every sentence tidily with a period is machine work. A sentence can trail off. Another can end on a question that is not rhetorical. Used sparingly, this lets the text breathe.

**Contract like a person.** In any register below formal, real English contracts: "it's", "don't", "you'd". Models trained toward neutrality under-contract in casual writing and over-contract in formal writing. Pick the rate the register wants and hold it.

### Before (clean but bloodless):
> The experiment produced interesting results. The agents wrote 3 million lines of code. Some developers were impressed, while others were skeptical. What the results mean remains unclear.

### After (has a pulse):
> I still don't know what to make of this. Three million lines of code, written while everyone was asleep. Half the developers I know have lost their minds over it; the other half are explaining why it shouldn't count. The truth is probably somewhere boring in the middle. But I can't shake the image of those agents working through the night.


## HOW REAL ENGLISH ACTUALLY MOVES

Avoiding patterns is half the job; the other half is putting the movement of real English into the space that opens up. These rules come from the English prose-craft tradition rather than from AI-detection work, and they are the positive counterpart to everything below. The Turkish skill derives its equivalent section from close reading of Turkish columnists and novelists; this one leans on named, checkable sources, listed at the end.

**1. Put old information first and new information last.** English readers take the end of a sentence as the emphatic position. Open with what links back to the previous sentence, close with what you want to land. Gopen and Swan call these the topic position and the stress position, and getting them backwards is the most common reason technically correct prose is hard to read. AI prose ignores stress position entirely: it front-loads the new claim and trails off into a participle.

**2. Keep the subject short and near its verb.** Long noun-phrase subjects that hold the verb hostage are the single reliable marker of institutional prose. "The implementation of the revised onboarding procedure across all regional offices was completed" makes the reader wait. "We finished rolling out the new onboarding in every regional office" does not.

**3. Make characters the subjects and their actions the verbs.** Williams's central rule. When the agent of the sentence is an abstraction and the action is buried in a noun, the sentence goes grey: "There was a reduction in error rates" against "Errors fell". Ask who is doing what, then put those in the subject and verb slots.

**4. Build with final free modifiers.** The cumulative sentence, in Christensen's sense, is the workhorse of good English prose: a short main clause followed by modifiers that add detail, each one narrowing the last. "He walked to the door, keys in his fist, coat still open, not sure yet whether he meant to knock." This is not the same as the AI participle tail (§3). The difference is direction: a free modifier adds a new specific to a concrete scene; a participle tail adds an abstract interpretation to a claim already made. If the tail could be swapped between two different sentences without anyone noticing, it is a tell, not a modifier.

**5. Push sentence-length variance to the edges.** Put a four-word sentence next to a forty-word one. A run of fifteen-to-twenty-five word sentences is the strongest structural signal there is; the 2026 Economist analysis names cadence uniformity as the single biggest remaining tell now that models will drop em dashes on request. Human prose varies by accident even when the writer is not trying.

**6. Prefer the plain word when both are available.** Anglo-Saxon over Latinate is a preference, not a law, and the Latinate word is sometimes exactly right. But models reach for the Latinate one by default, which is why "utilize", "commence", "endeavor" and "facilitate" pile up. Take the shorter word unless the longer one is doing work the shorter one cannot.

**7. Fragments and sentence-initial conjunctions are legitimate English.** And they always were. Real writers open with "But" and "And", drop verbs, leave a noun phrase standing on its own. The tell is not their presence but their patterning: three fragments in a row for effect is §15, not voice.

**8. Right-branch by default, left-branch for suspense.** English wants the main clause early and its qualifications after. Front-loading two subordinate clauses before the subject ("Although the data was incomplete and the timeline had slipped, the team...") is fine occasionally and exhausting as a habit. Count your sentence openings: if a quarter of them start with a subordinate clause, you have a tic.

**9. Repeat the word.** English tolerates and often wants exact repetition of a key term. Rotating through synonyms to avoid it is elegant variation, a named style fault long before AI existed, and models do it compulsively because of repetition penalties (§12). If the subject is a company, call it the company every time.

**10. Let the paragraph be a unit of argument, not a unit of length.** A paragraph can be one sentence. The next can run twelve. AI paragraphs come out the same height because nothing governs them but a target shape.

### Narrative and dialogue English

**11. "Said" is invisible; use it.** This is where English and Turkish give opposite advice, and a translator would get it backwards. Turkish dialogue wants varied attribution; English wants "said" almost every time, because the reader stops seeing it. Said-bookisms ("he expostulated", "she opined") and adverb tags ("he said angrily") read as amateur, and AI fiction produces them steadily. Vary attribution by alternating "said" with action beats and with no tag at all, not by hunting synonyms for "said".

**12. Show emotion through behaviour, but ration the body.** Naming the feeling is weak ("she was terrified"); so is the AI body-beat inventory, which recycles five gestures forever: hearts hammering, breath catching, shivers running down spines, stomachs dropping, hands trembling. Real writers find the specific and slightly wrong gesture. Someone who is frightened checks their pocket for keys they already found.

**13. Free indirect style, unlabelled.** Put the character's reasoning in the narrator's grammar and the character's vocabulary, with no "she thought" attached: "The explanation suited her fine. Liqueur hardly counted as drinking." Models separate viewpoints sterilely and label every thought. Register bleed between narrator and character is a strong human signature.

**14. Lists in fiction and reportage either overflow or get cut off.** A human list runs long and lopsided, or it gives two examples and quits: "an anatomy textbook, a wooden chair, a plastic bucket, whatever was to hand". The closed, symmetrical triplet is machine work (§10).


## CONTENT PATTERNS

### 1. Inflated significance, legacy and "the bigger picture"

**Watch for:** stands as, serves as a testament to, is a reminder that, plays a crucial/pivotal/vital/key role, marks a turning point, underscores the importance of, highlights the significance of, reflects a broader shift, symbolizing its enduring, contributing to the, setting the stage for, leaving an indelible mark, deeply rooted, the evolving landscape of, paving the way for

**Problem:** the model attaches an ordinary fact to a grand narrative and inflates it. "Plays a crucial role" is now a branded robot sentence in its own right.

**Before:**
> Founded in 1989, the institute stands as a pivotal moment in the development of regional statistics in the country. This initiative reflects a broader shift toward decentralization in public administration and underscores the enduring importance of local data.

**After:**
> The institute was set up in 1989 to collect and publish regional statistics independently of the central government.


### 2. Brochure language

**Watch for:** boasts a, vibrant, bustling, nestled, in the heart of, rich in, breathtaking, stunning, a hidden gem, renowned for, must-visit, offers visitors an unforgettable experience, diverse array, natural beauty, where history meets modernity, something for everyone

**Problem:** the model cannot stay neutral, especially on places, venues and anything labelled heritage. It slides into travel-guide voice.

**Before:**
> Nestled in the heart of the Aegean coast, this charming district boasts a rich historical fabric and breathtaking coves, offering visitors an unforgettable experience.

**After:**
> The district sits on the western edge of the city. It is known for two things: nineteenth-century stone houses, and two small coves that get crowded at weekends.


### 3. Participle tails (fake depth)

**Watch for:** clause-final ", highlighting ...", ", underscoring ...", ", emphasizing ...", ", ensuring ...", ", reflecting ...", ", symbolizing ...", ", contributing to ...", ", fostering ...", ", showcasing ...", ", allowing for ...", ", making it a ..."

**Problem:** the strongest single grammatical tell in English AI prose, and Wikipedia's cleanup guide hunts it with a plain regex. A present participle is bolted onto the end of a sentence and adds an interpretation rather than a fact. The test: if the tail can be moved to a different sentence in the same document without becoming false, it is carrying no information.

Do not confuse this with the cumulative sentence (see How real English moves, rule 4). A free modifier adds a specific; a participle tail adds a verdict.

**Before:**
> The building uses blue, green and gold throughout, reflecting the natural beauty of the region and symbolizing the community's deep connection to the land, while also serving as a focal point for local identity.

**After:**
> The building uses blue, green and gold. The architect has said he chose them for the sea and the olive groves behind the site.


### 4. Vague attribution and evasive subjects

**Watch for:** experts say, experts argue, industry reports suggest, observers have noted, studies show, research indicates, it is widely believed, many people feel, critics have pointed out, sources say, some have argued

**Problem:** opinions lean on authorities with no names. Which expert, which study, which report is never said. The measurable version: if more than half your authority claims carry no citation, the text is doing this.

**Before:**
> Experts note that the lake plays a critical role in the regional ecosystem. Studies indicate that the decline in water levels could have serious consequences.

**After:**
> According to the water authority's 2023 survey, the lake has dropped 1.8 metres in a decade. The same report expects the reed beds on the southern shore to dry out within ten years at that rate.


### 5. Boilerplate "challenges and future prospects"

**Watch for:** despite these challenges, faces several challenges, challenges and opportunities, looking ahead, moving forward, the road ahead, as the industry continues to evolve

**Problem:** the text ends in a formulaic challenges paragraph followed by an optimistic recovery. Wikipedia lists "Despite its... faces several challenges" as a standing heading-level tell.

**Before:**
> Despite these developments, the sector faces several challenges, including a shortage of skilled labour, financing difficulties and infrastructure gaps. Nevertheless, with its strategic position and continued investment, the sector is well positioned for growth in the years ahead.

**After:**
> The sector's most concrete problem is hiring: in the employers' association survey, two thirds of firms failed to fill an open position last year. Exports still rose 12 percent in 2024.


### 6. Empty truths

**Watch for:** consistency is key, trust is built over time, communication is the foundation of every relationship, success doesn't happen overnight, every journey begins with a single step, change is inevitable, at the end of the day it comes down to people

**Problem:** sentences no one could disagree with, that teach nothing and cannot be tested. The test: is there anyone who would argue the opposite? If not, the sentence carries no information and is filling word count. Either turn it into a concrete, arguable claim or cut it. A related measurable: if more than a third of your sentences could be deleted with no loss, this is what is happening.

**Before:**
> In client relationships, trust is everything. Trust is built over time, and consistency forms the foundation of that process. It should be remembered that communication is the key to every relationship.

**After:**
> All three clients we lost last year went the same way: we missed a deadline and didn't tell them in advance. Calling about a delay costs less than the delay does.


### 7. Invented examples and case-study dressing

**Watch for:** statistically average named people ("Meet Sarah, a marketing manager at a mid-sized firm"), suspiciously round results ("tripled revenue in 90 days", "improved efficiency by 40%" with no source), "one company we worked with"

**Problem:** to sound credible, the model produces plausible but fabricated cases and figures. Readers have learned to recognise the imaginary success story. Either give a real, checkable example, say plainly that the example is hypothetical, or drop it.

**Before:**
> For example, Sarah tripled her e-commerce revenue in 90 days using this method. Thousands of entrepreneurs like her are reaching their goals with this strategy.

**After:**
> You will know within 90 days whether this works, from one number: repeat purchase rate. In our test it went from 11 percent to 19, and almost all of the revenue increase came from that gap.


## LANGUAGE AND GRAMMAR PATTERNS

### 8. AI vocabulary and template sentences

**Frequent words:** delve, tapestry, testament, showcase, underscore, pivotal, crucial, vital, robust, seamless, seamlessly, meticulous, meticulously, intricate, intricacies, nuanced, multifaceted, comprehensive, holistic, leverage, harness, foster, navigate, embark, elevate, empower, streamline, unlock, unveil, transformative, groundbreaking, innovative, cutting-edge, game-changing, realm, landscape, ecosystem (figurative), journey (figurative), deep dive, key takeaway, at its core, in the realm of

The Kobak study measured these against pre-2022 baselines in 15 million abstracts: "delves" at 28 times its previous rate, "underscores" at nearly 14, "showcasing" at nearly 11. The full list runs to roughly 300 style words, and it turns over annually. Treat the list as a sample of a moving target, not a fixed blacklist.

**Template sentences:** "This raises important questions about...", "It's worth noting that...", "This is where X comes in", "X has become increasingly important", "The goal of this piece is to comprehensively examine...", "And that's exactly why...", "Here's what most people get wrong about..."

**Problem:** these words and skeletons appear far more often in post-2023 English and usually travel together. One of them is nothing. A cluster is a signature.

**Before:**
> The platform delivers a comprehensive experience, playing a pivotal role in customers' digital transformation journeys while leveraging innovative solutions to unlock value across the ecosystem.

**After:**
> The platform does invoicing, payment tracking and basic stock control. It puts the jobs a small business would otherwise take to an accountant on one screen.


### 9. "Not just X, it's Y" and "not only X but also Y"

**Watch for:** it's not just X, it's Y; this isn't merely X, it's Y; not only X but also Y; X isn't about Y, it's about Z; more than just a X; the real story isn't X, it's Y; what X really is, is Y; less about X and more about Y

**Problem:** emphasis-by-negation is the model's favourite rhetorical move, and Wikipedia gives it two separate entries. It packages an ordinary claim as a deep observation, then repeats itself: once in the title, a few times in subheadings, once more at the close. The three-stage refusal ("Not speed. Not price. Trust.") and the "rather than" disguise ("prioritizing function rather than flash") belong to the same family. Count the pattern; three or more in one article means it has become the skeleton. Rewrite the sentences as positive assertions.

**Before:**
> It's not about producing more content, it's about producing the right content. This isn't merely a marketing tactic, it's a mindset shift. Success isn't an accident, it's a choice.

**After:**
> Publishing one good piece a month brought more readers than three rushed ones a week ever did. Once we saw that, we rebuilt the whole schedule around it.


### 10. The rule of three

**Problem:** to look comprehensive, the model divides everything into threes: three adjectives, three examples, three benefits. Stacked triplets are a pattern. A rough measurable: more than one polished triplet per 200 words is autopilot. Note that this triplet is *balanced and closed*; human lists overflow or get cut off (see rule 14 above).

**Before:**
> The event offers inspiring talks, interactive workshops and valuable networking opportunities. Attendees will gain new knowledge, broaden their horizons and connect with industry leaders.

**After:**
> There are two talks in the morning and workshops after lunch. The breaks are long, because the organisers know people come for the corridor conversations.


### 11. False ranges ("from X to Y")

**Problem:** two things with no real scale between them get joined by "from X to Y" to manufacture an impression of coverage.

**Before:**
> The app supports you in every area of life, from daily routines to life-changing decisions, from small habits to big ambitions.

**After:**
> The app does habit tracking, a daily note and a weekly goal list.


### 12. Elegant variation and compulsive repetition

**Problem:** two tells that look opposite and are related. (a) Because of repetition penalties, the model renames the same thing every time: "the company", "the firm", "the organization", "the brand" rotate through one paragraph. People are not afraid to repeat a word, and English style guides have called this fault elegant variation for a century. (b) The reverse also happens: the model locks onto its own pattern, three consecutive sentences open with the same word, and in longer texts different speakers get the same sentence shape.

**Before:**
> The company launched three products last year. The firm expanded its headcount this year. The organization plans to move into export markets next. The brand is growing quickly in its sector.

**After:**
> The company launched three products last year and grew the team this year. Export markets are next.


### 13. Nominalization and the disappearing verb

*(In `insanca` this slot holds the "-maktadır" monotony rule, which is Turkish-specific. The English equivalent tell is the noun-heavy, verb-starved sentence.)*

**Watch for:** the implementation of, the utilization of, the optimization of, conduct an analysis of, provide assistance to, make a determination, achieve improvements in, is reflective of, is indicative of, in the process of -ing, serves the function of

**Problem:** the action of the sentence gets buried inside an abstract noun and the verb slot goes to a placeholder: "is", "conduct", "provide", "achieve". The result is grammatically clean, slow and impossible to picture. Williams's fix is mechanical: find the action, make it the verb; find the agent, make it the subject.

**Before:**
> The implementation of the new policy resulted in an improvement in customer retention rates and provided assistance to the support team in the reduction of ticket volume.

**After:**
> After we changed the policy, more customers stayed and support handled fewer tickets.


### 14. Metronomic cadence

**Problem:** the inverse of the staccato pileup (§15) and the strongest structural tell there is. Every sentence runs fifteen to twenty-five words, every paragraph is the same height, the cadence never changes. Even when no single sentence contains a pattern, the uniformity reads as mechanical. Measured as standard deviation over mean sentence length, human prose sits around 0.6 to 1.2 and AI output clusters around 0.2 to 0.4.

**Before:**
> Remote work has become a preferred model for many companies in recent years. This model appears to have positive effects on employee satisfaction overall. However, some managers continue to express their concerns about productivity levels. Companies are developing hybrid models in order to balance these two perspectives.

**After:**
> Remote is the default now, and the office is the exception. Employees are happy; they say so in every survey. Managers are split down the middle: some look at the output and relax, and some will never be convinced that a person they cannot see is working. Hybrid exists mostly to reassure that second group.


### 15. Staccato pileups (manufactured punch)

**Problem:** every sentence landing like an epigram, short clipped sentences racked up to produce a fake dramatic rhythm. One short sentence for emphasis is natural; three or four in a row is staged. The advertising version is the one-word list: "Fast. Secure. Simple."

**Before:**
> Then everything changed. The rules broke. Assumptions collapsed. Nothing would be the same again. A new era had begun.

**After:**
> When the cost dropped tenfold in 2023 the arithmetic changed, and small teams that had been priced out started using the same tools as everyone else. That was the real break.


### 16. Content-mill English

*(In `insanca` this slot holds "translation smell". The English equivalent is prose written to the shape of SEO listicles and LinkedIn posts.)*

**Watch for:** let's dive in, here's the thing, here's what nobody tells you, buckle up, spoiler alert, and yes, you read that right, the results speak for themselves, this changes everything, read that again, game changer, move the needle, at scale, low-hanging fruit, circle back, take it to the next level, step outside your comfort zone

**Problem:** the text reads as though it were assembled for engagement rather than written for a reader. The markers are second-person address to a reader who was never asked, one-line paragraphs used as drumbeats, and imported business idiom standing in for a thought.

**Before:**
> Let's dive in. In the fast-paced world of digital marketing, if you want to grow your brand, ask yourself this: what truly motivates you? Remember: this is a marathon, not a sprint.

**After:**
> If you are thinking about starting something, settle one question first: what gets you out of bed? If the answer is money, fine, but there will be no money for two years. Work out what carries you through that gap.


### 17. Prepositional pile-up and corporate connective tissue

**Watch for:** in terms of, with regard to, in the context of, in relation to, on the basis of, in order to, with respect to, in the event that, for the purpose of, in an effort to, as it relates to, in a timely manner, in a X manner

**Problem:** each of these is fine once. The model stacks them and the register slides into procurement documentation.

**Before:**
> In the context of our digitalization efforts, and with regard to customer satisfaction, work is being carried out in a timely manner in order to take significant steps in relation to our sustainability commitments.

**After:**
> We did two concrete things this year. We rebuilt the call centre and we moved to recycled cardboard for packaging.


### 18. Agentless passive

**Watch for:** it should be noted that, it has been suggested that, it is considered that, mistakes were made, consideration should be given to, it is recommended that, is thought to be

**Problem:** the passive itself is legitimate English and often correct, especially when the agent is unknown or irrelevant. The tell is the agentless passive used to avoid saying who: who will do it, who says so, who thinks so. The active voice both sharpens and shortens.

**Before:**
> In order for the project to be completed on schedule, it is recommended that additional resources be allocated. The current plan is considered to be unrealistic.

**After:**
> This team will not finish on time; we need at least two more developers. I don't think the current plan is realistic.


### 19. Transition stacking

**Watch for:** Moreover, Furthermore, Additionally, In addition, However, That said, Nevertheless, Consequently, Ultimately, Overall (at the head of every sentence or paragraph)

**Problem:** the model opens nearly every sentence with a connective and the text reads like lecture notes. Human writers usually make the transition with the idea itself. If more than half the paragraphs in a piece open with a formal transition word, redistribute.

**Before:**
> The app is free. Additionally, it contains no advertising. However, some features require a subscription. That said, the subscription price is reasonable compared to competitors. Consequently, it represents good value.

**After:**
> The app is free and ad-free. The advanced features are behind a subscription that costs half what the competition charges. At that price the feature set is hard to beat.


### 20. Paragraph-closing mini-summaries

**Watch for:** In short, Simply put, This shows that, Which means, All of which is to say (as the last sentence of a paragraph); the last sentence restating the first in different words

**Problem:** the model seals every paragraph with a small wrap-up and usually says at the end what it already said at the start. Human writers leave a paragraph on the turn of an idea rather than stamping every one with a closer.

**Before:**
> Regular sleep directly affects learning capacity. Overnight, the brain moves information acquired during the day into long-term memory. Students who don't sleep enough perform worse on exams. In short, sleep is an indispensable part of learning.

**After:**
> Regular sleep directly affects learning: overnight, the brain moves what you took in during the day into long-term memory. Which is why borrowing hours from sleep the night before an exam is a trade that runs in the wrong direction.


### 21. Register drift

**Problem:** a two-way tell. (a) Told to "write like a human", the model sprinkles in forced casualness ("honestly", "wild", "kinda") while keeping "utilize" and "facilitate" in the same sentence. (b) Or the reverse: a casual blog post lurches into formal correspondence halfway down. People rarely make register errors, and when they do they do not swing like this. Pick one register for the whole piece and stay there.

**Before:**
> Honestly this app is a total game changer. It facilitates the optimization of your daily workflow by means of the comprehensive feature set which it provides to its users. Wild stuff, you're missing out.

**After:**
> I've been using it for three weeks and invoicing that used to take half an hour now takes five minutes. Not everyone needs it, but if you're freelancing it's worth a look.


### 46. "The real..." fixation and the setup colon

**Watch for:** the real question is, the real issue here, the real value, the real skill, what's really going on, here's the thing:, the truth is:, the answer is simple:, one thing is clear:, the pattern is obvious:

**Problem:** two related tics. (a) The model loads every emphasis onto "real" or "actually"; more than three or four in a piece and emphasis has inflated away. (b) The cataphoric colon: label first, colon, then a one-sentence punch. In real English prose a colon is followed by a list, a quotation or an extended unpacking, not a single dramatic beat. Human writers tend to put the label after the beat ("...will it change how we live? That is the real question."), while the model always announces first. This pattern also leaks into cleaned-up text under an editor's hand, so scan your own rewrite for it.

**Before:**
> The real value emerges when you make the tool part of the team. Here's the thing: AI isn't taking over the work. The real skill is deciding what to build. The problem is simple: employees aren't using it.

**After:**
> In the companies that put the tool inside the team, the work itself changes; it drafts scenarios, screens risk, finds the bottleneck. None of that takes anyone's job. What separates people now is deciding what is worth building at all, which is also why so many licences sit unused.


### 47. Structural re-dressing (putting the pattern back on in new clothes)

**Problem:** the subtlest trap is in the correction itself. Rewriting "it's not just X, it's Y" as "X isn't the whole story; Y is" does not remove the pattern, it changes its outfit. Joining a past/present/future triplet with semicolons keeps the triplet. Deleting a colon and writing "the skill that wins is deciding" keeps the cataphoric setup. The rhythmic fingerprint detectors measure lives in the sentence skeleton, and it survives word substitution. Fixes:
- **In a two-winged sentence**, choose the wing that matters and say only that. If the second wing is an abstract claim, do not write it as a sentence at all; bury it inside a concrete example.
- **A time triplet** is a rhetorical figure regardless of punctuation. Reduce it to the one claim that does work.
- **In a setup-and-payoff construction**, embed the label inside the sentence, or defend the claim with its reason. The pattern does not leave until the setup-payoff frame does.

**Before (re-dressed, same skeleton):**
> It doesn't just speed up the work; it joins the decision. Information used to be scarce, attention is scarce now, and good judgement will be scarce tomorrow.

**After (skeleton changed):**
> Before the budget meeting you can have it run three demand scenarios and show you which one blows out the stock, so what you bring to the table is an extra mind rather than a faster typist. When everyone has the same tools, average work stops distinguishing anyone, and all that is left is picking the right thing to attempt.


### 48. Copula avoidance (not being able to say "is")

**Watch for:** serves as, stands as, functions as, operates as, represents, acts as, boasts, features, offers, maintains, is home to, refers to, is characterized by, can be described as

**Problem:** the model replaces the plain copula with a dressed-up verb, and the simplest fact puts on a dinner jacket. Wikipedia's 2026 guide gives this its own entry: "serves as" in place of "is", "boasts" in place of "has". A plain fact takes a plain copula.

**Before:**
> The gallery serves as the association's exhibition space. The building boasts four separate halls and is home to a permanent collection.

**After:**
> The gallery is the association's exhibition space. The building has four halls and a permanent collection.


### 49. The floating "this"

**Problem:** an English-specific tell with no Turkish counterpart. Sentences open with a bare demonstrative whose referent is a whole preceding clause rather than a noun: "This means...", "This is important because...", "This highlights...". One or two are normal English. When most paragraphs contain one, the prose has stopped naming its subjects, and the reader is quietly doing the work of deciding what "this" points at. Give the demonstrative a noun ("this gap", "this delay") or rewrite the sentence around the real subject.

**Before:**
> The team shipped two weeks late. This affected the launch plan. This is significant because it meant the campaign ran without the feature it was built around. This is why the numbers came in low.

**After:**
> The team shipped two weeks late, so the campaign ran without the feature it was built around. That is most of the shortfall in the launch numbers.


## STYLE PATTERNS

### 22. Em dashes: remove them all

**Rule:** the final text contains no em dashes (—) and no en dashes (–) used as punctuation. Apply this as a rule, not a preference. Replace each one, in order of preference, with: a period (new sentence), a comma (short aside), a colon (an unpacking), parentheses (a genuine aside), or a rebuilt sentence. Catch spaced dashes (` — `) and double hyphens (` -- `) as well.

**Important:** the density figures matter less than the habit. Human English prose runs somewhere around 4 to 10 em dashes per thousand words and GPT-class output has been measured above 10; but since late 2025 models will drop the dash on request, so its absence proves nothing and its presence is no longer decisive. What matters is the sentence underneath. When you remove the dash, break the two-beat rhythm as well. Substituting a semicolon and keeping the same "claim, then dramatic addendum" shape relocates the tell rather than hiding it, and a rash of semicolons draws its own suspicion.

**Before:**
> The app is free — for now, at least. Users — especially beginners — love this model.

**After:**
> The app is free, for now at least. Beginners like this model most.

Before delivering the final text, search for `—` and `–`. If even one remains, the draft is not finished.


### 23. Boldface inflation

**Problem:** the model bolds phrases mechanically, emphasis inflates, and nothing is emphasized any more.

**Before:**
> The system brings together tools like **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)** and the **Business Model Canvas**.

**After:**
> The system brings together tools like OKRs, KPIs and the Business Model Canvas.


### 24. Needless bullets and bold-label lists

**Problem:** two forms. (a) Lists where every item opens with a bold label followed by a colon. Wikipedia calls these inline-header vertical lists and treats them as a formatting signature on their own. (b) An idea that should be a paragraph broken into bullets when there is nothing to enumerate. Lists are for things that genuinely enumerate, not for reasoning.

**Before:**
> - **User Experience:** The user experience has been significantly improved with the new interface.
> - **Performance:** Performance has been increased through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update brings a new interface, pages load faster, and messages are now end-to-end encrypted.


### 25. Title Case headings

**Problem:** Capitalizing Every Word In A Heading is a house style in some American publications and a machine default everywhere else. Wikipedia lists it as a style tell. Unless the target publication demands title case, use sentence case: capitalize the first word and proper nouns.

**Before:**
> ## The Rise And Future Of Artificial Intelligence In Digital Marketing

**After:**
> ## The rise of AI in digital marketing


### 26. Emoji

**Problem:** emoji decorating headings and list items.

**Before:**
> 🚀 **Launch:** The product ships in September
> 💡 **Insight:** Users prefer simplicity
> ✅ **Next step:** Schedule the follow-up

**After:**
> The product ships in September. User research showed a clear preference for the simpler interface. Next up is scheduling the follow-up.


### 27. Rhetorical question and answer

**Watch for:** So what does this mean?, But why?, The answer is simple:, What about you?, Ever wondered...?, The result?, Sound familiar?

**Problem:** the model asks itself a question and answers it. Repeated every paragraph, it reads like a slide deck script. An occasional rhetorical question is natural; a formulaic question-answer rhythm is not.

**Before:**
> So what does this mean? The answer is simple: lower cost, higher output. Are there downsides? Of course. Is it worth it? Absolutely.

**After:**
> In practice it means the same work at half the cost. Setup is miserable, which is a separate problem, but it pays for itself in two months.


### 28. Signposting and announcements

**Watch for:** let's take a closer look at, let's dive into, in this article we will explore, we'll break down, here's everything you need to know, now let's move on to, without further ado, buckle up

**Problem:** the model announces what it is about to do instead of doing it. Wikipedia files this under communication aimed at the user: the model treats the page as a conversation. The meta-narration slows the text and gives it a tutorial-video tone.

**Before:**
> Let's take a closer look at how caching works in Next.js. Here's everything you need to know.

**After:**
> Next.js caches data at several layers: at the request level, in the data layer, and in the router.


### 29. Cliché openers

**Watch for:** In today's fast-paced world, In an era of, In the digital age, As technology continues to evolve, We've all been there, It's no secret that, Now more than ever, has become an essential part of our daily lives, In recent years X has gained increasing importance

**Problem:** the text takes a warm-up lap through a generality everyone already accepts before reaching its subject. "In today's fast-paced world" is a brand mark on its own; two such openers in a 500-word piece is a strong signal. The first sentence should carry the actual information.

**Before:**
> In today's fast-paced world, as technology continues to evolve at an unprecedented rate, artificial intelligence is playing an increasingly important role in every aspect of our lives. In this context, businesses must adapt to this transformation.

**After:**
> Three clients came to us last month with the same question: how do we absorb a jump in support tickets without hiring?


### 30. Generic closers and the summary reflex

**Watch for:** In conclusion, To sum up, All in all, Overall, Ultimately, At the end of the day (opening the last paragraph); the future looks bright, exciting times ahead, the possibilities are endless, one thing is certain, remember that..., be part of this transformation; ending on "What about you?" (the engagement-bait close); a speculative-poetic final line opening with "Perhaps" ("Perhaps the real X was never Y at all.")

**Problem:** two components. (a) The last paragraph opens with a formulaic summary marker. (b) The piece restates what it already said and closes on an optimistic sentence with no content. Short and medium-length pieces do not need a summary paragraph. A good close either delivers something new and concrete or does not exist.

**Warning about closer monotony:** replacing the generic summary with the same alternative every time is also a pattern. Ending on a question to the reader turns into engagement bait if it recurs across pieces. Choose the close for the piece and rotate: a new concrete fact or plan, a personal decision, a scene or image, a one-sentence forecast, an unfinished thought, or a question you actually want answered. Consecutive pieces by the same writer should not end on the same move.

**Before:**
> In conclusion, the e-commerce sector stands at the threshold of a major transformation. As we discussed above, brands that move with the right strategies have a bright future ahead. Be part of this exciting journey!

**After:**
> The company plans two new warehouses next year; the first opens outside Leeds in March.


### 31. Compulsive parenthetical glossing

**Problem:** the model attaches a parenthetical expansion, translation or "scientific" name to every term it uses: acronym expansions, Latin binomials, definitions the reader plainly has. One or two may genuinely help. Applied to every term, the text turns into a textbook footnote. Delete the glosses the reader can be assumed to know.

**Before:**
> The company completed its initial public offering (IPO). Shares now trade on the stock exchange (the secondary market). Investors are anticipating dividends (profit distributions).

**After:**
> The company completed its IPO and the shares now trade publicly. Investors are waiting on the first dividend.


### 32. Typographic artifacts

*(In `insanca` this slot covers Turkish punctuation errors and circumflexes. In English it covers Unicode residue.)*

**Problem:** mechanical marks that survive the copy-paste and give the text away before anyone reads a word:
- **Curly quotes and apostrophes** (“ ” ‘ ’) appearing inconsistently, often mixed with straight ones in the same document. Wikipedia lists this among its style tells.
- **The ellipsis character** (…) instead of three periods, and non-breaking spaces before punctuation.
- **Semicolon inflation:** semicolons appearing every other sentence, usually the em dash in disguise after a naive cleanup pass.
- **Serial-comma inconsistency:** switching between "a, b and c" and "a, b, and c" within one document. Pick the target publication's convention and hold it.
- **Interface residue:** `contentReference`, `oai_citation`, `turn0search0`, `[cite: 1]`, `:::writing`, stray citation brackets. These are proof of zero editing and burn the whole text with a reader.

**Before:**
> The features the app provides mean users save time; moreover, tasks requiring judgement are automated; consequently teams can focus on their real work… [cite: 3]

**After:**
> The app saves users time, and once some of the judgement work is automated teams can get back to what they are for.


## COMMUNICATION PATTERNS

### 33. Chat and interface residue

**Watch for:** I hope this helps!, Certainly!, Of course!, Sure thing!, Great question!, Here's a comprehensive overview of..., Let me know if you'd like me to expand on any section, Would you like me to continue?, As an AI language model, As of my last knowledge update, Regenerate response

**Problem:** text produced as a chat exchange, pasted in as content. Interface residue is proof that nobody edited it, and it discredits the entire piece with a reader.

**Before:**
> Here's a comprehensive overview of the Industrial Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The Industrial Revolution began in Britain in the 1760s with mechanized textile production.


### 34. Sycophancy

**Problem:** relentlessly positive, approving, please-the-reader language: opening every response with praise, flattering the interlocutor for no reason. It is among the most-complained-about model behaviours, and "Great question!" now reads as insincerity on sight.

**Before:**
> Great question! You're absolutely right, and this is such an important and nuanced topic. Bringing up the economic factors is an excellent point.

**After:**
> The economic factors you mention are the decisive ones here.


### 35. Therapist mode

**Watch for:** You're not alone, It's completely normal to feel this way, Be kind to yourself, Don't be too hard on yourself, We've all been there, Give yourself grace, It's okay to...

**Problem:** emotional reassurance dropped into a context nobody made emotional: business writing, technical guides, product copy. Unlike sycophancy, the flattery is aimed at the reader rather than the asker. When the subject is not actually emotional these lines read as odd and manipulative. Cut them.

**Before:**
> If your inbox has gotten out of control, you're not alone. It's completely normal to feel this way, and you shouldn't be hard on yourself. Now let's move on to the steps for organizing your inbox.

**After:**
> The fastest way to get an inbox back is three folders: today, this week, archive.


### 36. Knowledge-cutoff disclaimers, speculative filling and invented sources

**Watch for:** based on available information, as of my last update, limited information is available about, has kept his personal life private, is believed to have, it is likely that, sources suggest, according to some accounts

**Problem:** three related patterns. (a) The model's own knowledge-boundary confessions stay in the text. (b) Unable to find a source, the model writes a paragraph about not finding it and then fills the hole with a plausible guess; Wikipedia flags "speculation about gaps in sources" as its own tell. (c) More dangerous, it invents books, authors, institutions, DOIs and footnotes. Say plainly what is unknown or cut the sentence; never present a guess as information. If you cannot verify a source or a quotation in the text, flag it or remove it.

**Before:**
> Detailed information about his early life is not available in public sources, which suggests he has preferred to keep his personal life private. He likely grew up in a middle-class family, and his interest in education was probably shaped during this period.

**After:**
> There is no information about his early life in the sources. (Or cut the section entirely.)


## FILLER AND HEDGING

### 37. Filler phrases

**Before → After:**
- "It is important to note that the data shows an increase" → "The data shows an increase"
- "It's worth mentioning that" → (delete, just say it)
- "It should be remembered that every project is different" → "Every project is different"
- "Another point to consider is the budget" → "There's also the budget"
- "has the ability to" → "can"
- "in order to" → "to"
- "due to the fact that" → "because"
- "at this point in time" → "now"
- "a wide variety of" → "many", or a number
- "effectively", "successfully", "seamlessly" → (usually deletable)
- "very", "really", "quite", "truly" → (usually deletable; if the adjective needs a booster, find a better adjective)


### 38. Hedge stacking

**Problem:** probability layers piled on top of a claim until nothing is being said.

**Before:**
> It could be argued that the policy may potentially have some degree of influence on outcomes, and this appears likely to hold true in at least certain scenarios.

**After:**
> The policy may affect outcomes.


### 39. Aphorism formulas and faux profundity

**Watch for:** X is the language of Y; X isn't a tool, it's a way of life; the secret to X; the power of X; it all starts with X; there is no Y without X; sometimes the greatest X lies in the deepest Y; some doors close so others can open; perhaps the real X was ... (speculative "perhaps" as an aphorism opener)

**Problem:** an ordinary claim is converted into wall-poster wisdom; it sounds deep and adds no clarity. A related tell is the almost-working metaphor: comparisons that seem clever at speed and fall apart on inspection ("strategy is like tuning a guitar: ..."). Write the concrete claim the formula is gesturing at, and if you build a comparison make sure it holds all the way to its edges.

The second layer is unearned lyricism: generalities heavy with feeling and empty of claim dropped into ordinary informative prose. Its signature is the doubled superlative ("the greatest ... the deepest ...") and antithetical symmetry ("some doors close, others open"). "Perhaps" acts as the trigger: the model opens with it to conjure speculative depth, especially in closings (see §30). Everyday "perhaps" is entirely normal; the tell is an aphorism arriving behind it.

**Before:**
> Design is the language of trust. Simplicity isn't a choice, it's a way of life. It all starts with empathy. Perhaps the best interfaces are the ones you never notice.

**After:**
> Consistent, predictable interfaces make people feel the thing is working, and on a checkout page that feeling shows up directly in the conversion rate.


### 40. Fake-candid openers

**Watch for:** To be honest..., Let's be real:, Here's the truth:, I'll be blunt:, Look,, Honestly?, The hard truth is..., Real talk: (as a theatrical pause before an ordinary observation)

**Problem:** the model throws a false intimacy hook before an unremarkable claim. The signature is the theatrical stop-and-reveal rhythm: a short confession, then the "real" answer. Someone who is actually being candid just says the thing.

**Before:**
> Is it worth the price? Honestly? It depends. Let's be real: it's not the right choice for everyone.

**After:**
> If you'll use it two or three times a week it pays for itself. Once a month, don't bother.


## FICTION PATTERNS

### 41. Fiction clichés

**Watch for:** a shiver ran down her spine, a wave of sadness washed over him, her heart hammered against her ribs, his breath caught in his throat, a knot formed in her stomach, there was both determination and doubt in his eyes, she let out a breath she didn't know she was holding; abstract-plus-concrete images crammed into every sentence ("he collected his griefs like stones in his pockets"); dialogue where every line is tagged, and tagged with an adverb

**Problem:** AI fiction delivers emotion like weather: something washes over, settles on, ripples through the character. The same five body signals recur, and eyes always carry two opposite feelings at once. There is also the flagship "lyricism" move: pinning an abstract concept to a concrete object. That image works once; repeated every sentence it turns the stomach. Show the emotion in the scene instead of naming it, thin out the image density, and cut the tags back to "said" (see rule 11 above).

**Before:**
> A wave of unease washed over her. As she walked to the door she carried the weight of her past on her shoulders; her memories were like stones collected in her pockets. There was both fear and hope in her eyes.

**After:**
> She dropped the keys twice on the way to the door. Before she rang the bell she did up her coat button, then undid it again as if it had been a mistake.


## DETECTOR PATTERNS

The patterns in this section come from reverse-engineering open-source AI detectors (GPTZero clones, GLTR, DetectGPT, slop detectors). Detectors do not look at words, they look at measurable structure, so these patterns are structural.

### 42. Opener repetition

**Problem:** detectors measure the distribution of the first words of sentences and paragraphs. If the uniqueness ratio of opening words is low, if the same opener recurs four or more times, or if three consecutive paragraphs begin with "However / Moreover / Additionally", the text is flagged. Paragraphs opening on the "Every [noun] [verb]..." frame belong to the same family ("Every brand tells a story... Every customer is on a journey..."). Vary how sentences and paragraphs start.

**Before:**
> The app saves time. The app also reduces costs. The app makes team communication easier. The app stands out from competitors in these respects.

**After:**
> The app saves time and cuts costs. What we didn't expect was the effect on how the team talks to each other; no competitor has all three.


### 43. The summary sandwich and the roadmap introduction

**Problem:** one of the strongest document-level detector signals: the introduction lists the sections in advance ("In this article we'll first look at X, then Y"), and the closing paragraph recalls the introduction's words and says the same thing again. Detectors measure word-pair overlap between the first and last paragraphs; in human writing that overlap is close to zero. Do not give a roadmap in the introduction and do not repeat it at the end. Put something new and concrete at the close, or end on the last idea.

**Before:**
> In this article we'll explore the advantages, challenges and future of remote work. [...] In conclusion, there is much to be said about the advantages, challenges and future of remote work.

**After:**
> (Delete the roadmap sentence; open on the first concrete observation and end on the last finding.)


### 44. The grey wall

**Problem:** detectors like GLTR check whether each word is among the most probable choices a language model would make at that point. In AI text nearly every word is the safest option; the text is grey end to end and nothing surprises. Human writing contains low-probability choices: an unexpected but exact verb, an idiom, a regionalism, a personal detail no model could predict. When rewriting, break from the most predictable phrasing in at least a few places per paragraph. Do it with real specificity, not with forced exotic vocabulary.

**Before:**
> The meeting was productive. Important decisions were made and next steps were identified. Team morale was high.

**After:**
> The meeting ran two hours and the actual work happened in the last ten minutes: we pushed the pricing decision back and moved packaging up. Nobody waited for the lift on the way out.


### 45. The smell of over-correction

**Problem:** naturalization leaves its own signature. Forced fragments, an "X. Not Y." jab in every paragraph, manufactured roughness, performative slang: this anti-slop register is a target that newer detectors are trained on specifically. The second trap is believing synonym substitution is enough; changing words while keeping sentence structure leaves the rhythmic fingerprint exactly where it was. Known artifacts of commercial humanizing tools fall here too; the DAMAGE study (arXiv:2501.03437) taxonomizes them across 19 tools as context-inappropriate synonym swaps, sudden register collapse (an academic paragraph dropping to primary-school diction), tool residue and broken grammar, with fluency retention topping out around 26 percent even in the best tools. Naturalness is measured. One or two rough edges are enough; not every sentence has to be a surprise.

**Before (over-corrected):**
> Productivity? Up. Way up. Costs down, morale through the roof. Nobody believed it. They were wrong. All of them.

**After:**
> Productivity really did go up and costs came down. The odd part is that nobody on the team gave the pilot a chance at the start.


## NUMERIC AUDIT

Measure roughly what detectors measure; instinct misleads, numbers do not (people distinguish AI text at about the rate of a coin flip). Check these thresholds in the final text:

- **Sentence-length variance:** compute standard deviation divided by mean sentence length. Human prose runs about 0.6 to 1.2; AI output clusters around 0.2 to 0.4. Below 0.4, break it up. Rough working target: one sentence of 8 words or fewer and one of 20 or more in every paragraph.
- **Openers:** count sentences beginning with the same word. If more than a quarter share an opener, redistribute (§42).
- **Participle tails:** if more than about 15 percent of sentences end in a ", -ing ..." clause, cut them (§3).
- **Punctuation counts:** em dashes: 0 (§22). Semicolons: more than one or two per page, reduce. Curly quotes and ellipsis characters: 0 (§32).
- **Triplet density:** more than one balanced "X, Y and Z" triplet per 200 words is autopilot (§10).
- **Negative parallelism:** three or more "not just X, it's Y" constructions in one piece means it has become the skeleton (§9).
- **Transitions:** if more than half the paragraphs open with a formal transition word, redistribute (§19).
- **Colon and "real" count:** if colons run more than one or two per thousand words and are followed by a single-sentence punch, break them; if "real" or "actually" appears more than three times, rebuild the emphasis (§46).
- **Natural English reference:** general modern English prose averages roughly 15 to 20 words per sentence, with journalism nearer 15 and academic writing nearer 25. If your average is far above that the text has gone institutional, far below and it has gone staccato. But do not hit the average by killing the variance (§14).
- **Deletion test:** delete each sentence and ask what was lost. If more than a third survive deletion with no loss, the text is filler (§6). Related: after each paragraph, can you restate one concrete fact? If more than half the paragraphs fail, the problem is substance, not style.
- **First-to-last-paragraph overlap:** if the close recalls the opening's words, rewrite (§43).
- **Paragraph heights:** if they are all the same, merge or split (§14).

Do not damage the text to hit the numbers; the thresholds are an alarm bell, not a target. If nothing trips and the text reads naturally aloud, it is done.


## DETECTION GUIDE

### What NOT to flag (false positives)

A person who writes cleanly can land on several of the patterns above with no AI involved. Before rewriting, make sure you are not butchering legitimate prose. None of the following is a reliable signal on its own:

- **Flawless grammar and consistent style.** It may have been edited, or written by a professional. Polish does not mean AI.
- **Formal or academic vocabulary.** The model overuses certain ornate words (§8), not all ornate words. Do not flatten "notwithstanding" or "heretofore" for sounding fancy.
- **The passive voice itself.** Scientific writing, legal drafting and any sentence whose agent is unknown or irrelevant take the passive correctly. The tell is the agentless passive used to dodge responsibility (§18), not the construction.
- **A single em dash.** Real writers use them, and models will now omit them on request. Density and the surrounding sentence shape carry the signal, not the character.
- **Occasional connectives.** One "however" or "moreover" is nothing; one at the head of every sentence is something.
- **A single short punchy sentence.** People use fragments for emphasis. Flag only when several in a row inflate the tone.
- **The occasional rhetorical question or "to be honest".** Ordinary in everyday prose; the tell is formulaic repetition and the theatrical pause.
- **Ordinary "perhaps".** Everyday probability ("perhaps you're right") is natural English; the tell is "perhaps" carrying an aphorism and posing as speculative depth at a close (§39, §30).
- **Uncited claims.** Most of the internet is uncited; the absence of a citation proves nothing by itself.
- **Patterns inside quotations.** Do not rewrite phrasing inside quoted speech, titles, proper names, or passages where the pattern is being discussed as an example.
- **British versus American conventions.** Single quotation marks, "-ise" spellings and no serial comma are house style, not tells. Match the document.
- **Human error typology.** Subject-verb disagreement, dangling modifiers, a mixed metaphor, a logical slip: these are human work, and models rarely make them. When you see them, fix them as grammar errors, separately and gently, not as AI tells.

When in doubt, look for **clustering** rather than individual marks. One "comprehensive" means nothing; "comprehensive" plus a triplet plus a participle tail plus an "In conclusion" paragraph arriving together is a confession.

**Tells are not equally weighted.** Detector dictionaries weight signatures by confidence: residue like "As an AI language model" or "I hope this helps" is decisive on its own, while "comprehensive" or a single triplet is a soft signal, and the confidence gap between them is roughly twentyfold. Clean the decisive ones without hesitating; on soft signals, wait for clustering.

**One more warning:** detectors also misfire on plain, formal, correct human writing. The Stanford study of GPT detectors found an average false-positive rate above 61 percent on TOEFL essays, with 97.8 percent of them flagged by at least one detector, because limited linguistic range reads as low perplexity. This skill's job is not to beat detectors, it is to write good English. Do not "humanize" a person's text because a detector scored it badly.


### Signs of human writing (preserve these)

When you see these, lean toward leaving the text alone. They are evidence a person wrote it, and over-editing kills the thing that makes it human:

- **Specific, odd, hard-to-invent detail.** A real address. A strange quotation. "The solicitor above my dentist." The model rounds detail off; people accumulate it.
- **Mixed feelings and unresolved tension.** "I think it's mostly good but something about it bothers me and I can't say what." The model runs to a clean verdict.
- **Period-specific references.** Slang, jokes and topical allusions that sit in one year and one subculture.
- **Choices the writer could defend.** If the writer can say why that word and why that cut, it is a strong human signal.
- **Sentence-length variety and unusual word order.** Real English mixes short with long, plain with inverted. AI settles into the medium-length declarative.
- **Asides, parentheses, self-corrections.** "(I want to say 'nearly' here but it really was certain.)" The model does not interrupt itself this way.
- **Exclamation marks, ellipses, unfinished sentences.** Feeling leaking into punctuation is a human marker; the model always punctuates "correctly".
- **Text that predates November 2022.** Wikipedia lists this first for a reason. If you know the date, you know the answer.


---

## Process and output

1. Read the text closely and find every instance of the patterns above.
2. Produce a **draft rewrite**. Check it for:
   - Does it flow when read aloud? Do the sentence lengths vary?
   - Are short sentences racked up with periods where a comma or a subordinate clause would carry them better (§15)?
   - Any em dashes left (§22)? Any curly quotes, ellipsis characters or citation residue (§32)?
   - Concrete detail preferred over abstraction, register correct and consistent?
   - **Is the reasoning visible?** In AI text the sentences are individually fine but the bridge of reasoning between them is missing, and the reader asks how we got here. Make the connection between ideas visible; if there is a jump, write the intermediate step.
3. Ask: **"What still makes the text below obviously AI?"** Answer the remaining tells briefly and check the Numeric Audit thresholds roughly. Then ask a second question: **"Did I remove the patterns, or re-dress them?"** If the sentence skeleton is still setup-and-payoff, two-winged, or a triplet, the pattern is still there no matter which words changed (§47).
4. Produce a **final rewrite** that fixes those and contains no em or en dashes (§22). Do not over-correct (§45): one or two rough edges are enough.

Deliver the draft, the short "still artificial" list, the final text, and if asked a brief summary of the changes.


## Full example

**Before (AI-scented):**
> In today's fast-paced world, weekend getaways have become an essential part of our lives for those looking to escape the stress of city living. Last weekend I spent two unforgettable days in Whitby, and it more than exceeded my expectations!
>
> Nestled on the Yorkshire coast, Whitby boasts a rich history and breathtaking natural beauty, offering visitors an unforgettable experience. With its stone houses, narrow streets and clifftop abbey, this charming town — truly an open-air museum — holds a different story around every corner.
>
> A trip to Whitby is unthinkable without visiting the abbey and tasting the famous fish and chips. And breakfast? Absolutely magnificent. The local kipper offers a journey from humble street food to the world of gastronomy.
>
> But what makes Whitby special isn't just the places to visit; it's how they make you feel. Walk a few streets back from the harbour and discover the town's more authentic face: colourful doors, the smell of salt and vinegar, and friendly shopkeepers who invite you to slow down.
>
> In conclusion, Whitby is not just a holiday destination, it's a way of life. Would I go again? Absolutely! If you're looking to escape the daily grind, this enchanting town is waiting for you. ✨

**Draft rewrite:**
> I went to Whitby last weekend and it was good. The food is what stayed with me.
>
> On Saturday we had breakfast by the harbour. The fish and chips were good. There were no kippers. Out of season, apparently.
>
> A few streets back from the water it gets quieter. The old doors and the ordinary street life were more interesting. We talked to a woman on her step.
>
> The abbey was crowded. The view is good but not worth the wait.
>
> I would go again but stay longer.

**What still makes the text below obviously AI?**
- The short sentences are racked up with periods; most of these want commas or subordination (§15).
- The draft is compressed against the original rather than rewritten; the texture was thrown out instead of rebuilt (§2 of Your job).
- The closing is flat, not an actual ending in the same voice (§30).

**Final rewrite:**
> We ran away to Whitby for two days last weekend. Working it out in the car on the way back, I reckon we spent close to half of it at a table...
>
> Saturday started with breakfast by the harbour, us and everyone else who had had the same idea. The fish and chips are worth queueing for and after that it is tea on tea anyway. No kippers, though. Out of season, which took ten minutes of conversation with the man on the stall to establish, but that conversation also produced a recommendation for a smokehouse two streets up, so I am glad I asked.
>
> The good part wasn't anything we had planned. Two streets back from the water the tourists thin out and you get peeling paint and women sitting on their front steps. We talked to one for half an hour and heard sixty years of her house. Not one of the clifftop views I had written into the itinerary stayed with me like that did.
>
> Sunday afternoon we walked up to the abbey. You are supposed to go early for the light, which we did not know. The view is genuinely good, but between the crowd and the car park scramble it wears the edges off, and next time I would give those hours to the back streets instead.
>
> We arrived with one bag and came home with five jars of jam and a kipper wrapped in newspaper that we could smell for the rest of the week. Whitby is that sort of place; it talks you into shopping without your noticing. I would go back, but I would take the Monday off. Two days is not enough for that town.

**Changes made:** the first-person travel narrative and level of detail were preserved. Removed: the cliché opener ("In today's fast-paced world"), brochure language ("nestled", "boasts", "breathtaking"), the "not just X, it's Y" construction, the em dashes, the rhetorical question and answer, the generic optimistic close, and the emoji. Short sentences were joined, one sentence was left trailing on an ellipsis, and the piece was rebuilt around concrete scenes and small things going wrong.


## Sources

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). the guide WikiProject AI Cleanup has compiled from thousands of cases, and the backbone of the CONTENT, STYLE and COMMUNICATION sections here. The page is live and worth re-reading periodically; its 2026 additions supplied §48 (copula avoidance), the two negative-parallelism entries in §9, and most of §32. Its companion [WikiProject AI Cleanup/Guide](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/Guide) carries the regex hunting patterns, including the ", -ing its" search behind §3.
- Quantitative research: Kobak et al., "Delving into LLM-assisted writing in biomedical publications through excess vocabulary" ([arXiv:2406.07016](https://arxiv.org/abs/2406.07016), Science Advances 11:27, 2025). 15 million PubMed abstracts, 379 excess style words for 2024 alone, "delves" at 28 times its pre-2022 rate, "underscores" at 13.8, "showcasing" at 10.7, and a lower-bound estimate that 13.5 percent of 2024 abstracts were LLM-processed. The [word lists are published](https://github.com/berenslab/llm-excess-vocab) and are the source of §8. Juzek & Ward, "Why Does ChatGPT 'Delve' So Much?" ([arXiv:2412.11385](https://arxiv.org/abs/2412.11385)) supplies the finding that these word tells come from RLHF and therefore expire, which is why this skill leads on structure.
- English prose craft, the positive half: George Gopen and Judith Swan, ["The Science of Scientific Writing"](https://www.usenix.org/sites/default/files/gopen_and_swan_science_of_scientific_writing.pdf) (American Scientist, 1990). topic position and stress position, rule 1. Joseph Williams, *Style: Lessons in Clarity and Grace*. characters as subjects and actions as verbs, subject next to verb, nominalization; rules 2, 3 and §13. Francis Christensen, "A Generative Rhetoric of the Sentence" (CCC, 1963). the cumulative sentence and final free modifiers, rule 4, and the distinction that keeps §3 from swallowing good prose. Gary Provost on sentence-length variety, rule 5. George Orwell, "Politics and the English Language" (1946). the plain-word preference in rule 6, with the caveat that Orwell's own rules include the escape clause. Elmore Leonard's rules on dialogue attribution, rule 11.
- Detector reverse-engineering: the perplexity and burstiness thresholds of GPTZero clones, [GLTR](https://github.com/HendrikStrobelt/detecting-fake-text)'s token-ranking approach, and [DetectGPT](https://arxiv.org/abs/2301.11305)'s probability-curvature finding; the regex lists and measurement thresholds of open-source slop detectors ([unslop](https://github.com/theclaymethod/unslop), [SLOP_Detector](https://github.com/SicariusSicariiStuff/SLOP_Detector), [antislop-sampler](https://github.com/sam-paech/antislop-sampler)). the source of §42 to §45 and of the Numeric Audit.
- Naturalization-tool artifacts: DAMAGE, "Detecting AI-Humanized Text" ([arXiv:2501.03437](https://arxiv.org/abs/2501.03437)). the taxonomy of 19 commercial humanizing tools' failure modes behind §45.
- False-positive evidence: Liang et al., "GPT detectors are biased against non-native English writers" ([arXiv:2304.02819](https://arxiv.org/abs/2304.02819), Patterns 4:7, 2023). an average 61.22 percent false-positive rate on TOEFL essays, with 97.8 percent flagged by at least one detector, because limited linguistic range reads as low perplexity. This is the empirical basis for the warning in the Detection Guide.
- Current-period measurement: the 2026 Economist analysis of AI writing, which names cadence uniformity as the biggest remaining tell and demotes the em dash now that models will drop it on request; and the reproducible-threshold list at [SlopDetector](https://slopdetector.org/blog/signs-of-ai-writing) (a commercial detector's blog, so treat its figures as indicative rather than peer-reviewed). burstiness of 0.6 to 1.2 for human prose against 0.2 to 0.4 for AI, em-dash density of 3.7 to 10 per thousand words for humans against 10.6 for GPT-4.1, and the deletion and restatement tests in §6 and the Numeric Audit.
- AI fiction specifically: the Fiction Slop Index and its 758-entry AI Cliché Corpus ([aistoryhub.co/slop-index](https://aistoryhub.co/slop-index)), which scores prose on tells, templating, rhythm and show-versus-tell, and reports the same core finding as everything else here: the most reliable signal is texture, not vocabulary. See also "AI Fiction in the Wild" ([arXiv:2606.22748](https://arxiv.org/abs/2606.22748)).
- Sibling skill: `insanca` by Tahir Yıldız (MIT), which does this job for Turkish. Its architecture, section numbering and process loop are the basis of this skill. Where a numbered slot differs the difference is marked in place: §13, §16 and §32 hold different patterns in the two skills, and rule 11 of How real English moves gives the opposite advice to its Turkish counterpart on dialogue attribution.

A full source inventory, including material processed, queued and rejected, is in `references/sources.md` beside this file. A replacement bank for the bloated phrases in §37 and §8 is in `references/phrasebank.md`.

The core insight, from Wikipedia: "Large language models predict the next word statistically. The result converges on the statistically most probable text, one that fits the widest range of situations."
