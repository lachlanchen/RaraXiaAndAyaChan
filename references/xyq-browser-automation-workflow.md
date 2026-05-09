# Xiaoyunque Browser Automation Workflow

This records the browser-control work for 小云雀.

## What Happened In This Session

The already-open Chrome tab was visible and controllable through X11 screenshots and clicks. The target window title was:

```text
小云雀网页版 - Google Chrome
```

The target URL was:

```text
https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=e8217789-9938-4ebc-9e2f-f63a26a8db82&source=home_prompt&entrance_from=home
```

The external-link SVG provided by the user matched the visible `lucide-external-link` icon in the 小云雀 page. Clicking the visible icon opened a non-destructive video preview modal, confirming the page could be controlled at the UI level.

## Why The Existing Chrome Could Not Be CDP-Attached

The running Chrome process was launched as:

```text
/opt/google/chrome/chrome
```

It did not include:

```text
--remote-debugging-port=9222
```

Chrome DevTools Protocol and ChromeDriver-style attachment require the browser to be started with a remote-debugging port. A normal already-running Chrome tab cannot be attached later through CDP.

## Reusable CDP Launch

Use the controlled launch script:

```bash
scripts/xyq_chrome/launch_chrome.sh "https://xyq.jianying.com/home?tab_name=integrated-agent"
```

It launches Chrome with:

```bash
--remote-debugging-port=9222
--remote-allow-origins=http://127.0.0.1:9222
--user-data-dir=$HOME/.cache/xyq-chrome
```

The `--user-data-dir` preserves login state for future automated sessions.

## Reusable Driver Identity

For later Xiaoyunque work, reuse the same controlled driver instead of opening a normal Chrome tab:

```text
CDP endpoint: http://127.0.0.1:9222
Profile: /home/lachlan/.cache/xyq-chrome
Launch script: scripts/xyq_chrome/launch_chrome.sh
Attach helper: scripts/xyq_chrome/xyq_cdp.py
```

Check whether the driver is still alive:

```bash
curl -fsS http://127.0.0.1:9222/json/version
scripts/xyq_chrome/xyq_cdp.py --state
ps -eo pid,ppid,stat,etime,cmd | rg 'remote-debugging-port=9222|xyq-chrome'
```

If it is not alive, restart it:

```bash
scripts/xyq_chrome/launch_chrome.sh \
  "https://xyq.jianying.com/home?tab_name=integrated-agent"
```

Log in once in this profile. The login is stored under `/home/lachlan/.cache/xyq-chrome`, so later CDP runs can attach directly.

## Reusable CDP Tool

Use:

```bash
scripts/xyq_chrome/xyq_cdp.py
```

For quick control of an already-open Xiaoyunque tab by explicit page id, use:

```bash
scripts/xyq_cdp_browser.py
```

This helper was added on `2026-05-09` for the bottom `+ -> 从资产库选择` workflow. It can list tabs, inspect visible controls, click coordinates, take screenshots, run JavaScript probes, and set the Tiptap prompt safely.

Print page state:

```bash
scripts/xyq_chrome/xyq_cdp.py --state
```

Fill the visible prompt composer without submitting:

```bash
scripts/xyq_chrome/xyq_cdp.py --fill-prompt-file references/prompts/example.md
```

Click an indexed `lucide-external-link` icon:

```bash
scripts/xyq_chrome/xyq_cdp.py --click-external-link 0
```

Run a custom JavaScript probe:

```bash
scripts/xyq_chrome/xyq_cdp.py --eval "location.href"
```

List current CDP pages with the new helper:

```bash
scripts/xyq_cdp_browser.py list-pages
```

Inspect the current composer controls:

```bash
scripts/xyq_cdp_browser.py visible PAGE_ID
```

Set a prompt without corrupting text:

```bash
scripts/xyq_cdp_browser.py set-prompt PAGE_ID references/prompts/example.md
```

Select Xiaoyunque modes from the home composer:

```bash
scripts/xyq_chrome/xyq_cdp.py --url "https://xyq.jianying.com/home?tab_name=home" --select-mode agent
scripts/xyq_chrome/xyq_cdp.py --url "https://xyq.jianying.com/home?tab_name=home" --select-mode duanpian
scripts/xyq_chrome/xyq_cdp.py --url "https://xyq.jianying.com/home?tab_name=home" --select-mode long2
```

Use the dedicated short-drama Agent workspace directly:

```bash
scripts/xyq_chrome/xyq_cdp.py \
  --url "https://xyq.jianying.com/novel/list?enter_from=small_tool" \
  --state
```

Run the non-destructive mode smoke test:

```bash
scripts/xyq_chrome/test_modes.py --output references/xyq-mode-test-results.md
```

Prepare the dedicated short-drama Agent from the saved ChatGPT draft:

```bash
scripts/xyq_chrome/prepare_duanju_from_chatgpt.py
```

This uploads `Lala-Aya-Sasa-draft/duanju-agent-chatgpt-sushi.txt` to the `/novel/list` workspace, reuses `Trio.png` as the default character reference asset, waits for `剧本解析`, and does not submit generation.

Send a new synopsis into the existing ChatGPT script thread and save the answer:

```bash
scripts/xyq_chrome/chatgpt_thread_prompt.py \
  --prompt-file Lala-Aya-Sasa-draft/2026-05-09-today-script-synopsis.md \
  --output Lala-Aya-Sasa-draft/2026-05-09-hong-kong-rainy-tea-restaurant-chatgpt.md
```

This attaches to:

```text
https://chatgpt.com/c/69fc0bcd-4f2c-83ea-9117-46fc128a2496
```

It fills the visible ChatGPT composer, sends the prompt, waits for the new assistant message to stop changing, then writes a Markdown copy containing both the prompt and the response.

## Attach Test Result

The controlled Chrome launch was tested on `2026-05-08` with the thread URL above. After startup, Chrome listened on:

```text
127.0.0.1:9222
```

The CDP state probe succeeded:

```bash
scripts/xyq_chrome/xyq_cdp.py --state
```

Because the controlled profile was new, 小云雀 redirected to:

```text
https://xyq.jianying.com/login?redirect_url=%2Fhome%3Ftab_name%3Dintegrated-agent
```

Log in once in the controlled profile before using prompt-fill automation on the real workspace page.

After login, the same CDP state probe attached successfully to:

```text
https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=c883f4a0-8ffb-43ff-bf1a-2a8c1fffee82
```

It found one visible prompt composer and the page buttons, confirming the controlled driver profile is ready for prompt-fill automation.

## X11 Fallback Used For The Existing Tab

Because the existing Chrome tab lacked CDP, X11 was used for non-destructive tests:

- Enumerated windows with `python-xlib`.
- Focused the 小云雀 Chrome window by X11 window id.
- Captured screenshots with `window.get_image(...)` and Pillow.
- Sent harmless keys/clicks with `Xlib.ext.xtest`.
- Confirmed the external-link icon opened a preview modal.

This is useful for inspection, but CDP is the preferred method for robust prompt filling and state checks.

## Recommended Future Workflow

1. Launch 小云雀 with `scripts/xyq_chrome/launch_chrome.sh`.
2. Log in once in that controlled profile if needed.
3. Use `scripts/xyq_chrome/xyq_cdp.py --state` to confirm the page and editable fields.
4. Use `--fill-prompt-file` to fill generated prompts.
5. Submit manually or add an explicit submit helper only after verifying the send button selector on the page.

For reference-video generation through the API and browser driver together, use:

```bash
scripts/xyq_chrome/reference_video_until_credit.py \
  --video path/to/reference.mp4 \
  --thread-id THREAD_ID \
  --json-log outputs/xyq-reference-video-run.json
```

This uploads the reference file, fills the visible browser composer for traceability, submits the run through the Xiaoyunque skill API, auto-confirms once when asked, and stops on an insufficient-credit block or terminal run state.

For the current preferred web UI reference-video path, see:

```text
references/xyq-asset-library-reference-workflow.md
```

Important distinction:

- Bottom `+ -> 从资产库选择` attaches actual old generated videos as references.
- `@引用素材` is not the preferred path for old reference-video selection.
- Do not write UI steps into the prompt; attach the assets first, then keep the prompt focused on the story and `不要字幕`.
