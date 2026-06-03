# 2026-05-09 User Prompt History

This file records the user's Xiaoyunque / ChatGPT prompt instructions from today's work. Secrets are intentionally redacted; the full access key remains only in `.env`.

## ChatGPT Script Thread

User-provided ChatGPT script conversation:

```text
https://chatgpt.com/c/69fc0bcd-4f2c-83ea-9117-46fc128a2496
```

Instruction:

- Use the same Chrome Driver tab for ChatGPT.
- Generate or reuse a Chinese story/script answer from that thread.
- Save the answer locally.
- Use that saved answer as the Xiaoyunque prompt.

Saved local script files:

```text
Lala-Aya-Sasa-draft/2026-05-09-today-script-synopsis.md
Lala-Aya-Sasa-draft/2026-05-09-hong-kong-rainy-tea-restaurant-chatgpt.md
references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s.md
references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s-numbered-assets.md
```

## Main Story Prompt Used Today

Theme:

- A 15-second Chinese `沉浸式短片`.
- 啦啦侠、阿芽酱、飒飒君 in a rainy Hong Kong night street / tea restaurant story.
- LightMind AI glasses are part of the scene.
- The handmade patchwork notebook appears as a travel notebook / map / clue prop.
- Tone: warm, funny, healing, cinematic Hong Kong night atmosphere.
- Ending: the trio eats together; warm joke about adding another pineapple bun.
- Always say `不要字幕`.

Active prompt file:

```text
references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s-numbered-assets.md
```

## Correct Asset Numbering

The user corrected that prompt references must match the actual uploaded image order:

```text
图片1 = /home/lachlan/ProjectsLFS/LALACHAN/display.png
图片2 = /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
图片3 = /home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
图片4 = /home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
图片5 = /home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Meaning:

- `图片1`: LightMind AI glasses, sold at `lightmind.art`.
- `图片2`: homemade patchwork notebook, sold at `buy.layzing.art`; use for books, menus, scores, maps, and props.
- `图片3`: 啦啦侠 clothing/reference.
- `图片4`: 飒飒君 clothing/reference.
- `图片5`: trio character reference: giant panda = 啦啦侠, red panda = 阿芽酱, boy = 飒飒君.

## Xiaoyunque UI Corrections

The user repeatedly corrected the workflow:

- Work in the old Xiaoyunque tab; do not keep opening new tabs.
- Click the bottom `+` button.
- Choose `从资产库选择`.
- Select one or two old generated videos from history/assets.
- Use selected old videos for voice, characters, facial expression style, and action timing.
- Do not use `@引用素材` for the reference video.
- Do not put "use + to select old video" inside the prompt as if it were a content instruction.
- Attach images first, then select old video from asset library, then use the prompt with `不要字幕`.
- System upload/file picker is difficult; use the browser driver / CDP where possible.

Relevant DOM provided by the user:

```text
uploadMenu-SvO0HE
本地上传
从资产库选择
角色库
```

## Selected Old Reference Videos

Selected via `+ -> 从资产库选择`:

```text
资产 #7637271291062632985
资产 #7635834282704405017
```

The asset picker showed `已选 2 个素材`. After `应用`, one visible `@ 0:15` reference video card remained in the composer, so the current short composer appears to accept one visible video reference together with the five image references.

## Today's Stop Condition

The user later said:

```text
the video generation is on the way
you just record
record all you did before
and no need to care about the publish today now
```

Therefore no more publish / recharge / submit clicks should be attempted for today's run.

## Security Note

The Xiaoyunque access key was previously saved to `.env`. Do not copy the full key into tracked Markdown. Use `references/xyq-env-config.example` for redacted config examples.

