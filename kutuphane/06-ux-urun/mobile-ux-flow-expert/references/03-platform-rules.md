# Platform Rules

Contents: 1 iOS 26 and Liquid Glass · 2 Android 16 and Material 3 Expressive · 3 cross-platform parity decisions · 4 gestures and navigation mechanics · 5 App Store and Play review gates that constrain flows.

Platform convention is free conversion — Jakob's Law. Deviate only where you can name the user benefit.

---

## 1. iOS 26 / Liquid Glass

Introduced at WWDC June 2025; the largest Apple design change since iOS 7. Spans iOS 26, iPadOS 26, macOS Tahoe 26, watchOS 26, tvOS 26.

**What it is:** a translucent material that refracts rather than blurs ("lensing"), dynamically adapting to what's behind it. Recompiling with Xcode 26 gives navigation bars, tab bars, toolbars, sheets, popovers, menus, alerts, search bars and controls the treatment automatically.

**The golden rule — glass belongs to the navigation layer only.** Apple's own guidance: reserve it for the layer floating above content. Applying glass to list rows, cards, content backgrounds, or full-screen backgrounds is the most common iOS 26 design error and it destroys legibility.

**Flow-relevant behaviours:**

| Element | Behaviour to design around |
|---|---|
| Tab bar | Inset from screen edges (~21pt left/right/bottom); shrinks/recedes on scroll and re-expands on scroll up. Don't place critical persistent info directly behind it |
| Sheets | Glass + a dimming layer signals an *interrupting* task; glass without dimming signals a *parallel* task. As a sheet is dragged upward it becomes more opaque, signalling deeper engagement. Use detents so the parent stays visible |
| Navigation bar | Content scrolls under it; titles and background adapt. Test contrast against your busiest content |
| App icons | React to transparency and blur — keep icons simple, avoid fine detail |
| Search | Moved toward the bottom in many system apps, aligning with thumb reach |

**Constraints that still hold:** minimum tap target 44×44pt. Support Dynamic Type through the largest accessibility sizes. Respect Reduce Transparency and Reduce Motion — a flow that only reads correctly with glass enabled is inaccessible. Test glass surfaces against light *and* dark, and against photographic content, before shipping; contrast over translucency is the recurring accessibility complaint against the new look.

**Navigation conventions:** interactive swipe-from-left-edge to go back is expected and must never be disabled. Hierarchical drill-down via `NavigationStack`; tabs for peer sections; sheets for tasks. Sign in with Apple is required where other social logins exist.

---

## 2. Android 16 / Material 3 Expressive

Announced May 2025, shipped on Pixel with Android 16 QPR1 in September 2025; rolled through Google's own apps through late 2025 and 2026. It is an expansion of Material 3 / Material You, not a new generation. Backed by an unusually large research programme (46 studies, ~18,000 participants).

**What changed that affects flows:**

- **Spring-based motion system.** Transitions are physical and interruptible. Design flows assuming a user can reverse mid-transition.
- **Shape morphing** between states — useful for signalling that a FAB became a sheet, or a card became a detail screen. Use it to make navigation legible, not decorative.
- **Bigger type, rounder corners, stronger emphasis hierarchy.** Primary actions read louder than in Material 3; secondary actions correspondingly need deliberate de-emphasis.
- **48dp touch targets, enforced more consistently.** Cramped densities that survived before now fail review and accessibility scanning.
- **Default animation durations are slightly longer.** If your flow felt snappy at M3 timings, re-check perceived latency.
- **Short bottom bar** variant — Google's own apps (Phone, Pixel Journal) moved to it.
- **Live Updates** — the Android surface for ongoing progress (delivery, ride, navigation). If your flow has a long-running background task, this is where its status belongs, not a sticky in-app banner.
- **Dynamic colour** (Material You) means your flow's emphasis hierarchy must survive user-chosen palettes. Never rely on a specific hue to signal state.

**Navigation conventions:** predictive back (users see where back will take them) — implement back handling properly or the preview is wrong. Bottom navigation bar for peer destinations; navigation rail/drawer on larger screens and foldables. Gesture navigation is the default; keep 48dp of clearance from the gesture areas at screen edges.

**Adaptive layout is not optional on Android.** Foldables, tablets and desktop-mode change the flow: what is a full-screen step on a phone is often a two-pane list-detail on a tablet. Specify the breakpoint behaviour for any flow that will ship on large screens, and test with hinge angles.

---

## 3. Cross-platform parity decisions

For each of these, decide explicitly rather than defaulting to "same everywhere":

| Decision | Recommendation |
|---|---|
| Navigation structure | Keep the same IA, adapt the chrome. Tab bar ↔ bottom nav bar is a fair mapping; a hamburger on iOS is not |
| Back behaviour | Follow the platform: iOS edge-swipe + back chevron; Android system back + predictive back. Never ship an in-app back button that fights the system one |
| Sheets | iOS sheets with detents ↔ Material bottom sheets. Same content, different physics |
| Date/time pickers | Always native. Custom pickers are a reliable source of one-star reviews |
| Share | Native share sheet, always |
| Permission timing | Same strategy, different copy — Android's rationale dialog pattern differs from iOS's one-shot |
| Typography | SF on iOS, Roboto/Google Sans on Android, or a brand face on both — but match the *scale* to the platform, not just the family |
| Motion | iOS easing curves vs Android spring physics. Porting timings 1:1 makes one platform feel wrong |
| Paywall | Same offer, different store rules (see §5) |

Design tokens should encode the differences (target size, corner radius, motion, elevation) rather than forcing one platform's values on the other.

---

## 4. Gestures and reachability

- **Gestures are shortcuts, never requirements.** Every gesture needs a visible alternative. This is both a usability rule and an accessibility requirement (motor impairment, switch control).
- **Never override system gestures:** edge-swipe back (iOS), home indicator area, notification shade pull, Android gesture-nav zones.
- **Thumb zones.** Roughly three-quarters of mobile interaction is thumb-driven and about half of sessions are one-handed. Reachability degrades notably as screens exceed ~6.5". Practical allocation:
  - **Bottom third** — primary CTAs, tab bar, most-used controls.
  - **Middle** — content, secondary actions.
  - **Top corners** — close/dismiss (users tolerate the reach for exits), profile, rarely-used utilities. Never the primary action of a flow step.
- Right- and left-handed reach mirror; check both. On foldables in tablet mode the model shifts to two-thumb, and the upper-centre becomes the hard zone — split controls to bottom-left and bottom-right.
- **Long-press** should never be the only route to an action. **Swipe-to-delete** needs an undo, not a confirmation.
- **Haptics** confirm state change; don't fire them for routine navigation.

---

## 5. Store review gates that constrain flows

These are flow requirements, not legal footnotes — apps get rejected on them.

**Apple:**
- **5.1.1(v) — in-app account deletion.** Any app supporting account creation must let users *initiate* deletion from within the app. Enforced since 30 June 2022.
- **Sign in with Apple** required when other third-party sign-in options are offered.
- **3.1 — in-app purchase** for digital goods and services. Since May 2025 the **US storefront** permits external purchase links/buttons following a court order; Apple still asserts commission (27%, or 12% under Small Business Program) on link-attributed purchases, with mandatory reporting and a 7-day attribution window. The UI must be region-gated with StoreKit checks and a disclosure sheet — shipping the external-link UI globally is a common rejection. Elsewhere the prohibition still applies except under specific entitlements.
- **Restore Purchases** must be present and functional on any paywall.
- Subscription paywalls must clearly disclose price, period and renewal terms, and provide functional links to terms and privacy policy.
- **2.1 completeness** — reviewers need working demo credentials or an approved demo mode, live backends, and review notes explaining region- or storefront-specific behaviour. Any flow behind auth, payment, moderation or a regulated category needs a walkthrough in the notes (and often a video).
- Apps with user-generated content need a functioning report/block flow — that's a designed flow, not a menu item.
- Permission prompts must have meaningful `NSUsageDescription` strings explaining actual use.

**Google Play:**
- Account deletion required both in-app and via a web-accessible route.
- Data safety declarations must match actual runtime behaviour.
- Subscription and cancellation disclosures; billing failure/grace-period handling affects churn materially.
- Sensitive permission declarations require a documented core-feature justification.

**Practical implication:** budget review iterations for anything touching purchase, deletion, or external links. Teams shipping external purchase links in the first half of 2026 have generally needed a couple of rejection rounds before approval.
