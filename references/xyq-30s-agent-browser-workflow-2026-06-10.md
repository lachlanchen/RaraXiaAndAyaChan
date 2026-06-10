# Xiaoyunque 30s Agent Browser Workflow

This note records the reusable 30-second generation method used on 2026-06-10 for the AgInTi lab story. It is intentionally workflow-level, not story-specific.

## When To Use

Use this method when the requested video is about 30 seconds and the `沉浸式短片` composer is locked to `15秒` or defaults to a VIP short-film model. For 15-second videos, the normal `沉浸式短片` workflow is still preferred.

## Method

1. Attach to the logged-in Chrome CDP page:

```bash
python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 list-pages
python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 bring-to-front PAGE_ID
```

2. Open the `创作` page and stay in `创作 Agent` / integrated-agent mode. Do not force `沉浸式短片` if it only offers `15秒`.

3. Upload local images directly through the page upload control. Do not paste local file paths into the prompt:

```bash
python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 upload-images-verify PAGE_ID \
  /path/to/ref1.png /path/to/ref2.png /path/to/ref3.jpg \
  --timeout 240 \
  --screenshot outputs/xyq-run/example/after-upload.png
```

4. Use a compact prompt that says `30 秒` in the first sentence and describes the reference image order. Keep restrictions short; over-patched prompts tend to perform worse.

5. Fill and submit from the enabled send button:

```bash
python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 type-prompt PAGE_ID references/prompts/example-30s.md --wait 1
python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 screenshot PAGE_ID outputs/xyq-run/example/pre-submit.png
python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 click PAGE_ID SEND_X SEND_Y
```

6. Watch the resulting `integrated-agent` thread. If the Agent pauses after storyboard/material generation and asks to continue, reply in the same thread with `继续生成视频。`

```bash
python3 scripts/xyq_chrome/watch_thread_dom_download.py \
  --cdp-url http://127.0.0.1:9222 \
  --page-id PAGE_ID \
  --thread-url "THREAD_URL" \
  --output-dir outputs/xyq-run/example \
  --filename result_30s.mp4 \
  --copy-to Videos
```

## Caveats

- `沉浸式短片` can show `Seedance 2.0 Fast VIP` and `15秒`; do not fight this control for 30-second work.
- Agent mode may first produce a storyboard or assets before final rendering.
- Keep page control in the existing logged-in tab when possible.
- If Xiaoyunque appears to load forever, focus the address bar and press Enter in the controlled browser, then reattach to the same tab.
- Verify final local output with `ffprobe` and record the copied path.
