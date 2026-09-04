#!/usr/bin/env python3
"""
vo.py — ElevenLabs ile Turkce seslendirme. Metni once TTS icin duzeltir.

  python3 vo.py --text "..." --out vo.mp3 --voice george

ONEMLI: Metin TTS'e SOYLENDIGI gibi gider. reelsindustry deposunda olculdu
(ElevenLabs eleven_multilingual_v2, 2026-08-23):

  "426 km"      → «dört yüz yüzyüz mülandı vatid hilet»   (2/2 felaket)
  "%74'ü"       → «%50 kütüğü»
  "II. Mehmet"  → «3. Mehmet»
  "DSİ"         → «DSI»

Yani sayi+birim, yuzde simgesi, Roma rakami ve noktali kisaltma kirilir.
`motor/ses/okunus.py` bunlari yaziya cevirir; bu betik varsa onu kullanir.

MOONSTONE KURALI: **Seslendirme yuvarlar, ekran tam sayiyi gosterir.**
"96,54 metrekare" demek yerine ses "doksan alti metrekare" der; tam deger
gorsel plakada yazili durur. Hem daha dogal hem TTS tuzagindan uzak.
Ondalikli sayi + birim bilesimini seslendirmeye HIC koyma.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, urllib.request

VOICES = {   # marka icin denenen sesler
    # kadin
    "elif":    "4XsbOSxQHw4NUVaEeo2o",   # sakin ve dogal, genc — TURKCE ADLI SES,
                                         # Turkce telaffuzda en dogru aday
    "bella":   "hpp4J3VqNfWAUOO0d1Us",   # profesyonel, parlak, sicak, orta yas
    "jessica": "cgSgspJ2msm6clMCkdW9",   # neseli, parlak, sicak, genc
    "matilda": "XrExE9yKIg1WjnnlVkGX",   # profesyonel, orta yas
    "sarah":   "EXAVITQu4vr4xnSDxMaL",   # guven veren, genc
    "alice":   "Xb7hH8MSUJpSbSDYk0k2",   # berrak, ogretici, orta yas
    "laura":   "FGY2WhTYpPnrIDTdsKH5",   # coskulu, genc
    "lily":    "pFZP5JQG7iQjIQuC4Bku",   # kadifemsi, orta yas
    # erkek / notr
    "george":  "JBFqnCBsd6RMkjVDRZzb",   # sicak anlatici, orta yas
    "river":   "SAz9YHcvj6GT2YYXdXww",   # sakin, notr
}
REELSINDUSTRY = os.path.expanduser("~/Documents/GitHub/reelsindustry")

def okunusa_cevir(text):
    p = os.path.join(REELSINDUSTRY, "motor", "ses", "okunus.py")
    if not os.path.exists(p):
        sys.stderr.write("[not] okunus.py bulunamadi — metin oldugu gibi gonderiliyor\n")
        return text
    import importlib.util
    spec = importlib.util.spec_from_file_location("okunus", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    out = m.seslendirilebilir(text)
    return out[0] if isinstance(out, tuple) else out

def key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if k: return k
    p = os.path.expanduser("~/.config/elevenlabs/key")
    if os.path.exists(p): return open(p).read().strip()
    raise SystemExit("Anahtar yok. ELEVENLABS_API_KEY ya da ~/.config/elevenlabs/key")

def synth(text, out, voice="elif", stability=0.50, style=0.15, speed=0.88,
          model="eleven_v3"):
    """Varsayilanlar OLCUMLE secildi (bkz. references/turkce-seslendirme.md):
    eleven_v3 · hiz 0,88 · kararlilik 0,50 · stil 0,15.
    Bu ayarda 7 cumlenin 7'si de Turkce bildirme konturuyla (dusen) bitti,
    kelime hata orani %4. v2 ayni metinde %11 hata ve %67 dusus verdi.
    Kararliligi 0,75'e cikarmak dusus konturunu KIRIYOR (egim +20 yariton/sn,
    cumle yukselerek bitiyor, yabanci duyuluyor). Hizi 0,84'un altina indirmek
    de bir cumlenin konturunu bozdu. Bu ucluyu gerekcesiz degistirme."""
    vid = VOICES.get(voice, voice)
    body = json.dumps({
        "text": text, "model_id": model,
        "voice_settings": {"stability": stability, "similarity_boost": 0.75,
                           "style": style, "use_speaker_boost": True, "speed": speed},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
        data=body, headers={"xi-api-key": key(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r, open(out, "wb") as f:
        f.write(r.read())
    return out

# ───────────────────────────────────────────────── parcali (dinamik) sentez

def senaryo_uret(senaryo, out):
    """Metni parcalara bolup HER PARCAYA AYRI AYAR vererek sentezler, sonra
    aralarina sessizlik koyup birlestirir.

    Neden: tek cagrida butun metin ayni ayarla uretiliyor ve cumleler ayni
    perdede kaliyor — olculdu, kapanis cumlesi ortadakilerle birebir ayni
    F0'da cikti (222 Hz, 5,7 hece/sn). Vurgulanmasi istenen cumleyi ayri
    uretip yavaslatmak, stilini acmak ve oncesine bosluk koymak gercek bir
    dinamik araligi getiriyor.

    senaryo = {"ses": "elif", "parcalar": [
        {"metin": "…"},
        {"metin": "…", "hiz": 0.78, "stil": 0.40, "kararlilik": 0.42,
         "onceki_bosluk": 0.75}]}

    Parca ayarlari verilmezse ust duzey varsayilanlar kullanilir.
    """
    ses = senaryo.get("ses", "elif")
    vars_ = dict(hiz=senaryo.get("hiz", 0.88), stil=senaryo.get("stil", 0.15),
                 kararlilik=senaryo.get("kararlilik", 0.50),
                 model=senaryo.get("model", "eleven_v3"))
    tmp = tempfile.mkdtemp(prefix="ms-vo-")
    parcalar, listeler = [], []
    try:
        for i, p in enumerate(senaryo["parcalar"]):
            metin = p["metin"] if p.get("raw") else okunusa_cevir(p["metin"])
            # v3 ses etiketi: [slowly] [warmly] [emphasizes] gibi. Turkcede
            # OLCULDU — etiket sesli okunmuyor, yalnizca teslimati degistiriyor
            # ([slowly][emphasizes] perde araligini 10,0 → 11,2 yaritona acti).
            if p.get("etiket"):
                metin = p["etiket"] + " " + metin
            f = os.path.join(tmp, f"p{i}.mp3")
            synth(metin, f, ses,
                  stability=p.get("kararlilik", vars_["kararlilik"]),
                  style=p.get("stil", vars_["stil"]),
                  speed=p.get("hiz", vars_["hiz"]),
                  model=p.get("model", vars_["model"]))
            # parca bazli seviye: vurgulanacak cumleyi 1-2 dB one alir.
            # Perde kaydirmaktan daha guvenli — bu ffmpeg'de rubberband yok,
            # asetrate ile perde kaydirmak formantlari da kaydiriyor.
            if p.get("kazanc"):
                g = os.path.join(tmp, f"g{i}.mp3")
                subprocess.run(["ffmpeg","-v","error","-y","-i",f,
                                "-af",f"volume={p['kazanc']}dB","-c:a","libmp3lame",g], check=True)
                f = g
            bos = p.get("onceki_bosluk", 0.0 if i == 0 else 0.28)
            if bos > 0:
                s = os.path.join(tmp, f"s{i}.mp3")
                subprocess.run(["ffmpeg","-v","error","-y","-f","lavfi","-t",str(bos),
                                "-i","anullsrc=r=44100:cl=mono","-c:a","libmp3lame",s], check=True)
                listeler.append(s)
            listeler.append(f)
            parcalar.append((p["metin"][:40], bos))
        lst = os.path.join(tmp, "l.txt")
        with open(lst, "w") as fh:
            for f in listeler: fh.write(f"file '{f}'\n")
        subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,
                        "-c:a","libmp3lame","-b:a","192k", out], check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for m, b in parcalar:
        print(f"  ⟨{b:.2f} sn boşluk⟩ {m}…")
    return out


ESIKLER = dict(kelime_hata=0.08, dusen_cumle=0.80, konusma_hizi=(4.0, 6.2),
               f0_aralik=7.0, ton_cesitliligi=2.5)

def denetle(ses, metin):
    """Uretilen sesi olcup esiklere gore gecer/kalir verir.

    Esikler bu depodaki olcumlerden geldi, keyfi degil:
      kelime hata orani  <= %8   — ustunde telaffuz gercekten bozuk
      cumle sonu dususu  >= %80  — Turkce bildirme cumlesi sonda alcalir
      konusma hizi    4,0–6,2 hece/sn (duraklar dahil)
      F0 araligi         >= 7 yariton — altinda duz/robotik duyuluyor
    """
    import importlib.util
    sp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "soz_olcum.py")
    spec = importlib.util.spec_from_file_location("soz_olcum", sp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    r = m.olc(ses, metin)
    sorun = []
    k = r.get("kelime_hata_orani")
    if k is not None and k > ESIKLER["kelime_hata"]:
        sorun.append(f"kelime hata orani %{k*100:.0f} — sayilari yaziya cevir, "
                     f"bilesik kelimeleri ayir (metrekaresi → metrekare)")
    d = r.get("dusen_cumle_orani")
    if d is not None and d < ESIKLER["dusen_cumle"]:
        sorun.append(f"cumle sonu dususu %{d*100:.0f} — yukselerek biten cumleyi "
                     f"yeniden kur; sirali yan cumleyle bitirme "
                     f"(\"…sonra pencereye yurur.\" gibi)")
    h = r.get("konusma_hizi")
    lo, hi = ESIKLER["konusma_hizi"]
    if h is not None and not (lo <= h <= hi):
        sorun.append(f"konusma hizi {h:.1f} hece/sn — --speed ayarla")
    tc = r.get("ton_cesitliligi")
    if tc is not None and tc < ESIKLER["ton_cesitliligi"]:
        sorun.append(f"ton cesitliligi {tc:.1f} yariton — butun cumleler ayni perdede. "
                     f"--senaryo ile parcala; vurgulanacak cumleye etiket, "
                     f"kazanc ve oncesine bosluk ver")
    if r["f0_aralik_yariton"] < ESIKLER["f0_aralik"]:
        sorun.append(f"F0 araligi {r['f0_aralik_yariton']:.1f} yariton — duz duyuluyor, "
                     f"--stability dusur (0,75 kontur kiriyor)")
    m.yazdir(os.path.basename(ses), r)
    print("\n  " + ("✓ GEÇTİ" if not sorun else "⚠ KALDI"))
    for s in sorun: print("   · " + s)
    return not sorun


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--text")
    p.add_argument("--senaryo", help="parçalı sentez için JSON dosyası")
    p.add_argument("--out", required=True)
    p.add_argument("--voice", default="elif", help=", ".join(VOICES))
    p.add_argument("--speed", type=float, default=0.88)
    p.add_argument("--model", default="eleven_v3")
    p.add_argument("--stability", type=float, default=0.50)
    p.add_argument("--raw", action="store_true", help="okunus donusumunu atla")
    p.add_argument("--denetle", action="store_true",
                   help="uretim sonrasi prozodiyi olc ve esikleri denetle")
    a = p.parse_args()
    if a.senaryo:
        sen = json.load(open(a.senaryo, encoding="utf-8"))
        senaryo_uret(sen, a.out)
        d = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                            "-of","csv=p=0", a.out], capture_output=True, text=True).stdout.strip()
        print(f"{a.out}  {float(d):.2f}s  [{sen.get('ses','elif')}]  {len(sen['parcalar'])} parça")
        if a.denetle:
            denetle(a.out, " ".join(p["metin"] for p in sen["parcalar"]))
        raise SystemExit
    if not a.text: raise SystemExit("--text ya da --senaryo gerekli")
    t = a.text if a.raw else okunusa_cevir(a.text)
    if t != a.text:
        print(f"  okunus: {t}")
    synth(t, a.out, a.voice, stability=a.stability, speed=a.speed, model=a.model)
    d = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","csv=p=0", a.out], capture_output=True, text=True).stdout.strip()
    print(f"{a.out}  {float(d):.2f}s  [{a.voice}]  {len(t)} karakter")
    if a.denetle:
        denetle(a.out, a.text)
