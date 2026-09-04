---
name: mobile-puzzle-game-ui-designer
description: >-
  Use this skill when designing, styling, or engineering mobile puzzle game user interfaces (UI), visual design systems, color tokens, typography hierarchies, component libraries (Numpads, Tile Grids, Progress Bars, Toasts), spring physics animations, and 2026 visual aesthetics (Liquid Glass, Bento Grids, Tonal Surface Layers).
---

# Mobile Puzzle Game UI Designer (`mobile-puzzle-game-ui-designer`)

This skill defines the official design system standards, visual styling guidelines, component architecture, color palettes, and motion physics rules for **mobile puzzle game user interfaces**.

---

## 1. Visual Aesthetics & Design Philosophies (2026 Standards)

Mobile puzzle game UI must feel **living, responsive, and tactile**. The visual language balances visual delight with distraction-free clarity.

### A. Core Aesthetics
1. **Liquid Glass & Depth Layering**:
   - Use translucent, frosted-glass surfaces (`.ultraThinMaterial` / HSL surface fills) with 1pt hairline borders to establish clear foreground-background hierarchy.
2. **Bento Grid Architecture**:
   - Group information into clean, rounded cards (`16pt - 20pt` corner radius) with subtle tonal fill shifts instead of heavy drop shadows or harsh 3D bevels.
3. **Tactile Flat & Spring Motion**:
   - Elements feel physically touchable. Buttons compress smoothly (`scaleEffect(0.96)`) when tapped and spring back naturally.

---

## 2. Color Palette & Token System

All color tokens must be dynamic (Light/Dark mode aware) and maintain strict WCAG 2.2 AA contrast ratios (minimum 4.5:1 for text, 3:1 for controls).

### A. Standard Palette Tokens

| Token Name | Light Mode (Hex) | Dark Mode (Hex) | Functional Role |
| :--- | :--- | :--- | :--- |
| `Palette.bgCanvas` | `#F8F9FA` (Soft Paper) | `#0F172A` (Deep Slate) | Screen background canvas |
| `Palette.bgCard` | `#FFFFFF` (Pure White) | `#1E293B` (Muted Slate) | Primary card containers & Numpad keys |
| `Palette.textPrimary` | `#0F172A` (Navy Ink) | `#F8FAFC` (Off-White) | Primary titles, sequence numbers, key text |
| `Palette.textSecondary`| `#64748B` (Cool Grey) | `#94A3B8` (Slate Grey) | Subtitles, stage descriptions, stats labels |
| `Palette.border` | `#E2E8F0` (Hairline) | `#334155` (Slate Border) | 1pt card borders and key dividers |
| `Palette.accentPrimary`| `#6366F1` (Indigo) | `#818CF8` (Bright Indigo) | Primary CTAs, active selection state |
| `Palette.accentGold` | `#F59E0B` (Amber Gold) | `#FBBF24` (Gold Light) | Sequence Coin badges, Combo multipliers, Level perks |
| `Palette.success` | `#10B981` (Emerald) | `#34D399` (Emerald Light) | Correct answer flash, victory badges |
| `Palette.error` | `#EF4444` (Coral Red) | `#F87171` (Coral Light) | Delete key action, wrong answer flash, low time |

> [!IMPORTANT]
> **Accessibility First**: Never rely *solely* on color to convey state. Pair color shifts with distinct icons (e.g. `✓` for correct, `✗` for wrong) and haptic feedback.

---

## 3. Typographic Hierarchy

Puzzle games require crisp, instant readability for numbers and logic prompts.

- **Sequence & Key Numbers**: System Rounded Heavy (`.font(.system(size: 24, weight: .bold, design: .rounded))`).
- **Screen Titles & Stage Cards**: System Rounded Bold (`.font(.system(size: 20, weight: .bold, design: .rounded))`).
- **Stats Labels & Metadata**: System Monospaced Uppercase (`.font(.system(size: 11, weight: .bold, design: .monospaced))`).
- **Body & Explanations**: System Default Medium (`.font(.system(size: 14, weight: .medium, design: .default))`).

---

## 4. Component Library Specifications

### A. Ergonomic Numpad Keycaps
```swift
// Keycap Component Specs
Height: 56pt - 64pt
Corner Radius: 16pt (Continuous)
Fill: Palette.bgCard
Border: 1pt Palette.border
Press Animation: .scaleEffect(isPressed ? 0.96 : 1.0)
Haptic: UIImpactFeedbackGenerator(style: .light)
```

- **Digit Keys (0-9)**: Neutral background (`Palette.bgCard`) with high-contrast text (`Palette.textPrimary`).
- **Action Keys (Delete / Minus)**: Subtle tinted fills (e.g., Coral Red tint for Delete) for instant visual differentiation.

### B. Number & Sequence Boxes
- **Idle State**: White/Slate fill, 1pt border (`Palette.border`), rounded corners (`14pt`).
- **Hidden Index (`?`) State**: Amber Gold tint fill (`#F59E0B` at 15% opacity), 2pt Gold border, centered question mark.
- **Active User Input State**: Indigo tint fill (`#6366F1` at 15% opacity), 2pt Indigo border with subtle glow shadow.

### C. Dynamic Timer Progress Bar
- **Height**: 8pt - 10pt smooth capsule bar.
- **Interpolation**: Linear color shift:
  - Time > 50%: Indigo (`#6366F1`)
  - Time 20% - 50%: Amber (`#F59E0B`)
  - Time < 20%: Coral Red (`#EF4444`) with subtle pulse animation.

---

## 5. Motion Physics & Animation Curves

All UI animations must target **60fps / 120fps (16.67ms / 8.33ms frame budgets)** using GPU-accelerated property transitions (`transform`, `opacity`, `scaleEffect`).

- **Interactive Taps**: `.spring(response: 0.25, dampingFraction: 0.65)` (Instant, crisp recoil).
- **Screen Transitions & Sheets**: `.spring(response: 0.35, dampingFraction: 0.8)` (Smooth, non-jarring entry).
- **Flash & Overlay Triggers**: Opacity fade-in `100ms`, hold `600ms`, fade-out `300ms`.

---

## 6. UI Design Verification Checklist

Use this checklist during UI reviews to guarantee a 2026-standard mobile puzzle interface:

- [ ] **Design Tokens**: All colors, fonts, margins, and radii consume dynamic design tokens (`AppTheme`).
- [ ] **Surface Layering**: Content uses rounded Bento-grid cards (`16-20pt` radius) with 1pt hairline borders.
- [ ] **Ergonomic Numpad**: Keycaps are 56pt+ tall, spaced 8pt+ apart, and scale smoothly on press.
- [ ] **Contrast Compliance**: Text and numbers achieve WCAG 2.2 AA contrast (4.5:1+).
- [ ] **Multi-Sensory Parity**: Color changes are matched with unique icons and haptic tokens.
- [ ] **Spring Physics**: All interactive state changes use physics-driven spring curves.
- [ ] **GPU Performance**: Layout animations rely on `transform`, `opacity`, and `scaleEffect` to prevent frame drops.
