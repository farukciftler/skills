# Evaluating an app idea

The framework for "should I build this?" — designed to reach a defensible answer rather than an encouraging one.

## Contents
- [The five gates](#the-five-gates)
- [Reverse the number](#reverse-the-number)
- [Category saturation read](#category-saturation-read)
- [Where the openings actually are in 2026](#where-the-openings-actually-are-in-2026)
- [Red flags](#red-flags)
- [The distribution question](#the-distribution-question)
- [Worked example](#worked-example)

---

## The five gates

Run an idea through these in order. Failing an early gate makes the later ones irrelevant.

**Gate 1 — Is there a payer?**
Not "would people use this" — would someone *pay*, and who specifically. "Everyone" is a failing answer. The strongest form is a nameable role or situation: freelance translators, people managing a parent's medication, indie musicians releasing on Spotify.

**Gate 2 — Is the value legible fast?**
Hard paywalls convert 5× better than freemium, but only work when someone can see the value in under a minute. If the product needs a week of use to become obviously worth paying for, you are in freemium territory with a 2.1% median conversion, and your volume requirement multiplies accordingly.

**Gate 3 — Can you reach the payer?**
This is the gate most ideas fail and the one most people skip. 14,700 new subscription apps launch monthly against flat total downloads. App Store search is not a distribution channel for a new entrant in a competitive category. If the answer is "ASO and hope", the idea fails this gate regardless of quality.

**Gate 4 — Is there a moat that isn't just execution?**
With AI-assisted development, a clean SwiftUI utility can be cloned in a weekend. Durable advantages: a proprietary data asset, a regulatory certification, a distribution channel you own, deep platform integration a cross-platform clone can't match, a community, or a genuinely hard technical core. "It's well designed" is not a moat in 2026.

**Gate 5 — Does the math work at your cost base?**
Run the reverse calculation below. A Türkiye-based solo developer needs a much smaller outcome than a US-based team to justify continuing — that is a real advantage, and it should change the verdict rather than being a consolation.

## Reverse the number

Do not estimate revenue. Estimate the *requirement*, then judge plausibility.

```
target monthly revenue
  ÷ (price × (1 − commission) × (1 − tax))
  = required paying subscribers

required subscribers × monthly churn
  = subscribers you must replace every month

replacements ÷ download-to-paid conversion
  = required monthly installs

required installs ÷ realistic conversion from your channel
  = required monthly reach
```

Then ask the only question that matters: **can I produce that reach every month, indefinitely?**

Worked with realistic inputs — $3,000/month target, $9.99/month price, 15% commission, 2.6% D35 conversion (North America median), 8% monthly churn:

- Proceeds per subscriber ≈ $8.49 → **~354 paying subscribers needed**
- At 8% churn → **~28 replacements/month**, plus growth
- At 2.6% conversion → **~1,090 installs/month** just to stand still
- Getting to 354 from zero at that conversion → **~13,600 cumulative installs**

Is 1,000+ installs a month sustainable through the channels you actually have? For most people the honest answer is no without either paid acquisition or an existing audience. That is the finding, and it is more useful than any market-size figure.

**Run this with pessimistic inputs too.** Use freemium's 2.1% instead of a hard paywall's 10.7%, use 12% churn, use $14 emerging-market RLTV. If the idea survives the pessimistic case, it is robust.

## Category saturation read

How to judge whether a category has room:

| Signal | Read |
|---|---|
| Top 10 unchanged for 2+ years | Entrenched. Entry needs a wedge, not a better version |
| Top 10 churns regularly | Live category, room for a new entrant |
| Category revenue growing, download volume flat | Monetization is improving — good for a premium entrant |
| Many apps, low ratings across the top | Unmet need. The best signal there is |
| Dominated by one free app from a platform owner | Very hard. Apple/Google shipping it for free caps your ceiling |
| Requires ongoing content or data licensing | Capital-intensive, but that's also the moat |
| Apps from before 2020 hold the revenue | Normal — 69% of subscription revenue sits there globally |

**The most useful research action:** read one- and two-star reviews of the top five apps in the category. That is where the unserved need is stated explicitly by people who already tried to pay for a solution.

## Where the openings actually are in 2026

Reasoning from the structural facts rather than listing trends:

**1. Deep platform integration.** Foundation Models, App Intents/Siri, widgets, Live Activities, Watch. Cross-platform competitors cannot match these without significant bridging work, and most won't. This is the clearest durable advantage available to a native developer right now, and it is temporary — it closes as the tooling matures.

**2. Privacy as a product, not a feature.** On-device processing is a claim a cloud-based competitor structurally cannot make. In categories handling sensitive material — health, journaling, finance, personal notes — "nothing leaves your device" is a positioning that survives competition. Free on-device inference makes this economically viable in a way it wasn't two years ago.

**3. Professional verticals.** Small audiences, high willingness to pay, low competition, and App Store search actually works because the queries are specific. The premium-tail analysis in `pricing.md` describes the shape.

**4. Non-obvious localization.** A category that is well-served in English and unserved in Turkish, Arabic, or another market with real smartphone penetration. The catch is that these markets often have low ARPU — this works best when the local market has money or when the app can also serve the diaspora.

**5. Categories where AI genuinely changes the product**, not where AI is bolted on. The distinction: does the AI make a previously impossible feature possible, or does it add a chat button? The former is a product; the latter is 14,700 apps a month.

**Where it is hardest right now:** general AI chat wrappers, generic productivity, habit trackers, meditation, general fitness, photo editors, and anything where an AI-assisted developer can clone your entire feature set in a weekend.

## Red flags

Say these out loud when you see them:

- **"It's like X but better."** Better is not a distribution strategy against an incumbent with an installed base.
- **"We'll monetize later."** Decide the model before building — it shapes the product.
- **"The market is $XXX billion."** Especially when the figure is Apple's $1.4T ecosystem number. Your addressable market is the payers you can reach.
- **"It'll go viral."** Virality is a property of some product mechanics and not of most. If there is no share loop built into the core action, plan for paid or organic-slow.
- **"Turkish users will love it."** They probably will. That is not the same as paying for it.
- **No distribution answer.** The most common fatal flaw. If Gate 3 has no answer, nothing else matters.
- **A moat of "we'll execute better."** In an era of AI-assisted development this is a six-week lead at most.

## The distribution question

Since this is the gate most ideas fail, name the channels concretely:

| Channel | Works for | Reality |
|---|---|---|
| App Store search / ASO | Specific-intent categories, professional tools | Not a channel for a crowded consumer category |
| Apple featuring | Well-crafted, platform-native, timely apps | Not plannable, but real. Adopting new APIs early materially helps |
| Existing audience | Anyone with a newsletter, YouTube, or following | The highest-conversion channel that exists |
| Short-form video (Reels/TikTok/Shorts) | Visual, demonstrable products | High variance, high effort, genuinely works |
| Product Hunt / HN / Reddit | Developer and prosumer tools | One spike, not a channel |
| Paid UA | Anything with proven LTV > CAC | Requires capital and measured unit economics first. ATT opt-in near 25% makes attribution hard |
| Press | Novel or newsworthy | Diminishing returns, but a launch beat helps |
| Partnerships / bundles | B2B and vertical tools | Slow, durable |

**If the honest answer is "I have no audience and no budget", the viable paths narrow to: a specific-intent category where ASO works, a product with a native share loop, or building the audience before the app.** That is a real strategy, not a failure — but it should be a conscious choice.

## Worked example

*"Should I build a privacy-first personal assistant using on-device AI?"*

- **Gate 1 — payer:** people who want an assistant but won't send their notes and calendar to a cloud service. Real, identifiable, but a segment of a segment.
- **Gate 2 — legible value:** partly. "Nothing leaves your device" is legible immediately; "it's actually useful" requires trying it. Suggests freemium or a short hard trial, not an aggressive wall.
- **Gate 3 — reach:** the privacy angle is press-friendly and communities exist (privacy-focused forums, HN, the Apple indie ecosystem). Weak on App Store search — "assistant" is unwinnable. Passable but needs the press/community path worked deliberately.
- **Gate 4 — moat:** on-device Foundation Models integration is genuinely hard for a cross-platform competitor to match, and the privacy claim is structural, not marketing. This gate passes well. The risk is Apple itself — Siri occupies this space and improves annually.
- **Gate 5 — math:** at $4.99/month, a $1,000/month target needs ~235 subscribers; at 2.1% freemium conversion and 10% churn that's roughly 1,100 installs/month steady state. Plausible with sustained community and press effort. Meaningful income at a Türkiye cost base; not a business at a US one.

**Verdict:** buildable, with the caveats named. The real risks are (a) Apple absorbing the use case and (b) the distribution work being larger than the development work. Both should be planned for rather than discovered.

Note what this analysis did *not* do: quote a market size, project hockey-stick growth, or say "the AI assistant market is $X billion". None of that would have changed the decision.
