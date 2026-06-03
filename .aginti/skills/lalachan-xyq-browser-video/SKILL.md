---
id: lalachan-xyq-browser-video
label: LALACHAN Xiaoyunque Browser Video
description: Prepare, generate, monitor, download, and archive LALACHAN Xiaoyunque/Seedance videos through the logged-in Chrome/CDP browser workflow; use project defaults for Lala Xia, Rara Xia, Aya Chan, Sasa Kun, reference images, no-subtitle prompts, evidence capture, and browser-first validation.
triggers:
  - lalachan
  - lala xia
  - rara xia
  - aya chan
  - sasa kun
  - xiaoyunque
  - xyq
  - 小云雀
  - 沉浸式短片
  - seedance
  - 参考视频
  - 素材库
  - 不要字幕
  - no subtitles
  - browser video
tools:
  - run_command
  - read_file
  - write_file
  - search_files
  - read_image
  - open_url
  - click
  - type
  - press
  - wait
  - tmux_list_sessions
  - tmux_capture_pane
  - tmux_send_keys
---

# LALACHAN Xiaoyunque Browser Video

Use this project-local skill for LALACHAN Xiaoyunque video generation tasks. It is intentionally local so AgInTiFlow core stays general.

## Boundary

Do not move LALACHAN-specific defaults into AgInTiFlow core:

- no hard-coded `Trio.png`;
- no hard-coded Xiaoyunque thread IDs;
- no hard-coded `沉浸式短片`, `15s`, or `Seedance 2.0 Fast` in core code;
- no hard-coded RaraXia, Aya Chan, Sasa Kun, or Lala Xia identities in core code;
- no hard-coded Nutstore copy paths in core code.

AgInTiFlow core should provide general browser reconciliation, upload verification, pre-submit validation, evidence logging, watcher/retry loops, SCS validation, interrupt control, and download handling. This skill provides LALACHAN defaults.

## Default Policy

Use the logged-in Chrome/CDP browser workflow by default. Do not use the Xiaoyunque API unless the user explicitly asks for API generation.

Preserve the user's current browser state. Prefer the current visible Xiaoyunque tab. Do not open new tabs unless the current tab is unusable or the user asks.

For normal short videos, default to:

- Mode: `沉浸式短片`.
- Duration: `15s`.
- Model: `Seedance 2.0 Fast`, non-VIP unless the user requests VIP.
- Language: mainly Chinese.
- Prompt must mention: `不要字幕，不要生成字幕，不要文字遮挡角色脸部`.

## Project Paths

Work from:

```bash
cd /home/lachlan/ProjectsLFS/LALACHAN
```

Default reference images:

```text
/home/lachlan/ProjectsLFS/LALACHAN/display.png
/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
/home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Character and prop mapping:

- Lala Xia / Rara Xia: giant panda character.
- Aya Chan: red panda character.
- Sasa Kun: boy character.
- `display.png`: LightMind AI glasses, used when glasses appear.
- `patchwork-leather-notebook-luxury-clean-v2.png`: handmade notebook, used as book, menu, map, score sheet, prop, or tool.

## Required Browser Workflow

Before any submit action, reconcile browser state:

1. Find the active Chrome/CDP page.
2. Bring the target Xiaoyunque page to front.
3. Confirm the visible page is the same page being controlled.
4. Confirm mode is `沉浸式短片`.
5. Confirm model is `Seedance 2.0 Fast` and not VIP if the user requested non-VIP.
6. Confirm duration is `15s`.
7. Upload or select required images.
8. Select reference video from `+` button, then `从资产库选择`, not `@`, unless the user explicitly asks for `@`.
9. Verify visible attachment thumbnails/counts/filenames.
10. Fill prompt.
11. Verify prompt contains no-subtitle instruction.
12. Submit only if the user asked to submit.

Useful existing helper commands:

```bash
cd /home/lachlan/ProjectsLFS/LALACHAN
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py visible PAGE_ID
scripts/xyq_cdp_browser.py bring-to-front PAGE_ID
scripts/xyq_cdp_browser.py select-mode PAGE_ID "沉浸式短片"
```

Use project scripts when available. If a helper fails, inspect DOM/screenshot and continue with browser tools.

## Evidence Required

Never claim completion without evidence.

For prepare-only tasks, record:

- active page ID;
- URL;
- selected mode;
- selected model;
- selected duration;
- uploaded image count;
- reference video selected or reason missing;
- prompt saved path;
- screenshot path if possible;
- whether submit was intentionally skipped.

For generation tasks, record:

- submit time;
- thread URL;
- generation status;
- download path;
- copied output path;
- final MP4 exists and has nonzero size.

For Nutstore copy tasks, record destination path.

## Failure Handling

If upload verification fails, do not submit.

If model remains VIP while the user requested non-VIP, do not submit.

If duration cannot be set to 15s, do not submit.

If the page is stuck loading, try focusing the address bar and pressing Enter, then wait and re-check.

If Xiaoyunque reports credits insufficient, login required, captcha, internal error, or blocked generation, stop with screenshot/evidence and explain.

If a direct download URL returns `403`, use the logged-in browser download path or copy from `~/Downloads`.

## SCS Expectations

For this workflow, prefer SCS validation because completion depends on visible browser state and durable evidence.

Committee plans the browser steps and acceptance criteria.

Supervisor executes browser actions.

Student validates evidence before accepting finish.

Student must reject completion if any required state is unproven:

- wrong mode;
- wrong model;
- wrong duration;
- missing images;
- missing reference video when requested;
- prompt not filled;
- submit claimed without visible evidence;
- downloaded file not present.

If rejected, Committee proposes a revised plan and Supervisor retries.

## Dry-Run Prompt

For a safe test without submitting:

```text
Prepare a LALACHAN Xiaoyunque 15s 沉浸式短片 with the five default images, Seedance 2.0 Fast non-VIP, reference video from asset library, fill the prompt, but do not submit.
```

## When To Improve AgInTiFlow Core

Only improve AgInTiFlow core if the problem is general:

- browser helper cannot reliably identify visible tab;
- uploads cannot be verified generically;
- SCS accepts executor claims without evidence;
- long-running generation cannot be monitored;
- downloads cannot be detected or copied generally;
- Esc/interrupt does not stop active work;
- validator cannot compare task contract to evidence.

Keep LALACHAN defaults in this skill, not in core.
