# 2026-05-09 Xiaoyunque Prompts And Methods

This records today's Xiaoyunque / ChatGPT browser workflow, prompt files, selected assets, and reusable CDP methods.

## Browser State

- Chrome DevTools endpoint: `http://127.0.0.1:9222`
- Working page id: `6F1A89EC31D145D87AD9753CF116F027`
- ChatGPT script thread: `https://chatgpt.com/c/69fc0bcd-4f2c-83ea-9117-46fc128a2496`
- Xiaoyunque page reached after submission: `https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=815ad9e4-9dcf-43b1-94fd-c73d7e15350f&source=home_prompt&entrance_from=home`

After applying the reference video and continuing into the generated thread, a `扫码支付 ¥50` modal was observed. The user later confirmed the video generation was already on the way and explicitly said not to care about publishing today. Do not keep clicking publish, recharge, or submit controls for this run; only record the workflow and artifacts.

## Current Short-Video Setup

Mode:

- `沉浸式短片`
- `Seedance 2.0 Fast`
- `15s`
- With reference video enabled after asset-library selection
- User confirmation after submit: video generation is on the way.
- Current instruction: no publishing work today; record only.

Prompt file used:

```text
references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s-numbered-assets.md
```

Important correction from the user:

- The bottom `+` menu is for attaching assets.
- Do not pretend old videos are referenced by writing them into the prompt only.
- Use `+ -> 从资产库选择` to select old generated videos.
- Do not use the `@引用素材` button for the old video reference.
- Always include `不要字幕` in the Chinese prompt.
- If the user says "select one or two and ask use its voice and characters", this means select one or two old videos from the asset library, not add a sentence pretending to reference them.

## Image Numbering

The prompt uses these fixed image numbers:

```text
图片1: /home/lachlan/ProjectsLFS/LALACHAN/display.png
图片2: /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
图片3: /home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
图片4: /home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
图片5: /home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Meaning:

- `图片1` is the LightMind AI glasses product image.
- `图片2` is the handmade patchwork notebook / book / menu / map prop.
- `图片3` is a new outfit reference for 啦啦侠.
- `图片4` is a new outfit / face reference for 飒飒君.
- `图片5` is the trio reference: left 啦啦侠, middle 阿芽酱, right 飒飒君.

## Reference Video Selection

Asset-library selection was done through the bottom `+` button:

```text
上传参考素材 -> 从资产库选择
```

Two old video assets were selected in the asset modal:

```text
资产 #7637271291062632985
资产 #7635834282704405017
```

The UI showed `已选 2 个素材` in the asset picker. After applying, the short-video composer accepted a single `@ 0:15` video reference and switched the billing text to a reference-video mode. The accepted visible video thumbnail was the three-character Mars/adventure reference. This suggests the current short composer may accept only one video reference alongside the five image references.

Use these selected old videos as voice / character / timing references. The prompt itself should still be about the new story, with only normal creative instructions such as "保持三人声音、人物关系和动作节奏一致".

Screenshots saved:

```text
references/screenshots/2026-05-09-xyq-plus-menu-open.png
references/screenshots/2026-05-09-xyq-two-reference-videos-selected.png
references/screenshots/2026-05-09-xyq-reference-video-applied.png
references/screenshots/2026-05-09-xyq-credit-modal.png
```

## Reusable CDP Tool Added

New script:

```text
scripts/xyq_cdp_browser.py
```

Verified with:

```bash
python3 -m py_compile scripts/xyq_cdp_browser.py
```

Useful commands:

```bash
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py visible 6F1A89EC31D145D87AD9753CF116F027
scripts/xyq_cdp_browser.py screenshot 6F1A89EC31D145D87AD9753CF116F027 /tmp/xyq.png
scripts/xyq_cdp_browser.py set-prompt 6F1A89EC31D145D87AD9753CF116F027 references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s-numbered-assets.md
scripts/xyq_cdp_browser.py click 6F1A89EC31D145D87AD9753CF116F027 484 753
```

Implementation methods:

- Uses Chrome DevTools Protocol over `websocket-client`.
- Uses `Runtime.evaluate` for DOM inspection and Tiptap prompt insertion.
- Uses `Input.dispatchMouseEvent` for reliable coordinate clicks.
- Uses `Page.captureScreenshot` for state evidence.
- Uses Tiptap `editor.commands.setContent(...)` instead of keyboard typing, because chunked keyboard insertion corrupted text earlier.

## Exact UI Steps That Worked

1. Keep working in the old Xiaoyunque tab.
2. Confirm the toolbar says `短片`, `2.0 Fast`, `15s`.
3. Upload or keep the five image references as `图片1` to `图片5`.
4. Click the bottom-left `+` button, not the `@` button.
5. In the opened menu, click `从资产库选择`.
6. Select one or two old generated trio videos from the asset modal.
7. Click `应用`.
8. Confirm the composer shows the image cards plus an `@ 0:15` reference video card.
9. Keep the prompt in Chinese and include `不要字幕`.
10. On submit, the page may enter an integrated-agent thread and show the insufficient-credit / payment modal.
11. If the user says generation is already underway, stop interacting with the page and record the state only.

## Exact Action Log For This Run

These are the concrete browser actions used before stopping:

```bash
# Set the cleaned, numbered prompt via Tiptap.
scripts/xyq_cdp_browser.py set-prompt 6F1A89EC31D145D87AD9753CF116F027 \
  references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s-numbered-assets.md

# Open bottom-left plus menu.
scripts/xyq_cdp_browser.py click 6F1A89EC31D145D87AD9753CF116F027 484 753

# Choose "从资产库选择".
scripts/xyq_cdp_browser.py click 6F1A89EC31D145D87AD9753CF116F027 573 659

# Select old reference videos in the modal by their checkboxes.
scripts/xyq_cdp_browser.py click 6F1A89EC31D145D87AD9753CF116F027 943 187
scripts/xyq_cdp_browser.py click 6F1A89EC31D145D87AD9753CF116F027 265 536

# Apply selected assets.
scripts/xyq_cdp_browser.py click 6F1A89EC31D145D87AD9753CF116F027 1104 713
```

Observed UI checkpoints:

- Before video selection: five image cards were visible as `图片1` to `图片5`.
- Asset modal: selected `资产 #7637271291062632985` and `资产 #7635834282704405017`.
- After applying: composer showed the five images plus one `@ 0:15` reference-video card.
- Header changed to a reference-video billing mode.
- Page later navigated to an integrated-agent thread.
- User confirmed the video generation is on the way and asked to record only.

## Prompt Archive

Today's active prompt:

```text
references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s-numbered-assets.md
```

Earlier related prompts and defaults:

```text
references/prompts/2026-05-09-hk-rainy-tea-restaurant-duanpian-15s.md
references/prompts/lala-aya-sasa-sushi-lightmind-cn.md
references/prompts/forest-dinosaur-portrait-15s.md
references/prompts/lala-miao-ikaku-lazy-chat.md
references/xyq-lala-aya-sasa-defaults.md
```

The active prompt is the authoritative one for this run because it has the corrected image numbering and the final `不要字幕` instruction.
