# Lala Studio Yakiniku Run - 2026-07-20

## Result

Lala Studio refined **飞走的烤肉**, generated two reusable visual references, submitted one Xiaoyunque task, downloaded the result, and handed it to the normal LazyEdit publication workflow.

- Story: `references/stories/2026-07-20-story-20260720133400.md`
- Prompt: `references/prompts/2026-07-20-heaven-yakiniku-15s.md`
- References: `references/images/2026-07-20-heaven-yakiniku/`
- Source video: `Videos/2026-07-20-story-20260720133400.mp4`
- Xiaoyunque thread: `d435cd1f-1b62-4e90-ac8b-99ad26a42976`
- Video SHA-256: `b38f7c7fc6992b92fbe565e1c8d02f6e51bc4f9605c2bc6646af3765faa77ad1`

The source is `15.047s`, `1256x720`, H.264 with AAC stereo. Full video and audio decode checks passed.

## Generation Contract

- Mode: `沉浸式短片`
- Model: `Seedance 2.0 Mini 体验版`
- Duration: `15秒`
- Ratio: `16:9`
- Upload order: generated word card, 庄子, 啦啦侠, 阿芽酱, 飒飒君, generated scene keyframe
- Submission count: one; no regeneration or retry

Before submission, the browser-side blob hashes were matched byte-for-byte to all six local files. The button was clicked only after the prompt, login, model, duration, ratio, attachments, credit rate, and absence of blockers were verified.

## Publication Contract

Lala Studio invoked one normal `lazyedit_publish.py` workflow with the reviewed story as context. LazyEdit owns ASR correction, translations, metadata, portrait rendering, packaging, queueing, and monitoring.

- Platforms: Shipinhao, YouTube, Instagram, Douyin
- Category: `lalachan`
- Portrait mode: built-in LALACHAN blur-fill
- Subtitles: English, Japanese with ruby/romaji, and Chinese with pinyin
- Logo: configured LazyEdit logo at top-right
- LazyEdit video id: `486`
- Local publish job: `318`
- Remote AutoPublish job: `job-1784558642492-7`

Final platform state:

- Douyin: published and matched `烤肉飛走啦` in the management page
- Shipinhao: published and matched the generated description in the management page
- Instagram: publish confirmation received
- YouTube: published at `https://youtube.com/shorts/qKCymApdRUQ`

The local LazyEdit job and remote AutoPublish job both reached `done`. YouTube created a `LALACHAN` playlist, but the new playlist was not immediately selectable; publication continued without assigning this post to that playlist.

The corrected dialogue is:

```text
这片能吃了吗？
火不够旺，我来我来！
你别跟着飞！
还是夹子快。
哈哈哈
```

## Reliability Lessons

1. Reference-image prompts must use only `referenced_image_paths` when every input has a local path. Do not also pass `num_last_images_to_include`.
2. Natural requests such as “制作一张写实场景关键帧” must enable scene pre-generation before scene-source toggles are accessed.
3. Browser controller waits must require a new job ID as well as a terminal status. Otherwise an earlier completed job can make a new command return prematurely.
4. A timed-out result watcher does not justify another paid click. Reinspect the same thread and restart only the read-only watcher.
5. Accept a download only after duration, dimensions, audio presence, file size, full decode, and hash/copy checks pass.
