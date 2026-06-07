# Xiaoyunque Mars Chip Factory Browser Run

Date: `2026-06-07`

This records the full browser-first Xiaoyunque workflow used to generate the
Mars 2D atom chip factory short video with the seven-image reference set.

## Result

Submitted through the logged-in Xiaoyunque web UI, not the API.

```text
Thread: https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=6ea1116d-382e-42e1-a1c7-81c46adf0a08&agent_name=pippit_video_part_agent
Title shown in history: 火星芯片工厂短片
Output: outputs/xyq-2026-06-07-mars-chip/mars_2d_atom_chip_factory_zhuangzi_15s.mp4
Copy: Videos/mars_2d_atom_chip_factory_zhuangzi_15s.mp4
Duration: 15.125s
Dimensions: 1112x836
Size: 7166049 bytes
Observed credits: 707 -> 632
```

## Reference Images

Use this exact order and wording for future prompts:

```text
1. words card 小白屏学习卡
   /home/lachlan/ProjectsLFS/LALACHAN/artifacts/images/2026-06-07T02-10-31-891Z/image.png

2. LazyingArtRobot，机器人庄子
   /home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png

3. LightMind AI 眼镜
   /home/lachlan/ProjectsLFS/LALACHAN/display.png

4. 拼皮笔记本
   /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png

5. 啦啦侠 服装参考
   /home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg

6. 飒飒君 服装参考
   /home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg

7. 啦啦侠 －－ 阿芽酱 －－ 飒飒君 三人角色参考
   /home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Prompt used:

```text
references/prompts/2026-06-07-mars-2d-atom-chip-factory-zhuangzi-duanpian-15s.md
```

## Browser Preconditions

Attach to the persistent controlled Chrome profile:

```bash
curl -fsS http://127.0.0.1:9222/json/version
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py bring-to-front PAGE_ID
scripts/xyq_cdp_browser.py visible PAGE_ID
```

Known-good page ID during this run:

```text
1C53666076DB42C93A3CD8E44BDB6D07
```

Login was visible as:

```text
user40912720974
基础会员
707
```

## Clean New Session

Problem: staying on an old integrated-agent thread can leave old prompt text,
old reference assets, or no usable upload input. The old thread upload attempt
failed with:

```text
no nodes for selector: input[type=file]
```

Solution: use the page's own left-side `创作` button to return to a fresh
home composer in the same controlled tab.

```bash
scripts/xyq_cdp_browser.py click PAGE_ID 90 103
scripts/xyq_cdp_browser.py wait PAGE_ID 5
scripts/xyq_cdp_browser.py list-pages
```

Expected URL after the click:

```text
https://xyq.jianying.com/home?tab_name=home
```

Do not open a new tab for this reset. Use the same logged-in controlled tab.

## Pre-Submit Contract

From the fresh home composer:

1. Click `沉浸式短片`.
2. Open the model dropdown.
3. If it defaults to `Seedance 2.0 Fast VIP`, switch to non-VIP
   `Seedance 2.0 Fast`.
4. Confirm `15秒`.
5. Open the ratio menu and confirm `4:3`.
6. Upload the seven references.
7. Type the saved prompt.
8. Submit only after the arrow button is enabled.

Important observed caveats:

- Xiaoyunque defaulted to `Seedance 2.0 Fast VIP`; this must be changed when
  the user asks for normal/non-VIP.
- The ratio toolbar may still display only `比例`. The reliable proof is the
  dropdown active item or tooltip text `比例: 4:3`.
- The submit arrow changes position when long prompts expand the composer.
  Re-query its rectangle before clicking.
- After submit, the button can become disabled while the URL still appears as
  `tab_name=home`. Do not spam-click. Wait and poll; the route changed to the
  new thread after processing.

## Upload Command

```bash
scripts/xyq_cdp_browser.py upload-images-verify PAGE_ID \
  artifacts/images/2026-06-07T02-10-31-891Z/image.png \
  LazyingArtRobot.png \
  display.png \
  patchwork-leather-notebook-luxury-clean-v2.png \
  R1.jpg.jpeg R3.jpg.jpeg Trio.png \
  --screenshot outputs/xyq-2026-06-07-mars-chip/after-upload-fresh.png \
  --timeout 180 --interval 3
```

Successful upload evidence included all seven filenames:

```text
image.png
LazyingArtRobot.png
display.png
patchwork-leather-notebook-luxury-clean-v2.png
R1.jpg.jpeg
R3.jpg.jpeg
Trio.png
```

## Prompt And Submit

```bash
scripts/xyq_cdp_browser.py type-prompt PAGE_ID \
  references/prompts/2026-06-07-mars-2d-atom-chip-factory-zhuangzi-duanpian-15s.md
```

The helper reported:

```text
createDisabled: false
createClass: createButtonReady
```

Submit by clicking the current create-button rectangle, not a stale coordinate.
In this run the visible arrow was around:

```text
x=1318 y=734 w=36 h=36
```

## Watch And Download

Use the browser watcher, not the API:

```bash
scripts/xyq_chrome/watch_thread_dom_download.py \
  --page-id PAGE_ID \
  --thread-url "https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=6ea1116d-382e-42e1-a1c7-81c46adf0a08&agent_name=pippit_video_part_agent" \
  --output-dir outputs/xyq-2026-06-07-mars-chip \
  --filename mars_2d_atom_chip_factory_zhuangzi_15s.mp4 \
  --copy-to Videos \
  --interval 15 \
  --max-polls 240
```

Queue behavior:

- The thread first showed `排队等待中 / 优先处理中`.
- Estimated time fluctuated heavily: about 29 minutes, then lower, then briefly
  much higher, then back down.
- Do not restart just because the estimate jumps. Continue watching unless the
  page shows a real failure.
- It eventually moved to `生成中` and then exposed one video element.

Download caveat:

Direct external HTTP download failed for the protected Everphoto media URL:

```text
candidate: ERR:HTTPError https://everphoto-media.jianying.com/...
```

The watcher solved it by fetching from the logged-in browser context:

```text
browser fetch: status 200, type video/mp4, length 7166049
browser download trigger: ok
```

## Verification

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height \
  -of json Videos/mars_2d_atom_chip_factory_zhuangzi_15s.mp4
```

Expected output:

```json
{
  "streams": [
    {"codec_name": "h264", "width": 1112, "height": 836},
    {"codec_name": "aac"}
  ],
  "format": {"duration": "15.125000", "size": "7166049"}
}
```

## Screenshots Captured

```text
outputs/xyq-2026-06-07-mars-chip/after-click-create.png
outputs/xyq-2026-06-07-mars-chip/after-select-duanpian.png
outputs/xyq-2026-06-07-mars-chip/model-dropdown.png
outputs/xyq-2026-06-07-mars-chip/ratio-dropdown.png
outputs/xyq-2026-06-07-mars-chip/after-upload-fresh.png
outputs/xyq-2026-06-07-mars-chip/after-prompt.png
outputs/xyq-2026-06-07-mars-chip/after-submit.png
```

## Future Checklist

- Start from the page `创作` button for a fresh composer.
- Select `沉浸式短片`, then immediately fix model if it says `VIP`.
- Confirm `4:3` from the ratio dropdown or tooltip, not only from prompt text.
- Upload references before typing prompt when the prompt mentions `图片1..7`.
- Verify all filenames in the composer before submit.
- Do not submit from an old thread or history item.
- Do not use the Xiaoyunque API unless explicitly requested.
- If media URL download fails, rely on browser-context fetch/blob download.
