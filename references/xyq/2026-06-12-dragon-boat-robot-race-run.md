# 2026-06-12 Dragon Boat Robot Race Xiaoyunque Run

## Result

- Thread: `https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=40538d89-ea94-4e8e-a844-9dd8239f8166&agent_name=pippit_nest_agent`
- Mode: `创作 Agent` / integrated-agent, used because the target was about 30 seconds.
- Model: normal `Seedance 2.0`, not Fast, not VIP.
- Ratio: `4:3`.
- Uploaded files:
  - `LazyingArtRobot.png`
  - `patchwork-leather-notebook-luxury-clean-v2.png`
  - `R1.jpg.jpeg`
  - `R3.jpg.jpeg`
  - `Trio.png`
- Prompt: `references/prompts/2026-06-12-dragon-boat-robot-race-30s.md`
- Final video:
  - `outputs/xyq-run/2026-06-12-dragon-boat-robot-race/dragon_boat_robot_race_30s_2026-06-12.mp4`
  - `Videos/dragon_boat_robot_race_30s_2026-06-12.mp4`
- Verified by `ffprobe`: H.264/AAC, `1112x836`, `33.467s`, `47,098,438` bytes.

## Notes

The Agent first generated a 52-second storyboard, then compressed it to about 33 seconds. It paused after storyboard/reference generation and required a same-thread continuation message:

```text
继续生成视频。请保持 4:3、30秒左右、普通 Seedance 2.0、非 Fast、非 VIP、无字幕。
```

The page then hit a credit blocker. After recharge, the same thread needed a second same-thread recovery message:

```text
已充值，请继续生成视频。保持 4:3、30秒左右、普通 Seedance 2.0、非 Fast、非 VIP、无字幕。
```

The job entered queue, charged points, rendered five segments, then rendered `final_video.mp4`.

## Monitoring Fix

`scripts/xyq_chrome/watch_thread_dom_download.py` was improved for this run:

- Do not stop on stale `积分不足` when the thread later has `支付成功` or continues running.
- Detect new downloaded MP4 files in `~/Downloads` with safe path handling for filenames like `final_video (5).mp4`.
- If a final video is visible but direct URL fetch is blocked, click the Xiaoyunque page `下载` button and wait for the browser download.

The old monitor missed the existing download because the fallback verification command split filenames on spaces. Use `find -print0` or quoted paths for future manual checks.
