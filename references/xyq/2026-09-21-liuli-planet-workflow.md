# Liuli Planet Sunset Workflow

Story: [在另一颗星球看日落](../prompts/2026-09-21-liuli-planet-sunset-30s.md).
Publication context: [context](../publish/2026-09-21-liuli-planet-context.md).

## Preparation

- Reused the accepted scene PNG and new `planet / 惑星 / わくせい / 行星`
  learning-card PNG. Original files and persistent image previews were retained.
- Used the existing signed-in browser and created this episode through its
  `创作` button. All later steps remain in the same episode thread.
- Uploaded eight actual files in the documented order; all eight attachment
  cards reported `data-status=ready`. No Trio or private human portraits.
- The broad upload helper counted unrelated gallery images. Verified the actual
  `attachment-preview-card` elements and screenshot instead of trusting its
  generic image count.
- Closed the membership promotion overlay before working.
- Inspected preferences: selected Mini trial model, normal mode, 4:3; changed
  smart duration to custom 30 seconds. Automatic generation countdown was off;
  model-change confirmation was on.

## Storyboard Preflight

Three shots of 10 seconds each, sequential last-frame continuity, with a pause
after each shot for inspection. Mini trial UI showed 4 credits per second;
the three-shot estimate was 120 credits.

Inspected the actual storyboard preview, not only the assistant's summary.
The per-shot image labels differ from the initial upload order; its thumbnail
lists correctly map the scene, individual cast, glasses, card and notebook.
Each shot has two corresponding speaker voice references. The final shot
includes the original notebook image. The first includes the new learning card.

The browser header and assistant balance differed, so final cost accounting
must use the credit ledger rather than an old header or assistant claim.

## Tools

Used `scripts/xyq_cdp_browser.py` for `list-pages`, `click-text`, `click`,
`eval`, `upload-images-verify`, `set-prompt`, and `screenshot`. DOM inspection
checked controls and attachment status. Screenshots and private runtime details
stay in the ignored task folder.

The published Markdown contains the clean prompt and relative asset paths in
separate sections. Only the prompt section is sent to Xiaoyunque:

```bash
python scripts/xyq_cdp_browser.py --cdp-url "$XYQ_CDP" set-prompt "$PAGE_ID" \
  <(sed -n '/^制作30秒/,/^先展示.*暂停供检查。/p' \
    references/prompts/2026-09-21-liuli-planet-sunset-30s.md)
```

## Shot Review And Download

All three shots passed full decode and contact-sheet review. The first establishes
the four correct figurine identities and scenery; the second visibly shows
Sasa's jump, float, catch by Zhuangzi and the couple's laughing reaction. The
third shows Aya taking a photo with the glasses, a photo in the patchwork
notebook, the four companions seated together, and the sunset pullback.
Small prop/logo text was not consistently legible; character identities and
the main actions were accepted without spending credits on a retry.

The preview video has an AI corner label. Opening the exact resource card and
using its official **Download** control produced a clean included export, as
in the previous episode. No watermark masking or generation retry was used.
Keep previews and official exports separately. Native exports are 966x720,
approximately 10.08 seconds per shot; do not force a resize merely to make the
source dimensions mathematically 4:3.

One direct preview download was slow but completed. Official browser downloads
were quicker. An old multi-gigabyte `.crdownload` from a different date was
unrelated and left untouched; do not let any arbitrary partial download block
this episode's complete file.

The final refreshed ledger showed exactly three 40-credit Mini trial charges:
120 credits total, balance 56. It also showed 66 expired daily credits,
which explained the stale initial header. Music and merge added no visible
ledger charge at the final check.

## Status

All three shots accepted, each generated once. Selected `合成最终成片` and
clicked `继续` in the same thread. The final `output.mp4` was downloaded from
the resource panel using its official Download button. Its browser filename
was recorded before copying; unrelated older downloads were not substituted.

- Source: `Videos/liuli-planet-sunset-2026-09-21/liuli_planet_sunset_30s_2026-09-21.mp4`.
- Duration: 30.266666 seconds; H.264 968x720 at 30 fps; stereo AAC.
- Size: 16,902,176 bytes.
- SHA-256: `ffcba707a311e4326ac7d8e3adfff060c21df2ca1f5bea6f565f54285987aa85`.
- Full decode and final contact-sheet checks passed. No visible generated
  subtitle or platform corner mark appeared in the inspected final frames.
- Copied to the configured Nutstore LalaChan project folder under this episode
  date. A local copy is verified; cloud acknowledgement is not yet claimed.
- LazyEdit upload created video `582`; publication finished on four platforms.
  Subtitle recovery and the remaining Japanese token caveat are documented in
  the [publication record](../publish/2026-09-21-liuli-planet-publication.md).
