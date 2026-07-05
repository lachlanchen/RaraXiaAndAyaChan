#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/lalachan_story_improve_loop_codex.sh STORY.md [--rounds N] [--out-dir DIR]

Options:
  --rounds N       Number of improvement rounds. Default: 10.
  --out-dir DIR    Directory for round prompts/results.
  --model MODEL    Codex model. Default: gpt-5.5.
  --effort LEVEL   Reasoning effort. Default: xhigh.
  --dry-run        Write prompts only; do not call codex exec.
  -h, --help       Show this help.

Environment overrides:
  CODEX_MODEL
  CODEX_REASONING_EFFORT
  ROUNDS
  OUTDIR
  DRY_RUN=1
USAGE
}

STORY=""
ROUNDS="${ROUNDS:-10}"
MODEL="${CODEX_MODEL:-gpt-5.5}"
EFFORT="${CODEX_REASONING_EFFORT:-xhigh}"
OUTDIR="${OUTDIR:-}"
DRY_RUN="${DRY_RUN:-0}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --rounds)
      ROUNDS="${2:?missing value for --rounds}"
      shift 2
      ;;
    --out-dir)
      OUTDIR="${2:?missing value for --out-dir}"
      shift 2
      ;;
    --model)
      MODEL="${2:?missing value for --model}"
      shift 2
      ;;
    --effort)
      EFFORT="${2:?missing value for --effort}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ -n "$STORY" ]]; then
        echo "Only one STORY.md argument is supported." >&2
        exit 2
      fi
      STORY="$1"
      shift
      ;;
  esac
done

if [[ -z "$STORY" ]]; then
  usage >&2
  exit 2
fi

if [[ ! -f "$STORY" ]]; then
  echo "Story file not found: $STORY" >&2
  exit 1
fi

if ! [[ "$ROUNDS" =~ ^[0-9]+$ ]] || [[ "$ROUNDS" -lt 1 ]]; then
  echo "--rounds must be a positive integer." >&2
  exit 2
fi

if [[ "$DRY_RUN" != "1" ]] && ! command -v codex >/dev/null 2>&1; then
  echo "codex command not found. Install Codex CLI or run with --dry-run." >&2
  exit 1
fi

slug="$(basename "$STORY")"
slug="${slug%.*}"
timestamp="$(date +%Y%m%d-%H%M%S)"

if [[ -z "$OUTDIR" ]]; then
  OUTDIR="references/story-improvement-runs/${timestamp}-${slug}"
fi

mkdir -p "$OUTDIR"
cp "$STORY" "$OUTDIR/round-00-input.md"

current="$OUTDIR/round-00-input.md"

for n in $(seq 1 "$ROUNDS"); do
  round="$(printf "%02d" "$n")"
  prompt_file="$OUTDIR/round-${round}-prompt.md"
  result_file="$OUTDIR/round-${round}-result.md"

  {
    cat <<PROMPT
You are improving a LALACHAN story for a short Xiaoyunque video.

Run exactly one critique/revision round.

Model behavior:
- Use natural, readable Chinese.
- Avoid strange AI-like wording, report voice, slogans, and over-explained morals.
- Preserve the core premise unless there is a clear story reason to change it.
- Make causality clear. Do not use random "suddenly" events to glue scenes together.
- Make the characters distinct:
  - 啦啦侠: warm, brave, a little silly.
  - 阿芽酱: observant, practical, caring, lightly teasing.
  - 飒飒君: curious, quick, physical comedy if present.
  - 庄子机器人: precise and dry if present.
- Keep the story suitable for a cute, non-horror cartoon.

Round ${round} focus:
1. Identify the 3 most important problems still present.
2. Explain why each problem hurts clarity, humor, shareability, or video generation.
3. Rewrite the story.
4. Add concise Prompt Notes only for generation constraints.

Return Markdown with exactly these sections:
# Round ${round}
## Problems
## Revised Story
## Prompt Notes
## Next Round Focus

Current draft or previous round output:
PROMPT
    sed 's/^/> /' "$current"
  } > "$prompt_file"

  if [[ "$DRY_RUN" == "1" ]]; then
    echo "dry-run wrote $prompt_file"
    current="$prompt_file"
    continue
  fi

  codex exec \
    -m "$MODEL" \
    -c "model_reasoning_effort=$EFFORT" \
    -C "$PWD" \
    --sandbox read-only \
    -o "$result_file" \
    - < "$prompt_file"

  if [[ ! -s "$result_file" ]]; then
    echo "Round $round produced an empty result: $result_file" >&2
    exit 1
  fi

  current="$result_file"
  echo "round $round -> $result_file"
done

if [[ "$DRY_RUN" != "1" ]]; then
  cp "$current" "$OUTDIR/final.md"
  echo "final -> $OUTDIR/final.md"
else
  echo "dry-run complete -> $OUTDIR"
fi
