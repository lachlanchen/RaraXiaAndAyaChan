# Mooncake Together Publication

## Verified Source

- Story: [context](2026-09-25-mooncake-together-context.md).
- Generation: [workflow](../xyq/2026-09-25-mooncake-together-workflow.md).
- Source: `Videos/mooncake-together-2026-09-25/mooncake_together_trilingual_29s.mp4`.
- Source SHA-256: `8b491c16c4b9759ee0f6f48d3a3afbe98f5a7feeaa88d0029e9e44c4fbbb69bb`.
- Source duration: 29.141 seconds. No further paid generation.

## Normal LazyEdit Processing

Video ID: 592. Shared story context was supplied to LazyEdit for subtitle
correction and metadata generation. The configured DeepSeek provider was reused.
The generated metadata uses the four characters' names and the Mid-Autumn story.
It was not manually replaced.

Full-clip ASR had overly early starts for the first two utterances. A separate
CPU Whisper word-timing pass on the first 12 seconds provided acoustic evidence
for these reviewed intervals: 4.48-5.70, 8.88-9.94, and 9.94-10.80 seconds.
The three later greeting intervals were retained. The normal subtitle-correction
API saved the reviewed six-cue timeline with explicit timing replacement.
The skill timeline validator passed against this reviewed alignment; this was
an audio-backed retiming operation, not script text fitted to unrelated cues.

Settings:

- EN / JA / ZH / FR, top-to-bottom; CLI order `fr,zh-Hant,ja,en`.
- Japanese kanji furigana and kana romaji; Chinese pinyin.
- Subtitle lift zero; normal LazyEdit renderer and grammar colors.
- Normal LALACHAN portrait blur-fill, 1080x1920, source aspect preserved.
- Configured logo at top-right; category `lalachan`.
- Targets: Shipinhao, YouTube, Instagram, Douyin.

## Japanese Source Annotation Repair

Preview exposed a general LazyEdit bug: Japanese source speech bypassed
furigana annotation, although Japanese translations had readings. Fixed the
source-language branch to annotate without rewriting source text or timing,
validate full token coverage/readings, and use a distinct annotation cache key.
Eleven regression tests passed. Japanese translation was refreshed through the
normal API and the normal burn step rerun. `中秋節` now visibly has
`ちゅうしゅうせつ`; the speaker icon remains on the actual source-language row.

Fix: [LazyEdit commit 18c37ed](https://github.com/lachlanchen/LazyEdit/commit/18c37ed).

## Render And Queue Evidence

- Final: H.264/AAC, 1080x1920, 29.133333 seconds, 24,877,264 bytes.
- Complete ffmpeg decode passed; final greeting frame inspected.
- Final render and MP4 inside the publish ZIP have identical SHA-256:
  `6218ec8b68e72c82805f088c8cffef72f61e53064b2a6249403032f40d2feac0`.
- Nutstore-relative copy:
  `Projects/LalaChan/2026-09-25-mooncake-together/mooncake_together_trilingual_29s_published_portrait.mp4`.
- LazyEdit job: 433. Remote job: `job-1790330092620-10`.
- Final remote and LazyEdit reported status: `done`, 2026-09-25 18:10 HKT.

Platform completion evidence:

- Douyin: initial upload failed; the existing unpublished draft was reuploaded
  once, then submit was accepted. The management SPA remained stale during
  automatic verification. A read-only management-page reload subsequently
  showed the matching title, 2026-09-25 18:00 timestamp, and `已发布`.
  No second publish was submitted.
- Shipinhao: matching story description found in the management page; published.
  The optional `啦啦侠` collection was unavailable in the selector, so this post
  was not assigned to that collection. Category metadata remains `lalachan`.
- Instagram: shared and saved caption verified (1,383 characters).
  [Reel](https://www.instagram.com/lazyingart/reel/DdtNXbfu-uH/).
- YouTube: checks completed with no issues, LALACHAN playlist selected, and
  publication dialog confirmed [Short](https://youtube.com/shorts/5N4NXnXx-_s).

All four platforms completed. Nutstore local-copy SHA-256 matches the final
render. This verifies the sync-folder copy, not a separate cloud acknowledgement.
All task-owned processing and monitoring commands exited; no new GUI stack
was started and no unrelated service was stopped.

The publish-only command reused the verified render and metadata. It deliberately
omitted the already-applied context file to avoid triggering correction again:

```bash
python scripts/lazyedit_publish.py --video-id 592 \
  --use-current-settings --no-process --no-correct-subtitles --use-polished \
  --burn-subtitles --languages fr,zh-Hant,ja,en --subtitle-lift-ratio 0 \
  --portrait-blur-fill --portrait-blur-mode lalachan \
  --logo --logo-position top-right --publish-category lalachan \
  --platforms shipinhao,youtube,instagram,douyin \
  --guided-monitor --wait --poll-seconds 15 --publish-timeout 7200
```

For an ordinary new publication, supply the context once to the single normal
publish command. This staged run was recovery from observed timing and annotation
defects, not a replacement workflow. Processing step names for metadata are
`metadata_zh,metadata_en,metadata_ja`, not the unsupported shorthand `metadata`.
