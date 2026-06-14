# Xiaoyunque Words Card Prompt and 30s Default

This note records the useful result from the 2026-06-14 canyon/asura run. The
words card looked good when it was described as a small physical prop in the
scene instead of as overlay text.

## Default Duration

Future LALACHAN video generation should target `30秒` by default. Do not silently
compress a story to `15秒` just because the `沉浸式短片` UI is capped at `15秒`.

Use `15秒` only when the user explicitly asks for:

- `15s` / `15秒`
- cheapest / least credits / quick test
- the `沉浸式短片` workflow despite its visible `max=15` duration cap

For ordinary requests, use the 30s-capable Agent/integrated workflow and keep the
prompt compact.

## Words Card Pattern

Use `words-card.jpg` as `图1` unless a fresh generated card image already exists.
The prompt should ask Xiaoyunque to render the card as an in-scene object:

```text
图1 是小白屏学习卡风格参考，可作为场景边缘、桌面、道具架或实验台上的小道具。
卡片内容是 English: WORD；Japanese: 日本語；Furigana: ふりがな；中文：中文含义。
它只是场景里的真实道具，不是字幕，也不是画面说明文字。
```

Pick a word that fits the episode theme. For the canyon/asura battle, the
successful word was:

```text
English: courage
Japanese: 勇気
Furigana: ゆうき
中文：勇气
```

## Example Prompt Fragment

```text
参考图顺序：图1 是小白屏学习卡风格参考，可作为峡谷边缘一个小道具，卡片内容是 English: courage；Japanese: 勇気；Furigana: ゆうき；中文：勇气。图2 是 LazyingArtRobot，机器人名叫庄子，胸前 LazyingArt 标志必须保留。图3 是 LightMind AI 眼镜。图4 是拼皮笔记本。图5 是啦啦侠服装参考。图6 是飒飒君服装参考。图7 是啦啦侠、阿芽酱、飒飒君三人角色参考。不要在画面中显示本地文件路径。
```

Keep the words card as a prop. It should not replace the story, become a
subtitle, or appear as floating UI text.
