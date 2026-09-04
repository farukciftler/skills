#!/usr/bin/env python3
"""
soz_olcum.py — Turkce seslendirmenin prozodisini olcer. Kulak yerine sayi.

  python3 soz_olcum.py --ses vo.mp3 --metin "Yazdigim cumle."

Ucunu birden olcer:

1. ASR GERI-DONUSU — ElevenLabs Scribe sesi yaziya cevirir, aslıyla
   karsilastirilir. Kelimeler dogru cikti mi? (Telaffuz felaketlerini yakalar.)
   Sinir: ASR sayilari normalize eder ("kirk" → "40"), bu yuzden fark her zaman
   hata demek degil. Karsilastirma normalize edilmis metin uzerinden yapilir.

2. SON HECE DUSUSU — Turkce bildirme cumlesi sonda alcalir. TTS yabanci bir
   yukselis ya da duz kontur uretirse cumle "Turkce tonlamaya uymuyor" diye
   duyulur. Her cumlenin son 400 ms'indeki F0 egimi olculur; negatif olmali.

3. YUKLEM ONU ODAGI — Turkcede fiil cumlesinde vurgu **yuklemden bir onceki
   ogededir**. ASR kelime zaman damgasi verdigi icin, F0 tepesinin gercekten o
   kelimeye dusup dusmedigi olculebilir.

Ek olarak: konusma hizi (hece/sn), virgullerde duraklama, sessizlik orani.

F0 kestirimi otokorelasyonla yapilir; mutlak dogrulugu degil, EGILIMI olcmek
icin yeterli. Iki secenegi karsilastirmaya yarar, mutlak hakem degildir.
"""
import argparse, json, os, re, subprocess, sys, tempfile, unicodedata
import numpy as np

SR = 16000
UNLU = set("aeıioöuüAEIİOÖUÜ")

def key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if k: return k
    p = os.path.expanduser("~/.config/elevenlabs/key")
    return open(p).read().strip()

def yukle(path):
    wav = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path,
                    "-ac", "1", "-ar", str(SR), wav], check=True)
    import wave
    with wave.open(wav) as w:
        d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    os.unlink(wav)
    return d / 32768.0

# ───────────────────────────────────────────────────────────── F0 kestirimi

def f0_izi(x, hop=0.010, win=0.040, fmin=70, fmax=350):
    """Otokorelasyonla temel frekans izi. Sessiz cerceveler NaN."""
    H, W = int(hop * SR), int(win * SR)
    lo, hi = int(SR / fmax), int(SR / fmin)
    out, t = [], []
    for i in range(0, len(x) - W, H):
        f = x[i:i + W]
        e = np.sqrt((f ** 2).mean())
        if e < 0.006:
            out.append(np.nan); t.append(i / SR); continue
        f = f - f.mean()
        ac = np.correlate(f, f, "full")[W - 1:]
        if ac[0] <= 0:
            out.append(np.nan); t.append(i / SR); continue
        ac = ac / ac[0]
        seg = ac[lo:hi]
        if len(seg) == 0:
            out.append(np.nan); t.append(i / SR); continue
        k = int(np.argmax(seg)) + lo
        out.append(SR / k if seg[k - lo] > 0.32 else np.nan)
        t.append(i / SR)
    return np.array(t), np.array(out)

def egim(t, f, t0, t1):
    """Verilen aralikta F0'in yari-ton/saniye cinsinden egimi."""
    m = (t >= t0) & (t <= t1) & ~np.isnan(f)
    if m.sum() < 4: return None
    st = 12 * np.log2(f[m] / np.nanmedian(f[~np.isnan(f)]))
    return float(np.polyfit(t[m], st, 1)[0])

# ─────────────────────────────────────────────────────────────── yardimci

def sadelestir(s):
    s = unicodedata.normalize("NFC", s.lower())
    s = s.replace("i̇", "i")
    s = re.sub(r"[^\wçğıöşü ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

SAYI = {"sıfır":0,"bir":1,"iki":2,"üç":3,"dört":4,"beş":5,"altı":6,"yedi":7,
        "sekiz":8,"dokuz":9,"on":10,"yirmi":20,"otuz":30,"kırk":40,"elli":50,
        "altmış":60,"yetmiş":70,"seksen":80,"doksan":90,"yüz":100,"bin":1000}

# ASR ozel adlari kendi yazim alaskanligiyla dokuyor: marka adini bolup
# birlestirip yaziyor. Bunlar telaffuz hatasi DEGIL; karsilastirmadan once
# iki taraf da ayni bicime cekilir, yoksa kapi marka adi yuzunden kaliyor.
OZEL_AD = [
    (r"\bmoon\s*stone\b", "moonstone"),
    (r"\bay\s*tasi\b", "aytasi"),
    (r"\bay\s*taşı\b", "aytaşı"),
    (r"\baydın\s*tepe\b", "aydıntepe"),
    (r"\bayhan\s*lar\b", "ayhanlar"),
]

def ozel_adlari_esitle(s):
    for kalip, yerine in OZEL_AD:
        s = re.sub(kalip, yerine, s)
    return s

def sayilari_yaziya(s):
    """ASR '40' yazar, metinde 'kırk' var. Ikisini ayni tarafa cek."""
    ters = {str(v): k for k, v in SAYI.items()}
    return " ".join(ters.get(w, w) for w in s.split())

def hece_say(s):
    return sum(1 for c in s if c in UNLU)

def kelime_hatasi(a, b):
    """Basit Levenshtein (kelime duzeyinde) → kelime hata orani."""
    A, B = a.split(), b.split()
    d = np.zeros((len(A)+1, len(B)+1), dtype=int)
    d[:,0] = np.arange(len(A)+1); d[0,:] = np.arange(len(B)+1)
    for i in range(1, len(A)+1):
        for j in range(1, len(B)+1):
            d[i,j] = min(d[i-1,j]+1, d[i,j-1]+1, d[i-1,j-1] + (A[i-1] != B[j-1]))
    return d[len(A), len(B)] / max(1, len(A))

# ───────────────────────────────────────────────────────────────── olcum

def asr(path):
    import urllib.request
    boundary = "----msform"
    data = open(path, "rb").read()
    parts = []
    for k, v in (("model_id", "scribe_v1"), ("language_code", "tur")):
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\n"
                 f"Content-Type: audio/mpeg\r\n\r\n".encode() + data + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body,
        headers={"xi-api-key": key(), "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def olc(ses, metin=None, sessiz=False):
    x = yukle(ses)
    sure = len(x) / SR
    t, f = f0_izi(x)
    gecerli = ~np.isnan(f)
    medyan = float(np.nanmedian(f)) if gecerli.any() else 0.0
    aralik = (float(np.nanpercentile(f, 90)) - float(np.nanpercentile(f, 10))) if gecerli.sum() > 10 else 0.0
    yariton_aralik = 12 * np.log2(np.nanpercentile(f, 90) / np.nanpercentile(f, 10)) if gecerli.sum() > 10 else 0

    # sessizlik / duraklama
    H = int(0.010 * SR)
    enerji = np.array([np.sqrt((x[i:i+H]**2).mean()) for i in range(0, len(x)-H, H)])
    sessiz_m = enerji < 0.008
    duraklar, n = [], 0
    for s in sessiz_m:
        if s: n += 1
        else:
            if n >= 12: duraklar.append(n * 0.010)   # >=120 ms
            n = 0
    sonuc = dict(sure=sure, f0_medyan=medyan, f0_aralik_yariton=float(yariton_aralik),
                 sessizlik_orani=float(sessiz_m.mean()), duraklar=duraklar)

    d = asr(ses)
    soylenen = d.get("text", "")
    sonuc["asr"] = soylenen
    kelimeler = [w for w in d.get("words", []) if w.get("type") == "word"]
    if kelimeler:
        hece = sum(hece_say(w["text"]) for w in kelimeler)
        konusma = sure * (1 - sessiz_m.mean())
        sonuc["bogumlama_hizi"] = hece / max(0.1, konusma)   # duraklar HARIC
        sonuc["konusma_hizi"] = hece / max(0.1, sure)        # duraklar DAHIL
    if metin:
        a = ozel_adlari_esitle(sayilari_yaziya(sadelestir(metin)))
        b = ozel_adlari_esitle(sayilari_yaziya(sadelestir(soylenen)))
        sonuc["kelime_hata_orani"] = kelime_hatasi(a, b)

    # ── kontur: cumle sonu DUSER, cumle ici virgul YUKSELIR ───────────────
    # Turkcede virguldeki yukselis DOGRUDUR (devam konturu). Duraklara gore
    # bolmek bu dogru yukselisleri hata sayiyordu; bu yuzden kaynak metnin
    # noktalamasi ASR kelimelerine hizalanir.
    son_egim, dev_egim = [], []
    if kelimeler and metin:
        asr_k = [sadelestir(w["text"]) for w in kelimeler]
        cumle_son, virgul_son = set(), set()
        idx = 0
        for parca in re.split(r"(?<=[.!?])\s+", metin.strip()):
            kel = [sadelestir(w) for w in re.findall(r"[\w'çğıöşüÇĞİÖŞÜ]+[,;]?", parca)]
            for j, w in enumerate(kel):
                if w.endswith(","):
                    virgul_son.add((idx, w[:-1]))
                idx += 1
            if kel: cumle_son.add(idx - 1)
        # kaynak sirasini ASR sirasina kabaca esle (silme/ekleme toleransli)
        i_asr = 0
        kaynak = [sadelestir(w).rstrip(",;") for w in re.findall(r"[\w'çğıöşüÇĞİÖŞÜ]+[,;]?", metin)]
        virgul_idx = {i for i, _ in virgul_son}
        for i_src, w in enumerate(kaynak):
            # ASR'de bu kelimeyi ileriye dogru ara
            bulundu = None
            for k in range(i_asr, min(i_asr + 4, len(asr_k))):
                if asr_k[k] == w: bulundu = k; break
            if bulundu is None: continue
            i_asr = bulundu + 1
            son = kelimeler[bulundu]["end"]
            e = egim(t, f, max(0, son - 0.42), son)
            if e is None: continue
            if i_src in cumle_son: son_egim.append(e)
            elif i_src in virgul_idx: dev_egim.append(e)
    # ── cumle cumle ton profili: tek duze mi, dalgalaniyor mu? ────────────
    profil = []
    if kelimeler and metin:
        asr_k2 = [sadelestir(w["text"]) for w in kelimeler]
        i_asr, bas = 0, 0
        for parca in re.split(r"(?<=[.!?])\s+", metin.strip()):
            kel = [sadelestir(w).rstrip(",;") for w in re.findall(r"[\w'çğıöşüÇĞİÖŞÜ]+[,;]?", parca)]
            son_i = i_asr
            for w in kel:
                for k in range(son_i, min(son_i + 4, len(asr_k2))):
                    if asr_k2[k] == w: son_i = k + 1; break
            if son_i <= i_asr: continue
            t0 = kelimeler[i_asr]["start"]; t1 = kelimeler[son_i-1]["end"]
            m2 = (t >= t0) & (t <= t1) & ~np.isnan(f)
            hece = sum(hece_say(w) for w in kel)
            profil.append(dict(
                metin=parca[:44],
                f0=float(np.nanmedian(f[m2])) if m2.sum() > 3 else None,
                hiz=hece / max(0.2, t1 - t0),
                sure=t1 - t0,
                oncesi_bosluk=(t0 - kelimeler[i_asr-1]["end"]) if i_asr > 0 else 0.0))
            i_asr = son_i
    sonuc["profil"] = profil
    f0lar = [p["f0"] for p in profil if p["f0"]]
    if len(f0lar) > 1:
        # cumleler arasi perde oynamasi, yariton cinsinden
        sonuc["ton_cesitliligi"] = float(12 * np.log2(max(f0lar) / min(f0lar)))
        hizlar = [p["hiz"] for p in profil]
        sonuc["hiz_cesitliligi"] = float((max(hizlar) - min(hizlar)) / (sum(hizlar)/len(hizlar)))
    sonuc["cumle_sonu_egimleri"] = son_egim
    sonuc["virgul_egimleri"] = dev_egim
    sonuc["dusen_cumle_orani"] = (sum(1 for e in son_egim if e < -0.5) / len(son_egim)) if son_egim else None
    sonuc["yukselen_virgul_orani"] = (sum(1 for e in dev_egim if e > -6.0) / len(dev_egim)) if dev_egim else None
    return sonuc

def yazdir(ad, r):
    print(f"\n── {ad}")
    print(f"  süre {r['sure']:.1f} sn · F0 medyan {r['f0_medyan']:.0f} Hz · "
          f"F0 aralığı {r['f0_aralik_yariton']:.1f} yarıton")
    if "konusma_hizi" in r:
        kh, bh = r["konusma_hizi"], r["bogumlama_hizi"]
        print(f"  konuşma hızı {kh:.1f} hece/sn (duraklar dahil, doğal 4–6)  ·  "
              f"boğumlama {bh:.1f} hece/sn (duraklar hariç, doğal 5–7)   "
              f"{'✓' if 4 <= kh <= 6 else '⚠'}")
    if "kelime_hata_orani" in r:
        k = r["kelime_hata_orani"]
        print(f"  kelime hata oranı {k*100:.0f}%   {'✓' if k<0.10 else '⚠'}")
    d = r["dusen_cumle_orani"]
    if d is not None:
        print(f"  cümle sonu düşüşü {d*100:.0f}%   {'✓' if d>=0.8 else '⚠ Türkçe bildirme cümlesi sonda alçalır'}")
        print(f"    cümle sonu (yarıton/sn): {', '.join(f'{e:+.1f}' for e in r['cumle_sonu_egimleri'])}")
    v = r.get("yukselen_virgul_orani")
    if v is not None:
        print(f"  virgülde devam konturu {v*100:.0f}%   {'✓' if v>=0.6 else '⚠ virgülde de düşüyor, cümle parçalanmış duyuluyor'}")
        print(f"    virgül (yarıton/sn): {', '.join(f'{e:+.1f}' for e in r['virgul_egimleri'])}")
    print(f"  duraklama sayısı {len(r['duraklar'])} · sessizlik oranı {r['sessizlik_orani']*100:.0f}%")
    tc = r.get("ton_cesitliligi")
    if tc is not None:
        hc = r.get("hiz_cesitliligi", 0)
        print(f"  ton çeşitliliği {tc:.1f} yarıton · hız çeşitliliği %{hc*100:.0f}   "
              f"{'✓' if tc >= 2.0 else '⚠ cümleler aynı perdede, tek düze duyuluyor'}")
        for p in r.get("profil", []):
            f0s = f"{p['f0']:.0f} Hz" if p["f0"] else "  —   "
            print(f"    {f0s} · {p['hiz']:.1f} hece/sn · önce {p['oncesi_bosluk']:.2f} sn  │ {p['metin']}")
    print(f"  ASR: {r['asr'][:150]}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ses", required=True, nargs="+")
    p.add_argument("--metin")
    a = p.parse_args()
    for s in a.ses:
        yazdir(os.path.basename(s), olc(s, a.metin))
