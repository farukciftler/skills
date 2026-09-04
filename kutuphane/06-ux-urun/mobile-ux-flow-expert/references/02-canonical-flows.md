# Canonical Flows

Contents: 1 first-run/onboarding · 2 authentication · 3 permissions · 4 paywall & trial · 5 checkout & payment · 6 search & browse · 7 content creation · 8 notifications & re-engagement · 9 settings, account & deletion · 10 offboarding & cancellation · 11 AI and agentic flows · 12 cross-cutting: sheets, forms, destructive actions.

Each section gives the recommended shape, the decision points that actually matter, and the failure modes.

---

## 1. First-run experience and onboarding

The highest-leverage flow in the app. Activation predicts long-term retention better than store conversion or ad spend, and for half of all products 98% of new users are gone by Day 14.

**Shape that works for most consumer apps:**

```
Cold launch
  → [optional] 1–3 value screens, skippable, no auto-advance
  → sample the product (browse/preview/demo with no account)
  → personalisation only if it changes what the user sees next
  → the aha action (the success event)
  → contextual account creation ("save this")
  → permission soft-ask tied to a benefit just demonstrated
  → paywall (timing per §4)
```

**Decision points:**

- **Value screens: how many, and do they exist?** Justified only when the product's value isn't self-evident from the first screen. Three maximum, skippable, dots visible, no forced dwell time. If you can't write three screens that each say something non-obvious, ship one or none.
- **Signup placement.** Deferring signup until after the user experiences value typically lifts activation meaningfully. The cost is engineering: you need anonymous state that migrates cleanly to an account. If you can't migrate the state, don't defer — losing a user's first creation at the auth wall is worse than asking up front.
- **Personalisation quiz.** Only ask what visibly changes the next screen. A quiz whose answers don't alter anything trains users that your questions don't matter, and answers given to get past a wall are noise in your data. The legitimate version (used by Wayfair, Etsy, Depop-style apps) seeds the first feed.
- **Progressive profiling.** One or two data points per session across weeks beats a 15-field signup, which is a documented drop-off generator.
- **Empty state as onboarding.** For apps where the first screen is legitimately empty (notes, tasks, trackers), the empty state *is* the onboarding: explain, seed with a sample, offer one action.
- **Skip.** Always available, always visible, never a low-contrast afterthought — hiding skip is a dark pattern and it depresses Day-1 retention anyway.

**Instrument:** `onboarding_started`, one event per step, `onboarding_completed`, `onboarding_skipped` with `step_index`, and the activation event itself. The step-to-step funnel is the deliverable.

**Failure modes:** onboarding that ends in an empty app; carousels nobody reads; asking for permissions and payment in the first 20 seconds; personalisation that personalises nothing; a "quick tour" of coach marks that users dismiss without reading (teach in context, at the moment of use, instead).

---

## 2. Authentication

**2026 default stack:** passkey-first for returning users, with email OTP or magic link for initial onboarding before a passkey exists, plus social sign-on (Apple/Google) as a low-friction entry. SMS OTP is fallback-only — NIST SP 800-63B rev. 4 deprecates SMS for AAL2 and SIM-swap losses are well documented.

**Why it matters to the flow, not just security:** social sign-on typically converts far better than email+password on the first screen. Kayak reported roughly 50% faster sign-in and 4x fewer sign-in errors after passkeys. But every case study measures lift *after enrollment* — the real design problem is enrollment, and passkey adoption stalls at 5–10% without device-aware prompting.

**Shape:**

```
Identifier-first screen (email or phone)
  → system detects existing passkey → biometric prompt → done
  → no passkey → OTP / magic link → session
  → immediately after first successful sign-in, offer passkey enrollment
     with a concrete benefit ("sign in with Face ID next time"), skippable
```

**Rules:**

- **Identifier-first**, not email+password on one screen. Lets you route to the right method per user.
- **Fallback always visible without scrolling.** A failed passkey attempt with no visible alternative is a support ticket.
- **Never dead-end.** Every auth screen needs a route to recovery.
- **Preserve intent.** If auth interrupts a flow (deep link, checkout), return to the exact step with the input intact. This is the single most-skipped requirement in auth specs.
- **Label credentials human-readably** in account settings — "iPhone 15 (added March 2026)", not a credential ID.
- **Sign in with Apple** is required by App Store guidelines when you offer other third-party social logins on iOS.
- **Anonymous → account migration** must be defined explicitly: what carries over, what happens on conflict when the email already has an account.

**Failure modes:** QR-code cross-device handoff shown with no explanation (a top passkey support-ticket category); password requirements revealed only after submission; OTP screens that don't auto-read the code from SMS/clipboard; magic links opening in a different browser than the app's session; sign-out that doesn't clear cached PII.

---

## 3. Permission flows

The structural rule: **the OS prompt is a one-shot resource. Protect it with a soft-ask you control.**

```
value moment occurs
  → in-app primer (bottom sheet): one concrete benefit + "Enable" / "Not now"
  → "Enable" → native OS prompt
  → "Not now" → dismiss, never fire the OS prompt, re-ask at a later value moment
```

Priming can lift push opt-in 2–3x. Firing the native prompt on first launch is the single biggest mistake apps make.

**Primer copy rules:**
- One specific benefit, not a list. "We'll tell you when your order ships" beats "Get updates, reminders and personalised tips."
- User-controlled framing: "Want to hear when…" over "Enable notifications."
- Show a mock of what they'll receive where possible.
- Never guilt ("Are you sure you want to miss out?") — confirmshaming is squarely in dark-pattern territory under DSA Art. 25 and the coming DFA.

**Per-permission timing:**

| Permission | Ask when | Never |
|---|---|---|
| Notifications | After first completed value action, or session 2–3 | First launch |
| Location (when-in-use) | User taps something that needs it ("near me") | On launch; asking for Always before When-in-Use |
| Camera / photos | User taps the camera/attach control | Preemptively at onboarding. Prefer the limited-library picker where it suffices |
| Contacts | Only if the core feature is social graph, with a clear statement of what you upload | Ever, for "growth" alone — this is a trust cliff |
| ATT (iOS tracking) | After the user understands the app, with an honest pre-prompt about what it enables | Before any context. Note the pre-prompt cannot bribe or mislead per Apple's rules |
| Health / financial data | At the moment the feature is used, with a data-handling statement | Bundled with other asks |

**Denied state is a design surface.** Define what the app does without the permission, how it tells the user what's degraded, and where the "turn this on in Settings" affordance lives — offered on the second contextual attempt, not immediately after the denial.

---

## 4. Paywall, trial and monetisation flows

The 2026 evidence base (RevenueCat SOSA 2026: 115,000+ apps, $16B revenue, 1B+ transactions) reshaped the defaults:

- **Hard paywall vs freemium:** median Day-35 download→paid is **10.7%** hard paywall vs **2.1%** freemium — roughly 5x. Revenue per install at Day 60 is ~8x higher. One-year retention of yearly subscribers is essentially the same (27% vs 28%), so the "hard paywalls destroy retention" argument doesn't survive the data.
- **Day 0 dominates.** ~50% of paid conversions happen on Day 0. Onboarding *is* the monetisation flow.
- **Trials are cancelled instantly.** 55.4% of 3-day trial users cancel on Day 0; ~84% of 3-day trial cancellations happen by end of Day 1. 7-day trials: ~39.8% cancel Day 0.
- **Platform gap is a funnel-entrance problem, not a trial problem.** Median Day-35 download→paid: iOS 2.6%, Android 0.9% — yet Android trial→paid is 32.5%. The Android leak is upstream of the trial.
- **Price tier:** high-priced apps convert downloads ~2x better than low-priced (2.8% vs 1.4% median). Higher prices filter for intent.
- Short trials are trending: apps using trials of ≤4 days rose from 42.1% to 46.5% year over year.

**Do not read these as "always use a hard paywall."** They're medians across categories; a hard paywall suppresses the top-of-funnel volume that word-of-mouth and content-driven growth need. The honest framing: hard paywall optimises revenue per install, freemium optimises reach. Pick according to which constraint binds.

**Paywall flow anatomy:**

1. Context established first — the paywall lands after the value moment, not before it. A paywall shown before context "feels jarring" and converts worse.
2. One screen, one decision. Plan selection visible without scrolling; the recommended plan visually distinct but not deceptive.
3. **Price, period, and renewal terms in plain language, above the fold.** Not in a footer. This is both conversion and compliance.
4. Restore purchases visible (required by App Store review).
5. Close affordance genuinely tappable — hidden or delayed X buttons are a classic dark pattern and an App Review rejection reason.
6. Post-purchase: immediate, unmistakable confirmation of what they now have and when they'll be charged.

**Trial design:** state the charge date explicitly, and send a reminder before it. Trial-reminder emails/notifications reduce refund requests and involuntary churn complaints far more than they reduce conversion.

**Billing health is a UX surface.** A meaningful share of Play Store cancellations trace to billing failure rather than deliberate rejection. Grace periods, in-app "fix your payment method" prompts, and account-hold states belong in the flow spec.

---

## 5. Checkout and payment

Baymard's research is the evidence base and it's remarkably stable:

- ~39–48% of abandonments involve unexpected extra costs surfacing late.
- ~19% abandon because account creation was required (guest checkout is not optional).
- ~18% abandon because the process felt too long or complicated.
- Average checkout ships ~11.3 form fields across ~5.1 steps; 7–8 fields is achievable. Completion drops ~4–6% per field beyond the eighth.

**Mobile-specific rules:**

- **Wallets first.** Apple Pay / Google Pay above the traditional form, not below it. On mobile this is the single largest lever.
- **Total cost visible from the first checkout screen** — shipping, tax, fees. No surprises at step 4.
- **Progress indicator** with honest step counts.
- **Correct keyboard per field** (`email`, `tel`, `numeric`) and correct `autocomplete`/`textContentType` tokens. Never disable autofill wholesale; use specific tokens instead.
- **Address autocomplete** and postal-code lookup — typing an address on a phone is the worst part of any checkout.
- **Inline validation on blur**, never on every keystroke, never only at submit. Keep the user's input on error.
- **No steps within steps.** A modal inside a checkout step is a documented abandonment cause.
- **One-handed reachability:** the primary "Pay" button in the bottom third, full-width, and never adjacent to a destructive control.
- **Never lose the cart** on session expiry, backgrounding, or auth interruption.

---

## 6. Search, browse and filtering

- **Zero-state does work:** recent searches, popular queries, or categories. A blank search screen wastes the highest-intent moment in the app.
- **Query-as-you-type** with debounce; show what's being searched.
- **Zero-results state must echo the query**, offer to clear filters individually (not just "clear all"), and suggest corrections or adjacent results. This is the most commonly neglected screen in mobile apps.
- **Filters as a sheet**, with applied count visible on the trigger, individually removable chips, and an explicit Apply when the result set is expensive to compute.
- **Preserve scroll position and filter state** on back navigation from a detail screen. Losing the user's place in a list after they tap through and return is a top-tier frustration and trivially avoidable.
- **Sort and filter are different things** and users conflate them; label them explicitly.

---

## 7. Content creation and multi-step input

The flow where "losing work" complaints concentrate. Mobile form abandonment is frequently cited around 80% (directional — the underlying methodology varies), and the pattern behind it is consistent: a user starts, gets interrupted, returns to a blank form.

Non-negotiables:
- **Autosave drafts locally** on every meaningful change, not on submit.
- **Restore field values, scroll position, and step index** after backgrounding.
- **Confirm before discarding** anything the user typed; offer "Save draft" as the middle option.
- **Optimistic UI with rollback** for posts/comments; show pending state, never a blocking spinner.
- **Upload resilience:** background upload, retry, per-item progress, and the ability to leave the screen.

---

## 8. Notifications and re-engagement

Push opt-in is the multiplier on every retention campaign: roughly 43–54% on iOS versus 81–91% on Android (Android historically defaulted on pre-Android 13, so its number is falling).

- **Every notification must deep-link to the exact relevant state**, hydrated. A push that opens the home screen is a broken flow and trains users to ignore you.
- **Notification settings inside the app**, per-category, before users go find the OS-level nuclear option.
- **Frequency and quiet hours** respected; behavioural triggers outperform scheduled blasts.
- The EU's direction of travel (Parliament's 2023 addictive-design resolution, and the forthcoming DFA) explicitly names constant push notifications, infinite scroll, autoplay and streak mechanics that penalise breaks. Design retention loops that survive that scrutiny.

---

## 9. Settings, account management and deletion

- **In-app account deletion is mandatory** on iOS for any app supporting account creation (App Store Review Guideline 5.1.1(v), enforced since 30 June 2022). It must be *initiable in the app* — not "email support". Play has an equivalent requirement including a web-accessible route.
- Deletion flow: explain what's deleted vs retained (and legal retention periods), offer the lighter alternatives (deactivate, export data, unsubscribe) *once* without burying deletion, require an explicit confirmation, then confirm completion and sign out.
- **Data export** belongs next to deletion (GDPR/KVKK portability).
- **Subscription management** must be reachable in-app, linking to the platform's management surface where applicable.
- **Privacy/consent controls** must be as easy to reverse as they were to grant — asymmetry here is the textbook regulator example.

---

## 10. Offboarding and cancellation

Now a legal surface as much as a design one. The FTC's click-to-cancel rule was vacated in July 2025 and reopened via ANPRM in March 2026, but ROSCA and 30+ state auto-renewal statutes still require that cancellation be as simple as sign-up. The EU DFA is expected to target subscription and cancellation traps directly.

Design it as a genuine flow, not a wall:
- Cancellation reachable from account settings within two taps.
- **One** retention offer maximum, honestly framed, with a clearly equal-weight "Continue cancelling".
- No phone-call requirement, no retention gauntlet, no confirmshaming copy.
- Confirm what happens: access until date X, data retained for Y days, how to come back.
- Exit survey optional and after cancellation is confirmed — never as a gate.

Peak-end rule applies: a clean cancellation is a meaningful share of winback conversions later.

---

## 11. AI and agentic flows

Design patterns that are now baseline expectations:

- **Streaming output** rather than a spinner for anything over ~2s — perceived wait drops sharply even when total time is identical.
- **Visible stop control** that actually cancels the request.
- **Buffer incomplete markdown/code** during streaming; render text immediately, defer code blocks until the closing fence.
- **Confidence and provenance signals** — citations, source links, "AI draft" labels. Layer them: available on demand, hidden by default, so users who trust the answer move on and users who want to verify can drill down.
- **Three designed states per AI feature: success, degraded, failure.** Degraded is the one teams skip — what the feature does when the model is slow, rate-limited, or offline. For on-device models, degraded includes "model not downloaded" and "device unsupported".
- **Capability transparency before input** — users should be able to tell what the assistant can and can't do before typing. Suggested prompts do this better than a help screen.
- **Undo and override on anything the AI changes**, plus a one-sentence "why you're seeing this" for adaptive UI. Silent interface rearrangement drew distrust in early-2026 implementations; the pattern that stuck pairs every adaptive change with a visible reason and a one-click reset.
- **Agentic actions** need planning visibility, tool-use disclosure, per-step override, and an explicit confirmation gate before anything irreversible (payment, send, delete).
- **Accessibility:** announce streamed content via live regions; long AI responses need heading structure, not one undifferentiated block.

The ethical line: personalisation that adapts to a user is a feature; personalisation that exploits an inferred vulnerability is what the DFA is being written to prohibit.

---

## 12. Cross-cutting patterns

**Sheets and modals.** Use for self-contained tasks that interrupt the main flow. On iOS 26, pair the glass with dimming for interrupting tasks, and use detents so the user retains context. Never nest modals. Always provide both an explicit close and swipe-to-dismiss, and confirm dismissal if data would be lost.

**Forms.** One column. Labels above fields (not placeholders-as-labels — they vanish on focus and break screen readers). Mark optional rather than required when most fields are required. Group with the law of proximity. Show the keyboard type that matches the input. Keep the submit button visible above the keyboard.

**Destructive actions.** Confirm only when genuinely irreversible; otherwise prefer undo via a snackbar/toast — it's faster and less annoying. Never place destructive controls adjacent to primary ones, and never make the destructive option the visually dominant one (nor the reverse, if that's what the user actually asked for).

**Progress and waiting.** Under 400ms: nothing. 400ms–2s: skeleton matching final layout. Over 2s: meaningful progress with cancellation. Over 10s: let the user leave and notify on completion.

**Errors.** Say what happened, why if you know, and what to do next. Preserve the user's input. Give a retry that actually retries. Never show a raw code without human text, and never blame the user.
