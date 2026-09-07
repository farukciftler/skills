#!/usr/bin/env python3
"""
synth_impacts.py — turn a physics collision log into a finished audio track.

Offline modal synthesis. The simulation writes an event log; this renders every
impact from material parameters instead of playing samples, so 400 collisions
produce 400 genuinely different sounds with no library and no repetition.

Why offline rather than in-engine: there is no real-time budget, so every event
gets its full mode bank, the polyphony is unlimited, reverb and limiting are
proper, and the audio can be re-rendered without touching the video.

Usage:
    ./synth_impacts.py events.json -o track.wav
    ./synth_impacts.py events.json -o track.wav --materials assets/materials.json
    ./synth_impacts.py events.json -o track.wav --reverb 0.35 --lufs -14
    ./synth_impacts.py events.json --report          # analyse, render nothing

Event log schema (written by assets/contact_logger.gd):
{
  "sample_rate": 48000,
  "duration": 13.0,
  "seed": 1001,
  "events": [
    {"t": 0.512, "energy": 3.4, "material": "wood", "size": 0.22, "x": -0.6, "kind": "impact"},
    {"t": 1.02, "energy": 0.8, "material": "metal", "size": 0.18, "x": 0.3,
     "kind": "roll", "duration": 0.7}
  ]
}

  t         seconds from clip start
  energy    impact energy proxy — 0.5*m_eff*v_rel^2, in joules-ish. Only the
            relative scale matters; the mix is normalised at the end.
  material  key into the material bank
  size      characteristic dimension in metres; sets the fundamental
  x         horizontal position in metres, for stereo placement
  kind      "impact", "roll" or "slide"
"""

import argparse
import json
import math
import sys
import wave
from pathlib import Path

import numpy as np

SPEED_OF_SOUND_REF = 1.0  # placeholder; f0 comes from the material's f0_scale
EPS = 1e-12


# --------------------------------------------------------------- material bank

DEFAULT_BANK = Path(__file__).resolve().parent.parent / "assets" / "materials.json"


def load_bank(path):
    if not path.is_file():
        sys.exit(f"material bank not found: {path}")
    bank = json.loads(path.read_text())
    if "materials" not in bank or "shape_templates" not in bank:
        sys.exit("material bank must contain 'materials' and 'shape_templates'")
    return bank


def mode_set(mat, template, size, rng, n_modes):
    """Build (freqs, decays, gains) for one struck object.

    Frequencies come from the shape's ratio template scaled by a fundamental
    derived from object size. Decay rates come from Rayleigh damping, which is
    the whole reason a material sounds like itself:

        d_i = 0.5 * (alpha + beta * omega_i^2)

    Because beta multiplies omega squared, high modes die fastest. Metal has a
    tiny beta and rings; plastic has a large alpha and thuds. Nothing else in
    this function matters as much as those two numbers.
    """
    size = max(float(size), 0.01)
    f0 = mat["f0_scale"] / size

    ratios = np.array(template, dtype=np.float64)
    if n_modes > len(ratios):
        # Extend the template by continuing its spacing, so bigger mode counts
        # stay in the same family instead of collapsing onto a harmonic series.
        last, step = ratios[-1], ratios[-1] - ratios[-2]
        extra = last + step * np.arange(1, n_modes - len(ratios) + 1)
        ratios = np.concatenate([ratios, extra])
    ratios = ratios[:n_modes]

    # Per-hit inharmonic scatter. Physically this stands in for the object not
    # being an ideal shape; perceptually it is what stops repeated hits sounding
    # like the same sample fired twice.
    scatter = 1.0 + mat.get("inharmonicity", 0.05) * rng.standard_normal(len(ratios))
    freqs = f0 * ratios * np.clip(scatter, 0.5, 2.0)

    nyq = 24000.0
    keep = (freqs > 20.0) & (freqs < nyq * 0.95)
    freqs = freqs[keep]
    if freqs.size == 0:
        freqs = np.array([min(f0, 8000.0)])

    omega = 2.0 * np.pi * freqs
    decays = 0.5 * (mat["alpha"] + mat["beta"] * omega ** 2)
    decays = np.maximum(decays, 0.5)

    # Hit position determines which modes get excited. A node for one mode is an
    # antinode for another, so a uniform random gain per hit is a decent and very
    # cheap stand-in for solving the eigenvector at the contact point.
    rolloff = mat.get("mode_gain_rolloff", 1.0)
    gains = (freqs / freqs[0]) ** (-rolloff) * rng.uniform(0.25, 1.0, size=freqs.size)

    return freqs, decays, gains


# ------------------------------------------------------------------- synthesis

def render_impact(mat, template, size, energy, rng, sr, n_modes, max_len_s):
    """One impact: a modal ring plus an acceleration-noise click."""
    freqs, decays, gains = mode_set(mat, template, size, rng, n_modes)

    # Render only as long as the slowest mode stays audible (-60 dB).
    tail = float(np.max(6.91 / decays))
    length = int(min(tail, max_len_s) * sr) + 1
    if length < 8:
        length = 8
    t = np.arange(length, dtype=np.float64) / sr

    # Modal sum. Each mode is a_i * exp(-d_i t) * sin(2 pi f_i t).
    env = np.exp(-np.outer(decays, t))
    osc = np.sin(2.0 * np.pi * np.outer(freqs, t) + rng.uniform(0, 2 * np.pi, (freqs.size, 1)))
    modal = (gains[:, None] * env * osc).sum(axis=0)

    # Acceleration noise: the broadband transient radiated by the sudden change
    # in velocity, distinct from the modal ringing (Chadwick et al. 2012). Only
    # a few milliseconds, but it is the difference between a "thwack" and a
    # disembodied "ting" — without it impacts sound synthetic.
    click_len = max(4, int(mat.get("click_ms", 3.0) * 1e-3 * sr))
    click = rng.standard_normal(click_len)
    click *= np.exp(-np.arange(click_len) / (click_len / 3.0))
    click = highpass(click, mat.get("click_hp_hz", 1500.0), sr)
    # Soft materials need the click band-limited, not just high-passed: an
    # unbounded noise burst reads as a bright hiss, which is exactly wrong for
    # rubber or cardboard where the transient should be dull.
    lp = mat.get("click_lp_hz")
    if lp:
        click = lowpass(click, float(lp), sr)
    out = modal.copy()
    out[:click_len] += click * mat.get("click_gain", 1.0) * np.max(np.abs(modal) + EPS)

    # Impact energy sets amplitude. Loudness scales roughly with the square root
    # of energy, which is far closer to how the ear reads a heavier hit than a
    # linear map — linear makes soft contacts inaudible and hard ones clip.
    amp = math.sqrt(max(energy, 0.0))
    peak = np.max(np.abs(out))
    if peak > EPS:
        out = out / peak * amp
    return out


def render_continuous(mat, template, size, energy, duration, rng, sr, n_modes, kind):
    """Rolling or sliding: the same mode bank excited by a continuous noisy force
    rather than a single impulse. Rolling is a train of micro-impacts (bumpy,
    low-passed); sliding is broadband friction. Both are resonated by the object
    so they still sound like its material."""
    length = max(8, int(duration * sr))
    freqs, decays, gains = mode_set(mat, template, size, rng, min(n_modes, 24))

    excite = rng.standard_normal(length)
    if kind == "roll":
        # Bumpy contact: low-passed noise, so the excitation is a rumble.
        excite = lowpass(excite, 400.0, sr)
        excite = np.abs(excite)          # contact force is one-sided
        excite -= excite.mean()
    else:
        excite = highpass(excite, 800.0, sr)

    # Resonate: run the excitation through each mode as a two-pole resonator.
    out = np.zeros(length)
    for f, d, g in zip(freqs, decays, gains):
        out += g * resonate(excite, f, d, sr)

    fade = max(4, int(0.01 * sr))
    win = np.ones(length)
    win[:fade] = np.linspace(0, 1, fade)
    win[-fade:] = np.linspace(1, 0, fade)
    out *= win

    amp = math.sqrt(max(energy, 0.0))
    peak = np.max(np.abs(out))
    if peak > EPS:
        out = out / peak * amp * 0.35   # continuous layers sit under impacts
    return out


def resonate(x, freq, decay, sr):
    """Two-pole resonator at freq with the given decay rate (1/s)."""
    r = math.exp(-decay / sr)
    theta = 2.0 * math.pi * freq / sr
    a1 = -2.0 * r * math.cos(theta)
    a2 = r * r
    gain = 1.0 - r
    if _lfilter is not None:
        return _lfilter([gain], [1.0, a1, a2], x)
    y = np.zeros_like(x)
    y1 = y2 = 0.0
    for n in range(x.size):
        y0 = gain * x[n] - a1 * y1 - a2 * y2
        y[n] = y0
        y2, y1 = y1, y0
    return y


# ------------------------------------------------------------------- filtering

try:
    from scipy.signal import lfilter as _lfilter
except ImportError:                       # numpy-only fallback
    _lfilter = None


def _biquad(x, b0, b1, b2, a1, a2):
    if _lfilter is not None:
        return _lfilter([b0, b1, b2], [1.0, a1, a2], x)
    y = np.zeros_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for n in range(x.size):
        y0 = b0 * x[n] + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        y[n] = y0
        x2, x1 = x1, x[n]
        y2, y1 = y1, y0
    return y


def highpass(x, cutoff, sr, q=0.707):
    w = 2.0 * math.pi * min(cutoff, sr * 0.45) / sr
    alpha = math.sin(w) / (2.0 * q)
    cosw = math.cos(w)
    a0 = 1.0 + alpha
    return _biquad(x, (1 + cosw) / 2 / a0, -(1 + cosw) / a0, (1 + cosw) / 2 / a0,
                   -2 * cosw / a0, (1 - alpha) / a0)


def lowpass(x, cutoff, sr, q=0.707):
    w = 2.0 * math.pi * min(cutoff, sr * 0.45) / sr
    alpha = math.sin(w) / (2.0 * q)
    cosw = math.cos(w)
    a0 = 1.0 + alpha
    return _biquad(x, (1 - cosw) / 2 / a0, (1 - cosw) / a0, (1 - cosw) / 2 / a0,
                   -2 * cosw / a0, (1 - alpha) / a0)


# ------------------------------------------------------------------ mix bus

def make_reverb_ir(sr, decay_s=0.45, rng=None):
    """Exponentially decaying noise IR. Crude but effective: physics impacts are
    transient, and any small amount of space stops them sounding like they were
    recorded inside a vacuum."""
    rng = rng or np.random.default_rng(7)
    n = int(decay_s * sr)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (decay_s * sr / 5.0))
    ir = highpass(ir, 300.0, sr)
    ir[: int(0.004 * sr)] = 0.0           # small pre-delay, keeps transients dry
    return ir / (np.max(np.abs(ir)) + EPS)


def convolve(x, ir):
    n = 1 << (int(x.size + ir.size - 1).bit_length())
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[: x.size]


def compress(x, threshold_db=-18.0, ratio=4.0, sr=48000,
             attack_ms=5.0, release_ms=120.0):
    """Peak compressor with a smoothed envelope. Physics audio has a huge crest
    factor; without this the mix sounds thin once a platform normalises it."""
    thr = 10 ** (threshold_db / 20.0)
    atk = math.exp(-1.0 / (attack_ms * 1e-3 * sr))
    rel = math.exp(-1.0 / (release_ms * 1e-3 * sr))
    absx = np.abs(x)
    if _lfilter is not None:
        # Single-coefficient follower: attack and release differ in a real
        # compressor, but for peaky impact material the release constant governs
        # the audible behaviour, and this runs orders of magnitude faster.
        env = _lfilter([1 - rel], [1.0, -rel], absx)
        env = np.maximum(env, absx * (1 - atk))
    else:
        env = np.zeros_like(absx)
        e = 0.0
        for n in range(absx.size):
            a = absx[n]
            coef = atk if a > e else rel
            e = coef * e + (1 - coef) * a
            env[n] = e
    gain = np.ones_like(x)
    over = env > thr
    gain[over] = (thr + (env[over] - thr) / ratio) / (env[over] + EPS)
    return x * gain


def limit(x, ceiling=0.97):
    """Soft-knee peak limiter. Deliberately does NOT rescale the whole signal:
    doing so would undo the loudness targeting applied just before it."""
    knee = ceiling * 0.7
    out = x.copy()
    over = np.abs(x) > knee
    if np.any(over):
        sign = np.sign(x[over])
        excess = np.abs(x[over]) - knee
        span = ceiling - knee
        out[over] = sign * (knee + span * np.tanh(excess / span))
    return out


def lufs_estimate(x, sr):
    """Rough integrated loudness. Not ITU-compliant — a K-weighting stand-in for
    getting a series into the same ballpark. Use ffmpeg loudnorm for the real
    measurement before publishing."""
    y = highpass(x, 60.0, sr)
    rms = math.sqrt(float(np.mean(y ** 2)) + EPS)
    return 20.0 * math.log10(rms + EPS) - 0.691


# ---------------------------------------------------------------------- main

def write_wav(path, left, right, sr):
    stereo = np.stack([left, right], axis=1)
    pcm = np.clip(stereo, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser(description="Render a collision log to audio.")
    ap.add_argument("events", type=Path)
    ap.add_argument("-o", "--out", type=Path, help="output WAV")
    ap.add_argument("--materials", type=Path, default=DEFAULT_BANK)
    ap.add_argument("--modes", type=int, default=32,
                    help="modes per impact (16 is enough for wood/plastic, "
                         "48+ pays off for metal and porcelain)")
    ap.add_argument("--reverb", type=float, default=0.25,
                    help="wet mix 0..1; 0 disables")
    ap.add_argument("--reverb-decay", type=float, default=0.45)
    ap.add_argument("--max-tail", type=float, default=2.0,
                    help="seconds; caps how long one impact may ring")
    ap.add_argument("--width", type=float, default=0.6,
                    help="stereo width 0..1 from event x position")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--report", action="store_true",
                    help="print event statistics and exit")
    args = ap.parse_args()

    if not args.events.is_file():
        sys.exit(f"event log not found: {args.events}")
    log = json.loads(args.events.read_text())
    events = log.get("events") or []
    if not events:
        sys.exit("event log contains no events — check that the logger ran and "
                 "that contact_monitor is enabled on the bodies")

    sr = int(log.get("sample_rate", 48000))
    duration = float(log.get("duration") or (max(e["t"] for e in events) + 2.0))
    seed = args.seed if args.seed is not None else int(log.get("seed", 12345))

    # ---- report
    energies = np.array([float(e.get("energy", 0.0)) for e in events])
    mats = {}
    for e in events:
        mats[e.get("material", "wood")] = mats.get(e.get("material", "wood"), 0) + 1
    print(f"events    {len(events)}  over {duration:.2f}s "
          f"({len(events)/max(duration,EPS):.1f}/s)")
    print(f"energy    min {energies.min():.3f}  median {np.median(energies):.3f}  "
          f"max {energies.max():.3f}")
    print(f"materials {', '.join(f'{k}×{v}' for k, v in sorted(mats.items()))}")

    if len(events) / max(duration, EPS) > 120:
        print("  ! over 120 events/s — this will read as noise rather than as "
              "objects. Raise the energy threshold in the logger.")
    if energies.max() / max(energies.min(), EPS) > 5000:
        print("  ! energy spans more than 5000x — the quiet tail will be "
              "inaudible. Consider clamping in the logger.")
    if args.report:
        return 0
    if not args.out:
        sys.exit("no output path — pass -o track.wav")

    bank = load_bank(args.materials)
    materials, templates = bank["materials"], bank["shape_templates"]

    n = int(duration * sr) + int(args.max_tail * sr) + 1
    left = np.zeros(n)
    right = np.zeros(n)
    rng = np.random.default_rng(seed)

    skipped = 0
    for ev in events:
        name = ev.get("material", "wood")
        mat = materials.get(name)
        if mat is None:
            skipped += 1
            continue
        template = templates.get(mat.get("shape_template", "box"), templates["box"])
        start = int(float(ev["t"]) * sr)
        if start >= n:
            continue

        kind = ev.get("kind", "impact")
        if kind in ("roll", "slide"):
            sig = render_continuous(mat, template, ev.get("size", 0.2),
                                    float(ev.get("energy", 0.0)),
                                    float(ev.get("duration", 0.3)),
                                    rng, sr, args.modes, kind)
        else:
            sig = render_impact(mat, template, ev.get("size", 0.2),
                                float(ev.get("energy", 0.0)),
                                rng, sr, args.modes, args.max_tail)

        end = min(start + sig.size, n)
        seg = sig[: end - start]

        # Constant-power pan from horizontal position.
        pan = float(np.clip(ev.get("x", 0.0) * args.width, -1.0, 1.0))
        angle = (pan + 1.0) * math.pi / 4.0
        left[start:end] += seg * math.cos(angle)
        right[start:end] += seg * math.sin(angle)

    if skipped:
        known = ", ".join(sorted(materials))
        if skipped == len(events):
            sys.exit(f"\nevery event referenced a material not in the bank, so "
                     f"nothing was rendered.\nbank contains: {known}")
        print(f"  ! {skipped} of {len(events)} events referenced materials not in "
              f"the bank and were skipped (bank has: {known})")

    # ---- bus
    if args.reverb > 0.0:
        ir = make_reverb_ir(sr, args.reverb_decay, np.random.default_rng(seed + 1))
        left = (1 - args.reverb) * left + args.reverb * convolve(left, ir)
        right = (1 - args.reverb) * right + args.reverb * convolve(right, ir)

    peak = max(np.max(np.abs(left)), np.max(np.abs(right)), EPS)
    left, right = left / peak * 0.7, right / peak * 0.7

    left = compress(left, sr=sr)
    right = compress(right, sr=sr)

    # Limiting changes loudness, so match, limit, re-measure and correct. Two
    # passes lands within a few tenths of a dB, which is close enough that a
    # whole series sits at a consistent level.
    for _ in range(3):
        measured = lufs_estimate((left + right) * 0.5, sr)
        adjust = 10 ** ((args.lufs - measured) / 20.0)
        left, right = limit(left * adjust), limit(right * adjust)

    write_wav(args.out, left, right, sr)
    final = lufs_estimate((left + right) * 0.5, sr)
    print(f"\n→ {args.out}  {n/sr:.2f}s stereo {sr} Hz, "
          f"~{final:.1f} LUFS (estimate)")
    print("Mux with the video:")
    print(f"  ffmpeg -i video.mp4 -i {args.out} -c:v copy -c:a aac -b:a 192k "
          f"-shortest final.mp4")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        pass
