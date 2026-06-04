# Hokkaido Dolphin Shark Xiaoyunque Web Run

Date: `2026-06-02` to `2026-06-03`

This records the successful Xiaoyunque browser workflow for the LALACHAN Hokkaido sea story. The task used the web UI through Chrome/CDP, not the Xiaoyunque API.

## Prompt Files

```text
references/prompts/2026-06-02-hokkaido-dolphin-shark-15s.md
references/prompts/2026-06-02-hokkaido-dolphin-shark-submit-15s.md
```

## Xiaoyunque Settings

```text
Mode: 沉浸式短片
Model: Seedance 2.0 Fast
Duration: 15秒
Prompt language: Chinese
No-subtitle instruction: included
Thread URL: https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=d6cc0e25-7a78-4abb-a5ce-caee22e19a75&agent_name=pippit_video_part_agent
```

Five local reference images were uploaded and verified:

```text
/home/lachlan/ProjectsLFS/LALACHAN/display.png
/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
/home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Screenshots and watch logs were saved under:

```text
outputs/xyq-2026-06-02-hokkaido-dolphin-shark/
```

## Browser Commands Used

List and attach to the existing controlled Chrome tab:

```bash
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py bring-to-front E27328AAC0E159A6BD8DBA16E0880652
scripts/xyq_cdp_browser.py visible E27328AAC0E159A6BD8DBA16E0880652
```

Fill and submit workflow:

```bash
scripts/xyq_cdp_browser.py upload-images-verify PAGE_ID \
  display.png patchwork-leather-notebook-luxury-clean-v2.png \
  R1.jpg.jpeg R3.jpg.jpeg Trio.png \
  --screenshot outputs/xyq-2026-06-02-hokkaido-dolphin-shark/home-uploaded-five.png

scripts/xyq_cdp_browser.py type-prompt PAGE_ID \
  references/prompts/2026-06-02-hokkaido-dolphin-shark-submit-15s.md
```

The submit button was clicked only after confirming mode/model/duration and the five images.

## Watcher

The browser watcher was started in tmux:

```text
tmux session: xyq_hokkaido_watch
log: outputs/xyq-2026-06-02-hokkaido-dolphin-shark/watch-vip.log
```

Command pattern:

```bash
scripts/xyq_chrome/watch_thread_dom_download.py \
  --page-id PAGE_ID \
  --thread-url "THREAD_URL" \
  --output-dir outputs/xyq-2026-06-02-hokkaido-dolphin-shark \
  --filename 2026-06-02-hokkaido-dolphin-shark_15s.mp4 \
  --copy-to Videos \
  --copy-to "/home/lachlan/Nutstore Files/AutoPublish/AutoPublish" \
  --interval 30 \
  --max-polls 240 \
  --reload-every 300
```

The watcher saw the task progress through:

```text
排队等待中
优先处理中
生成中
下载
```

After VIP was paid, the page showed priority handling, for example:

```text
优先处理中（1586/18889位），还需34分钟
```

The watcher detected a video preview, but direct `everphoto` / `365yg` download URLs returned `403 Forbidden`. This means future runs should keep the browser watcher but expect a manual/browser download fallback when protected URLs appear.

## Final Copy To Nutstore

The user-downloaded files appeared in `~/Downloads`:

```text
/home/lachlan/Downloads/v03c76g10004d8ffveiljhtdlimp.346.mp4
/home/lachlan/Downloads/v03c76g10004d8fg02iljht3aq91.142.mp4
```

They were copied to Nutstore:

```bash
cp -v /home/lachlan/Downloads/v03c76g10004d8ffveiljhtdlimp.346.mp4 \
  "/home/lachlan/Nutstore Files/AutoPublish/AutoPublish/"

cp -v /home/lachlan/Downloads/v03c76g10004d8fg02iljht3aq91.142.mp4 \
  "/home/lachlan/Nutstore Files/AutoPublish/AutoPublish/"
```

Final files:

```text
/home/lachlan/Nutstore Files/AutoPublish/AutoPublish/v03c76g10004d8ffveiljhtdlimp.346.mp4
/home/lachlan/Nutstore Files/AutoPublish/AutoPublish/v03c76g10004d8fg02iljht3aq91.142.mp4
```

## Lessons

- Use browser workflow, not API, unless explicitly requested.
- Verify the visible page, not only a background CDP page.
- `Trio.png` and all four other images must be visible in the attachment list before submit.
- `基础会员` may still be visible in the header, but task-level VIP priority can still appear in the queue text.
- Direct media URL scraping can fail with `403`; use the page download/manual download fallback and then copy from `~/Downloads`.
