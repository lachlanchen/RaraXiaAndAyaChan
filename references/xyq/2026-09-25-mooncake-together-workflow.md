# Mooncake Together: Generation And Review

Story and clean generation prompt:
[给你一个大月饼](../prompts/2026-09-25-mooncake-together-30s.md).

## Current Status

The initial 30-second plan required 120 credits against a balance of 116.
The user approved 29 seconds. All three clips completed once, using
9 + 10 + 10 seconds at 36 + 40 + 40 credits. The website merged them at zero
additional cost; the official download is 29.141 seconds. The refreshed account
balance is 0 credits, matching the 116-credit total. Download and local review
are complete. No publication was requested or performed. LocalVideoGen was
researched as a fallback, not started as a duplicate generation task. See the
[hybrid handoff](localvideogen-hybrid-handoff.md).

## Assets And Story

- Generated a new mooncake learning card using the original `words-card.jpg`
  as an image reference. Visually verified the four unlabeled lines:
  `mooncake / 月餅 / げっぺい / 月饼`.
- Generated one courtyard scene reference using the four individual character
  images and the new learning card. Reviewed all four identities and the robot
  chest mark. Both PNGs are preserved under the ignored episode asset folder.
- Opened both images in persistent viewers on the physical desktop, separate
  from the existing browser review desktop.
- The joke has one cause and payoff: too much filling becomes two mooncakes
  shared by the couple. Prepared snow-skin wrappers make immediate tasting
  plausible. Sasa stamps the pattern; Zhuangzi plates the mooncakes.
- The final scene includes Japanese, Chinese and English Mid-Autumn greetings.

## Browser Preflight

Reused the established signed-in Chrome and existing noVNC stack. Created the
new daily episode through `创作`, then kept all work in that episode.

Confirmed in the actual preferences UI:

- Agent workflow, not the duration-limited short-film mode.
- `Seedance 2.0 Mini 体验版`, selected via `aria-pressed=true`.
- `4:3`, normal mode, custom duration changed from `30` to `29` seconds after
  user approval.
- Displayed rate: 4 credits per second; revised total budget 116 credits.
- Eight actual uploaded files in the story document's order; every attachment
  reported `data-status=ready`. No Trio and no private portrait references.
- Automatic generation countdown off; model-change confirmation on.
- Included official AIGC-label-free export setting already enabled. Verify the
  final downloaded file; this setting alone does not prove a clean export.

Evidence stays under `outputs/xyq/2026-09-25-mooncake-together/`, including
preferences, attachment thumbnails, filled prompt and countdown settings.

## Tools And UI Notes

Used the existing `scripts/xyq_cdp_browser.py` commands: `eval`, `click`,
`click-text`, `screenshot`, `upload-images-verify`, and `set-prompt`.

Only the prompt section was sent to the website:

```bash
python scripts/xyq_cdp_browser.py --cdp-url "$XYQ_CDP_URL" \
  set-prompt "$PAGE_ID" \
  <(sed -n '/^制作30秒/,/^先展示.*暂停供检查。/p' \
    references/prompts/2026-09-25-mooncake-together-30s.md)
```

- Close the membership promotion dialog before interacting with controls.
- `click` accepts observed x/y coordinates, not a CSS selector.
- Some Radix menu/tab controls did not respond to a DOM `.click()`. A real
  CDP pointer click at the observed element center worked. Verify resulting
  selected state rather than assuming a successful helper call changed it.
- The upload helper includes unrelated gallery images in its generic evidence
  count. Check actual ready attachment elements and ordered thumbnails.
- In this layout, personal settings and `Agent 设置` are separate. The latter
  appears inside the episode and contains the automatic generation countdown.
- Disabling the countdown alone did not guarantee a separate cost card for a
  below-threshold task. The initial credit reminder threshold was 450; set it
  to 0 in Agent settings so later paid clips require a visible confirmation.
- The storyboard preview can remain on an older version after a correction.
  Compare the actual task payload and selected reference thumbnails, not just
  the preview title. Before shot 1, added the missing Sasa/robot individual
  references and removed a uniform body-proportion redesign instruction.
- A direct transfer from the second clip's inline-player URL stalled; a
  browser `fetch` attempt also failed. Opening `对话文件`, selecting the exact
  `shot_02.mp4` resource and clicking its official `下载` worked. The stalled
  transfer was stopped, with its partial file retained. Later clips and the
  final output used this official UI route directly.
- The header balance stayed at 116 during the conversation. Per-render charges
  showed 36, 40 and 40; refreshing after the completed download showed 0.

## Review Commands

Download the observed video URL from the exact episode result, preserving
each clip. `watch_thread_dom_download.download()` supports resumable transfers.
Do not select the first video element after multiple results exist, and do not
mistake a storyboard Markdown download for the finished video.

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,duration \
  -show_entries format=duration,size -of json "$CLIP"
ffmpeg -v error -i "$CLIP" -f null -
ffmpeg -v error -i "$CLIP" -vf 'fps=1,scale=400:-1,tile=3x3' \
  -frames:v 1 "$CONTACT_SHEET"
whisper "$CLIP" --model small --device cpu --language zh \
  --output_format json --output_dir "$ASR_DIR" --threads 4 --fp16 False
```

Use appropriate language detection or separate ranges for the multilingual
ending. ASR supports content review; its timestamps alone do not prove lip sync.
Shot 1's preview decoded fully, measured about 9.09 seconds at 966x720, showed
the four referenced characters, and ASR recognized `给你包个大的`. A brief
double-moon background artifact was retained rather than spending on a rerun.
The preview contains an AI corner label. Sampled official downloads and the
final export did not contain that corner label; no local masking was applied.

## Final Delivery

- Local file: `Videos/mooncake-together-2026-09-25/mooncake_together_trilingual_29s.mp4`.
- Nutstore-relative folder: `Projects/LalaChan/2026-09-25-mooncake-together/`.
- Three official original clips are preserved in the local `original-shots/`.
- Final: H.264, 968x720, 30 fps, 29.140998 seconds, AAC 44.1 kHz stereo,
  16,024,065 bytes. The UI selected 4:3; encoded dimensions are slightly wider
  than mathematically exact 4:3. Preserved the export rather than rescaling it.
- Full ffmpeg decode passed; the final contact sheet confirms the intended
  sequence and the four identities. No dialogue subtitles were generated.
- Original dialogue and environment sound retained. No extra music generation
  was requested after the budget was spent.
- Local and Nutstore-copy SHA-256:
  `8b491c16c4b9759ee0f6f48d3a3afbe98f5a7feeaa88d0029e9e44c4fbbb69bb`.
  This verifies the local sync-folder copy, not a separate cloud acknowledgement.

Review caveats: the opening briefly shows two moons, small card/logo lettering
drifts, and the final group shot resets Lala's mooncake to a partly wrapped
state. These are retained generation imperfections, not reasons to spend on an
unapproved rerun. Character identity and the main joke remain recognizable.

ASR recognized both Chinese story lines. Full-clip ASR translated the initial
Japanese greeting into Chinese, so the first three seconds were checked again
with Japanese recognition. It recognized `おめでとうございます` with an
imperfect kanji rendering of `中秋節`; the Chinese crop recognized `中秋快乐`,
and the English greeting was recognized as `Happy Mid-Autumn Festival`.
Preserved the original audio; do not replace it based on ASR orthography alone.

The same signed-in browser/noVNC stack remains available for review. It was
preexisting and shared; no additional GUI or model runtime was started. All
short-lived download/ASR tasks launched here have ended.
