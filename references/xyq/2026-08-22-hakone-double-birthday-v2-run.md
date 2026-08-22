# 箱根共同生日旅行 V2 生成记录

## 结论

- 实际模型：`Seedance 2.0 Mini 体验版`。
- 模型证据：提交前页面选中该模型，生成会话中的模型标签也显示该名称。
- 生成规格：`30 秒`、`4:3`、3 个连续分镜。
- 可见费用：`120` 积分；余额由 `320` 降至 `200`，只提交一次。
- 下载成片：`Videos/hakone_shared_birthday_seedance_mini_v2_2026-08-22.mp4`。
- 媒体验证：H.264 视频、AAC 音频、`968x720`、`30.21s`；完整解码无错误。

## 为什么 V2 比 V1 稳定

V1 和 V2 都使用 `Seedance 2.0 Mini 体验版`。V1 的主要问题不是模型，而是把 30 秒拆成 11 个镜头，并让系统反复重建设定，导致啦啦侠服装变化、庄子变成其他造型、主角身份漂移。

V2 保留同一模型，只做了三项关键调整：

1. 将故事压成 3 个连续场景，每段约 10 秒。
2. 先核对生成的 4 个角色资产，再确认继续生成视频。
3. 用简短续写消息要求沿用已经绑定的角色，不重新设计、不增加前景人物。

这说明角色一致性问题应先从分镜数量、参考图绑定和中间资产验收处理，不能无证据地归因于 Mini 模型，也不能声称必须换成 Fast。

## 上传素材顺序

1. 生日主题 words card。
2. 庄子机器人。
3. LightMind AI 眼镜。
4. 拼皮笔记本。
5. 啦啦侠个人参考。
6. 阿芽酱个人参考。
7. 飒飒君个人参考。
8. 箱根缆车四人场景参考。

上传后页面可见 `8/20`，并逐一核对了 8 张缩略图。未上传 `Trio.png`。

## 验收证据

- 提示词：`references/prompts/2026-08-22-hakone-double-birthday-30s-mini-v2.md`
- 上传截图：`outputs/2026-08-22-hakone-double-birthday-v2/after-upload.png`
- 提交前检查：`outputs/2026-08-22-hakone-double-birthday-v2/preflight.png`
- 角色预览：`outputs/2026-08-22-hakone-double-birthday-v2/r1-preview.png` 至 `r4-preview.png`
- 成片联系表：`outputs/2026-08-22-hakone-double-birthday-v2/contact-sheet.png`

联系表检查结果：

- 啦啦侠保持白色背带裤大熊猫造型。
- 阿芽酱保持深蓝水手服小熊猫造型。
- 飒飒君保持熊猫连体服男孩造型。
- 庄子保持白色关节机器人和胸前 LazyingArt 标志。
- 三个场景中没有陌生人物替换主角。
- 画面没有生成字幕。

## LazyEdit 校正与发布

- LazyEdit 视频 ID：`530`。
- 原始 ASR 与校正字幕均为 7 条；校验确认条目顺序和全部时间戳一致。
- 原始 ASR 将第 4 句识别为 `¡Gracias!`，结合实际对话校正为 `Buon compleanno!`。
- 最终字幕没有添加 `Thank you`、`谢谢` 或 `Grazie`。
- 发布成片：`1080x1920`、`30.20s`，LALACHAN 竖屏背景填充，英语、日语、繁体中文、意大利语四行字幕，右上角现有 LazyEdit logo。
- 本地发布任务：`367`。
- 远端发布任务：`job-1787366974851-2`。
- 抖音提交已接受；视频号、Instagram 和 YouTube 均返回发布成功。
- YouTube：`https://youtube.com/shorts/aMW0cIFjoL8`

V1 文件继续保留，未覆盖，也没有在本次任务中重新发布。
