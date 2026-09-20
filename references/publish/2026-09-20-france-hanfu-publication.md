# France Hanfu Publication: Four Languages, Zero Lift

## Requested Output

- Episode: 塞纳河边，风也想合影.
- Source: `Videos/france-hanfu-seine-breeze-2026-09-20/france_hanfu_seine_breeze_30s.mp4`.
- LazyEdit video ID: `573`.
- Use portrait background blur-fill, the configured top-right logo, and normal LazyEdit subtitles.
- Subtitle lift is `0`, not a global settings change.
- CLI language order is bottom-to-top: `fr,zh-Hant,ja,en`.
- Visible order is English, Japanese, Chinese, French. Japanese kanji have furigana; the normal kana romaji and Chinese pinyin remain enabled.

## Context And Alignment

[Story context](2026-09-20-france-hanfu-context.md) was supplied to LazyEdit for normal subtitle correction and metadata generation. Actual dialogue remains authoritative; the story is not a substitute transcript.

The initial ASR produced eight cues, including isolated nonlexical interjections and an early start for the final dialogue. Ordinary correction preserved its timestamps but did not resolve the alignment problem. A separate full-audio Whisper large-v3 pass without a script prompt, followed by word alignment, supported six lexical dialogue cues:

| Start | End | Reviewed dialogue |
| --- | --- | --- |
| 1.760 | 2.880 | Bonjour，巴黎！ |
| 2.880 | 4.020 | 帮我拍张照吧。 |
| 8.620 | 10.800 | 我怎么多了顶帽子？ |
| 13.800 | 15.120 | 谢谢啦啦侠， |
| 15.120 | 16.620 | 也谢谢这顶帽子！ |
| 21.760 | 22.900 | 就留这张！ |

The initial eight-cue files were preserved privately. This was an explicit alignment recovery, not permission for ordinary text correction to move timestamps or invent speech. The reviewed SRT was imported through LazyEdit's existing `--subtitle-file` / `--subtitle-language zh` workflow. The reviewed six-cue timeline matched the independent aligned-ASR timeline exactly.

Word alignment initially hit a Whisper/Triton compatibility error: `JITCallable._set_src() takes 1 positional argument but 2 were given`. In an isolated verification process, median filtering and DTW ran on CPU while inference remained on GPU 1. No installed package or shared runtime code was changed. Machine transcription/alignment and visual review were performed; no human listening verification is claimed.

## Metadata Recovery

The normal shared context produced an overly detailed description. LazyEdit's metadata steps were rerun using this [short metadata brief](2026-09-20-france-hanfu-metadata-brief.md). An incorrect English reference to the fan landing on Aya's hat was corrected by clarifying the supplied context and rerunning `metadata_en` only. Metadata JSON was not manually rewritten.

Final English title: `Aya Chan & Rara Xia in Hanfu Along the Seine`. Category: `lalachan`. The public description concerns the Hanfu outing, fan mishap, group photo, and riverside croissants, not production instructions or private background.

## Verification

- Processed output: `france_hanfu_seine_breeze_30s_2026-09-20_portrait_subtitles_logo.mp4`.
- Dimensions: `1080x1920`; duration: `30.279002s`; size: `26,340,530` bytes.
- Full video/audio decode passed.
- SHA-256: `f09ccb659277cc982cfb209ad7d5d5e0e74340d2964ef2418ca1520721198188`.
- The MP4 inside the publish ZIP has the same SHA-256 as the inspected processed output.
- Japanese token data provided readings for every kanji-bearing token. Rendered samples visibly show readings for 写真, 撮, 帽子, and 増.
- Sample frames confirmed zero lift, four language rows, grammar colors, pinyin, and the top-right logo.
- Long English/French lines use the existing timed page-splitting behavior; a later-frame check confirmed the rest of the sentence appears.
- A local copy of the processed output was placed beside the source assets in the configured Nutstore project folder. Cloud synchronization acknowledgement was not independently checked.

Private QA artifacts remain in `.lalastudio/runs/2026-09-20-france-hanfu/publish-qc/`, including preserved initial ASR, reviewed SRT, alignment notes, and frame samples. Generated media and private browser/session data are not part of this commit.

## Publication Queue

The first submission was LazyEdit job `415`, remote `job-1789890924363-1`, targeting Douyin, Shipinhao, YouTube, and Instagram. Douyin upload failed after the publisher's initial attempt and two automatic retries, before the remaining platforms executed.

The verified processed output was reused for job `416`, remote `job-1789891421476-2`, targeting only Shipinhao, YouTube, and Instagram. Shipinhao initially displayed only the navigation shell, then its normal retry loaded the editor and completed upload. This recovery did not regenerate video, subtitles, or metadata.

Job `416` completed successfully on all three selected platforms:

| Platform | Evidence |
| --- | --- |
| Shipinhao | Publisher verified the matching episode description on the content-management page after submission. The requested collection was not available; the post still succeeded without it. |
| Instagram | [Published reel](https://www.instagram.com/lazyingart/reel/DdgH0-xuZvw/); saved caption verified after sharing. |
| YouTube | [Published Short](https://youtube.com/shorts/vHt4JrODRiw); checks completed without issues; publication receipt confirmed; LALACHAN playlist selected. |

## Douyin Recovery

DNS lookup and HTTPS connectivity tests on the publishing host succeeded for the Shipinhao site, Douyin creator site, Douyin upload host, and YouTube Studio. These checks did not establish a router/DNS outage and did not justify disrupting the network.

After the other three platforms finished, a Douyin-only recovery reused the same ZIP through AutoPublish's existing API:

```bash
curl -fsS -X POST "$AUTOPUBLISH_API/publish" \
  --data-urlencode filename=france_hanfu_seine_breeze_30s_2026-09-20.zip \
  --data reuse_existing=true \
  --data publish_douyin=true \
  --data restart_platforms=douyin
```

Remote recovery job: `job-1789892013379-3`. Only the Douyin browser was restarted, with its existing logged-in profile. The same file then uploaded successfully on the first attempt in that fresh browser. No shared service restart, router reset, video re-encode, paid generation, or source-code change was needed for this recovery. A transient browser/session or upload-endpoint issue is plausible, but the exact initial failure cause was not proven.

Douyin subsequently accepted the publish action, navigated to content management, and the publisher matched `汉服游巴黎塞纳河畔` in the management list. Recovery job `job-1789892013379-3` finished `done` with no error. The remote queue was empty and idle after completion. All four requested platforms are complete, with no repeated post on the three already successful platforms.

The original failed job remains part of the audit trail. Its failure must not be mistaken for the final episode status: job `416` covers Shipinhao/Instagram/YouTube and the separate remote recovery covers Douyin.

## Reuse Command

For an already verified output, run from the configured LazyEdit repository and environment:

```bash
python scripts/lazyedit_publish.py \
  --api-url "$LAZYEDIT_API" --video-id 573 \
  --no-process --no-correct-subtitles --publish \
  --platforms shipinhao,instagram,youtube \
  --use-current-settings --languages fr,zh-Hant,ja,en \
  --use-polished --burn-subtitles --subtitle-lift-ratio 0 \
  --portrait-blur-fill --logo --logo-position top-right \
  --publish-category lalachan \
  --guided-monitor --wait --poll-seconds 20 --publish-timeout 5400
```

This is a record of the recovery submission, not an instruction to run it again after success. Check queue/history first and retry only a demonstrably missing platform.
