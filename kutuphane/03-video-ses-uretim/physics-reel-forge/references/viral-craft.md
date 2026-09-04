# Shot craft for the physics genre

The simulation is the easy half. This file is the other half.

Contents:
1. Length and pacing
2. The first frame
3. Looping
4. Safe zones and framing
5. Camera
6. Palette and lighting
7. Audio
8. Overlays and text
9. Anti-slop checklist
10. Series thinking

---

## 1. Length and pacing

**7–15 seconds** for a pure satisfaction loop. **15–25 seconds** if there is a build-up and a payoff (tower rising then collapsing, container filling then overflowing).

Instagram now permits Reels up to 20 minutes but does not push anything over 3 minutes to non-followers, and engagement still concentrates well under 90 seconds. For this genre, none of that ceiling is relevant — the constraint is that watch-time percentage drives distribution, and a 10-second clip watched twice beats a 40-second clip abandoned at 15.

Structure inside those seconds:

| Time | What happens |
|---|---|
| 0.0–0.5 s | Motion already in progress. No establishing shot, no logo, no empty frame. |
| 0.5–2 s | The mechanism becomes legible — the viewer understands what is being attempted. |
| 2 s – (end−1.5 s) | The event. Escalation if possible. |
| last 1.5 s | Resolution, and a state that matches the opening if looping. |

The most common failure is a two-second empty frame before anything falls. That is where the audience leaves, and it is entirely self-inflicted — start capture later, or spawn the first bodies just above the frame edge so they enter on frame one.

## 2. The first frame

Assume the video is judged on a single static thumbnail-sized glance. On the first frame there should be:

- Motion, or an object in an obviously unstable position.
- A visible goal — the container, the pivot, the gap, the target.
- Strong figure/ground contrast.

If the first frame looks like a still life, the clip will underperform regardless of how good the simulation is.

## 3. Looping

A seamless loop multiplies watch time, and watch time is the distribution signal. Two ways to get one:

**Design the sim to return to its start state.** Cyclical mechanisms — pendulums, rotating pivots, a spiral that refills — can genuinely close. Best result, hardest to arrange.

**Match cut.** End the clip on a visual state closely matching frame one: same camera, similar object distribution, similar brightness. The eye forgives a lot if the composition matches. Verify by concatenating the clip to itself and watching the seam — `scripts/encode_reel.sh --loop-check` does this.

Do not crossfade. A crossfaded loop reads as a video editing artefact and breaks the illusion that this is a continuous physical event.

Also acceptable and often better: **a hard resolution ending** — everything comes to rest, one final object drops, cut. This works when there is a clear question with a clear answer, and it pairs well with a counter overlay.

## 4. Safe zones and framing

Instagram overlays UI on every Reel. Working numbers for 1080×1920:

- **Top ~250 px:** account name, sometimes an audio label.
- **Bottom ~400 px:** caption, follow button, like/comment/share/save stack.
- **Right edge ~120 px:** action button column extends up.
- **Safe region: the central 1080×1420.** Keep the payoff there.

This does not mean leaving the top and bottom empty — bland margins waste the format. Put continuing texture there: the top is where bodies fall in from, the bottom is where debris accumulates. The *event* stays central.

Test on an actual phone before publishing a series. The overlay geometry shifts between app versions, and a series that renders its counter under the follow button is a series that gets rebuilt.

## 5. Camera

- **Locked off.** No handheld shake, no random drift. The physics is the motion; competing camera motion makes both illegible.
- **Slow push or orbit is acceptable** if it is perfectly linear and slow (under ~3° per second). Anything faster fights the simulation.
- **Slightly telephoto** — 35–50 mm equivalent, not wide. Wide angles distort falling motion in a way that reads as fake, because the perspective change during the fall is not what the eye expects.
- **Orthographic** is worth trying for 2D-feeling recipes (domino lines, pendulum arrays). It reads as diagrammatic and clean, and it removes perspective-related readability problems entirely.
- **Height:** slightly above the action's midpoint, tilted down 10–20°. Pure eye-level flattens depth; steep top-down loses the fall.

## 6. Palette and lighting

**Three to five colours, decided before rendering.** Randomly-coloured bodies is the single clearest amateur tell in this genre. Pick a palette, assign by role (falling bodies / static geometry / accent / background), and hold it across a series so the channel becomes recognisable.

- **Dark background, bright bodies** is the default for a reason — phone screens are often viewed in bright rooms, and value contrast survives compression better than hue contrast.
- **One emissive accent colour** used sparingly reads as intentional and gives the eye an anchor. Used on everything, it reads as a preset.
- **Contact shadows are non-negotiable.** They are how the eye confirms objects are touching. A physics clip without them looks like objects floating past each other, no matter how correct the simulation.
- **Soft key light plus a rim** separates bodies from background. Flat ambient-only lighting makes a pile of cubes read as a single blob.
- **AgX tonemapping** handles bright emissives without the clipped, plasticky highlights that older tonemappers produce.
- **Slight motion blur** if available. Real cameras have it; without it, fast bodies strobe and look computer-generated. Godot's motion blur is limited — an alternative is rendering at 4× the target frame rate and blending frames down, which produces accumulation blur that looks genuinely photographic. Costs 4× render time, so reserve it for hero clips.

## 7. Audio

Silent physics clips underperform dramatically. Both because platforms weight audio engagement and because impact sound is what makes the physics feel *physical*.

Layer structure:

1. **Impact layer** — collision-triggered, impulse-mapped. The wiring is in `godot-pipeline.md` §7. This is the essential layer.
2. **Ambience** — a low room tone or soft pad, very quiet (−30 dB). Absence of any bed makes the impacts feel disconnected and dry.
3. **Music** — optional, and often better omitted. Pure impact audio is a recognisable aesthetic in this genre and avoids copyright and platform-audio complications. If music is used, keep it under the impacts, not over them.

Sample selection: short, dry, transient-heavy. Long reverb tails smear together into mush once a dozen bodies are colliding. Two to four variations per material, chosen randomly, prevents the machine-gun repetition effect.

Master bus: compressor then limiter, target around −14 LUFS. Mobile playback is loudness-normalised, so an uncompressed mix with 20 dB peaks gets turned down and the body disappears.

## 8. Overlays and text

Mostly: don't. The genre works because it is wordless and legible in any language.

The exceptions that reliably earn their place:

- **A counter** — objects placed, capacity filled, time survived. Converts a passive watch into a question. Large, monospaced, top-centre inside the safe zone.
- **A one-line premise** when the goal is not visually obvious. Under six words. First two seconds only, then gone.

Never: watermarks in the corner (the safe zone has no room), subtitle-style captions, animated text stings, or a channel logo bumper. Each costs first-second attention and buys nothing.

## 9. Anti-slop checklist

Before publishing, check each:

- [ ] Motion on frame one
- [ ] Contact shadows visible at every collision
- [ ] Deliberate palette, not per-object random colour
- [ ] No interpenetration visible at any point — objects passing through each other destroys credibility instantly
- [ ] No jitter in settled objects
- [ ] Impact audio present, impulse-mapped, no settling chatter
- [ ] Payoff inside the central 1080×1420
- [ ] Loop seam checked, or a clean resolution ending
- [ ] Default grey material appears nowhere
- [ ] Camera locked or moving under 3°/s
- [ ] Verified on an actual phone at actual size
- [ ] Simulation runs at plausible speed — not everything slow-motioned. Slow motion on every clip is a tell; use it on one moment, not the whole shot.

## 10. Series thinking

Single clips do not build anything. What compounds:

**Fixed format, varied content.** Same camera, same palette, same duration, same audio treatment — different mechanism each time. This is what makes a channel recognisable in a feed and what lets the production line run without redesign per clip.

**One escalating parameter across a series.** Ten links, then twenty, then fifty. Viewers who saw the earlier one are primed for the later one, and the escalation gives a reason to follow rather than just watch.

**Publish the failures too.** Simulations that explode, jam, or do something absurd frequently outperform the clean ones. Keep a folder of them rather than deleting.

**Cross-post the same master.** 1080×1920 H.264 works unchanged on Reels, Shorts and TikTok. One render, three destinations — the whole reason the pipeline targets this exact spec.
