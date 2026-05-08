# 2026-05-09 XYQ Video Generation and UI Automation Log

This note records the recent user prompts, operations, tools, code patterns, failed attempts, and final working solutions for two related tasks:

- VoidAbyss Xiyouzhiyuan Studio layout: 50/50 draggable left/right split.
- Xiaoyunque/XYQ video generation: select/apply asset, submit generation, poll, extract video, download artifact.

## User Prompts Captured

```text
make the webapp half half left and right and the separator can be moved left and right
```

```text
maybe you can mix use of element selection like selenium with your current method? you needn't to hard code

you now already opened the assets library and you just select one or two and then click yingyong/applay
```

```text
yes you selected and plz click the submit button and generate video
```

```text
and document all your operations my prompts into references/

and all your code, tools, scripts, methods and trial and errors and the final successful solutions
```

## Repository/UI Work: Draggable Studio Split

Changed file:

- `scripts/xiyouzhiyuan_studio.py`

Commit:

- `bd67f4f8a Add draggable Xiyouzhiyuan studio split`

Tools used:

- `apply_patch` for code edits.
- `python -m py_compile scripts/xiyouzhiyuan_studio.py` for syntax verification.
- `./scripts/run-xiyouzhiyuan-studio-tmux.sh restart` to restart only the Studio webapp.
- `curl http://127.0.0.1:8799/` to verify the served HTML included the new split elements.

Final behavior:

- Desktop `main` now starts with a 50/50 split between Thought Pipe and PDF viewer.
- A vertical divider is inserted between the panes.
- The divider can be dragged horizontally with pointer events.
- Keyboard support exists on the divider:
  - Left/right arrow: adjust by 3%.
  - Home/End: jump to 35%/65%.
  - Enter/Space: reset to 50%.
- Split width is persisted in `localStorage` key `xiyouzhiyuanStudioLeftPane`.
- Mobile keeps the existing stacked layout and hides the resizer.

Core implementation pattern:

```js
function setSplitPercent(percent, persist = true) {
  const safePercent = clamp(Number(percent) || 50, 28, 72);
  $("workspace").style.setProperty("--left-pane", `${safePercent}%`);
  if (persist) localStorage.setItem(splitStorageKey, String(safePercent));
}

function resizeSplitFromClientX(clientX) {
  const workspace = $("workspace");
  const rect = workspace.getBoundingClientRect();
  const dividerWidth = $("splitResizer").getBoundingClientRect().width || 12;
  const minLeft = Math.min(300, rect.width * .35);
  const minRight = Math.min(360, rect.width * .38);
  const leftPx = clamp(clientX - rect.left, minLeft, rect.width - minRight - dividerWidth);
  setSplitPercent((leftPx / rect.width) * 100);
}
```

Trial/error:

- A headless Chrome screenshot command stalled on the live page, likely because the page/event stream stayed active. It was stopped and replaced with HTML inspection via `curl` plus Python syntax checks.
- The Studio tmux launcher resolved the repo through `/home/lachlan/ProjectsLFS/VoidAbyss`, which is a symlink to `/home/lachlan/Documents/VoidAbyss`; both paths point to the same files.

## XYQ Video Generation Automation

Skill consulted:

- `xyq-nest-skill`
- File read: `/home/lachlan/.agents/skills/xyq-nest-skill/SKILL.md`

Browser environment:

- Active Chrome had remote debugging enabled:
  - `--remote-debugging-port=9222`
  - profile path visible in process list: `/home/lachlan/.cache/xyq-chrome`
- CDP endpoint:
  - `http://127.0.0.1:9222/json/list`

Main tools used:

- Chrome DevTools Protocol over `websocket-client`.
- Python standard library: `json`, `urllib.request`, `itertools`, `time`, `pathlib`, `subprocess`.
- CDP methods:
  - `Runtime.evaluate`
  - `Page.bringToFront`
  - `Input.dispatchMouseEvent`
  - `Page.reload`
- `curl` for downloading the final signed MP4 URL.
- `ffprobe` for checking duration, size, codecs, and dimensions.

No Selenium package was installed in this Python environment. Instead, the same idea was implemented directly through CDP: inspect DOM, locate elements by text/class/role, and click their real centers. This avoided hard-coded screen coordinates.

## XYQ Browser Tabs Found

The useful tabs were discovered from:

```bash
curl -fsS http://127.0.0.1:9222/json/list
```

Important tabs:

- `6F1A89EC31D145D87AD9753CF116F027`
  - XYQ home tab with 6 attached reference assets.
  - First submit attempt came from this tab.
- `90E1FE5E869995D6261509C42B31CAB4`
  - XYQ home tab with asset-library drawer open and one selected asset.
  - Final successful submit came from this tab.
- `2B19D4226C99828F5D7811A352B5B432`
  - Existing XYQ novel/script detail tab, not used for final generation.

## DOM Inspection Method

Visible elements were listed by evaluating JavaScript in each XYQ tab:

```js
(() => {
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== "hidden" && s.display !== "none";
  };
  return [...document.querySelectorAll("button,[role=button],a,input,textarea,[contenteditable=true],.semi-button")]
    .filter(visible)
    .map((el, i) => {
      const r = el.getBoundingClientRect();
      return {
        i,
        tag: el.tagName,
        text: (el.innerText || el.value || el.getAttribute("aria-label") || el.title || el.placeholder || "").trim().slice(0, 80),
        cls: String(el.className).slice(0, 80),
        x: Math.round(r.x),
        y: Math.round(r.y),
        w: Math.round(r.width),
        h: Math.round(r.height),
        disabled: !!el.disabled || el.getAttribute("aria-disabled")
      };
    });
})();
```

## First Attempt and Failure

Action:

- Found an enabled XYQ `createButton` in tab `6F1A89EC31D145D87AD9753CF116F027`.
- Clicked through CDP using `Input.dispatchMouseEvent`.

Result:

- The UI submitted a thread:
  - `815ad9e4-9dcf-43b1-94fd-c73d7e15350f`
- The task did not generate video.
- XYQ reported:

```text
哎呀，本次任务积分不够啦~ 本次任务需要消耗150积分，若需获得更多积分请通过下述路径～
```

Reason:

- That setup used `15s` with a reference-video mode at `10` points/sec, requiring 150 points.
- The account initially showed 92 points.

Safety decision:

- I did not click recharge, purchase, upgrade, or any payment button.
- The recharge modal was observed only as a result of the insufficient-points flow.

## Successful Solution

The other XYQ tab already had an asset library drawer open with a selected asset and a visible `应用` button.

Steps:

1. Bring tab `90E1FE5E869995D6261509C42B31CAB4` to front.
2. Click the visible `应用` button by DOM text.
3. Wait for the asset drawer to close/apply.
4. Click the enabled `createButton`.
5. XYQ created a new integrated-agent thread:
   - `9bc74944-ae43-463b-ad40-d9427c72e1a1`
6. Poll page text and media elements.
7. The UI initially stayed at:

```text
生成中，大约还需1分钟
```

8. After several polls, force a page reload through `Page.reload`.
9. Reload revealed the completed result:
   - status lines included `0:15` and `00:15`
   - a `video` element exposed a signed MP4 URL.
10. Download the MP4 with `curl`.
11. Verify with `ffprobe`.

Final local artifacts:

- `outputs/xyq/hongkong_night_snack_20260509_065950.mp4`
- `outputs/xyq/hongkong_night_snack_20260509_065950.json`

Video verification:

- Duration: about `15.1s`
- Size: about `12 MB`
- Video: H.264, 30 fps
- Resolution: `836x1112`
- Audio: AAC stereo

## Successful Click Pattern

Reusable Python/CDP pattern:

```python
def click_center(selector_expr, label):
    info = eval_js(f"""
(() => {{
  const el = {selector_expr};
  if (!el) return {{ok:false, reason:'not found', label:{json.dumps(label)}}};
  el.scrollIntoView({{block:'center', inline:'center'}});
  const r = el.getBoundingClientRect();
  return {{
    ok: true,
    label: {json.dumps(label)},
    x: r.left + r.width / 2,
    y: r.top + r.height / 2,
    text: (el.innerText || el.getAttribute('aria-label') || el.title || '').trim(),
    cls: String(el.className)
  }};
}})()
""")
    if not info or not info.get("ok"):
        return False
    call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": info["x"], "y": info["y"], "button": "none"})
    call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": info["x"], "y": info["y"], "button": "left", "clickCount": 1})
    call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": info["x"], "y": info["y"], "button": "left", "clickCount": 1})
    return True
```

Selectors used:

```python
apply_selector = "[...document.querySelectorAll('button,[role=button]')].find(el => (el.innerText||'').trim() === '应用')"

create_selector = "[...document.querySelectorAll('button')].find(el => String(el.className).includes('createButton') && !el.disabled && el.getAttribute('aria-disabled') !== 'true')"
```

## Successful Polling and Extraction Pattern

After submit:

```js
(() => {
  const text = document.body.innerText || "";
  const lines = text.split("\n").map(s => s.trim()).filter(Boolean);
  const media = [...document.querySelectorAll("video,source,a,img")]
    .map((el) => ({
      tag: el.tagName,
      src: el.currentSrc || el.src || el.href || "",
      href: el.href || "",
      text: (el.innerText || el.alt || el.title || "").trim().slice(0, 120),
      cls: String(el.className).slice(0, 80)
    }))
    .filter(x => x.src || x.href || x.text);
  return {
    url: location.href,
    status: lines.filter(l => /(生成中|大约还需|完成|失败|错误|下载|重新生成|积分|2026\/5\/9|0:15)/.test(l)).slice(-30),
    media: media.filter(m => /(mp4|video|download|tos|byte|capcut|jianying)/i.test(m.src + m.href + m.text)).slice(-30)
  };
})();
```

The final MP4 URL came from:

```js
(() => {
  const videos = [...document.querySelectorAll("video,source")]
    .map(el => el.currentSrc || el.src || "")
    .filter(Boolean);
  return videos.find(url => url.includes("video_mp4") || url.includes(".mp4") || url.includes("download=true")) || "";
})();
```

The full signed URL is intentionally not copied into this Markdown because it is temporary and sensitive-ish. The saved metadata file contains the exact URL observed at download time.

## Download and Verification Commands

Download command pattern:

```bash
curl -L --fail --retry 3 --connect-timeout 20 --max-time 600 \
  -o outputs/xyq/hongkong_night_snack_20260509_065950.mp4 \
  "<signed_mp4_url_from_video_element>"
```

Verification command:

```bash
ffprobe -v error -show_entries format=duration,size -show_streams -of json \
  outputs/xyq/hongkong_night_snack_20260509_065950.mp4
```

## API Attempt and Limitation

I checked the `xyq-nest-skill` API path:

- `submit_run.py`
- `get_thread.py`
- `download_results.py`

But `XYQ_ACCESS_KEY` was not present in the shell environment at that time:

```bash
env | rg "^XYQ_"
```

returned no usable key. Therefore the browser/CDP path was used instead of the skill API.

## Future Runbook

1. Prefer CDP selector/text automation over fixed screen coordinates.
2. Use `http://127.0.0.1:9222/json/list` to find active XYQ tabs.
3. Inspect visible DOM elements before clicking.
4. Avoid clicking any payment/recharge/upgrade buttons.
5. If submit fails due to points:
   - reduce duration,
   - remove expensive reference-video mode,
   - use a lower-cost model/path,
   - or wait for the user to handle points manually.
6. If generation appears stuck but not failed:
   - poll visible text and `video/source` elements,
   - reload once with `Page.reload`,
   - re-check media elements.
7. Save results under `outputs/xyq/`.
8. Save a metadata JSON beside every downloaded media artifact.
9. Verify media with `ffprobe`.

## Important Outcome

Final successful result:

```text
Thread: 9bc74944-ae43-463b-ad40-d9427c72e1a1
Local MP4: outputs/xyq/hongkong_night_snack_20260509_065950.mp4
Local metadata: outputs/xyq/hongkong_night_snack_20260509_065950.json
```

The first failed submit is also useful for audit:

```text
Thread: 815ad9e4-9dcf-43b1-94fd-c73d7e15350f
Failure: insufficient points for a 150-point run
```
