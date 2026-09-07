#!/usr/bin/env bash
# preflight.sh — verify the toolchain before building anything.
# Usage: ./preflight.sh [/path/to/Godot/binary]

set -uo pipefail

GODOT_BIN="${1:-/Applications/Godot.app/Contents/MacOS/Godot}"
FAIL=0
WARN=0

green() { printf "  \033[32m✓\033[0m %s\n" "$1"; }
red()   { printf "  \033[31m✗\033[0m %s\n" "$1"; FAIL=$((FAIL+1)); }
yell()  { printf "  \033[33m!\033[0m %s\n" "$1"; WARN=$((WARN+1)); }
head_() { printf "\n\033[1m%s\033[0m\n" "$1"; }

head_ "Hardware"

ARCH="$(uname -m)"
if [[ "$ARCH" == "arm64" ]]; then
  CHIP="$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo 'Apple Silicon')"
  green "Apple Silicon: $CHIP"
  PCORES="$(sysctl -n hw.perflevel0.physicalcpu 2>/dev/null || echo '?')"
  ECORES="$(sysctl -n hw.perflevel1.physicalcpu 2>/dev/null || echo '0')"
  MEM_GB=$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1073741824 ))
  green "Cores: ${PCORES} performance + ${ECORES} efficiency   Memory: ${MEM_GB} GB"
  [[ "$MEM_GB" -lt 16 ]] && yell "Under 16 GB — skip the RAM disk for frame caching, and keep body counts modest."
else
  yell "Not Apple Silicon (arch=$ARCH). Metal backend and VideoToolbox behaviour will differ from this skill's assumptions."
fi

if command -v pmset >/dev/null 2>&1; then
  if pmset -g | grep -qE 'lowpowermode[[:space:]]+1'; then
    yell "Low Power Mode is ON — this throttles the GPU. Turn it off before a batch."
  else
    green "Low Power Mode off"
  fi
fi

head_ "Godot"

if [[ -x "$GODOT_BIN" ]]; then
  VER="$("$GODOT_BIN" --version 2>/dev/null | head -1)"
  green "Binary: $GODOT_BIN"
  green "Version: $VER"

  MAJOR="$(printf '%s' "$VER" | sed -n 's/^\([0-9]*\)\..*/\1/p')"
  MINOR="$(printf '%s' "$VER" | sed -n 's/^[0-9]*\.\([0-9]*\).*/\1/p')"
  MAJOR="${MAJOR:-0}"; MINOR="${MINOR:-0}"

  if [[ "$MAJOR" -ge 5 ]] || { [[ "$MAJOR" -eq 4 ]] && [[ "$MINOR" -ge 6 ]]; }; then
    green "Jolt is the default 3D physics engine at this version."
  elif [[ "$MAJOR" -eq 4 ]] && [[ "$MINOR" -ge 4 ]]; then
    yell "Jolt ships in-engine but is NOT default. Set physics/3d/physics_engine = \"Jolt Physics\" in project settings."
  else
    red "Godot < 4.4 — no in-engine Jolt. Upgrade to 4.6+, or install the godot-jolt GDExtension."
  fi

  case "$VER" in
    *mono*|*dotnet*) yell "This is the .NET build. The standard build iterates faster unless C# is required." ;;
  esac
else
  red "Godot not found at: $GODOT_BIN"
  red "Download from godotengine.org, or pass the binary path as the first argument."
fi

head_ "ffmpeg"

if command -v ffmpeg >/dev/null 2>&1; then
  green "ffmpeg: $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f1-3)"
  ENCODERS="$(ffmpeg -hide_banner -encoders 2>/dev/null)"

  if printf '%s' "$ENCODERS" | grep -q 'h264_videotoolbox'; then
    green "h264_videotoolbox present — hardware preview encoding available"
  else
    red "h264_videotoolbox MISSING. Install via Homebrew (brew install ffmpeg) — that build enables VideoToolbox."
  fi

  if printf '%s' "$ENCODERS" | grep -q 'libx264'; then
    green "libx264 present — master encoding available"
  else
    red "libx264 MISSING. Masters cannot be encoded at shipping quality without it."
  fi

  printf '%s' "$ENCODERS" | grep -q 'hevc_videotoolbox' \
    && green "hevc_videotoolbox present (do NOT use for Instagram — forces an extra transcode)"

  if command -v ffprobe >/dev/null 2>&1; then
    green "ffprobe present — output verification available"
  else
    yell "ffprobe missing. Verifying actual output dimensions becomes manual."
  fi
else
  red "ffmpeg not found. Install with: brew install ffmpeg"
fi

head_ "Live encoder test"

if command -v ffmpeg >/dev/null 2>&1; then
  TMP="$(mktemp -d)"
  if ffmpeg -hide_banner -loglevel error -y \
      -f lavfi -i "testsrc=size=1080x1920:rate=30:duration=1" \
      -c:v h264_videotoolbox -b:v 8M -pix_fmt yuv420p \
      "$TMP/vt.mp4" 2>"$TMP/vt.err"; then
    green "VideoToolbox encoded a 1080x1920 test clip successfully"
  else
    red "VideoToolbox failed on 1080x1920. Error:"
    sed 's/^/      /' "$TMP/vt.err" | head -5
  fi
  rm -rf "$TMP"
fi

head_ "Optional tools"

command -v caffeinate >/dev/null 2>&1 \
  && green "caffeinate present — wrap batches to stop display sleep interrupting capture" \
  || yell "caffeinate missing (unexpected on macOS)"

command -v python3 >/dev/null 2>&1 \
  && green "python3: $(python3 --version 2>&1)" \
  || red "python3 missing — batch_render.py will not run"

head_ "Result"
if [[ "$FAIL" -gt 0 ]]; then
  printf "  \033[31m%d blocking issue(s)\033[0m, %d warning(s). Fix the blockers before building a project.\n\n" "$FAIL" "$WARN"
  exit 1
fi
printf "  \033[32mReady.\033[0m %d warning(s).\n" "$WARN"
printf "  Next: read references/godot-pipeline.md before creating the project.\n\n"
