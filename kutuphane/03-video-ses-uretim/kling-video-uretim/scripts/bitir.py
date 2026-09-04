#!/usr/bin/env python3
"""
bitir.py — Kling kliplerini (ve sabit görselleri) yayın formatına getirir.

Kalıpların kaynağı: ~/Documents/GitHub/weftrecords (ambient-video-forge,
build_soc_video.py) ve ~/projects/reelsindustry (motor/kurgu/ffmpeg_serit.py,
goruntu/durgun.py, kart.py) — ölçülmüş kararlar references/post-produksiyon.md §1b.
Bu makinenin ffmpeg'i drawtext/subtitles içermiyor: yazı yalnızca PNG overlay.

Girdi: MP4 ve/veya PNG/JPG (görsel → Ken Burns klibi; kat planı, eskiz, harita).

Sırayla:
  1. her klip: trim → oturt (kırp | bulanık kendi-dolgu | lacivert bant) →
     setsar=1, fps=30 (filtre olarak, CFR), settb=AVTB, format=yuv420p
  2. xfade zinciri; ofset zincir uzunluğu üzerinden birikir; ya da concat
  3. --bekle (tpad) · --dongu (ileri+geri) · --dongu-xfade (kuyruk→baş)
  4. --katman PNG: alfa fade + enable aralığı
  5. --kapanis kartı: GÖVDEDEN SONRA eklenir (önce eklenirse süre kırpması kartı yer)
  6. --derece: kimlik dosyasındaki derecelendirme dizesi, olduğu gibi
  7. --muzik: iki geçişli loudnorm (önce ölç, sonra linear=true), platform hedefi
     (instagram −16 · youtube/tiktok −14), 48 kHz stereo, video süresine kes
  6b. --seslendirme: konuşma + yatak (1–3 kHz −7 dB oyuk, sidechain ducking) → miks WAV → ölç → linear
  6c. --altyazi: altyazi.py concat listesi, eof_action=pass
  8. kodlama: yayın = libx264 crf 17 veryfast High 4.2 (Instagram yeniden kodlar,
     temiz kaynak kazanır) · --hizli = h264_videotoolbox 12M önizleme ·
     bt709 etiketi · GOP 2 sn · faststart · -t toplam
  9. QC: akış hatasız çözülmeli (ffmpeg -v error … -f null) · süre ±0,3 sn ·
     ölçü · boyut/bit hızı · <out>.qc.json raporu

Denetim modları (çıktı üretmeden çıkar):
  --son-kare son.png        ilk klibin son karesi (zincirleme)
  --kapak 1.0 --out k.png   kapak karesi (1. saniyeden; ilk kare sık karanlık açılır)
  --guvenli-alan            UI bantlarını kırmızı basar, gözle bak
  --dongu-kontrol           klibi kendine ekler, dikişe bak (çapraz geçişle "düzeltme")

  python3 bitir.py k1.mp4 k2.mp4 --preset reels --katman katman.png --katman-baslangic 4.4 \
      --kapanis logo-kart.png --muzik m.mp3 --platform instagram --out r.mp4
  python3 bitir.py plan_tip5.png --klip-sure 6 --kb yukari --doldur bulanik --out plan.mp4
"""
import argparse, json, os, re, shlex, subprocess, sys

PRESETS = {"reels": (1080, 1920), "story": (1080, 1920), "feed-45": (1080, 1350),
           "kare": (1080, 1080), "web": (1920, 1080), "web-4k": (3840, 2160)}
FPS = 30
IMG_EXT = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
LUFS = {"instagram": -16.0, "youtube": -14.0, "tiktok": -14.0, "web": -16.0}
# güvenli alan bantları (px): üst, alt, sağ — Instagram Reels; TikTok alt 400 zaten kapsıyor
SAFE = {"reels": (250, 400, 180), "story": (250, 250, 65), "feed-45": (60, 60, 60),
        "kare": (56, 56, 56), "web": (0, 0, 0), "web-4k": (0, 0, 0)}
KB_MAX, KB_REF_S = 0.06, 9.0        # durgun.py: en fazla %6 zoom, 9 sn referans; kısa klipte orantılı az
INK = "#040C1D"

def probe(path):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams",
                                   "-show_format", path], capture_output=True, text=True, check=True).stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    fr = (v or {}).get("avg_frame_rate", "30/1")
    try:
        a, b = fr.split("/"); fps = float(a) / float(b) if float(b) else 30.0
    except Exception:
        fps = 30.0
    return dict(w=int(v["width"]) if v else 0, h=int(v["height"]) if v else 0,
                dur=float(j["format"].get("duration", 0) or 0), fps=fps,
                audio=any(s["codec_type"] == "audio" for s in j["streams"]),
                size=int(j["format"].get("size", 0) or 0),
                codec=(v or {}).get("codec_name"), pix=(v or {}).get("pix_fmt"))

def run(cmd, capture=False):
    sys.stderr.write("$ " + " ".join(shlex.quote(c) for c in cmd) + "\n")
    return subprocess.run(cmd, check=True, capture_output=capture, text=capture)

def is_img(p):
    return os.path.splitext(p)[1].lower() in IMG_EXT

def fit_chain(W, H, mode, fy):
    if mode == "bulanik":   # weftrecords 'pillar': arkada bulanık büyütülmüş kopya, önde tam kare
        return (f"split=2[bgsrc][fgsrc];"
                f"[bgsrc]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
                f"gblur=sigma=40,eq=brightness=-0.18:saturation=0.85,setsar=1[bg];"
                f"[fgsrc]scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos,setsar=1[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2:format=auto,")
    if mode == "bant":
        return (f"scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos,"
                f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:{INK},")
    return f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}:(iw-ow)/2:{fy},"

def kenburns(W, H, fy, seg, move, amount):
    """durgun.py kalıbı: 2× çalışma tuvali (tam piksel adım titremesi kalkar), süreye orantılı zoom."""
    frames = max(2, int(round(seg * FPS)))
    pay = min(amount, amount * seg / KB_REF_S)
    adim = pay / frames
    if move.startswith("uzaklas"):
        z = f"if(eq(on,0),{1 + pay:.6f},max(zoom-{adim:.8f},1.0))"
    else:
        z = f"min(zoom+{adim:.8f},{1 + pay:.6f})"
    mx, my = "(iw-iw/zoom)*0.5", "(ih-ih/zoom)*0.5"
    if move == "yukari":   my = f"(ih-ih/zoom)*(1-on/{frames})"
    elif move == "asagi":  my = f"(ih-ih/zoom)*(on/{frames})"
    elif move.endswith("-sol"): mx = f"(iw-iw/zoom)*(1-on/{frames})"
    elif move.endswith("-sag"): mx = f"(iw-iw/zoom)*(on/{frames})"
    if amount <= 0:
        return f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}:(iw-ow)/2:{fy},"
    return (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase:flags=lanczos,crop={W*2}:{H*2}:(iw-ow)/2:{fy},"
            f"zoompan=z='{z}':x='{mx}':y='{my}':d=1:s={W}x{H}:fps={FPS},")

def loudnorm_measure(path, total, target):
    """1. geçiş: karışımı ölç. Tek geçişli loudnorm kompresör gibi pompalar."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-t", f"{total:.3f}",
                        "-af", f"loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    blocks = re.findall(r"\{[^{}]*\}", r.stderr)      # JSON'dan sonra başka satırlar geliyor; son bloğu al
    try:
        return json.loads(blocks[-1]) if blocks else None
    except Exception:
        return None

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("klipler", nargs="+")
    p.add_argument("--preset", default="reels", help=", ".join(PRESETS))
    p.add_argument("--out")
    p.add_argument("--odak", default="center", choices=["center", "top", "bottom"])
    p.add_argument("--doldur", default="kirp", choices=["kirp", "bulanik", "bant"])
    p.add_argument("--gecis", type=float, default=0.6, help="xfade sn; 0 = sert kesme")
    p.add_argument("--gecis-tipi", default="fade")
    p.add_argument("--klip-sure", type=float, help="her klibi baştan bu kadar sn; görsel klibi süresi (vars. 5)")
    p.add_argument("--kb", default="yakinlas,uzaklas",
                   help="görsel girdiler için Ken Burns hareketi, virgülle sırayla: yakinlas uzaklas yukari asagi yakinlas-sol uzaklas-sag; 'yok' sabit")
    p.add_argument("--kb-miktar", type=float, default=KB_MAX, help="9 sn'de azami zoom payı (0.06 = %%6)")
    p.add_argument("--bekle", type=float, default=0)
    p.add_argument("--katman", action="append", default=[],
                   help="şeffaf PNG; tekrarlanabilir; 'yol@bas:bit' ile aralık (bit boş = sona kadar)")
    p.add_argument("--katman-baslangic", type=float, default=0.0)
    p.add_argument("--katman-bitis", type=float); p.add_argument("--katman-fade", type=float, default=0.5)
    p.add_argument("--kapanis"); p.add_argument("--kapanis-sure", type=float, default=2.5)
    p.add_argument("--acilis-karartma", type=float, default=0.4)
    p.add_argument("--derece", help="derecelendirme filtre dizesi (kimlik dosyasından, olduğu gibi)")
    p.add_argument("--muzik"); p.add_argument("--platform", default="instagram", choices=list(LUFS))
    p.add_argument("--seslendirme", help="seslendir.py çıktısı WAV; müzik altına oyulur ve ducking uygulanır")
    p.add_argument("--ses-baslangic", type=float, default=0.6, help="seslendirmenin başlangıcı (sn)")
    p.add_argument("--muzik-db", type=float, default=-20.0, help="konuşma altındaki yatak seviyesi (dB)")
    p.add_argument("--altyazi", help="altyazi.py concat listesi (altyazi.txt)")
    p.add_argument("--muzik-ses", type=float, help="LUFS hedefi; boşsa platforma göre")
    p.add_argument("--dongu", action="store_true"); p.add_argument("--dongu-xfade", type=float, default=0)
    p.add_argument("--son-kare"); p.add_argument("--kapak", type=float)
    p.add_argument("--guvenli-alan", action="store_true"); p.add_argument("--dongu-kontrol", action="store_true")
    p.add_argument("--hizli", action="store_true", help="önizleme: h264_videotoolbox 12M (yayına libx264)")
    p.add_argument("--kodlayici", help="libx264 | h264_videotoolbox | hevc_videotoolbox (Instagram'a HEVC verme)")
    p.add_argument("--crf", type=int, default=17); p.add_argument("--bitrate", default="12M")
    p.add_argument("--kuru", action="store_true")
    a = p.parse_args()

    if a.preset not in PRESETS:
        sys.exit("preset bilinmiyor")
    W, H = PRESETS[a.preset]
    src0 = a.klipler[0]

    # ---------------- denetim modları
    if a.son_kare:
        run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.05", "-i", src0, "-frames:v", "1", "-q:v", "1", a.son_kare])
        print(a.son_kare); return
    if a.kapak is not None:
        out = a.out or os.path.splitext(src0)[0] + "-kapak.png"
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(a.kapak), "-i", src0, "-frames:v", "1", out])  # -ss girişten önce: arar, çözmez
        print(out); return
    if a.guvenli_alan:
        t, b, r = SAFE[a.preset]
        out = a.out or os.path.splitext(src0)[0] + "-guvenli-alan.mp4"
        vf = (f"drawbox=x=0:y=0:w={W}:h={t}:color=red@0.35:t=fill,"
              f"drawbox=x=0:y={H-b}:w={W}:h={b}:color=red@0.35:t=fill,"
              f"drawbox=x={W-r}:y=0:w={r}:h={H}:color=red@0.25:t=fill")
        run(["ffmpeg", "-y", "-v", "error", "-i", src0, "-vf", vf, "-c:v", "h264_videotoolbox", "-b:v", "4M", "-an", out])
        print(out, "— kırmızı bantlara giren metin/logo var mı, gözle bak"); return
    if a.dongu_kontrol:
        out = a.out or os.path.splitext(src0)[0] + "-dongu-kontrol.mp4"
        lst = out + ".txt"
        with open(lst, "w") as f:
            f.write(f"file '{os.path.abspath(src0)}'\nfile '{os.path.abspath(src0)}'\n")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-fflags", "+genpts", out])
        os.remove(lst)
        print(out, "— dikişte sıçrama varsa döngü kapanmıyor: son kareyi ilk kareye eşle ya da --dongu-xfade; sonradan çapraz geçişle örtme"); return

    out = a.out or os.path.splitext(src0)[0] + f"-{a.preset}.mp4"
    inputs, fc, durs = [], [], []
    n = len(a.klipler)
    fy = {"top": "0", "center": "(ih-oh)/2", "bottom": "ih-oh"}[a.odak]
    kb_moves = [m.strip() for m in a.kb.split(",") if m.strip()]
    img_i = 0
    TAIL = f"setsar=1,fps={FPS},settb=AVTB,format=yuv420p"

    # ---------------- 1. klipler
    for i, c in enumerate(a.klipler):
        if is_img(c):
            seg = a.klip_sure or 5.0
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{seg:.3f}", "-i", c]
            move = kb_moves[img_i % len(kb_moves)] if kb_moves and kb_moves[0] != "yok" else "yok"
            img_i += 1
            kb = kenburns(W, H, fy, seg, move, 0 if move == "yok" else a.kb_miktar)
            fc.append(f"[{i}:v]{kb}trim=duration={seg:.3f},setpts=PTS-STARTPTS,{TAIL}[v{i}]")
            durs.append(seg)
        else:
            inf = probe(c)
            if inf["dur"] <= 0:
                sys.exit(f"{c}: süre okunamadı")
            inputs += ["-i", c]
            d = min(inf["dur"], a.klip_sure) if a.klip_sure else inf["dur"]
            trim = f"trim=0:{d:.3f},setpts=PTS-STARTPTS," if a.klip_sure else ""
            fc.append(f"[{i}:v]{trim}{fit_chain(W, H, a.doldur, fy)}{TAIL}[v{i}]")
            durs.append(d)
    if a.gecis > 0 and n > 1 and min(durs) <= a.gecis:
        sys.exit(f"bir klip ({min(durs):.2f} sn) geçişten ({a.gecis} sn) kısa — dur")

    # ---------------- 2. birleştir: offset_k = offset_{k-1} + d_k − f ; toplam = Σd − (N−1)f
    cur, total, off = "v0", durs[0], 0.0
    for i in range(1, n):
        if a.gecis > 0:
            off += durs[i - 1] - a.gecis
            fc.append(f"[{cur}][v{i}]xfade=transition={a.gecis_tipi}:duration={a.gecis}:offset={off:.3f}[x{i}]")
            total += durs[i] - a.gecis
        else:
            fc.append(f"[{cur}][v{i}]concat=n=2:v=1:a=0[x{i}]"); total += durs[i]
        cur = f"x{i}"

    # ---------------- 3. döngü / bekleme
    if a.dongu:
        fc.append(f"[{cur}]split[pa][pb];[pb]reverse,trim=start_frame=1,setpts=PTS-STARTPTS[pr];"
                  f"[pa][pr]concat=n=2:v=1:a=0[pp]"); cur = "pp"; total *= 2
    if a.dongu_xfade > 0:
        xf = a.dongu_xfade
        fc.append(f"[{cur}]split=3[da][db][dc];"
                  f"[da]trim=start={xf}:end={total - xf:.3f},setpts=PTS-STARTPTS[mid];"
                  f"[db]trim=start={total - xf:.3f},setpts=PTS-STARTPTS[tail];"
                  f"[dc]trim=end={xf},setpts=PTS-STARTPTS[head];"
                  f"[tail][head]xfade=transition=fade:duration={xf}:offset=0[cf];"
                  f"[mid][cf]concat=n=2:v=1:a=0[dl]"); cur = "dl"; total -= xf
    if a.bekle > 0:
        fc.append(f"[{cur}]tpad=stop_mode=clone:stop_duration={a.bekle}[hold]"); cur = "hold"; total += a.bekle

    # ---------------- 4. katman(lar) (PIL PNG + overlay; drawtext bu makinede yok)
    idx = n
    for ki, spec in enumerate(a.katman):
        path, st_, end = spec, a.katman_baslangic, (a.katman_bitis if a.katman_bitis else total)
        if "@" in spec:
            path, ar = spec.rsplit("@", 1)
            b_, _, e_ = ar.partition(":")
            st_ = float(b_) if b_ else st_; end = float(e_) if e_ else total
        end = min(end, total); fd = a.katman_fade
        inputs += ["-loop", "1", "-i", path]
        fc.append(f"[{idx}:v]scale={W}:{H},setsar=1,fps={FPS},settb=AVTB,format=rgba,"
                  f"fade=t=in:st={st_:.3f}:d={fd}:alpha=1,fade=t=out:st={max(0, end - fd):.3f}:d={fd}:alpha=1[ov{ki}]")
        fc.append(f"[{cur}][ov{ki}]overlay=0:0:shortest=1:format=auto:enable='between(t,{st_:.3f},{end:.3f})'[ovd{ki}]")
        cur = f"ovd{ki}"; idx += 1

    # ---------------- 4b. altyazı: PNG concat demuxer, ara kodlama yok (reelsindustry kalıbı)
    if a.altyazi:
        inputs += ["-f", "concat", "-safe", "0", "-i", a.altyazi]
        fc.append(f"[{idx}:v]fps={FPS},scale={W}:{H},setsar=1,format=rgba,settb=AVTB[alt]")
        fc.append(f"[{cur}][alt]overlay=0:0:format=auto:eof_action=pass[valt]")
        cur = "valt"; idx += 1

    # ---------------- 5. kapanış — GÖVDEDEN SONRA
    if a.kapanis:
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{a.kapanis_sure:.3f}", "-i", a.kapanis]
        fc.append(f"[{idx}:v]scale={W}:{H},{TAIL},fade=t=out:st={a.kapanis_sure - 0.6:.3f}:d=0.6[card]")
        fc.append(f"[{cur}][card]xfade=transition=fadeblack:duration=0.6:offset={total - 0.6:.3f}[fin]")
        cur = "fin"; total += a.kapanis_sure - 0.6; idx += 1
    if a.derece:
        fc.append(f"[{cur}]{a.derece}[gr]"); cur = "gr"
    if a.acilis_karartma > 0:
        fc.append(f"[{cur}]fade=t=in:st=0:d={a.acilis_karartma}[vo]"); cur = "vo"
    # bt709 etiketi: yalnızca CLI bayrağı filter_complex çıktısında primaries/trc yazmıyor (ölçüldü) → setparams
    fc.append(f"[{cur}]setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv[vtag]"); cur = "vtag"

    # ---------------- 6. ses: (a) konuşma + oyulmuş/ducking'li yatak → WAV, (b) ölç, (c) linear loudnorm
    maps = ["-map", f"[{cur}]"]
    target = a.muzik_ses if a.muzik_ses is not None else LUFS[a.platform]
    meas = None; ses_kaynak = None
    if a.seslendirme:
        mix = out + ".miks.wav"
        g = []
        g.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(a.ses_baslangic*1000)}|{int(a.ses_baslangic*1000)},"
                 f"apad,atrim=0:{total:.3f},asetpts=PTS-STARTPTS[konusma]")
        if a.muzik:
            g.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,aloop=loop=-1:size=2e9,atrim=0:{total:.3f},"
                     f"asetpts=PTS-STARTPTS,equalizer=f=2000:t=q:w=1.2:g=-7,volume={a.muzik_db}dB[yatak_ham]")
            g.append("[konusma]asplit=2[k1][k2];[yatak_ham][k2]sidechaincompress=threshold=0.03:ratio=8:attack=15:release=350[yatak]")
            g.append("[k1][yatak]amix=inputs=2:duration=first:normalize=0[karisim]")
        else:
            g.append("[konusma]anull[karisim]")
        g.append(f"[karisim]afade=t=in:st=0:d=0.3,afade=t=out:st={max(0, total-1.0):.3f}:d=1.0,aresample=48000[son]")
        ins = ["-i", a.seslendirme] + (["-i", a.muzik] if a.muzik else [])
        if not a.kuru:
            run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", ";".join(g), "-map", "[son]",
                 "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", mix])
            meas = loudnorm_measure(mix, total, target)
        ses_kaynak = mix
    elif a.muzik:
        ses_kaynak = a.muzik
        meas = None if a.kuru else loudnorm_measure(a.muzik, total, target)
    if ses_kaynak:
        inputs += ["-i", ses_kaynak]
        ln = f"loudnorm=I={target}:TP=-1.5:LRA=11"
        if meas:
            ln += (f":measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:measured_LRA={meas['input_lra']}"
                   f":measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
        fades = "" if a.seslendirme else f"afade=t=in:st=0:d=1,afade=t=out:st={max(0, total - 1.5):.3f}:d=1.5,"
        fc.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
                  f"{fades}{ln},aresample=48000[ao]")
        maps += ["-map", "[ao]", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
        idx += 1
    else:
        maps += ["-an"]

    # ---------------- 7. kodlama
    enc_name = a.kodlayici or ("h264_videotoolbox" if a.hizli else "libx264")
    gop = ["-g", str(FPS * 2), "-keyint_min", str(FPS)]
    if enc_name == "libx264":
        enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", str(a.crf), "-profile:v", "high", "-level", "4.2",
               "-x264-params", "aq-mode=3"]
    elif enc_name == "h264_videotoolbox":
        enc = ["-c:v", "h264_videotoolbox", "-b:v", a.bitrate, "-maxrate", "16M", "-bufsize", "24M",
               "-profile:v", "high", "-coder", "cabac", "-spatial_aq", "1"]
    else:
        if a.platform in ("instagram", "tiktok"):
            sys.stderr.write("[UYARI] HEVC Instagram/TikTok'ta ek bir transcode tetikler; H.264 gönder\n")
        enc = ["-c:v", enc_name, "-b:v", a.bitrate, "-tag:v", "hvc1"]
    enc += ["-pix_fmt", "yuv420p", "-r", str(FPS)] + gop + COLOR + ["-t", f"{total:.3f}", "-movflags", "+faststart"]

    cmd = ["ffmpeg", "-y", "-v", "error", "-stats"] + inputs + ["-filter_complex", ";".join(fc)] + maps + enc + [out]
    if a.kuru:
        print(" ".join(shlex.quote(c) for c in cmd)); print(f"# beklenen süre {total:.3f} sn"); return
    run(cmd)

    # ---------------- 8. QC — süreç bittikten sonra ölç
    chk = subprocess.run(["ffmpeg", "-v", "error", "-i", out, "-f", "null", "-"], capture_output=True, text=True)
    inf = probe(out)
    mbps = inf["size"] * 8 / max(inf["dur"], 0.01) / 1e6
    sorun = []
    if chk.stderr.strip(): sorun.append("akış doğrulaması sessiz değil: " + chk.stderr.strip()[:300])
    if abs(inf["dur"] - total) > 0.3: sorun.append(f"süre beklenen {total:.2f}, ölçülen {inf['dur']:.2f}")
    if (inf["w"], inf["h"]) != (W, H): sorun.append(f"ölçü {inf['w']}x{inf['h']} ≠ {W}x{H}")
    if inf["pix"] != "yuv420p": sorun.append(f"pix_fmt {inf['pix']}")
    ct = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                         "stream=color_primaries,color_transfer", "-of", "csv=p=0", out], capture_output=True, text=True).stdout
    if "bt709" not in ct: sorun.append("renk etiketi (bt709) yazılmamış")
    if a.muzik and not inf["audio"]: sorun.append("ses izi yok")
    if inf["dur"] > 60 and a.platform in ("instagram", "youtube"): sorun.append("60 sn üstü")
    rapor = dict(cikti=out, plan_sure=round(total, 3), olculen_sure=round(inf["dur"], 3), boyut_mb=round(inf["size"] / 1e6, 2),
                 mbps=round(mbps, 1), cozunurluk=f"{inf['w']}x{inf['h']}", fps=round(inf["fps"], 2), kodlayici=enc_name,
                 klip_sayisi=n, platform=a.platform, lufs_hedef=target if a.muzik else None,
                 loudnorm_giris=({k: meas[k] for k in ("input_i", "input_tp", "input_lra")} if meas else None),
                 sorunlar=sorun, tamam=not sorun)
    rapor["seslendirme"] = bool(a.seslendirme); rapor["altyazi"] = bool(a.altyazi)
    if a.seslendirme and os.path.exists(out + ".miks.wav"):
        os.remove(out + ".miks.wav")
    with open(out + ".qc.json", "w", encoding="utf-8") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=2)
    print(f"{'✓' if not sorun else '✗'} {out}  {inf['w']}x{inf['h']}  {inf['dur']:.2f} sn  {inf['size']/1e6:.1f} MB  "
          f"{mbps:.1f} Mb/s  {enc_name}  ({a.preset}, {a.platform})")
    for s in sorun:
        print("  [SORUN] " + s)
    print("  Açıklamaya ekle: 'Görseller temsilidir; yapay zekâ desteğiyle hareketlendirilmiştir.'")

if __name__ == "__main__":
    main()
