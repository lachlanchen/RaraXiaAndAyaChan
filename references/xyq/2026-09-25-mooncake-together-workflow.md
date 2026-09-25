# Mooncake Together: Preparation And Resume

Story and clean generation prompt:
[给你一个大月饼](../prompts/2026-09-25-mooncake-together-30s.md).

## Current Status

Preparation completed; no paid video render submitted. Xiaoyunque explicitly
stopped at insufficient credits: 116 available versus an estimated 120 for
30 seconds. The planning response reports zero credits consumed. Await a
recharge or an explicit duration adjustment, then resume the same episode.
No video has been downloaded or published for this episode.

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
- `4:3`, normal mode, custom duration `30` seconds.
- Displayed estimate: 120 credits at 4 credits per second.
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

## Resume

Use the current `中秋手办月饼短片` conversation. After funds are available,
continue the existing 30-second plan; do not create another thread or select
the site's suggested 15-second compression without user approval. Inspect the
actual storyboard and per-shot cost before paid confirmation. Review the first
paid clip before subsequent clips. Preserve all outputs, use the official
download, and validate full decode, duration, audio and character identity.
Publishing is not part of the current request.
