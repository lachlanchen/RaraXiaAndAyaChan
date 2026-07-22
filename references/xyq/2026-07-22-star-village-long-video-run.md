# Star Village Long-Video Run

This run records the verified browser workflow for the 30-second episode
`星星村的庭院晚饭`.

## Production Contract

- Top-level mode: `创作 Agent`; `沉浸式短片` was not used.
- Model: `Seedance 2.0 Mini 体验版`.
- Duration control: `30秒`; Xiaoyunque produced three shots totaling 32 seconds.
- Ratio: `4:3`.
- Visible rate before submission: `4积分/秒`.
- References: eight real uploaded files, including six cast/prop references,
  the 一二/布布 identity image, and the approved scene keyframe.
- Submission count: one.

For work longer than 15 seconds, select the exact top-level Agent workflow and
make sure the short-film chip is not active. Mini may still be available inside
Agent mode even when the short-film workflow itself is capped at 15 seconds.
Do not split or compress a longer story unless the user asks.

## Same-Thread Continuation

The Agent first generated a storyboard and references, then paused for
confirmation. Continue in the existing thread with `继续生成视频。`; do not open a
new session or repeat the original paid submission. The final storyboard had
three shots and a nominal duration of 32 seconds.

## Browser Topology Check

The canonical logged-in Xiaoyunque profile was exposed through:

```text
CDP: http://127.0.0.1:9344
X display: :98
noVNC: http://127.0.0.1:6099/
profile: ~/.cache/xyq-chrome
```

A stale local setting pointed to port `9222`, which belonged to another Chrome
profile and display. A responsive CDP port alone is not proof that it is the
correct browser. Before upload or submission, verify the Chrome process profile,
X display, page URL, and noVNC view all describe the same tab. Explicit Studio
`LALA_STUDIO_XYQ_*` settings must take precedence over legacy project values.

## Download And Verification

The watcher scoped discovery to the current completed result. Direct protected
URL fetch failed, so it opened the current result preview, clicked its visible
download control once, and accepted the new browser download.

Final file:

```text
Videos/2026-07-22-star-village-gyugyu-hug.mp4
```

Verified properties:

- duration: `32.367s`
- video: H.264, `968x720`, 30 fps
- audio: AAC stereo, 44.1 kHz
- size: `37,193,546` bytes
- SHA-256: `2e3b3fc3b12ae132d44ce10c4414dd5252b4e244d1ca186f06681bf0b4773862`
- complete video and audio decoding passed

The approved scene keyframe SHA-256 was
`2041fcb412a0240f668b3ee0dd1ac6594f5f9dbf03e4ec90d340cbc34b2b005f`.
