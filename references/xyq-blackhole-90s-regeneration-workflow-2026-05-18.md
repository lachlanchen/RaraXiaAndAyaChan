# Xiaoyunque 90s Long Video Regeneration Workflow

Date: 2026-05-18
Thread: `d4997b86-9eed-4efa-80a0-24b81e5ccc67`
Page: `https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=d4997b86-9eed-4efa-80a0-24b81e5ccc67&source=home_prompt&entrance_from=home`

## Result

The failed 13s run was regenerated as a full long video through the logged-in Xiaoyunque web UI, not the API.

- Mode: `Agent 模式`
- Duration plan: 9 shots, about 98s total
- Ratio: 16:9
- Subtitles: none requested
- Key gate: `Trio.png` confirmed by Xiaoyunque before generation
- Final status on page: 9 shot videos succeeded, 0 failed, final video duration `1:38`
- Browser-reported video duration: `98.733333s`

## Why The Earlier Run Failed

The earlier thread first created a 90s storyboard, then hit an insufficient-credit step requiring `990` points. The follow-up `continue` changed the task into a damaged continuation state: it switched to `4:3`, regenerated partial shots, and finally composed only a `0:13` video while still claiming it was a full 90s output.

For long-video failures, do not keep forcing the damaged thread. Start a fresh `Agent 模式` conversation and keep the duration/ratio requirements explicit.

## Saved Prompt Files

```bash
references/prompts/2026-05-18-blackhole-photon-race-agent-90s-regenerate.md
references/prompts/2026-05-18-blackhole-photon-race-agent-90s-followup.md
references/prompts/2026-05-18-blackhole-photon-race-agent-90s-confirm.md
```

The prompt explicitly says:

- Do not output `13s` or `15s`.
- Generate 9 shots, each about 10s.
- If one shot fails, retry that shot instead of composing a partial short video.
- If `Trio.png` is not successfully read, do not generate.

## Assets Used

Default local references:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/display.png
/home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/Trio.png
/home/lachlan/ProjectsLFS/LALACHAN/outputs/xyq-90s-regenerate-check/patchwork-notebook-upload.jpg
```

The original notebook PNG uploaded too slowly and stayed stuck in `uploading-yQkl23`, so a smaller JPG was prepared:

```bash
mkdir -p outputs/xyq-90s-regenerate-check
ffmpeg -y \
  -i /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png \
  -vf "scale='min(1600,iw)':-2" \
  -q:v 4 \
  outputs/xyq-90s-regenerate-check/patchwork-notebook-upload.jpg
```

Final prompt numbering after this upload order:

- image 1: `display.png`
- image 2: `R1.jpg.jpeg`
- image 3: `R3.jpg.jpeg`
- image 4: `Trio.png`
- image 5: `patchwork-notebook-upload.jpg`

## Browser Commands

List the Xiaoyunque page:

```bash
scripts/xyq_cdp_browser.py list-pages
PAGE=5FE7F1E7533C817C02AB149F89F1E2C6
```

Open a fresh conversation:

```bash
scripts/xyq_cdp_browser.py click-text "$PAGE" 新对话
```

Upload images through the web UI file input:

```bash
scripts/xyq_cdp_browser.py set-file-input "$PAGE" \
  /home/lachlan/ProjectsLFS/LALACHAN/display.png \
  /home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg \
  /home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg \
  /home/lachlan/ProjectsLFS/LALACHAN/Trio.png \
  /home/lachlan/ProjectsLFS/LALACHAN/outputs/xyq-90s-regenerate-check/patchwork-notebook-upload.jpg \
  --index 0
```

Verify all attachments succeeded. This is the hard gate:

```bash
scripts/xyq_cdp_browser.py eval "$PAGE" \
"(() => [...document.querySelectorAll('[class*=fileItem]')]
  .map((el,i)=>({i,text:(el.innerText||'').trim().replace(/\\n/g,' | '),
  cls:String(el.className)})))()"
```

Required state before submit:

```text
Trio.png -> success-jcmK32
```

If `Trio.png` stays `uploading-yQkl23`, do not submit. Remove it and re-upload it alone.

Fill the main prompt:

```bash
scripts/xyq_cdp_browser.py set-prompt "$PAGE" \
  references/prompts/2026-05-18-blackhole-photon-race-agent-90s-regenerate.md
```

Submit the fresh Agent task:

```bash
scripts/xyq_cdp_browser.py click "$PAGE" 1186 721
```

When Xiaoyunque asks for storyboard/material confirmation, fill:

```bash
scripts/xyq_cdp_browser.py set-prompt "$PAGE" \
  references/prompts/2026-05-18-blackhole-photon-race-agent-90s-confirm.md
scripts/xyq_cdp_browser.py click "$PAGE" 680 727
```

## Important UI Notes

- Use `Agent 模式` for long video. `沉浸式短片` is for 15s short output.
- The top banner advertising `Seedance 2.0 Fast VIP` is not the actual mode selector.
- Do not click the bottom send button while it says `停止生成`; that opens a cancel modal.
- If the cancel modal appears, click `继续等待`, not `确认取消`.
- The successful run had a confirmation gate before rendering. Confirm only after the page says all reference assets succeeded and the storyboard is full length.

## Completion Evidence

The page reported:

```text
【分镜视频生成结果】成功 9 个，失败 0 个
S1.mp4 ... S9.mp4
9个分镜全部生成成功，0个失败
生成合成视频
1:38
全部完成
```

The local automated download was interrupted because the video was downloaded manually. The partial local file was renamed:

```bash
outputs/xyq-90s-regenerate-check/blackhole_photon_race_90s.partial.mp4
```

Do not treat that partial file as the final asset.
