# Xiao Xiao Zhu MV Generation Plan

Date prepared: 2026-06-29  
Intended run date: 2026-06-30  
Status: planning only. Do not generate from this note unless explicitly asked.

## Goal

Generate a LALACHAN/Xiaoyunque MV for Musia song **你是一只猪 / Xiao Xiao Zhu**.

The main creative decision is fixed:

- 阿芽酱 / Aya Chan, the red panda, is the lead singer and camera center.
- 啦啦侠, 飒飒君, and 庄子机器人 are supporting dancers, backing singers, comic reactions, and protectors.
- 小小猪 is a soft cloud-pig rest mascot, not an insult.
- The video should feel like a warm bedroom-pop MV about being allowed to rest.

## Use These Source Notes

Main paste note:

```text
/home/lachlan/ProjectsLFS/LALACHAN/references/MusiaVideo/xiao-xiao-zhu-lalachan-lazyedit-paste-2026-06-29.md
```

Paste-ready Xiaoyunque full MV prompt:

```text
/home/lachlan/ProjectsLFS/LALACHAN/references/prompts/2026-06-29-xiao-xiao-zhu-full-mv-92s.md
```

Musia handoff:

```text
/home/lachlan/ProjectsLFS/Musia/references/MusiaVideo/xiao-xiao-zhu-mv-handoff-2026-06-29.md
```

Local MV package:

```text
/home/lachlan/ProjectsLFS/Musia/data/creative_projects/ni-shi-yi-zhi-zhu-20260629/mv/xiao-xiao-zhu-comfort-mv-20260629
```

## Recommended Generation Strategy

### Full MV Run

Use this if credits are enough and the page supports long generation:

```text
Mode: 创作 Agent
Duration target: about 92 seconds
Ratio: 16:9
Audio: upload Mandarin Musia MP3 as 音频1
Subtitles: off
Prompt: full MV prompt
```

This is the preferred real MV route because the song is about 92 seconds. Do not use 沉浸式短片 for the full version if it is limited to 15-30 seconds.

### Lower-Risk Test Run

Use this only as a preview before spending on the full MV:

```text
Mode: 沉浸式短片
Duration: 15-30 seconds
Ratio: 16:9
Section focus: chorus / final chorus
```

The test should prove that Aya Chan is clearly the lead singer, the characters stay consistent, and Xiaoyunque understands 小小猪 as a cloud-pig rest mascot.

## Upload Assets

Upload the normal LALACHAN references in this order:

```text
图1 /home/lachlan/ProjectsLFS/LALACHAN/words-card.jpg
图2 /home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png
图3 /home/lachlan/ProjectsLFS/LALACHAN/display.png
图4 /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
图5 /home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg
图6 /home/lachlan/ProjectsLFS/LALACHAN/ayachan.png
图7 /home/lachlan/ProjectsLFS/LALACHAN/sasakun.jpeg
图8 /home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Upload the Mandarin song:

```text
音频1 /home/lachlan/ProjectsLFS/MusiaSongs/audio/xiao-xiao-zhu-zh-Hans.mp3
```

Public audio reference:

```text
https://lazyingart.github.io/MusiaSongs/audio/xiao-xiao-zhu-zh-Hans.mp3
```

## Pre-Submit Checklist

Before spending credits, confirm visually in Xiaoyunque:

- Prompt text is the Xiao Xiao Zhu full MV prompt, not an old daily story prompt.
- Aya Chan / 阿芽酱 is explicitly described as red panda lead singer and camera center.
- Audio attachment exists and is the Mandarin MP3.
- All eight image references are attached if the page accepts them.
- If the upload limit complains, drop lower-priority assets in this order: words card, LightMind glasses, notebook, Trio. Keep individual characters and robot.
- Ratio is `16:9`.
- Full MV route uses `创作 Agent`; short test route uses `沉浸式短片`.
- Subtitles and lyric text are disabled in the prompt.
- Prompt says no file paths, no UI text, no watermark-like text.
- Do not click submit until all visible attachment chips and mode settings are correct.

## Generation Prompt Quality Notes

Keep the prompt clear, not overpatched. The model should understand:

- This is an MV, not a talking short.
- Music is primary.
- Dialogue is sparse and only in gaps.
- Aya Chan sings most main shots.
- Supporting characters dance, clap, protect, and react.
- Deadline storm is funny and non-horror.
- Final feeling is rest, warmth, and being allowed to stop for one night.

Do not add extra complex lore during generation. Extra lore usually makes the video less coherent.

## Output Naming

Suggested raw Xiaoyunque download name after moving into LALACHAN:

```text
/home/lachlan/ProjectsLFS/LALACHAN/Videos/xiao_xiao_zhu_mv_xyq_2026-06-30.mp4
```

Suggested final song-locked output:

```text
/home/lachlan/ProjectsLFS/LALACHAN/Videos/xiao_xiao_zhu_mv_song_locked_2026-06-30.mp4
```

## Post-Generation Checks

Run:

```bash
ffprobe -v error \
  -show_entries format=duration \
  -show_entries stream=index,codec_type,codec_name,width,height \
  /home/lachlan/ProjectsLFS/LALACHAN/Videos/xiao_xiao_zhu_mv_xyq_2026-06-30.mp4
```

Check:

- Duration is close to the intended run: about 92 seconds for full MV, or chosen short test length.
- Video is playable.
- Audio exists.
- Aya Chan is visible as lead singer in repeated shots.
- No subtitles or lyric text are baked into the picture.
- No local paths or fake UI labels appear.
- Small pig/cloud mascot reads as cute and affectionate.

## Song-Locked Audio Fix

If Xiaoyunque changes, weakens, or desynchronizes the music, keep the visuals and mux the Musia Mandarin MP3 back in:

```bash
/home/lachlan/ProjectsLFS/LazySkills/skills/musia-lalachan-mv-workflow/scripts/mux_musia_audio.sh \
  --video /home/lachlan/ProjectsLFS/LALACHAN/Videos/xiao_xiao_zhu_mv_xyq_2026-06-30.mp4 \
  --audio /home/lachlan/ProjectsLFS/MusiaSongs/audio/xiao-xiao-zhu-zh-Hans.mp3 \
  --output /home/lachlan/ProjectsLFS/LALACHAN/Videos/xiao_xiao_zhu_mv_song_locked_2026-06-30.mp4
```

Then verify the final:

```bash
ffprobe -v error \
  -show_entries format=duration \
  -show_entries stream=index,codec_type,codec_name,width,height \
  /home/lachlan/ProjectsLFS/LALACHAN/Videos/xiao_xiao_zhu_mv_song_locked_2026-06-30.mp4
```

## If The Full MV Fails

Fallback route:

1. Generate a 15-30 second chorus MV first.
2. Use the same image references and Mandarin MP3.
3. Focus on the chorus: cloud-bed world, group dance, Aya Chan center.
4. If the result is coherent, use it as a style reference for a second full MV attempt.

Do not immediately retry the same failed full prompt without changing one variable:

- shorten duration,
- reduce asset count,
- simplify prompt,
- or use the successful short test as reference.

## Website And Publish Later

This note is only for video generation. After a good final MV exists:

1. Copy it into `LALACHAN/Videos/`.
2. Refresh `../LalaMedias` if it should become part of the archive.
3. Add a Musia `fun.lazying.art` MV item only after the final video is stable.
4. Use LazyEdit publishing only after metadata is concise and viewer-facing.

Do not publish the raw first generation automatically.

