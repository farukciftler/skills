# Audit, Instrumentation and Validation

Contents: 1 the audit procedure · 2 scoring rubric · 3 leak diagnosis · 4 event taxonomy · 5 funnel design · 6 validation methods · 7 the audit report format.

---

## 1. Audit procedure

Run in this order. The order matters — auditing screens before knowing the success event produces a list of opinions rather than a list of leaks.

1. **Establish the success event.** One instrumented event that means the flow worked. If the team can't name it, that's finding #1.
2. **Reconstruct the actual flow**, including every entry point. Not the flow in the design file — the flow in the build. Screenshots, a screen recording, or the app itself.
3. **Pull the funnel** if data exists: step-to-step conversion, time between steps, drop-off by platform / OS version / device class / locale / acquisition source. If data doesn't exist, that's finding #2, and the audit becomes qualitative.
4. **Walk it cold**, as a new user, on a real device, one-handed, on a slow connection. Then walk it as a returning user, and as a user who denied every permission.
5. **Run the edge-state matrix** (`01-flow-primitives.md` §3) against every step.
6. **Score against the rubric** below.
7. **Rank leaks by estimated impact × confidence ÷ effort.** Estimate the impact in users or revenue, not in severity adjectives.
8. **Write the report** (§7), leading with the three things worth doing this sprint.

---

## 2. Scoring rubric

Score each dimension 0–3. Be honest — an inflated score makes the audit useless. Anything at 0 or 1 belongs in the report regardless of estimated impact.

| # | Dimension | 0 | 3 |
|---|---|---|---|
| 1 | **Goal clarity** | User can't tell what this flow is for | Purpose obvious within one screen; single named success event |
| 2 | **Step economy** | Steps and fields exist for internal reasons | Every step earns its place; nothing asked that could be inferred or deferred |
| 3 | **Value ordering** | Asks (signup, permission, payment) precede any value | Value demonstrated before every ask |
| 4 | **Platform fidelity** | Custom navigation, wrong gestures, non-native pickers | Fully conventional; deviations justified |
| 5 | **Reachability** | Primary actions in top corners; targets under minimum | Primary actions in thumb zone; ≥44pt/48dp throughout |
| 6 | **State coverage** | Only happy path designed | All 17 matrix rows designed and built |
| 7 | **Error recovery** | Dead ends, generic messages, lost input | Specific, actionable, input preserved, retry works |
| 8 | **Persistence** | Work lost on interruption | Drafts autosaved; step, scroll and field state restored |
| 9 | **Latency handling** | Spinners and unexplained waits | Optimistic UI, skeletons, streaming, cancellable long tasks |
| 10 | **Copy** | Jargon, blame, vague | Plain, specific, in the user's voice and language |
| 11 | **Accessibility** | Fails contrast, Dynamic Type, screen-reader order | WCAG 2.2 AA behaviours verified with a real screen reader |
| 12 | **Ethics/compliance** | Dark patterns present; cancellation harder than signup | Symmetric consent; honest urgency; compliant deletion and cancellation |
| 13 | **Instrumentation** | Can't measure the funnel | Every step and failure reason instrumented and consented |
| 14 | **Re-entry** | Deep links and pushes land on the wrong screen | Every entry point hydrates correctly and preserves intent |

Totals: **0–20** structurally broken, rebuild the flow. **21–31** working but leaking; targeted fixes will pay. **32–37** solid; optimise at the margin. **38–42** ship it and go find a worse flow.

---

## 3. Leak diagnosis

When a funnel shows a drop, work through the causes in this order — teams routinely jump to copy when the cause is technical.

| Symptom | Check first | Common actual cause |
|---|---|---|
| Big drop at step 1 | Store listing vs first screen | Expectation mismatch from the listing or ad creative |
| Drop between two adjacent steps | Latency and error rate at that step | A slow or failing API call, not the design |
| Drop concentrated on one platform | OS version, device class | A layout bug on small screens, or an SDK failing |
| Drop concentrated in one locale | Text expansion, translated CTAs | Truncated button, missing translation, wrong keyboard |
| Drop concentrated on new users | Empty state | Nothing to do after arriving |
| Users complete but never return | Activation vs habit | The flow succeeded once; there's no recurring value moment |
| High completion, high refunds | Paywall clarity | Charge terms weren't understood — a compliance risk too |
| Funnel looks worse with no design change | Crash-free rate, ANR, cold start | A performance regression reads as a UX regression |
| Users abandon and return later at step 1 | Persistence | Interruption destroying state, so they restart |

Always separate **won't** from **can't**. Drop-off from a deliberate decision (saw the price, declined) is a different problem from drop-off from failure (couldn't type the address). Session replay distinguishes them faster than any funnel chart.

---

## 4. Event taxonomy

Specify the taxonomy with the flow, not after it.

**Naming:** `snake_case`, all lowercase, `object_action` order with present-tense verbs — `checkout_started`, `paywall_viewed`, `permission_granted`. Never mix casing; tools treat names as case-sensitive and will silently split one action into two events. Agree a platform-neutral screen-naming convention *before* instrumentation or the cross-platform funnel breaks.

**Structure per flow:**

```
<flow>_started          { entry_point, variant }
<flow>_step_viewed      { step_index, step_name }
<flow>_step_completed   { step_index, step_name, duration_ms }
<flow>_failed           { step_name, reason, error_code }
<flow>_abandoned        { step_name, last_action }
<flow>_completed        { duration_ms, variant, path }
```

Failure reason is a **property**, not a separate event name — otherwise the event count explodes and the funnel can't aggregate.

**Rules:**
- 15–30 well-chosen events for most apps. Firebase's free tier caps at 500 distinct names and 25 properties per event, and silently drops beyond it.
- Never track pure UI chrome (`back_button_tapped`, `menu_opened`) unless a specific question needs it.
- Never put dynamic values in event *names*; they belong in properties.
- Maintain an event dictionary as a single source of truth (Confluence, Notion, a README) — definition, owner, properties, and which dashboard consumes it.
- Migrations: ship the new event alongside the old, run both for a transition period, then retire the old one.
- Validate schemas in CI. Malformed events corrupt reports quietly.
- **Consent gating.** Under GDPR/KVKK, events collected before the consent decision may not be storable. Configure delayed SDK initialisation or a default-off state; a consent banner that loads after the SDK is a compliance defect, not a sequencing quirk.
- Retire anything nobody has opened in 30 days.

---

## 5. Funnel design

- **Funnels are step-ordered, cohorted, and windowed.** State the window explicitly (Day 0, Day 7, Day 35) — an unwindowed funnel is uncomparable to any benchmark.
- **Instrument the denominator you actually care about.** Download→activation and session-start→activation answer different questions.
- **Segment by:** platform, OS version, device tier, locale, acquisition source, new vs returning, and permission state. Aggregate funnels hide the leak that matters.
- **Pair each funnel with a guardrail:** crash-free sessions, cold start time, ANR rate, support ticket volume, refund rate. A conversion win bought with a stability loss isn't a win.
- **Time-between-steps** is as diagnostic as conversion. A step users complete slowly is a step they're struggling with even if they eventually pass it.

---

## 6. Validation methods

Choose by the question, not by habit.

| Question | Method | Notes |
|---|---|---|
| Where do people get stuck? | Moderated usability testing, 5–8 participants, their own device, realistic context | Catches most severe issues. In-context (couch, commute) beats lab |
| Is this step harder than that one? | Single Ease Question (1–7) after each task | Cheap, comparable over time |
| Which of two flows converts better? | A/B test | Needs traffic and a pre-registered primary metric; don't peek |
| What are people actually doing? | Session replay + funnel | Replay explains what the funnel can only locate |
| Is the copy understood? | 5-second test / comprehension test | Especially for permission primers and pricing |
| Is the IA right? | Tree test, card sort | Do this before drawing screens, not after |
| Does it work for screen-reader users? | Manual pass with VoiceOver and TalkBack | Automated scanners catch a minority of real issues |
| Does it survive the real world? | Dogfooding on a slow connection, old device, largest Dynamic Type | The cheapest high-yield test there is |

For an A/B test on a flow, define up front: primary metric, minimum detectable effect, run length, guardrails, and what you'll do if it's flat. Flow tests need longer runs than UI tests because the effect propagates into retention.

---

## 7. Audit report format

Use this structure. Lead with what to do, not with what you observed.

```markdown
# [Flow name] — UX Flow Audit
**Scope:** [platforms, app version, date, what was and wasn't examined]
**Success event:** [the one event]
**Current performance:** [funnel numbers, or "not instrumented — see F0"]

## Do these three things first
1. [Fix] — [expected impact] — [effort] — [how we'll know]
2. …
3. …

## Score
[Rubric table, 14 dimensions, 0–3, with total and band]

## Findings
### F1 — [Title]  ·  Impact: High  ·  Effort: S  ·  Confidence: High
**Where:** step 3, permission primer
**What happens:** [observed behaviour]
**Why it costs:** [mechanism, with evidence or benchmark]
**Fix:** [specific and buildable]
**Measure:** [event/metric and target]

[… findings ranked by impact × confidence ÷ effort …]

## Edge-state coverage
[Matrix table: which of the 17 conditions are designed, built, both, or neither]

## Instrumentation gaps
[Events missing to diagnose this flow]

## Compliance notes
[Accessibility, consent, store guidelines, dark-pattern exposure]

## Out of scope / open questions
```

Findings that amount to taste, say so and mark them low priority. An audit that mixes "the button is the wrong blue" with "users lose their work when a call comes in" gets ignored wholesale.
