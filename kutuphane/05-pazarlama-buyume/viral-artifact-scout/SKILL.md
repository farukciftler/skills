---
name: viral-artifact-scout
description: Finds, feasibility-gates and scores "shareable artifact" app opportunities — the Receiptify / Instafest / Wrapped-clone / roast-generator genre where the real product is an image people post to X and Instagram Stories — and turns them into a ranked opportunity dossier with a data-access gate, a Turkey-specific gap analysis and honest monetization math. Use whenever someone asks what viral image-sharing app or site to build, what is trending on X that could be cloned, what exists in the West but not yet in Turkey, whether a "wrapped" / "stats" / "receipt" / "poster generator" idea can make money, or which APIs still permit this kind of app. Trigger on Turkish phrasings like "viral olacak app fikri", "twitterda paylaşılan uygulamalar", "batıda var Türkiye'de yok", "ne para getirir", "yan proje fikri bul", "wrapped benzeri bir şey", "paylaşılabilir görsel üreten uygulama". Use it even when they never say "viral" — if the question is which small product to build for share-driven growth, this applies.
---

# Viral Artifact Scout

## The mental model

These are not apps. They are **artifact factories**.

The product is a single image that says something about the person holding it. The app is just the machine that prints it. Receiptify is not a music analytics tool — it is a receipt-shaped status object. Instafest is not a festival planner — it is a poster that says *my taste is a headliner*. Nobody opens these twice. That is fine, because the unit of distribution is the image, not the session.

Everything downstream follows from this. Retention is irrelevant. Onboarding must be under 30 seconds. The image must be legible as a thumbnail in a timeline. And the business question is never "how do I keep users" — it is **"what do I capture during a 72-hour spike, and what makes the spike come back."**

Most people asking about this category are quietly hoping for a lottery ticket. The honest job of this skill is to separate the three or four ideas that could actually pay from the forty that will produce a nice weekend and eleven dollars.

## Two failure modes to avoid

**Fantasy list.** A list of clever ideas that all die on contact with an API terms-of-service page. The Spotify genre — the single most-copied template in this category — is effectively closed to new builders as of March 2026. Anyone brainstorming here without checking data access first is writing fiction. Feasibility comes before creativity, not after.

**Translation list.** "Receiptify but Turkish." Direct translations are the weakest opportunities, because the status signal usually doesn't transfer and the original already ranks for the Turkish queries. The strongest opportunities are **TR-native artifact formats with no Western analogue** — status objects built on things Turkey has and the West doesn't.

## Language

Write the deliverable in whatever language the person is using. Keep craft terms in English inside a Turkish report (artifact, share rate, viral coefficient, OG image, rate limit, funnel, RPM, print-on-demand) — that is how practitioners actually talk.

## Phase 0 — Constraints before ideas

Ask one short round of questions (use the interactive options tool if available, otherwise 2–3 inline). Do not skip this: the same idea is a great fit for a solo iOS dev with an existing app and a terrible fit for someone wanting standalone recurring revenue.

1. **Build surface and budget.** Web (fastest to virality, no store review), iOS, or both? Any per-user cost tolerance — an idea with an LLM or image-gen call per artifact has real unit economics, one with pure client-side rendering has none.
2. **Goal.** Standalone revenue, top-of-funnel for a product they already own, portfolio/reputation, or a paid campaign product sold to brands? These select completely different ideas.
3. **Market.** Turkey only, Turkey-first then global, or global-English from day one? This decides everything about monetization math — see `references/04-tr-market.md` on why TR-only ad plays rarely clear.
4. **Timebox.** A weekend, a month, or a real product. Ambition should match; a two-week idea evaluated as a startup produces a useless verdict.

If they just want ideas fast ("hızlıca birkaç fikir"), say so back and run Phases 1–3 in short form plus the scoring table. Do not silently downgrade a full scout.

## Phase 1 — Inventory what already worked

Research live; do not answer from memory. This category turns over every few months and half of the canonical examples are now dead.

Read `references/02-hit-catalog.md` first for the seed catalog and the graveyard, then extend it with current research:

- **Chart diffing.** The single most mechanical method: compare US/UK App Store *Top Free* in Entertainment, Lifestyle, Photo & Video and Graphics & Design against the TR charts for the same categories. Anything ranking in one and absent from the other is a lead. Do the same on Google Play.
- **Builder channels.** Product Hunt (daily/weekly leaderboards), Show HN with high comment counts, r/SideProject, r/InternetIsBeautiful, Indie Hackers milestone posts.
- **The artifact itself.** Search X and TikTok for the *output*, not the product — people post "my spotify receipt", "benim listem", "look at this" without naming the tool. High image-to-text ratio in a search result is the signal.
- **Google Trends.** Compare the term in TR vs US. A US spike with a flat TR line is either an opportunity or a cultural non-transfer — Phase 3 decides which.

For each hit, capture: what the artifact looks like, what data feeds it, how the user authenticates, how it monetized (or didn't), when it peaked, and whether it is still alive. **Verify alive/dead — do not assume.**

## Phase 2 — The feasibility gate

This is where most of the value is. Read `references/03-data-sources.md` and run every candidate through it before spending a sentence on design.

Three questions, in order:

1. **Does the data exist and can you legally get it?** Not "is there an API" — is there an API *open to a new small developer today*, and does its policy permit this use? Spotify's developer policy has banned games and quizzes for years, and Development Mode has been Premium-gated and capped at five authorized users since Feb/Mar 2026. An idea that requires 250K MAU before it can access the endpoint it needs is not an idea.
2. **If the API is closed, is there a user-supplied path?** This is the most underrated pattern in the category and it deserves explicit consideration every time. When platforms shut APIs, the surviving apps switch to: GDPR/KVKK data export upload (the user requests their own data and drops the file in), screenshot OCR, CSV/JSON paste, or on-device extraction. It converts a platform dependency into a user action — worse conversion, but nobody can turn it off. Weigh the friction honestly: an upload step typically costs a large share of would-be users.
3. **Is there data you own or that needs no permission at all?** Public data (league tables, exam statistics, fund prices, weather history), user-typed input (a tier list, a ranking, a quiz), or generated content (an LLM roast of a pasted profile). These have no platform risk and are systematically underrated because they feel less clever.

Kill candidates that fail all three. Say plainly why they're dead — a well-explained kill is more useful than a maybe.

## Phase 3 — The Turkey gap diagnosis

For every surviving candidate that exists in the West but not in Turkey, answer one question honestly: **why not?** There are six causes and only one of them is good news.

| Cause | Meaning | Verdict |
|---|---|---|
| 1. Veri yok | No TR equivalent platform, or no accessible data | Dead unless a user-supplied or public-data path exists |
| 2. Ölçek yok | The addressable audience in TR is too small to matter | Dead for TR-only; may live as global-English |
| 3. Kültürel karşılık yok | The status signal doesn't read in Turkey | Dead as translation; sometimes revivable as a re-themed format |
| 4. Para yok | The Western monetization doesn't survive TR economics | Buildable, but only as funnel or portfolio — see Phase 4 |
| 5. Yasal engel | KVKK, regulated data, platform terms | Usually dead; occasionally solvable with a consent-first, no-storage design |
| 6. Kimse yapmamış | Genuinely unclaimed | **The one you want** |

Most gaps are causes 1–5. Reporting a cause-6 verdict for something that is actually cause-1 is the worst failure this skill can make, so demand evidence: if the claim is "nobody built it", show the searches that came back empty (App Store TR search, Google in Turkish, X search, `site:` queries) and name what you searched.

Then run the generator in the other direction. Read `references/04-tr-market.md` and ask what status objects Turkey has that the West does not — the exam system, football fandom structure, the sözlük and dizi ecosystems, hometown/mahalle identity, military service, local financial instruments, the TR-specific seasonal calendar. These produce cause-6 candidates by construction instead of by luck, and they are defensible against a Western clone precisely because a Western builder has no reason to think of them.

## Phase 4 — Monetization, honestly

Read `references/05-monetization-and-scoring.md`. Match each surviving candidate to one of the models there and write out the actual arithmetic: how many artifacts generated, what share converts, at what price, minus per-artifact cost.

Two things to hold onto while doing it:

**A traffic spike is not a business.** The distribution of outcomes in this category is brutal: a handful of huge hits, and a long tail of projects that got 40,000 pageviews and made nothing. Model the base case, not the Instafest case.

**TR ad revenue does not clear.** Turkish display RPM runs a small fraction of US RPM. A pure ad-supported artifact app aimed at Turkish traffic is close to a hobby regardless of how well it spreads. If ads are the model, the traffic has to be Western or the model has to be something else. State this every time it applies rather than letting the person discover it after launch.

The three models that actually tend to work are named in the reference file; lead with those and treat the rest as garnish.

## Phase 5 — Score and rank

Score each surviving candidate on the six-factor rubric in `references/05-monetization-and-scoring.md`. Use `scripts/score.py` to compute the composite so the ranking is reproducible and the weights are visible rather than vibes.

Do not rank more than about eight candidates. A shortlist of five with real reasoning beats twenty with a paragraph each — the person can only build one anyway.

## Phase 6 — The dossier

Deliver in this structure:

```
# [Kategori] — Fırsat Dosyası

## Özet
Bir paragraf + skor tablosu (ilk 5, sıralı)

## Batıda ne çalıştı
Her hit için: artifact, veri kaynağı, zirve, durum (canlı/ölü), para modeli

## Feasibility duvarı
Neyin kapalı olduğu ve neden — tarih ve kaynakla

## Fırsatlar
Her fırsat için:
  - Artifact: paylaşılan görsel tam olarak nedir (bir cümlede tarif et)
  - Veri: kaynak, erişim yolu, risk
  - TR boşluk nedeni: 1–6 hangisi, kanıtla
  - Para: model + rakamlı senaryo
  - Yapım: efor tahmini, teknik yaklaşım
  - Öldürücü risk: bunu batıracak tek şey

## Elenenler
Kısa liste + tek cümle gerekçe (bu bölüm atlanamaz)

## Öneri
Hangisi, neden, ilk hafta ne yapılır
```

Include the eliminated list every time. It is the part that proves the work was real, and it stops the person re-proposing the same dead idea in three months.

## Evidence discipline

**Never invent numbers.** No fabricated download counts, traffic estimates, revenue figures, or "this got 2M users." If a number matters and can't be observed, name the tool that would produce it (Similarweb, Sensor Tower, App Store chart position) and mark it as needed.

**Mark every claim.** `[VERIFIED]` — fetched and read it. `[INFERRED]` — reasonable from evidence, stated as such. `[NEEDS DATA]` — genuinely outside what's visible.

**Absence of evidence is not evidence.** "Did not appear in the TR App Store searches I ran" ≠ "does not exist in Turkey."

**Date the platform facts.** API rules in this space change quarterly. Every access claim carries the date it was true and, where possible, the source URL. A stale feasibility verdict is worse than none.

**Don't pad.** Five real opportunities beat thirty generic ones. If the honest answer is that the category is picked over and the only live plays are TR-native, say that.

## What this skill will not do

Turn these down and explain the alternative rather than complying:

- **Scraping or unofficial-API workarounds** against a platform that closed access. It gets the app killed at exactly the moment it works, and it exposes the builder. Point to the user-supplied-data pattern instead — it is legitimate, durable, and usually the better product anyway.
- **Cloning a specific live product's name, visual identity, or copy.** Formats are not ownable; brands are. "A receipt-format artifact" is fair game; "Receiptify but with our logo" is not.
- **Harvesting or retaining personal data beyond the artifact.** The safe design in this category — and the one to recommend by default — is stateless: authorize, render, discard. Under KVKK, storing a Turkish user's linked-account data creates obligations most side projects cannot meet. Consent-first, no server-side storage, no third-party data sharing.
- **Engagement bait built on humiliation.** Roast formats are fine. Formats whose share value comes from ranking real named people, exposing someone's data, or comparing bodies are not.
- **Guaranteeing virality.** Nobody can. Give the realistic distribution (most of these get no traction), the mechanics that raise the odds, and what would falsify the thesis within two weeks of launch.

## Handoffs

When a candidate is chosen and moves into build, this skill's job ends. Hand off:

- **Store listing and keyword strategy** → `aso-expert`
- **Launch content, threads, and the seed posts that start the spike** → `trend-setter`
- **The 30-second path from landing to artifact** → `mobile-ux-flow-expert`
- **Discovery pages and the "how to get your X" long tail** → `seo-expert`

Mention the handoff explicitly in the dossier's recommendation section — the launch plan matters more than the build in this category.

## Reference files

Read each at the start of its phase; don't load them all at once.

| File | Read it for |
|---|---|
| `references/01-artifact-anatomy.md` | Why these spread, the five ingredients, format taxonomy, image design rules for X and Stories |
| `references/02-hit-catalog.md` | Seed catalog of Western hits, the API graveyard, what each one taught |
| `references/03-data-sources.md` | Feasibility register per platform, with dates; user-supplied and public-data patterns |
| `references/04-tr-market.md` | TR-native status objects, data availability, payment rails, KVKK, seasonal calendar |
| `references/05-monetization-and-scoring.md` | Ten monetization models with real math, the scoring rubric, dossier detail |
