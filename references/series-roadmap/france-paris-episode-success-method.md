# 法国巴黎篇成功记录

## 成果

- 故事：[巴黎的面包桶宴会](../stories/2026-08-16-paris-baguette-bucket-banquet-30s.md)
- 提示词：[小云雀生成提示词](../prompts/2026-08-16-paris-baguette-bucket-banquet-30s-mini.md)
- 发布上下文：[简洁元数据背景](../publish-context/2026-08-16-paris-baguette-bucket-banquet.md)
- 原始成片：`Videos/paris-baguette-bucket-banquet-2026-08-16.mp4`
- 成片规格：`968x720`、`4:3`、`43.467s`，视频与音频完整解码通过
- 生成方式：创作 Agent、Seedance 2.0 Mini 体验版
- 小云雀会话：`thread_id=30049a58-a9cf-4e57-a4f8-5c8c8485f941`

## 这集有效的写法

故事始终围绕一件事推进：四个伙伴采购食物，穿过巴黎，最后在塞纳河边完成面包宴会。`baguette` 和 `bucket` 的误听既是笑点，也是贯穿开头与结尾的道具线。埃菲尔铁塔、凯旋门和历史信息都由角色正在看见的景物引出，没有另开一段讲解。

台词只回应眼前发生的事：

```text
阿芽酱：“Bonjour！Une baguette, s'il vous plaît.”
阿芽酱：“我说的是 baguette，不是 bucket。不过这个桶正好装面包。”
飒飒君：“这个 bucket 今天总算没拿错。”
```

法语用于点餐和开饭，日语用于开场的自然评价，中文承担主要叙事。角色声音与人物关系清楚，外语没有变成额外说明。

## 素材与词卡

本集上传七张图片，不使用 `Trio.png`：

| 图号 | 素材 |
| --- | --- |
| 图1 | 本集实体学习卡 |
| 图2 | `LazyingArtRobot.png`，庄子机器人 |
| 图3 | `display.png`，LightMind AI 眼镜 |
| 图4 | `patchwork-leather-notebook-luxury-clean-v2.png` |
| 图5 | `raraxia.jpeg`，啦啦侠 |
| 图6 | `ayachan.png`，阿芽酱 |
| 图7 | `sasakun.jpeg`，飒飒君 |

词卡保存于：

```text
.lalastudio/generated-assets/2026-08-16-paris-baguette-bucket-banquet/words-card-baguette.png
references/images/2026-08-16-paris-baguette-bucket-banquet/words-card-baguette.png
```

卡面只有四行准确正文：

```text
Baguette
バゲット
ばげっと
法棍面包
```

它在塞纳河宴会镜头中作为真实道具出现。第一条是工作副本，第二条是版本库中的长期参考副本；两者 SHA-256 均为 `cb15ef777ef814b43a537577387ae75dfbe283977db09a7e94bff59815030c4b`。

## 发布结果

LazyEdit 使用现有 DeepSeek 默认配置完成转写、翻译和元数据生成。发布母版为 `1080x1920`，采用 LALACHAN 竖屏模糊背景、下方字幕空间和右上角标志。

字幕从上到下为：

```text
English
Japanese（汉字注音与罗马字）
Chinese（拼音）
French
```

法语原声行的声音标记跟随法语行，中文原声行的标记跟随中文行。最终发布包分类为 `lalachan`。

发布完成：

- LazyEdit video：`520`
- publication session：`67`
- LazyEdit job：`353`
- AutoPublish job：`job-1786853802989-4`
- 平台：抖音、视频号、YouTube、Instagram
- YouTube：<https://youtube.com/shorts/u9ZwPwG-b-s>

视频号和 Instagram 在平台页面完成验证；YouTube 返回公开链接；抖音接受发布后，内容管理索引仍在更新。

## 以后复用

为目的地选择一条清楚的行动主线、一个来自当地语言或食物的自然笑点、两三个可见地点和一个回到开头的结尾。提示词保留故事、人物、动作、声音与参考图关系即可。发布时把当地语言放在最下方字幕行，并让声音标记跟随实际原声语言。
