# Xiaoyunque AgInTi Lab Continue And Download Log

Date: 2026-06-09  
Project: LALACHAN / RaraXiaAndAyaChan

This records the browser-only methods used to continue the current Xiaoyunque
video job and download the last completed result. No Xiaoyunque API submission
was used.

## Threads

30s long-video job, still queued after continuation:

```text
https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=520dd393-8af7-4c84-9f9b-f6f5c651a4ea&agent_name=pippit_nest_agent
```

15s short-film job, completed and downloaded:

```text
https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=3dc92cb6-18ea-46af-9347-7669aea5838b&agent_name=pippit_video_part_agent
```

## Tools Used

- `scripts/xyq_cdp_browser.py`: CDP page listing, navigation, screenshots,
  DOM inspection, typed chat reply, and button clicks.
- `scripts/xyq_chrome/watch_thread_dom_download.py`: browser-thread polling and
  video detection.
- `ffprobe`: final MP4 validation.
- Controlled Chrome/CDP endpoint: `http://127.0.0.1:9222`.

## Continue Step

The 30s job generated a storyboard and reference materials, then stopped for a
human confirmation:

```text
如符合预期我将继续生成视频。
```

Use real browser typing rather than direct DOM replacement, because React/Tiptap
may not enable the send button after raw DOM insertion.

Create an ignored temporary message file, for example
`outputs/xyq-2026-06-09-aginti-autonomous-lab-v2/continue-message.md`, with
exactly this content:

```text
继续生成视频。
```

Then type it into the current chat input:

```bash
scripts/xyq_cdp_browser.py type-prompt PAGE_ID \
  outputs/xyq-2026-06-09-aginti-autonomous-lab-v2/continue-message.md \
  --wait 0.3

scripts/xyq_cdp_browser.py click PAGE_ID SEND_BUTTON_X SEND_BUTTON_Y
```

In this run the send button rect was approximately `x=664,y=802,w=36,h=36`, so
the click point was `682 820`. After sending, the 30s thread advanced to:

```text
确认故事板和素材后生成分镜视频 (generate_shot_video)
进行中
```

Later status check:

```text
优先处理中（807/16447位），还需42分钟
```

## Download Step

The user asked to open a new tab to download the last video. A separate CDP tab
was opened for the earlier 15s thread, leaving the 30s job untouched.

```bash
python3 - <<'PY'
import json, urllib.parse, urllib.request
url = "THREAD_URL"
req = urllib.request.Request(
    "http://127.0.0.1:9222/json/new?" + urllib.parse.urlencode({"url": url}),
    method="PUT",
)
with urllib.request.urlopen(req) as r:
    print(r.read().decode())
PY
```

If Chrome creates `about:blank`, navigate that new page id explicitly:

```bash
scripts/xyq_cdp_browser.py navigate NEW_PAGE_ID "THREAD_URL"
```

The watcher detected completion and a visible `<video>` element:

```text
poll 101: points=377 status=完成 videos=1
```

Direct downloads from protected `everphoto` / `365yg` URLs failed with HTTP
errors. The reliable fallback was the page's own top-right `下载` button. Inspect
the page controls first:

```bash
scripts/xyq_cdp_browser.py eval PAGE_ID '(() => {
  const visible = el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== "none" && s.visibility !== "hidden";
  };
  return [...document.querySelectorAll("button,[role=button],a")]
    .filter(visible)
    .map((b, i) => ({
      i,
      text: (b.innerText || "").trim(),
      aria: b.getAttribute("aria-label"),
      cls: String(b.className).slice(0, 120),
      rect: (() => {
        const r = b.getBoundingClientRect();
        return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
      })()
    }));
})()'
```

In this run the reliable button was:

```text
text: 下载
rect: x=1600,y=120,w=70,h=36
```

Then click the button and check `~/Downloads`:

```bash
scripts/xyq_cdp_browser.py click PAGE_ID 1635 138
find ~/Downloads -maxdepth 1 -type f -name '*.mp4' -printf '%T@ %s %p\n' \
  | sort -nr | head
```

## Output

Downloaded file:

```text
/home/lachlan/Downloads/v03c76g10004d8k1e5qljhtd7s03.558.mp4
```

Copied file:

```text
/home/lachlan/ProjectsLFS/LALACHAN/Videos/aginti_autonomous_lab_microenvironment_15s.mp4
```

Validation:

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=width,height,codec_name \
  -of default=noprint_wrappers=1 \
  Videos/aginti_autonomous_lab_microenvironment_15s.mp4
```

Result:

```text
codec_name=h264
width=1112
height=836
codec_name=aac
duration=15.125000
size=21679271
```

## Lessons

- If Xiaoyunque asks for confirmation, reply in the current thread with a short
  natural message such as `继续生成视频。`.
- Use `type-prompt` for chat replies. Raw DOM insertion can leave the send
  button disabled.
- For long-video agent mode, completion can pause at storyboard/material review
  before video generation. Check the tail text before assuming failure.
- Direct `video.currentSrc` downloads may fail even when the browser plays the
  video. Prefer the visible page `下载` button when protected URLs fail.
- If a watcher process was started without a TTY, it cannot be interrupted with
  stdin. Stop it by PID before switching to manual page-download flow.
- Always verify the final MP4 with `ffprobe` and copy it to `Videos/`.
