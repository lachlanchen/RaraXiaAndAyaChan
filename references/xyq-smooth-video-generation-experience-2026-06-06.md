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

5. If the old thread is stale or already completed, use the page `创作` /
   new-session control in the same controlled tab, then record the new thread
   URL. Avoid accumulating extra tabs.
6. Set the pre-submit contract and prove it before generation:

- `沉浸式短片`
- normal `Seedance 2.0 Fast`, no `VIP` label
- `15秒`
- `4:3` ratio unless the user requests another ratio
- all required image references uploaded, normally the seven-image set:
  words card, robot `庄子`, LightMind glasses, patchwork notebook, `R1`,
  `R3`, and `Trio`
- prompt contains `不要字幕，不要生成任何字幕、说明文字、下三分之一文字或画面文字。`
- prompt contains no local filesystem paths or filenames; use uploaded-image
  labels such as `图1` through `图7`

7. The compact ratio toolbar may only show `比例`; open the dropdown and check
   the active item or tooltip, for example `比例: 4:3`.
8. Upload images through `upload-images-verify`; wait until every upload card is
   success. One stuck `uploading` card keeps the submit button disabled.
9. Fill the prompt with `type-prompt`, not only DOM value replacement. The
   prompt should describe references by upload order, not by local path.
10. If JavaScript `.click()` does not submit, use a real coordinate click on the
   enabled arrow button after verifying its current rectangle.
11. Watch the submitted thread with `watch_thread_dom_download.py`.

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
- Local image paths are only for the upload command. If paths are pasted into
  the prompt, the model may treat them as visible text or confusing story
  content. Run `rg -n '/home|ProjectsLFS|artifacts|\.png|\.jpg|\.jpeg'
  references/prompts/PROMPT.md || true` before submission.

## 2026-06-07 Driver And Login Check

For the Mars 2D atom chip factory run, the correct controlled Chrome endpoint
was still:

```text
http://127.0.0.1:9222
```

The active CDP page was:

```text
Page ID: 1C53666076DB42C93A3CD8E44BDB6D07
Title: 小云雀网页版
URL: https://xyq.jianying.com/home?tab_name=integrated-agent&agent_name=pippit_video_part_agent&thread_id=6191b607-cd9a-4c2e-a980-87e9e4496874
```

Login was confirmed from visible page text:

```text
Account: user40912720974
Membership: 基础会员
Credits: 707
```

Reusable check:

```bash
curl -fsS http://127.0.0.1:9222/json/version
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py bring-to-front PAGE_ID
scripts/xyq_cdp_browser.py visible PAGE_ID
scripts/xyq_cdp_browser.py eval PAGE_ID \
  "(() => ({url: location.href, title: document.title, text: document.body.innerText.slice(0, 2000)}))()"
```

Problems observed:

- The visible page could be logged in even when the compose toolbar was partly
  hidden or summarized as `Auto`; use DOM probes plus screenshots before
  submitting.
- Navigating to the compose URL can create a fresh `thread_id`. Record the
  final URL after navigation and again after submit.
- The submit arrow stays disabled until prompt text and uploads are fully
  accepted. Re-check upload state and button class before clicking.
- Do not open a new tab just to recover loading. Reload the same controlled tab
  with `navigate` or `Ctrl+L` then `Enter`.
- Do not use the Xiaoyunque API for these browser-first runs unless explicitly
  requested.

Detailed runbook for the successful seven-image Mars chip factory video:

```text
references/xyq-mars-chip-browser-run-2026-06-07.md
```

Detailed runbook for the corrected seven-image upload-only/no-path prompt:

```text
references/xyq-uploaded-images-no-path-workflow-2026-06-09.md
```
