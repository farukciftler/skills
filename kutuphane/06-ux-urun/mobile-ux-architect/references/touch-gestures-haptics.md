# Ergonomics, Touch Targets & Micro-Interactions

## Touch Target & Ergonomics Guidelines
- **iOS Target**: 44 × 44 pt minimum.
- **Android Target**: 48 × 48 dp minimum.
- **Thumb Zone**:
  - **Natural Zone**: Bottom 30-40% of screen height. Best for primary actions.
  - **Stretch Zone**: Middle 30% of screen height. Best for secondary content cards.
  - **Hard Zone**: Top 20% of screen height. Best for static header titles or non-critical secondary icons.

## Gestures & Micro-Animations
- **Swipe-to-Dismiss**: Standard gesture for modals, bottom sheets, and banner notifications.
- **Pull-to-Refresh**: Standard for stream/feed refresh with progress indicator.
- **Animation Speed**: 150ms - 300ms using ease-out or spring physics.
- **Haptic Tokens**:
  - `light`: Tab switches, slider drags, segmented control selection.
  - `medium`: Button presses, pull-to-refresh trigger.
  - `heavy` / `error`: Form validation failure, destructive action confirm.
