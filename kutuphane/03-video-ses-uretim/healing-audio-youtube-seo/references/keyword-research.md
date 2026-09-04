# Keyword Research for Functional Audio

## Contents

1. The one thing to internalise
2. Intent taxonomy — the demand map
3. Seed phrase banks
4. Harvesting live demand (autocomplete + search + competitors)
5. Competitor n-gram extraction
6. Scoring a phrase before you commit
7. Choosing primary and secondaries
8. Language and geography
9. Freshness — what goes stale

---

## 1. The one thing to internalise

Search intent in this niche is **situational, not artistic**. The viewer is lying in bed at 1 a.m., or sitting down to revise, or opening a massage room. They type the situation. Every winning title therefore contains a *situation phrase* — and the whole optimisation problem is: which situation phrase, how early in the title, and can you honestly serve it.

There is a second, quieter path: **suggested/recommended traffic**, which is most of the volume on long-form ambient once a video establishes itself. Suggested traffic responds to session behaviour and to topical proximity — which is why playlist architecture and consistent series language (see `catalog-architecture.md`) matter as much as the search phrase.

## 2. Intent taxonomy — the demand map

Pick exactly one primary lane per upload. Two lanes in one title splits the retention signal and confuses the recommendation system.

| Lane | Typical session | Notes on value |
|---|---|---|
| Sleep / insomnia / bedtime | 1–8 h, overnight, passive | Longest watch sessions in the vertical; wellness advertisers; strong lane |
| Meditation / mindfulness / breathwork | 10–60 min, semi-active | Benefits from real narration or structured sections |
| Study / focus / deep work / ADHD-adjacent | 1–4 h, background | Education + productivity advertisers; competitive |
| Frequency / solfeggio / binaural / chakra | 30 min–8 h | Highest claim risk; see `claims-and-policy.md` |
| Spa / massage / reiki / yoga (professional use) | 1–3 h | B2B-ish, low competition sub-phrases, loyal repeat use |
| Rain / nature / fireplace / ambience | 1–10 h | Huge demand, huge supply; win on specificity of scene |
| Lo-fi / jazz / piano background | 1–3 h | Aesthetic-led; needs visual identity to survive |
| Cinematic / trailer / royalty-free-for-creators | 2–10 min | Highest CPM tier, lowest saturation, creator audience |
| Anxiety / stress relief / calm | 15 min–3 h | Sensitive framing; keep to experience language |

If the person is choosing a lane rather than a single title, note the trade: sleep and cinematic sit at the favourable end for both policy risk and advertiser value; generic beat compilations and type-beat formats sit at the bad end on every axis.

## 3. Seed phrase banks

Use these as *starting points to test against live autocomplete*, never as a finished keyword list. Titles are written in English for global reach unless the channel is deliberately TR-targeted (§8).

**Situation heads** — `music for deep sleep` · `sleep music` · `relaxing music` · `meditation music` · `study music` · `focus music` · `spa music` · `massage music` · `yoga music` · `reiki music` · `healing music` · `calming music` · `ambient music` · `background music for` · `sound bath`

**Modifier tails** — `for deep sleep` · `for insomnia` · `to fall asleep fast` · `for babies` · `for anxiety` · `for stress relief` · `for concentration` · `for reading` · `for work` · `for meditation` · `for yoga` · `for massage` · `for studying` · `to relax` · `to unwind`

**Spec tokens** — `432 Hz` · `528 Hz` · `396 Hz` · `417 Hz` · `639 Hz` · `741 Hz` · `852 Hz` · `963 Hz` · `delta waves` · `theta waves` · `alpha waves` · `binaural beats` · `solfeggio` · `chakra` · `8 hours` · `3 hours` · `1 hour` · `10 minutes` · `black screen`

**Scene tokens** — `rain` · `thunderstorm` · `ocean waves` · `forest` · `fireplace` · `night` · `snowfall` · `river` · `wind chimes` · `singing bowls` · `harp` · `piano` · `handpan` · `flute` · `cello` · `drone`

Two under-served pockets worth checking every time, because they carry intent without carrying the crowd: **professional-use phrasing** ("music for massage therapists", "spa treatment room music") and **scene-specific compounds** ("rain on a tin roof piano"), where specificity beats volume.

## 4. Harvesting live demand

Run all four. Twenty minutes of this is worth more than any amount of intuition.

1. **Autocomplete sweep.** Take each candidate head and expand it: append `for `, then each letter a–z; prepend the spec tokens. Autocomplete is YouTube telling you what real people finish typing. Capture the exact suggested strings verbatim — spacing and word order matter, `432hz` and `432 Hz` are different tokens in practice, so record which form appears.
2. **Search the phrase and read the shelf.** For each surviving candidate, run `web_search` on the phrase plus "youtube" and inspect the top results: view counts, upload dates, channel size, durations. What you want is any result in the top rows that is **recent and from a small channel** — that is the tell that the phrase is winnable. If every top result has millions of views and 1M+ subscribers, the phrase is a wall; take a longer-tail compound instead.
3. **Velocity over totals.** A 40M-view video from 2019 tells you the phrase has demand but not whether it is currently contestable. A 200k-view video from three weeks ago tells you both.
4. **Check the frequency trend specifically.** Which Hz values are being uploaded and searched right now shifts on a scale of months. Confirm rather than assume.

## 5. Competitor n-gram extraction

The single highest-yield analytical move: take the **top 10 currently-ranking videos** for your intended phrase and extract the repeated word sequences across their titles. What repeats in 7 of 10 titles is the grammar of that query — the tokens the audience and the algorithm both expect. What appears in only one is that channel's branding, not a requirement.

Record it as a table: token, how many of the 10 titles contain it, its usual position (front / middle / tail). Then build your title to satisfy the high-frequency tokens **in their usual positions**, and differentiate on the tokens that are absent — your scene, your instrument, your series name. Match the grammar, differ in the content. Copying a competitor's title wholesale loses on both counts: you look interchangeable to viewers and templated to detection systems.

## 6. Scoring a phrase before you commit

Score each finalist 1–5 on four axes and write the numbers down; a phrase that wins on demand and loses on winnability is a trap.

| Axis | Reading it |
|---|---|
| **Demand** | Appears in autocomplete unprompted? Multiple high-view results? Autocomplete presence is the cheapest reliable signal available without a paid tool. |
| **Winnability** | Any recent small-channel result in the top rows? Are top results poorly titled or badly served (wrong duration, low audio quality, mismatched promise)? A saturated phrase served badly is still an opening. |
| **Value tier** | Sleep, meditation, cinematic and study lanes draw wellness/education/B2B advertisers; generic loop compilations draw remnant inventory. Realistic 2026 spread runs roughly $3–$8 RPM in premium lanes versus well under $1 in saturated ones — verify current figures rather than quoting these. |
| **Honest fit** | Can the actual file serve this promise? A 40-minute bed cannot bid on "8 hours". A bright major-key piece cannot bid on "deep sleep" without hurting retention. |

Kill any phrase that requires a claim you cannot make honestly, however large its demand. `claims-and-policy.md` lists which ones those are.

## 7. Choosing primary and secondaries

- **One primary phrase.** It goes at the front of the title, verbatim, in the word order autocomplete gave you. Do not rearrange it for elegance.
- **Two secondaries.** They live in the description's first paragraph and in tags, phrased as natural prose, never as a comma-dump.
- **Do not stack primaries in the title.** Three head phrases in one title is the classic error of this niche: it truncates into nonsense on mobile and asks the recommendation system to place you in three unrelated audiences at once.

## 8. Language and geography

Default to **English titles** — the audience for functional audio is global and English phrasing captures the largest addressable demand, and audience geography is one of the strongest levers on revenue per view. Options if Turkish matters:

- English title, Turkish subtitle/localised metadata via YouTube's translation fields (not by stuffing both languages into the 100 characters).
- A Turkish-language title only when the piece is culturally specific and the target is TR listeners — makam-based work, Sufi-adjacent instrumentation, Turkish-language guided material. Here the Turkish phrase is the honest primary: `ney ile meditasyon müziği`, `uyku müziği 8 saat`.
- Never a bilingual title. It halves both keywords and eats the truncation window.

## 9. Freshness — what goes stale

Re-run research when: the channel's impressions-per-upload drop while retention holds (the phrase has become contested); a new frequency or modality enters the mainstream; a competitor's new title format starts appearing across the top shelf; or more than a quarter has passed since the last sweep. Keep the last sweep's n-gram table in the workspace so the next one is a diff, not a restart.
