#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: doubao_lock_soundtrack.sh VIDEO.mp4 AUDIO.mp3 OUTPUT.mp4 [START_SECONDS]

Replaces a generated video's audio with an excerpt from an external soundtrack.
The output ends with the shorter of the video and remaining audio.
EOF
}

if [[ $# -lt 3 || $# -gt 4 ]]; then
  usage >&2
  exit 2
fi

video=$1
audio=$2
output=$3
start=${4:-0}

[[ -s "$video" ]] || { echo "Video not found: $video" >&2; exit 1; }
[[ -s "$audio" ]] || { echo "Audio not found: $audio" >&2; exit 1; }
mkdir -p "$(dirname "$output")"

ffmpeg -y \
  -i "$video" \
  -ss "$start" -i "$audio" \
  -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  "$output"

ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=index,codec_type,codec_name,width,height \
  -of json "$output"
