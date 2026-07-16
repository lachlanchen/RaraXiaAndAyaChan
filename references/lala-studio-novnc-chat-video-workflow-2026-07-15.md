# Lala Studio noVNC Chat-to-Video Workflow

This run validated a first-party story studio that can write, review, save, prepare, and generate a LALACHAN video through explicit visible browser controls.

## Isolated Desktop

The Studio browser is isolated from Xiaoyunque, JLCEDA, and AgenticApp automation:

| Service | Address |
| --- | --- |
| Lala Studio | `http://127.0.0.1:4412` |
| noVNC | `http://127.0.0.1:6116/vnc_lite.html?host=127.0.0.1&port=6116&autoconnect=1&scale=1` |
| Chrome CDP | `http://127.0.0.1:9466` |
| X display | `:96` |
| Browser profile | `${XDG_CACHE_HOME:-$HOME/.cache}/lala-studio-browser` |

Start or inspect it from the standalone `LalaStudio` repository:

```bash
scripts/launch_studio_novnc.sh start --project-root "$LALACHAN_ROOT"
node tools/lala-studio-browser.mjs status
node tools/lala-studio-browser.mjs screenshot --label operator-check
```

The controller operates the visible DOM through Playwright over CDP. It does not bypass the webapp with hidden API mutations. It reuses one Studio tab and captures evidence after every command.

## Chat-to-Video Contract

1. Select a story in the Studio library.
2. Ask the Studio chat to draft, review, or finalize it.
3. Apply the assistant response and save it through visible buttons.
4. Ask for video generation in chat. The app parses mode, model, ratio, duration, references, and subtitle policy into a visible production card.
5. Inspect or prepare freely. Paid generation requires both an explicit user request and `--confirm-paid`.
6. The execution job uses one accountable executor, uploads real files, verifies visible settings, submits once, monitors the existing thread, downloads, and probes the result.

Example paid action after inspection:

```bash
node tools/lala-studio-browser.mjs production \
  --operation generate \
  --confirm-paid \
  --wait-seconds 7200
```

## Validated Run

- Story: `references/stories/2026-07-15-qiandaohu-grass-mat-glide-15s.md`
- Output: `Videos/2026-07-15-qiandaohu-grass-mat-glide-15s.mp4`
- Xiaoyunque mode: 沉浸式短片
- Model: Seedance 2.0 Mini 体验版
- Format: 15 seconds, 4:3, no subtitles
- References: words card, 庄子 robot, LightMind glasses, notebook, 啦啦侠, 阿芽酱, 飒飒君; no Trio image
- Result probe: `15.047s`, `960x720`, H.264 video, AAC stereo audio
- SHA-256: `ba82157fd0d6a049ad3f066cbde1abe5a8466a5b4cc18061d9f139011e14a97c`

## Failure Learned

The first watcher implementation inspected all page-level video elements and initially found a 371-second promotional video. That file was rejected because its duration did not match the 15-second contract.

The durable fix is in `scripts/xyq_chrome/watch_thread_dom_download.py`:

- resolve media from the current result card or visible result preview;
- pass `--expected-duration` to the watcher;
- reject candidates outside the configured duration tolerance;
- open the result preview before using its native download control when needed;
- support protected browser-context blob downloads;
- verify copied files with `ffprobe` and SHA-256.

Never resubmit a paid job to fix a download problem. Preserve the completed thread, repair the watcher, and recover the already-generated artifact.

## Reusable Skill

The generic workflow is packaged as `novnc-webapp-control`. Its core rules are dedicated browser isolation, semantic selectors, visible control, evidence-backed validation, one paid submit, and artifact identity checks. The Xiaoyunque-specific details remain in `lalachan-xyq-browser-video` rather than being hard-coded into the generic skill.
