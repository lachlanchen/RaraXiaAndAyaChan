# 2026-06-13 Snow Valley Sunrise Xiaoyunque Run

## Result

- Thread: `https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=75a03d09-ccd8-4bff-8c95-1cc6f8f1a83d&agent_name=pippit_nest_agent`
- Mode: `创作 Agent` / integrated-agent, used because `沉浸式短片` duration was capped at 15 seconds.
- Model: `Seedance 2.0 Fast`, non-VIP.
- Ratio: `4:3`.
- Target duration: `30s`.
- Charged points: `150` points, from `660` to `510`.
- Uploaded files:
  - `LazyingArtRobot.png`
  - `R1.jpg.jpeg`
  - `R3.jpg.jpeg`
  - `Trio.png`
- Prompt: `references/prompts/2026-06-13-snow-valley-sunrise-freedom-30s.md`
- Final video:
  - `outputs/xyq-run/2026-06-13-snow-valley-sunrise/snow_valley_sunrise_freedom_30s_2026-06-13.mp4`
  - `Videos/snow_valley_sunrise_freedom_30s_2026-06-13.mp4`
- Verified by `ffprobe`: H.264/AAC, `1112x836`, `30.434s`, `46,787,712` bytes.

## Notes

The user asked for the least-credit model, then changed the target from 15s to
30s. The short-film duration input exposed `max=15`, so the run switched to
the Agent composer. Agent mode still allowed choosing `Seedance 2.0 Fast`.

The Agent first generated a 48-second storyboard, then automatically compressed
it to four shots totaling exactly 30 seconds:

- S1: 8s
- S2: 8s
- S3: 6s
- S4: 8s

The Agent paused after storyboard/reference asset generation. A same-thread
continuation was sent:

```text
继续生成视频。请保持 4:3、30秒左右、Seedance 2.0 Fast、低积分优先、无字幕。
```

The render completed successfully. The resource panel had to be switched from
`参考 4` to `生成结果 1`; the final `final_video.mp4` card was below the viewport
and needed `scrollIntoView()` before opening.

The protected video URL failed direct browser-context fetch, but the updated
watcher clicked the page `下载` button and detected:

```text
/home/lachlan/Downloads/final_video (6).mp4
```

The watcher copied it to the output run folder and `Videos/`.
