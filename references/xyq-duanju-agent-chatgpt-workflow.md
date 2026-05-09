# Xiaoyunque 短剧 Agent ChatGPT Draft Workflow

Recorded on `2026-05-08`.

This workflow prepares the Xiaoyunque short-drama Agent from the saved ChatGPT script conversation.

## Fixed Inputs

ChatGPT source conversation:

```text
https://chatgpt.com/c/69fc0bcd-4f2c-83ea-9117-46fc128a2496
```

Short-drama Agent workspace:

```text
https://xyq.jianying.com/novel/list?enter_from=small_tool
```

Default character image:

```text
/home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Draft files:

```text
Lala-Aya-Sasa-draft/duanju-agent-chatgpt-sushi.md
Lala-Aya-Sasa-draft/duanju-agent-chatgpt-sushi.txt
```

The `.txt` file is used for Xiaoyunque because the short-drama upload control accepts `.txt` and `.docx`.

## Script

```bash
scripts/xyq_chrome/prepare_duanju_from_chatgpt.py
```

Default behavior:

- Reuses `XYQ_TRIO_ASSET_ID` from `.env` if available.
- Otherwise uploads `Trio.png` through the Xiaoyunque skill API.
- Opens the dedicated short-drama Agent tab.
- Uploads the `.txt` draft into the page.
- Waits until the `剧本解析` button appears.
- Writes a no-secret JSON log.
- Does not submit generation.

Run:

```bash
scripts/xyq_chrome/prepare_duanju_from_chatgpt.py
```

Output log:

```text
outputs/xyq-duanju-agent-chatgpt-prepare.json
```

## Latest Result

The latest run uploaded:

```text
Lala-Aya-Sasa-draft/duanju-agent-chatgpt-sushi.txt
```

The browser confirmed:

```text
hasParseButton: true
submitted_generation: false
```

The Trio image is recorded as the default character reference asset in local `.env`.
