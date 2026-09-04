# Shipping: submission gates, review, and monetization plumbing

Some requirements live in the App Review Guidelines. Others — SDK floors, age ratings, required-reason APIs, regional compliance — sit outside them and can block an *upload* before review even starts. A checklist has to cover both.

## Contents
- [Hard gates before you can upload](#hard-gates-before-you-can-upload)
- [Metadata and privacy](#metadata-and-privacy)
- [Age ratings](#age-ratings)
- [What actually gets apps rejected](#what-actually-gets-apps-rejected)
- [Review notes that work](#review-notes-that-work)
- [StoreKit 2](#storekit-2)
- [Commission and programs](#commission-and-programs)
- [Regional compliance](#regional-compliance)
- [Handling a long review or a rejection](#handling-a-long-review-or-a-rejection)

---

## Hard gates before you can upload

| Gate | Since / status |
|---|---|
| Built with iOS 26 / iPadOS 26 / tvOS 26 / visionOS 26 / watchOS 26 SDK, i.e. Xcode 26+ | **April 28, 2026**, no announced grace period |
| Age rating questionnaire answered under the new system | **January 31, 2026** — unanswered blocks update submission |
| Active Apple Developer Program membership | ongoing |
| Valid distribution certificate and provisioning profile | ongoing |
| Live, reachable privacy policy URL | ongoing |
| Complete App Privacy labels | ongoing |
| Privacy manifest (`PrivacyInfo.xcprivacy`) declaring required-reason API use and tracking domains, including for bundled third-party SDKs | ongoing |
| EU trader status verified (Digital Services Act) | since February 2025 — unverified apps get removed in the EU |

Existing apps stay live if you don't update. The moment you ship an update, current gates apply.

## Metadata and privacy

- **App Privacy labels** must match reality including third-party SDKs. Analytics and ad SDKs collect more than developers expect — read their published label guidance rather than assuming.
- **Privacy manifests** are required from you *and* from SDKs you bundle. A stale SDK without a manifest blocks your upload, not theirs.
- **ATT** — if you track across apps/sites, you need the prompt, and enforcement has tightened. Global opt-in rates sit near 25%; design your measurement around SKAdNetwork and contextual signals rather than assuming consent.
- **Declared Age Range API** (2026, iOS 26+/iPadOS 26+/macOS 26+) shares an age-category signal without collecting birthdates. Use it instead of asking for a date of birth where you need age gating.
- **Account deletion** is mandatory in-app if you support account creation. Reviewers check this specifically.
- **Screenshots** must show the actual app. Marketing frames around real screenshots are fine; mockups of features that don't exist are not.

## Age ratings

The system now has 4+, 9+, 13+, 16+, 18+ (replacing the old bands), assigned per country/region, with new questionnaire items for sensitive content and the ability to set a higher minimum than the questionnaire produces.

**The AI clause matters:** Apple explicitly requires you to consider how *AI assistants and chatbot functionality* affect the frequency of sensitive content in your app when answering. An app that embeds an LLM has to answer honestly about what that LLM can produce. Under-rating an AI feature is a rejection risk and a removal risk.

Regional variation is live and changing — e.g. Australia retired 15+ (apps moved to 16+) and Vietnam requires a region-specific rating under Decree 147 Article 38, both effective June 18, 2026. Check the storefronts you ship to.

## What actually gets apps rejected

In rough order of frequency:

1. **2.1 Completeness** — placeholder text, dead URLs, crashes, features behind a login the reviewer can't get past, a build that isn't a final version.
2. **4.2 Minimum functionality** — a thin wrapper around a website, or an app that could be a web page. Very common for first submissions.
3. **3.1.1 In-app purchase** — digital goods sold outside IAP, or an external purchase link without the applicable entitlement.
4. **5.1.1 Data collection** — asking for data you don't need, permission prompts without clear purpose strings, mandatory account creation for features that don't need one.
5. **2.3 Accurate metadata** — screenshots or description promising things the app doesn't do.
6. **4.3 Spam** — near-duplicate apps from the same developer. Templated app families get caught.
7. **5.1.2 / privacy** — undeclared tracking, mismatched privacy labels.
8. **Guideline 1.x safety** — user-generated content without moderation, reporting, and blocking. AI-generated content counts as UGC for this purpose, and Apple's 2025–2026 guideline updates specifically addressed creator apps, AI-generated content, and mini apps.

Recent guideline movement to be aware of: stricter age-verification mechanisms, US state App Store Accountability Laws, and the EU's transition from the Core Technology Fee to the Core Technology Commission.

## Review notes that work

Reviewers are time-constrained. The notes field is the highest-leverage thing in a submission.

Include:
- **A working demo account** with credentials, pre-populated with real-looking data. An empty account makes the app look non-functional.
- **A short walkthrough** — "Tap X, then Y, to reach the feature described in the release notes."
- **A video** for anything hardware-dependent, hard to reach, or dependent on a real-world condition.
- **An explanation for anything unusual** — why you need a permission, why a feature is region-limited, what an entitlement is for.
- **For AI features:** what model runs where, what content it can produce, and what guardrails exist. This preempts the age-rating and UGC questions.

Do not include arguments about guidelines. Include facts that make approval easy.

## StoreKit 2

Modern, `async/await`-based, `Transaction.currentEntitlements` for entitlement checks, `Transaction.updates` for a listener, and server-side `App Store Server API` + `App Store Server Notifications V2` if you have a backend.

- **Verify on-device or on your server**, not by trusting a local flag. `VerificationResult` gives you the signed payload.
- **Restore purchases** must exist and work. Reviewers test it.
- **StoreKit Testing in Xcode** with a local `.storekit` configuration lets you test the whole matrix without sandbox flakiness. Use it.
- **Offer codes, promotional offers, win-back offers** exist and are underused; they're the cheapest retention levers available.
- **RevenueCat** is worth it for most indie apps — server infrastructure, cross-platform entitlements, and analytics you would otherwise build. The cost is a dependency in your revenue path.

## Commission and programs

- **Standard commission: 30%.**
- **App Store Small Business Program: 15%** for developers under $1M in annual proceeds. Enroll — there is no downside for a small developer, and as of iOS 27 it also gates **free Private Cloud Compute access** for apps under 2M lifetime first-time downloads.
- **Subscription year 2+: 15%.**
- **China: 25% standard / 12% Small Business** since March 2026.
- **EU:** alternative distribution, alternative payments, and the Core Technology Commission regime. Only relevant if you actually distribute outside the App Store in the EU; for most indie developers it is noise.

## Regional compliance

Relevant if you ship to Turkey or the EU:

- **Turkey** — Rekabet Kurumu's 2023 decision permits steering users to alternative payment methods, which in principle lowers commission exposure. In practice this is constrained by Apple's own policies and is not a reliable plan for an indie app. Turkey's digital services tax on App Store sales dropped from 7.5% to 5% in January 2026. Apple adjusts Turkish prices for FX regularly (e.g. November 2025) — but **subscription prices are never auto-adjusted**; you must update those manually.
- **EU** — DSA trader status is mandatory. GDPR applies. DMA changes the distribution and payment landscape.
- **US states** — App Store Accountability Laws (e.g. Texas SB2420) add consent requirements for apps distributed there.

## Handling a long review or a rejection

**Long review (over a week with no movement):** this is usually a queue or an unstated concern, not a decision. Open a Developer Support ticket that is specific — app name, Apple ID, submission date, build number, what the app does in one sentence, and a direct question. Vague "please help" tickets get vague responses. Do not resubmit the same build; it resets your position.

**Rejection:** read the actual guideline number cited, not the summary text. Reply in Resolution Center with either (a) the change you made, or (b) a factual explanation of why the guideline does not apply, with evidence. Appeals to the App Review Board exist for genuine misapplications and are worth using when you are actually right — but only after the Resolution Center conversation.

**Rejections are usually specific and fixable.** The trap is guessing at the cause and shipping three speculative fixes; ask the reviewer what specifically triggered it if the message is ambiguous.
