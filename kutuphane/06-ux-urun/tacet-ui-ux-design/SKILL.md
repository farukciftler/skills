---
name: tacet-ui-ux-design
description: Strict design system, UI/UX architecture, typography, palette tokens, and interaction guidelines for the Tacet iOS app. Enforces "Night Ink" single surface minimalism, SF Pro + New York Serif typographic dualism, Ensō mark dynamics, quiet 44pt touch targets, and 1px hairline card styling.
---

# Tacet UI/UX Design System & Architectural Standards

This skill defines the official, non-negotiable UI/UX standards and design system rules for **Tacet**. Every feature, view, sheet, component, and interaction in Tacet must adhere strictly to these principles.

---

## 1. Core Philosophy: "Night Ink" & Single Surface Minimalism

Tacet is built on a **calm, paper-and-ink single-surface philosophy**. The UI avoids noisy multi-border containers, heavy drop shadows, bright accent badges, or artificial carousels.

- **"Don't tell, show."**: Present information through clean typography, high contrast, and direct interactive example chips.
- **Quiet Interface**: State is told with plain words, cool grey tones, and deterministic events — not loud warning badges or artificial color coding.
- **Zero Distraction**: Surfaces blend seamlessly into the background token (`Palette.background`).

---

## 2. Color Palette ("Night Ink") — Spec §3.1

All color tokens are dynamic (light/dark mode aware) and defined in [`Theme.swift`](file:///Users/farukciftler/Documents/GitHub/tacet-app/Tacet/Design/Theme.swift).

| Token | Light Mode (Hex) | Dark Mode (Hex) | Contrast / Usage |
| :--- | :--- | :--- | :--- |
| `Palette.background` | `#F7F3EA` (Paper) | `#0B1220` (Night ground) | Main window & view canvas |
| `Palette.ink` | `#131C2E` (Navy ink) | `#E9E4D8` (Paper ink) | Primary body text, send button fill (15.4:1 / 14.8:1) |
| `Palette.grey` | `#4C5568` | `#97A1B4` | Secondary text, active chip text (6.8:1 / 7.2:1) |
| `Palette.muted` | `#636D82` | `#7D8698` | Section titles, tags, placeholders (4.7:1 / 5.1:1) |
| `Palette.divider` | `#E6E0D1` | `#1E2A40` | 1px hairline borders, separators, chip frames |
| `Palette.fill` | `#EDE7D9` | `#17233A` | User bubble background, card backgrounds |
| `Palette.accent` | `#7E6410` (Darkened Brass) | `#C9A227` (Brass) | **Brand moments ONLY** (Ensō dot, selection checkmarks) |
| `Palette.error` | `#B4483C` | `#D46A5E` | Failed tool execution traces only |

> [!IMPORTANT]
> `Palette.grey` and `Palette.muted` are **not neutral greys** — they are cool dilutions of the same navy ink family. Never use generic system grey (`Color.gray`).

---

## 3. Typographic Dualism — Spec §3.2

Tacet uses two distinct typographic voices defined in [`Theme.swift`](file:///Users/farukciftler/Documents/GitHub/tacet-app/Tacet/Design/Theme.swift):

1. **User Voice & System Controls (SF Pro Default)**:
   - User messages, buttons, text fields, section labels, and navigation.
   - `Typography.user()` → Callout size (`.system(.callout, design: .default)`).
   - `Typography.chip()` → Caption size (`.system(.caption, design: .default)`).
   - `Typography.tag()` → Caption2 uppercase tracking (`.system(.caption2, design: .default)`).

2. **Tacet Voice & Brand Moments (New York Serif)**:
   - Tacet replies, empty state hero titles, and brand headings.
   - `Typography.tacet()` → Body size (`.system(.body, design: .serif)`).
   - `Typography.brand()` → Title3 size (`.system(.title3, design: .serif).weight(.medium)`).

> [!CAUTION]
> Fixed point sizes (e.g. `.font(.system(size: 16))`) are **strictly forbidden**. Always use `Typography` tokens bound to relative system text styles to preserve Dynamic Type scaling.

---

## 4. Spacing Scale & Touch Targets — Spec §3.3

- **Spacing Token Scale**:
  - `Spacing.s1`: `4pt`
  - `Spacing.s2`: `8pt`
  - `Spacing.s3`: `12pt`
  - `Spacing.s4`: `16pt`
  - `Spacing.s5`: `22pt` (Screen horizontal margin)
- **Borders & Corners**:
  - `Spacing.hairline`: `1pt` border width using `Palette.divider`.
  - `Spacing.chipCorner`: `24pt` continuous rounded corner radius.
- **Ergonomics & Touch Target**:
  - Minimum touch target: **44×44pt** (`@ScaledMetric(relativeTo: .body) private var touchTarget = 44`).

---

## 5. Ensō Mark Dynamics

The official Ensō logo (`TacetMark`) is Tacet's primary brand amble.

- **Idle / Stationary State**: `TacetMark(size: size)` renders the open brush circle with the brass dot (`Palette.accent`) at (274.2, 116.1).
- **Active / Streaming / Thinking State**: `SpinningTacetMark(size: size, reduceMotion: reduceMotion)` continuously spins the Ensō mark smoothly.
  - Used in `TopBar` when model is generating or working.
  - Used in `TimelineRibbon` ("seyir") during step execution.
  - Used in `TacetReply` streaming typing indicator.

---

## 6. Standard Component Patterns

### A. Sample Chip (`SampleChip`)
Single-line pill button used in `EmptyState` and list selections.
```swift
Text(text)
    .font(Typography.chip())
    .foregroundStyle(Palette.grey)
    .padding(.horizontal, Spacing.s3)
    .padding(.vertical, Spacing.s2)
    .frame(minHeight: touchTarget)
    .overlay(
        RoundedRectangle(cornerRadius: Spacing.chipCorner, style: .continuous)
            .stroke(Palette.divider, lineWidth: Spacing.hairline)
    )
```

### B. Section Header
Uppercase tracked label matching `Capabilities.swift` and `SkillBoard.swift`.
```swift
Text(title)
    .font(Typography.tag())
    .textCase(.uppercase)
    .tracking(1.2)
    .foregroundStyle(Palette.muted)
```

### C. Interactive Selection Pills (e.g. Tool Chips in `SkillBoard.swift`)
```swift
HStack(spacing: Spacing.s1) {
    if selected {
        Image(systemName: "checkmark")
            .font(Typography.chip())
            .foregroundStyle(Palette.accent)
    }
    Text(label)
        .font(Typography.chip())
        .foregroundStyle(selected ? Palette.ink : Palette.grey)
}
.padding(.horizontal, Spacing.s3)
.padding(.vertical, Spacing.s2)
.background(selected ? Palette.fill : Palette.background)
.clipShape(Capsule())
.overlay(
    Capsule().stroke(selected ? Palette.accent : Palette.divider, lineWidth: Spacing.hairline)
)
```

---

## 7. Localization & Language Enforcements

- **100% Localized Strings**: Never hardcode English strings in View labels, buttons, headers, footers, or placeholders.
- Always wrap text in `String(localized: "...")` or `Text(LocalizedStringKey("..."))`.
- Turkish & English frontmatter triggers must be present in all built-in skills (`SkillStore`).

---

## 8. Haptic Feedback Standards

Add light sensory feedback on touch actions:
```swift
.sensoryFeedback(.impact(weight: .light), trigger: tapCounter)
```
