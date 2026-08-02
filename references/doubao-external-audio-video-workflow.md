# Doubao External-Audio Video Workflow

Use the shared Xiaoyunque Chrome profile and visible noVNC desktop:

```text
Profile: ~/.cache/xyq-chrome
CDP: http://127.0.0.1:9344
noVNC: http://127.0.0.1:6099/vnc.html?host=127.0.0.1&port=6099&autoconnect=1&resize=scale
```

## Prepare

Log into Doubao visibly first. Then run:

```bash
python scripts/doubao_cdp_browser.py open
python scripts/doubao_cdp_browser.py status
python scripts/doubao_cdp_browser.py prepare \
  --prompt-file references/MusiaVideo/PROJECT/DOUBAO_PROMPT.md \
  --audio /path/to/song.mp3 \
  --image /path/to/reference.png \
  --screenshot outputs/doubao/PROJECT-prepared.png
```

The prepare command selects video generation, uploads the external soundtrack
and references, fills the prompt, records evidence, and does **not** submit.
Check visible attachment chips because Doubao may change its upload controls.

## Submit

Submit once, only after visible validation and explicit approval:

```bash
python scripts/doubao_cdp_browser.py submit --confirm-paid
```

Monitor and download the completed card:

```bash
python scripts/doubao_cdp_browser.py result --activate
python scripts/doubao_cdp_browser.py download --output Videos/result.mp4
```

When the active mode cannot accept audio, lock the reviewed soundtrack after
download:

```bash
scripts/doubao_lock_soundtrack.sh \
  Videos/result.mp4 reviewed-song.mp3 Videos/result-song-locked.mp4 0
```

Never retry merely because a result is slow. If the task is queued or credits
changed, monitor the existing task. Download the result, verify duration and
audio streams with `ffprobe`, and keep the external soundtrack as the final
audio authority when Doubao changes it.

## Recovery

- Login missing: stop and let the user log in through noVNC.
- Page partly loaded: foreground the tab, then use Ctrl+L and Enter visibly.
- No file input: open the visible attachment control before rerunning upload.
- Audio upload unsupported in the selected video mode: generate visuals from
  the image and prompt, then mux the external track locally with FFmpeg.
- A realistic human-face reference is rejected: keep it as local composition
  guidance and retry in the same conversation as text-to-video without that
  attachment. Do not weaken the requested realism unless text-to-video also
  rejects it.
- Never paste local paths into the creative prompt.

## Verified 2026-08-02 Behavior

- Doubao video mode exposed Seedance 2.0 Mini with automatic `10s` generation.
- Its file input accepted images only; direct MP3 upload was unavailable.
- A photorealistic face reference image was rejected by portrait protection.
- Text-to-video with the same realistic goddess direction was accepted using
  the daily free quota.
- The completed result card lazy-loads its `<video>` only after the card is
  opened; `download` handles that activation before resolving the signed MP4.
