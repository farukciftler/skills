# Per-episode research — August 2026 wave

Condensed findings from the per-episode deep-research passes (full agent
reports lived in session; sources inline). Companion to
`melody-sync-research-2026-08.md` and `oneshot-inorder-research-2026-08.md`.

## ESCAPE #4 — "TURBO" accelerando episode (18 Aug)

- **Series variation doctrine**: structural DNA fixed (format, palette,
  numbered title, opening pattern), one secondary axis varies per episode.
  No measured comparison of variation axes exists — the song is this format's
  primary variable; speed is the correct *additional* axis.
  ([Postoria](https://postoria.io/blog/youtube-shorts-series-playlists-retention-scaling))
- **Melody tempo science (the key numbers)**: familiar melodies are
  identifiable at ~0.8–6.0 notes/s; best recognition at ~3.0; degrades at 6.0
  ([PubMed 9793121](https://pubmed.ncbi.nlm.nih.gov/9793121/),
  [PubMed 18459260](https://pubmed.ncbi.nlm.nih.gov/18459260/)). Brain
  recognizes a familiar tune in 100–300 ms
  ([ScienceDaily](https://www.sciencedaily.com/releases/2019/10/191030073312.htm)).
  → **Accelerando, not constant-fast**: first ~10 notes at 3–4 notes/s
  (recognition window), peak ≤6.5, never >8.
- **Turkish March**: established viral TikTok sound; recognition lands ~5th
  note (the C drop in B-A-G#-A-C), guaranteed by ~9-10.
  Avg name-that-tune recognition is 6 notes
  ([APA Monitor](https://www.apa.org/monitor/jun06/tune.html)).
- **Params shipped**: `spin_scale` 1.25/1.35/1.5 mini-sweep (profile
  (0.40+0.12·i)·scale), `speed_max` 4.6, `v0` 1.5, shatter window 26–44 s,
  accent palette slot → amber #ff8c2d, title "Guess the Song — TURBO
  ESCAPE #4 ⚡".
- Gaps: no measured comparison of variation axes; no documented "no way it
  escapes this" comment evidence; speed-run demand inferred from tool
  ecosystems packaging it as a mode
  ([ViralBalls](https://viralballs.com/en/blog/10-satisfying-ball-physics-video-ideas-that-go-viral)).

## MULTIPLY #3 — "The Floor Opens" drain-loop (17 Aug)

- **Pure drain is an empty niche** — no "swarm drains to one" format found;
  nearest kin are gravity-well/hourglass ASMR. Frame it as **elimination
  ("SURVIVOR"), not loss** — last-one-standing is a winner (marble-race
  convention), and fail-endings are algorithmically punished.
- **Reverse-payoff loop** (1→240→1): no direct empirical evidence exists; it
  is the narrative version of the visual loop (last frame IS the first state).
  Musical unbuild is standard production practice (trance outros strip
  elements over 32–64 bars —
  [Myloops](https://www.myloops.net/trance-song-structure-breakdown-basics)).
- **Granular physics** (measured): flow ~Beverloo (D−kd)^{5/2}; 3D critical
  outlet ~5 grain diameters; 2D jam probability falls fast with R=D/d, R≥5-6
  effectively never jams for 240 live (agitated) balls
  ([Janda 2D silo](https://www.researchgate.net/publication/235675878_Jamming_and_critical_outlet_size_in_the_discharge_of_a_two-dimensional_silo),
  [Zuriguel clogging](https://arxiv.org/pdf/1412.5806)).
  → gap arc 6–7 ball diameters (0.29–0.34 m at arena_r 0.6), friction ≤0.1.
- **Drain pacing**: live-ball drain is exponential decay, 240→1 ≈ 5.5τ;
  target τ≈4–4.5 s → ~22–26 s drain. The exponential shape IS the reverse
  dramaturgy (gush → thinning → slow final balls).
- **Structure chosen**: compressed fill (quota 1.2 s ×0.85 → full ~18-20 s)
  + dwell 2.5 s + drain ~20-23 s + sealed last ball, ~48-52 s total. Loop
  frame picked from motion.bin by matching final-ball pose+velocity to an
  opening frame.
- **Last-ball moment**: freeze → 1/3 slow-mo → solo hero phrase (elimination
  winner convention + stickman findings).

## ONE SHOT #2 — "Pull One Block." Jenga (19 Aug)

- **Genre exists** (TikTok discover pages for Jenga collapses; slow-mo + ASMR
  block sounds is the formula) but no per-clip view counts verifiable — gap.
- **Torsion beats pancake and is the natural physics**: a tower rotates
  around the remaining support edge, it doesn't drop
  ([APlusPhysics](https://aplusphysics.com/community/index.php?%2Fblogs%2Fentry%2F30349-jenga%2F=),
  [Riddler sim](https://mihagazvoda.com/posts/riddler-jenga/)). Pull an EDGE
  block from row 2–3 (not bottom row, not center) for guaranteed asymmetry.
- **The definitive sim reference**: CMU/Sony "Strategic Jenga Play"
  ([arXiv 2505.09377](https://arxiv.org/pdf/2505.09377)) — jitter must be in
  block DIMENSIONS and mass (±0.8% half-extents, ±5% mass), not just pose;
  friction calibrated until **~47% of blocks are movable** (matches MIT
  hardware measurements, Science Robotics 2019); push-through stick beats a
  gripper.
- **Numbers**: wood friction ~0.3–0.4 (sweep 0.28–0.45 per-block ±0.08),
  restitution 0.05–0.1, floor friction 0.6–0.7, tower 20 rows × 3, blocks
  0.75×0.25×0.15 m (5× real), pull 0.25–0.35 m/s (block clears ~2.7 s),
  ground micro-vibration ±0.5 mm 8–12 Hz for the frame-0 tremble (real
  physics + free creak audio).
- **Tension gap**: no measured number for physical-tension holds — 1.5 s
  safe if the "nothing" is micro-tremble + settle ticks, not a dead frame.
- **Survival episodes**: publishable but rare (~1 in 8-10) and only if
  dramatic (top-third sway ≥5-6° then recovery); pinned "Seed 41 survived.
  Pull another?".
- **Camera**: 4-6% push-in over the pull+tension, damped-sine shake at first
  big impact, locked after; loop via composition (frame 0 = block half-pulled
  + trembling tower).
- **Selection criteria** (collapse_report.py): collapse onset 1.0–2.2 s after
  block clears; top-third net yaw ≥10° (torsion); debris spread 1.2–2.2×
  base; collapse+settle 3–5 s; single-peak contact-rate histogram; survival
  flag = <10% displaced + sway ≥5°.

## Production-side lessons this wave

- **Loop takes are ~60 MB each** (double body count) — sweeps must prune
  losing takes immediately after scoring, or 120 sims = 7 GB and the disk
  fills. Never leave a full sweep tree on disk.
- Studio upload editor: never write metadata before the editor settles —
  the filename prefill overwrites late inserts. Mouse-first (triple-click)
  + real keyboard is the reliable path; tags always real keyboard.
