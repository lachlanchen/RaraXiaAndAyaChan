#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/video_blurfill.sh INPUT OUTPUT [options]

Creates a vertical 9:16 video with a blurred duplicate of the current frame
behind the original video, similar to common TikTok/Reels/Shorts layouts.

Default behavior:
  - Keeps the full original foreground frame.
  - Covers the bottom-right watermark using ffmpeg delogo.
  - Builds the background from the full frame, scaled and center-cropped
    symmetrically to 9:16, then blurred.

Options:
  --width N              Output width. Default: 1080
  --height N             Output height. Default: 1920
  --blur N               gblur sigma. Default: 36
  --crf N                x264 quality. Lower is higher quality. Default: 18
  --preset NAME          x264 preset. Default: medium
  --delogo X:Y:W:H       Watermark patch rectangle. Default: 1190:666:84:44
  --no-delogo            Do not patch a watermark.
  --crop X:Y:W:H         Crop source before foreground/background processing.
                         Example for previous crop-removal: 0:0:1168:664
  --background-dim N     Background brightness adjustment. Default: -0.05
  --background-sat N     Background saturation multiplier. Default: 1.10
  -h, --help             Show help.

Examples:
  # Full original frame, smooth watermark patch, TikTok-style blur fill.
  scripts/video_blurfill.sh input.mp4 output.mp4

  # Crop watermark out first, then make blur-fill portrait.
  scripts/video_blurfill.sh input.mp4 output.mp4 --crop 0:0:1168:664 --no-delogo

  # Full frame, no watermark patch.
  scripts/video_blurfill.sh input.mp4 output.mp4 --no-delogo
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

input=$1
output=$2
shift 2

width=1080
height=1920
blur=36
crf=18
preset=medium
delogo_rect="1190:666:84:44"
use_delogo=1
crop_rect=""
background_dim="-0.05"
background_sat="1.10"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --width)
      width=$2
      shift 2
      ;;
    --height)
      height=$2
      shift 2
      ;;
    --blur)
      blur=$2
      shift 2
      ;;
    --crf)
      crf=$2
      shift 2
      ;;
    --preset)
      preset=$2
      shift 2
      ;;
    --delogo)
      delogo_rect=$2
      use_delogo=1
      shift 2
      ;;
    --no-delogo)
      use_delogo=0
      shift
      ;;
    --crop)
      crop_rect=$2
      shift 2
      ;;
    --background-dim)
      background_dim=$2
      shift 2
      ;;
    --background-sat)
      background_sat=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required but was not found in PATH." >&2
  exit 1
fi

mkdir -p "$(dirname "$output")"

pre_filters=()
if [[ -n "$crop_rect" ]]; then
  IFS=: read -r crop_x crop_y crop_w crop_h <<<"$crop_rect"
  pre_filters+=("crop=${crop_w}:${crop_h}:${crop_x}:${crop_y}")
fi

if [[ "$use_delogo" -eq 1 ]]; then
  IFS=: read -r delogo_x delogo_y delogo_w delogo_h <<<"$delogo_rect"
  pre_filters+=("delogo=x=${delogo_x}:y=${delogo_y}:w=${delogo_w}:h=${delogo_h}:show=0")
fi

if [[ "${#pre_filters[@]}" -gt 0 ]]; then
  prefix="$(IFS=,; echo "${pre_filters[*]}"),"
else
  prefix=""
fi

filter_complex="[0:v]${prefix}split=2[fgsrc][bgsrc];"
filter_complex+="[bgsrc]scale=${width}:${height}:force_original_aspect_ratio=increase,"
filter_complex+="crop=${width}:${height},gblur=sigma=${blur},"
filter_complex+="eq=brightness=${background_dim}:saturation=${background_sat}[bg];"
filter_complex+="[fgsrc]scale=${width}:-2[fg];"
filter_complex+="[bg][fg]overlay=(W-w)/2:(H-h)/2"

ffmpeg -hide_banner -loglevel error -y -i "$input" \
  -filter_complex "$filter_complex" \
  -c:v libx264 -preset "$preset" -crf "$crf" \
  -c:a copy -movflags +faststart "$output"

printf '%s\n' "$output"
