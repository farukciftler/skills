---
name: mobile-ux-architect
description: >-
  Use this skill when auditing, architecting, or designing mobile application user experiences (UX), user flows, navigation hierarchies, screen states, micro-interactions, touch ergonomics, and accessibility for iOS and Android platforms.
  Enforces 2026 Mobile UX standards: Thumb Zone ergonomics, minimum touch targets (Apple 44x44pt / Android 48x48dp / WCAG 2.5.8), skeleton loading & error recovery states, Haptic feedback, and design system tokens.
---

# Mobile UX & Flow Architect Skill (`mobile-ux-architect`)

This skill provides step-by-step guidance for architecting seamless mobile app user flows, designing intuitive navigation, enforcing thumb-zone ergonomics, managing edge-case UI states, and maintaining design system consistency.

---

## UX Audit & Flow Architecture Workflow

### Step 1: Thumb Zone & Ergonomic Layout Audit
1. **Primary Thumb Zone (Bottom 1/3)**:
   - Place high-frequency actions (Primary CTAs, Navigation Bar, Floating Action Buttons) in the natural thumb sweep area.
   - Avoid placing critical destructive or primary actions in the upper-opposite corner (hard reach).
2. **Touch Target Dimensions**:
   - **Apple HIG (iOS)**: Minimum **44 × 44 points** hit area.
   - **Google Material Design 3 (Android)**: Minimum **48 × 48 dp** hit area.
   - **WCAG 2.5.8**: Minimum 24px diameter with required spacing buffer to prevent mis-taps.

---

### Step 2: Information Architecture & Navigation Patterns
1. **Navigation Hierarchy**:
   - **Bottom Tab Bar (3 - 5 items)**: Use for top-level peer destinations. Keep icons paired with clear text labels.
   - **Stack Navigation (Push/Pop)**: Use for hierarchical drill-down detail screens. Provide clear back buttons and swipe-to-back gesture support.
   - **Bottom Sheets (Modal/Detent)**: Use for contextual tasks, quick filters, or secondary choices without breaking screen flow context.
   - **Modals (Full Screen)**: Reserve exclusively for self-contained tasks (e.g., checkout, creation flows, multi-step forms).
2. **Deep Linking & Back-Stack**: Ensure physical/gesture back button correctly unwinds the back stack.

---

### Step 3: Complete State Architecture (The 5 Core UI States)
Every mobile screen flow MUST explicitly handle all 5 UI states:
1. **Ideal / Content State**: Fully populated content with smooth rendering.
2. **Loading State**:
   - Use **Skeleton Screens** matching content layouts for initial data fetches (minimizes perceived latency).
   - Use subtle inline spinners for background refreshes or action buttons.
3. **Empty State**:
   - Never leave a blank screen. Provide an illustration/icon, clear explanation (*"No messages yet"*), and a primary call-to-action (*"Send a message"*).
4. **Error State**:
   - Provide non-technical explanations and an immediate recovery action (*"Retry"* button, *"Check network"* prompt).
5. **Partial / Searching State**: Filter/search results state with clear filter reset options.

---

### Step 4: Micro-Interactions, Haptics & Motion Design
1. **Feedback Loops**: Every tap must trigger instant feedback (< 100ms) via visual state change (pressed state) or haptic feedback.
2. **Animation Duration**: Keep transitions between **150ms and 300ms**. Use natural easing (`cubic-bezier` / spring dynamics).
3. **Haptic Tokens**: Use light impact for selection, medium impact for action confirmation, and notification warning/error for failures.

---

## Mobile UX Verification Checklist

- [ ] All interactive elements meet 44x44pt (iOS) or 48x48dp (Android) hit target sizes.
- [ ] Primary CTAs are placed within the natural Thumb Zone (bottom 1/3 of screen).
- [ ] Bottom Tab Bar has between 3 and 5 items max with text labels.
- [ ] Screen handles all 5 UI States: Ideal, Loading (Skeleton), Empty, Error (Retry), and Partial/Filter.
- [ ] Keyboard avoidance is handled cleanly on forms without obscuring input fields or primary submit buttons.
- [ ] Contrast ratio meets WCAG 2.2 AA standards (minimum 4.5:1 for normal text).
- [ ] Haptic & visual feedback provided for interactive buttons and gestures.
