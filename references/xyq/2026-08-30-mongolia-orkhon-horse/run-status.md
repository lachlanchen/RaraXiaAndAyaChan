# Mongolia Orkhon Horse Run Status

## Generation

- Xiaoyunque thread: `95f63d0b-99bf-4330-bebd-2623bddd6921`
- Workflow: `创作 Agent`
- Model: `Seedance 2.0 Mini`
- Duration: `30s`
- Ratio: `4:3`
- Automatic countdown: disabled
- Paid confirmation clicks: `1`
- Displayed cost: `180` points
- Balance: `387 -> 207`

Uploaded references, in order:

1. words card
2. LazyingArtRobot / 庄子
3. LightMind AI glasses
4. patchwork notebook
5. 啦啦侠 individual reference
6. 阿芽酱 individual reference
7. 飒飒君 individual reference

The generated scene reference repeatedly stalled during upload and was excluded. `Trio.png` was intentionally not uploaded.

The first storyboard contained a duration inconsistency. It was corrected in the same thread before the paid confirmation to three shots of `15s + 8s + 7s = 30s`. The paid render was not retried.

## Download And QA

- Source output: `Videos/mongolia_orkhon_horse_30s_2026-08-30.mp4`
- Duration: `30.333333s`
- Frame size: `1112x836`
- Video/audio: H.264 + AAC
- Source SHA-256: `19668950228898a146810ce47a749249dd80e99e75c7d86fd70eb81daf5c1eeb`
- Full decode: passed
- Character review: 啦啦侠、阿芽酱、飒飒君、庄子 identities accepted
- Story review: grassland, horses, river valley, ruins, yurt, notebook and words card accepted
- Generated dialogue subtitles: none

## LazyEdit Publication

- LazyEdit video ID: `549`
- Publication session: `88`
- Local publish job: `389`
- Remote AutoPublish job: `job-1788104383083-25`
- Final status: `done`
- Platforms: Douyin, Shipinhao, Instagram, YouTube
- YouTube: `https://youtube.com/shorts/LXw503WDUVM`
- Category: `lalachan`
- Portrait output: `1080x1920`, LALACHAN blur-fill
- Logo: top-right
- Subtitle rows, top-to-bottom: English, Japanese, Chinese, Mongolian
- Final publication master SHA-256: `9015c9ad1086008556cb954cc8a9a407a555396880a879b75430d77a60c59f22`

The source ASR and polished SRT passed the nine-cue timeline validator. Correction preserved all cue timestamps. Clear identity errors in translated subtitles were repaired through LazyEdit's translation correction endpoint: English `Lala Man` became `Lala Xia`, and Japanese `ララちゃん` became `ララシャ`. The same session was then rebuilt through LazyEdit's independent subtitle burn endpoint, preserving its normal multilingual styling, ruby/romaji, pinyin, blur-fill and logo.

The final half-second ASR cue `这边是` was retained as an incomplete audible/source cue instead of being completed from the script.

## Subtitle Policy Clarification

Xiaoyunque prompts request no generated subtitles. If a generated artifact still contains subtitle pixels and the artifact is accepted, keep those pixels as part of the source image. They do not replace LazyEdit publication subtitles. Normal LALACHAN publication still burns LazyEdit multilingual subtitles unless the user explicitly requests a subtitle-free publication.
