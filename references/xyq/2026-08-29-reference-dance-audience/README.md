# Reference Dance With Quiet Audience

## Goal

Adapt the supplied portrait Luoshen dance reference into a `4:3` video while
keeping its complete soundtrack. Lala Xia, Aya Chan, Sasa Kun, and Zhuangzi
sit quietly at the side like a real concert audience. They do not speak,
sing, dance, or enter the stage.

## Xiaoyunque Attempt

- Workflow: `舞蹈模仿`
- Model: `Seedance 2.0 Mini 体验版`
- Ratio: `4:3`
- Requested duration: `45s`
- Attachments: source video, then Lala Xia, Aya Chan, Sasa Kun, and Zhuangzi
- Prompt: [`../../prompts/2026-08-29-luoshen-dance-quiet-audience-4x3.md`](../../prompts/2026-08-29-luoshen-dance-quiet-audience-4x3.md)

The Agent initially invented extra actions. A correction was sent before any
render to keep only the reference dance and the seated audience. The corrected
storyboard required `224` points while the account had `181`, so Xiaoyunque
blocked the render. No points were deducted and no paid retry was made.

## Completed Local Recovery

To preserve the reference more faithfully without another paid generation:

1. The source video remained the moving performance.
2. Its lower lyric/waveform area was excluded from the visible stage screen.
3. Static title and AI-label pixels were repaired frame by frame.
4. A generated `4:3` concert-side plate placed the four named characters in a
   fixed audience row at the right.
5. The source AAC track was copied into the output without replacement music.

Final video:

```text
Videos/luoshen_dance_quiet_audience_4x3_2026-08-29.mp4
```

Validated properties:

- H.264/AAC MP4
- `960x720`
- `24 fps`
- `1145` video frames
- `47.708333s`
- Full decode succeeds
- Decoded source and output audio SHA-256 values are identical

Run evidence and generated intermediate assets are under:

```text
outputs/xyq-runs/2026-08-29-reference-dance-audience/
```

## Reuse Note

For a reference-performance adaptation where the added characters should do
almost nothing, describe them as a fixed side audience. Avoid asking the video
model to create dialogue, reaction shots, or a parallel story. If a paid
storyboard adds unsupported actions, correct it before rendering and re-check
the displayed cost.
