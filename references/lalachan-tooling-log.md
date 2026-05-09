# LALACHAN Tooling Log

This records the reusable code, methods, scripts, and verification steps created for the LALACHAN media workflow.

## Video Blur-Fill And Watermark Work

Script:

```bash
scripts/video_blurfill.sh
```

Method:

- Builds a `1080x1920` portrait frame from landscape source video.
- Uses a zoomed, blurred duplicate of the current frame as the background.
- Places the original video over the center without cropping the foreground.
- Uses a smooth `delogo`/blur patch for the bottom-right watermark area when requested.

Documentation:

```bash
references/video-blurfill-watermark-workflow.md
```

## Subtitle Removal Work

Script:

```bash
scripts/remove_subtitle_band.py
```

Method:

- Reads frames with OpenCV and preserves the source audio with `ffmpeg`.
- Scans the lower frame for subtitle-like bright text.
- Smooths the detected subtitle band position frame to frame.
- Applies a feathered Gaussian blur only to that band.
- Supports `--mode mask-inpaint` for clips where blur leaves visible glyph shapes.
- Keeps an inpaint mode for simple backgrounds, but blur is preferred for detailed animated scenes.

Recent outputs:

```bash
Videos/edited/v03c76g10004d7spspaljht0mpia.885_2026_05_05_15_41_55_COMPLETED_subtitle_removed_dynamic.mp4
Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_dynamic.mp4
Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_mask_inpaint_v3.mp4
```

Documentation:

```bash
references/subtitle-removal-workflow.md
```

## Xiaoyunque Browser Automation

Scripts:

```bash
scripts/xyq_chrome/launch_chrome.sh
scripts/xyq_chrome/xyq_cdp.py
scripts/xyq_chrome/reference_video_until_credit.py
scripts/xyq_chrome/test_modes.py
scripts/xyq_chrome/prepare_duanju_from_chatgpt.py
scripts/xyq_chrome/chatgpt_thread_prompt.py
scripts/xyq_cdp_browser.py
```

Method:

- Launches Chrome with a persistent controlled profile and `--remote-debugging-port=9222`.
- Attaches through Chrome DevTools Protocol, matching the `../ProteinStructure` approach.
- Detects visible prompt fields, buttons, media, and `svg.lucide-external-link` icons.
- Can list/select visible Xiaoyunque creation modes such as `Agent 模式` and `沉浸式短片`.
- Can smoke-test `Agent 模式`, `沉浸式短片`, `智能长视频 2.0`, and the direct `短剧 Agent` tab without submitting generation.
- Can fill prompts without submitting and can click indexed external-link icons.
- Can submit a local reference video plus the default three Lala/Aya/Sasa images through the Xiaoyunque skill API, auto-confirm once, and stop at the insufficient-credit generation step.
- Can prepare `短剧 Agent` directly from the saved ChatGPT conversation draft, upload the `.txt` script to the `/novel/list` workspace, and set `Trio.png` as the default uploaded character reference asset.
- Can send a synopsis into the existing ChatGPT `小云雀剧本` thread through the same Chrome driver and save the new assistant answer to Markdown.
- Can drive the current already-open Xiaoyunque tab by page id, set Tiptap prompts safely, click the bottom `+` upload menu, choose `从资产库选择`, select old generated videos, and save screenshots.

Documentation:

```bash
references/xyq-browser-automation-workflow.md
references/xyq-duanju-agent-chatgpt-workflow.md
references/xyq-reference-video-credit-run.md
references/xyq-asset-library-reference-workflow.md
references/2026-05-09-xiaoyunque-prompts-methods.md
references/2026-05-09-user-prompt-history.md
references/xyq-lala-aya-sasa-defaults.md
references/xyq-mode-test-results.md
```

## Prompt Assets

Saved prompt references:

```bash
references/prompts/forest-dinosaur-portrait-15s.md
references/prompts/lala-miao-ikaku-lazy-chat.md
```

## Verification Commands

Compile Python scripts:

```bash
python3 -m py_compile scripts/remove_subtitle_band.py scripts/xyq_chrome/xyq_cdp.py
```

Check video metadata:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate \
  -show_entries format=duration \
  output.mp4
```

Check Xiaoyunque CDP state:

```bash
scripts/xyq_chrome/xyq_cdp.py --state
```

Smoke-test Xiaoyunque mode selection:

```bash
scripts/xyq_chrome/test_modes.py --output references/xyq-mode-test-results.md
```

Send a synopsis to the ChatGPT script thread and save the response:

```bash
scripts/xyq_chrome/chatgpt_thread_prompt.py \
  --prompt-file Lala-Aya-Sasa-draft/2026-05-09-today-script-synopsis.md \
  --output Lala-Aya-Sasa-draft/2026-05-09-hong-kong-rainy-tea-restaurant-chatgpt.md
```

Use the current-tab Xiaoyunque CDP helper:

```bash
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py visible PAGE_ID
scripts/xyq_cdp_browser.py set-prompt PAGE_ID references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s-numbered-assets.md
scripts/xyq_cdp_browser.py click PAGE_ID 484 753
```

## 2026-05-10 Moon Video Preparation

Prepared tomorrow's Xiaoyunque `沉浸式短片` draft in the existing Chrome tab without submitting generation.

Saved inputs and outputs:

```bash
Lala-Aya-Sasa-draft/2026-05-10-moon-universe-fight-synopsis.md
Lala-Aya-Sasa-draft/2026-05-10-moon-universe-fight-chatgpt-retry.md
references/prompts/2026-05-10-moon-universe-fight-duanpian-15s-numbered-assets.md
references/2026-05-10-moon-universe-fight-prep.md
```

Browser state:

- Mode: `沉浸式短片`
- Model: `Seedance 2.0 Fast`
- Duration: `15s`
- Images: `display.png`, `patchwork-leather-notebook-luxury-clean-v2.png`, `R1.jpg.jpeg`, `R3.jpg.jpeg`, `Trio.png`
- Asset-library reference video: `资产 #7637271291062632985`
- Final prompt includes the no-subtitles instruction and short Chinese dialogue.
- Stopped with the final create arrow enabled, not clicked.
