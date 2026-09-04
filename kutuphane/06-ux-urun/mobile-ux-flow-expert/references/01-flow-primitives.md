# Flow Primitives

Contents: flow artifact taxonomy · what a "step" actually contains · the state matrix · Mermaid notation · information architecture and navigation model selection · common structural anti-patterns.

---

## 1. Which artifact, and when

These terms get used interchangeably and it causes real confusion in reviews. Be precise about which one you're producing and say so.

| Artifact | What it shows | Branching | Fidelity | Use when |
|---|---|---|---|---|
| **Task flow** | Linear steps to complete one task, plain language | No | None | Aligning on scope fast; whiteboard-level; a single goal |
| **User flow** | All paths a user might take from entry to goal, including decisions and dead ends | Yes | None/low | Designing a feature; finding unhandled branches |
| **Wireflow** (NN/g) | Wireframe screens joined by flow arrows, annotated with system behaviour | Yes | Low-mid | Apps with few unique screens whose content changes dynamically — i.e. most mobile apps. The default mobile deliverable |
| **Flowchart** | System logic including back-end decisions | Yes | None | Handoff to engineering; auth, sync, payment logic |
| **Screen-flow / prototype map** | Real screens wired in Figma order | Yes | High | Usability testing, stakeholder sign-off |
| **User journey map** | End-to-end experience across touchpoints with emotions, pain points, channels | Cross-channel | N/A | Strategy, not build. Includes pre-install and post-churn |
| **Service blueprint** | Journey plus back-stage actors and systems | Yes | N/A | Flows with human support, logistics, or offline steps |

Rule of thumb: **user flow to decide, wireflow to design, flowchart to build, journey map to argue about strategy.** NN/g's distinction is worth keeping — user flows capture steps and system responses; journey maps contextualise them with thoughts and emotions. Don't put emotions in a user flow; don't put pixel decisions in a journey map.

The best source of real user-flow data is usability testing (watching people actually do it), with analytics — funnels, heatmaps, session replay — as the secondary source. Analytics tells you *where*; watching tells you *why*.

---

## 2. Anatomy of a step

A step in a flow spec is not "a screen". It is a row with these columns. If any is blank, the step isn't specified.

1. **State name** — `signup.email_entry`, `paywall.trial_offer`. Namespaced, stable, matches analytics screen names.
2. **Precondition** — what must be true to arrive here (authenticated? has network? feature flag on?).
3. **What the user sees** — layout, primary/secondary actions, and the actual copy strings.
4. **User actions available** — including "do nothing".
5. **System response per action** — including latency expectation and what shows during it.
6. **Data written/read** — what persists locally vs remotely, and *when* it's saved.
7. **Exits** — forward, back, cancel, escape hatch, timeout, external (deep link out, browser, system settings).
8. **Analytics** — event names fired here and their properties.
9. **Edge states** — the row's answers to the matrix below.

---

## 3. The edge-state matrix

Every step gets checked against every row. Fill it out per flow, not per app; a checkout's offline behaviour is not an onboarding's.

| # | Condition | Design question | Typical default |
|---|---|---|---|
| 1 | **Loading** | What shows between action and result? | Skeleton matching final layout for >400ms; optimistic UI where the action is safe to assume |
| 2 | **Empty** | Zero items, first run, cleared list | Explain why it's empty + one primary action; no bare illustration |
| 3 | **No results** | Search/filter returns nothing | Echo the query, offer to clear filters, suggest alternatives |
| 4 | **Partial** | Some data loaded, some failed | Render what you have; inline retry for the missing part; never block the whole screen |
| 5 | **Offline** | No connectivity | Queue the write, show it as pending, sync later. Never lose input |
| 6 | **Slow** | Request >2s | Progress with meaning ("Uploading 2 of 5"), cancellable |
| 7 | **Validation error** | Bad input | Inline, next to the field, on blur not on keystroke, keep the input |
| 8 | **Server error** | 5xx / unknown | Specific where possible, retry affordance, never a raw code alone |
| 9 | **Permission denied** | User said no | Degrade gracefully; explain what's unavailable; deep link to Settings only after a second, contextual ask |
| 10 | **Auth expired** | Session gone mid-flow | Re-auth in place (sheet), then return to exact step with input intact |
| 11 | **Interruption** | Backgrounded, call, notification | Restore scroll position, field values, and step index |
| 12 | **Back / cancel** | User retreats | Define per step: discard, save draft, or confirm. Destructive discard always confirms |
| 13 | **Deep link mid-flow** | Arriving at step 4 cold | Either hydrate required state or route to the correct start with intent preserved |
| 14 | **Duplicate / re-entry** | User already did this | Idempotent — don't create a second account, order, or subscription |
| 15 | **Locale** | Long strings, RTL, different formats | Layout survives ~35% text expansion; no truncated CTAs |
| 16 | **Accessibility** | Screen reader, Dynamic Type XXL, reduced motion | Logical focus order; nothing conveyed by colour alone; targets ≥44pt/48dp |
| 17 | **Low-end device** | Old phone, low memory | Flow must complete without the animation layer |

A flow that handles rows 1–8 is competent. Rows 9–14 are where apps that feel *solid* separate from apps that feel flimsy — and they are also where App Store reviewers, accessibility auditors, and one-star reviews live.

---

## 4. Mermaid notation

Default to Mermaid `flowchart TD`. Conventions to keep diagrams readable and reviewable:

```
flowchart TD
    Entry([Push notification tap]) --> Check{Signed in?}
    Check -->|Yes| Detail[order.detail]
    Check -->|No| Auth[auth.signin<br/>intent preserved]
    Auth -->|success| Detail
    Auth -.->|cancel| Home[home.feed]
    Detail --> Track[order.tracking]
    Detail -.->|network error| Err[/Retry state/]
    Err -.->|retry| Detail
```

- `([ ])` entry and exit points
- `[ ]` screens/states — use the namespaced state name, not a friendly title
- `{ }` decisions — phrase as a yes/no or enumerated question
- `[/ /]` error or system states
- `-->` primary path, `-.->` error, cancel, or fallback path
- Every edge labelled with the *user action* or *system condition*
- `<br/>` for a short annotation on a node (what's preserved, what's required)

Split when a diagram exceeds ~15 nodes: one diagram per flow, with a named handoff node linking them. A single "everything" diagram is a diagram nobody reads.

For **wireflows**, the same graph structure with each node replaced by a low-fidelity screen sketch plus a numbered annotation list. When producing these in a chat context, an SVG or HTML rendering is usually better than Mermaid.

---

## 5. Choosing the navigation model

The flow's shape is constrained by the app's information architecture. Pick deliberately:

| Model | Fits | Breaks when |
|---|---|---|
| **Tab bar** (2–5 destinations) | Peer sections users switch between constantly | You have 6+ sections, or sections are sequential rather than parallel |
| **Stack / hierarchical drill-down** | Content hierarchies: list → detail → sub-detail | Depth exceeds ~3 levels; users lose their place |
| **Modal / sheet** | Self-contained task that interrupts the main flow | Used for navigation rather than tasks; nested modals |
| **Wizard / stepper** | Genuinely sequential, dependent steps (KYC, checkout) | Steps are independent — then it's just friction |
| **Feed / infinite** | Browse and discovery | The user has a specific target — needs search |
| **Hub and spoke** | Utility apps with unrelated tools | Frequent switching between spokes |
| **Search-first** | Large inventories, no natural hierarchy | Users don't know the vocabulary of the domain |
| **Conversational** | Open-ended intent, AI assistants | The task has a fixed shape a form would do better |

Two structural decisions carry most of the weight:

**Where does the primary action live?** One primary action per screen, in the bottom third, visually unambiguous. If two actions compete for primary, the screen is doing two jobs.

**How deep is the goal?** Count taps from cold launch to the app's core value. If it's more than three for the main job, the IA is wrong, not the flow.

---

## 6. Structural anti-patterns

Name these when you see them; they're the recurring causes of flow-level failure.

- **Screen-list thinking** — designing screens then wiring them, instead of designing states then rendering them. Symptom: no one can say what happens on back.
- **Happy-path-only spec** — the flow "works" in the prototype and falls apart in the field.
- **The blocking wall** — signup, permission, or paywall placed before any value has been demonstrated.
- **Steps within steps** — a wizard that spawns a modal that spawns another wizard. Baymard names this explicitly as a checkout killer.
- **Data-collection creep** — fields added by teams who wanted analytics, never removed.
- **The orphan branch** — an error or empty state that has no way forward except force-quit.
- **The unlabelled decision** — a diagram diamond with unlabelled edges; means the condition was never actually decided.
- **Navigation invention** — a custom gesture or bespoke nav pattern where a platform standard exists.
- **The false progress bar** — "Step 2 of 3" that turns into 5 steps. Destroys trust permanently.
- **Undead state** — the user completes the flow but the app still shows the pre-completion state until relaunch.
