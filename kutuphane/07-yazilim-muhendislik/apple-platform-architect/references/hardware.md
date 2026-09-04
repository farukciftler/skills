# Hardware: what the device can actually carry

Software decisions are constrained by silicon. This file exists so you can answer "will this run, and on what?" without guessing. Verify current lineup after each September event — this reflects August 2026, before the iPhone 18 announcement.

## Contents
- [Why this matters](#why-this-matters)
- [iPhone silicon matrix](#iphone-silicon-matrix)
- [iPad and Mac](#ipad-and-mac)
- [Apple Intelligence eligibility](#apple-intelligence-eligibility)
- [Memory budgets](#memory-budgets)
- [Neural Engine and GPU neural accelerators](#neural-engine-and-gpu-neural-accelerators)
- [Thermal behaviour](#thermal-behaviour)
- [Choosing a deployment target](#choosing-a-deployment-target)
- [Testing matrix](#testing-matrix)

---

## Why this matters

Three concrete decisions depend on hardware:

1. **Can this device run an on-device model at usable speed?** Token throughput varies roughly 1.6× between A18 and A19 Pro on the same workload. That is the difference between a feature feeling instant and feeling broken.
2. **Will this get jetsam-killed?** iOS gives apps a fraction of physical RAM. An app that works on a 12 GB iPhone 17 Pro can die on an 8 GB iPhone 16.
3. **What is the frame budget?** GPU core count and sustained thermal headroom differ by more than the marketing suggests, especially over long sessions.

## iPhone silicon matrix

| Chip | Ships in | CPU | GPU | Neural Engine | RAM | Process |
|---|---|---|---|---|---|---|
| A16 Bionic | iPhone 14 Pro, 15, 15 Plus | 6-core | 5-core | 16-core, ~17 TOPS | 6 GB | N4 |
| **A17 Pro** | iPhone 15 Pro/Pro Max | 6-core | 6-core | 16-core, ~35 TOPS | 8 GB | N3B |
| A18 | iPhone 16, 16 Plus, 16e | 6-core | 5-core | 16-core, ~35 TOPS | 8 GB | N3E |
| A18 Pro | iPhone 16 Pro/Pro Max | 6-core | 6-core | 16-core, ~35 TOPS | 8 GB | N3E |
| A19 | iPhone 17, 17e | 6-core | 5-core | 16-core + GPU neural accelerators | 8 GB | N3P |
| **A19 Pro** | iPhone 17 Pro/Pro Max, iPhone Air | 6-core (2P @ ~4.26 GHz, 4E), 16 MB L2, 32 MB SLC | 6-core (5-core in Air), ~1620 MHz | 16-core + GPU neural accelerators, ~4× A18 Pro peak compute | 12 GB LPDDR5X (9600; 8533 in Air), ~75.8 GB/s | N3P |

Notes that matter:

- **A17 Pro is the Apple Intelligence floor.** The iPhone 15 and 15 Plus shipped with A16 and 6 GB and are excluded permanently.
- **A19 Pro's 40% better sustained performance** over A18 Pro comes as much from vapor chamber cooling in the 17 Pro as from the chip. The iPhone Air has A19 Pro without vapor chamber and throttles differently.
- **GPU neural accelerators are the A19-generation story.** Every GPU core gets one; AI workloads can use Neural Engine *and* GPU together. This is why the on-device model story improves sharply at A19 even though the Neural Engine core count didn't change.
- Approximate Geekbench 6 single/multi: A17 Pro ~2,885/7,779 · A18 Pro ~3,445/9,441 · A19 ~3,320/8,373.
- **iPhone 18 lineup expected September 2026** — verify before advising on current hardware.

## iPad and Mac

- **iPad:** any M-series (M1, M2, M3, M4 and later) supports Apple Intelligence. Among A-series iPads only the current iPad mini (A17 Pro) qualifies. Base entry-level iPads on older silicon do not.
- **Mac:** every Apple silicon Mac supports Apple Intelligence, from the original M1 MacBook Air upward, plus the A18 Pro-based MacBook Neo. Intel Macs never will — no Neural Engine.
- **Mac unified memory is the enabler for serious local models.** 32 GB+ runs models that are impossible on any iPhone. If a workflow needs a genuinely capable local LLM, the Mac is the device, and MLX is the framework.
- **Apple Watch:** watchOS 27 adds Private Cloud Compute access via Foundation Models — an on-wrist app can reach Apple's server model without an API key.

## Apple Intelligence eligibility

**Supported:** iPhone 15 Pro / 15 Pro Max, every iPhone 16 model (including 16e), every iPhone 17 model (including 17e and iPhone Air) · iPads with M1 or later, plus iPad mini (A17 Pro) · all Apple silicon Macs.

**Not supported, permanently:** iPhone 15 / 15 Plus and everything earlier, A-series iPads below A17 Pro, Intel Macs.

Apple drew a further line *inside* Apple Intelligence in 2026 — some capabilities are gated to newer silicon beyond the base eligibility. Verify per-feature availability rather than assuming eligibility is binary.

**Design implication:** any app whose core value is Apple Intelligence has an addressable market smaller than "iPhone users". Always ship a defined non-AI path, and check `SystemLanguageModel.availability` at runtime rather than gating on device model strings.

## Memory budgets

Physical RAM is not what you get. iOS enforces per-app limits and jetsams over-consumers — these appear as terminations, not crashes, and are easy to miss in crash reporting.

Rough working guidance (verify against current OS behaviour with a memory-limit test on device):

| Device RAM | Comfortable app footprint | Notes |
|---|---|---|
| 6 GB (A16 and earlier) | conservative | Not Apple Intelligence eligible anyway |
| 8 GB (A17 Pro–A19) | moderate | The realistic target for on-device AI apps |
| 12 GB (A19 Pro) | generous | Headroom for larger models and bigger scenes |

Extensions get far less than the host app — widget and Live Activity extensions have tight limits, and loading a language model inside one is generally not viable. Do the work in the app, share results through an App Group.

**Loading a model is the big allocation.** Foundation Models' on-device model is system-managed and shared, which is a significant advantage — you are not paying its memory cost from your own budget. A model you bundle through Core AI or MLX *is* your budget.

## Neural Engine and GPU neural accelerators

The Neural Engine has been 16 cores since A11, but per-core capability and memory bandwidth have grown by roughly 2× from A16 to A17 Pro and again meaningfully into the A19 generation. TOPS figures (17 → 35 → higher) are marketing-adjacent; treat them as ordering, not as a performance model.

What actually predicts on-device LLM throughput:
1. **Memory bandwidth** — LLM decode is bandwidth-bound. A19 Pro's ~75.8 GB/s LPDDR5X is the practical ceiling on iPhone.
2. **Whether the GPU neural accelerators are in play** — A19 generation and later.
3. **Thermal state** — a warm phone is a slow phone.

Observed order-of-magnitude for a small on-device model: roughly 28 tokens/sec on A18, roughly 45 on A19 Pro. Treat these as illustrative, not as a spec — measure on your own workload.

**Design implication:** stream output. At 28 tokens/sec a 200-token response takes seven seconds. Streaming makes that feel responsive; waiting for the whole thing does not.

## Thermal behaviour

- Sustained load throttles on every iPhone. Benchmark numbers are peak, not sustained.
- The iPhone 17 Pro's vapor chamber materially changes this; the Air (same chip, no vapor chamber) does not get the same sustained numbers.
- `ProcessInfo.processInfo.thermalState` is observable. For anything long-running — a game session, a batch inference job, video export — react to it: reduce frame rate, pause background inference, warn the user.
- **Test warm.** A 3-minute benchmark run on a cold device tells you nothing about minute 20.

## Choosing a deployment target

The framing that produces good decisions: **what fraction of your addressable users does the previous version cost you, and what does supporting them cost in code?**

Apple OS adoption is fast — a new version typically reaches a large majority of active devices within months, and iOS 27 dropped no devices from iOS 26's list, so the base moves together. Practical rules:

- **N-1 (currently iOS 26)** — the default for a new app in 2026. Costs almost nothing in reach, gives you modern SwiftUI, Swift 6 ergonomics and Foundation Models.
- **N-2 (iOS 25/18)** — only if you have data showing your specific audience skews old. Every backported API is code you maintain.
- **N (iOS 27-only)** — only for something whose entire premise is a 27 feature, and accept the small initial audience.
- **Build SDK ≠ deployment target.** Since April 28, 2026 you must *build* with the iOS 26 SDK to upload. That does not force your minimum deployment target upward. People conflate these constantly.

## Testing matrix

The minimum honest set:

| Slot | Why |
|---|---|
| Oldest supported device | Performance and memory truth |
| A17 Pro or A18 device | The Apple Intelligence floor — where AI features feel slowest |
| Current-generation Pro | What reviewers and your own dev machine see |
| An iPad, if you ship iPad | Layout, split view, keyboard, pointer |
| Simulator | Fast iteration only. Never trust it for performance, memory, camera, or ML |

The simulator runs your Mac's silicon. Any performance conclusion drawn from it is wrong.
