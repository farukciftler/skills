#!/usr/bin/env python3
"""
uretim.py — senaryo.json'dan yayın Reels'ine tek komutla iş akışı.

  hazirla → klipler → ses → altyazi → katman → montaj → paket

  python3 uretim.py senaryo.json                 # hepsi (fal anahtarı yoksa --taslak'a düşer)
  python3 uretim.py senaryo.json --taslak        # Kling yerine Ken Burns klipleri (bugün çalışır)
  python3 uretim.py senaryo.json --adim ses      # tek aşama
  python3 uretim.py senaryo.json --kuru          # komutları bas, çalıştırma
  python3 uretim.py senaryo.json --sessiz        # seslendirmeyi atla (K8: mimari post sessiz)

Her aşama çıktısı varsa atlanır (--uzerine-yaz ile yenilenir). Klip seçimi:
`secim: {"01-crane-inis": 2}` yoksa 1. varyant — **skor seçmez, göz seçer**;
Kling varyantlarını izleyip `secim` yazmak insanın işi.

senaryo.json alanları (senaryo-sablonlari.md §2 + bu betik):
  cikti_dizini, varsayilan{model,sure,cfg,ses,tekrar}, cekimler[{ad, gorsel, kaynak?, odak?,
  prompt, ekran_metni?, taslak_hareket?}], kapanis{kart,sure}, gecis?, muzik?, ambiyans_prompt?,
  seslendirme{aktif, ses, ton, satirlar[{cekim, metin, ton?}]}, secim{ad: varyant},
  aciklama, alt_metin, etiketler, platform?
"""
import argparse, json, os, shlex, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable

def sh(cmd, kuru=False, capture=False):
    sys.stderr.write("$ " + " ".join(shlex.quote(str(c)) for c in cmd) + "\n")
    if kuru: return None
    r = subprocess.run([str(c) for c in cmd], check=True, capture_output=capture, text=capture)
    return r.stdout if capture else None

def probe_dur(p):
    try:
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                    capture_output=True, text=True).stdout.strip() or 0)
    except Exception:
        return 0.0

def fal_key_var():
    return bool(os.environ.get("FAL_KEY")) or (Path.home() / ".config" / "fal" / "key").is_file()

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("senaryo"); ap.add_argument("--adim", default="hepsi",
                    choices=["hazirla", "klipler", "ses", "altyazi", "katman", "montaj", "paket", "hepsi"])
    ap.add_argument("--taslak", action="store_true", help="Kling yerine Ken Burns")
    ap.add_argument("--sessiz", action="store_true"); ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--uzerine-yaz", action="store_true"); ap.add_argument("--hizli", action="store_true", help="montaj önizleme kodlayıcı")
    a = ap.parse_args()

    S = json.loads(Path(a.senaryo).read_text(encoding="utf-8"))
    root = Path(a.senaryo).resolve().parent
    while root != root.parent and not (root / "CLAUDE.md").exists():
        root = root.parent
    D = root / S["cikti_dizini"]
    for sub in ("kaynak", "klipler", "ses", "alt", "katman"):
        (D / sub).mkdir(parents=True, exist_ok=True)
    V = S.get("varsayilan", {}); gecis = float(S.get("gecis", 0.6))
    cek = S["cekimler"]; adlar = [c["ad"] for c in cek]
    taslak = a.taslak or not fal_key_var()
    if taslak and not a.taslak:
        sys.stderr.write("[not] fal anahtarı yok → --taslak (Ken Burns) moduna düşüldü\n")
    steps = ["hazirla", "klipler", "ses", "altyazi", "katman", "montaj", "paket"] if a.adim == "hepsi" else [a.adim]
    def rel(p): return os.path.relpath(p, os.getcwd())
    def fresh(p): return a.uzerine_yaz or not Path(p).exists()

    # ---------------- 1. hazirla: kaynak → 9:16 jpg
    if "hazirla" in steps:
        for c in cek:
            g = root / c["gorsel"]
            if c.get("kaynak") and fresh(g):
                sh([PY, HERE / "hazirla.py", root / c["kaynak"], "--oran", c.get("oran", "9:16"),
                    "--odak", c.get("odak", "center"), "--out", g], a.kuru)
            elif not g.exists() and not a.kuru:
                sys.exit(f"{c['ad']}: görsel yok: {g} (kaynak alanı ver ya da dosyayı koy)")

    # ---------------- 2. klipler
    secim = S.get("secim", {})
    klip = {c["ad"]: D / "klipler" / f"{c['ad']}-{secim.get(c['ad'], 1)}.mp4" for c in cek}
    if "klipler" in steps:
        if taslak:
            for i, c in enumerate(cek):
                out = D / "klipler" / f"{c['ad']}-1.mp4"
                if fresh(out):
                    mv = c.get("taslak_hareket", ["yakinlas", "uzaklas", "yukari"][i % 3])
                    sh([PY, HERE / "bitir.py", root / c["gorsel"], "--preset", "reels", "--klip-sure", str(V.get("sure", 5)),
                        "--kb", mv, "--gecis", "0", "--acilis-karartma", "0", "--hizli", "--out", out], a.kuru)
        else:
            eksik = [c for c in cek if fresh(D / "klipler" / f"{c['ad']}-1.mp4")]
            if eksik:
                sh([PY, HERE / "kling_video.py", "toplu", Path(a.senaryo).resolve(), "--out-dir", D / "klipler"]
                   + (["--uzerine-yaz"] if a.uzerine_yaz else []), a.kuru)
    durs = [probe_dur(klip[c["ad"]]) or float(V.get("sure", 5)) for c in cek]
    bas = []; t = 0.0
    for i, d in enumerate(durs):
        bas.append(t); t += d - (gecis if i < len(durs) - 1 else 0)
    govde = t
    kap = S.get("kapanis") or {}
    toplam = govde + (float(kap.get("sure", 2.5)) - 0.6 if kap else 0)

    # ---------------- 3. ses: seslendirme (parçalı, çekime hizalı) + yatak
    ses = S.get("seslendirme") or {}
    vo = D / "ses" / "vo.wav"; vo_ok = False
    yatak = root / S["muzik"] if S.get("muzik") else None
    if "ses" in steps and not a.sessiz and ses.get("aktif", True) and ses.get("satirlar"):
        if fresh(vo):
            satirlar = []
            for s_ in ses["satirlar"]:
                i = adlar.index(s_["cekim"]); b = bas[i] + float(s_.get("gecikme", 0.6))
                satirlar.append({"metin": s_["metin"], "bas": round(b, 3), "bit": round(bas[i] + durs[i], 3), "ton": s_.get("ton", ses.get("ton", "sakin"))})
            sat = D / "ses" / "satirlar.json"
            sat.write_text(json.dumps({"satirlar": satirlar}, ensure_ascii=False, indent=2), encoding="utf-8")
            sh([PY, HERE / "seslendir.py", "parcali", sat, "--out", vo, "--ses", ses.get("ses", "bill"),
                "--ton", ses.get("ton", "sakin"), "--toplam", f"{toplam:.3f}"], a.kuru)
        vo_ok = vo.exists() or a.kuru
        if not yatak and S.get("ambiyans_prompt"):
            amb = D / "ses" / "ambiyans.mp3"
            if fresh(amb):
                sh([PY, HERE / "seslendir.py", "ambiyans", S["ambiyans_prompt"], "--sure", str(min(22, int(toplam) + 2)), "--out", amb], a.kuru)
            yatak = amb
    else:
        vo_ok = vo.exists() and not a.sessiz and ses.get("aktif", True)

    # ---------------- 4. altyazi
    alt = D / "alt" / "altyazi.txt"
    if "altyazi" in steps and vo_ok and (fresh(alt) or a.uzerine_yaz):
        sh([PY, HERE / "altyazi.py", vo.with_suffix(".zamanlama.json"), "--out-dir", D / "alt", "--toplam", f"{toplam:.3f}"], a.kuru)

    # ---------------- 5. katman: çekim ekran metinleri + kapanış kartı
    katmanlar = []
    for i, c in enumerate(cek):
        if c.get("ekran_metni"):
            png = D / "katman" / f"{c['ad']}.png"
            if "katman" in steps and fresh(png):
                arg = ["--tek-kelime", c["ekran_metni"]] if c.get("tek_kelime") else ["--baslik", c["ekran_metni"]]
                sh([PY, HERE / "katman.py", "--preset", "cross-9x16"] + arg + ["--out", png], a.kuru)
            b = bas[i] + 0.8; e = bas[i] + durs[i] - 0.4
            katmanlar.append(f"{png}@{b:.2f}:{e:.2f}")
    kart = D / "katman" / "logo-kart.png"
    if kap and "katman" in steps and fresh(kart):
        sh([PY, HERE / "katman.py", "--preset", "cross-9x16", "--sadece-logo", "--out", kart], a.kuru)

    # ---------------- 6. montaj
    out = D / f"{D.name}.mp4"
    if "montaj" in steps:
        cmd = [PY, HERE / "bitir.py"] + [klip[c["ad"]] for c in cek] + ["--preset", "reels", "--gecis", str(gecis),
               "--platform", S.get("platform", "instagram"), "--out", out]
        for k in katmanlar: cmd += ["--katman", k]
        if kap: cmd += ["--kapanis", kart, "--kapanis-sure", str(kap.get("sure", 2.5))]
        if vo_ok: cmd += ["--seslendirme", vo, "--ses-baslangic", "0"]
        if vo_ok and alt.exists(): cmd += ["--altyazi", alt]
        if yatak and (Path(yatak).exists() or a.kuru): cmd += ["--muzik", yatak, "--muzik-db", str(S.get("muzik_db", -20 if vo_ok else 0))]
        if S.get("derece"): cmd += ["--derece", S["derece"]]
        if a.hizli: cmd += ["--hizli"]
        sh(cmd, a.kuru)

    # ---------------- 7. paket: kapak, açıklama, künye
    if "paket" in steps and not a.kuru and out.exists():
        sh([PY, HERE / "bitir.py", out, "--kapak", "1.0", "--out", D / "kapak.png"])
        beyan = ["Temsili görseldir; görseller yapay zekâ desteğiyle hareketlendirilmiştir."]
        if vo_ok: beyan.append("Seslendirme yapay zekâ ile üretilmiştir.")
        acik = S.get("aciklama", "").strip()
        for b in beyan:
            if b not in acik: acik = acik.replace("\n\n#", f"\n\n{b}\n\n#", 1) if "\n\n#" in acik else acik + "\n\n" + b
        txt = (f"{S.get('baslik','')}\n\n=== AÇIKLAMA ===\n{acik}\n\n=== ALT METİN ===\n{S.get('alt_metin','')}\n"
               f"\n=== KONUM ===\n{S.get('konum','Aydıntepe, Tuzla')}\n\n=== KAYNAK NOTU ===\n{S.get('kaynak_notu','')}\n"
               f"\n=== ÜRETİM ===\nklipler: {'taslak Ken Burns' if taslak else 'Kling ' + V.get('model','v3-pro')}\n"
               f"seslendirme: {'evet, ' + ses.get('ses','bill') if vo_ok else 'yok'}\nsüre: {toplam:.1f} sn\n")
        (D / "aciklama.txt").write_text(txt, encoding="utf-8")
        qc = json.loads((str(out) + ".qc.json") and Path(str(out) + ".qc.json").read_text(encoding="utf-8")) if Path(str(out) + ".qc.json").exists() else {}
        print(f"\n✓ paket: {rel(D)}\n  video   {out.name}  {qc.get('olculen_sure')} sn  {qc.get('boyut_mb')} MB  "
              f"{'TEMİZ' if qc.get('tamam') else 'SORUN: ' + '; '.join(qc.get('sorunlar', []))}\n"
              f"  kapak   kapak.png · açıklama aciklama.txt · qc {out.name}.qc.json\n"
              f"  {'TASLAK — kaynak katalog türevi / Ken Burns; Kling ve ofis render’ı ile yeniden üretilecek' if taslak else ''}")

if __name__ == "__main__":
    main()
