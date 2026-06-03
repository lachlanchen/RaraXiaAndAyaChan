# Xiaoyunque Asset-Library Reference Workflow

This is the reusable workflow for attaching an old generated video as the real reference video in Xiaoyunque.

## When To Use

Use this when the user says:

- "select one or two old videos"
- "use its voice and characters"
- "choose old video from history"
- "use the three fight with the fire dragon / old generated trio video"

This means attach actual Xiaoyunque asset-library videos. Do not only describe the old video inside the prompt.

## Correct Sequence

1. Keep the current Xiaoyunque tab. Do not open new tabs unless asked.
2. Confirm mode and model, usually `短片`, `2.0 Fast`, `15s`.
3. Attach the image references first.
4. Click the bottom-left `+` button in the composer toolbar.
5. Choose `从资产库选择`.
6. In the asset modal, select one or two old trio videos.
7. Click `应用`.
8. Confirm a video reference card appears in the composer, for example `@ 0:15`.
9. Fill or keep the Chinese prompt, with `不要字幕`.
10. Submit only if the user has asked to generate.

## Do Not Use

- Do not use `@引用素材` for this reference-video step.
- Do not use the physical system file picker when a CDP or asset-library path can do the job.
- Do not write UI instructions such as `从 + 选择旧视频` into the actual video prompt.
- Do not keep clicking publish or recharge if the user says generation is already on the way.

## CDP Helper Commands

List open tabs:

```bash
scripts/xyq_cdp_browser.py list-pages
```

Inspect visible controls:

```bash
scripts/xyq_cdp_browser.py visible PAGE_ID
```

Open the bottom `+` menu:

```bash
scripts/xyq_cdp_browser.py click PAGE_ID 484 753
```

Click `从资产库选择` after the menu opens:

```bash
scripts/xyq_cdp_browser.py click PAGE_ID 573 659
```

Capture evidence:

```bash
scripts/xyq_cdp_browser.py screenshot PAGE_ID /tmp/xyq-state.png
```

Set a prompt safely through Tiptap:

```bash
scripts/xyq_cdp_browser.py set-prompt PAGE_ID references/prompts/example.md
```

## 2026-05-09 Confirmed Asset Modal Details

The upload menu DOM contained:

```text
uploadMenu-SvO0HE
uploadMenuItem-GDs2iL: 本地上传
uploadMenuItem-GDs2iL: 从资产库选择
uploadMenuItem-GDs2iL: 角色库
```

The asset cards used class names like:

```text
assetCard-tUt0jS
assetCardSelected-TOZN8m
assetThumbDuration-g81WK3
```

Old trio videos selected:

```text
资产 #7637271291062632985
资产 #7635834282704405017
```

The picker showed `已选 2 个素材`, then the composer showed one visible `@ 0:15` reference card after applying.

## Prompt Rule

In the final prompt, reference the attached assets semantically:

```text
请参考已上传的五张图片和已选择的旧三人视频，保持啦啦侠、阿芽酱、飒飒君的声音、人物关系、动作节奏、可爱表情和整体动画质感一致。
```

Then describe the new story. Always include:

```text
不要字幕，不要生成任何字幕、说明文字、下三分之一文字或画面文字。
```

