# 小云雀 Lala/Aya/Sasa 默认创作配置

记录日期：`2026-05-08`

这个文件记录 LALACHAN 项目在小云雀里生成视频时的默认规则、常用模式、参考素材和中文提示词工作流。

## 默认工具选择

默认优先使用已登录的 Chrome Driver 控制小云雀网页，因为网页模式更容易确认模式、参考素材、分镜和积分状态。

保留小云雀 Agent / Skill API 作为可用后备方案，用于上传素材、提交任务和轮询进度，但默认不直接用 API 代替网页操作，除非明确需要批量上传或自动轮询。

```text
Chrome Driver endpoint: http://127.0.0.1:9222
Chrome profile: /home/lachlan/.cache/xyq-chrome
Launch script: scripts/xyq_chrome/launch_chrome.sh
CDP helper: scripts/xyq_chrome/xyq_cdp.py
```

Skill install command, saved for availability:

```bash
npx skills add https://gitee.com/Pippit-dev/pippit-skills.git -y -g
```

Access key policy:

- Full `XYQ_ACCESS_KEY` is stored only in `.env`.
- Tracked docs/config examples do not include the full key.
- Key name recorded locally: `LazyingArt`.
- Expiration recorded locally: `2027-04-26 09:51`.

## 小云雀常用创作模式

从网页下拉菜单记录的模式：

- `Agent 模式`: 全能创作 Agent，图片、短片、长视频一站式创作。
- `短剧 Agent`: 一键进入短剧创作工作台，快速开始分镜与剧情生成。
- `沉浸式短片`: 15 秒内音画同出短视频，一句话秒出片。
- `智能长视频 2.0`: 自动多分镜编排，轻松生成高质量长片。
- `生成图片`: 输入描述即刻出图，快速验证创意灵感。
- `智能长视频`: 基础长视频流程，速度稳定均衡。

主要使用：

- `Agent 模式`
- `沉浸式短片`
- `短剧 Agent` 需要直接使用专用工作台：

```text
https://xyq.jianying.com/novel/list?enter_from=small_tool
```

默认规则：

- 用户明确说 `短片`、`duanpian`、`沉浸式短片`、`15秒`、`快速测试` 时，使用 `沉浸式短片`。
- `沉浸式短片` 默认时长固定按 `15s` 设计，不额外写更长时长。
- `沉浸式短片` 默认使用普通 `Seedance 2.0`，非 Fast，非 VIP；只有用户明确要求 Fast 时才选择 `Seedance 2.0 Fast`。
- 用户没有指定模式时，默认使用 `Agent 模式`。
- `Agent 模式` 默认按更长视频处理，目标为 `1分钟以上` 或平台允许的最长稳定长度。
- 用户明确说 `智能长视频 2.0` 或 `zhineng changshipin 2.0` 时，从首页模式下拉选择 `智能长视频 2.0`。
- 用户明确说 `短剧 Agent`、`duanju agent` 或剧本工作台时，直接打开 `/novel/list?enter_from=small_tool`。
- 如果要做可控的短中文对话视频，优先 `沉浸式短片`。
- 如果要做复杂长剧情、分镜、参考视频复刻，优先 `Agent 模式`。

CDP mode helper:

```bash
scripts/xyq_chrome/xyq_cdp.py --list-modes
scripts/xyq_chrome/xyq_cdp.py --select-mode agent
scripts/xyq_chrome/xyq_cdp.py --select-mode duanpian
scripts/xyq_chrome/xyq_cdp.py --select-mode long2
scripts/xyq_chrome/xyq_cdp.py --url "https://xyq.jianying.com/novel/list?enter_from=small_tool" --state
scripts/xyq_chrome/test_modes.py --output references/xyq-mode-test-results.md
```

如果网页当前已经进入某个专用工作台，模式下拉可能不可见。此时先回到小云雀首页，再打开模式下拉菜单。

最近一次非提交模式测试记录：

```text
references/xyq-mode-test-results.md
```

## 固定参考素材

生成 Lala/Aya/Sasa 相关视频时，默认使用这三张图片作为参考：

```text
/home/lachlan/ProjectsLFS/LALACHAN/display.png
/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
/home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

角色映射：

- `啦啦侠 / Lala Xia`: `Trio.png` 里的男大熊猫角色。
- `阿芽酱 / Aya Chan`: `Trio.png` 里的女小熊猫角色。
- `飒飒君 / Sasa Kun`: `Trio.png` 里的男孩角色。
- `display.png`: LightMind AI 眼镜产品图，来自 `lightmind.art`，角色在合适场景中佩戴这种眼镜，并显示 `LightMind` logo。
- `patchwork-leather-notebook-luxury-clean-v2.png`: 手工拼皮笔记本产品图，来自 `buy.layzing.art`，用于书、菜单、琴谱/曲谱、钢琴谱、地图、任务册、工具或其他可作为道具展示的物件。

固定产品站点：

```text
LightMind AI glasses: https://lightmind.art
Handmade notebook: https://buy.layzing.art
```

默认语言：

- 主要使用中文提示词。
- 对话、故事、角色动作说明默认写中文。
- 如果需要日语台词，只保留非常短的固定句子，并在中文说明中解释。

## ChatGPT 剧本来源

ChatGPT conversation:

```text
https://chatgpt.com/c/69fc0bcd-4f2c-83ea-9117-46fc128a2496
```

本地记录：

```text
Lala-Aya-Sasa-draft/chatgpt-draft-history.md
Lala-Aya-Sasa-draft/duanju-agent-chatgpt-sushi.md
Lala-Aya-Sasa-draft/duanju-agent-chatgpt-sushi.txt
```

默认流程：

1. 在 ChatGPT 里用中文生成或优化故事/对话。
2. 把 ChatGPT 答案保存到本地 Markdown。
3. 将保存后的中文脚本复制到小云雀。
4. 在小云雀里选择模式：短片用 `沉浸式短片`，未指定用 `Agent 模式`。
5. 上传或引用三张固定图片。
6. 如有参考视频，再一起上传参考视频。
7. 提交任务后，通过 Chrome Driver 检查页面状态、分镜确认和积分提示。

2026-05-09 update for short-video reference assets:

- For `沉浸式短片`, use five image references when available: `display.png`, `patchwork-leather-notebook-luxury-clean-v2.png`, `R1.jpg.jpeg`, `R3.jpg.jpeg`, `Trio.png`.
- Attach old generated trio videos through the bottom `+ -> 从资产库选择` menu.
- Do not use `@引用素材` as the default path for old reference videos.
- The old videos should be used as real reference assets for voices, character identity, expressions, and action rhythm.
- Do not put asset-selection UI instructions into the prompt itself.
- Always include `不要字幕`.
- If generation is already on the way, stop interacting with publish/recharge controls and record only.

2026-06-07 update for extended seven-image reference order:

Use this exact order when a run includes the words card widget and LazyingArt
robot in addition to the usual Lala/Aya/Sasa references. Include the paths in
documentation and prompt drafts to avoid mixing up R1/R3 or the Trio image.

```text
1. words card 小白屏学习卡
   /home/lachlan/ProjectsLFS/LALACHAN/words-card.jpg

2. LazyingArtRobot，机器人庄子
   /home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png

3. LightMind AI 眼镜
   /home/lachlan/ProjectsLFS/LALACHAN/display.png

4. 拼皮笔记本
   /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png

5. 啦啦侠 服装参考
   /home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg

6. 飒飒君 服装参考
   /home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg

7. 啦啦侠 －－ 阿芽酱 －－ 飒飒君 三人角色参考
   /home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

脚本与草稿保存规则：

- 每次我们自己生成或改写的提示词、剧本、分镜，都保存到 `references/prompts/` 或 `Lala-Aya-Sasa-draft/`。
- ChatGPT `小云雀剧本` 会话里的有用回答也同步保存到本地 Markdown。
- 小云雀网页里实际使用过的模式、素材、提示词和测试结果保存到 `references/`。
- 默认主要使用中文提问、中文提示词和中文对话。

Reusable command:

```bash
scripts/xyq_chrome/prepare_duanju_from_chatgpt.py
```

Current-tab helper for the web UI:

```bash
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py visible PAGE_ID
scripts/xyq_cdp_browser.py set-prompt PAGE_ID references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s-numbered-assets.md
```

这个脚本默认打开 `短剧 Agent` 专用页面，上传 `.txt` 剧本文件，并复用 `.env` 中的 `XYQ_TRIO_ASSET_ID` 作为 `Trio.png` 默认角色参考资产。不会提交生成。

Reference-video command:

```bash
scripts/xyq_chrome/reference_video_until_credit.py \
  --video path/to/reference-video.mp4 \
  --thread-id THREAD_ID \
  --prompt "$(cat references/prompts/lala-aya-sasa-sushi-lightmind-cn.md)"
```

这个脚本默认会同时上传三张固定图片。如不想上传默认图片，显式加：

```bash
--no-include-default-images
```

## 默认短片提示词模板

```text
请参考上传的三张图片，保持啦啦侠、阿芽酱、飒飒君的人物形象、声音、性格、服装和说话方式一致。啦啦侠是男大熊猫，阿芽酱是女小熊猫，飒飒君是男孩。三人都戴着 LightMind AI 眼镜，镜片有轻微蓝色 HUD 光效，并显示 LightMind logo。整体为温暖、可爱、轻松搞笑的高质量动画风格。

请生成一个 15 秒中文短片。故事要简单、有趣、对话自然，三人的位置可以灵活变化，但人物形象不能漂移。请突出三个人之间的吐槽、误会和温馨互动。画面不要出现恐怖、阴暗、低质量 3D、角色变形、眼镜消失或字幕遮挡脸部。
```

## 默认 Agent 提示词模板

```text
请参考上传的三张图片和参考视频，保持啦啦侠、阿芽酱、飒飒君的人物形象、声音、性格、服装和说话方式一致。啦啦侠是男大熊猫，阿芽酱是女小熊猫，飒飒君是男孩。三人都戴着 LightMind AI 眼镜，镜片显示 LightMind logo 和轻微蓝色 HUD。请用中文创作一个轻松搞笑、温暖治愈的长视频故事，默认时长按平台可稳定生成的较长时长处理。

请先生成清晰故事线和分镜，再继续生成视频。三人的站位和镜头可以灵活变化，但角色设定必须保持一致。重点表现自然中文对话、可爱表情、轻松吐槽和温馨结尾。
```
