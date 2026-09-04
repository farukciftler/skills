# Metrics & Performance Diagnosis

## Metric definitions (post-March-2025 reality)

- **Views**: counted on every play or replay, no minimum watch time. Inflated by design — never diagnose from raw views alone.
- **Engaged views**: views with meaningful watch time (also the monetization-relevant count). Use this as the real reach number.
- **Viewed vs. swiped away** (Studio, Shorts-only): % of feed impressions where the viewer stayed instead of swiping. This is the verdict on your first 1–2 seconds + first frame + title.
- **Average percentage viewed (APV)**: can exceed 100% thanks to loops. The single best proxy for "the algorithm will push this."
- **Retention curve**: where people leave. Shape matters more than the average (see below).
- **Traffic sources**: Shorts feed vs. search vs. channel page. A search-heavy Short is an evergreen asset (metadata matters more); a feed-heavy Short is a hook/retention game.
- **Subs per 1,000 engaged views**: conversion quality of the audience you're reaching.

## Directional benchmarks

Treat as creator-observed heuristics, not official thresholds; calibrate against the channel's own history first (a video should beat the channel's median, then the niche).

| Metric | Weak | Decent | Strong |
|---|---|---|---|
| Viewed vs. swiped | <60% | 70–75% | 80%+ |
| APV, ≤30s Short | <65% | 65–80% | 90%+ (loops >100%) |
| APV, 30–60s Short | <50% | 50–70% | 80%+ |
| Likes / engaged views | <2% | 3–4% | 5%+ |
| First-hour engagement | flat | some traction | fast spike (posting when the audience is awake helps here) |

Reported fan-out thresholds: ~65% APV for sub-30s, ~50% for 30–60s. If a Short sits just under these, retention edits (tightening, re-cutting the hook, adding a loop) are the highest-ROI move.

## Decision tree — walk in order, stop at the first failing stage

Diagnose the failing stage, fix that stage only. Report which stage failed by name.

**Stage 0 — Distribution: did it even get impressions?**
Very few impressions ever (never left seed test) → suspect: channel has no coherent audience model (topic whiplash), reuploaded/duplicate content flags, policy limited, or brand-new channel still calibrating. Fix: niche consistency run (10–15 Shorts, one theme), verify no yellow icons, originality of footage. NOT a hashtag problem.

**Stage 1 — Feed hold: viewed vs. swiped low (<65%)?**
Viewers reject it before it starts. Suspects: weak first frame, dead first second, title not functioning as a hook, mis-categorized audience (wrong/misleading tags & hashtags → wrong seeding). Fix order: recut first 1–2s (start mid-action), rewrite title (playbook), correct categorization metadata.

**Stage 2 — Retention shape: where does the curve break?**
- **Cliff in first 3s** (but swipe rate was OK): hook promised, opening didn't deliver instantly. Move the payoff earlier; cut all setup.
- **Steady bleed**: pacing — no re-hooks. Add pattern changes every 2–3s; cut 20–30% of runtime.
- **Mid-video cliff**: the moment the content stops matching the promise. Find the exact second, cut or restructure from there.
- **Strong until the end, drop at outro**: kill the outro; end mid-beat or loop.
- **>100% APV but low engagement**: loop is working; now add a comment-provoking element (open question, mild controversy, deliberate detail people correct).

**Stage 3 — Engagement: retention fine, likes/comments/shares low?**
Content is watchable but inert. Add a stance (opinions get shared, information gets watched), a question worth answering, or a share-trigger ("send this to the friend who..."). Pin a comment with a question. Satisfaction surveys reward content people are glad they watched — pure filler retains but doesn't satisfy.

**Stage 4 — Conversion: views fine, no subscribers?**
Audience mismatch or no serial promise. Fix: recognizable series format ("Part 2 tomorrow", consistent hook style), niche coherence so the viewer knows what subscribing gets them. One-off viral topics convert worst — this is normal; say so.

**Stage 5 — One-hit-wonder pattern: one outlier, everything else flat?**
Not a problem — an unmined asset. Iterate the outlier: same format, adjacent topics, 5–10 variants. Most channels never do this and it's the most reliable growth move available.

## Reading a stats screenshot

When the user drops a Studio screenshot: extract every number visible, restate them back in a compact table (so errors get caught), then run the tree. If the screenshot lacks the stage you need (e.g., no retention curve), name the exact panel to screenshot next: *Analytics → Engagement → Audience retention* or the *Viewed vs. swiped away* card on the Short's own analytics.
