# Words Card Widget System

The words card is a recurring physical prop for language and technical concept
learning. It should look like a desirable desktop gadget that viewers might want
to own: clean, tactile, slightly futuristic, and useful.

## Design Identity

Object:

- Small e-ink or low-power display card.
- Thin translucent acrylic frame.
- Rounded but not toy-like corners.
- Clear stand or tiny robot-compatible dock.
- A small LazyingArt / panda mark can appear on the bottom edge.

Screen style:

- Warm white display, not glowing like a phone.
- Large main English word.
- Japanese word below with furigana.
- Tiny concept icon or diagram if useful.
- Optional color accents in red, green, and black, matching existing cards.

## Story Role

The card should teach without becoming a lecture.

Good uses:

- The robot slides the card into frame when a concept appears.
- Aya Chan flips the card to correct Lala Xia's misunderstanding.
- Sasa Kun reads the word wrong, causing the joke.
- The card becomes a tiny key, ticket, map label, lab status board, or AR widget.

Bad uses:

- Long paragraph text on screen.
- Subtitles pretending to be a prop.
- Too many words at once.
- Explaining the whole technology instead of one memorable concept.

## Word Format

Use this template:

```text
English: yield
Japanese: 歩留まり
Furigana: ぶどまり
Micro-meaning: good chips divided by total chips
Scene use: the card sits beside a wafer tray and flashes when bad chips turn gray
```

## Episode Vocabulary Examples

Chip series:

- `yield / 歩留まり / ぶどまり`: how many chips survive manufacturing.
- `wafer / ウェハー`: the round silicon disc.
- `mask / マスク`: the stencil for chip patterns.
- `node / ノード`: process generation, but not just physical size.
- `package / パッケージ`: how chips connect to memory and boards.
- `cache / キャッシュ`: small fast memory close to the compute unit.
- `NPU / ニューラル処理装置`: AI accelerator for edge devices.
- `ISA / 命令セットアーキテクチャ`: the contract between software and CPU.

Robotics series:

- `perception / 認識 / にんしき`: sensing the world.
- `control / 制御 / せいぎょ`: deciding motion.
- `trajectory / 軌道 / きどう`: planned path.
- `grip / 把持 / はじ`: holding an object.
- `haptics / 触覚 / しょっかく`: touch feedback.
- `SLAM / 同時位置推定と地図作成`: mapping while localizing.
- `latency / 遅延 / ちえん`: delay between action and response.
- `spatial / 空間 / くうかん`: content anchored in 3D space.

## Prompt Snippet

```text
画面中有一个真实存在的桌面单词卡小装置，像电子墨水学习卡，放在桌面或实验台上，不是字幕。它只显示一个关键词：English word + Japanese word + furigana。单词卡和剧情互动，例如被机器人拿起、被阿芽酱指给大家看、或变成解谜钥匙。不要生成旁白字幕，不要下三分之一字幕，不要大段说明文字。
```

## First Widget Concept

Theme: chip manufacturing.

Card text:

```text
yield
歩留まり
ぶどまり
good chips / total chips
```

Visual:

- Card stands beside a tiny wafer model.
- A few die squares glow green and a few glow gray.
- LazyingArtRobot points at the card with one finger.
- Lala Xia thinks "yield" means "give me snacks."
- Aya Chan explains it means how many chips pass the test.

