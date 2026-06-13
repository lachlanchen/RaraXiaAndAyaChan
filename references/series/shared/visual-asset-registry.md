# Visual Asset Registry

This registry records recurring image references for LALACHAN video prompts.

## Core Trio And Products

Use these seven uploaded images for most current Xiaoyunque character videos.
The paths are for browser upload only; prompts should refer to them as `图1`
through `图7`, not by filename or local path.

```text
图1 /home/lachlan/ProjectsLFS/LALACHAN/words-card.jpg
图2 /home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png
图3 /home/lachlan/ProjectsLFS/LALACHAN/display.png
图4 /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
图5 /home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
图6 /home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
图7 /home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Meaning:

- 图1: `words-card.jpg` / 小白屏学习卡. Use as the default physical desktop learning
  widget style reference in the scene, not as a subtitle overlay. Each new
  episode should display a fresh story-relevant word or concept. Use a
  pre-generated card image as 图1 only when that new card was intentionally made
  for the episode.
- 图2: robot `庄子`. White robot body with LazyingArt panda logo on chest.
- 图3 / `display.png`: LightMind AI glasses product reference. Use when characters
  wear AR/AI glasses or when a futuristic display appears.
- 图4 / `patchwork-leather-notebook-luxury-clean-v2.png`: Aya Chan's handmade
  notebook. Use as book, menu, map, score, chart, protocol card, factory log, or
  repair manual.
- 图5 and 图6 / `R1.jpg.jpeg` and `R3.jpg.jpeg`: updated costume references for Lala Xia and
  Sasa Kun.
- 图7 / `Trio.png`: trio character consistency reference.

## New Robot Character

```text
/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png
```

Visual notes:

- White humanoid robot with black mechanical joints.
- LazyingArt panda logo on chest.
- Tabletop/product-like proportions, friendly and precise.
- Can carry tools, point at screens, hold the word-card, or use its hand as a
  miniature factory robot.

Story role:

- Technical explainer character.
- Safety and checklist personality.
- Comic flaw: too literal; it treats metaphors as commands.
- Best used in chip, robotics, drone, AR, and factory episodes.

## Words Card Physical Widget

```text
/home/lachlan/ProjectsLFS/LALACHAN/words-card.jpg
/home/lachlan/ProjectsLFS/LALACHAN/words_card_arabic.JPG
/home/lachlan/ProjectsLFS/LALACHAN/artifacts/images/2026-06-07T02-10-31-891Z/image.png  # generated example, not the default upload
```

Visual notes:

- Looks like a small physical e-ink display or desktop study card.
- Mounted on a clear or white stand.
- It should sit in the scene: on a desk, factory bench, cockpit, lab counter,
  robot charging table, drone landing pad, or AR workspace.
- It should not float like an overlay subtitle.

Content rule:

- One main word or concept per episode.
- Generate a new word for every new story/video. Do not reuse the previous
  episode's word unless the user asks for continuity.
- English in large readable type.
- Japanese below it.
- Furigana for the Japanese reading.
- Optional third language only when it fits the story.
- Keep it short enough that the card remains visually credible.

Example:

```text
yield
歩留まり
ふりがな: ぶどまり
meaning: good chips / total chips
```

## Prompt Usage

There are two valid implementation paths:

1. Pre-generate a new words-card image first, for example with AgInTi image
   generation, using the existing card only as style reference. Upload that new
   generated image as `图1`.
2. Upload the existing words-card as `图1` as a style/example reference, then
   give Xiaoyunque the exact card content and ask it to render the new card in
   the scene.

Both methods are acceptable. Use whichever works better for the run, or combine
them if needed. Prefer pre-generation when the exact visible text matters.

When using the word card in Xiaoyunque prompts:

```text
Place a small physical desktop e-ink word-card widget on the lab table. The card
is part of the scene, not a subtitle. It displays one readable learning word in
English and Japanese with furigana. Choose a new word that matches this episode.
Card content: English = TOPIC_WORD; Japanese = 日本語; Furigana = ふりがな;
Chinese meaning = 简短中文解释.
```

If the model tends to create subtitles, add:

```text
不要字幕。画面里只能出现作为真实道具存在的单词卡，不要生成任何旁白字幕或说明文字。
```

For Xiaoyunque prompts, prefer this reference mapping:

```text
参考图顺序：图1 是小白屏学习卡，每集显示新的主题词；图2 是机器人庄子；图3 是 LightMind AI 眼镜；
图4 是拼皮笔记本；图5 是啦啦侠服装参考；图6 是飒飒君服装参考；
图7 是啦啦侠、阿芽酱、飒飒君三人角色参考。
本集单词卡内容：English: TOPIC_WORD；Japanese: 日本語；Furigana: ふりがな；中文含义：简短解释。
```
