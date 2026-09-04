# Shorts strategy — what actually gets watched, and how often to post

Research pass, August 2026. Prompted by the stickman tournament (three
technically solid cuts, no traction): the problem was not execution, it was
format. This file is the format map, the cadence rules, and what both mean for
this pipeline. Binding rules distilled from it live in `CLAUDE.md` § "Shorts
format & cadence rules"; the pick-a-format checklist is the `shorts-strategy`
skill.

## 1. The format hierarchy in simulation Shorts

The genre is not a meritocracy of craft. It is a handful of *proven formats*
that the feed already knows how to route, plus a long tail of everything else.
The stickman bracket was in the long tail: a one-shot narrative with no
escalation curve, no open question, and a winner card that closes the loop and
invites the swipe.

### Tier 1 — "Will the ball escape?" (ball-escape / bouncing-ball brainrot)

The dominant simulation format since late 2023, and still the highest-ceiling
one ([Know Your Meme](https://knowyourmeme.com/memes/will-the-ball-escape-ball-bouncing-brainrot)):

- One or more **colour-shifting balls bounce inside concentric rings/circles**,
  breaking walls, multiplying, or gaining speed/size with each impact.
- Reference numbers: satisfying.ba11s **67M views** on a single video (Dec
  2023), another at **38M in five months**; CodeCraftedPhysics 4.4M with
  regenerating wall layers. Format born 7 Nov 2023 (a square in a shrinking
  square, 191k views).
- **Melody sync is half the format**: each bounce plays the next note of a
  recognisable song, so the melody resolves as the ball accelerates. The
  audience literally waits for the tune to complete.
- The engine of it is a **question with a visible payoff**: "will it escape?"
  Every slip-through pays off — a wall shatters, a colour floods, the ball
  splits. Tension is structural, not scripted.

Why this matters here: **this is a rigid-body format.** A ball, kinematic
rotating arcs with gaps, contact events. The pipeline's contact log already
drives audio synthesis; a pitch ladder over it is melody sync. This is the
single best fit between what hypes and what `forge` can build.

### Tier 2 — escalation loops (multiply / fill / break)

Same grammar, different verbs: ball splits on every bounce until the screen
fills; balls break bricks and flood a shape with colour; an object grows until
it no longer fits. All rigid-body compatible. The shared skeleton:

1. **State that only moves one way** (count, size, speed, coverage).
2. **A visible end condition** the viewer can see coming.
3. **Reaching it ends the video** — ideally on a frame that matches frame one.

### Tier 3 — marble race (what we already have)

Proven but crowded; Jelle's Marble Runs built 1.4M subs on it and the Algodoo
lineage is long. It works when it has **stakes and identity** — named teams,
elimination rules, a championship arc — not just motion
([Wikipedia](https://en.wikipedia.org/wiki/Jelle%27s_Marble_Runs)). Our
gauntlet with its enforced ≥4 lead changes is a sound Tier-3 entry; it will
grind, not spike.

### What doesn't work (for us, now)

- **One-shot narratives** (the stickman bracket): no escalation, closed ending,
  format is the star and this isn't a format the feed knows.
- **Soft-body** remains the 2025–26 trend leader and rigid bodies cannot fake
  it — already documented in hype-scenarios.md; don't retry.
- **Craft-first clips** (our quality pass) matter only *within* a working
  format. Polish does not rescue a format the feed has no lane for.

## 2. The mechanics of why these formats hold retention

- **Hook inside 0.5–2 s**: the question must be visible before the first swipe
  impulse — ball already moving, gap already visible, text overlay stating the
  stake ("ESCAPE IN 60s?"). ([Shortimize](https://www.shortimize.com/blog/how-does-youtube-shorts-algorithm-work), [Metricool](https://metricool.com/youtube-shorts-algorithm/))
- **Retention is the ranking currency.** Average percentage viewed ~70%+ is
  healthy; Shorts average ~73%. The algorithm promotes performance relative to
  impressions, not upload volume. ([Shortimize retention benchmarks](https://www.shortimize.com/blog/youtube-shorts-retention-rate))
- **Loops push APV over 100%.** Ending frame ≈ opening frame means accidental
  rewatches; >100% watched is one of the strongest promote signals a Short can
  emit. Design the escape/fill/finish to land visually where the clip began.
  ([Digital Blacksmiths](https://digitalblacksmiths.io/youtube-shorts-algorithm-secret-loopable-videos-increase-watch-time/), [nealschaffer.com](https://nealschaffer.com/youtube-shorts-looping/))
- **Escalation defers the payoff without boring the viewer** — speed/melody
  curves give continuous progress; the brain stays for the resolution.
- **Comment bait is structural**: "will it escape?" formats collect guesses;
  melody formats collect song-name comments. Engagement is a by-product of the
  format, not a CTA.

## 3. Cadence — how often to publish

Consensus across 2025–26 sources ([AIR](https://air.io/en/youtube-hacks/the-death-of-daily-uploads-what-cadence-actually-triggers-algorithm-love-in-2025), [Theme Circle](https://www.themecircle.net/youtube-upload-frequency-explained-what-works-best-in-2026/), [Metricool](https://metricool.com/youtube-shorts-algorithm/), [Conbersa](https://www.conbersa.ai/learn/youtube-shorts-upload-strategy)):

- **Floor: 3–4/week.** Below ~3/week each Short starts cold; the channel never
  builds a routing pattern.
- **Sweet spot: 1, at most 2 per day** of one consistent format. 3–4/week of
  high-retention beats 7/week of mediocre — a weekly 60%-retention Short
  outranks a daily 25% one.
- **Volume ≠ growth, but reps = calibration**: channels tend to need ~200
  Shorts before view patterns stabilise. Expect the first months to be
  parameter search, and instrument accordingly (track APV per variant).
- Posting time is a second-order effect; consistency of format and cadence is
  first-order. Our own publishing-throughput notes already cap the honest rate
  (content checks ~9 min each, overlap them; hourly floor for a 5-batch).

## 4. Channel strategy

- **2–3 repeatable series, recognisable at a glance** — same palette, same
  framing, numbered titles ("ESCAPE #47"). Sessions of same-series watching
  teach the algorithm who to route the next one to. ([vidIQ](https://vidiq.com/blog/post/understanding-youtube-algorithm/), [dataslayer](https://www.dataslayer.ai/blog/youtube-algorithm-2025-how-to-get-your-videos-recommended))
- **The 30-video test**: if a format cannot obviously produce 30 videos from
  the same recipe with different seeds/parameters, it is not a series, it is a
  stunt. (The stickman bracket fails this test; ring-escape passes trivially.)
- **Do not delete low-view videos for the view count alone.** Deleting erases
  the watch time and engagement they contributed, breaks every inbound link
  permanently (YouTube has no redirects), and the algorithm does not punish a
  back catalogue of duds — it ranks what works. Delete only what is off-niche,
  outdated, or policy-risky; otherwise set stray experiments to Private and
  keep the stats. ([AIR](https://air.io/en/youtube/yes-you-can-delete-your-old-videos-but-heres-the-catch), [vidIQ](https://vidiq.com/blog/post/delete-old-youtube-videos/), [The Marketing Heaven](https://themarketingheaven.com/should-i-delete-youtube-videos-with-low-views/))

## 5. What this pipeline should build next (mapped to capability)

Priority order, all rigid-body, all sim-cheap:

1. **`ring-escape`** — ball inside 6–10 concentric kinematic arc rings, each
   with a gap, counter-rotating; ball speeds up per bounce (restitution >1 or
   impulse feed); breaking through a ring shatters it (release its segments as
   dynamic debris). Contact events → melody notes on a pitch ladder
   (extend `synth_impacts.py` with a `melody` map: nth impact → nth note of a
   configured tune). Title format: "ESCAPE #N". Text hook baked by
   `textcard.swift`: "Will it escape?"
2. **`ball-split`** — every wall hit spawns a clone until a count cap; end
   state = screen full = loop point back to one ball.
3. **`brick-flood`** — ball(s) erode a brick wall filling a silhouette with
   colour; completion frame composed to match the opening frame.
4. Keep **gauntlet** as the Tier-3 series (named teams, championship
   numbering), 2–3/week alongside the daily Tier-1 series.

Instrumentation to add when publishing: log per-video APV and swipe data into a
CSV next to the seed/params, so the ~200-Short calibration phase is an actual
parameter sweep and not vibes.
