# Trend Scan — where to look and how to score

Read this at G0. The goal is a ranked candidate list with evidence links, not a feeling about what is popular.

## Contents
- Source hierarchy
- What each source can and cannot tell you
- The scoring rubric
- Saturation read
- Output format

---

## Source hierarchy

Work top-down. The higher a source sits, the closer it is to money actually being spent.

### Tier 1 — Money in motion (strongest signal)

Someone paying to run a creative right now is the only evidence that survives contact with reality.

- **TikTok Creative Center** — Top Ads, filtered by Games category and region. Free, shows currently-running creative, engagement proxies, and often the exact hook framing. This is the single best free source in the stack.
- **Meta Ad Library** — search by advertiser (publisher names below) to see what is live, how many variants are running, and how long each has been running. A creative running for weeks is a creative that works.
- **Ad intelligence platforms** (Sensor Tower creative gallery, AppMagic, Apptica, SocialPeta) — mostly paid, but their public blog posts and free tiers publish creative teardowns and top-advertiser lists regularly. Search for the current quarter's reports rather than relying on any figure recalled from memory.

### Tier 2 — Chart movement

- **App Store Top Free → Games**, and the relevant subcategory, in several geos. Read the *velocity*, not the position. A title that entered the top 100 in the last two weeks is the interesting one.
- **AppMagic / Appfigures / Sensor Tower "breakout" and "rising" lists** — these are published as free blog content on a regular cadence. Find the most recent one.
- **Publisher release feeds** — a publisher shipping four titles on the same mechanic in a month is telling you they found something.

### Tier 3 — Upstream culture

Where the hook comes from before it is a game.

- TikTok and Reels: satisfying-process content, physics sims, ASMR mechanics, trend sounds attached to a repeatable visual
- YouTube Shorts, r/oddlysatisfying, r/gaming discourse
- Viral browser toys and web games — many hyper-casual hits are a web toy with a fail state and an ad SDK

### Tier 4 — Industry commentary

Useful for market structure, not for picking a mechanic: GameAnalytics benchmark reports, Liftoff casual gaming reports, Adjust/AppsFlyer benchmark publications, Unity and AppLovin state-of-the-industry posts, deconstructor.of.fun, GameRefinery/Liftoff teardowns, Mobile Dev Memo.

Use these for the *current* structural picture — including whether pure hyper-casual is still a viable model at all versus hybrid-casual (IAA plus light IAP, deeper meta layer, longer retention curves). That structural answer has shifted meaningfully in recent years, so establish it from a current source at the start of a scan rather than assuming.

---

## What each source cannot tell you

- Creative galleries show what is being advertised, **not what retains**. Plenty of well-advertised games die at D3.
- Chart position shows install volume, **not profitability**. A publisher can buy a chart position at a loss to test.
- Download estimates from third-party tools are modeled, with wide error bars in smaller markets. Treat them as rank ordering, not measurement.
- Nothing in Tier 1-3 tells you eCPM. That comes from mediation dashboards after launch, or from benchmark reports with a date attached.

State these limits when presenting candidates. A candidate list that pretends to more certainty than the sources support leads to a bad G3 commitment.

---

## Scoring rubric

Score each candidate 1-5 on six axes. Present as a table with the total, and never hide a low score behind a high total.

| Axis | 5 = | 1 = |
|---|---|---|
| **Hook legibility** | The appeal is obvious in 2 seconds with no sound | Needs explanation or context |
| **Thumb simplicity** | One finger, one gesture, no tutorial | Multi-touch, complex input, needs onboarding |
| **Build cost** | Prototype in 3 days | Weeks of systems work |
| **Creative headroom** | Ten obviously different ad angles exist | One angle, already worn out |
| **Saturation** | Rising, few credible clones shipped | Several established incumbents at scale |
| **Hybrid potential** | An obvious meta layer / progression / IAP could be added later if it retains | Purely disposable, no path past D3 |

Hybrid potential deserves weight. A concept with no path beyond a single loop caps out early even if it tests well, and the current market rewards depth more than the pure-hyper-casual era did.

**Bar for advancing to G1:** no axis below 2, and the total in the top third of the candidate set. If nothing clears it, widen the scan rather than promoting the least-bad option.

---

## Saturation read

For each surviving candidate, do a focused App Store search on the mechanic's keywords and answer three questions with evidence:

1. How many shipped titles already implement this mechanic?
2. Are any of them at scale — meaning a known publisher is running ads for it right now?
3. Is there an angle nobody has taken — a theme, a geo, a control scheme, a hybrid layer?

If the answer to 2 is yes and to 3 is no, kill the candidate. Competing against a funded incumbent's UA machine on a small budget is not a test, it is a loss with extra steps. It also raises real App Store rejection risk under the spam/clone guideline — verify the current guideline text before advising on this.

---

## Output format — `konsept-adaylari.md`

```markdown
# Konsept Adayları — [tarih]

## Tarama kapsamı
Kaynaklar, sorgular, tarama tarihi. Neyin bakılmadığı da yazılır.

## Adaylar

### 1. [İsim]
- **Mekanik:** tek cümle
- **Reklam kancası:** tek cümle
- **Kanıt:** [link] — nerede görüldü, ne zaman
- **Doygunluk:** kaç rakip, kim ölçekte, hangi açı boş
- **Build tahmini:** N gün
- **Skor:** kanca X / parmak X / maliyet X / kreatif X / doygunluk X / hybrid X = **toplam**

## Öneri
Hangisi G1'e geçiyor ve neden. Elenenler tek satırla gerekçeli.

## Kaynakların söyleyemedikleri
Bu listenin dayanmadığı şeyler.
```
