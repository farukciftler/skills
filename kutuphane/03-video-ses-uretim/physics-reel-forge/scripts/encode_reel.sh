#!/usr/bin/env bash
# encode_reel.sh — transcode captures to platform-ready 9:16 video, and check them.
#
#   ./encode_reel.sh take.avi                       # master (libx264, ships)
#   ./encode_reel.sh take.avi --preview             # fast VideoToolbox preview
#   ./encode_reel.sh frames/frame_%05d.png --wav audio.wav
#   ./encode_reel.sh take.avi --blur 4              # accumulation motion blur
#   ./encode_reel.sh clip.mp4 --loop-check          # concat to itself, inspect seam
#   ./encode_reel.sh clip.mp4 --safezone            # overlay Instagram UI zones
#   ./encode_reel.sh clip.mp4 --verify              # report actual specs

set -euo pipefail

INPUT=""; OUT=""; WAV=""
MODE="master"; FPS=30; SRC_FPS=""; BLUR=0
W=1080; H=1920

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --preview)    MODE="preview" ;;
    --loop-check) MODE="loopcheck" ;;
    --safezone)   MODE="safezone" ;;
    --verify)     MODE="verify" ;;
    --wav)        WAV="${2:?--wav needs a path}"; shift ;;
    --fps)        FPS="${2:?--fps needs a number}"; shift ;;
    --src-fps)    SRC_FPS="${2:?--src-fps needs a number}"; shift ;;
    --blur)       BLUR="${2:?--blur needs a frame count}"; shift ;;
    --size)       W="${2%%x*}"; H="${2##*x}"; shift ;;
    -o|--out)     OUT="${2:?--out needs a path}"; shift ;;
    -h|--help)    usage 0 ;;
    -*)           echo "unknown option: $1" >&2; usage 1 ;;
    *)            INPUT="$1" ;;
  esac
  shift
done

[[ -n "$INPUT" ]] || usage 1
command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found (brew install ffmpeg)" >&2; exit 1; }

# A %0Nd pattern is a sequence, not a file that exists on disk.
IS_SEQ=0
[[ "$INPUT" == *%0*d* ]] && IS_SEQ=1
if [[ "$IS_SEQ" -eq 0 && ! -f "$INPUT" ]]; then
  echo "input not found: $INPUT" >&2; exit 1
fi

BASE="$(basename "${INPUT%.*}")"
DIR="$(dirname "$INPUT")"

# ------------------------------------------------------------ inspection modes

if [[ "$MODE" == "verify" ]]; then
  command -v ffprobe >/dev/null 2>&1 || { echo "ffprobe not found" >&2; exit 1; }
  echo "--- $INPUT"
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,r_frame_rate,pix_fmt,nb_frames,codec_name,profile \
    -of default=noprint_wrappers=1 "$INPUT"
  ffprobe -v error -select_streams a:0 \
    -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 \
    "$INPUT" 2>/dev/null || echo "audio: none  <- silent physics clips underperform badly"
  DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT" || echo 0)"
  printf 'duration=%.2f s\n' "$DUR"

  read -r VW VH < <(ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height -of csv=p=0 "$INPUT" | tr ',' ' ')
  echo
  if [[ "$VW" == "1080" && "$VH" == "1920" ]]; then
    echo "✓ 1080x1920 — correct for Reels / Shorts / TikTok"
  else
    echo "! ${VW}x${VH} — expected 1080x1920. Check the SubViewport size and Retina scaling."
  fi
  awk -v d="$DUR" 'BEGIN{
    if (d < 5)       print "! under 5 s — usually too short to establish the mechanism";
    else if (d > 30) print "! over 30 s — this genre performs best at 7-25 s";
    else             print "✓ duration in the productive range";
  }'
  exit 0
fi

if [[ "$MODE" == "loopcheck" ]]; then
  LIST="$(mktemp)"; trap 'rm -f "$LIST"' EXIT
  ABS="$(cd "$DIR" && pwd)/$(basename "$INPUT")"
  printf "file '%s'\nfile '%s'\n" "$ABS" "$ABS" > "$LIST"
  OUT="${OUT:-$DIR/${BASE}_loopcheck.mp4}"
  ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "$LIST" -c copy "$OUT"
  echo "→ $OUT"
  echo "Watch the midpoint seam. A visible jump means the loop does not close — either"
  echo "match the end state to frame one, or switch to a clean resolution ending."
  echo "Do not fix it with a crossfade; that reads as an editing artefact."
  exit 0
fi

if [[ "$MODE" == "safezone" ]]; then
  OUT="${OUT:-$DIR/${BASE}_safezone.mp4}"
  TOP=$(( H * 250 / 1920 )); BOT=$(( H * 400 / 1920 )); BOTY=$(( H - BOT ))
  ffmpeg -hide_banner -loglevel error -y -i "$INPUT" -vf "
    drawbox=x=0:y=0:w=iw:h=${TOP}:color=red@0.35:t=fill,
    drawbox=x=0:y=${BOTY}:w=iw:h=${BOT}:color=red@0.35:t=fill
  " -c:v h264_videotoolbox -b:v 5M -pix_fmt yuv420p -an "$OUT" 2>/dev/null \
    || ffmpeg -hide_banner -loglevel error -y -i "$INPUT" -vf "
    drawbox=x=0:y=0:w=iw:h=${TOP}:color=red@0.35:t=fill,
    drawbox=x=0:y=${BOTY}:w=iw:h=${BOT}:color=red@0.35:t=fill
  " -c:v libx264 -crf 26 -preset ultrafast -pix_fmt yuv420p -an "$OUT"
  echo "→ $OUT   (throwaway — never publish this file)"
  echo "Anything important under red will sit beneath Instagram's UI overlays."
  exit 0
fi

# ------------------------------------------------------------ encode modes

OUT="${OUT:-$DIR/${BASE}_${MODE}.mp4}"

VF="scale=${W}:${H}:flags=lanczos"
if [[ "$BLUR" -gt 1 ]]; then
  WEIGHTS="$(printf '1 %.0s' $(seq 1 "$BLUR"))"
  VF="tmix=frames=${BLUR}:weights='${WEIGHTS# }',fps=${FPS},${VF}"
  echo "accumulation motion blur: blending ${BLUR} frames down to ${FPS} fps"
  echo "(source must have been captured at ${BLUR}x${FPS} fps for this to be correct)"
fi

INPUT_ARGS=()
if [[ "$IS_SEQ" -eq 1 ]]; then
  INPUT_ARGS+=(-framerate "${SRC_FPS:-60}" -i "$INPUT")
else
  INPUT_ARGS+=(-i "$INPUT")
fi
[[ -n "$WAV" ]] && INPUT_ARGS+=(-i "$WAV")

if [[ "$MODE" == "preview" ]]; then
  CODEC=(-c:v h264_videotoolbox -b:v 6M)
  ABR="128k"
else
  # libx264 for anything that ships: Instagram re-encodes on ingest, and
  # VideoToolbox needs ~1.5-2x the bitrate to match this perceptual quality.
  CODEC=(-c:v libx264 -crf 17 -preset veryfast -profile:v high -level 4.2
         -colorspace bt709 -color_primaries bt709 -color_trc bt709)
  ABR="192k"
fi

set +e
ffmpeg -hide_banner -loglevel error -y "${INPUT_ARGS[@]}" \
  "${CODEC[@]}" \
  -vf "$VF" -r "$FPS" -pix_fmt yuv420p \
  -c:a aac -b:a "$ABR" -ar 48000 -ac 2 \
  -movflags +faststart -shortest \
  "$OUT"
RC=$?
set -e

if [[ "$RC" -ne 0 ]]; then
  echo "encode failed (exit $RC)." >&2
  if [[ "$MODE" == "preview" ]]; then
    echo "VideoToolbox is picky about dimensions and rejects -crf outright." >&2
    echo "Retry without --preview to use libx264." >&2
  fi
  exit "$RC"
fi

SIZE_MB="$(awk -v b="$(wc -c <"$OUT")" 'BEGIN{printf "%.1f", b/1e6}')"
echo "→ $OUT (${SIZE_MB} MB)"

if [[ "$MODE" == "master" ]]; then
  echo
  echo "Before publishing:"
  echo "  $0 $OUT --verify       # confirm dimensions, fps, audio present"
  echo "  $0 $OUT --safezone     # confirm the payoff clears Instagram's UI"
  echo "  $0 $OUT --loop-check   # confirm the loop seam, if it loops"
fi
