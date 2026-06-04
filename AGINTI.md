# LALACHAN — AgInTi Supervision Notes

## 持久化 Tmux 会话

- **AgInTi CLI 会话**: `lalachan-aginti`
- **目标**: `lalachan-aginti:0.0`
- **工作目录**: `/home/lachlan/ProjectsLFS/LALACHAN`
- **状态**: AgInTi Flow interactive chat，已就绪
- **创建时间**: 2026-05-19 HKT

当用户说"继续 aginti"时，使用 `tmux_send_keys` 将简短任务指令发送到 `lalachan-aginti:0.0`，
并使用 `tmux_capture_pane` 获取输出。

不要把用户与 Codex 的完整对话原文转发给 AgInTi。像真人监督者一样，只发送当前任务所需的简短指令。

如果 AgInTi 跑偏或任务需要暂停，先发送 `Esc`。若 `Esc` 无法立即停止运行，再把问题记录为 AgInTiFlow 工具层 bug，在 `/home/lachlan/ProjectsLFS/Agent/AgInTiFlow` 中做通用修复。

如果 AgInTi 因系统缺陷无法完成任务，不要只靠更长、更细的提示词硬救。先判断这是哪一层问题：计划、SCS 监督、浏览器/CDP 工具、权限策略、状态可见性、失败恢复、证据验证或工作流默认值。能复现的通用问题要回到 AgInTiFlow 仓库修复其逻辑、设计、哲学、harness 或 workflow，加回归测试，提交推送并本地安装新版，然后继续同一个 tmux/session。

## 项目摘要

LALACHAN 项目 workspace，位于 `/home/lachlan/ProjectsLFS/LALACHAN`。
Docker 挂载于 `/workspace`。

这里主要保存 LALACHAN 的视频提示词、参考素材、媒体处理脚本与小云雀工作流记录。内容创作写在本仓库；AgInTiFlow 工具能力改进写在 `/home/lachlan/ProjectsLFS/Agent/AgInTiFlow`，两者不要混在一起。

## 常用命令参考

- `tmux send-keys -t lalachan-aginti '<short human task instruction>' Enter`
- `tmux capture-pane -t lalachan-aginti -p -S -120`
- `tmux send-keys -t lalachan-aginti Escape`

## 运行时上下文

- 时区: Asia/Hong_Kong (HKT, UTC+8)
- Docker workspace 模式
- 包安装策略: allow
- 持久环境: /aginti-env
- 持久缓存: /aginti-cache

## 已验证任务

- 2026-05-19: AgInTi 生成并保存了 `references/prompts/2026-05-19-episode09-big-bang-duanpian-15s.md`，用于小云雀沉浸式短片 / Seedance 2.0 Fast / 15s / 非 VIP / 无字幕。
- 2026-05-19: 因小云雀网页自动化暴露 AgInTiFlow 缺陷，已在 `/home/lachlan/ProjectsLFS/Agent/AgInTiFlow` 修复并安装 `0.20.153`：SCS plan 等待会显示 `scs_plan`，继续会话会记录 `conversation.continued`，宽泛浏览器点击返回整页文本时会被视为可疑并触发监督复核。
- 2026-05-19: 复用 `lalachan-aginti` / `web-agent-e5ff4a98-e8f8-42b8-9390-ca6255a192f6` 做小云雀状态检查；页面已登录且有 composer，但当前无法确认短片 / 普通 Seedance 2.0 Fast / 15s，AgInTi 已按规则停止，未上传、未选素材、未提交。
- 2026-05-19: AgInTiFlow 已更新到 `0.20.155` 并本地全局安装。新增浏览器提交工作流保护：小云雀/Chrome/CDP 提交类任务默认给更大 step budget；如果最终报告承认未选资产库参考视频、未设置非 VIP 模型或未提交，SCS 会拒绝 finish，除非有真实外部阻塞（登录、积分不足、验证码、内部错误等）。源码提交: `3338c50 Harden browser submit workflows`。
- 2026-05-19: AgInTi 曾通过网页点击提交了一次 Big Bang 15s 任务，但它同时承认两个缺陷：toolbar 显示 `2.0 Fast VIP`，且未通过底部 `+ -> 从资产库选择` 添加旧三人参考视频。之后不要把这类“已提交但缺要求”的报告视为合格完成；必须继续修复 UI 状态或明确外部阻塞。
- 2026-05-19: 已训练 AgInTi 在小云雀页面上传五张本地参考图并做 DOM/截图验证。先上传五图后外部复核发现只有 `4/10`，缺 `patchwork-leather-notebook-luxury-clean-v2.png`；随后要求 AgInTi 只补传缺失图片并验证成功。最终证据：页面 `43DDE7795CFAD60B2F49A149928C8E8F`，`assetCount: "5/10"`，`patchworkFound: true`，截图 `outputs/xyq-upload-training/upload-verification-5of10.png`。本次没有点击生成、没有使用 API、没有提交。
- 2026-05-19: 用户仍看不到图片时，AgInTi 复核得出根因：五图确实在后台 CDP 页面 `tab_name=montage&mode=create`，但用户可见标签可能是 `home` 或 `integrated-agent`。诊断报告保存到 `diagnosis/upload-visibility-report.md`。后续上传工作必须在报告完成前执行 `bring-to-front` 或等价操作，并明确“当前用户可见页面”和“后台 CDP page”是否一致。

## 小云雀上传训练要点

优先使用项目脚本做上传和验证：

```bash
/home/lachlan/miniconda3/bin/python scripts/xyq_cdp_browser.py upload-images-verify PAGE_ID \
  display.png patchwork-leather-notebook-luxury-clean-v2.png R1.jpg.jpeg R3.jpg.jpeg Trio.png \
  --screenshot outputs/xyq-upload-training/upload-verification.png
```

不要在网页内部自己 `fetch("http://127.0.0.1:9222/json")` 或创建 WebSocket；这会在小云雀页面里超时。正确做法是在宿主侧使用 `scripts/xyq_cdp_browser.py set-file-input`、`verify-attachments`、`screenshot`。

`set-file-input ok` 不是完成证据。完成必须同时看到：

- 页面资源计数如 `5/10`
- DOM 中的五个文件名，尤其 `patchwork-leather-notebook-luxury-clean-v2.png`
- 截图保存到 `outputs/xyq-upload-training/`

如果用户说“看不到上传”，先检查是不是控制了后台 CDP page：

```bash
/home/lachlan/miniconda3/bin/python scripts/xyq_cdp_browser.py list-pages
/home/lachlan/miniconda3/bin/python scripts/xyq_cdp_browser.py bring-to-front PAGE_ID
/home/lachlan/miniconda3/bin/python scripts/xyq_cdp_browser.py verify-attachments PAGE_ID
```
