# humanly

Finds the fingerprints of AI writing in English prose and rewrites it so it reads like a person wrote it.

This is the English sibling of [`insanca`](../insanca), which does the same job for Turkish. It is not a translation. Roughly a third of the Turkish rules depend on Turkish morphology and have no English equivalent, and English carries tells that Turkish does not, so the shared thing between the two skills is the architecture: the same section order, the same numbering, the same pattern-entry format, the same draft/audit/final loop.

## What carried over, what changed

Nine sections in twelve are direct counterparts, because the tell is the same in both languages: inflated significance, brochure language, vague attribution, empty truths, invented examples, negative parallelism, the rule of three, em dashes, boldface inflation, needless bullets, emoji, rhetorical question and answer, signposting, cliché openers, generic closers, chat residue, sycophancy, therapist mode, hedge stacking, faux profundity, and the detector-derived structural patterns.

Three numbered slots hold different content in the two skills, and each is marked in place:

| Slot | `insanca` | `humanly` |
|---|---|---|
| §13 | "-maktadır" monotony and end-of-sentence rhyme | Nominalization and the disappearing verb |
| §16 | Translation smell (English thought, Turkish words) | Content-mill English (SEO listicle and LinkedIn cadence) |
| §32 | Turkish punctuation errors and circumflexes | Typographic artifacts (curly quotes, ellipsis characters, interface residue) |

One slot is new: §49, the floating "this", a demonstrative with no noun behind it. Turkish has no equivalent because it drops pronouns rather than stranding them.

One rule gives the **opposite** advice in the two skills, which is the clearest evidence that translating would have gone wrong. Turkish dialogue wants varied attribution; English wants "said" nearly every time, because the reader stops seeing it. A translator would have exported the Turkish rule and produced textbook amateur English fiction.

## The other difference: where the positive half comes from

Both skills have a section on how the language actually moves, on the theory that removing patterns is only half the job. `insanca` derives its version from close reading of real Turkish prose: columnists from 2012 to 2019, Gürpınar, a modern novel, a translated classic. `humanly` derives its version from named craft authorities instead: Gopen and Swan on topic and stress position, Williams on nominalization and agency, Christensen on the cumulative sentence, Orwell, Leonard.

Authorities are checkable; corpora are evidence. They are not the same thing, and this is a real gap rather than a stylistic choice. Until an English corpus pass is done, treat the rules in "How real English moves" as well-sourced convention. It is the biggest single improvement available to this skill, and it is logged as such in `references/sources.md`.

## Files

- `SKILL.md` — the skill itself. 49 patterns, a numeric audit, a false-positive guide and a worked example.
- `references/phrasebank.md` — replacement bank for bloated verbs, copula avoidance, nominalizations and filler. Read on demand.
- `references/sources.md` — the source inventory: what was processed, what is queued, what was deliberately excluded and why.

## Limits

It does not beat AI detectors, and does not try to. The Liang study found detectors misclassify more than 61 percent of TOEFL essays as machine-written, because a limited linguistic range reads as low perplexity. Writing to a detector score punishes exactly the writers detectors already misjudge. The skill's job is good English.

It does not add personality to writing that should not have any. Encyclopedic, legal, technical and reference prose is supposed to be neutral, and neutral plain language is the right human voice there.

It does not verify facts. If a source, quotation or figure in the text cannot be checked, the skill flags it rather than repairing it.

## License

MIT. Derived from `insanca` by Tahir Yıldız, whose copyright notice is retained in `LICENSE`.
