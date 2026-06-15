# Current Xiaoyunque Reference Image Order

Use this as the default LALACHAN image memory after the 2026-06-15 filename
update. These local paths are for upload commands only. In Xiaoyunque prompts,
refer to the uploaded images as `图1` through `图8`; never paste paths or
filenames into the prompt.

| Label | Local file | Meaning |
| --- | --- | --- |
| 图1 | `/home/lachlan/ProjectsLFS/LALACHAN/words-card.jpg` | 小白屏学习卡 style reference; use a fresh English/Japanese/furigana word each episode |
| 图2 | `/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png` | LazyingArt Robot, named `庄子`; preserve the chest logo |
| 图3 | `/home/lachlan/ProjectsLFS/LALACHAN/display.png` | LightMind AI glasses |
| 图4 | `/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png` | handmade patchwork notebook/tool prop |
| 图5 | `/home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg` | individual 啦啦侠 / Rara Xia reference |
| 图6 | `/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png` | individual 阿芽酱 / Aya Chan reference |
| 图7 | `/home/lachlan/ProjectsLFS/LALACHAN/sasakun.jpeg` | individual 飒飒君 / Sasa Kun reference |
| 图8 | `/home/lachlan/ProjectsLFS/LALACHAN/Trio.png` | group identity reference for 啦啦侠, 阿芽酱, and 飒飒君 |

Default upload command:

```bash
scripts/xyq_cdp_browser.py upload-images-verify PAGE_ID \
  words-card.jpg \
  LazyingArtRobot.png \
  display.png \
  patchwork-leather-notebook-luxury-clean-v2.png \
  raraxia.jpeg \
  ayachan.png \
  sasakun.jpeg \
  Trio.png \
  --timeout 180 \
  --screenshot outputs/xyq-run/after-upload-eight.png
```

Prompt wording:

```text
参考图顺序：图1 是小白屏学习卡风格参考；图2 是机器人庄子；
图3 是 LightMind AI 眼镜；图4 是拼皮笔记本；
图5 是啦啦侠单人参考；图6 是阿芽酱单人参考；
图7 是飒飒君单人参考；图8 是三人组合角色参考。
请只根据这些已经上传的图片参考，不要把任何文件名或路径画进视频。
```
