# Procedural impact audio

No sample library. Every collision is synthesised from the physics that caused it, so 400 impacts produce 400 different sounds and the audio is automatically in sync with the picture — because it is derived from the same event stream.

Contents:
1. The architectural choice: offline, not in-engine
2. Modal synthesis in one page
3. The material bank and where its numbers come from
4. Acceleration noise — the layer everyone forgets
5. Getting reliable impact energy out of Godot
6. Rolling, sliding, and continuous contact
7. Event log schema
8. Mixing and mastering
9. Tuning by ear: what to change when it sounds wrong
10. Verification

---

## 1. The architectural choice: offline, not in-engine

There are two places the audio could be made:

**In-engine, real time.** Godot plays sounds as collisions happen; Movie Maker captures the master bus into the video file. Sync is free. But there is a per-frame CPU budget, so polyphony is capped, mode counts are small, and reverb has to be cheap.

**Offline, from an event log.** The simulation writes a list of collisions with timestamps; a separate pass renders the whole audio track at 48 kHz, then it is muxed with the video.

**For video production, offline wins, and not narrowly.** There is no real-time budget, so every impact gets its full mode bank; polyphony is unlimited; reverb and limiting are proper; the render is deterministic from the seed; and — the practical benefit that matters most day to day — **audio can be re-rendered without re-rendering video.** Changing a material from wood to metal is a 3-second job instead of a fresh 60-second capture.

Use both, for different stages:

| Stage | Approach |
|---|---|
| Authoring, judging whether a sim reads | in-engine sample playback, quick and rough |
| Seed sweeps | render silent, log events, skip audio entirely |
| Selected winners | offline modal synthesis, muxed with the full-resolution video |

When rendering the final video, render it **silent** and mux the synthesised track in. Two sources of audio in one file is how sync problems get introduced.

## 2. Modal synthesis in one page

A struck rigid body rings at its vibration modes. Each mode is an exponentially decaying sinusoid, so the sound of an impact is a sum of them:

```
s(t) = Σ  a_i · e^(−d_i · t) · sin(2π f_i t + θ_i)
```

Three quantities per mode. Where each comes from:

**f_i — frequency.** Determined by geometry and stiffness. Scale a shape-specific set of ratios by a fundamental derived from object size:

```
f_0 = f0_scale / size          (size in metres)
f_i = f_0 · ratio_i
```

The ratios matter more than people expect. A free-free bar's transverse modes go roughly `1 : 2.756 : 5.404 : 8.933` — strongly inharmonic, and that inharmonicity is *why a struck bar sounds like a bar* rather than a note. Plates and boxes are denser and less ordered. Spheres are sparse and nearly harmonic. `assets/materials.json` carries a template per shape.

**d_i — decay rate**, in units of 1/s. This comes from Rayleigh damping, and it is the single most important relationship in this whole file:

```
d_i = ½ (α + β ω_i²)      where ω_i = 2π f_i
```

Amplitude reaches −60 dB at `t = 6.91 / d_i`.

Read the formula: **α damps every mode equally; β damps high modes much harder because it multiplies ω².** That is the entire physical explanation of material timbre. Metal has a tiny β, so its highs survive and it rings. Plastic has a huge α, so everything dies at once and it ticks. Wood has a large β, so the highs vanish in milliseconds and what remains is a dull low knock. Get α and β right and the material is right; nothing else in the synthesiser comes close in importance.

**a_i — amplitude.** Depends on the impact and on *where* the object was struck: a point that is a node for one mode is an antinode for another. Solving that properly needs the eigenvectors at the contact point. A random gain per mode per hit is a cheap stand-in that is physically motivated — and it is what stops repeated impacts sounding like the same sample fired twice. Overall level scales with `√energy`, because loudness tracks amplitude far better than it tracks energy; a linear map makes soft contacts inaudible and hard ones clip.

Total level and mode count: 16 modes is plenty for wood, plastic, cardboard and rubber, whose highs are gone almost immediately anyway. Metal, glass and porcelain reward 48 or more, since that is where the audible content lives.

## 3. The material bank and where its numbers come from

The α and β values for **wood, plastic, metal, glass and porcelain** in `assets/materials.json` are the parameters estimated from real recordings by Ren, Yeh & Lin (*Example-Guided Physically Based Modal Sound Synthesis*, ACM TOG 32(1), 2013, Table I). That paper's central result is what makes them useful here: **α and β are geometry-invariant** — properties of the material rather than of the object — so parameters estimated from a recording of a plate transfer correctly to a cube, a chain link or a sphere. That is exactly the reuse this pipeline needs.

Rough behaviour at a 0.22 m object size, measured from the synthesiser:

| Material | α | β | ring to −40 dB |
|---|---|---|---|
| metal | 6.30 | 2.12e-8 | ~950 ms |
| porcelain | 0.037 | 8.41e-8 | ~510 ms |
| glass | 18.3 | 1.43e-7 | ~190 ms |
| plastic | 52.6 | 8.78e-7 | ~90 ms |
| wood | 2.14 | 3.08e-6 | ~60 ms |

Note that porcelain has near-zero α — almost no uniform damping — yet metal still rings roughly twice as long, because metal's β is four times smaller and β dominates at these frequencies. If a change to β does not audibly change the ring length, something is wrong in the mode generation, not the material.

`cardboard`, `rubber` and `stone` are extrapolated, not measured, and tuned by ear. They are labelled as such in the bank. Cardboard and rubber barely use the modal layer at all — they are almost pure click, which is exactly right.

One useful piece of perspective from that paper's perceptual study: **listeners identified real recordings of wood correctly only about half the time, routinely confusing wood with plastic, and glass with porcelain.** Do not spend hours chasing a distinction the audience cannot hear. What listeners *do* reliably hear is hard-versus-soft and big-versus-small. Spend the effort there.

## 4. Acceleration noise — the layer everyone forgets

Modal ringing is not the whole impact. There is also a broadband transient radiated by the sudden change in the body's velocity, independent of any resonance (Chadwick et al., 2012, on precomputed acceleration noise). It lasts two to twelve milliseconds.

It is the difference between a *thwack* and a disembodied *ting*. A modal-only impact sounds synthetic in a way that is hard to name until the click is added, at which point the sound suddenly has a physical body. Skip it and no amount of material tuning will fix the result.

Implementation: a short noise burst with a fast exponential decay, band-limited per material.

- **Hard materials** (metal, glass, porcelain, stone): short, 1–3 ms, high-passed, full bandwidth above that.
- **Soft materials** (rubber, cardboard): longer, 7–12 ms, and **low-passed as well**. An unbounded noise burst on rubber reads as a bright hiss, which is exactly wrong — the transient should be dull. This is what `click_lp_hz` in the bank controls.
- Scale click level with the modal peak so the balance holds across impact strengths.

## 5. Getting reliable impact energy out of Godot

**`PhysicsDirectBodyState3D.get_contact_impulse()` is not trustworthy for this.** It reports a zero vector on the first frame of a contact — which is the only frame a bouncy body may have, so the loudest impacts report silence — and its values have been inconsistent across versions. Building the audio chain on it produces a mix where the biggest hits are missing.

Derive the energy instead. It is more reliable and it is the physically meaningful quantity anyway:

```
E = ½ · m_eff · v_rel²        m_eff = m₁m₂/(m₁+m₂)   (= m₁ against static geometry)
```

The critical detail: **capture velocities on the tick before the solver runs.** After the solve, the approach velocity is already gone and the energy reads as near zero. `assets/contact_log.gd` does this by snapshotting `linear_velocity` for every tracked body each `_physics_process` with `process_priority = -100`, then using the snapshot when `body_shape_entered` fires.

Three further details that matter:

- **Per-pair cooldown.** Without it, one contact fires repeatedly across consecutive ticks and a single collision becomes a machine-gun burst.
- **Energy threshold.** A settling pile generates hundreds of micro-contacts. Without a floor, the result is a continuous hiss of clicks. This is the most important single tuning knob in the whole audio chain — more important than any material parameter, because it decides what is a sound event at all.
- **The harder material wins.** A wooden cube landing on a steel plate rings the plate; it does not thud like wood. Tag static geometry with a material and pick the harder of the pair.

## 6. Rolling, sliding, and continuous contact

Impacts alone leave a scene feeling stilted, because real objects also roll and scrape.

Both are the same mode bank excited by a *continuous* force instead of an impulse:

- **Rolling** — a train of micro-impacts from surface irregularity. Low-passed noise, rectified so the contact force is one-sided, then run through the resonators. Amplitude and bandwidth scale with angular velocity. Trigger when a body has contacts and its angular velocity exceeds a threshold.
- **Sliding/scraping** — broadband friction. High-passed noise through the same resonators. Amplitude scales with tangential velocity times normal force.

Keep both well under the impacts — around −10 dB relative. They are texture, not events. Overdone, they turn into a constant wash that buries the thing the viewer is actually watching.

## 7. Event log schema

```json
{
  "sample_rate": 48000,
  "duration": 13.0,
  "seed": 1001,
  "physics_ticks_per_second": 180,
  "events": [
    {"t": 0.512, "energy": 3.4, "material": "wood", "size": 0.22, "x": -0.6, "kind": "impact"},
    {"t": 1.02, "energy": 0.8, "material": "metal", "size": 0.18, "x": 0.3,
     "kind": "roll", "duration": 0.2}
  ]
}
```

`t` is derived as `tick / physics_ticks_per_second`, which is why determinism matters: the same seed produces the same event list, so audio and video stay locked without any alignment step.

`x` drives constant-power stereo panning. Keep the width moderate (0.6 or so) — hard-panned impacts are distracting on headphones and vanish entirely on a phone speaker, which is where most of the audience is.

## 8. Mixing and mastering

Order matters:

1. **Sum** all events with per-event gain and pan.
2. **Reverb**, 20–35% wet, short decay (0.35–0.5 s), with a few milliseconds of pre-delay so transients stay dry and defined. Impacts with no space at all sound like they were recorded in a vacuum; too much and the piece turns to mud once a dozen objects are colliding.
3. **Compression**, threshold around −18 dB, ratio 4:1. Physics audio has an enormous crest factor. Without this the mix sounds thin the moment a platform normalises it.
4. **Loudness match to about −14 LUFS**, then limit — and re-measure, because limiting changes loudness. A limiter that rescales the whole signal undoes the loudness targeting it was supposed to protect; use a soft-knee limiter that only touches peaks, and iterate the match two or three times.

For a series, consistency matters more than any individual number. Run `ffmpeg loudnorm` in two-pass mode on the finals so every clip lands at the same perceived level.

## 9. Tuning by ear: what to change when it sounds wrong

| Symptom | Cause | Fix |
|---|---|---|
| Constant hiss of tiny clicks | settling contacts below the noise floor of interest | raise `MIN_ENERGY` in the logger |
| One collision sounds like a burst | contact firing on consecutive ticks | raise `COOLDOWN_TICKS` |
| Impacts sound synthetic, "ting" not "thwack" | no acceleration noise | raise `click_gain`; check the click is actually being added |
| Everything sounds like the same object | mode gains not varying per hit | check the per-hit random gain and inharmonic scatter are active |
| Rubber and cardboard sound bright and hissy | click not band-limited | set `click_lp_hz` |
| Metal doesn't ring | β too large, or too few modes | lower β; raise mode count to 48+ |
| Mix is loud but feels weak | crest factor, no compression | check compressor is engaged before the loudness match |
| Wall of noise at a collapse | too many simultaneous events | raise the energy threshold; the ear cannot resolve more than ~20 impacts a second anyway |
| Audio drifts out of sync | sim logic in `_process` rather than `_physics_process` | move it; only fixed-tick timestamps are reliable |

## 10. Verification

Do not trust the ear alone on a first setup — measure. Render a single impact per material and check:

- **Ring length ordering.** Metal > porcelain > glass > plastic ≈ stone > wood > cardboard ≈ rubber. Measure on a smoothed RMS envelope, not raw samples: raw samples cross zero constantly and any naive threshold test will report nonsense.
- **Spectral centroid ordering.** Hard materials higher, soft materials lower.
- **Size drives pitch.** Halving `size` should roughly double the dominant frequency. If it doesn't, the fundamental is not being derived from geometry and every object will sound the same size.

`scripts/synth_impacts.py --report` prints event statistics and flags the two failure modes that ruin a mix before it is rendered: event rates above roughly 120/s (which read as noise rather than as objects) and energy ranges spanning more than about 5000× (where the quiet tail is inaudible no matter what the mastering does).
