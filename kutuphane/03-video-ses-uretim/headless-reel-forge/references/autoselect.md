# Scoring takes without rendering them

`pipeline/score_take.py`. This is the stage that makes the pipeline economical, and it is also the one that needs judgement, because it encodes an aesthetic.

## What it is for

Every take is physically correct. The score does not measure correctness — it measures whether the *shot* works, from data that is already on disk. Rendering is the only expensive stage, so every take rejected here is a render that never happens.

The score is also the fastest feedback loop available for tuning a recipe. It answers "is my container too wide" in 4 milliseconds instead of 20 seconds, and it answers it in the same terms the renderer will.

## The components

| Component | Weight | What it reads |
|---|---|---|
| `action_spread` | 0.30 | Per-frame displacement of released bodies, bucketed into seconds. The fraction of buckets above 8% of the peak bucket. Catches "all the action is in the first three seconds". |
| `in_frame` | 0.30 | Final positions projected through the **real render camera** into NDC; the fraction inside the frame. Bodies behind the camera project to infinity and never count as visible. |
| `settled` | 0.15 | Mean speed over the last 0.4 s, mapped to 0 at 0.5 m/s. A clip that cuts mid-motion has no payoff. |
| `fill` | 0.15 | Screen-space spread of the final arrangement. A correct simulation that ends as a small heap in the middle of a tall frame is a wasted upload. |
| `no_escapes` | 0.10 | Bodies below the lowest static geometry. Falling through the floor is rare and fatal. |

Reported but **not scored**, because they mean different things per recipe:

- `loop_error` — mean distance between the first and last pose. Only meaningful for recipes with no spawn schedule; with one, parked bodies dominate it and the number is noise.
- `event_rate` — contact events per second. Below ~5 the track will be silent; above ~120 the impacts smear into hiss. Both produce a note.

## The parking distinction

A body still sitting at the recipe's parking position has not entered the shot yet. It is *not* off-screen — it is not yet released, and counting it as a failure would punish exactly the spawn scheduling that makes the clip work. `bodies.json` records the parking point and the scorer masks against it. Any new criterion has to respect the same distinction.

## How well it actually discriminates

Honestly: it depends entirely on how much the recipe leaves to the seed, and the two shipped recipes bracket the range.

**cube-rain**, 12 seeds, well-tuned parameters:

```
0.936  0.934  0.934  0.934  0.933  0.932  0.931  0.931  0.929  0.928  0.928  0.927
```

A 0.009 spread. Every roll is fine, and the ranking is close to arbitrary — a container with walls does not leave much for the seed to ruin.

**chain-drop**, 12 seeds, same sweep:

```
0.37  0.37  0.37  0.37  0.31  0.31  0.31  …
```

Wide spread and a clear failure mode named in the notes (`bodies leave the frame` — the chain whips off the peg and lands low), which is real and actionable.

The lesson: **the score is a rejection filter, not a taste ranking.** When a sweep clusters, that is information — the recipe is robust and the seed barely matters, so stop sweeping seeds and start sweeping *parameters* (drop height, count, restitution, bias), where the variance actually lives. When it spreads, the notes tell you what to fix.

Do not read a 0.936 as better than a 0.934. Do read a 0.37 as a shot that needs work.

## Reweighting

`WEIGHTS` at the top of the file is meant to be edited per recipe family. There is no universal aesthetic; there is a consistent one, and consistency is what makes a sweep rankable at all.

- **Fill/pour shots** — as shipped. `fill` and `settled` carry the payoff.
- **Collapse/domino shots** — raise `action_spread`, drop `settled` (the interest is the fall, not the rest state).
- **Loop shots** — add `loop_error` with real weight and drop `settled` to zero; the clip is meant to be caught mid-motion.

## Adding a criterion

Anything computable from `motion.bin`, `bodies.json` and `events.jsonl` is fair game and costs nothing. Ideas that have earned their place elsewhere:

- **Occlusion churn** — how often bodies cross in front of each other, as a proxy for visual busyness.
- **Silhouette change per second** — a clip whose outline stops changing has stopped being interesting before it stopped moving.
- **First-second motion** — the hook. A shot that is static for the first 30 frames loses the scroll regardless of what happens later.
- **Colour balance in frame** — how evenly the palette is distributed across the final arrangement.

Add it to the returned `parts`, give it a weight, and add a note that says what to *do* when it is low. A score with no actionable note is a number nobody uses.
