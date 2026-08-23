# 小云雀 Lala/Aya/Sasa 默认创作配置

记录日期：`2026-05-08`

这个文件记录 LALACHAN 项目在小云雀里生成视频时的默认规则、常用模式、参考素材和中文提示词工作流。

## 默认工具选择

默认优先使用已登录的 Chrome Driver 控制小云雀网页，因为网页模式更容易确认模式、参考素材、分镜和积分状态。

保留小云雀 Agent / Skill API 作为可用后备方案，用于上传素材、提交任务和轮询进度，但默认不直接用 API 代替网页操作，除非明确需要批量上传或自动轮询。

```text
Chrome Driver endpoint: http://127.0.0.1:9344
Chrome profile: /home/lachlan/.cache/xyq-chrome
Launch script: scripts/xyq_chrome/launch_chrome.sh
CDP helper: scripts/xyq_chrome/xyq_cdp.py
```

`9344` is the current canonical Xiaoyunque profile endpoint. Do not assume that
another responsive CDP port belongs to the logged-in Xiaoyunque browser; verify
the Chrome process profile, current page URL, and noVNC display together.

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

- 用户未指定时长时，默认目标为 `30秒`，不要因为 `沉浸式短片` 上限是 `15秒` 就静默压缩故事。
- 用户明确说 `15秒`、`快速测试`、`cheapest`、`least credits` 时，才使用 `沉浸式短片` 的 `15秒` 低成本流程。
- 如果用户要 30 秒，而 `沉浸式短片` 被限制在 `15秒`，改用 30 秒可行的 `Agent 模式` / integrated workflow。
- 模型名称和积分价格会变化，不把历史型号写成永远默认。每次以网页当前可见选项为准，选择满足时长、画幅、参考图和质量要求的最低积分型号，并在提交前截图证明实际型号、档位和积分；提示词里的型号名称不算证明。
- `VIP` 是硬性阻断条件：模型下拉、工具栏、确认消息、积分预览或扣费记录里出现 `Seedance2.0Fast VIP` / `Fast VIP` / `VIP通道` 时，不要继续提交或渲染，先切换到可证明的非 VIP 模型；如果找不到非 VIP 选项，停止并报告。
- 用户没有指定模式时，默认使用能稳定生成 `30秒` 的 `Agent 模式` / integrated workflow。
- 只有用户明确要求 `1分钟`、`长视频` 或更长剧情时，才把 `Agent 模式` 按 `1分钟以上` 或平台允许的最长稳定长度处理。
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

## 历史三素材配置

以下三素材配置仅用于理解旧任务。新任务使用本文后面的当前单人角色参考顺序，不要把这个历史段落当成默认上传清单：

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
8. 视频生成完成后，默认自动下载 MP4，`ffprobe` 验证时长和尺寸，复制到 `Videos/`。
9. 下载验证后默认提交到 LazyEdit。优先用 LazyEdit CLI 直接上传；如果直接上传不方便，可以复制到 Nutstore AutoPublish 文件夹。用户没有明确要求发布到平台时，只导入/处理 LazyEdit，使用 `--no-publish`，不要自动发布到 YouTube/Instagram/视频号。

2026-05-09 historical update for short-video reference assets:

- This older five-image setup has been replaced by the current eight-image
  setup below. Do not use deleted `R1.jpg.jpeg` or `R3.jpg.jpeg` in new runs.
- Attach old generated trio videos through the bottom `+ -> 从资产库选择` menu.
- Do not use `@引用素材` as the default path for old reference videos.
- The old videos should be used as real reference assets for voices, character identity, expressions, and action rhythm.
- Do not put asset-selection UI instructions into the prompt itself.
- Always include `不要字幕`.
- If generation is already on the way, stop interacting with publish/recharge controls and record only.

2026-06-15 update for current eight-image reference order:

Use this exact order for new Xiaoyunque browser uploads. Include the paths in
documentation and prompt drafts only for local upload commands. In the final
Xiaoyunque prompt, refer to them as `图1` through `图8`, not as paths.

```text
1. words card 小白屏学习卡
   /home/lachlan/ProjectsLFS/LALACHAN/words-card.jpg

2. LazyingArtRobot，机器人庄子
   /home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png

3. LightMind AI 眼镜
   /home/lachlan/ProjectsLFS/LALACHAN/display.png

4. 拼皮笔记本
   /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png

5. 啦啦侠 / Rara Xia 单人参考
   /home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg

6. 阿芽酱 / Aya Chan 单人参考
   /home/lachlan/ProjectsLFS/LALACHAN/ayachan.png

7. 飒飒君 / Sasa Kun 单人参考
   /home/lachlan/ProjectsLFS/LALACHAN/sasakun.jpeg

8. 啦啦侠 －－ 阿芽酱 －－ 飒飒君 三人角色参考
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
