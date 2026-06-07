# Story Script Quality Audit

Date: `2026-06-07`

Scope: old LALACHAN story scripts and Xiaoyunque prompt scripts under
`references/stories/`, `references/prompts/`, and `Lala-Aya-Sasa-draft/`.
This is a writing-quality audit only. It does not rewrite existing scripts.

## Summary

The old scripts often have good visual imagination, but many stories are too
abstract, too dense, and too prompt-like. The dialogue sometimes sounds like an
AI explaining a theme instead of characters talking naturally. For future
stories, prioritize clear cause-and-effect, normal spoken language, and one
simple emotional/comic idea per short video.

Quick scan:

```text
82 story/prompt markdown or text files reviewed by sample and pattern scan.
14 prompt files exceed 1200 characters, which is usually too dense for 15s.
```

## Main Problems Found

### 1. Too Much Story For 15 Seconds

Many 15s prompts try to include full world-building, several props, multiple
plot turns, science explanation, jokes, and a cliffhanger. This makes videos
hard to follow and dialogue rushed.

Examples:

```text
references/prompts/2026-06-07-mars-2d-atom-chip-factory-zhuangzi-duanpian-15s.md
references/prompts/2026-05-18-episode08-blackhole-photon-sphere-duanpian-15s.md
references/prompts/2026-05-19-episode09-big-bang-duanpian-15s.md
```

Future rule: a 15s story should usually have 3 beats:

```text
setup -> problem -> funny/meaningful payoff
```

Use 3-5 spoken lines total. Keep the core story around 180-260 Chinese
characters before visual/style instructions.

### 2. Dialogue Sounds Like Explanation, Not People Talking

Some lines exist to explain the concept to the audience rather than because the
character would naturally say them.

Examples:

```text
阿芽酱：“保护边缘，不是只追求更薄。”
阿芽酱：“路不是给我们炫耀的，是给迷路的人看见回家的。”
啦啦侠：“真正的美食，不是战斗，而是分享！”
```

These are understandable, but they feel written, moralized, or symbolic. Future
dialogue should pass a spoken-language test: would a person actually say this
while running, eating, panicking, or joking?

Better direction:

```text
阿芽酱：“别碰中间，坏的是边上这一圈。”
啦啦侠：“先别讲道理，先救我的饭团。”
飒飒君：“这个灯塔怎么还要考试啊？”
```

### 3. Character Voices Are Not Distinct Enough

The trio often all speak in the same “cute AI comedy” voice. 阿芽酱 becomes a
generic explainer, 啦啦侠 becomes generic food jokes, and 飒飒君 becomes generic
panic.

Future voice rules:

```text
啦啦侠: warm, food-minded, brave after one silly misunderstanding.
阿芽酱: practical, observant, short corrections, not long lectures.
飒飒君: impulsive, physical comedy, says what a childlike adventurer would say.
庄子/robots: concise, dry, slightly deadpan, not poetic.
```

### 4. Abstract Or Poetic Lines Become Hard To Understand

Some endings sound mysterious but are not concrete enough for a short video.

Examples:

```text
庄子：“这工厂以前醒过。”
飒飒君：“今天我学会了，宇宙里也要讲礼貌。”
黑洞深处传来低沉反派声音：“星田碎片，迟早会落进我的视界。”
```

These lines may work in a longer series, but in 15s they can feel strange
because the viewer has not had enough time to understand the rule of the world.

Future rule: make the mystery visible and concrete before making it poetic.

```text
Screen action first: an old machine powers on by itself.
Line after: 庄子：“等一下，这不是我们开的。”
```

### 5. Science Concepts Are Overloaded

The scripts introduce useful concepts like `yield`, `event horizon`, `photon
sphere`, `2D materials`, and `supernova`, but they often explain too much in
one scene.

Problem examples:

```text
references/stories/2026-06-07-mars-2d-atom-chip-factory-zhuangzi.md
references/prompts/2026-05-18-episode08-blackhole-photon-sphere-long-60s.md
```

Future rule for educational concepts:

```text
one term -> one visual metaphor -> one joke -> one action
```

Example:

```text
Term: 良率
Visual: green chips vs gray chips
Joke: 啦啦侠以为 yield 是让零食先过
Action: 阿芽酱 points to the bad edge and fixes the process
```

Do not add a second technical topic in the same 15s video unless it is only a
background prop.

### 6. Random Prop Stacking Weakens Causality

Many scripts stack too many recurring objects: LightMind glasses, patchwork
notebook, U disk, star key, water-bucket baguette, bronze cups, blue fire,
paper kite, golden bird, robot, lighthouse, black-hole company, etc.

This can look imaginative but can also feel arbitrary. The viewer may not know
which object matters.

Future rule:

```text
For 15s: one main prop, one helper prop, one surprise prop at most.
```

The main prop should solve the problem. Extra props should stay in the
background unless they directly change the action.

### 7. Cause And Effect Is Sometimes Too Sudden

Several scripts use `突然`, `忽然`, or magical object changes to move the story
forward. This creates motion but not always logic.

Examples:

```text
青铜脸忽然眨眼，地面裂开蓝光。
空碗灯吸进红砂，变成小旋风。
晶圆中心浮现金色小鸟电路。
```

Future rule: before a magic event, show a reason or setup:

```text
The character touches the wrong button.
The robot warns them not to move a cup.
The card detects a mismatch.
The old machine recognizes the notebook pattern.
```

### 8. Prompt Boilerplate Leaks Into Story Thinking

Old prompt scripts repeatedly say:

```text
电影级动画质感
温暖可爱、科幻冒险、轻松搞笑
对话刚好覆盖15秒，不要太密，不要空
不要字幕，不要生成任何字幕
```

These are useful for generation, but they do not make the story better. When
the writing starts from boilerplate, the actual human situation can become
thin.

Future workflow:

```text
First write a normal mini-story.
Then add Xiaoyunque technical constraints.
Keep the two sections separate.
```

### 9. Mixed-Language Jokes Need Cleaner Setup

Mixed English/Japanese/Chinese jokes can work, but they need a simple reason.
The `yield` joke is promising, but it becomes odd when repeated too many times
or tied to a heavy technical plot.

Future rule:

```text
Use one language joke per episode.
Explain it through action, not lecture.
```

Good structure:

```text
Character misunderstands a word.
Another character corrects it in one short line.
The misunderstanding accidentally helps solve the problem.
```

### 10. Moral Or Theme Lines Are Too Direct

Some endings explain the lesson instead of letting the action show it. This can
feel preachy or AI-written.

Future rule: end with behavior, not lesson.

Instead of:

```text
“宇宙里也要讲礼貌。”
```

Use:

```text
飒飒君小声对纸鸢说：“下次你要借竹子，先说一声。”
```

## Future Writing Standard

Before sending any new story to Xiaoyunque, check it against this list:

```text
1. Can a child understand the story after one watch?
2. Does every event have a visible cause?
3. Does each character sound different?
4. Are there no more than 3-5 spoken lines for 15s?
5. Is there only one main idea or concept?
6. Are the jokes based on character action, not slogans?
7. Does the ending show the feeling instead of explaining the lesson?
8. Are prompt constraints separated from story content?
```

## Better 15s Template

Use this shape for future scripts:

```text
一句设定：他们在哪里，正在做什么。
一句问题：什么出错了。
三句对白：误会、纠正、行动。
一句结尾：一个清楚好笑或温暖的动作。
```

Example rhythm:

```text
火星芯片工厂里，庄子让大家别碰晶圆边缘。
啦啦侠以为“良率”是让零食先走，真的把饭团放到输送带上。
阿芽酱：“不是让饭团先走，是好芯片的比例。”
飒飒君：“那坏芯片是不是要补课？”
庄子把灰色芯片扫到返修区，机器人手臂突然递出一个小饭团。
啦啦侠小声说：“这个工厂，懂我。”
```

This is more normal, easier to understand, and still funny.

## Files Most Worth Reworking Later

If old stories are revised, start with these because they show the biggest
density or abstraction problems:

```text
references/prompts/2026-06-07-mars-2d-atom-chip-factory-zhuangzi-duanpian-15s.md
references/prompts/2026-05-18-episode08-blackhole-photon-sphere-duanpian-15s.md
references/prompts/2026-05-19-episode09-big-bang-duanpian-15s.md
references/prompts/2026-06-07-red-sand-bronze-kite-duanpian-15s.md
references/prompts/2026-06-08-red-sand-lighthouse-three-lamps-duanpian-15s.md
Lala-Aya-Sasa-draft/universe-adventure-40-episodes-v2/xiaoyunque-15s-prompts.md
```

Do not delete these files. They are useful as visual-idea archives. The issue
is not imagination; the issue is clarity, timing, and natural dialogue.
