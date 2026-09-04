# Shorts Audit Framework

Audit in three layers. The layers are ordered by how often they are the real bottleneck — but always find THE bottleneck rather than listing every imperfection. A Short with a broken hook does not need hashtag advice.

## Layer 1 — Content & Hook (usually the real problem)

Assess from the video itself if viewable, otherwise from the retention curve and the user's description of the video.

1. **Hook (0–2s).** Does the first frame + first spoken/overlaid line create an open loop, a bold claim, a visual anomaly, or an immediate payoff promise? Kill criteria: logo intros, "hey guys welcome back", slow establishing shots, greeting the camera. The viewer decides to swipe in under a second.
2. **Re-hooks / pacing.** A pattern change (cut, zoom, caption change, scene change, new question) every ~2–3 seconds. Flag dead air, repeated shots, filler sentences.
3. **Payoff.** Does the video deliver what the hook promised? Hook-payoff mismatch is the #1 cause of mid-video drop and bad satisfaction survey results.
4. **Length fit.** Is every second earning its place? Most Shorts should be ≤35s; go longer only when the retention curve proves the format holds (storytime, tutorials). A 55s video that could be 28s is a retention leak.
5. **Loop potential.** Does the ending connect back to the beginning (seamless loop, ending mid-beat, "wait, what?" endings)? Loops push average view percentage above 100% — one of the strongest signals available.
6. **Ending.** No long outros, no "like and subscribe" longer than 1s. The last second should either loop or land the payoff.
7. **Accessibility & clarity.** Burned-in captions (most feed viewing starts muted or in noisy contexts), readable text size for phones, safe zones respected (top ~10% and bottom ~15% are covered by UI).
8. **Audio.** Trending or fitting sound? Music bed under voice? Silence is a swipe trigger.

## Layer 2 — Packaging (title, hashtags, tags, description, first frame)

Full rules and rewrite formulas live in `metadata-playbook.md` — read it when scoring this layer. Check:

1. Title: hook function + search function, length, no wasted characters.
2. Hashtags: 2–5, niche-specific, ≤15 total, no `#viral`/`#fyp`, no `#Shorts` needed.
3. Tags: not misleading, not stuffed, reinforce the title keywords.
4. Description: first line restates/extends the hook with keywords; not empty, not keyword salad.
5. First frame / thumbnail: legible and intriguing at small size (matters for search results, channel page, and some feed surfaces).

## Layer 3 — Channel strategy (the pattern across videos)

Only assessable with 5+ videos or channel access. This layer explains why *technically fine* Shorts still underperform.

1. **Niche coherence.** Can you state in one sentence who this channel is for and what they get? Random topics scatter the audience model — the algorithm can't find a stable audience to seed to. Flag topic whiplash across the last 10 uploads.
2. **Format repetition.** Winning channels productize: a recognizable repeatable format (same intro style, same series concept). Check whether the channel's best performer was ever followed up. An outlier that was never iterated on is the biggest wasted asset in most channels.
3. **Outlier analysis.** Identify the top 10–20% performers. What do they share (topic, format, hook style, length)? Recommend doubling down before recommending anything new.
4. **Cadence realism.** Frequency isn't a ranking factor per-video, but volume = more lottery tickets and faster learning. Recommend a cadence the creator can sustain for 90 days, not a heroic sprint.
5. **Language/market fit.** Is the metadata language consistent with the audience being targeted? Mixed-language metadata splits the audience model.

## Scoring

Score each layer 1–5. Anchors: 1 = actively harming distribution, 3 = neutral/competent, 5 = best-practice with evidence it's working. Don't inflate — a 3 is a normal score. The overall verdict is the *lowest* layer, because Shorts performance is bottleneck-driven, not average-driven.

## Report template

ALWAYS use this structure for audit output:

```
# Shorts Audit — [channel/video name]

## Verdict
[2–3 sentences: the #1 bottleneck, the mechanism it breaks, and the single highest-leverage fix.]

## Scores
Content & Hook: X/5 — [one-line reason]
Packaging: X/5 — [one-line reason]
Channel strategy: X/5 or N/A — [one-line reason]

## What's working
[2–3 bullets — real strengths to keep, tied to evidence. Skip if auditing blind.]

## Fixes (do in this order)
1. [Highest impact — with the concrete rewrite/change, not advice]
2. ...
3. ... (max 5)

## Metadata fix table
[The before → after table from Mode 2, if metadata was flawed]

## What I'd need to go deeper
[Only if data was missing: e.g., "retention curves for the last 5 Shorts", "viewed vs swiped %"]
```

For channel audits, add a **Pattern findings** section before Fixes: outlier analysis, niche coherence verdict, and the one format worth productizing.
