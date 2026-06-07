# Visual Asset Registry

This registry records recurring image references for LALACHAN video prompts.

## Core Trio And Products

Use these five images for most Xiaoyunque character videos:

```text
/home/lachlan/ProjectsLFS/LALACHAN/display.png
/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
/home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Meaning:

- `display.png`: LightMind AI glasses product reference. Use when characters
  wear AR/AI glasses or when a futuristic display appears.
- `patchwork-leather-notebook-luxury-clean-v2.png`: Aya Chan's handmade
  notebook. Use as book, menu, map, score, chart, protocol card, factory log, or
  repair manual.
- `R1.jpg.jpeg` and `R3.jpg.jpeg`: updated costume references for Lala Xia and
  Sasa Kun.
- `Trio.png`: trio character consistency reference.

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
```

Visual notes:

- Looks like a small physical e-ink display or desktop study card.
- Mounted on a clear or white stand.
- It should sit in the scene: on a desk, factory bench, cockpit, lab counter,
  robot charging table, drone landing pad, or AR workspace.
- It should not float like an overlay subtitle.

Content rule:

- One main word or concept per episode.
- English in large readable type.
- Japanese below with furigana if helpful.
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

When using the word card in Xiaoyunque prompts:

```text
Place a small physical desktop e-ink word-card widget on the lab table. The card
is part of the scene, not a subtitle. It displays one readable learning word in
English and Japanese with furigana.
```

If the model tends to create subtitles, add:

```text
不要字幕。画面里只能出现作为真实道具存在的单词卡，不要生成任何旁白字幕或说明文字。
```

