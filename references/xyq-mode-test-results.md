# Xiaoyunque Mode Smoke Test

Generated: `2026-05-08 14:10:12`

Scope: non-destructive browser test through the controlled Chrome driver. No prompt was submitted and no video generation was started.

| Mode | Result | Evidence |
| --- | --- | --- |
| Agent 模式 | PASS | Agent 模式 动漫萌娃误入人类世界 古风姐妹团玩真心话大冒险 特摄风猫狗大战 食材茶话会 / Agent 模式 / Agent 模式 / Agent 模式 |
| 沉浸式短片 | PASS | 沉浸式短片 Seedance 2.0 Fast VIP 按 1 秒 11 积分扣除     短片 2.0 Fast VIP 参考 15s 潮汕功夫茶宣传片 猫狗偷玩手机一秒装睡 漫剧：超绝人物特写 线稿转视频 / 沉浸式短片 Seedance 2.0 Fast VIP 按 1 秒 11 积分扣除 / 沉浸式短片 Seedance 2.0 Fast VIP 按 1 秒 11 积分扣除 / 短片 2.0 Fast VIP 参考 15s /  |
| 智能长视频 2.0 | PASS | 视频 2.0 自动 潮汕功夫茶宣传片 猫狗偷玩手机一秒装睡 漫剧：超绝人物特写 线稿转视频 / 视频 2.0 自动 / 视频 2.0 自动 / 视频 2.0 自动 |
| 短剧 Agent | PASS | 连接 Agent / 26 / 基础会员 / 上传我的剧本 / AI 生成剧本 剧本限免1次 / 粘贴文本 / 管理 |

## Mode Defaults

- `Agent 模式`: default mode when the user does not ask for a specific mode; use for longer Agent-driven videos.
- `沉浸式短片`: default short-video mode; set duration to `15s` before submission.
- `智能长视频 2.0`: selectable from the home composer dropdown; use only when explicitly requested or when long-video multi-shot planning is needed.
- `短剧 Agent`: use the dedicated tab directly: `https://xyq.jianying.com/novel/list?enter_from=small_tool`.

## Re-run

```bash
scripts/xyq_chrome/test_modes.py --output references/xyq-mode-test-results.md
```
