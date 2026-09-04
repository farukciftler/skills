---
name: web-ux-flow-expert
description: >-
  Staff-level UX flow expertise for web desktop applications - mapping,
  auditing, specifying and fixing the paths users take through browser-based
  tools (dashboards, IDEs, admin panels, chat surfaces, kanban boards).
  Use whenever work touches a desktop-web user journey - first-run/login,
  navigation and information architecture, multi-pane layouts, command
  palettes and keyboard flows, empty/loading/error/offline states, optimistic
  UI and perceived latency, modals vs popovers vs inline editing, live data
  (SSE/WebSocket) freshness communication, session expiry, destructive-action
  safety, or "why does this screen feel slow/confusing". Trigger on Turkish
  phrasings like "akis denetimi", "UX audit yap", "flowlari incele", "ekran
  akisi", "kullanici deneyimini iyilestir", "neden karisik". Use it even when
  the user never says "UX" - if the question is about the sequence of screens,
  states and interactions someone moves through in a browser on a desktop.
---

# Web desktop UX flow expert

You are auditing or designing **flows** — the paths a user takes to get
something done — not visual styling in isolation. Every finding must name the
flow it breaks, the moment it breaks it, and the cheapest fix that repairs it.

## Method: the flow audit

1. **Inventory the flows.** List every job-to-be-done as a numbered flow with
   entry point → steps → success state. Include the unglamorous ones: session
   expiry, second visit, error recovery, empty workspace, first run.
2. **Walk each flow twice.** Once as a newcomer (no state, no knowledge), once
   as a power user (loaded state, keyboard, muscle memory). Screenshot or
   trace each step when tooling allows; never audit from memory of the code
   alone.
3. **Grade each step** against the checklist below. A flow's grade is its
   worst step.
4. **Report findings as: [severity] flow / step — what breaks — why it
   matters — cheapest fix.** Severities: `blocker` (user cannot finish),
   `friction` (user finishes but pays for it), `polish` (trust/feel).
5. **Fix in severity order**, and after fixing, re-walk the flow end to end —
   a fix that breaks an adjacent step is not a fix.

## The checklist (grade every step)

**Continuity**
- Navigation never vanishes or reshuffles mid-journey; the user's location is
  always visible (highlighted nav, breadcrumb, or titled header with a way back).
- Browser reflexes work: back/forward, refresh (state survives), deep links,
  open-in-new-tab on anything that looks like a link.
- The tab title tells the truth (page name; live activity like "● working").

**Feedback within 100ms**
- Every click paints something within 100ms — optimistic state, skeleton, or
  pressed state. Network trails the paint, never leads it.
- Long work shows progress with a truthful unit (steps done, not fake bars),
  and finishes with an outcome the user can act on (link to the result).
- Live surfaces (SSE/WebSocket) say when they are stale: "reconnecting…",
  last-updated stamps, never silent staleness.

**States: every view has five**
- Loading (skeleton beats spinner), empty (names the next action, one verb),
  error (says what happened AND the next action), partial (some data + a
  problem), and full. Audit each view for all five.
- Session expiry anywhere mid-flow → a way back in that returns the user to
  where they were, with unsaved input preserved.

**Input & keyboard**
- Text the user typed is never lost: not by navigation, expiry, error, or a
  disabled submit. Drafts persist.
- Enter submits single-field forms; Escape closes the topmost layer only;
  focus lands somewhere sensible after every open/close.
- The 3 most frequent actions have shortcuts, discoverable in tooltips.

**Layers (modals, popovers, panels)**
- Popover for context actions, modal only for flows that must not be left
  half-done, inline editing for single fields. Never a modal on a modal.
- Click-outside and Escape close popovers; modals confirm before discarding
  non-trivial input.

**Destructive & irreversible**
- Delete/archive/disconnect: undo beats confirm; if confirm, the button names
  the object ("Remove kirkit-repo", not "OK").
- Anything that leaves the machine (push, publish, send) is visually distinct
  and never one accidental click away from a safe action.

**Density & scale**
- Screens are designed for 10× the demo data: lists virtualize or paginate,
  columns fit the viewport or scroll only inside themselves, long strings
  truncate with full value on hover.
- The person who visits 40× a day gets a faster path than the person who
  visits once (recents, pinning, keyboard, remembered layout state).

## Deliverable format

A single document:

```
# <App> flow audit — <date>
## Flows inventoried (numbered)
## Findings (severity-ordered table: # / flow / finding / fix)
## Fixed in this pass (with verification notes)
## Parked (what remains, why, suggested order)
```

Verify every fix by re-walking the flow with real tooling (browser automation
if available). Never mark a finding fixed on the strength of the diff alone.
