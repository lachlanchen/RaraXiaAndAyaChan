# 2026-05-10 Moon Universe Fight Prep

This records the prepared Xiaoyunque browser state for tomorrow's Lala/Aya/Sasa short video. The generation button was not clicked.

## Source Script

ChatGPT thread:

```text
https://chatgpt.com/c/69fc0bcd-4f2c-83ea-9117-46fc128a2496
```

Saved files:

```text
Lala-Aya-Sasa-draft/2026-05-10-moon-universe-fight-synopsis.md
Lala-Aya-Sasa-draft/2026-05-10-moon-universe-fight-chatgpt.md
Lala-Aya-Sasa-draft/2026-05-10-moon-universe-fight-retry-prompt.md
Lala-Aya-Sasa-draft/2026-05-10-moon-universe-fight-chatgpt-retry.md
references/prompts/2026-05-10-moon-universe-fight-duanpian-15s-numbered-assets.md
```

The first ChatGPT answer only returned `LightMindLightMind`, so a retry prompt was sent. The retry answer was saved, then polished into the final Xiaoyunque prompt with fewer lines of dialogue and an explicit no-subtitles instruction.

## Xiaoyunque Composer State

Target tab:

```text
https://xyq.jianying.com/home?tab_name=home
```

Prepared mode:

```text
沉浸式短片
Seedance 2.0 Fast
15s
```

Uploaded references in this order:

```text
图片1 /home/lachlan/ProjectsLFS/LALACHAN/display.png
图片2 /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
图片3 /home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
图片4 /home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
图片5 /home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Selected old reference video from the bottom `+` menu via `从资产库选择`:

```text
资产 #7637271291062632985
Duration: 15s
Reason: old generated trio video in a Mars/space scene, useful for character, voice, and sci-fi movement reference.
```

The prompt includes:

```text
不要字幕，不要生成任何字幕、说明文字、下三分之一文字或画面文字。
```

## Browser Automation Commands

Main helper:

```bash
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py visible 6F1A89EC31D145D87AD9753CF116F027
scripts/xyq_cdp_browser.py set-prompt 6F1A89EC31D145D87AD9753CF116F027 references/prompts/2026-05-10-moon-universe-fight-duanpian-15s-numbered-assets.md
```

Direct image upload used Chrome DevTools `DOM.setFileInputFiles`:

```bash
scripts/xyq_cdp_browser.py set-file-input 6F1A89EC31D145D87AD9753CF116F027 \
  display.png \
  patchwork-leather-notebook-luxury-clean-v2.png \
  R1.jpg.jpeg \
  R3.jpg.jpeg \
  Trio.png \
  --selector 'input[type=file]' \
  --index 0
```

The old video was selected manually through the browser UI:

1. Click bottom `+` button.
2. Choose `从资产库选择`.
3. Select `资产 #7637271291062632985`.
4. Click `应用`.
5. Stop before clicking the final create arrow.

## Verification

Verified final state:

```text
Toolbar: 短片 / 2.0 Fast / 参考 / 15s
Prompt length: 825 characters
No-subtitle text present: yes
Preview media: 图片1-5 plus one 0:15 video
Create button enabled: yes
Create button clicked: no
```

Screenshots:

```text
references/screenshots/2026-05-10-moon-universe-fight-before-asset-select.png
references/screenshots/2026-05-10-moon-universe-fight-asset-modal.png
references/screenshots/2026-05-10-moon-universe-fight-prepared.png
```
