# Xiao Xiao Zhu MV Handoff

Date: 2026-06-29

Use this note in LALACHAN when generating a Xiaoyunque/Seedance MV for Musia song **你是一只猪 / Xiao Xiao Zhu**.

## Source Package

```text
/home/lachlan/ProjectsLFS/Musia/data/creative_projects/ni-shi-yi-zhi-zhu-20260629/mv/xiao-xiao-zhu-comfort-mv-20260629
```

Main prompt:

```text
/home/lachlan/ProjectsLFS/Musia/data/creative_projects/ni-shi-yi-zhi-zhu-20260629/mv/xiao-xiao-zhu-comfort-mv-20260629/XYQ_PROMPT_FULL_MV.md
```

Copy kept in this repo:

```text
references/prompts/2026-06-29-xiao-xiao-zhu-full-mv-92s.md
```

## Audio

Preferred upload:

```text
/home/lachlan/ProjectsLFS/Musia/../MusiaSongs/audio/xiao-xiao-zhu-zh-Hans.mp3
```

Public URL:

```text
https://lazyingart.github.io/MusiaSongs/audio/xiao-xiao-zhu-zh-Hans.mp3
```

Duration: about `92.0s`.

## Visual Concept

Cute comfort bedroom-pop MV. `小小猪` is an affectionate cloud-pig rest mascot. Aya Chan / 阿芽酱 is the red panda lead singer and camera center. The LALACHAN four buddies are tired from homework, messages, reports, and alarms. A comic deadline storm chases them, but they turn it into pillows, stars, and a warm rest world.

## Generation Setup

```text
Mode: 创作 Agent for full 92s MV, or 沉浸式短片 for a short chorus test.
Ratio: 16:9 for the full MV.
Upload: 图1-图8 normal LALACHAN references plus 音频1 Musia MP3.
Subtitles: off.
Prompt: paste references/prompts/2026-06-29-xiao-xiao-zhu-full-mv-92s.md.
```

For a cheaper test, use the chorus section:

```text
27.91-43.99s first chorus
62.59-80.07s final chorus
```

## Final Audio Rule

The Musia MP3 is the final soundtrack authority. If Xiaoyunque changes the song, mux the Musia audio back:

```bash
export MUSIA_ROOT="${MUSIA_ROOT:-/home/lachlan/ProjectsLFS/Musia}"
export LALACHAN_ROOT="${LALACHAN_ROOT:-/home/lachlan/ProjectsLFS/LALACHAN}"
export LAZYSKILLS_ROOT="${LAZYSKILLS_ROOT:-/home/lachlan/ProjectsLFS/LazySkills}"

"$LAZYSKILLS_ROOT/skills/musia-lalachan-mv-workflow/scripts/mux_musia_audio.sh" \
  --video "$LALACHAN_ROOT/Videos/xiao_xiao_zhu_mv_xyq_2026-06-29.mp4" \
  --audio "$MUSIA_ROOT/../MusiaSongs/audio/xiao-xiao-zhu-zh-Hans.mp3" \
  --output "$LALACHAN_ROOT/Videos/xiao_xiao_zhu_mv_song_locked_2026-06-29.mp4"
```
