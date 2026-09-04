---
name: mobile-puzzle-game-ux-audit-expert
description: >-
  Use this skill when auditing, architecting, or designing mobile puzzle game user experiences (UX), mathematical & logic game loops, input/numpad ergonomics, cognitive load management, rewarding micro-interactions, onboarding & difficulty ramp, hint systems, and retention mechanics.
  Enforces 2026 Mobile Puzzle Game UX standards.
---

# Mobile Puzzle Game UX Audit Expert (`mobile-puzzle-game-ux-audit-expert`)

This skill defines the official, non-negotiable UX architecture guidelines, behavioral psychology models, ergonomic standards, and audit procedures for **mobile puzzle, logic, and mathematical brain games**. 

---

## 1. Core Puzzle UX Philosophy: "Invisible Interface & Flow State"

In 2026 mobile puzzle design, **UX is invisible**. If a player spends mental energy deciphering the interface or struggling with touch targets, the immersion breaks and churn rises.

- **The Flow State (Goldilocks Zone)**: Maintain a balance where difficulty scales dynamically with player skill—challenging enough to prevent boredom, but forgiving enough to prevent anxiety.
- **Zero Input Friction**: Mechanical friction must be near zero so 100% of cognitive capacity is dedicated to solving the puzzle.
- **First Win Principle (Onboarding)**: Guarantee a satisfying victory within the first 60 seconds to build confidence and emotional investment.

---

## 2. Behavioral Psychology & Retention Loops

### A. The Peak-End Rule
Players evaluate their game session based on **its highest peak moment** and **its conclusion**, not the average of the whole session.
- **Peak UX**: Triumphant victory overlays, particle bursts, and combo multipliers.
- **End UX**: Non-punitive game over screens. Always highlight progress, XP gained, and coins earned rather than harsh failure messages.

### B. The Near-Miss Effect
When a player loses by a tiny margin (e.g. 1 second remaining or off by 1 digit), reframe it as *"So close!"* rather than a failure. This triggers the impulse to retry immediately.

### C. The Zeigarnik Effect & Open Loops
Design level progressions so players always see the next milestone (e.g. *"Stage 10 Unlock: New Rule Unlocked!"*). Unfinished goals encourage "one more level" behavior.

### D. Industry Retention Benchmarks (2026 Standards)
- **Day 1 (D1)**: Target **~27%+**
- **Day 7 (D7)**: Target **8–14%**
- **Day 30 (D30)**: Target **3–7%**

---

## 3. Input Controls & Thumb-Zone Ergonomics

### A. Numpad & Touch Target Architecture
1. **Primary Thumb Zone (Bottom 40%-50%)**:
   - Anchor all high-frequency controls (Numpad keys, Submit buttons, Tile grids) in the lower half of the screen.
2. **Touch Target Dimensions**:
   - **Apple HIG (iOS)**: Minimum **44 × 44 pt** hit target.
   - **Google Material 3 (Android)**: Minimum **48 × 48 dp** hit target.
   - **Numpad Keys**: Ideal height **56pt - 64pt** with **8pt - 12pt inter-key spacing**.
3. **Input Feedback & Mis-Tap Prevention**:
   - Instant visual spring scale (`scaleEffect(0.96)`) on press.
   - Unmistakable **Delete/Backspace (⌫)** and **Minus (-)** controls.
   - Clear visual boundaries with high-contrast readable typography.

---

## 4. Multi-Tiered "Juice" & Micro-Interactions

"Juice" is the rich, multi-sensory feedback provided in response to player actions.

```
Player Action ──> [<50ms] Visual Spring + Haptic Tap ──> [<150ms] Rule Evaluation ──> Multi-Sensory Reward
```

| Event Type | Visual Feedback ("Juice") | Haptic Token | Audio Feedback |
| :--- | :--- | :--- | :--- |
| **Key Tap** | Scale effect (`0.96`), soft border highlight | `UIImpactFeedbackGenerator(.light)` | Non-blocking key click |
| **Regular Correct** | Subtle emerald green background flash (`#10B981` at 15% opacity), checkmark animation | `UIImpactFeedbackGenerator(.medium)` | Ascending pitch chime |
| **Fast Answer Bonus** | Speed badge pulse, carried bonus time indicator | `UIImpactFeedbackGenerator(.medium)` | Bright double chime |
| **Combo Streak (3+)** | Gold background flash (`#F59E0B`), `x1.25 BOOSTER` pill, floating particles | `UINotificationFeedbackGenerator(.success)` | Harmonic combo fanfare |
| **Incorrect / Timeout** | Coral red flash (`#EF4444` at 15% opacity), subtle horizontal card shake | `UINotificationFeedbackGenerator(.error)` | Low-frequency soft thud |

---

## 5. Stage Progression & Dynamic Difficulty Curve

A well-balanced puzzle game uses progressive disclosure without long text walls:

```
[ Stage 1-10 ] ──> [ Stage 11-50 ] ──> [ Stage 51-100 ] ──> [ Stage 100+ ]
   Onboarding         Expansion           Mastery              Expert
```

- **Stage 1-10 (Onboarding)**:
  - Simple single rules (e.g. $+2$, $+5$, $n^2$). Generous time budget (20s+). Teach by playing.
- **Stage 11-50 (Expansion)**:
  - Introduce Chained rules ($a_n = a_{n-1} \times 2 + 1$). Random gap mechanic (hidden index varies from 0 to 4).
- **Stage 51-100 (Mastery)**:
  - Alternating rules (odd/even index rules). 30% chance of Reversed sequence. Time bonus carryover system active.
- **Stage 100+ (Expert)**:
  - Digit sum/product operations. Dynamic time budget (decreases 1s per 5 stages, capped at 5s minimum floor).

---

## 6. Post-Game Review & Educational UX

Losing a level must become a learning moment, not a wall:

1. **Step-by-Step Explanation**: Show the incorrect question, the user's input, the correct answer, and explicit step derivations (e.g., `+3 → +6 → +12`).
2. **One-Tap Re-entry**: Provide a high-contrast primary CTA (*"Play Again ↺"*) anchored in the thumb zone.
3. **Transparent Reward Summaries**: Display earned XP, Level progress, and Sequence Coins earned during the run.

---

## 7. The 10-Point Mobile Puzzle UX Audit Checklist

Before declaring any mobile puzzle game feature production-ready, verify against this audit checklist:

- [ ] **Thumb Zone Anchor**: All primary input controls (Numpad, tiles, submit) are anchored in the lower 50% of the screen.
- [ ] **Touch Target Sizes**: All keys/buttons meet minimum 44×44pt (iOS) or 48×48dp (Android) guidelines with >8pt gaps.
- [ ] **Instant Feedback (<50ms)**: Every tap produces immediate visual scaling and light haptic feedback.
- [ ] **First Win Onboarding**: Players achieve a clear, rewarding win within the first 60 seconds.
- [ ] **Peak-End Preservation**: Game over screens emphasize progress (XP/Coins) and provide a clean 1-tap retry.
- [ ] **Juice Layering**: Multi-sensory rewards (Visual, Audio, Haptics) scale with speed and combo streaks.
- [ ] **Dynamic Difficulty**: Time budgets and rule complexities scale smoothly without sudden spikes.
- [ ] **Near-Miss Reframing**: Close losses show *"So close!"* feedback to motivate immediate retries.
- [ ] **Educational Step Reviews**: Incorrect answers show step-by-step visual rule explanations.
- [ ] **Accessibility & Performance**: Contrast ratios meet WCAG 2.2 AA (4.5:1+) and 60fps frame pacing is maintained.
