# Source map

The inventory behind `humanly`, and the queue in front of it. States: **processed** (a rule or pattern in the skill derives from it) · **queued** (high priority, to be mined) · **worth a look** (medium or low priority) · **unavailable**.

## 1. AI writing patterns

| Source | State | Contribution |
|---|---|---|
| [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | **processed** + **queued** | The backbone. Content, style and communication sections; §48 copula avoidance, §9 both negative-parallelism entries, §32 typographic tells, §25 title case, §24 inline-header lists. The page is live and should be re-read each quarter. |
| [WikiProject AI Cleanup/Guide](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/Guide) | **queued** | Regex hunting patterns, including the ", -ing its" search behind §3. Worth mining in full for a grep-able companion script. |
| [Kobak et al., excess vocabulary (arXiv:2406.07016)](https://arxiv.org/abs/2406.07016) | **processed** | §8. 15M abstracts, 379 excess style words for 2024, ratios for delves/underscores/showcasing. [Word lists on GitHub](https://github.com/berenslab/llm-excess-vocab) are the authoritative version and turn over annually. |
| [Juzek & Ward (arXiv:2412.11385)](https://arxiv.org/abs/2412.11385) | **processed** | The finding that word tells originate in RLHF and therefore expire. The reason this skill leads on structure. |
| [DAMAGE (arXiv:2501.03437)](https://arxiv.org/abs/2501.03437) | **processed** | §45. Failure taxonomy of 19 commercial humanizing tools; the 26 percent fluency-retention ceiling. |
| [Liang et al., detector bias (arXiv:2304.02819)](https://arxiv.org/abs/2304.02819) | **processed** | The false-positive warning in the Detection Guide. 61.22 percent FPR on TOEFL essays. |
| [SlopDetector: 12 patterns with thresholds](https://slopdetector.org/blog/signs-of-ai-writing) | **processed** | Numeric Audit thresholds. Commercial source; figures are indicative, not peer-reviewed, and should be re-derived if they ever carry weight in a decision. |
| The Economist 2026 AI-writing analysis | **processed** (secondhand) | Cadence uniformity as the leading 2026 tell; the em dash demoted. Read via press summaries; the original is paywalled and should be read directly when accessible. |
| [Fiction Slop Index / AI Cliché Corpus](https://aistoryhub.co/slop-index) | **processed** (partial) | §41 and narrative rules 11 to 14. The 758-entry corpus itself was not retrieved; the four scoring axes were. Mining the corpus is the single highest-value item in this queue. |
| ["AI Fiction in the Wild" (arXiv:2606.22748)](https://arxiv.org/abs/2606.22748) | **queued** | Field study of AI fiction; likely source of further §41 material. |
| [tropes.fyi](https://tropes.fyi/) | **queued** | Phrase-frequency tracking across models; useful for keeping §8 current. |
| [EQ-Bench Slop Score](https://eqbench.com/slop-score.html) | **queued** | Per-model slop profiles. The only data source for a possible "which model produced this" feature. |
| unslop, SLOP_Detector, antislop-sampler, GLTR, DetectGPT | **processed** | §42 to §45 and the Numeric Audit. |
| [stop-slop](https://github.com/hardikpandya/stop-slop), [skill-deslop](https://github.com/stephenturner/skill-deslop) | worth a look | Scoring-rubric ideas; academic-context exemptions. |
| [Scientific American on model style differences](https://www.scientificamerican.com/article/chatgpt-and-gemini-ai-have-uniquely-different-writing-styles/) | worth a look | Peer-reviewed evidence that ChatGPT skews formal and Gemini conversational. |
| [Adversarial Paraphrasing (arXiv:2506.07001)](https://arxiv.org/abs/2506.07001) | worth a look | Academic grounding for "move the text into the human distribution" rather than "delete the patterns". |

## 2. English prose craft (the positive half)

| Source | State | Contribution |
|---|---|---|
| [Gopen & Swan, "The Science of Scientific Writing"](https://www.usenix.org/sites/default/files/gopen_and_swan_science_of_scientific_writing.pdf) | **processed** | Rule 1: topic position and stress position, old information first and new last. The most load-bearing rule in the section. |
| Joseph Williams, *Style: Lessons in Clarity and Grace* | **processed** | Rules 2 and 3, and §13. Characters as subjects, actions as verbs, subject near verb, nominalization diagnosis. |
| Francis Christensen, "A Generative Rhetoric of the Sentence" (CCC, 1963) | **processed** | Rule 4: the cumulative sentence and final free modifiers. Also the line that stops §3 from eating good prose. |
| Gary Provost, on sentence-length variety | **processed** | Rule 5. |
| Orwell, "Politics and the English Language" (1946) | **processed** | Rule 6, with its own escape clause attached. |
| Elmore Leonard, rules of writing | **processed** | Rule 11: "said" is invisible; no said-bookisms, no adverb tags. |
| Ursula Le Guin, *Steering the Craft* | **queued** | Sentence rhythm and paragraph-level movement; likely to sharpen rules 5 and 10. |
| Verlyn Klinkenborg, *Several Short Sentences About Writing* | **queued** | The counter-case to rule 4; useful tension to hold rather than resolve. |
| Fowler, *Modern English Usage* ("elegant variation") | **processed** | §12 and rule 9. The fault was named a century before models existed. |
| Garner, *Modern English Usage* | worth a look | Adjudication on contested usage; the reference for §32 house-style questions. |
| Chicago Manual of Style / New Hart's Rules | worth a look | Serial comma, quotation and dash conventions; needed if this skill grows publication-specific profiles. |

## 3. Human-prose corpora (pre-2022 reference)

Anything written before November 2022 is uncontaminated by definition, which makes date the cheapest filter available.

| Source | State | Contribution |
|---|---|---|
| [Project Gutenberg](https://www.gutenberg.org) | worth a look | Public-domain prose; heavy period skew, so useful for narrative rhythm and useless for register. |
| [COCA](https://www.english-corpora.org/coca/) / [BNC](http://www.natcorp.ox.ac.uk) | worth a look | Frequency baselines for any claim about what English "usually" does. Registration required. |
| Pre-2022 long-form journalism and essay archives | **queued** | The closest English equivalent to the Turkish skill's columnist corpus. The positive section here leans on craft manuals instead, which is a real gap: no rule in "How real English moves" was derived from close reading of a named corpus. Closing that gap is the biggest single improvement available to this skill. |

Note on the gap above: `insanca` derives its positive section from reading actual Turkish prose (columnists 2012-2019, Gürpınar, a modern novel, a translated classic). `humanly` derives its positive section from named craft authorities instead. Authorities are checkable and corpora are evidence, and the two are not the same thing. Until a corpus pass is done, treat the craft rules as well-sourced convention rather than as measured fact.

## 4. Deliberately excluded

- **Detector-evasion tooling.** The skill's stated job is good English, not a low detector score, and the Liang study is the reason: optimizing for detector output punishes exactly the writers detectors already misjudge.
- **Translation corpora (OPUS, Tatoeba) as style references.** They carry translationese, which is the thing §16's Turkish counterpart exists to remove.
- **Generic "power words" and copywriting lists.** They point in the opposite direction from everything here.
