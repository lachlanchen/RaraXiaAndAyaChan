# France Hanfu: Mini Normal-Mode Workflow

Story and submitted prompt: [Seine breeze](../prompts/2026-09-20-france-hanfu-30s.md).

## Scope

One approximately 30-second, 4:3 character video, using the cheapest suitable
visible ordinary model. This request covers generation and download, not
publication. The cast uses its fictional individual figurine references.

## Preparation

- Generated a fresh physical word-card reference from `words-card.jpg`:
  `breeze / そよ風 / 微风 / brise`, with `かぜ` above `風` and no language labels.
- Generated a Paris/Hanfu scene reference using the individual cast references.
  Aya wears pink/white Hanfu; Rara wears blue/white Hanfu. Sasa and Zhuangzi
  retain their own appearance.
- Inspected both generated PNGs and opened persistent desktop previews.
- Uploaded all eight files in the exact order in the story document. No Trio
  image or private human portrait was used.
- Checked actual attachment titles, upload status and progress. The broad
  upload helper's image count can include unrelated gallery images.

## Browser and Rendering

Reused the logged-in browser and its existing noVNC desktop. Created the new
story through the page's `创作` control, then kept all work in that one thread.

The actual toolbar showed `Seedance 2.0 Mini 体验版`, normal mode, 30 seconds,
4:3 and 120 credits. The prepared storyboard was 11 + 10 + 9 seconds.
Its first preview omitted the uploaded scene reference from the per-shot
reference lists. A short correction added that image to each shot while
retaining individual identity references. Selected sequential tail-frame
continuity.

The new interface did not present a separate paid-render confirmation button:
after the storyboard reply, the agent started the first shot within the
preflighted budget. Record the actual behavior rather than assuming the older
confirmation-card flow. Ordinary mode is not itself proof that rendering will
pause. Inspect settings and references before agreeing to the storyboard.

The agent paused after shot 1 as requested. Its downloaded contact sheet
confirmed the three characters appearing there had the correct identities and
Hanfu. The continuation explicitly reused shot 1 and authorized only the
remaining 10 + 9 seconds within the remaining 76 credits, followed by merging.

## Official Download

Settings > General offered `保存内容去除 AIGC 水印`. Enabled the included setting
before rendering. Its help text says it affects future generated results;
branding watermarks are a separate setting/benefit.

The first-shot preview URL returned a video with an `AI生成` corner label.
The resource panel's **Download** button returned a clean official export at
the same 966x720 resolution and 11.104-second duration. A sampled official
frame verified the label was absent. Both versions were preserved. The files
have different bitrates, so do not describe them as bit-identical exports.

Prefer the actual official download over a preview URL for final delivery.
No masking or paid regeneration is needed merely because the preview has a
label. Verify the exported file itself.

## Verification Tools

Use the existing `scripts/xyq_cdp_browser.py` commands for page inventory,
DOM inspection, screenshots, exact controls, prompt entry and file upload.
Read-only DOM state and the visible result card identify the active output;
do not select an arbitrary old download by modification time alone.

```bash
ffprobe -v error -show_entries stream=codec_type,width,height \
  -show_entries format=duration,size -of json "$VIDEO"
ffmpeg -v error -i "$VIDEO" -f null -
ffmpeg -v error -i "$VIDEO" \
  -vf 'fps=0.7,scale=384:-1,tile=4x2' -frames:v 1 "$CONTACT_SHEET"
```

Keep browser/profile details, screenshots containing account information,
signed download URLs and runtime logs in the ignored local run folder.

## Credit Evidence

The ledger confirms the first two video charges as 44 and 40 credits, both
explicitly labeled Mini trial. The initial header was stale by 60 credits:
the ledger identifies those 60 as the previous day's expired free credits,
not a charge for today's voice anchor. Final ledger: 44 + 40 + 36 = **120
credits**, remaining balance **176**. All three entries are Mini trial. No
paid rerender occurred.

## Final Delivery

- Output: `Videos/france-hanfu-seine-breeze-2026-09-20/france_hanfu_seine_breeze_30s.mp4`.
- 30.300 seconds, 968x720, 30 fps, H.264, AAC stereo 44.1 kHz.
- The selected UI ratio was 4:3; the platform's native export is slightly wider
  than exact 4:3. Kept the delivered image without another resize/re-encode.
- Official final download: 22,022,114 bytes. Full video/audio decode passed.
- Audio mean -22.0 dB, peak -1.3 dB; non-silent. No claim of word-perfect ASR
  verification is made for this generation-only run.
- Final contact sheet showed the intended figurine cast, Hanfu, Paris setting,
  fan gag, photo/notebook and picnic. No generated subtitle or platform corner
  label was visible in the sampled official export. Embedded AIGC provenance
  metadata remains intact.
- Minor limitations: the fan changes position across a cut, glasses disappear
  in the final wide picnic shot, and small card/logo lettering is not perfectly
  preserved. These did not cause an unauthorized paid retry.
- Copied the final video, scene PNG, word-card PNG and story into the local
  Nutstore `Projects/LalaChan/2026-09-20-france-hanfu` folder. Local source and
  destination SHA-256 match. This check does not assert a remote cloud receipt.
- SHA-256: `e8fdf248a0aa9a076d7ecdc578288e960aee341e349b805661575e0a3181ce92`.
- Raw shot previews, official clean shot exports, screenshots and the final
  contact sheet remain in the ignored task run folder. Source assets retained.
- Not published, not submitted to LazyEdit, and no new GUI stack was launched.
