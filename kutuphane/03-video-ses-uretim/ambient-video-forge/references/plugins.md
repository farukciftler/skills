# Optional plugins: install, verdict, limits

Everything in this skill runs on ffmpeg's built-in filters. This file covers the
two optional packages, what they measurably add, and — more usefully — which of
their filters are *not* worth using, so you don't spend an afternoon rediscovering
that.

All timings below were measured on one CPU core with ffmpeg 6.1.1.

## Install

```bash
# Debian / Ubuntu (also what the ffmpeg in most Docker images expects)
sudo apt-get update && sudo apt-get install -y frei0r-plugins gmic

# Alpine
apk add frei0r-plugins gmic

# Fedora / RHEL
sudo dnf install -y frei0r-plugins gmic

# macOS
brew install frei0r gmic
```

Plugins land in `/usr/lib/frei0r-1/*.so` (136 files on Ubuntu 24.04). Verify with
`bash scripts/check_env.sh`.

**The one confusing failure mode:** ffmpeg is usually built with
`--enable-frei0r`, so `ffmpeg -filters | grep frei0r` shows the filter *even when
no plugins are installed*. The filter then fails at runtime with "frei0r filter
not found". `has_frei0r()` in `render_video.py` probes by actually running a
tiny render, which is the only reliable test.

If installing is not an option (locked-down host, minimal container), nothing
breaks: `--plugins off` or a missing plugin dir falls back to built-in paths.

## Hard limitation: frei0r parameters cannot be animated

ffmpeg's `frei0r` wrapper declares no `process_command`, so there is no
`sendcmd`, no per-frame expressions, no `eval=frame`. Confirmed by inspection
(`ffmpeg -h filter=frei0r` lists no commands).

Consequences:

- Any frei0r filter is **one fixed parameter set for the whole render**.
- Motion from frei0r can only come from plugins that animate on their own
  internal clock (`distort0r` with velocity, `vertigo`, `baltan`, `nervous`,
  `ising0r`, `plasma`, `partik0l`, `lissajous0r`).
- Those self-animating plugins are **not seamless-loop safe** — their phase does
  not return to its start at frame L. Pair them with `--seamless xfade`, which
  renders L+X seconds and crossfades the tail into the head.
- Therefore all the *loopable* motion in this skill stays on native filters
  (`crop`/`rotate`/`zoompan`/`eq` with `t`-based expressions).

## Worth using

| filter | what it gives | cost / note |
|---|---|---|
| `glow` | highlight bloom in one filter, temporally rock-steady | ~single-filter cost, replaces a split+curves+gblur+blend subgraph. Wired as `post.glow`. |
| `vignette` | softer falloff with `clearcenter`/`soft` control | nicer than the built-in on faces/centre-weighted art |
| `distort0r` | self-animating sine wave distortion (amplitude, frequency, velocity) | real heat-haze/liquid motion without displace maps — but needs `--seamless xfade` |
| `cartoon`, `colorhalftone`, `dither`, `scanline0r`, `pixeliz0r`, `posterize` | print/retro/lo-fi stylisation | for lo-fi, chiptune, VHS looks; static params are fine here |
| `sopsat`, `three_point_balance`, `curves`, `levels`, `colorize`, `balanc0r`, `primaries` | grading toolbox | use when `colorbalance`+`eq` can't reach a look |
| `alphagrad`, `alphaspot`, `mask0mate` | generated gradient/spot masks | for localising an effect to one region (rays only top-left, etc.) |
| `rgbsplit0r` | chromatic aberration | prefer native `rgbashift` — same result, no RGBA round-trip |
| `sobel`, `edgeglow` | edge outlines / edge glow | niche; good on line-art or calligraphic covers |
| `defish0r`, `lenscorrection`, `c0rners`, `perspective`, `elastic_scale`, `scale0tilt` | lens/geometry | static only, so use for one-off framing fixes, not motion |
| `partik0l` | an actual particle system source | many parameters, undocumented; needs an exploration session before it beats the `dust` plate |
| `plasma`, `ising0r`, `lissajous0r` | generative animated sources | `plasma` is garish raw — only usable heavily blurred and desaturated |

## Measured as *not* worth using

- **`IIRblur`** — 138 ms/frame at 2880×1620 versus `gblur=sigma=45` at ~48 ms.
  The RGBA round-trip costs more than the blur saves. Use `gblur`.
- **`softglow`** — with default-ish parameters it milks the whole frame; the
  contrast loss is exactly the failure mode trap 1 in SKILL.md warns about.
  `glow` plus a `curves` threshold is more controllable.
- **`vertigo` / `baltan` / `delay0r` / `lightgraffiti`** — accumulating temporal
  trails. Dreamy in theory; in practice they wash the frame toward gray and
  never return to their starting state, so they fight the whole loop
  architecture. Skip unless the deliverable is a one-pass non-looping video.
- **`glitch0r`, `nervous`, `tehroxx0r`** — wrong genre. Fine for a glitch/IDM
  cover, actively harmful for healing content where any jump wakes the viewer.

## G'MIC

`gmic` is a large image-processing language, useful in principle for baking
plates offline (it never touches the ffmpeg graph). Verdict after testing:

- `gmic W,H turbulence <scale>,<octaves>,<gain> normalize 0,255 -o plate.png`
  runs fast (165 ms at 800×450) but at every scale tried it produced
  high-frequency static rather than the large soft cloud structures healing
  visuals need. The numpy fBm + domain-warp in `make_plates.py` produced
  visibly better smoke.
- `plasma` gives a usable soft cloud field, roughly equivalent to the `fog`
  plate — no reason to switch.
- Where gmic probably *does* earn its place, and where an exploration session
  would pay off: `water`, `deform`, `wind`, `blur_bloom`, `light_patch`,
  `stylize`, and its inpainting/upscaling commands for repairing a low-resolution
  cover before it goes into the pipeline.

So: install it if you want the option, but do not make any preset depend on it.

## Adding a plugin effect to a preset

Wire it as an optional post step so the preset still renders without the plugin:

```python
if plugins and post.get("glow", 0) > 0 and has_frei0r("glow"):
    chains.append(f"[{cur}]format=rgb24,frei0r=filter_name=glow:"
                  f"filter_params={post['glow']:.3f},format=gbrp[glowed]")
    cur = "glowed"
elif post.get("bloom", 0) > 0:
    ...built-in fallback...
```

Two details that will bite otherwise: frei0r wants **packed RGB** (`format=rgb24`
in, `format=gbrp` out to rejoin the rest of the graph), and boolean parameters
are passed as `y`/`n` while enums are numbers — a bool given as `0` fails with
"Invalid value '0' for parameter 'Edge'". Parameter *order* is positional and
undocumented in ffmpeg; discover it by passing values and reading which
parameter name the error blames.
