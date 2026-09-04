#!/usr/bin/env python3
"""
music.py — Moonstone icin prosedurel ambiyans yatagi uretir. Ornek dosya yok,
telif yok, her cagri ayni tohumla ayni sonucu verir.

  python3 music.py --out yatak.wav --duration 16 --mood gece --seed 7

Mood'lar
  gece    A minor pentatonik, derin drone, seyrek can — marka/atmosfer icin
  veri    daha berrak, hafif ritmik nabiz — plan ve sayi anlatimlari icin
  acilis  yukselen ped, tek buyuk can — kanca/acilis icin

Tasarim: nabiz yok, tempo yok. Reels'te konusma ve kesme ritmi zaten var;
altina bir de tempo koymak ikisini carpistiriyor. Bu yuzden yatak zamansiz.
"""
import argparse, math, struct, wave
import numpy as np

SR = 48000

def adsr(n, a, d, s, r, sus=0.7):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    s = max(0, n - a - d - r)
    return np.concatenate([
        np.linspace(0, 1, a, endpoint=False) if a else np.array([]),
        np.linspace(1, sus, d, endpoint=False) if d else np.array([]),
        np.full(s, sus),
        np.linspace(sus, 0, r) if r else np.array([]),
    ])[:n]

def sine(f, n, phase=0.0):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t + phase)

def pad(f, n, rng, detune=0.004, partials=4):
    """Hafif detune edilmis sinuslerden nefes alan ped."""
    out = np.zeros(n)
    for k in range(1, partials + 1):
        for d in (-1, 1):
            ph = rng.uniform(0, 2 * np.pi)
            lfo = 1 + 0.0016 * np.sin(2 * np.pi * rng.uniform(0.03, 0.09) * np.arange(n) / SR + ph)
            out += (sine(f * k * (1 + d * detune * k), n, ph) / (k ** 1.7)) * lfo
    return out / partials

def bell(f, n, rng, decay=3.2):
    t = np.arange(n) / SR
    env = np.exp(-t / decay)
    s = sine(f, n) + 0.42 * sine(f * 2.01, n) + 0.18 * sine(f * 3.02, n)
    return s * env / 1.6

def wash(n, rng, cut=0.06):
    """Alcak geciren filtreli gurultu — mekan hissi."""
    x = rng.normal(0, 1, n)
    b = np.exp(-2 * np.pi * cut)
    y = np.zeros(n); acc = 0.0
    # tek kutuplu IIR, vektorlestirilmis yaklasim yerine blok blok
    blk = 4096
    for i in range(0, n, blk):
        seg = x[i:i + blk]
        for j, v in enumerate(seg):
            acc = b * acc + (1 - b) * v
            y[i + j] = acc
    return y / (np.abs(y).max() + 1e-9)

def norm(x, peak=0.9):
    m = np.abs(x).max()
    return x * (peak / m) if m > 0 else x

MOODS = {
    # kok, ped akorlari (yariton), can notalari, parlaklik
    "gece":   dict(root=110.0, chords=[[0, 7, 12, 15], [-2, 5, 10, 14]], bells=[24, 19, 15, 12], rate=(3.5, 6.5), wash=0.16),
    "veri":   dict(root=146.83, chords=[[0, 7, 12, 16], [0, 5, 12, 17]], bells=[24, 21, 19, 16, 12], rate=(2.0, 3.4), wash=0.10),
    "acilis": dict(root=98.0,  chords=[[0, 7, 14, 19]],                  bells=[26, 19],            rate=(6.0, 9.0), wash=0.20),
}

def build(duration, mood, seed):
    rng = np.random.default_rng(seed)
    M = MOODS[mood]
    n = int(duration * SR)
    out = np.zeros(n)

    # 1) drone — kok ve besli
    out += 0.30 * pad(M["root"] / 2, n, rng, detune=0.002, partials=3)
    out += 0.12 * pad(M["root"] * 1.5 / 2, n, rng, detune=0.003, partials=2)

    # 2) ped akorlari, yavas donusumlu
    seg = n // max(1, len(M["chords"]))
    for i, ch in enumerate(M["chords"]):
        s = i * seg; e = min(n, s + seg + SR)
        ln = e - s
        acc = np.zeros(ln)
        for st in ch:
            acc += pad(M["root"] * 2 ** (st / 12), ln, rng)
        env = adsr(ln, 2.2, 1.0, 0, 2.4, sus=0.85)
        out[s:e] += 0.16 * acc / len(ch) * env

    # 3) seyrek canlar
    t = rng.uniform(1.2, 2.4)
    while t < duration - 1.0:
        st = rng.choice(M["bells"])
        f = M["root"] * 2 ** (st / 12)
        ln = min(n - int(t * SR), int(rng.uniform(2.6, 4.2) * SR))
        if ln > 1000:
            b = bell(f, ln, rng, decay=rng.uniform(2.4, 3.8))
            out[int(t * SR):int(t * SR) + ln] += rng.uniform(0.10, 0.19) * b
        t += rng.uniform(*M["rate"])

    # 4) mekan wash
    out += M["wash"] * 0.5 * wash(n, rng)

    # 5) genel zarf — bas ve son yumusak
    f_in, f_out = int(1.4 * SR), int(1.8 * SR)
    env = np.ones(n)
    env[:f_in] = np.linspace(0, 1, f_in) ** 1.5
    env[-f_out:] = np.linspace(1, 0, f_out) ** 1.2
    out *= env

    # 6) yumusak limit
    out = np.tanh(out * 1.25) * 0.86
    return norm(out, 0.85)

def write_wav(path, mono, stereo_width=0.25):
    """Hafif stereo genislik — ayni sinyal, saga/sola gecikmeli."""
    d = int(0.012 * SR)
    L = mono.copy()
    R = np.concatenate([np.zeros(d), mono[:-d]]) if d else mono.copy()
    R = (1 - stereo_width) * mono + stereo_width * R
    data = np.stack([L, R], axis=1)
    pcm = np.clip(data, -1, 1)
    pcm = (pcm * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", required=True)
    p.add_argument("--duration", type=float, default=16.0)
    p.add_argument("--mood", default="gece", choices=list(MOODS))
    p.add_argument("--seed", type=int, default=7)
    a = p.parse_args()
    write_wav(a.out, build(a.duration, a.mood, a.seed))
    print(f"{a.out}  {a.duration:.1f}s  [{a.mood}] tohum={a.seed}")
