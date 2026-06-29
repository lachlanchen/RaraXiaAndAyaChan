# Musia to LALACHAN MV Research

Date: 2026-06-28  
Scope: check `../Musia` and decide whether it can generate a 15s song/MV workflow for the four buddies: 啦啦侠, 阿芽酱, 飒飒君, and 庄子机器人.

## Current MV Mode Research

Use this note when choosing between a complete full-song MV and a short 副歌/高潮 cut:

```text
references/MusiaVideo/mv-style-research-full-vs-chorus-2026-06-29.md
```

Current decision for **Aya Chan Hikari Ame**: make the `68.04s` full-song MV first, then optionally derive a chorus/highlight cut later.

## Conclusion

Yes. `../Musia` can already support a practical song-first MV workflow.

Best current route for a 15s LALACHAN MV:

1. Generate or select a short original Musia song/audio clip.
2. Review the audio before using credits on video generation.
3. Upload the audio plus the normal LALACHAN reference images to Xiaoyunque.
4. Generate a 15s or 30s MV in `沉浸式短片`.
5. If Xiaoyunque changes/compresses the music too much, replace the video audio with the reviewed Musia track using `ffmpeg`.

Use Musia as the source of rhythm, melody, emotional arc, and song rights. Use Xiaoyunque as the image/video generator.

## Evidence From Local Repo

Musia CLI is installed and healthy:

```bash
node ../Musia/bin/musia.js --version
node ../Musia/bin/musia.js doctor --json
```

Observed state:

- package version: `0.1.1`
- conda env: `musia`
- `ffmpeg`, `tmux`, `codex`, OpenAI key, DeepSeek key, and HF token present
- scripts present

Core supported workflows:

- song analysis: stems, lyrics, beats, chords, reports
- song planning: idea, lyrics, chords, melody, reference audio
- full song generation: ACE-Step / ACE-Step 1.5 route
- short singing package: SoulX verse route
- LALACHAN handoff: generated `LALACHAN_SONG_TO_VIDEO_HANDOFF.md`
- QA: `musia_quality_check.py`, review reports, ASR overlap, levels

Important docs in `../Musia`:

```text
README.md
references/musia-full-capability-guide.md
references/musia-song-workbench.md
references/lalachan-song-first-video-workflow.md
references/lalachan-musia-musical-short-film-handoff.md
references/soulx-verse-tool.md
references/local-quality-backend-install-status.md
```

## Existing Usable Audio

Good immediate candidates:

```text
../Musia/data/soulx_verses/rain-day-bilingual-verse/mix.wav
duration: 16.30s, 24 kHz mono WAV

../Musia/data/soulx_verses/rain-day-english-short-verse-20260628/mix.wav
duration: 15.88s, 24 kHz mono WAV

../Musia/data/creative_projects/aya-chan-hikari-ame-20260628/final/aya-chan-hikari-ame-selected.mp3
duration: 68.04s, 48 kHz stereo MP3
```

The 16s SoulX mixes are already close to a 15s MV. The 68s Aya Chan song is better as a theme-song reference and can be cut to a 15s excerpt.

Old handoff files sometimes say `Musai` in paths. Treat that as stale naming. The actual current repo checked here is `../Musia`.

## Recommended 15s Song Routes

### Route A: Fastest, Use Existing Short SoulX Mix

Use when the goal is quick MV proof-of-concept.

```bash
ffmpeg -y \
  -i ../Musia/data/soulx_verses/rain-day-bilingual-verse/mix.wav \
  -t 15 \
  -ar 48000 -ac 2 -c:a libmp3lame -b:a 192k \
  outputs/musia-video/rain-day-15s.mp3
```

Pros:

- already close to 15 seconds
- has `lyrics.md`, `manifest.json`, and `LALACHAN_HANDOFF.md`
- low engineering risk

Cons:

- audio is a first-pass short verse, not a polished full song
- SoulX mix may sound dry unless we add ambience/reverb/instrumentation

### Route B: Trim Reviewed Aya Chan Theme Song

Use when the goal is a more musical, richer reference.

```bash
ffmpeg -y \
  -ss 20 -i ../Musia/data/creative_projects/aya-chan-hikari-ame-20260628/final/aya-chan-hikari-ame-selected.mp3 \
  -t 15 \
  -af "afade=t=in:st=0:d=0.25,afade=t=out:st=14.4:d=0.6,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:a libmp3lame -b:a 192k \
  outputs/musia-video/aya-hikari-ame-15s.mp3
```

Pros:

- selected/reviewed song package exists
- richer arrangement
- good timing/emotional reference for a musical short

Cons:

- Japanese lyric accuracy is imperfect in the current selected version
- for public music-focused release, run another correction pass first

### Route C: Generate A New 15s Song Package

Use when the video needs a fresh original song for the four buddies.

Create lyrics first, short and singable. Example:

```text
[Verse]
雨后的小舞台 亮起来
Aya sings, the forest sways
啦啦侠跳一步 飒飒笑起来
庄子弹着吉他 say okay
```

Then create a project:

```bash
cd ../Musia
node bin/musia.js song init \
  --title "Four Buddies Tiny Stage" \
  --idea "A 15 second warm forest MV for Rara Xia, Aya Chan, Sasa Kun, and Zhuangzi robot." \
  --character "Rara Xia, Aya Chan, Sasa Kun, and Zhuangzi robot" \
  --vocal-language zh \
  --genre "cute cinematic character theme" \
  --style "light guitar, tiny drums, warm forest ambience, clear cheerful vocal" \
  --mood "warm, playful, hopeful" \
  --voice-notes "clear upfront fictional vocal, no real singer imitation" \
  --duration 15 \
  --bpm 96 \
  --keyscale "C major" \
  --lyrics-file /path/to/lyrics.txt
```

Generate and review:

```bash
data/creative_projects/<song-id>/commands.sh generate
data/creative_projects/<song-id>/commands.sh review
```

Only use the generated audio for video if the review and a human listening pass are acceptable.

## Xiaoyunque MV Generation

Use the existing LALACHAN browser workflow:

- logged-in Chrome profile
- no API unless explicitly requested
- `沉浸式短片`
- default 15s unless user asks otherwise
- 4:3 unless user asks otherwise
- upload actual files, not local path text
- no subtitles unless user explicitly asks

Upload order for normal LALACHAN images:

```text
图1: words-card.jpg
图2: LazyingArtRobot.png, 庄子机器人
图3: display.png, LightMind AI glasses
图4: patchwork-leather-notebook-luxury-clean-v2.png
图5: raraxia.jpeg
图6: ayachan.png
图7: sasakun.jpeg
图8: Trio.png
```

For an MV, also upload the selected Musia audio file as soundtrack/timing reference if the Xiaoyunque UI accepts it. The browser upload input observed on 2026-06-27 accepts images, videos, and audio extensions including `.mp3` and `.wav`.

If the UI accepts audio:

```bash
python3 scripts/xyq_cdp_browser.py --cdp-url "$XYQ_CDP_URL" upload-images-verify PAGE_ID \
  words-card.jpg LazyingArtRobot.png display.png patchwork-leather-notebook-luxury-clean-v2.png \
  raraxia.jpeg ayachan.png sasakun.jpeg Trio.png \
  outputs/musia-video/aya-hikari-ame-15s.mp3
```

Note: the current helper is named `upload-images-verify`, but CDP `setFileInputFiles` can send audio if the page input accepts audio. Verification may need enhancement because the visible evidence logic is image-focused.

## If Xiaoyunque Does Not Preserve Audio

Generate the MV with the audio as reference, then replace final audio:

```bash
ffmpeg -y \
  -i xiaoyunque-video.mp4 \
  -i outputs/musia-video/selected-15s.mp3 \
  -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  outputs/musia-video/four-buddies-mv-final.mp4
```

If the video duration is slightly longer than audio, either loop ambience or use `apad`:

```bash
ffmpeg -y \
  -i xiaoyunque-video.mp4 \
  -i outputs/musia-video/selected-15s.mp3 \
  -filter_complex "[1:a]apad=pad_dur=2[a]" \
  -map 0:v:0 -map "[a]" \
  -c:v copy -c:a aac -b:a 192k -shortest \
  outputs/musia-video/four-buddies-mv-final.mp4
```

## Proposed MV Prompt Structure

Keep prompts simple. Overpatched prompts perform worse.

Required:

- identify uploaded images by number
- say the audio is the rhythm/emotion reference
- ask for a music-video feeling, not normal dialogue-heavy story
- say no subtitles, no lyrics text, no filenames, no paths
- include the four buddies clearly

Example:

```text
请生成15秒、4:3比例的温暖音乐动画MV。请跟随上传的歌曲音频节奏和情绪变化，不要改变成普通剧情片。

图1是小白屏学习卡道具，图2是庄子机器人，图3是LightMind AI眼镜，图4是拼皮笔记本，图5是啦啦侠，图6是阿芽酱，图7是飒飒君，图8是三人整体参考。保持啦啦侠、阿芽酱、飒飒君和庄子机器人形象稳定。

场景：雨后的森林小木亭。阿芽酱在亭子里唱歌，庄子机器人弹小吉他，啦啦侠和飒飒君跟着节奏跳舞。动作要踩着音乐节拍，镜头在歌声开始时轻轻推进，副歌/高点时四个伙伴一起开心转圈。结尾阳光照进小木亭，四个伙伴向观众挥手。

不要字幕，不要歌词文字，不要说明文字，不要文件名或路径。
```

See `15s-mv-prompt-template.md` in this folder.

## Quality Gates

Before using a song for video:

- audio is the expected duration, ideally 15-16s
- vocal is audible if this is a vocal song
- no obvious clipping
- no unauthorized real singer imitation
- generated lyrics are original
- Musia project path, lyrics, manifest, and QA/review are saved

Before paying Xiaoyunque credits:

- correct mode/duration/ratio/model visible
- all images uploaded and visible
- audio uploaded or fallback merge plan prepared
- prompt has no local filesystem paths
- prompt says no subtitles/text
- create button clicked once only

After video:

- download MP4
- verify with `ffprobe`
- if needed, merge final Musia audio back into video
- save final MP4 to `Videos/`
- save story/prompt/audio manifest under `references/MusiaVideo/runs/` or `references/prompts/`

## Recommended Next Experiment

Run a low-risk 15s MV proof:

1. Trim `aya-chan-hikari-ame-selected.mp3` to 15s.
2. Upload the 8 reference images and the 15s MP3 in the noVNC Xiaoyunque browser.
3. Generate `沉浸式短片`, 15s, 4:3.
4. Download the MP4.
5. Compare generated audio with the original MP3.
6. If the soundtrack changed, merge the original MP3 back in.

This tests the full path without generating a new song first.


## 2026-06-28 Snow Mountain MV Run Notes

Observed working pattern for song-first MV:

1. Use Musia to prepare and review the 15s song first. For this run the selected track was `snow-mountain-dance-ja-selected.mp3`, about 15.0s, Japanese vocal hook, around 129 BPM.
2. Use Xiaoyunque only for visuals if direct audio upload causes an internal error. The failed direct-audio attempt showed `小云雀遇到了一些问题，请稍后重试` and did not deduct credits.
3. If the failed thread has no reply input, inspect the page. The actual retry control may be a small `lucide-refresh-ccw` icon under the error message. Clicking it may return to the home composer with prompt/assets restored rather than immediately generating.
4. For the reliable path, remove audio-specific dependency from the Xiaoyunque prompt. Ask for a 15s 4:3 MV visual that fits the song tempo and mood, then mux the reviewed Musia audio into the downloaded MP4 with ffmpeg.
5. Upload actual image files through the browser. Do not paste local paths into the prompt.
6. Keep all eight default assets when possible:
   - words-card.jpg
   - LazyingArtRobot.png
   - display.png
   - patchwork-leather-notebook-luxury-clean-v2.png
   - raraxia.jpeg
   - ayachan.png
   - sasakun.jpeg
   - Trio.png
7. Fallback only after a real Xiaoyunque complaint about too many assets. Do not preemptively reduce uploads. Remove exactly one optional asset at a time, retry, and stop removing as soon as the page accepts the set. Drop optional props in this order: words card, LightMind glasses, notebook, group Trio image. Keep individual character references and the robot when the story needs them.
8. After download, replace/mux audio locally:

```bash
scripts/musia_mv_finalize.sh \
  --video Videos/<xyq-visual>.mp4 \
  --audio ../Musia/data/creative_projects/<project>/final/<selected>.mp3 \
  --output Videos/<final-mv>.mp4
```

This creates an MP4 with the XYQ video stream and the exact selected Musia audio, using AAC at 192 kbps and `-shortest`.
