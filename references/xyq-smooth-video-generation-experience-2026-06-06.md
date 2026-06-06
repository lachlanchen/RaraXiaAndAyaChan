# Xiaoyunque Smooth Video Generation Experience

This records the practical browser-first workflow learned across the recent
LALACHAN video runs. Do not use the Xiaoyunque API unless the user explicitly
asks for API usage.

## Reliable Path

1. Save the story and final submit prompt under `references/`.
2. Use the controlled Chrome/CDP browser, normally `http://127.0.0.1:9222`.
3. Verify the endpoint before touching the page:

```bash
curl -fsS http://127.0.0.1:9222/json/list
scripts/xyq_cdp_browser.py list-pages
```

4. If the visible Xiaoyunque page is blank or infinite-loading, reload the same
   tab by address bar (`Ctrl+L`, `Enter`) or CDP navigate. Do not open a new tab:

```bash
scripts/xyq_cdp_browser.py navigate PAGE_ID \
  "https://xyq.jianying.com/home?tab_name=integrated-agent"
sleep 8
scripts/xyq_cdp_browser.py visible PAGE_ID
```

5. Set the pre-submit contract and prove it before generation:

- `沉浸式短片`
- normal `Seedance 2.0 Fast`, no `VIP` label
- `15秒`
- `4:3` ratio unless the user requests another ratio
- all five image references uploaded
- prompt contains `不要字幕，不要生成任何字幕、说明文字、下三分之一文字或画面文字。`

6. The compact ratio toolbar may only show `比例`; open the dropdown and check
   the active item or tooltip, for example `比例: 4:3`.
7. Upload images through `upload-images-verify`; wait until every upload card is
   success. One stuck `uploading` card keeps the submit button disabled.
8. Fill the prompt with `type-prompt`, not only DOM value replacement.
9. If JavaScript `.click()` does not submit, use a real coordinate click on the
   enabled arrow button after verifying its current rectangle.
10. Watch the submitted thread with `watch_thread_dom_download.py`.

## Download Lessons

Xiaoyunque result URLs are often protected. Direct `urllib` or `curl` may return
HTTP errors while the logged-in browser can fetch the same `video.currentSrc`.
The watcher now handles this smoother path:

1. Detect visible `<video>` elements on the submitted thread.
2. Try normal direct download with browser-like `Referer` and `User-Agent`.
3. If direct download fails and the URL is the active video source, probe from
   browser context with `fetch(..., {credentials: 'include'})`.
4. If the browser fetch returns `200` and `video/mp4`, trigger an in-page blob
   download with a unique filename.
5. Wait for the file in `~/Downloads`, copy it to the requested output file, and
   then copy to `Videos/` or Nutstore.

## Tools And Scripts

- `scripts/xyq_chrome/launch_chrome.sh`: starts the persistent logged-in Chrome
  profile with remote debugging enabled.
- `scripts/xyq_cdp_browser.py`: lists pages, navigates/reloads tabs, clicks,
  screenshots, uploads images, fills prompts, and runs DOM checks.
- `scripts/xyq_chrome/watch_thread_dom_download.py`: polls thread status,
  detects videos, handles protected media URLs, downloads MP4s, and copies them.
- `ffmpeg`: compresses oversized image references and extracts visual frames.
- `ffprobe`: verifies final dimensions, duration, size, and streams.
- `git`: commits prompt/docs/tooling changes after each successful edit.

## Verification Example

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=width,height,codec_name \
  -of json Videos/result.mp4
```

```bash
ffmpeg -y -loglevel error -i Videos/result.mp4 \
  -vf "select='eq(n,20)+eq(n,180)+eq(n,330)',scale=480:-1,tile=3x1" \
  -frames:v 1 outputs/run/contact_sheet.jpg
```

## Common Failure Causes

- Normal Chrome is visible but has no remote debugging endpoint; relaunch the
  controlled profile before upload/submission.
- The Xiaoyunque SPA is blank until same-tab address reload.
- The model dropdown can show both `Seedance 2.0 Fast` and `Seedance 2.0 Fast VIP`;
  the visible active model must not include `VIP`.
- The submit arrow moves after attachments expand the composer; re-query its
  rectangle before clicking.
- The queue can take 30-50 minutes; credits may drop before the status changes
  from queue to `生成中`.
- A visible video can appear before direct download works; use browser-context
  fetch/blob download rather than retrying external HTTP blindly.
