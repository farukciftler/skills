# Claims and Policy

The two things that end functional-audio channels are **what the words promise** and **how interchangeable the uploads look**. Both are naming problems. This file is the gate.

## Contents

1. The one heuristic
2. The claim substitution table
3. Tiers of risk
4. Medical-misinformation exposure, concretely
5. Inauthentic content — the templated-catalogue trap
6. Reused content — the duplicate-audio trap
7. AI disclosure
8. Content ID before publishing
9. The safety line
10. Advertiser framing
11. Verify before you rely on this

## 1. The one heuristic

**Verbs about the music are safe. Verbs about the body are not.**

| Safe subject | Risky subject |
|---|---|
| tuned to · composed for · designed for · recorded at · built around · written to accompany · for · to unwind with | heals · cures · repairs · regenerates · detoxes · rewires · lowers your blood pressure · boosts immunity · balances your hormones · fixes |

"Tuned to 528 Hz" is a verifiable fact about the recording. "528 Hz DNA Repair" is a claim about the listener's biology, unsupported, and pointed straight at the most sensitive policy surface on the platform. The keyword `528 Hz` survives either way — which is the whole point. **You never have to sacrifice the search term to drop the claim.**

## 2. The claim substitution table

| Don't write | Write instead |
|---|---|
| DNA Repair / Cell Regeneration / Cellular Healing | `528 Hz` alone, or `528 Hz Ambient for Deep Rest` |
| Heals Your Body / Whole-Body Healing | `for restful listening`, `slow, warm, low-volume` |
| Cures Insomnia / Fall Asleep in 3 Minutes Guaranteed | `for sleepless nights`, `Sleep Music for Insomnia` (the *query*, not a cure) |
| Cures / Eliminates Anxiety | `to unwind with`, `for a restless evening`, `Calming Music` |
| Removes Negative Energy from Your Home | `in the sound-healing tradition`, `a slow clearing ritual` — tradition-framed, never guaranteed |
| Activates Your Pineal Gland / Third Eye Opening | `963 Hz`, `crown-chakra tradition`, framed as practice not physiology |
| Lowers Blood Pressure / Heart Rate in 10 Minutes | drop entirely — a measurable physiological claim needs real evidence |
| Better Than Medication / Instead of Therapy / Skip the Pills | **never.** Discouraging professional care is the single most serious line in this domain |
| Doctor Recommended / Clinically Proven / Scientifically Proven | drop, or cite a real, linked, correctly-described study |
| Autism / ADHD / Dementia Treatment | drop the treatment framing; `Focus Music` describes a use, not a therapy |
| Miracle Tone (as effect) | acceptable only as the phrase's traditional *name*, in the description, marked as such — never as an outcome |
| Heals Trauma / Emotional Release Guaranteed | `written for slow evenings`, `a quiet hour` |

Two extra notes:

- **The query is not the claim.** Bidding on the phrase "sleep music for insomnia" describes what people search for and what the music is for. "Cures insomnia" asserts a medical result. The first is legitimate optimisation; the second is the violation. Keep the noun, drop the promise.
- **Tradition framing is a real and honest option** for the spiritual register: name the practice ("in the reiki tradition", "a chakra-sequence meditation") rather than asserting a mechanism. It reads as more authentic to the actual audience, too.

## 3. Tiers of risk

- **Tier 1, never, in any field:** anything discouraging professional medical care; any named-disease treatment claim (cancer, diabetes, depression as treatable-by-audio); fabricated clinical authority. This tier risks removal, not just demonetisation.
- **Tier 2, avoid:** unqualified physiological outcome claims (DNA, blood pressure, immunity, hormones) — the standard vocabulary of the niche's older titles, and the reason many of those channels sit under review.
- **Tier 3, use with care:** spiritual and energetic language. Legitimate as tradition or practice description; problematic as guaranteed effect.
- **Tier 4, free:** tuning facts, duration, instrumentation, mood, use-case queries, scene description. Everything you actually need.

## 4. Medical-misinformation exposure, concretely

YouTube's medical-misinformation policy prohibits content that contradicts health-authority guidance on prevention, treatment or denial for specific conditions, and explicitly covers **promoting unproven treatments in place of approved care** and **discouraging viewers from seeking professional treatment**. It applies to titles, descriptions, comments and links — not just the audio or video. A music upload whose title offers a cure for a named condition, or whose description tells viewers to try frequencies instead of their prescribed treatment, is inside that policy's scope regardless of the fact it is "just music".

The practical rule: an ambient track can be *for* sleep. It cannot be *treatment for* insomnia. And nothing in the metadata may ever position it as an alternative to care.

## 5. Inauthentic content — the templated-catalogue trap

In July 2025 YouTube renamed its "repetitious content" monetisation policy to **"inauthentic content"**, clarifying that it covers content that is repetitive or mass-produced — templated with little variation between videos, or easily replicable at scale. It was already ineligible for monetisation before the rename; the rename signalled where enforcement was going, and enforcement has since been reported to run at **channel level**, not just per video. AI use is not itself the violation; the interchangeability is.

Naming-side signals that read as templated:

- Titles differing only by a number or a single swapped adjective.
- One title skeleton repeated across most of the catalogue.
- Thumbnails sharing an identical layout with a changed word.
- Upload cadence far above what the channel's age and production story would support.

Naming-side defences, all cheap:

- Vary the lexical body of the title, not just the spec tokens — different scene, different instrument, different phrasing.
- Real chapter lists with named sections (a curation artefact a template does not produce).
- A stated curation logic per upload or per series ("recorded low and slow for the last hour before sleep").
- The differentiation ledger in `catalog-architecture.md`, so variation is designed rather than hoped for.

Run `scripts/metadata_audit.py --catalog` on every new title. Pairwise similarity against the existing catalogue is the only way to see this pattern forming before it is 40 uploads deep.

## 6. Reused content — the duplicate-audio trap

Separate policy, adjacent failure. Reported as clarified in 2026 to explicitly cover AI-generated audio. Three patterns to refuse outright, no matter how the request is framed:

1. **Thumbnail farming** — the same audio uploaded repeatedly under different titles and thumbnails. Audio fingerprinting makes this trivially detectable.
2. **Third-party re-uploads** — republishing tracks pulled from someone else's Suno/Udio gallery or channel without transformation.
3. **Loop padding** — a 60-second loop repeated sixty times sold as a one-hour piece.

The test to apply: *would a human listener consider each upload a distinct piece of work?* If not, it is reused content, whoever or whatever made the audio.

## 7. AI disclosure

Suno-generated audio means toggling the **altered or synthetic content** disclosure in YouTube Studio. Disclosure has been required since 2024 and is enforced more strictly since; it does **not** by itself remove monetisation or limit reach. Non-disclosure is its own violation, independent of topic. So: disclose, always, and stop treating it as a cost.

Do not put "AI generated" in the title unless it is the actual selling point (a tools-and-process channel). The Studio toggle is the compliance mechanism; the title is for the viewer.

## 8. Content ID before publishing

Generative models can produce output that resembles training material closely enough to trigger Content ID. Run every track through the copyright check in Studio before publishing; if a claim appears, regenerate rather than dispute-and-hope. A catalogue with repeated claims risks monetisation and strikes.

## 9. The safety line

Include in the description of any sleep, hypnosis-adjacent or deep-relaxation upload, in plain language:

> Not medical advice. Don't listen while driving or operating machinery. If you have a health condition, speak to a clinician.

It is the convention in this niche for good reason: it protects listeners, it signals good faith to reviewers, and it costs nothing.

## 10. Advertiser framing

The wellness lane is favourable ground — sleep, meditation and mindfulness draw premium advertiser categories, and reporting indicates YouTube relaxed monetisation on some mental-health-adjacent topics in January 2026. What forfeits that advantage is not the topic but the framing: clinical claims, distress-baiting ("Why You Can't Sleep — The Truth"), and mismatched clickbait. Calm, honest, specific metadata is the version of this niche that advertisers pay for.

## 11. Verify before you rely on this

Policy names, enforcement posture and monetisation figures in this file reflect reporting up to mid-2026 and will drift. Before delivering compliance-sensitive advice, search for the current state of: the inauthentic-content policy, the reused-content policy, synthetic-content disclosure requirements, and the medical-misinformation policy. Present the finding, not a remembered version of it.
