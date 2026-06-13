# LALACHAN Writing Problems Ledger

This is a living critique ledger for LALACHAN stories and video prompts. It
records recurring writing problems, examples, and repair rules. Use it before
submitting stories to Xiaoyunque.

## Core Standard

A good LALACHAN story should feel like a tiny scene from a real cartoon:

- one clear situation;
- one small problem;
- one physical or emotional response;
- one joke or surprise;
- one warm ending.

The viewer should understand the story without reading a prompt note.

## Recurring Problems

### 1. Report-Like Dialogue

Problem: characters say lines that sound like a summary, a lab report, or an AI
lesson.

Bad examples:

```text
结论：实验需要冷静，也需要一点点节奏。
真正的美食，不是战斗，而是分享。
保护边缘，不是只追求更薄。
```

Repair:

```text
看来，做实验要静得下来，也要踩得准拍子。
先别讲道理，先救我的饭团。
别碰中间，坏的是边上这一圈。
```

Rule: remove words like `结论`, `意义`, `真正的`, `本质上`, `系统提示`, unless a
character would really say them in that moment.

### 2. Strange Translated Wording

Problem: phrases sound translated or mechanically assembled.

Bad examples:

```text
跳舞的版本可能不太稳。
生命数据完成同步。
幸福值爆表。
```

Repair:

```text
跳舞嘛……不太行。
它亮了！
我快开心到说不出话了。
```

Rule: if the phrase would sound odd in a normal conversation, replace it with a
plain spoken sentence.

### 3. Prompt Voice Leaks Into Story

Problem: the story reads like a video-generation instruction instead of a scene.

Bad pattern:

```text
整体画面温暖治愈，角色表情丰富，镜头缓慢推进。
```

Repair: keep this in the prompt section, not the story. The story should say
what happens:

```text
灯慢慢亮起来。阿芽酱看着培养皿，声音放轻了。
```

### 4. Too Many Concepts In One Short Video

Problem: one 15s or 30s story tries to include science, product, lore, comedy,
battle, new props, and a moral ending.

Repair rule:

```text
15s: 1 situation + 1 problem + 1 joke/payoff.
30s: 1 situation + 2 small turns + 1 payoff.
```

If a term is educational, use one term only.

### 5. Weak Cause And Effect

Problem: the plot moves by `突然` without setup.

Bad pattern:

```text
突然，机器发光。
突然，地面裂开。
突然，怪物出现。
```

Repair:

```text
啦啦侠按错了按钮，机器才发光。
庄子提醒不要碰杯子，飒飒君还是碰了一下。
阿芽酱发现温度波动，培养箱才开始报警。
```

Rule: before surprise, show the cause.

### 6. Character Voices Blur Together

Keep voices distinct:

- 啦啦侠: warm, brave, food-minded, slightly clumsy; short sincere reactions.
- 阿芽酱: practical, observant, gentle correction, light teasing.
- 飒飒君: curious, physical comedy, fast reactions.
- 庄子: precise and dry, but cute; avoid long reports.

Quick test: remove the speaker names. If every line could be said by anyone,
rewrite.

### 7. Theme Is Explained Instead Of Shown

Problem: ending states the lesson directly.

Bad examples:

```text
自由是有人喊你的名字。
人生也会发光。
宇宙里也要讲礼貌。
```

Repair: show the action:

```text
他们互相喊名字，确认每个人都到了山顶。
店门口的灯亮着，三个人回头笑了一下。
飒飒君把最后一块点心递回去。
```

Rule: let behavior carry the theme.

### 8. Comedy Without Grounding

Problem: joke appears but has no physical setup.

Repair: make each joke visible:

```text
庄子说自己手稳，下一秒脚跟着节拍动了一下。
啦啦侠说负责安静，却喊得最大声。
飒飒君想帮忙，先把自己绕进胶带里。
```

### 9. Product Props Feel Forced

Problem: LightMind glasses, notebook, words card, or robot appear only because
the prompt says they must.

Repair: give each visible prop one job:

- LightMind: notices something the characters miss.
- Notebook: records a recipe/map/protocol.
- Words card: one learning word on a real desk object.
- 庄子: precise hands, safety check, dry joke.

If a prop has no job, put it in the background or remove it from the story.

### 10. Xiaoyunque Prompt Overpatching

Problem: prompts become huge lists of rules and negative instructions. This can
make the model focus on constraints instead of the scene.

Repair:

1. Story paragraph first.
2. Reference-image mapping second.
3. 3-5 visual requirements.
4. One short no-subtitle line.

Avoid repeating the same warning many times.

## Critic Checklist

Before saving a final prompt, answer:

- Can a viewer explain the story in one sentence?
- Does every line sound speakable?
- Is there one main conflict or joke?
- Does the ending happen through action, not a lesson line?
- Are props doing jobs instead of being listed?
- Is the duration realistic for the amount of dialogue?
- Are there any words like `结论`, `本质`, `版本`, `真正的`, `系统`, `意义` that should be removed?
- Does the prompt keep story and technical constraints separate?

## Workflow

Use this sequence:

```text
draft -> critic pass -> rewrite -> Xiaoyunque prompt -> path-leak check -> submit
```

If using AgInTi writer:

```text
AgInTi writing_specialist draft -> human/critic review -> final v2 file
```

Do not treat AgInTi's summary as proof of writing quality. Read the story.

