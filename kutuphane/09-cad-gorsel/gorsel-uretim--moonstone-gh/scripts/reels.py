#!/usr/bin/env python3
"""
reels.py — Moonstone icin dikey motion icerik (Reels · Story · TikTok).

  python3 reels.py --recipe tarif.json --out cikti.mp4

Tasarim kararlari, hepsi olculmus gerekcelere dayali:

1. BUTUN TIPOGRAFI PILLOW'DA RASTERLENIR. Bu makinedeki ffmpeg libass,
   freetype ve fontconfig OLMADAN derlenmis — `drawtext` ve `subtitles`
   filtreleri yok (dogrulandi: `ffmpeg -filters` ikisini de listelemiyor).
   Metin seffaf PNG olarak cizilir, ffmpeg yalnizca `overlay` yapar.
   Bu bir gecici cozum degil: font dosyasi depoda oldugu icin cikti
   makineden makineye bit-bit ayni kaliyor.

2. ZOOMPAN ONCESI YUKSEK OLCEK. zoompan tam piksel adimlarla calisir; kaynak
   buyutulmeden uygulanirsa titrer. Once 2x olceklenir, sonra kirpilir.

3. KOSINUS YUMUSATMA. Dogrusal zoom mekanik duruyor;
   z = 1 + a*(1-cos(PI*t))/2 yavas baslayip ortada hizlanip yumusak duruyor.

4. SES: muzik yatagi + seslendirme, yan zincir sikistirma ile ducking.
   Konusma varken yatak otomatik olarak geri cekilir.

Muzik ve Turkce okunus donusumu icin reelsindustry motorlari kullanilir
(bkz. references/motion-hatti.md).
"""
import argparse, json, os, subprocess, sys, tempfile, shutil
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frame as F

W, H = 1080, 1920
GOLD, WHITE, INK = F.GOLD, F.WHITE, F.INK

def run(cmd, quiet=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-1800:] + "\n")
        raise SystemExit(f"ffmpeg hatasi: {' '.join(cmd[:6])}…")
    return r

def probe(path, stream="v"):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream + ":0",
                        "-show_entries", "stream=width,height,duration",
                        "-show_entries", "format=duration", "-of", "json", path],
                       capture_output=True, text=True)
    d = json.loads(r.stdout or "{}")
    st = (d.get("streams") or [{}])[0]
    dur = st.get("duration") or d.get("format", {}).get("duration")
    return dict(w=st.get("width"), h=st.get("height"), dur=float(dur) if dur else None)

# ─────────────────────────────────────────────────────────── metin plakalari

def plate(spec, out):
    """Seffaf 1080x1920 metin katmani. Guvenli alan: ust 140 / alt 400 —
    Instagram ve TikTok'un ortak (en dar) alani, tek surumle ikisi de kurtulur."""
    st, sb, sl, sr = 140, 400, 70, 130
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cw = W - sl - sr
    align = spec.get("align", "bottom")
    fg = F.parse_color(spec.get("fg", "white"))
    acc = F.parse_color(spec.get("accent", "gold"))

    blocks = []
    if spec.get("eyebrow"):
        f = F.load(F.BODY_BOLD_CHAIN, spec.get("eyebrow_size", 28), "body")
        h = int(f.size * 1.35)
        blocks.append((h + 22, lambda y, f=f, h=h: (F.tracked(d, (sl, y), spec["eyebrow"].upper(), f, acc, 0.22), h)[1]))
    if spec.get("rule", True) and spec.get("eyebrow"):
        blocks.append((3 + 30, lambda y: (d.rectangle([sl, y, sl + 110, y + 3], fill=acc), 3)[1]))
    if spec.get("number"):
        f = F.load(F.DISPLAY_CHAIN, spec.get("number_size", 150), "display")
        h = int(f.size * 1.02)
        blocks.append((h + 18, lambda y, f=f, h=h: (F.tracked(d, (sl, y - int(f.size * .24)), spec["number"], f, acc, .01), h)[1]))
    if spec.get("title"):
        f = F.load(F.DISPLAY_CHAIN, spec.get("title_size", 82), "display")
        lines = F.wrap(spec["title"], f, cw, .02)
        lh = int(f.size * 1.16); h = lh * len(lines)
        def dt(y, f=f, lines=lines, lh=lh, h=h):
            yy = y - int(f.size * .22)
            for ln in lines:
                F.tracked(d, (sl, yy), ln, f, fg, .02); yy += lh
            return h
        blocks.append((h + 22, dt))
    if spec.get("body"):
        f = F.load(F.BODY_CHAIN, spec.get("body_size", 38), "body")
        lines = []
        for para in spec["body"].split("\n"):
            lines += F.wrap(para, f, cw) if para.strip() else [""]
        lh = int(f.size * 1.52); h = lh * len(lines)
        def db(y, f=f, lines=lines, lh=lh, h=h):
            yy = y
            for ln in lines:
                d.text((sl, yy), ln, font=f, fill=fg); yy += lh
            return h
        blocks.append((h + 16, db))

    total = sum(b[0] for b in blocks)
    y = {"bottom": H - sb - total, "center": (H - total) // 2, "top": st}[align]
    y += spec.get("offset", 0)
    for adv, fn in blocks:
        fn(y); y += adv

    if spec.get("logo"):
        lp = F.logo_png(spec.get("logo_variant", "dark"), 480)
        if lp:
            lg = Image.open(lp).convert("RGBA"); lg.thumbnail((spec.get("logo_w", 160), 600), Image.LANCZOS)
            pos = spec.get("logo_pos", "top-left")
            lx = sl if "left" in pos else (W - sr - lg.width if "right" in pos else (W - lg.width) // 2)
            ly = st if "top" in pos else H - sb - lg.height
            img.alpha_composite(lg, (lx, ly))
    img.save(out)
    return out

def scrim_png(out, strength=0.92, ease=0.75, where="bottom", color=None):
    """Okunabilirlik katmani. Aydinlik temada `color` krem verilir ve metin
    koyu olur; koyu temada lacivert kalir ve metin beyaz olur."""
    col = F.parse_color(color) if color else INK
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if where in ("bottom", "both"):
        img.alpha_composite(F.vgradient(W, H, col, 0, int(255 * strength), ease=ease))
    if where in ("top", "both"):
        img.alpha_composite(F.vgradient(W, H, col, int(255 * strength * .55), 0, ease=1.8))
    img.save(out); return out

# ─────────────────────────────────────────────────────────────── cekim akisi

def shot_filter(idx, sh, fps):
    """Tek cekimi 1080x1920'ye getirir + hareket uygular. Cikti: [vN]

    sh["grade"]: kare bazli renk duzeltmesi, ffmpeg filtre dizesi.
    B-roll'ler markanin lacivert-altin paletine oturmuyorsa burada duzeltilir;
    ornek: "eq=saturation=0.55:contrast=1.06,colorbalance=bs=0.10:rm=-0.04"
    (yesile kacan bitki/beton kliplerini laciverte ceker)."""
    dur = sh["dur"]
    g = ("," + sh["grade"]) if sh.get("grade") else ""
    if sh.get("kind") == "still":
        # 2x olcek → zoompan (titremeyi onler) → kirp
        z0, z1 = sh.get("z", [1.0, 1.12])
        px, py = sh.get("focus", [0.5, 0.5])
        n = max(2, int(dur * fps))
        zexpr = f"{z0}+({z1}-{z0})*(1-cos(PI*on/{n-1}))/2"
        return (f"[{idx}:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,"
                f"crop={W*2}:{H*2},"
                f"zoompan=z='{zexpr}':x='iw*{px}-(iw/zoom/2)':y='ih*{py}-(ih/zoom/2)'"
                f":d={n}:s={W}x{H}:fps={fps},"
                f"trim=duration={dur},setpts=PTS-STARTPTS{g},format=yuv420p[v{idx}]")
    ss = sh.get("in", 0)
    return (f"[{idx}:v]trim=start={ss}:duration={dur},setpts=PTS-STARTPTS,"
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"fps={fps}{g},format=yuv420p[v{idx}]")

def build(recipe, out, workdir):
    fps = recipe.get("fps", 30)
    shots = recipe["shots"]
    total = sum(s["dur"] for s in shots)

    inputs, filt = [], []
    for i, sh in enumerate(shots):
        if sh.get("kind") == "still":
            inputs += ["-loop", "1", "-t", str(sh["dur"] + 0.2), "-i", sh["src"]]
        else:
            inputs += ["-i", sh["src"]]
        filt.append(shot_filter(i, sh, fps))

    # cekimleri capraz gecisle birlestir
    xf = recipe.get("xfade", 0.5)
    cur, off = "v0", shots[0]["dur"] - xf
    for i in range(1, len(shots)):
        lbl = f"x{i}"
        filt.append(f"[{cur}][v{i}]xfade=transition={recipe.get('transition','fade')}"
                    f":duration={xf}:offset={off:.3f}[{lbl}]")
        cur = lbl; off += shots[i]["dur"] - xf
    vtotal = total - xf * (len(shots) - 1)

    n = len(shots)
    # scrim
    scr = scrim_png(os.path.join(workdir, "scrim.png"),
                    recipe.get("scrim_strength", 0.92), recipe.get("scrim_ease", 0.75),
                    recipe.get("scrim", "bottom"), recipe.get("scrim_color"))
    inputs += ["-loop", "1", "-i", scr]
    filt.append(f"[{cur}][{n}:v]overlay=0:0:format=auto[sc]"); cur = "sc"; n += 1

    # metin plakalari — belirme/kaybolma zamanli
    for j, p in enumerate(recipe.get("plates", [])):
        png = plate(p, os.path.join(workdir, f"plate{j}.png"))
        inputs += ["-loop", "1", "-i", png]
        t0, pd = p.get("t", 0.0), p.get("dur", 4.0)
        fi, fo = p.get("fade_in", 0.6), p.get("fade_out", 0.6)
        sl = p.get("slide", 26)
        filt.append(f"[{n}:v]format=rgba,fade=t=in:st={t0}:d={fi}:alpha=1,"
                    f"fade=t=out:st={t0+pd-fo}:d={fo}:alpha=1[p{j}]")
        yexpr = f"'if(lt(t,{t0+fi}),{sl}-{sl}*(t-{t0})/{fi},0)'"
        filt.append(f"[{cur}][p{j}]overlay=0:y={yexpr}:enable='between(t,{t0},{t0+pd})'[o{j}]")
        cur = f"o{j}"; n += 1

    # --- karaoke altyazi: PNG dizisi concat demuxer'i ile DOGRUDAN girdi olur
    if recipe.get("altyazi"):
        import altyazi as A
        cfg = recipe["altyazi"]
        kaynak = cfg.get("ses") or recipe.get("vo_file")
        kl = A.kelime_zamanlari(kaynak)
        liste, _ = A.uret(kl, os.path.join(workdir, "alt"),
                          gecikme=cfg.get("gecikme", recipe.get("vo_delay", 0.0)),
                          boy=cfg.get("boy", 46), y=cfg.get("y", 1000))
        inputs += ["-f", "concat", "-safe", "0", "-i", liste]
        filt.append(f"[{n}:v]fps={fps},format=rgba[cap]")
        filt.append(f"[{cur}][cap]overlay=0:0:eof_action=pass:format=auto[capout]")
        cur = "capout"; n += 1

    # kapanis: hafif grade + vinyet + grain (ambient-video-forge dersleri)
    filt.append(f"[{cur}]eq=saturation={recipe.get('saturation',0.96)}:contrast={recipe.get('contrast',1.04)},"
                f"vignette=PI*{recipe.get('vignette',0.13)},"
                f"noise=alls={recipe.get('grain',6)}:allf=t+u,"
                f"fade=t=in:st=0:d=0.5,fade=t=out:st={vtotal-0.6:.2f}:d=0.6,"
                f"format=yuv420p[vout]")

    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", ";".join(filt),
           "-map", "[vout]", "-t", f"{vtotal:.3f}",
           "-r", str(fps), "-c:v", "hevc_videotoolbox", "-q:v", "62", "-tag:v", "hvc1",
           os.path.join(workdir, "video.mp4")]
    run(cmd)
    return os.path.join(workdir, "video.mp4"), vtotal

def mix_audio(video, recipe, out, workdir, dur):
    music, vo = recipe.get("music_file"), recipe.get("vo_file")
    if not music and not vo:
        shutil.copy(video, out); return
    ins, filt = ["-i", video], []
    idx = 1
    if music:
        ins += ["-i", music]; m = idx; idx += 1
    if vo:
        ins += ["-i", vo]; v = idx; idx += 1

    if music and vo:
        vd = recipe.get("vo_delay", 1.0)
        filt.append(f"[{v}:a]adelay={int(vd*1000)}|{int(vd*1000)},volume={recipe.get('vo_gain',1.25)},"
                    f"highpass=f=90,acompressor=threshold=0.12:ratio=3:attack=8:release=180,"
                    # sessizlikle uzat: sidechaincompress yan zincir bitince duruyor,
                    # uzatilmazsa muzik seslendirme bitiminde kesiliyor
                    f"apad=whole_dur={dur:.3f},"
                    f"asplit=2[vo1][vo2]")   # bir etiket yalnizca bir kez tuketilebilir
        filt.append(f"[{m}:a]volume={recipe.get('music_gain',0.55)}[bed]")
        # yan zincir ducking: konusma varken yatak geri cekilir
        filt.append("[bed][vo1]sidechaincompress=threshold=0.045:ratio=7:attack=12:release=420[duck]")
        filt.append(f"[duck][vo2]amix=inputs=2:duration=first:dropout_transition=0,"
                    f"atrim=duration={dur:.3f},alimiter=limit=0.94,aformat=sample_fmts=fltp[aout]")
    elif music:
        filt.append(f"[{m}:a]volume={recipe.get('music_gain',0.8)},atrim=duration={dur:.3f},"
                    f"afade=t=out:st={max(0,dur-1.4):.2f}:d=1.2,alimiter=limit=0.94[aout]")
    else:
        filt.append(f"[{v}:a]volume={recipe.get('vo_gain',1.2)},atrim=duration={dur:.3f}[aout]")

    run(["ffmpeg", "-y"] + ins + ["-filter_complex", ";".join(filt),
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-shortest", out])

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--recipe", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--keep", action="store_true", help="ara dosyalari sakla")
    a = p.parse_args()
    recipe = json.load(open(a.recipe, encoding="utf-8"))
    wd = tempfile.mkdtemp(prefix="ms-reels-")
    try:
        vid, dur = build(recipe, a.out, wd)
        mix_audio(vid, recipe, a.out, wd, dur)
        info = probe(a.out)
        print(f"{a.out}  {info['w']}x{info['h']}  {info['dur']:.1f}s  "
              f"{os.path.getsize(a.out)/1048576:.1f} MB")
    finally:
        if a.keep: print("ara dosyalar:", wd)
        else: shutil.rmtree(wd, ignore_errors=True)

if __name__ == "__main__":
    main()
