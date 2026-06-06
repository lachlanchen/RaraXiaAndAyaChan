# Red Sand Paper Kite Series Workflow

This document records the story design, Xiaoyunque generation run, and reusable
method for the current LALACHAN red-sand series.

## Source Handling

The story direction was informed by local context from:

- `/home/lachlan/ProjectsLFS/ZhJpBook/build/`
- `/home/lachlan/Documents/VoidAbyss`
- prior LALACHAN universe/adventure episodes in `references/stories/`

Use these only as motif and structure references. Do not quote, summarize, or
name the source books inside the generated story or Xiaoyunque prompt unless the
user explicitly asks. The output should feel original: red frontier, old ritual
objects, gates, lamps, paper kite, fragile settlement ethics, and ordinary
characters making kind choices under pressure.

## Series Canon

Current series name:

```text
红砂纸鸢 / Red Sand Paper Kite
```

Core characters:

- `啦啦侠`: warm, hungry, confident, funny.
- `阿芽酱`: careful, emotionally intelligent, gentle but sharp with jokes.
- `飒飒君`: impulsive, brave, often misunderstands magical rules.

Recurring props:

- `LightMind AI 眼镜`: all three wear them.
- `拼皮笔记本`: Aya Chan's notebook, reacts to old mechanisms.
- `竹子玩具`: Sasa Kun calls it his courage; it can be blown or pulled away.
- `发光纸鸢`: guide and mischievous road administrator.

Series rule:

Each episode should contain a tiny moral choice, but never sound preachy. The
fun is that the heroes accidentally learn that the fastest, brightest, or
strongest option is not always the right one.

## Saved Episodes

Episode 01:

```text
references/stories/2026-06-07-red-sand-bronze-kite-15s.md
references/prompts/2026-06-07-red-sand-bronze-kite-duanpian-15s.md
Videos/red_sand_bronze_kite_15s.mp4
outputs/xyq-2026-06-07-red-sand-bronze-kite/red_sand_bronze_kite_15s.mp4
```

Commit:

```text
e13dd49 Add red sand bronze kite story
```

Episode 02 draft for tomorrow:

```text
references/stories/2026-06-08-red-sand-lighthouse-three-lamps-15s.md
references/prompts/2026-06-08-red-sand-lighthouse-three-lamps-duanpian-15s.md
references/stories/red-sand-paper-kite-series-notes.md
```

Commit:

```text
7532305 Add red sand lighthouse continuation
```

## Xiaoyunque Run Details

Use browser UI, not API, unless explicitly requested.

Submitted thread:

```text
https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=65eabc08-6fad-49e2-8453-170022b93256&agent_name=pippit_video_part_agent
```

Final pre-submit state:

```text
Mode: 沉浸式短片
Model: Seedance 2.0 Fast
Model tier: normal, no VIP label
Duration: 15秒
Ratio: 4:3
Resolution: 720P
Reference images: 5 uploaded
Prompt rule: no subtitles / no on-screen text
```

Reference image order:

```text
1. display.png
2. patchwork-leather-notebook-luxury-clean-v2.png
3. R1.jpg.jpeg
4. R3.jpg.jpeg
5. Trio.png
```

The generated file was verified by `ffprobe`:

```text
duration: 15.125s
video: h264, 1112x836
audio: aac
size: 6,790,099 bytes
```

## Browser Commands Used

Check Chrome/CDP:

```bash
curl -fsS http://127.0.0.1:9222/json/version
python3 scripts/xyq_cdp_browser.py list-pages
```

Bring page forward:

```bash
python3 scripts/xyq_cdp_browser.py bring-to-front PAGE_ID
python3 scripts/xyq_cdp_browser.py visible PAGE_ID
```

Recover same tab if needed:

```bash
python3 scripts/xyq_cdp_browser.py navigate PAGE_ID \
  "https://xyq.jianying.com/home?tab_name=integrated-agent"
python3 scripts/xyq_cdp_browser.py wait PAGE_ID 8
```

Upload and verify five images:

```bash
python3 scripts/xyq_cdp_browser.py upload-images-verify PAGE_ID \
  display.png patchwork-leather-notebook-luxury-clean-v2.png \
  R1.jpg.jpeg R3.jpg.jpeg Trio.png \
  --screenshot outputs/xyq-run/after-upload.png \
  --timeout 90 --interval 3
```

Type prompt:

```bash
python3 scripts/xyq_cdp_browser.py type-prompt PAGE_ID \
  references/prompts/2026-06-07-red-sand-bronze-kite-duanpian-15s.md
```

Watch and download:

```bash
python3 scripts/xyq_chrome/watch_thread_dom_download.py \
  --page-id PAGE_ID \
  --thread-url "THREAD_URL" \
  --output-dir outputs/xyq-2026-06-07-red-sand-bronze-kite \
  --filename red_sand_bronze_kite_15s.mp4 \
  --copy-to Videos \
  --interval 15 \
  --max-polls 240
```

## Observed Queue Behavior

The job started at about 30 minutes queued, then moved to generation near the
end. Credits dropped from `782` to `707`, confirming the task was accepted.
The watcher saw:

```text
排队等待中 -> 生成中 -> no explicit status with videos=1
```

Direct HTTP download failed because the media URL was protected. Browser-context
fetch succeeded with `video/mp4`, then the watcher triggered an in-page blob
download and copied the MP4 to `Videos/`.

## Future Checklist

1. Write story in `references/stories/YYYY-MM-DD-title-15s.md`.
2. Write matching Xiaoyunque prompt in `references/prompts/YYYY-MM-DD-title-duanpian-15s.md`.
3. Keep prompt concise enough for 15 seconds; use clear actions and short dialog.
4. Include `不要字幕，不要生成任何字幕、说明文字、下三分之一文字或画面文字。`
5. Commit and push story/prompt before video work.
6. In Xiaoyunque, verify `沉浸式短片`, normal `Seedance 2.0 Fast`, `15秒`, and `4:3`.
7. Upload all five references with the plus/material workflow.
8. Submit once only; do not resubmit while queued.
9. Watch with `watch_thread_dom_download.py`.
10. Verify final MP4 with `ffprobe`.

