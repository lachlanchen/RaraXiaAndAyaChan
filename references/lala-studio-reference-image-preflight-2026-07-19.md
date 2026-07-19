# Lala Studio Reference Image Preflight

Lala Studio now supports two reusable image outputs before Xiaoyunque video generation:

1. A fresh physical multilingual word card.
2. An episode-specific cinematic scene keyframe.

The **Produce** workspace provides an explicit scene-image toggle, visual brief, and independent source-reference selector. The image job runs before browser upload, previews both PNGs, caches them by a content fingerprint, and appends the scene keyframe after the normal Xiaoyunque references.

## Text Reliability

Image-model text must not be accepted as authoritative. The first trial copied the old card word even though the requested episode word had changed. The corrected workflow therefore generates the physical card body, then uses Lala Studio's deterministic renderer to place the canonical English, Japanese, furigana, and Chinese strings on the inner display.

```bash
studio/scripts/render_word_card_text.sh BASE.png FINAL.png word-card-spec.json
```

## Visible Operation

```bash
cd studio
node tools/lala-studio-browser.mjs production \
  --message "First generate a cinematic scene keyframe, then prepare this 15 second video" \
  --operation references \
  --video-assets word-card,raraxia,ayachan \
  --scene-assets raraxia,ayachan
```

This controller action manipulates the visible Studio UI. It does not submit a Xiaoyunque video.

`--video-assets` controls the files uploaded for the final video independently
from `--scene-assets`, which controls only the sources used to create the scene
keyframe. After either selection changes, the controller rebuilds the video
prompt through the visible Studio UI and blocks submission if preflight fails.

## 2026-07-19 Result

- Story: [`stories/2026-07-19-story-20260719120341.md`](stories/2026-07-19-story-20260719120341.md)
- Scene: [`images/2026-07-19-star-palace-harbor/scene-reference.png`](images/2026-07-19-star-palace-harbor/scene-reference.png)
- Word card: [`images/2026-07-19-star-palace-harbor/word-card-harbor.png`](images/2026-07-19-star-palace-harbor/word-card-harbor.png)

The video run uploaded six real files: the generated word card, Zhuangzi robot,
RaraXia, Aya Chan, Sasa Kun, and the generated scene keyframe. It used one paid
submission with Seedance 2.0 Mini 体验版 at 15 seconds and 16:9. Do not retry a
successful paid run only because a requested cast member is hard to see. For the
next episode, strengthen the positive composition instruction so Sasa Kun and
Zhuangzi are both visibly staged in at least one clear shot.

## Subtitle And Publish Recovery

The default ASR produced unrelated speech and incorrect timing. An independent
word-timestamp transcription recovered two spoken lines, and LazyEdit accepted
their exact timing through its validated `replace_timing` correction path. The
final publish master used portrait blur-fill, a top-right logo, and the normal
English/Japanese/Chinese subtitle renderer with Japanese ruby and Chinese
pinyin. The inspected ZIP and master MP4 had the same SHA-256.

All four targets reached terminal success: Shipinhao, YouTube, Instagram, and
Douyin. Metadata was regenerated from the short viewer-facing context file in
`references/prompts/`, not copied from the full storyboard. A stopped draft
publish must not be treated as a public failure when a later corrected session
has already completed successfully.
