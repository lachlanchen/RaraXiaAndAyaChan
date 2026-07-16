# Xiaoyunque Uploaded-Images No-Path Workflow

This records the corrected LALACHAN Xiaoyunque workflow after the 2026-06-09
Mars cleanroom run. The main lesson is simple: local paths are for browser file
upload only. Never paste local filesystem paths into the Xiaoyunque prompt.

## Current Default Reference Order

Always upload the files in this order when the user asks for the standard
LALACHAN image set:

| Image | File | Meaning |
| --- | --- | --- |
| 图1 | `words-card.jpg` | words card / 小白屏学习卡 style reference; show a fresh word each episode |
| 图2 | `LazyingArtRobot.png` | robot `庄子`; keep LazyingArt logo on chest |
| 图3 | `display.png` | LightMind AI glasses |
| 图4 | `patchwork-leather-notebook-luxury-clean-v2.png` | handmade patchwork notebook |
| 图5 | `raraxia.jpeg` | individual 啦啦侠 / Rara Xia reference |
| 图6 | `ayachan.png` | individual 阿芽酱 / Aya Chan reference |
| 图7 | `sasakun.jpeg` | individual 飒飒君 / Sasa Kun reference |
| 图8 | `Trio.png` | three-character identity reference: 啦啦侠, 阿芽酱, 飒飒君 |

Prompt text should refer to these only as `图1` through `图8`. Do not include
`/home`, `ProjectsLFS`, `artifacts/`, `.png`, `.jpg`, or `.jpeg` in the prompt.
For `图1`, choose a new story-relevant concept every time. The visible card
must contain the multilingual values only, with no language names, field
labels, colons, bullets, or numbering. Check every value equally for correct
spelling, script, reading, and meaning. All values must represent the same
concept.

The reliable prompt style is: `图1 是已经制作好的小白屏学习卡，可作为场景边缘、桌面、道具架或实验台上的小道具。卡面依次显示 WORD、日本語、ふりがな、目标语言含义，不带语言标签。它只是场景里的真实道具，不是字幕。`

Two implementation paths are valid:

- Generate a new words-card image first with image generation, inspect the
  rendered text at original resolution, and upload that new card as `图1`.
- Upload the existing words-card as the `图1` style/example reference, then give
  Xiaoyunque the exact English/Japanese/furigana content and let it render the
  card in-scene.

Use either path, or both, as long as the final prompt and uploaded materials make
the fresh words card clear.

## Pre-Submit Contract

For the usual short-video workflow, verify all of these before submission:

- target `30秒` by default unless the user explicitly asks for 15s/cheapest/quick test
- use a 30s-capable Agent/integrated workflow when `沉浸式短片` is capped at `15秒`
- `Seedance 2.0 Fast` non-VIP for the current low-credit default, unless the user explicitly requests normal non-Fast or higher quality
- `4:3` unless the user explicitly asks for another ratio
- eight uploaded image chips/cards, all with `success` upload state
- prompt includes `不要字幕，不要生成任何字幕、说明文字、下三分之一文字或画面文字。`
- prompt contains no local paths or filenames
- submit arrow is enabled

If any item is unproven, do not submit yet.

## Browser Setup

Use the controlled Chrome/CDP profile, not the Xiaoyunque API:

```bash
cd /home/lachlan/ProjectsLFS/LALACHAN
curl -fsS http://127.0.0.1:9222/json/list
scripts/xyq_cdp_browser.py list-pages
```

If the page is blank or infinitely loading, recover the same tab instead of
opening a new tab:

```bash
scripts/xyq_cdp_browser.py navigate PAGE_ID \
  "https://xyq.jianying.com/home?tab_name=integrated-agent"
sleep 8
scripts/xyq_cdp_browser.py visible PAGE_ID
```

Bring the chosen page forward before every major operation:

```bash
scripts/xyq_cdp_browser.py bring-to-front PAGE_ID
scripts/xyq_cdp_browser.py visible PAGE_ID
```

If the current Xiaoyunque thread is completed, stale, or showing the wrong
workflow, create a fresh composer from the page itself. Use the visible
`创作` / new-session button in the existing controlled tab, then verify the new
thread URL. Do not keep opening extra tabs just to start a new job.

## Upload The Eight Images

Upload through the page file input. The path arguments are for the browser
upload command only; they are not prompt content.

```bash
scripts/xyq_cdp_browser.py upload-images-verify PAGE_ID \
  words-card.jpg \
  LazyingArtRobot.png \
  display.png \
  patchwork-leather-notebook-luxury-clean-v2.png \
  raraxia.jpeg \
  ayachan.png \
  sasakun.jpeg \
  Trio.png \
  --screenshot outputs/xyq-run/after-upload-eight.png \
  --timeout 180
```

Check that the visible upload cards are successful. A single `uploading` card
keeps the submit button disabled. If one file stalls, remove that chip and retry
that file. If a large PNG repeatedly stalls, a temporary smaller copy can be used
for upload, but the prompt must still say `图1` rather than a path.

## Prompt Validation

Save the prompt under `references/prompts/` and run a path leak check:

```bash
rg -n '/home|ProjectsLFS|artifacts|\.png|\.jpg|\.jpeg' \
  references/prompts/PROMPT.md || true
```

The corrected prompt pattern is:

```text
参考图顺序：图1 是小白屏学习卡风格参考，可作为场景边缘、桌面、道具架或实验台上的小道具。
本集单词卡已经制作完成，卡面依次显示：TOPIC_WORD、日本語、ふりがな、目标语言含义。
卡面不要显示语言名称、字段标签、冒号、编号或项目符号。
它只是场景里的真实道具，不是字幕。图2 是 LazyingArtRobot，机器人庄子；
图3 是 LightMind AI 眼镜；图4 是拼皮笔记本；图5 是啦啦侠单人参考；
图6 是阿芽酱单人参考；图7 是飒飒君单人参考；图8 是啦啦侠、阿芽酱、飒飒君三人角色参考。
请只根据这些已经上传的图片参考，不要把任何文件名或路径画进视频。
```

Fill the prompt with user-like typing:

```bash
scripts/xyq_cdp_browser.py type-prompt PAGE_ID references/prompts/PROMPT.md
```

After filling, inspect the page text or editor content to confirm the prompt is
present and no local paths were pasted.

## Submit And Watch

Submit only after the full contract is proven. Record the final thread URL,
page id, screenshots, selected model, duration, ratio, and prompt path.

Use the browser watcher:

```bash
scripts/xyq_chrome/watch_thread_dom_download.py \
  --page-id PAGE_ID \
  --thread-url "THREAD_URL" \
  --output-dir outputs/xyq-run \
  --filename result_30s.mp4 \
  --copy-to Videos \
  --interval 30 --max-polls 240 --reload-every 300
```

Xiaoyunque media URLs are often protected. Direct external download can fail
even when the logged-in browser can play the video. Prefer these fallbacks in
order:

1. Browser-context watcher download.
2. In-page `fetch(..., {credentials: 'include'})` plus blob download.
3. Manual click on Xiaoyunque `下载`, then copy from `~/Downloads`.

The browser-context fetch is still browser UI/CDP work, not Xiaoyunque API
submission.

## Successful Corrected Run

Run date: 2026-06-09.

Corrected prompt:

```text
references/prompts/2026-06-08-mars-cleanroom-riceball-alarm-duanpian-15s-uploaded-images-only.md
```

Thread:

```text
https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=5c27f83d-5e94-49a9-87c3-fd8982e88340&agent_name=pippit_video_part_agent
```

Evidence screenshots:

```text
outputs/xyq-2026-06-09-cleanroom-riceball-uploaded-only/after-upload-seven-direct.png
outputs/xyq-2026-06-09-cleanroom-riceball-uploaded-only/after-prompt-no-path.png
outputs/xyq-2026-06-09-cleanroom-riceball-uploaded-only/pre-submit-ready.png
outputs/xyq-2026-06-09-cleanroom-riceball-uploaded-only/completed-thread.png
```

Output files:

```text
outputs/xyq-2026-06-09-cleanroom-riceball-uploaded-only/mars_cleanroom_riceball_alarm_15s_uploaded_images_only.mp4
Videos/mars_cleanroom_riceball_alarm_15s_uploaded_images_only.mp4
```

Verified output:

```text
duration: 15.125s
video: H.264, 1112x836
audio: AAC
size: 6015704 bytes
```

## Mistake To Avoid

The earlier run pasted absolute local paths into the prompt. That is wrong. The
model cannot access local filesystem paths as images; it may treat them as
visible text, prop labels, or confusing story material. The corrected future
workflow uploads the eight images through the browser file input and references
them only as `图1` to `图8`.

## Skill Update

The local Codex skill was updated:

```text
/home/lachlan/.codex/skills/lalachan-xyq-browser-video/SKILL.md
```

Future Xiaoyunque work should load this note together with:

```text
references/xyq-browser-video-generation-skill.md
references/xyq-smooth-video-generation-experience-2026-06-06.md
references/xyq-mars-chip-browser-run-2026-06-07.md
```
