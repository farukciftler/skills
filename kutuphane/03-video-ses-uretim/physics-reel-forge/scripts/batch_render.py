#!/usr/bin/env python3
"""
batch_render.py — render a recipe across many seeds, transcode, record metadata.

The workflow this supports: most simulation rolls are boring and you cannot tell
which will be good from the parameters. So render many cheap variants, watch them,
then re-render the winners at full quality. Every variant gets a JSON sidecar
recording its seed and parameters so any roll can be reproduced exactly.

Usage:
    ./batch_render.py recipe.json                       # sweep per recipe
    ./batch_render.py recipe.json --seeds 1,2,3         # explicit seeds
    ./batch_render.py recipe.json --seeds 100-130       # seed range
    ./batch_render.py recipe.json --final --seeds 117   # full-res master
    ./batch_render.py recipe.json --dry-run

Recipe JSON:
{
  "name": "chain-drop",
  "project": "/Users/me/reels/physics-project",
  "scene": "res://scenes/chain_drop.tscn",
  "seeds": [1, 2, 3, 4, 5],
  "duration_s": 15,
  "fps": 60,
  "preview_resolution": "540x960",
  "final_resolution": "1080x1920",
  "params": { "link_count": 24, "link_mass": 0.4, "velocity_iters": 20 }
}

Params are passed to Godot as REEL_PARAM_<UPPERCASE_KEY> environment variables,
plus REEL_PARAMS_JSON holding the whole block. Read them in _ready() so a scene
can be swept without editing scene files.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_GODOT = "/Applications/Godot.app/Contents/MacOS/Godot"


# ---------------------------------------------------------------- helpers

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_seeds(spec):
    """Accept '1,2,3', '100-130', or a mix of both."""
    seeds = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk.lstrip("-"):
            lo, _, hi = chunk.partition("-")
            try:
                lo_i, hi_i = int(lo), int(hi)
            except ValueError:
                die(f"bad seed range: {chunk!r}")
            if hi_i < lo_i:
                die(f"seed range reversed: {chunk!r}")
            seeds.extend(range(lo_i, hi_i + 1))
        else:
            try:
                seeds.append(int(chunk))
            except ValueError:
                die(f"bad seed: {chunk!r}")
    return seeds


def which_or_die(name, hint):
    path = shutil.which(name)
    if not path:
        die(f"{name} not found on PATH. {hint}")
    return path


def probe(ffprobe, path):
    """Return actual dimensions/fps/frames of a produced file, or None."""
    try:
        out = subprocess.run(
            [ffprobe, "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
             "-of", "json", str(path)],
            capture_output=True, text=True, timeout=60, check=True,
        ).stdout
        streams = json.loads(out).get("streams") or []
        return streams[0] if streams else None
    except (subprocess.SubprocessError, json.JSONDecodeError, IndexError):
        return None


# ---------------------------------------------------------------- stages

def render_take(godot, recipe, seed, resolution, frames, raw_path, dry_run,
                events_path=None):
    """Run Godot in non-real-time capture mode. Returns elapsed seconds."""
    cmd = [
        godot,
        "--path", recipe["project"],
        "--write-movie", str(raw_path),
        "--fixed-fps", str(recipe.get("fps", 60)),
        "--resolution", resolution,
        "--quit-after", str(frames),
    ]
    if recipe.get("scene"):
        cmd.append(recipe["scene"])
    if recipe.get("rendering_driver"):
        cmd += ["--rendering-driver", recipe["rendering_driver"]]

    env = os.environ.copy()
    env["REEL_SEED"] = str(seed)
    env["REEL_PARAMS_JSON"] = json.dumps(recipe.get("params", {}))
    if events_path:
        # contact_log.gd writes the collision log here; synth_impacts.py reads it.
        env["REEL_EVENTS_PATH"] = str(events_path)
    for key, value in recipe.get("params", {}).items():
        env[f"REEL_PARAM_{key.upper()}"] = str(value)

    if dry_run:
        print("    would run:", " ".join(cmd))
        return 0.0

    start = time.monotonic()
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
    elapsed = time.monotonic() - start

    # Godot's exit code is unreliable with --quit-after; trust the artefact.
    if not raw_path.exists() or raw_path.stat().st_size < 10_000:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-8:]
        print("    render produced no usable output:", file=sys.stderr)
        for line in tail:
            print(f"      {line}", file=sys.stderr)
        print("    (--write-movie needs a rendering context: a window must open, "
              "and --headless will not work)", file=sys.stderr)
        return None
    return elapsed


def transcode(ffmpeg, raw_path, out_path, resolution, fps, final, dry_run):
    """VideoToolbox for previews, libx264 for masters."""
    width, _, height = resolution.partition("x")
    vf = f"scale={width}:{height}:flags=lanczos"

    if final:
        codec = ["-c:v", "libx264", "-crf", "17", "-preset", "veryfast",
                 "-profile:v", "high", "-level", "4.2",
                 "-colorspace", "bt709", "-color_primaries", "bt709",
                 "-color_trc", "bt709"]
    else:
        codec = ["-c:v", "h264_videotoolbox", "-b:v", "6M"]

    cmd = ([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw_path)]
           + codec
           + ["-vf", vf, "-r", str(fps), "-pix_fmt", "yuv420p",
              "-c:a", "aac", "-b:a", "192k" if final else "128k", "-ar", "48000",
              "-movflags", "+faststart", str(out_path)])

    if dry_run:
        print("    would run:", " ".join(cmd))
        return True

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"    transcode failed: {proc.stderr.strip()[:400]}", file=sys.stderr)
        return False
    return True


def synth_and_mux(ffmpeg, events_path, video_path, out_path, modes, dry_run):
    """Render audio from the collision log and mux it onto the silent video.

    Kept separate from the video render on purpose: audio can be re-rendered in
    seconds this way, without re-capturing a single frame.
    """
    if not events_path.exists():
        print(f"    no event log at {events_path} — is contact_log.gd installed as "
              f"an autoload, and does the scene call ContactLog.track()?")
        return False

    synth = Path(__file__).resolve().parent / "synth_impacts.py"
    wav = events_path.with_suffix(".wav")
    synth_cmd = [sys.executable, str(synth), str(events_path), "-o", str(wav),
                 "--modes", str(modes)]
    mux_cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
               "-i", str(video_path), "-i", str(wav),
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
               "-shortest", "-movflags", "+faststart", str(out_path)]

    if dry_run:
        print("    would run:", " ".join(synth_cmd))
        print("    would run:", " ".join(mux_cmd))
        return True

    proc = subprocess.run(synth_cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"    audio synthesis failed: {proc.stderr.strip()[:400]}",
              file=sys.stderr)
        return False
    proc = subprocess.run(mux_cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"    mux failed: {proc.stderr.strip()[:400]}", file=sys.stderr)
        return False
    return True


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Batch-render physics reel variants.")
    ap.add_argument("recipe", type=Path)
    ap.add_argument("--seeds", help="e.g. 1,2,3 or 100-130 (overrides recipe)")
    ap.add_argument("--final", action="store_true",
                    help="full resolution + libx264 master quality")
    ap.add_argument("--out", type=Path, help="output directory")
    ap.add_argument("--godot", default=os.environ.get("GODOT_BIN", DEFAULT_GODOT))
    ap.add_argument("--keep-raw", action="store_true",
                    help="keep MJPEG intermediates (they are huge)")
    ap.add_argument("--audio", action="store_true",
                    help="synthesise impact audio from the collision log and mux "
                         "it in (requires contact_log.gd in the project)")
    ap.add_argument("--audio-modes", type=int, default=32,
                    help="modes per impact; 48+ for metal, glass, porcelain")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="re-render variants that already exist")
    args = ap.parse_args()

    if not args.recipe.is_file():
        die(f"recipe not found: {args.recipe}")
    try:
        recipe = json.loads(args.recipe.read_text())
    except json.JSONDecodeError as exc:
        die(f"recipe is not valid JSON: {exc}")

    for key in ("name", "project"):
        if not recipe.get(key):
            die(f"recipe is missing required key: {key!r}")
    if not Path(recipe["project"]).is_dir():
        die(f"project directory does not exist: {recipe['project']}")

    if not args.dry_run and not Path(args.godot).exists():
        die(f"Godot not found at {args.godot} — pass --godot or set GODOT_BIN")
    ffmpeg = which_or_die("ffmpeg", "Install with: brew install ffmpeg") if not args.dry_run else "ffmpeg"
    ffprobe = shutil.which("ffprobe")

    seeds = parse_seeds(args.seeds) if args.seeds else recipe.get("seeds") or [1]
    fps = int(recipe.get("fps", 60))
    duration = float(recipe.get("duration_s", 15))
    frames = int(round(duration * fps))
    resolution = (recipe.get("final_resolution", "1080x1920") if args.final
                  else recipe.get("preview_resolution", "540x960"))
    stage = "final" if args.final else "preview"

    out_dir = args.out or Path.cwd() / "takes" / recipe["name"] / stage
    raw_dir = out_dir / "_raw"
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nrecipe    {recipe['name']}  [{stage}]")
    print(f"seeds     {len(seeds)}  ({seeds[0]}..{seeds[-1]})")
    print(f"output    {resolution} @ {fps}fps, {duration}s = {frames} frames")
    print(f"dest      {out_dir}\n")

    results, t0 = [], time.monotonic()

    for i, seed in enumerate(seeds, 1):
        stem = f"{recipe['name']}_{stage}_s{seed:05d}"
        out_path = out_dir / f"{stem}.mp4"
        raw_path = raw_dir / f"{stem}.avi"

        if out_path.exists() and not args.force and not args.dry_run:
            print(f"[{i}/{len(seeds)}] seed {seed}: exists, skipping (--force to redo)")
            continue

        events_path = out_dir / f"{stem}.events.json" if args.audio else None

        print(f"[{i}/{len(seeds)}] seed {seed}: rendering...", flush=True)
        elapsed = render_take(args.godot, recipe, seed, resolution,
                              frames, raw_path, args.dry_run, events_path)
        if elapsed is None:
            results.append({"seed": seed, "ok": False, "stage_failed": "render"})
            continue

        print(f"              transcoding ({'x264' if args.final else 'videotoolbox'})...",
              flush=True)
        if not transcode(ffmpeg, raw_path, out_path, resolution, fps,
                         args.final, args.dry_run):
            results.append({"seed": seed, "ok": False, "stage_failed": "transcode"})
            continue

        if args.audio:
            print("              synthesising audio...", flush=True)
            silent = out_path.with_name(out_path.stem + "_silent.mp4")
            if not args.dry_run:
                out_path.replace(silent)
            if synth_and_mux(ffmpeg, events_path, silent, out_path,
                             args.audio_modes, args.dry_run):
                if not args.dry_run:
                    silent.unlink(missing_ok=True)
            elif not args.dry_run and silent.exists():
                silent.replace(out_path)      # keep the silent video rather than nothing

        if args.dry_run:
            results.append({"seed": seed, "ok": True})
            continue

        actual = probe(ffprobe, out_path) if ffprobe else None
        if actual:
            got = f"{actual.get('width')}x{actual.get('height')}"
            if got != resolution:
                print(f"              WARNING: produced {got}, expected {resolution}. "
                      f"Check the SubViewport size and Retina scale factor.")

        # Sidecar: everything needed to reproduce this exact take.
        sidecar = {
            "recipe": recipe["name"],
            "seed": seed,
            "stage": stage,
            "rendered_at": datetime.now(timezone.utc).isoformat(),
            "requested_resolution": resolution,
            "actual_stream": actual,
            "fps": fps,
            "duration_s": duration,
            "frames": frames,
            "params": recipe.get("params", {}),
            "render_seconds": round(elapsed, 1),
            "godot": args.godot,
            "scene": recipe.get("scene"),
            "audio": {"synthesised": bool(args.audio),
                      "modes": args.audio_modes if args.audio else None},
        }
        out_path.with_suffix(".json").write_text(json.dumps(sidecar, indent=2))

        if not args.keep_raw:
            raw_path.unlink(missing_ok=True)

        size_mb = out_path.stat().st_size / 1e6
        print(f"              done in {elapsed:.0f}s → {out_path.name} ({size_mb:.1f} MB)")
        results.append({"seed": seed, "ok": True, "render_seconds": round(elapsed, 1)})

    if not args.keep_raw and not args.dry_run and raw_dir.exists():
        try:
            raw_dir.rmdir()
        except OSError:
            pass

    ok = [r for r in results if r.get("ok")]
    bad = [r for r in results if not r.get("ok")]
    total = time.monotonic() - t0

    print(f"\n{len(ok)} rendered, {len(bad)} failed, {total/60:.1f} min total")
    if ok:
        times = [r["render_seconds"] for r in ok if "render_seconds" in r]
        if times:
            print(f"mean {sum(times)/len(times):.0f}s per variant "
                  f"— use this number for planning, not an estimate")
    for r in bad:
        print(f"  FAILED seed {r['seed']} at {r['stage_failed']}")

    if ok and not args.final and not args.dry_run:
        print(f"\nNext: watch {out_dir}, pick the winners, then re-render at full "
              f"resolution:\n  {sys.argv[0]} {args.recipe} --final --seeds <winners>")

    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\ninterrupted — completed variants are kept; re-run to resume", file=sys.stderr)
        sys.exit(130)
    except BrokenPipeError:
        os._exit(0)  # output was piped into something that closed early (e.g. head)
