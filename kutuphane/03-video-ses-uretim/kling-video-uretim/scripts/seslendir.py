#!/usr/bin/env python3
"""
seslendir.py — ElevenLabs ile Türkçe seslendirme (Moonstone). Standart kütüphane + ffmpeg.

Kaynak: ~/projects/reelsindustry motor/ses/tts.py + okunus.py, ölçümler
.claude/skills/turkce-anlati/references/olcumler.md (23 Ağu 2026). Buradaki
okunuş kuralları o ölçümlerden; Moonstone'a özgü biçimler (m², 3+1, net/brüt)
eklendi. Ayrıntı: references/seslendirme.md

Anahtar: ELEVENLABS_API_KEY ya da ~/.config/elevenlabs/key (600). Depoya girmez.

Alt komutlar
  okunus   "metin"                     yazılı metni söylenen hâle çevirir (API yok)
  uret     "metin" --out ses.wav       sentez → WAV 48 kHz mono −16 LUFS + ses.zamanlama.json
  deneme   "metin" --sesler a,b,c      aynı cümleyi birden çok sesle üretir (ses seçimi için)
  sesler   [--dil tr]                  hesaptaki sesleri listeler
  ambiyans "prompt" --sure 12 --out a.mp3   ses efekti / ambiyans üretir
  kota                                 karakter kotası

  python3 seslendir.py uret "Ay taşının zarafeti, yaşamın en değerli hali." --ses bill --out vo.wav
  python3 seslendir.py deneme "Tip beş, üç artı bir, net doksan altı virgül elli dört metrekare." --sesler bill,george,daniel --out-dir deneme/
"""
import argparse, base64, json, os, re, subprocess, sys, tempfile, urllib.error, urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"          # Türkçe destekli; v3 alpha zamanlama vermiyor [?]
SESLER = {                                # reelsindustry ölçümü: altısı da Türkçe WER %0; fark tını
    "bill": "pqHfZKP75CvOlQylNhV4", "brian": "nPczCjzI2devNBz1zQrb",
    "george": "JBFqnCBsd6RMkjVDRZzb", "daniel": "onwK4e9ZLuTAKqWW03F9",
    "adam": "pNInz6obpgDQGcFmaJgB", "arnold": "VR6AewLTigWG4xSOukaG",
}
LUFS = -16.0
UA = "moonstone-seslendir/1.0"
# Tonlama = voice_settings + metin. stability düşük → iniş çıkış artar; yüksek → düz.
TON = {
    "sakin": dict(kararlilik=0.62, stil=0.0,  hiz=0.94),   # mimari, manifesto — düz, prestijli
    "sicak": dict(kararlilik=0.45, stil=0.15, hiz=0.97),   # yaşam, rehber — konuşur gibi
    "kanca": dict(kararlilik=0.35, stil=0.25, hiz=1.0),    # ilk cümle — iniş çıkış belirgin
}
BREAK = re.compile(r'<break\s+time="[\d.]+s"\s*/>')

# ---------------------------------------------------------------- anahtar / http

def key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if k:
        return k
    f = Path.home() / ".config" / "elevenlabs" / "key"
    if f.is_file() and f.read_text().strip():
        return f.read_text().strip()
    sys.exit("ElevenLabs anahtarı yok: ~/.config/elevenlabs/key (chmod 600) ya da ELEVENLABS_API_KEY")

def req(method, path, data=None, raw=False, params=None):
    url = API + path + (("?" + urllib.parse.urlencode(params)) if params else "")
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, method=method,
                               headers={"xi-api-key": key(), "Content-Type": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            b = resp.read()
            return b if raw else json.loads(b)
    except urllib.error.HTTPError as e:
        det = e.read().decode("utf-8", "replace")[:400]
        hint = {401: "anahtar geçersiz", 402: "ödeme/kota (payment_issue)", 422: "istek gövdesi hatalı",
                429: "hız sınırı — bekle"}.get(e.code, "")
        sys.exit(f"ElevenLabs HTTP {e.code} {hint}: {det}")
import urllib.parse  # noqa: E402

# ---------------------------------------------------------------- okunuş (ölçülmüş kurallar)

BIRLER = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ONLAR = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
BASAMAK = [(10**9, "milyar"), (10**6, "milyon"), (10**3, "bin")]
BIRIMLER = {"m²": "metrekare", "m2": "metrekare", "km": "kilometre", "m": "metre", "cm": "santimetre",
            "dk": "dakika", "sn": "saniye", "sa": "saat", "kg": "kilogram", "km²": "kilometrekare"}
SIRA = {1: "birinci", 2: "ikinci", 3: "üçüncü", 4: "dördüncü", 5: "beşinci", 6: "altıncı", 7: "yedinci",
        8: "sekizinci", 9: "dokuzuncu", 10: "onuncu", 11: "on birinci", 12: "on ikinci"}
SESLI = "aeıioöuüAEIİOÖUÜ"

def sayi_yaz(n):
    if n == 0: return "sıfır"
    p = []
    for d, ad in BASAMAK:
        if n >= d:
            a, n = n // d, n % d
            p.append(ad if (a == 1 and ad == "bin") else sayi_yaz(a) + " " + ad)
    if n >= 100:
        y, n = n // 100, n % 100
        p.append("yüz" if y == 1 else BIRLER[y] + " yüz")
    if n >= 10:
        p.append(ONLAR[n // 10]); n %= 10
    if n: p.append(BIRLER[n])
    return " ".join(p)

def _ek(soylenen, ek):
    """'3+1'e' → 'üç artı bire'; ünsüz yumuşaması (dört → dördü)."""
    if not ek: return soylenen
    ek = ek.lstrip("'’")
    k = soylenen.split(); s = k[-1]
    if ek[:1] in SESLI and s[-1:] in "ptçk":
        s = s[:-1] + {"p": "b", "t": "d", "ç": "c", "k": "ğ"}[s[-1]]
    k[-1] = s + ek
    return " ".join(k)

def _ondalik(s):
    t, v = s.split(",")
    return f"{sayi_yaz(int(t))} virgül {sayi_yaz(int(v))}"

def okunus(metin):
    """(söylenen metin, görünüm haritası[(söylenen ifade, ekranda)]) döner."""
    harita = []
    def kaydet(soy, gor):
        harita.append((soy, gor)); return soy
    birim = "|".join(re.escape(b) for b in sorted(BIRIMLER, key=len, reverse=True))
    kurallar = [
        # oda sayısı: 3+1'e, 1+1'den
        (re.compile(r"\b(\d)\+(\d)(['’]\w+)?"),
         lambda m: kaydet(_ek(f"{BIRLER[int(m.group(1))]} artı {BIRLER[int(m.group(2))]}", m.group(3)), m.group(0))),
        # ondalık + birim: 40,49 m²
        (re.compile(r"\b(\d+,\d+)\s*(" + birim + r")\b(['’]\w+)?"),
         lambda m: kaydet(_ek(f"{_ondalik(m.group(1))} {BIRIMLER[m.group(2)]}", m.group(3)), m.group(0))),
        # tam sayı (binlik noktalı olabilir) + birim: 3.000 m², 36 m²
        (re.compile(r"\b(\d{1,3}(?:\.\d{3})+|\d+)\s*(" + birim + r")\b(['’]\w+)?"),
         lambda m: kaydet(_ek(f"{sayi_yaz(int(m.group(1).replace('.', '')))} {BIRIMLER[m.group(2)]}", m.group(3)), m.group(0))),
        # yüzde
        (re.compile(r"%\s?(\d+)(['’]\w+)?"),
         lambda m: kaydet(_ek(f"yüzde {sayi_yaz(int(m.group(1)))}", m.group(2)), m.group(0))),
        # sıra sayısı: 10. kat, 11. kat
        (re.compile(r"\b(\d{1,2})\.\s+(?=[a-zçğıöşü])"),
         lambda m: kaydet(SIRA.get(int(m.group(1)), sayi_yaz(int(m.group(1))) + "uncu") + " ", m.group(0).strip() + " ")),
        # yıl + ek ve ondalık tek başına: DOKUNMA (ölçüldü, doğru okunuyor)
        # kalan 4+ haneli sayı (telefon parçası gibi) → yazıyla
        (re.compile(r"\b(\d{4,})\b(?!['’])"), lambda m: kaydet(sayi_yaz(int(m.group(1))), m.group(0))),
    ]
    tags = BREAK.findall(metin)
    out = BREAK.sub(" \x00 ", metin)
    for desen, f in kurallar:
        out = desen.sub(f, out)
    for t in tags:
        out = out.replace("\x00", t, 1)
    # sesli okunmayan işaretler
    out = re.sub(r"\s*[—–]\s*", ", ", out).replace("…", "...")   # üç nokta kalır: askıda ton (bkz. seslendirme.md §4b)
    out = re.sub(r"\s{2,}", " ", out).strip()
    return out, harita

# ---------------------------------------------------------------- sentez

def normalize(ham, out):
    """48 kHz mono, −16 LUFS. Konuşma tek geçişte oturuyor (reelsindustry ölçümü)."""
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(ham), "-af",
                    f"loudnorm=I={LUFS}:TP=-1.5:LRA=11,aresample=48000", "-ac", "1", "-ar", "48000",
                    "-c:a", "pcm_s16le", str(out)], check=True)

def kelimeler(align):
    """Karakter hizalaması → kelime zamanlaması."""
    ks, bs, es = align["characters"], align["character_start_times_seconds"], align["character_end_times_seconds"]
    out, cur, bas, son = [], [], None, None
    for k, b, e in zip(ks, bs, es):
        if k.isspace():
            if cur: out.append({"kelime": "".join(cur), "bas": round(bas, 3), "bit": round(son, 3)}); cur, bas = [], None
            continue
        if bas is None: bas = b
        cur.append(k); son = e
    if cur: out.append({"kelime": "".join(cur), "bas": round(bas, 3), "bit": round(son, 3)})
    return [w for w in out if "<" not in w["kelime"] and ">" not in w["kelime"] and not w["kelime"].startswith("time=")]

def _norm(w):
    return re.sub(r"[^\wçğıöşü]", "", w.lower())

def gorunume_topla(zam, harita):
    """Yazıya çevrilen ifadeleri altyazı için özgün biçime geri toplar."""
    for soy, gor in harita:
        s = [_norm(x) for x in soy.split()]
        i = 0
        while i <= len(zam) - len(s):
            if [_norm(z["kelime"]) for z in zam[i:i + len(s)]] == s:
                son = zam[i + len(s) - 1]["kelime"]
                nokta = son[-1] if son[-1:] in ".,!?:;" else ""        # toplanan ifadenin noktalaması korunur
                zam[i:i + len(s)] = [{"kelime": gor.strip() + nokta, "bas": zam[i]["bas"], "bit": zam[i + len(s) - 1]["bit"]}]
            i += 1
    return zam

def sentez(metin, out, ses="bill", hiz=None, kararlilik=None, benzerlik=0.8, stil=None, ton="sakin",
           onceki=None, sonraki=None):
    """ton: sakin | sicak | kanca (TON tablosu); açık verilen hiz/kararlilik/stil tonu ezer.
    onceki/sonraki: parçalı sentezde bağlam — ElevenLabs previous_text/next_text, cümleler arası tını tutarlılığı."""
    ses_id = SESLER.get(ses.lower(), ses)
    T = TON.get(ton, TON["sakin"])
    hiz = T["hiz"] if hiz is None else hiz
    kararlilik = T["kararlilik"] if kararlilik is None else kararlilik
    stil = T["stil"] if stil is None else stil
    soy, harita = okunus(metin)
    govde = {"text": soy, "model_id": MODEL,
             "voice_settings": {"stability": kararlilik, "similarity_boost": benzerlik, "style": stil,
                                "use_speaker_boost": True, "speed": max(0.7, min(1.2, hiz))}}
    if onceki: govde["previous_text"] = okunus(onceki)[0]
    if sonraki: govde["next_text"] = okunus(sonraki)[0]
    c = req("POST", f"/text-to-speech/{ses_id}/with-timestamps", govde, params={"output_format": "mp3_44100_128"})
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        mp3 = Path(td) / "ham.mp3"; mp3.write_bytes(base64.b64decode(c["audio_base64"]))
        normalize(mp3, out)
    al = c.get("alignment") or c.get("normalized_alignment") or {}
    zam = gorunume_topla(kelimeler(al), harita) if al.get("characters") else []
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                               capture_output=True, text=True).stdout.strip() or 0)
    rapor = {"dosya": str(out), "ses": ses, "ses_id": ses_id, "model": MODEL, "sure": round(dur, 3),
             "ton": ton, "ayar": {"stability": kararlilik, "style": stil, "speed": hiz},
             "metin": metin, "soylenen": soy, "kelime_sayisi": len(zam), "zamanlama": zam,
             "not": "Seslendirme yapay zekâ ile üretilmiştir."}
    out.with_suffix(".zamanlama.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")
    return rapor

def parcali(satirlar, out, ses="bill", ton="sakin", toplam=None):
    """satirlar: [{"metin","bas","ton"?}] — her satır ayrı sentez (bağlamlı), zamanına yerleştirilir,
    tek WAV + birleşik zamanlama. Satır kendi çekiminden uzunsa uyarır (kırpmaz)."""
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    parcalar, zam, uyar = [], [], []
    for i, s_ in enumerate(satirlar):
        onceki = satirlar[i - 1]["metin"] if i > 0 else None
        sonraki = satirlar[i + 1]["metin"] if i + 1 < len(satirlar) else None
        r = sentez(s_["metin"], out.parent / f"{out.stem}-{i+1:02d}.wav", ses, ton=s_.get("ton", ton),
                   onceki=onceki, sonraki=sonraki)
        bas = float(s_.get("bas", 0))
        parcalar.append((r["dosya"], bas, r["sure"]))
        for w in r["zamanlama"]:
            zam.append({"kelime": w["kelime"], "bas": round(w["bas"] + bas, 3), "bit": round(w["bit"] + bas, 3)})
        if s_.get("bit") and bas + r["sure"] > float(s_["bit"]) + 0.2:
            uyar.append(f"satır {i+1} çekimi {bas + r['sure'] - float(s_['bit']):.1f} sn aşıyor: {s_['metin'][:40]}…")
    son = max(b + d for _, b, d in parcalar)
    T = toplam or son + 0.5
    ins, g = [], []
    for k, (f, b, d) in enumerate(parcalar):
        ins += ["-i", f]
        g.append(f"[{k}:a]aresample=48000,adelay={int(b*1000)}|{int(b*1000)}[p{k}]")
    g.append("".join(f"[p{k}]" for k in range(len(parcalar))) + f"amix=inputs={len(parcalar)}:normalize=0,apad,atrim=0:{T:.3f}[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", ";".join(g), "-map", "[o]",
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(out)], check=True)
    rapor = {"dosya": str(out), "ses": ses, "ton": ton, "sure": round(T, 3), "parcalar": [
        {"dosya": f, "bas": b, "sure": d, "metin": satirlar[k]["metin"]} for k, (f, b, d) in enumerate(parcalar)],
        "kelime_sayisi": len(zam), "zamanlama": zam, "uyarilar": uyar,
        "not": "Seslendirme yapay zekâ ile üretilmiştir."}
    out.with_suffix(".zamanlama.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")
    for u in uyar: sys.stderr.write("[UYARI] " + u + "\n")
    return rapor

# ---------------------------------------------------------------- komutlar

def cmd_okunus(a):
    soy, h = okunus(a.metin)
    print(soy)
    for s, g in h: print(f"  {g!r} → {s!r}")

def cmd_uret(a):
    r = sentez(a.metin, a.out, a.ses, a.hiz, a.kararlilik, a.benzerlik, a.stil, ton=a.ton)
    print(f"✓ {r['dosya']}  {r['sure']} sn  {r['kelime_sayisi']} kelime  ({r['ses']})")
    print("  söylenen: " + r["soylenen"])

def cmd_deneme(a):
    d = Path(a.out_dir); d.mkdir(parents=True, exist_ok=True)
    for s in a.sesler.split(","):
        s = s.strip()
        r = sentez(a.metin, d / f"deneme-{s}.wav", s, ton=a.ton)
        print(f"{s:<10} {r['sure']:>5.2f} sn  {r['dosya']}")
    print("Dinle, seç; seçim marka kararıdır — kimlik dosyasına yaz.")

def cmd_parcali(a):
    j = json.loads(Path(a.satirlar).read_text(encoding="utf-8"))
    r = parcali(j["satirlar"] if isinstance(j, dict) else j, a.out, a.ses, a.ton, a.toplam)
    print(f"✓ {r['dosya']}  {r['sure']} sn  {len(r['parcalar'])} parça  {r['kelime_sayisi']} kelime")

def cmd_sesler(a):
    j = req("GET", "/voices")
    for v in j.get("voices", []):
        lab = v.get("labels") or {}
        satir = f"{v['name']:<22} {v['voice_id']}  {v.get('category',''):<10} {lab.get('gender','')}/{lab.get('age','')}/{lab.get('accent','')}  {lab.get('use_case','')}"
        if not a.dil or a.dil.lower() in json.dumps(lab).lower() or a.dil.lower() in (v.get("name") or "").lower():
            print(satir)

def cmd_ambiyans(a):
    b = req("POST", "/sound-generation", {"text": a.prompt, "duration_seconds": a.sure,
                                          "prompt_influence": a.etki}, raw=True)
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(b)
    print(f"✓ {out}  ({len(b)/1e3:.0f} KB, {a.sure} sn)  — Reels müziği değil, yatak; bitir.py --muzik ile")

def cmd_kota(a):
    j = req("GET", "/user/subscription")
    print(f"plan: {j.get('tier')}  karakter: {j.get('character_count')}/{j.get('character_limit')}  "
          f"yenileme: {j.get('next_character_count_reset_unix')}")

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    q = sp.add_parser("okunus"); q.add_argument("metin"); q.set_defaults(fn=cmd_okunus)
    q = sp.add_parser("uret"); q.add_argument("metin"); q.add_argument("--out", required=True)
    q.add_argument("--ses", default="bill"); q.add_argument("--ton", default="sakin", choices=list(TON))
    q.add_argument("--hiz", type=float); q.add_argument("--kararlilik", type=float)
    q.add_argument("--benzerlik", type=float, default=0.8); q.add_argument("--stil", type=float); q.set_defaults(fn=cmd_uret)
    q = sp.add_parser("deneme"); q.add_argument("metin"); q.add_argument("--sesler", default="bill,george,daniel")
    q.add_argument("--out-dir", default="deneme"); q.add_argument("--ton", default="sakin", choices=list(TON)); q.set_defaults(fn=cmd_deneme)
    q = sp.add_parser("parcali", help="satırlar JSON'u ({satirlar:[{metin,bas,bit?,ton?}]}) → tek WAV + zamanlama")
    q.add_argument("satirlar"); q.add_argument("--out", required=True); q.add_argument("--ses", default="bill")
    q.add_argument("--ton", default="sakin", choices=list(TON)); q.add_argument("--toplam", type=float); q.set_defaults(fn=cmd_parcali)
    q = sp.add_parser("sesler"); q.add_argument("--dil"); q.set_defaults(fn=cmd_sesler)
    q = sp.add_parser("ambiyans"); q.add_argument("prompt"); q.add_argument("--sure", type=float, default=12)
    q.add_argument("--etki", type=float, default=0.3); q.add_argument("--out", required=True); q.set_defaults(fn=cmd_ambiyans)
    sp.add_parser("kota").set_defaults(fn=cmd_kota)
    a = p.parse_args(); a.fn(a)

if __name__ == "__main__":
    main()
