#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/prepend-image-cover.sh COVER_IMAGE INPUT_VIDEO OUTPUT_VIDEO [DURATION]

Prepends a still-image cover to a video while matching the source dimensions,
frame rate, and stereo audio layout. DURATION defaults to 2 seconds.
EOF
}

if [[ $# -lt 3 || $# -gt 4 ]]; then
  usage >&2
  exit 2
fi

cover_image=$1
input_video=$2
output_video=$3
cover_duration=${4:-2}

for input in "$cover_image" "$input_video"; do
  if [[ ! -f "$input" ]]; then
    echo "Input not found: $input" >&2
    exit 1
  fi
done

IFS=',' read -r width height fps < <(
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,r_frame_rate \
    -of csv=p=0 "$input_video"
)

if [[ -z "$width" || -z "$height" || -z "$fps" ]]; then
  echo "Could not probe source video geometry: $input_video" >&2
  exit 1
fi

mkdir -p "$(dirname "$output_video")"

ffmpeg -y \
  -loop 1 -framerate "$fps" -t "$cover_duration" -i "$cover_image" \
  -i "$input_video" \
  -filter_complex "
    [0:v]scale=${width}:${height}:force_original_aspect_ratio=increase,
         crop=${width}:${height},setsar=1,
         zoompan=z='min(zoom+0.0005,1.03)':d=1:s=${width}x${height}:fps=${fps},
         trim=duration=${cover_duration},setpts=PTS-STARTPTS,format=yuv420p[coverv];
    anullsrc=channel_layout=stereo:sample_rate=44100,
         atrim=duration=${cover_duration},asetpts=PTS-STARTPTS[covera];
    [1:v]fps=${fps},scale=${width}:${height},setsar=1,
         setpts=PTS-STARTPTS,format=yuv420p[mainv];
    [1:a]aresample=44100,aformat=channel_layouts=stereo,
         asetpts=PTS-STARTPTS[maina];
    [coverv][covera][mainv][maina]concat=n=2:v=1:a=1[outv][outa]
  " \
  -map '[outv]' -map '[outa]' \
  -c:v libx264 -preset slow -crf 14 \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  "$output_video"

ffprobe -v error \
  -show_entries stream=codec_name,width,height \
  -show_entries format=duration,size \
  -of json "$output_video"
