# Compliance and Ethics

Contents: 1 accessibility · 2 the dark pattern catalogue · 3 the regulatory map · 4 consent and tracking · 5 minors and vulnerability · 6 the practical test.

Design ethics used to be an argument about taste. In 2026 it's an argument about exposure. Treat this file as flow requirements, not as a legal appendix.

---

## 1. Accessibility

**Status.** The European Accessibility Act has been enforceable since **28 June 2025**, covering private-sector products and services including e-commerce, banking, telecoms, e-books and consumer electronics — B2C and B2B, and non-EU companies selling into the EU. The harmonised standard is **EN 301 549**; v3.2.1 incorporates **WCAG 2.1 AA** and is today's benchmark. **v4.1.1, incorporating WCAG 2.2, is expected during 2026** — design to 2.2 now. EN 301 549 Chapter 11 covers non-web software, i.e. mobile apps, specifically. Enforcement has been ramping through 2026 (the Dutch ACM and Swedish PTS are the visible early movers). Contracts concluded before June 2025 must comply by June 2027.

**Flow-level requirements** — the ones that actually get failed:

| Requirement | What it means in a flow |
|---|---|
| Focus order | Screen-reader traversal follows visual order; after a transition, focus lands on the new screen's heading, not back at the top of a stale view |
| Focus visibility (WCAG 2.2) | Keyboard/switch focus indicator always visible and not obscured by sticky bars or the keyboard |
| Target size (WCAG 2.2 SC 2.5.8) | ≥24×24 CSS px minimum; platform minima (44pt iOS / 48dp Android) are the real target |
| Dragging alternatives (WCAG 2.2) | Any drag interaction needs a single-pointer alternative |
| Consistent help (WCAG 2.2) | Help/support in the same relative place across screens |
| Redundant entry (WCAG 2.2) | Don't ask for information the user already supplied earlier in the flow |
| Accessible authentication (WCAG 2.2) | No cognitive-function test (puzzle, transcription) without an alternative. Passkeys and password-manager paste support satisfy this; blocking paste in an OTP field violates it |
| Contrast | 4.5:1 body text, 3:1 large text and UI components — verify translucent surfaces (iOS 26 glass) against real content, light and dark |
| Not colour alone | Error, selected, and required states need a second signal |
| Dynamic Type / font scale | Flow completes at the largest accessibility size without truncation or trapped buttons |
| Reduced motion / transparency | The flow is fully usable and legible with both enabled |
| Labels and roles | Every control has an accessible name; icon-only buttons especially |
| Timeouts | Warn and allow extension |
| Captions and alternatives | Media in onboarding needs captions and a text alternative |

**Process:** automated scanners catch a minority of real issues. A manual pass with VoiceOver and TalkBack through the whole flow is the minimum bar. An accessibility statement is a separate administrative obligation under the EAA.

**The commercial argument, since it always comes up:** every accessibility fix in this list is also a usability fix for people in sunlight, on a train, one-handed, or tired. There is no version of "accessible" that costs conversion.

---

## 2. Dark pattern catalogue

Named patterns, what they look like in a mobile flow, and what to do instead. The FTC's *Bringing Dark Patterns to Light* (2022) and the EU Commission's fitness check are the reference taxonomies; a 2022 Commission study found **97% of popular EU websites and apps used at least one dark pattern**, with estimated consumer harm of at least **€7.9bn/year**.

| Pattern | In a mobile flow | Instead |
|---|---|---|
| **Roach motel** | Easy signup, cancellation buried or phone-only | Cancellation as easy as signup, two taps from settings |
| **Confirmshaming** | "No thanks, I don't want to save money" | Neutral decline copy of equal weight |
| **Preselection** | Pre-ticked marketing consent, pre-selected priciest plan | Nothing pre-ticked that has a cost or a consent implication |
| **Hidden costs / drip pricing** | Fees revealed at the final step | Full total on the first checkout screen |
| **False urgency / scarcity** | Fake countdowns, "only 1 left" that never changes | Real deadlines only, or none |
| **Visual interference** | Decline button low-contrast, tiny, or off-screen | Equal visual weight for accept and decline |
| **Nagging** | Rating prompt or permission ask on every launch | Rate-limited, contextual, with a real "don't ask again" |
| **Forced continuity** | Trial auto-converts with no reminder | Pre-charge reminder; visible charge date at signup |
| **Trick wording** | Double negatives in consent toggles | One idea, positive phrasing, per toggle |
| **Obstruction** | Multi-screen retention gauntlet before cancel | One offer maximum, then straight through |
| **Sneak into basket** | Add-ons defaulted on | Opt-in, itemised |
| **Disguised ads** | Ad styled as a system alert or app content | Clear labelling and visual separation |
| **Privacy zuckering** | Consent granted in one tap, withdrawal takes six | Symmetric: same number of taps to grant and to revoke |
| **Hard-to-close paywall** | Delayed or invisible X | Immediately tappable close of adequate size |
| **Addictive mechanics** | Streaks that punish breaks, infinite scroll, autoplay by default, notification pressure | Streak freezes, session boundaries, autoplay off by default, digest notifications |

The EU Parliament's 2023 addictive-design resolution explicitly named infinite scrolling, default autoplay, constant push notifications and read receipts as candidates for prohibition. Retention loops built on those mechanics are building on sand.

---

## 3. Regulatory map (as of July 2026)

**EU**
- **DSA Article 25** — in force since 2024. Bans online platform interfaces that deceive, manipulate, or materially distort users' ability to make free and informed decisions. Applies to platforms; VLOPs carry additional obligations including mitigating addictive-design risks and a ban on personalised ads to minors.
- **UCPD** — the general unfair-commercial-practices baseline that already covers most dark patterns; Annex I is the blacklist.
- **Digital Fairness Act** — Commission proposal expected **Q4 2026** (part of the 2030 Consumer Agenda adopted 19 Nov 2025). Scope: dark patterns, addictive design, unfair personalisation and personalised pricing, influencer marketing, in-game currencies, and **subscription/cancellation traps** — with particular attention to minors. Not yet law; adoption is years away. Design for it now anyway; the direction is unambiguous.
- **GDPR** — consent must be freely given, specific, informed, unambiguous, and as easy to withdraw as to give. Consent obtained through manipulative design is not valid consent.
- **EAA / EN 301 549** — §1 above.
- **AI Act** — transparency obligations where users interact with an AI system; high-risk obligations phasing in from August 2026.

**US**
- **FTC click-to-cancel (Negative Option Rule, 2024)** — **vacated by the 8th Circuit in July 2025** on procedural grounds. The FTC reopened the question with an **ANPRM on 11 March 2026**. Meanwhile **ROSCA**, **FTC Act §5**, and **30+ state automatic-renewal statutes** remain fully enforceable, and enforcement history (Amazon, Adobe, Vonage — $100M in refunds) is instructive. Practical guidance is unchanged: make cancellation as easy as signup, disclose materially before taking billing information, obtain unambiguous affirmative consent, and retain proof.
- **State privacy laws** increasingly treat dark-pattern consent as invalid consent.

**Türkiye**
- **KVKK** — consent and transparency obligations broadly parallel to GDPR; explicit consent must be specific and freely given. Data localisation and transfer rules affect where flow telemetry can go.
- Consumer protection law (Tüketicinin Korunması Hakkında Kanun) covers distance contracts, pre-contractual disclosure and withdrawal rights — relevant to subscription and checkout flows.
- Apps serving EU users are in EAA and DSA scope regardless of where the company sits.

**Platform rules** — Apple and Google enforce a subset of the above directly through review (account deletion, purchase disclosure, restore, data safety). See `03-platform-rules.md` §5. In practice App Review is the fastest-acting regulator most teams meet.

---

## 4. Consent, tracking and ATT

- **Sequence matters.** The consent decision must precede analytics/attribution SDK initialisation, or you're storing data you had no basis to store. Configure delayed init or default-off.
- **ATT pre-prompts are permitted but constrained** — they may not offer incentives, mislead about what tracking does, or imply the app won't work without it. An honest pre-prompt that states the actual benefit is both compliant and the reason education-category opt-in roughly doubled between 2023 and 2025.
- **Symmetry test for any consent surface:** count the taps to accept and the taps to reject. If they differ, that asymmetry is the finding.
- **Granularity:** bundle nothing. Marketing consent, personalisation consent, and functional permissions are separate decisions.
- **Re-consent** when purposes change materially. Silence is not consent.

---

## 5. Minors and vulnerability

If under-18s plausibly use the app, this is not optional.

- No personalised advertising to minors (DSA).
- Age-appropriate defaults: strictest privacy settings on by default, geolocation off, profile non-discoverable.
- No engagement mechanics designed to maximise time-on-app for minors — this is the DFA's most explicitly telegraphed target.
- Spend controls and clear, non-obfuscated in-app currency pricing (soft currencies that hide real cost are named in the DFA scope).
- Apple's Kids Category and Google's Families policy impose their own flow requirements — parental gates before external links, purchases, or data collection.

**Vulnerability more broadly:** personalisation that targets a user's inferred financial stress, health condition, or negative emotional state is the specific practice the DFA is being written to prohibit. If a targeting rule would be embarrassing to state out loud to the user it's targeting, don't ship it.

---

## 6. The practical test

Before shipping any step that nudges, defaults, urges, or obstructs, apply these three in order:

1. **The comprehension test.** *Would this still work if the user fully understood what it was doing?* If persuasion depends on the user not noticing, it's a dark pattern.
2. **The symmetry test.** *Is the path out as easy as the path in?* Applies to consent, subscription, notification opt-in, data sharing, and account creation.
3. **The daylight test.** *Would we describe this step, in these words, in a press release or a regulator's questionnaire?* This catches the cases the first two miss.

A step that fails any of the three should be raised in the audit as a finding with a compliance flag, not softened into a style note. Teams push back on ethics arguments and concede to exposure arguments — so frame it as both, honestly: here is the user harm, and here is the regulation it sits under.
