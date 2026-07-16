# Xiaoyunque Words Card and Duration Workflow

This note records the useful result from the 2026-06-14 canyon/asura run. The
words card looked good when it was described as a small physical prop in the
scene instead of as overlay text.

## Duration

The current ordinary LALACHAN default is `15秒`. Use a longer duration only when
the user asks for it or the story package explicitly targets a longer workflow.
Do not silently compress an explicitly requested 30-second story to 15 seconds.

Use the 15-second workflow for:

- ordinary daily episodes
- `15s` / `15秒`
- cheapest / least credits / quick tests
- the `沉浸式短片` workflow

Use the 30-second Agent/integrated workflow only for an explicitly requested
longer episode, and keep its prompt compact.

## Words Card Pattern

Use `words-card.jpg` only as the visual style reference. Prefer generating a
fresh card image before video submission and upload that rendered card as
`图1`. Labels are useful in story metadata, but the physical card face contains
only the values:

```text
图1 是已经制作好的小白屏学习卡，可作为场景边缘、桌面、道具架或实验台上的小道具。
卡面只显示四行内容：
WORD
日本語
ふりがな
目标语言含义
不要显示语言名称、字段标签、冒号、项目符号或编号。
它只是场景里的真实道具，不是字幕，也不是画面说明文字。
```

Pick a concept that fits the episode theme. The metadata may identify the
languages for authoring and validation, for example:

```text
English: courage
Japanese: 勇気
Furigana: ゆうき
中文：勇气
```

Before upload, verify every value independently: spelling, script, reading, and
meaning must be correct, and all lines must express the same concept. No
language receives weaker validation than another. Inspect the final image at
original resolution and regenerate it if any line is wrong, duplicated,
missing, unreadable, or labeled.

## Example Prompt Fragment

```text
参考图顺序：图1 是已经制作好的小白屏学习卡，卡面依次显示 courage、勇気、ゆうき、勇气，不带语言标签；图2 是 LazyingArtRobot，机器人名叫庄子，胸前 LazyingArt 标志必须保留。图3 是 LightMind AI 眼镜。图4 是拼皮笔记本。图5 是啦啦侠服装参考。图6 是飒飒君服装参考。图7 是啦啦侠、阿芽酱、飒飒君三人角色参考。不要在画面中显示本地文件路径。
```

Keep the words card as a prop. It should not replace the story, become a
subtitle, or appear as floating UI text.
