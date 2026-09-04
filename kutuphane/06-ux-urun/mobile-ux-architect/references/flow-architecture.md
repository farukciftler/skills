# Mobile Flow Architecture & Navigation Reference

## Screen Navigation Types
- **Bottom Tab Bar**: Top-level persistent destinations. Do not use for sequential steps.
- **Push / Stack Navigation**: Sequential drill-down (Home -> Product List -> Product Detail).
- **Bottom Sheet (Modal Detents)**: Medium (50%) and Large (90%) detents for contextual actions (Filter, Share, Item Options).
- **Full-Screen Modal**: Self-contained tasks with explicit "Cancel" / "Done" headers.

## State Machine Architecture
```text
[Initial Launch] -> [Loading / Skeleton] -> (Fetch Success) -> [Ideal State]
                                        -> (No Data)       -> [Empty State + CTA]
                                        -> (Fetch Error)   -> [Error State + Retry]
```

## Offline-First & Perceived Speed
- Cache last-known valid state locally for immediate display on app launch.
- Use optimistic UI updates for instant feedback (e.g., toggling a favorite icon immediately before network ACK).
- Retain form inputs locally during transient network losses.
