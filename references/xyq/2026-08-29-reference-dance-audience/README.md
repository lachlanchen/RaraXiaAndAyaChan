# Luoshen MV With Four Buddies As Audience

## Result

Xiaoyunque regenerated the supplied Luoshen performance as a `4:3` MV. The
female dancer remains the main performer while Lala Xia, Aya Chan, Sasa Kun,
and Zhuangzi sit at the side as a natural concert audience. They gently move
light sticks, react to the performance, and stay off the stage.

Final delivery:

```text
Videos/luoshen_mv_four_buddies_audience_4x3_2026-08-29.mp4
```

Raw Xiaoyunque download:

```text
outputs/xyq-runs/2026-08-29-reference-dance-audience/luoshen_mv_four_buddies_audience_xyq_47s.mp4
```

The final delivery uses the generated picture track, crops four pixels from
each side to produce exact `960x720` `4:3`, freezes the last frame briefly,
and stream-copies the complete AAC track from the supplied source. The source
and final compressed audio packet hashes are identical.

## Source And Prompt

- Source: `/home/lachlan/Nutstore Files/Projects/LalaChan/2026-08-28_22-28-00.MP4`
- Prompt: [`../../prompts/2026-08-29-luoshen-mv-enter-and-watch-4x3.md`](../../prompts/2026-08-29-luoshen-mv-enter-and-watch-4x3.md)
- Xiaoyunque thread: `6bcef848-e9fa-40c2-9b4c-335a9d0e0bd8`
- Workflow: integrated Agent using four generated video segments
- Model: `Seedance 2.0 Mini 体验版`
- Ratio: `4:3`
- Segment durations: `15s + 12s + 12s + 8s`

The prompt treats the four characters as people already present in the
performance world. It does not ask them to enter the video later. The dancer
and environment use realistic cinematic imagery; only the four established
characters retain their figurine/robot appearances.

## Paid Preflight And Cost

Preflight evidence:

```text
outputs/xyq-runs/2026-08-29-reference-dance-audience/preflight-final-324pts.png
outputs/xyq-runs/2026-08-29-reference-dance-audience/preflight-shot4-retry-68pts.png
```

- Visible starting balance: `673`
- Balance after initial four-segment confirmation: `389`
- Initial observed deduction: `284`
- Fourth-segment retry deduction: `68`
- Final visible balance: `321`
- Total observed deduction: `352`

The fourth segment needed one retry after Xiaoyunque reported a short
reference. The first three completed segments were not regenerated. A later
accidental stop interrupted only the Agent's post-generation work; sending a
single continuation message resumed stitching without another paid render.

## Local Audio Lock

Xiaoyunque's assembled file was `968x720`, `47.400s`, with a re-encoded
`44.1 kHz` AAC track. The source track is `48 kHz`, `47.701s`. The delivery was
therefore rebuilt locally with the source AAC stream copied unchanged:

```bash
ffmpeg -i RAW_XYQ.mp4 -i SOURCE.MP4 \
  -filter_complex '[0:v]crop=960:720:4:0,tpad=stop_mode=clone:stop_duration=0.35,format=yuv420p[v]' \
  -map '[v]' -map 1:a:0 \
  -c:v libx264 -preset slow -crf 14 \
  -c:a copy -movflags +faststart -shortest FINAL.mp4
```

Validated final properties:

- H.264/AAC MP4
- `960x720`, exact `4:3`
- `30 fps`, `1428` decoded video frames
- Container duration `47.701s`
- Audio `48 kHz`, stereo, duration `47.701s`
- Full decode succeeds
- Source and final audio packet SHA-256:
  `92dd04d858612f930bc708df6e3a34866ec063f15462402aacd2c212145e92b5`
- Final file SHA-256:
  `7a66e17aacce2e1432a2a2bc581539e95672ae38fc41c051c43dcf98271ae0fe`

Visual evidence:

```text
outputs/xyq-runs/2026-08-29-reference-dance-audience/validation/contact-sheet-12.png
```

The contact sheet confirms a realistic female dancer as the visual focus and
the four named characters appearing as a small side audience. There are no
lyrics or dialogue subtitles. Xiaoyunque's small platform-provided `AI生成`
label remains at the top-left.

## Watcher Improvement

`scripts/xyq_chrome/watch_thread_dom_download.py` now supports expected aspect
ratio checks, rejected SHA-256 values, and exact output file destinations.
This prevents a same-duration source upload from being mistaken for the final
generated video and rejects intermediate clips that do not match the requested
duration or ratio.
