#!/usr/bin/env python3
"""
render_video.py — build a healing/ambient music video from one still cover
plus a stack of procedural effect layers, then loop it under a full-length
track without re-encoding the video.

Core idea (read this before changing anything):

  1. Effect textures are baked ONCE as still grayscale plates (make_plates.py).
  2. ffmpeg animates those plates with PERIODIC expressions over a short loop
     of L seconds, so frame 0 and frame L are identical -> a perfect loop.
  3. The L-second loop is encoded at high quality, then concatenated N times
     and muxed with the audio using `-c:v copy`.

That is why a 68-minute sleep video costs ~2 minutes of CPU instead of two
hours: only L seconds of video are ever rendered.

Stages (any can be run alone with --stage):
  plan   -> resolve preset + variation, print the effect plan
  plates -> generate the plates this plan needs
  probe  -> 4-frame contact sheet PNG so you can LOOK at it before committing
  loop   -> render the L-second loop.mp4
  mux    -> loop x N + audio -> final deliverable
  all    -> everything (default)

Examples:
  python3 render_video.py --cover cover.png --audio track.flac \
      --preset sufi-incense --out out/nefes.mp4

  python3 render_video.py --cover cover.png --preset forest-mist \
      --stage probe --sheet look.png            # fast visual check

  python3 render_video.py --cover cover.png --audio a.wav --preset cosmic-drift \
      --album-seed 4211 --track 3 --out out/03.mp4   # album-consistent variant
"""
import argparse
import json
import math
import os
import random
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import make_plates  # noqa: E402

PRESET_FILE = os.path.join(SKILL, "assets", "presets.json")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def run(cmd, quiet=False):
    if not quiet:
        print("$ " + " ".join(shlex.quote(c) for c in cmd)[:4000])
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-4000:] + "\n")
        raise SystemExit(f"command failed ({p.returncode})")
    return p.stderr


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True,
    )
    try:
        return float(out.stdout.strip())
    except ValueError:
        raise SystemExit(f"could not read duration of {path}")


def probe_size(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=p=0:s=x", path],
        capture_output=True, text=True,
    )
    try:
        w, h = out.stdout.strip().split("x")[:2]
        return int(w), int(h)
    except Exception:
        raise SystemExit(f"could not read dimensions of {path}")


# Time offset used when rendering a single frame from the middle of the loop.
# Instead of asking ffmpeg to seek (which would render every frame up to that
# point), we shift every oscillator's phase so the wanted moment IS frame 0.
_T0 = 0.0


def sin_expr(amp, cycles, loop, phase=0.0, var="t"):
    """Periodic expression that returns to its exact starting value at t=loop.
    `cycles` MUST be an integer or the loop point will jump."""
    cycles = max(1, int(round(cycles)))
    if abs(amp) < 1e-6:
        return "0"
    phase = phase + 2 * math.pi * cycles * _T0 / loop
    return f"{amp:.4f}*sin(2*PI*{cycles}*{var}/{loop:.4f}+{phase:.4f})"


# How hard to crush each plate's blacks before screen-blending it.
# This is THE difference between "smoke wisps floating over the artwork" and
# "someone poured milk on the artwork": a screen blend lifts every non-black
# pixel, so any mid-gray in the plate becomes global haze and eats the contrast
# and saturation of the cover. Crushing first keeps only the wisps.
CRUSH = {
    "fog": 0.42, "plume": 0.38, "ink": 0.40, "dust": 0.34, "bokeh": 0.12,
    "stars": 0.18, "rays": 0.34, "caustics": 0.28, "warpmap": 0.0, "grain": 0.0,
}

_FREI0R = None


def has_frei0r(name="glow"):
    """frei0r plugins are an optional dependency. ffmpeg here is built with
    --enable-frei0r, but the plugin .so files ship separately, so the filter
    can exist while every plugin is missing. Probe once, cache the answer."""
    global _FREI0R
    if _FREI0R is None:
        r = subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
             "-i", "color=c=black:s=32x32", "-vf",
             f"format=rgb24,frei0r=filter_name={name}:filter_params=0.3",
             "-frames:v", "1", "-f", "null", "-"],
            capture_output=True, text=True)
        _FREI0R = r.returncode == 0
    return _FREI0R


GRADES = {
    # name: (colorbalance args, eq args, curves preset or points)
    "warm-amber":  ("rs=.06:gs=.01:bs=-.06:rm=.05:bm=-.05:rh=.04:bh=-.06", "saturation=1.02:contrast=1.03", None),
    "candle":      ("rs=.10:gs=.02:bs=-.10:rm=.07:bm=-.07:bh=-.04", "saturation=0.96:contrast=1.05:brightness=-0.02", None),
    "cool-teal":   ("rs=-.05:bs=.07:gm=.02:bm=.05:rh=-.03:bh=.04", "saturation=0.94:contrast=1.04", None),
    "moonlit":     ("rs=-.06:bs=.10:bm=.06:rh=-.04:bh=.03", "saturation=0.72:contrast=1.06:brightness=-0.03", None),
    "sepia-dust":  ("rs=.09:gs=.03:bs=-.11:rm=.05:bm=-.08", "saturation=0.55:contrast=1.02", None),
    "monochrome":  ("", "saturation=0.0:contrast=1.08", None),
    "rose-dawn":   ("rs=.09:bs=.02:rm=.05:gm=-.02:bm=.02:rh=.05", "saturation=1.05:contrast=1.01", None),
    "deep-space":  ("rs=-.07:bs=.12:gm=-.02:bm=.07:rh=-.05", "saturation=0.9:contrast=1.09:brightness=-0.04", None),
    "forest":      ("rs=-.05:gs=.06:bs=-.02:gm=.04:bm=.02", "saturation=0.98:contrast=1.04", None),
    "neutral":     ("", "contrast=1.01", None),
}


# --------------------------------------------------------------------------
# preset resolution
# --------------------------------------------------------------------------


def load_presets():
    with open(PRESET_FILE, encoding="utf-8") as f:
        return json.load(f)


def resolve(preset_id, album_seed, track, overrides):
    presets = load_presets()
    if preset_id not in presets:
        raise SystemExit(
            f"unknown preset '{preset_id}'.\nAvailable: {', '.join(sorted(presets))}"
        )
    p = json.loads(json.dumps(presets[preset_id]))  # deep copy
    p["id"] = preset_id

    # --- per-track variation ---------------------------------------------
    # An album should look like one album. So the palette, the layer stack and
    # the grade stay fixed; only seed, phases, speeds and opacities wander
    # inside a small band. Same (album_seed, track) always yields the same look.
    seed = album_seed * 7919 + track * 104729
    p["seed"] = seed
    rng = random.Random(seed)
    if track > 0:
        for lay in p["layers"]:
            lay["phase"] = round(rng.uniform(0, 6.283), 3)
            lay["opacity"] = round(
                min(0.95, max(0.05, lay["opacity"] * rng.uniform(0.82, 1.18))), 3
            )
            if "pan" in lay:
                lay["pan"] = [round(v * rng.uniform(0.8, 1.25), 1) for v in lay["pan"]]
    for k, v in overrides.items():
        if v is not None:
            p[k] = v
    return p


# --------------------------------------------------------------------------
# filter graph
# --------------------------------------------------------------------------


def cheap_blur(sigma, rw, rh, div=4):
    """Just gblur. Measured at 2880x1620: sigma=45 costs ~48 ms/frame while a
    shrink-blur-grow of the same strength costs ~22 ms/frame and looks blocky —
    ffmpeg's gblur is an IIR approximation, so cost is nearly independent of
    sigma. Not worth trading quality for. (frei0r's IIRblur measured 3x SLOWER
    than gblur because of the RGBA round-trip.)"""
    if sigma <= 0:
        return None
    return f"gblur=sigma={sigma:.2f}"


def build_graph(p, cover, plate_paths, loop, fps, W, H, ss, t0=0.0):
    """Return (filter_complex string, input args, label of final video).
    t0 shifts all oscillators so that output frame 0 shows loop time t0."""
    global _T0
    _T0 = t0
    RW, RH = int(W * ss) // 2 * 2, int(H * ss) // 2 * 2  # internal render size
    chains = []
    inputs = ["-loop", "1", "-framerate", str(fps), "-i", cover]
    plate_idx = {}
    for name in p["_plates"]:
        plate_idx[name] = len(plate_idx) + 1
        inputs += ["-loop", "1", "-framerate", str(fps), "-i", plate_paths[name]]

    base = p.get("base", {})
    layout = p.get("layout", "auto")
    cw, ch = probe_size(cover)
    if layout == "auto":
        cover_ar, frame_ar = cw / ch, W / H
        layout = "pillar" if abs(cover_ar - frame_ar) > 0.18 else "fill"

    # ---- 1. base plate: fit the artwork into the frame ------------------
    OS = 1.4  # artwork headroom for zoompan; more than this is wasted pixels
    head = int(RH * OS) // 2 * 2
    wide = int(RW * OS) // 2 * 2
    if layout == "fill":
        chains.append(
            f"[0:v]scale={wide}:{head}:force_original_aspect_ratio=increase,"
            f"crop={wide}:{head},setsar=1,format=gbrp[art]"
        )
    elif layout == "full":  # letterbox, artwork untouched
        chains.append(
            f"[0:v]scale={wide}:{head}:force_original_aspect_ratio=decrease,"
            f"pad={wide}:{head}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,format=gbrp[art]"
        )
    else:  # pillar: blurred blown-up copy behind the intact artwork
        blur = p.get("pillar_blur", 60)
        dim = p.get("pillar_dim", -0.22)
        inset = p.get("pillar_inset", 0.94)
        chains.append(
            f"[0:v]split=2[bgsrc][fgsrc];"
            f"[bgsrc]scale={wide}:{head}:force_original_aspect_ratio=increase,"
            f"crop={wide}:{head},{cheap_blur(blur, wide, head)},"
            f"eq=brightness={dim}:saturation=0.9,setsar=1,format=gbrp[bg];"
            f"[fgsrc]scale=-1:{int(head*inset)}:flags=lanczos,setsar=1,format=gbrp[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2:format=auto,format=gbrp[art]"
        )

    # ---- 2. base motion: breathing zoom + slow drift --------------------
    z0 = 1.0 + base.get("zoom", 0.04)
    za = base.get("zoom", 0.04) * 0.9
    nf = max(1, int(round(loop * fps)))
    zc = max(1, int(base.get("zoom_cycles", 1)))
    dx, dy = base.get("drift", [0, 0])
    on0 = int(round(t0 * fps))
    onv = f"(on+{on0})" if on0 else "on"
    zexpr = f"{z0:.4f}{'+' if za>=0 else '-'}{abs(za):.4f}*sin(2*PI*{zc}*{onv}/{nf})"
    xexpr = f"iw/2-(iw/zoom/2)+{sin_expr(dx,base.get('drift_cycles',1),loop,0.0,'on/'+str(fps))}"
    yexpr = f"ih/2-(ih/zoom/2)+{sin_expr(dy,base.get('drift_cycles',1),loop,1.57,'on/'+str(fps))}"
    chains.append(
        f"[art]zoompan=z='{zexpr}':x='{xexpr}':y='{yexpr}':d=1:s={RW}x{RH}:fps={fps}[cur0]"
    )
    cur = "cur0"

    # ---- 3. optional displace warp of the artwork itself ----------------
    if base.get("warp", 0) > 0 and "warpmap" in plate_idx:
        s = base["warp"]
        mi = plate_idx["warpmap"]
        chains.append(
            f"[{mi}:v]scale={int(RW*1.25)}:{int(RH*1.25)},"
            f"crop={RW}:{RH}:x='(iw-ow)/2+{sin_expr(RW*0.06,1,loop)}':"
            f"y='(ih-oh)/2+{sin_expr(RH*0.06,1,loop,2.1)}',"
            # NOTE: displace forces one pixel format across all three inputs.
            # If the maps are `gray`, ffmpeg silently converts the ARTWORK to
            # gray too and you lose all colour. Keep the maps in rgb24.
            f"format=gbrp,eq=contrast={s:.3f}:brightness=0,split=2[wx][wy]"
        )
        chains.append(f"[{cur}][wx][wy]displace=edge=smear[warped]")
        cur = "warped"

    # ---- 4. effect layers ----------------------------------------------
    for i, lay in enumerate(p["layers"]):
        idx = plate_idx[lay["plate"]]
        sc = lay.get("scale", 1.3)
        lw, lh = int(RW * sc) // 2 * 2, int(RH * sc) // 2 * 2
        px, py = lay.get("pan", [40, 25])
        cyc = lay.get("cycles", 1)
        ph = lay.get("phase", 0.0)
        seg = [f"[{idx}:v]scale={lw}:{lh}:flags=bicubic"]
        seg.append(
            f"crop={RW}:{RH}:x='(iw-ow)/2+{sin_expr(px,cyc,loop,ph)}'"
            f":y='(ih-oh)/2+{sin_expr(py,cyc,loop,ph+1.9)}'"
        )
        if lay.get("rotate", 0):
            seg.append(
                f"rotate=a='{sin_expr(math.radians(lay['rotate']),max(1,cyc),loop,ph+0.7)}'"
                f":c=black@0:bilinear=1"
            )
        if lay.get("blur", 0):
            seg.append(cheap_blur(lay["blur"] * ss, RW, RH))
        crush = lay.get("crush", CRUSH.get(lay["plate"], 0.3))
        if crush > 0:
            seg.append(f"curves=all='0/0 {crush:.3f}/0 1/1'")
        if lay.get("gamma") or lay.get("pulse"):
            # eq is a luma filter. Fed packed RGB it mangles channels (measured:
            # an orange sky came out magenta), so run it in yuv and come back.
            gm = lay.get("gamma", 1.0)
            pulse = lay.get("pulse", 0.0)
            br = sin_expr(pulse, lay.get("pulse_cycles", 1), loop, ph + 0.4) if pulse else "0"
            seg += ["format=yuv420p", f"eq=gamma={gm}:brightness='{br}':eval=frame"]
        seg.append("format=gbrp")
        tint = lay.get("tint")
        if tint:
            r, g, b = tint
            seg.append(f"colorchannelmixer=rr={r}:gg={g}:bb={b}")
        chains.append(",".join(seg) + f"[lay{i}]")
        chains.append(
            f"[{cur}][lay{i}]blend=all_mode={lay.get('blend','screen')}"
            f":all_opacity={lay['opacity']}[mix{i}]"
        )
        cur = f"mix{i}"

    # ---- 5. post: bloom, grade, vignette, downscale, grain -------------
    post = p.get("post", {})
    plugins = p.get("_plugins", True)

    # frei0r `glow` does highlight bloom in a single filter and is temporally
    # rock-steady. It replaces the split/curves/gblur bloom when available.
    if plugins and post.get("glow", 0) > 0 and has_frei0r("glow"):
        chains.append(
            f"[{cur}]format=rgb24,frei0r=filter_name=glow:"
            f"filter_params={post['glow']:.3f},format=gbrp[glowed]")
        cur = "glowed"
    elif post.get("bloom", 0) > 0:
        b = post["bloom"]
        chains.append(
            f"[{cur}]split=2[bk][bl];"
            f"[bl]curves=all='0/0 {post.get('bloom_threshold',0.62)}/0 1/1',"
            f"{cheap_blur(post.get('bloom_radius',34)*ss, RW, RH, div=6)}[blr];"
            f"[bk][blr]blend=all_mode=screen:all_opacity={b}[bloomed]"
        )
        cur = "bloomed"

    grade = GRADES.get(post.get("grade", "neutral"), GRADES["neutral"])
    gseg = []
    if grade[0]:
        gseg.append(f"colorbalance={grade[0]}")  # colorbalance is RGB-native
    gseg.append("format=yuv420p")  # everything below (eq, vignette, noise) is YUV
    if grade[1]:
        gseg.append(f"eq={grade[1]}")
    if post.get("vignette", 0) > 0:
        # Calibrated by measuring corner luminance: PI*0.05 keeps ~90% of the
        # corner, PI*0.20 keeps ~45%. ffmpeg's default (PI/5) is already heavy.
        v = min(1.0, max(0.0, post["vignette"]))
        ang = 0.05 + 0.15 * v
        gseg.append(f"vignette=angle=PI*{ang:.4f}:mode=forward")
    if post.get("chroma", 0):
        # rgbashift is native ffmpeg — no plugin needed. frei0r's rgbsplit0r
        # does the same thing but costs an RGBA round-trip.
        px = max(1, int(round(post["chroma"] * W / 100)))
        gseg.insert(0, f"rgbashift=rh={px}:bh=-{px}")
    if post.get("sharpen", 0):
        gseg.append(f"unsharp=5:5:{post['sharpen']}:5:5:0")
    if ss != 1.0:
        gseg.append(f"scale={W}:{H}:flags=lanczos")
    grain = post.get("grain", 0)
    if grain:
        # luma-only temporal grain. Two jobs: film texture AND dithering the
        # smooth gradients that otherwise band badly on YouTube.
        gseg.append(f"noise=c0s={grain}:c0f=t+u:all_seed={p['seed'] % 30000}")
    chains.append(f"[{cur}]" + ",".join(gseg) + "[vout]")

    return ";".join(chains), inputs, "[vout]"


# --------------------------------------------------------------------------
# stages
# --------------------------------------------------------------------------


def stage_plates(p, work, W, H, ss):
    # Size the plates to the largest layer scale so no plate is ever upscaled
    # (upscaled dust looks like mush).
    mx = min(1.35, max([l.get("scale", 1.3) for l in p["layers"]] + [1.3]))
    pw = int(W * ss * mx) // 2 * 2
    ph = int(H * ss * mx) // 2 * 2
    print(f"[plates] {pw}x{ph} seed={p['seed']}")
    return make_plates.build(p["_plates"], os.path.join(work, "plates"), p["seed"], pw, ph)


def stage_probe(p, cover, plates, loop, fps, W, H, ss, sheet):
    """Render 4 frames spread over the loop and tile them into one PNG.
    Cheap, and it lets a human (or Claude) actually LOOK before the long render."""
    graph, inputs, _ = build_graph(p, cover, plates, loop, fps, W, H, ss)
    tmp = os.path.join(os.path.dirname(sheet) or ".", "_probe")
    os.makedirs(tmp, exist_ok=True)
    marks = [0.02, 0.27, 0.52, 0.77]
    files = []
    for i, m in enumerate(marks):
        fr = max(0, int(m * loop * fps))
        out = os.path.join(tmp, f"f{i}.png")
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
             "-filter_complex", graph, "-map", "[vout]",
             "-vsync", "0", "-frames:v", "1",
             "-ss", f"{fr/fps:.3f}", out], quiet=True)
        files.append(out)
    from PIL import Image
    ims = [Image.open(f) for f in files]
    tw, th = ims[0].width // 2, ims[0].height // 2
    grid = Image.new("RGB", (tw * 2, th * 2))
    for i, im in enumerate(ims):
        grid.paste(im.resize((tw, th)), ((i % 2) * tw, (i // 2) * th))
    grid.save(sheet)
    print(f"[probe] contact sheet -> {sheet}")
    return sheet


def stage_loop(p, cover, plates, loop, fps, W, H, ss, out, crf, preset, seamless, xf):
    graph, inputs, _ = build_graph(p, cover, plates, loop, fps, W, H, ss)
    dur = loop + xf if seamless == "xfade" else loop
    cmd = ["ffmpeg", "-y", "-hide_banner", *inputs,
           "-filter_complex", graph, "-map", "[vout]",
           "-t", f"{dur:.3f}", "-r", str(fps),
           "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
           "-pix_fmt", "yuv420p", "-g", str(fps * 2), "-keyint_min", str(fps),
           "-x264-params", "aq-mode=3:deblock=1,1", "-an",
           "-movflags", "+faststart", out]
    run(cmd)
    if seamless == "xfade":
        out = close_loop_xfade(out, loop, xf, fps, crf, preset)
    print(f"[loop] {out}  ({os.path.getsize(out)/1e6:.1f} MB)")
    return out


def close_loop_xfade(clip, loop, xf, fps, crf, preset):
    """Turn a (loop+xf)-second clip with one-directional motion into a perfect
    loop of exactly `loop` seconds: keep [xf..loop], then crossfade the tail
    [loop..loop+xf] into the head [0..xf]. Start and end then match exactly."""
    out = clip.replace(".mp4", "_seamless.mp4")
    g = (
        f"[0:v]split=3[a][b][c];"
        f"[a]trim=start={xf}:end={loop},setpts=PTS-STARTPTS[mid];"
        f"[b]trim=start={loop}:end={loop+xf},setpts=PTS-STARTPTS[tail];"
        f"[c]trim=start=0:end={xf},setpts=PTS-STARTPTS[head];"
        f"[tail][head]xfade=transition=fade:duration={xf}:offset=0[cf];"
        f"[mid][cf]concat=n=2:v=1:a=0[vout]"
    )
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", clip,
         "-filter_complex", g, "-map", "[vout]", "-r", str(fps),
         "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-g", str(fps * 2), "-an",
         "-movflags", "+faststart", out])
    return out


def stage_mux(loop_clip, audio, out, fade_in, fade_out, loudnorm, work):
    ldur = probe_duration(loop_clip)
    adur = probe_duration(audio)
    n = max(1, math.ceil(adur / ldur) + 1)
    lst = os.path.join(work, "concat.txt")
    ap = os.path.abspath(loop_clip)
    with open(lst, "w") as f:
        f.write("".join(f"file '{ap}'\n" for _ in range(n)))
    af = []
    if loudnorm:
        af.append("loudnorm=I=-14:TP=-1.0:LRA=11")
    if fade_in:
        af.append(f"afade=t=in:st=0:d={fade_in}")
    if fade_out:
        af.append(f"afade=t=out:st={max(0, adur-fade_out):.3f}:d={fade_out}")
    cmd = ["ffmpeg", "-y", "-hide_banner",
           "-f", "concat", "-safe", "0", "-i", lst, "-i", audio,
           "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy"]
    if af:
        cmd += ["-af", ",".join(af)]
    cmd += ["-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-t", f"{adur:.3f}", "-shortest",
            "-movflags", "+faststart", "-fflags", "+genpts", out]
    run(cmd)
    print(f"[mux] {out}  {adur/60:.1f} min  {os.path.getsize(out)/1e6:.1f} MB "
          f"(video looped {n}x from {ldur:.1f}s)")
    return out


# --------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cover", required=True)
    ap.add_argument("--audio")
    ap.add_argument("--preset", required=True)
    ap.add_argument("--out", default="out/video.mp4")
    ap.add_argument("--work", default=None, help="scratch dir (default: <out>/_work)")
    ap.add_argument("--stage", default="all",
                    choices=["plan", "plates", "probe", "loop", "mux", "all"])
    ap.add_argument("--sheet", default=None, help="contact sheet path for --stage probe")
    ap.add_argument("--res", default=None, help="WxH, default from preset")
    ap.add_argument("--fps", type=int, default=None)
    ap.add_argument("--loop", type=float, default=None, help="loop length in seconds")
    ap.add_argument("--ss", type=float, default=None,
                    help="supersample factor; 1.5-2.0 kills pan stepping on slow motion")
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--x264-preset", default="slow")
    ap.add_argument("--seamless", default="oscillate", choices=["oscillate", "xfade"])
    ap.add_argument("--xfade", type=float, default=4.0)
    ap.add_argument("--album-seed", type=int, default=1)
    ap.add_argument("--track", type=int, default=0)
    ap.add_argument("--fade-in", type=float, default=2.0)
    ap.add_argument("--fade-out", type=float, default=6.0)
    ap.add_argument("--loudnorm", action="store_true")
    ap.add_argument("--layers", type=int, default=None,
                    help="use only the first N effect layers (for bisecting a look)")
    ap.add_argument("--no-post", action="store_true",
                    help="skip bloom/grade/vignette/grain")
    ap.add_argument("--plugins", default="auto", choices=["auto", "off"],
                    help="use optional frei0r plugins when present (default auto)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    p = resolve(a.preset, a.album_seed, a.track, {})
    if a.layers is not None:
        p["layers"] = p["layers"][: a.layers]
    if a.no_post:
        p["post"] = {}
    p["_plugins"] = a.plugins == "auto"
    canvas = p.get("canvas", {})
    W, H = (int(v) for v in (a.res or canvas.get("res", "1920x1080")).lower().split("x"))
    fps = a.fps or canvas.get("fps", 30)
    loop = a.loop or p.get("loop", 24)
    ss = a.ss if a.ss is not None else p.get("ss", 1.5)
    p["_plates"] = sorted({l["plate"] for l in p["layers"]} |
                          ({"warpmap"} if p.get("base", {}).get("warp", 0) else set()))

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    work = a.work or os.path.join(os.path.dirname(os.path.abspath(a.out)), "_work")
    os.makedirs(work, exist_ok=True)

    print(f"[plan] preset={p['id']} seed={p['seed']} {W}x{H}@{fps} loop={loop}s ss={ss}")
    print(f"[plan] layers=" + ", ".join(
        f"{l['plate']}({l.get('blend','screen')} {l['opacity']})" for l in p["layers"]))
    print(f"[plan] grade={p.get('post',{}).get('grade','neutral')} "
          f"grain={p.get('post',{}).get('grain',0)} plates={p['_plates']}")
    if a.dry_run:
        graph, inputs, _ = build_graph(p, a.cover, {n: f"<{n}.png>" for n in p["_plates"]},
                                       loop, fps, W, H, ss)
        print("\n--- filter_complex ---\n" + graph.replace(";", ";\n"))
        return
    if a.stage == "plan":
        return

    plates = stage_plates(p, work, W, H, ss)
    if a.stage == "plates":
        return

    if a.stage == "probe":
        stage_probe(p, a.cover, plates, loop, fps, W, H, ss,
                    a.sheet or os.path.join(work, "probe.png"))
        return

    clip = os.path.join(work, "loop.mp4")
    clip = stage_loop(p, a.cover, plates, loop, fps, W, H, ss, clip,
                      a.crf, a.x264_preset, a.seamless, a.xfade)
    if a.stage == "loop":
        return

    if not a.audio:
        raise SystemExit("--audio is required to mux the final video")
    stage_mux(clip, a.audio, a.out, a.fade_in, a.fade_out, a.loudnorm, work)


if __name__ == "__main__":
    main()
