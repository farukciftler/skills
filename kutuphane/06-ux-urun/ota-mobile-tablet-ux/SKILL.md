---
name: ota-mobile-tablet-ux
description: Design and audit ComeSyria's phone and tablet experience — the booking funnel (search, results, hotel detail, room selection, checkout, confirmation) and the operator consoles (partner dashboard, admin). Use when building or changing any UI that will be seen on a phone or tablet, when reviewing a screen for responsive/touch/RTL correctness, or when asked to audit or improve mobile/tablet UX. Covers phone portrait, tablet portrait and tablet landscape, plus Arabic RTL.
---

# ComeSyria mobile & tablet UX

Most of ComeSyria's guests arrive on a phone. Most of its partners run their
property from a tablet on a front desk. Neither is a shrunken desktop, and the
tablet is not a big phone — it is the form factor teams forget, because a phone
layout and a desktop layout between them appear to "cover" it.

This skill is the standard for that work. It assumes the stack in
`docs/ARCHITECTURE.md` and the tokens in `src/index.css`.

---

## 0. Before you change anything

Read the real values first. This project has a specific vocabulary and
inventing a parallel one is the fastest way to make the UI incoherent.

- **Tokens live in `src/index.css`** (the Tailwind 4 `@theme` block), with a
  legacy numeric scale in `src/styles/variables.css` consumed only by
  `src/styles/components.css`.
- **There are no custom breakpoints.** The project runs on stock Tailwind 4:
  `sm 640` · `md 768` · `lg 1024` · `xl 1280` · `2xl 1536`. Do not write
  arbitrary-value breakpoints; if you believe a new breakpoint is needed, add it
  to `@theme` so it is shared.
- **Reuse the primitives in `src/components/ui` and `src/components/common`.**
  There is a `Modal` with a sheet mode, a `Table`, `Tabs`, `LazyImage`,
  `Toast`, `Skeleton`, `EmptyState`, `ErrorState`. Adding a fifth bespoke
  dropdown is a regression even if it looks right.

### The layout vocabulary you must use

| Concern | Token / idiom |
| --- | --- |
| Page gutter | `px-margin-mobile md:px-margin-desktop` (16px → 40px) |
| Page max width | `max-w-container-max` (1280px) |
| Grid gap | `gap-gutter` (24px) |
| Vertical rhythm | `stack-sm` 4 · `stack-md` 12 · `stack-lg` 24 |
| Type | `font-body-md text-body-md`, `font-headline-md text-headline-md`, … |
| Color | Material-3 roles: `bg-surface-container-low`, `text-on-surface-variant`, `border-outline-variant`, `text-primary` |

Type scale, actual values: `display-lg` 52/62 · `headline-lg` 32/40 ·
`headline-lg-mobile` 24/30 · `headline-md` 20/26 · `body-lg` 18/29 ·
`body-md` 16/26 · `body-sm` 14/22 · `label-md` 13/16 · `price-tag` 20/24 ·
`title-card` 20/27 · `eyebrow` 11/16.

> `label-lg` **does not exist**. Several files reference `font-label-lg
> text-label-lg`, which silently resolves to nothing. Use `label-md`, or add
> the token — do not propagate the ghost.

---

## 1. The three form factors

Design for these three, in this order. Everything else interpolates.

| Name | Viewport | What it is |
| --- | --- | --- |
| **Phone portrait** | 360–430 × 780–930 | The majority of guest traffic. Design here first. |
| **Tablet portrait** | 768–834 wide | iPad Air 820, iPad Pro 11" 834, iPad mini 768. |
| **Tablet landscape** | 1024–1366 wide | iPad Air 1180, iPad Pro 11" 1194, 12.9" 1366. |

These are **CSS pixels**, not hardware pixels — a 2× iPad Air reports 820 CSS px
regardless of its 1640 physical px. Never reason from marketing resolutions.

### The 768–1023 dead band is this project's known trap

Tablet portrait lands squarely in it. Two rules follow:

1. **Never pair `lg:` "show" with `md:hidden` "hide" on the same affordance.**
   That leaves 768–1023 with neither. This is not hypothetical — the header
   shipped exactly this bug: primary nav `hidden lg:flex`, hamburger `md:hidden`,
   so on every iPad in portrait the site had no navigation at all.
2. **When you hide something at a breakpoint, state where it reappears.** Write
   the pair together and check the gap: `md:hidden` needs a `md:` replacement,
   not an `lg:` one.

**Audit command** — run this whenever you touch chrome:

```bash
# Any element hidden below lg AND hidden at md is unreachable at 768–1023px.
grep -rn "lg:flex\|lg:block\|lg:inline" src/components src/features | grep "hidden"
grep -rn "md:hidden" src/components src/features
```

### Breakpoint by content, not by device

Pick the breakpoint where *the content* stops working — where the line gets too
long, where a third card would fit. Then check that the result is sane at 820
and 1180. Choosing `lg:` because "that's the tablet" is how the dead band gets
created.

---

## 2. Touch ergonomics — the current shortfall

**WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA: 24×24 CSS px.**
**WCAG 2.2 SC 2.5.5 Target Size (Enhanced), Level AAA: 44×44 CSS px.**
Apple HIG: 44×44 pt. Material 3: 48×48 dp.

Target **44×44 CSS px** for anything on the booking path. 24px is a legal floor,
not a design goal — a mis-tap in a checkout costs a booking.

This codebase does not currently meet that:

| Class / component | Computed | Verdict |
| --- | --- | --- |
| `.btn` (default) | ≈39px | **under** — no `min-height` set |
| `.btn-sm` | ≈30px | **well under** — and it is what table row actions use |
| `.btn-lg` | ≈51px | ok |
| `.input-field` | ≈43px | borderline |
| `.btn-icon-square`, `.btn-fab`, `.nav-capsule-item` | 44px | ok |
| `Pagination` item | 36px | under |
| `FavoriteButton` overlay | 36px | under |
| `Checkbox` box | 20px | ok only because the label is clickable |

**Rule:** give `.btn` and `.input-field` a `min-height: 2.75rem`. Reserve
`.btn-sm` for genuinely dense operator tables, and even there pad the *row* so
the hit area reaches 44px even when the glyph does not.

**Spacing:** ≥8px between adjacent targets. Two 44px buttons flush against each
other still mis-tap.

**Thumb reach:** on a 900px-tall phone the top ~25% is a stretch one-handed.
Primary actions belong at the bottom — which the hotel detail and checkout pages
already do correctly with sticky bars. Do not put a primary CTA in the header.

### Hover is not an affordance

Anything reachable only through `:hover` or `group-hover` does not exist on
touch. Decorative hover (`group-hover:scale-105` on a photo) is fine. Functional
hover is a bug.

- Known offender: `DestinationCard.tsx` — an action button that is
  `opacity-0 group-hover:opacity-100` with no `focus-visible:` and no touch
  fallback. Permanently invisible on every phone and tablet.
- `Table` row `hover:bg-…` is the only signal that a row is clickable — invisible
  on touch. Give clickable rows a persistent affordance (a chevron, or make the
  action an explicit button).

Gate hover-only enhancements behind capability, never assume it:

```css
@media (hover: hover) and (pointer: fine) { /* mouse refinements only */ }
```

A tablet with a Magic Keyboard reports **both** coarse and fine pointers. Design
so the touch path is complete and the pointer path is a bonus.

---

## 3. Sheets, modals and navigation

`Modal` (`src/components/ui/Modal.tsx`) already provides the pattern:
`sheet="bottom"` and `sheet="end"`, focus-trapped, scroll-locked, with RTL-aware
animations.

**Its one flaw: the sheet behaviour only applies below `sm` (640px).** At 640px+
it reverts to a centred dialog — so *no tablet ever gets a sheet*, in either
orientation. When you touch this, the sheet breakpoint should be `md` (768) for
bottom sheets, so tablet portrait gets them too.

Only four call sites use sheets today (header drawer, auth, results filters,
results sort). Every partner and admin dialog — room forms, bulk rates, unit
creation, role changes — renders as a centred dialog on a phone. Convert the
ones users hit on a phone.

Rules:

- **Bottom sheet** for a focused choice returning to the same context (filters,
  sort, guest picker, date picker). Escape and backdrop dismiss; the browser
  back button should too.
- **Full-screen route** for a step that has its own URL and can be linked or
  refreshed (checkout, ticket detail).
- **Never a centred dialog on a phone** for anything with more than two fields.
- **`AdminLayout` hand-rolls its own drawer** instead of using `Modal sheet="end"`,
  so there are two divergent implementations with different focus behaviour.
  Consolidate on the primitive.

Also missing and worth adding when the drawer is next touched: safe-area padding
on `sheet="end"` (the bottom sheet has it; the end drawer does not), and
swipe-to-dismiss.

---

## 4. The guest funnel

Design each stage on a 393px-wide canvas first.

### Search entry

- The search widget is the page's job. On a phone it collapses to a stacked
  card at `md`; that is correct.
- The date and guest pickers currently render as **popovers at every size** —
  a 320px popover inside a 360px viewport. On a phone these must be bottom
  sheets. Failure mode: the popover clips at the viewport edge and the user
  cannot see the month they are picking.
- Default to a sensible stay when the user gives no dates rather than blocking
  the search. Showing prices requires dates; refusing to search does not.
- Keep the hero short enough that the search widget is above the fold on a
  phone. A hero that pushes the primary interaction below the fold is a
  conversion bug, not an aesthetic choice.

### Results

- Card: image 4:3 or 16:9, name, location, rating, **price with its basis
  stated** ("per night" vs "total"). Ambiguous price is the single most
  complained-about pattern in OTAs.
- Two cards visible above the fold on a phone; the second card should be
  partly cut to signal scrollability.
- Sticky filter/sort bar with an **active-filter count** and a clear-all. The
  results page already does this well — copy it, do not reinvent it.
- Filters in a bottom sheet with an explicit **Apply** button and a live result
  count on that button. Live-apply on mobile makes users lose their place.
- **The map has no list companion below `lg`** — on a phone the map is a dead
  end. Pair it with a swipeable card strip over the map, or a segmented
  list/map toggle that preserves scroll position.
- Returning from a hotel back to results **must** restore scroll position and
  filters. Losing them is the most expensive bug on this screen.

### Hotel detail

- The swipeable hero gallery with a photo counter is right. Keep it.
- The sticky bottom booking bar (`lg:hidden`, with `env(safe-area-inset-bottom)`)
  is right. Keep it.
- Order for a phone: gallery → name/rating/location → price + CTA → **rooms** →
  amenities → reviews → location → policies. "See rooms" must be reachable
  without a long scroll; it is the next step in the funnel.

### Room selection & checkout

- One column. Never split a checkout form into columns on a tablet — a form is
  a sequence, and two columns make the order ambiguous.
- Field order: name → email → phone → requests. Set `autocomplete`
  (`given-name`, `family-name`, `email`, `tel`), `inputmode` (`email`, `tel`),
  and `type` so the right keyboard appears.
- **Inputs must be ≥16px font** or iOS zooms on focus and the user is stranded
  at 1.3× with the layout shifted. `body-md` is 16px — use it, not `body-sm`.
- Validate on blur, not on keystroke. Errors adjacent to the field, never only
  in a summary at the top.
- Price breakdown fully expanded before the confirm button. Every line named.
  The one thing this product has over its competitors is that there is no card
  and no prepayment — **say so next to the button**, not in a footnote.
- `StayBar` currently sits 2×2 on a phone, squeezing two date fields into ~50%
  of a 360px screen. Dates deserve full width; go 1-column below `sm`.

### Confirmation

On screen: reference, property, dates, total, what happens next, and how to
cancel. In the email: the same, plus contact details. The reference must be
selectable text, not baked into an image.

---

## 5. Tablet

### Portrait (768–834)

- Two-column card grid. One column at this width gives a card ~750px wide with a
  tiny thumbnail and a lake of whitespace.
- Body text max **~70 characters per line**. At 820px, full-bleed prose exceeds
  100 — constrain with `max-w-[65ch]`.
- Filters: a drawer or sheet, not a permanent sidebar. A 3-column sidebar at
  820px leaves ~570px for results.
- Type: this is *not* where you use the desktop `display-lg` (52px). The current
  home hero jumps `headline-lg-mobile` → `sm:text-4xl` → `md:display-lg`, so at
  820px it is already at full desktop size and the headline wraps badly.

### Landscape (1024–1366)

- A persistent filter sidebar becomes correct here.
- Three result cards per row at ≥1280; two below that.
- List + map side by side is the strongest layout this product has and it is
  only enabled at `lg` today — good, keep it.
- Still touch-first. 1180px wide does not mean a mouse.

### Orientation change

Rotating must preserve scroll position, form state, open sheet, gallery index
and map viewport. Rotation remounts nothing in React — but it does change
`100vh`. Use **`dvh`** for anything full-height (`h-[100dvh]`), never `100vh`,
which on mobile Safari measures the viewport *without* the browser chrome and
overflows.

### Operator consoles on a tablet

Partner and admin are used on tablets at a front desk. They are currently the
weakest surfaces: **every admin tab and most partner tabs have zero responsive
handling**, and the tables run 5–11 columns behind nothing but `overflow-x-auto`.

- `Tabs` has no `overflow-x-auto` — six tabs wrap or overflow on a phone. Add
  horizontal scroll with scroll-snap.
- Tables need **column priority**: decide which 3–4 columns matter, keep those,
  and collapse the rest into an expandable row or a card layout below `md`.
  Horizontal scroll alone hides the actions column off-screen, which is where
  the buttons are.
- Row actions must not be hover-revealed.
- Give the first column `position: sticky` if you keep horizontal scroll.

---

## 6. RTL (Arabic)

The codebase is in good shape here and must stay that way: **zero** uses of
`ml-/mr-/pl-/pr-/text-left/text-right/rounded-l/rounded-r/border-l/border-r`.

- Always use logical utilities: `ms-` `me-` `ps-` `pe-` `start-` `end-`
  `text-start` `text-end`, and `border-s`/`border-e`.
- `inset-x-*` is symmetric and safe.
- Mirror directional **icons** with `rtl:-scale-x-100` or `rtl:rotate-180` —
  back arrows, carousel chevrons, logout glyphs.
- Do **not** mirror: numerals, prices, dates, phone numbers, or map geography.
- Arabic needs more leading; `html[lang='ar']` already sets `line-height: 1.75`
  and kills letter-spacing. Do not override it.
- Test every new screen at `?lang=ar`. A layout that only breaks in RTL is still
  broken.

Known remaining bug: `SplashScreen.tsx` uses `right-2.5` for a rating badge —
should be `end-2.5`.

---

## 7. Images and perceived speed

- Use `LazyImage` with the right `layout` (`hero` `card` `thumb` `gallery`
  `full`). It emits `srcSet`, `sizes`, explicit `width`/`height` for CLS, and
  `loading`/`fetchPriority`.
- **The LCP hero is currently a raw `<img>` with `sizes="100vw"` and no
  `srcSet`** — a 393px phone downloads the same asset as a 4K desktop. A `sizes`
  attribute without a `srcSet` is inert. Fix by giving it a real srcSet.
- `LAYOUT_SIZES.card` in `src/lib/image.ts` claims 2 columns from 640px and 3
  from 1024px, but the results grid is actually `md:grid-cols-2 xl:grid-cols-3`
  (768/1280). **Keep the `sizes` string and the grid in sync** or the browser
  picks the wrong candidate at every mismatched width.
- Skeletons, not spinners, for content whose shape is known.
- Reserve space for sticky bars and late images. CLS on a checkout is how a user
  taps the wrong button.

---

## 8. Accessibility floor

- Visible focus on every interactive element. `focus-visible:outline-2
  focus-visible:outline-primary` is the house style.
- Announce dynamic result counts to screen readers (`aria-live="polite"`).
- Respect `prefers-reduced-motion` — already honoured by `Skeleton`, `Spinner`,
  `LazyImage`, `SplashScreen`. Match it.
- Contrast: text over a hero photo needs a scrim, not hope. The home hero
  subtitle currently sits directly on a light part of the image.
- Every icon-only button needs an `aria-label`.

---

## 9. How to audit a screen

1. **Capture.** Playwright at 393×852, 820×1180, 1180×820. Set
   `isMobile: true, hasTouch: true` — layout alone is not the whole story.
   Use `deviceScaleFactor: 1`; 2× at full-page across several viewports will
   exhaust memory on a small box.
2. **Pre-seed state** so the shot is of the screen and not of an overlay:
   ```js
   await context.addInitScript(() => {
     localStorage.setItem('comesyria_consent', 'granted');
     sessionStorage.setItem('comesyria_splash_seen', 'true');
   });
   ```
   Then capture the consent banner deliberately, once — it covers the home
   search CTA on a phone and that is itself a finding.
3. **Look for, in order:** unreachable navigation · a primary CTA below the fold
   · tap targets under 44px · horizontal overflow · text over 70ch · hover-only
   affordances · dead whitespace on tablet · anything that only appears at `lg`.
4. **Flip to `?lang=ar`** and repeat on at least the funnel screens.
5. **Fix the funnel first.** A misaligned card on the careers page costs
   nothing; a filter sheet that will not close costs a booking.

Report findings as: screen → what breaks → at which viewport → why it costs
something → the fix in this codebase's vocabulary.
