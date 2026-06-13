# Publish Video Procedure with LazyEdit, LALACHAN, and AutoPublish

This document records the full practical procedure for publishing a generated or recorded video through LazyEdit and the AutoPublish stack. It is intended for future Codex or AgInTi sessions that need to publish videos reliably with subtitle correction, metadata generation, logo burning, and platform monitoring.

## Scope

Use this workflow when a video should be published from LALACHAN, RARACHAN, local recordings, Nutstore AutoPublish imports, or an existing LazyEdit video entry.

The normal target platforms are:

- Shipinhao
- YouTube
- Instagram

If the user says `no sph`, `no shipinhao`, or asks for only YouTube and Instagram, do not publish Shipinhao.

If the user asks for only Shipinhao, reuse the existing processed output with `--no-process` unless a rerun is explicitly needed.

## System Map

LazyEdit backend and CLI:

```bash
/home/lachlan/DiskMech/Projects/lazyedit
http://127.0.0.1:18787
scripts/lazyedit_publish.py
```

LazyEdit Studio web UI:

```bash
http://127.0.0.1:18791/editor
```

LALACHAN repo:

```bash
/home/lachlan/ProjectsLFS/LALACHAN
```

LALACHAN generated videos:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/Videos
```

LALACHAN prompts, stories, and run notes:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/references/prompts
/home/lachlan/ProjectsLFS/LALACHAN/references/stories
/home/lachlan/ProjectsLFS/LALACHAN/references/xyq
```

Nutstore AutoPublish import folder:

```bash
/home/lachlan/Nutstore Files/AutoPublish/AutoPublish
```

AutoPubMonitor local repo and tmux session:

```bash
/home/lachlan/DiskMech/Projects/autopub-monitor
tmux session: autopub-monitor
```

Remote AutoPublish host:

```bash
ssh lachlan@lazyingart
/home/lachlan/Projects/autopub
tmux session: autopub
remote API: http://lazyingart:8081/publish
```

## Core Principle

Prefer the LazyEdit CLI:

```bash
scripts/lazyedit_publish.py
```

The CLI creates normal LazyEdit videos, process jobs, publish jobs, and queue records. That means the webapp publish tab stays synchronized with what the CLI does.

Avoid manual browser publishing unless the CLI or AutoPublish code is broken and you are debugging the platform automation itself.

## Environment Setup

Run from the LazyEdit repo:

```bash
cd /home/lachlan/DiskMech/Projects/lazyedit
source ~/miniconda3/etc/profile.d/conda.sh
conda activate lazyedit
```

Use `python`, not `python3`, after activating the conda environment.

## Preflight Checklist

Before publishing, identify these inputs:

- Source video path.
- Intended platforms.
- Whether Shipinhao is included.
- Context markdown path for generated videos.
- Whether to process from scratch or reuse an existing run.
- Whether subtitles should be burned. Default: yes.
- Whether corrected or polished subtitles should be used. Default: yes.
- Whether the existing LazyEdit logo should be burned. Default: yes.

For LALACHAN generated videos, find the matching context files:

```bash
find /home/lachlan/ProjectsLFS/LALACHAN/references -type f \
  \( -iname '*KEYWORD*.md' -o -iname '*story*.md' -o -iname '*run*.md' \)
```

Use the most specific prompt or story file as context. Usually the best file is under:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/references/prompts
```

The `references/xyq` run note is useful for provenance and verification, but the prompt or story file is usually better for subtitle correction. For metadata, create a separate short viewer-facing brief.

## Source Video Verification

Always verify the source video before uploading or publishing:

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height \
  -of json /absolute/path/to/video.mp4

sha256sum /absolute/path/to/video.mp4
```

Record duration, dimensions, size, and SHA256 when using direct upload. Pass them to the CLI for important generated videos:

```bash
--expect-sha256 SHA256
--expect-duration 33.467
--duration-tolerance 0.2
--expect-min-size-mb 44
--expect-max-size-mb 46
```

This prevents publishing the wrong `final_video (N).mp4` or stale copied file.

## Logo Preflight

For real publishes, burn the existing LazyEdit Studio logo at the top-left unless the user explicitly says no logo.

Check current logo settings:

```bash
curl -fsS http://127.0.0.1:18787/api/ui-settings/logo_settings | jq .
```

Required state:

```json
{
  "enabled": true,
  "logoPath": "...",
  "position": "top-left"
}
```

Do not invent or replace the logo. Use the configured webapp logo. Normal logo-burned outputs often end in:

```text
_subtitles_logo.mp4
```

## Subtitle and Language Defaults

Default behavior for real publishes:

- Use polished or corrected subtitles.
- Burn subtitles unless the user explicitly turns burning off.
- Use current Studio settings with `--use-current-settings`.
- Do not persist one-shot CLI overrides unless explicitly requested.

Important setting semantics:

- `--use-current-settings` reads the current webapp settings.
- `--languages` is bottom-to-top subtitle language order.
- `--persist-settings` writes options back to webapp preferences.
- Without `--persist-settings`, CLI overrides are one-shot and do not change Studio settings.
- `--no-process` reuses an already completed output.
- `--new-run` creates a separate publication run.
- Omitting `--new-run` normally uses the current output.

Typical current language setup is Traditional Chinese, Japanese, and English, with webapp layout slots controlling exact row positions.

## Subtitle Correction Philosophy

For generated videos, always use the corresponding script, prompt, or story as context for subtitle polish. Use a separate short metadata brief for metadata generation.

Treat the script as a reference, not a forced transcript.

Correction should follow a human middle path:

- Do not over-edit.
- Do not stay too conservative when ASR is obviously broken.
- Fix clear recognition errors.
- Fix broken names, objects, and phrases when context makes the intended meaning clear.
- Preserve timing and line structure where possible.
- Do not invent unsupported dialogue.
- If audio or generated content differs from the script, follow the likely spoken content, not the script verbatim.
- Read neighboring subtitle lines to decide whether a sentence makes sense.
- Use context to infer likely phrases when Whisper output is abnormal, fragmented, or inconsistent.

For example, if the script says a character is rescuing zongzi and the ASR produces a broken unrelated phrase, correct toward the likely zongzi sentence only when the surrounding lines support it.

## Metadata Context Philosophy

For generated videos, the script or prompt is background context, not the final metadata text.

Do not let metadata become a full script summary, a scene-by-scene storyboard, or an over-detailed dump of every line. Metadata should be platform-facing: concise, attractive, searchable, and faithful to the actual video.

Important operational rule: split subtitle context from metadata context. Use the full script with `--correction-prompt-file`, and create a short temporary metadata brief for `--metadata-prompt-file`. Avoid `--prompt-file FULL_SCRIPT.md` when the processing step includes `metadata_zh` or `metadata_en`, because that can make the generated metadata read like the entire script.

Use the script to understand:

- main characters;
- setting and mood;
- central conflict or joke;
- culturally important objects;
- correct names and terms;
- likely subtitle corrections;
- good keywords and hashtags.

Do not copy the script structure into title, description, or captions. Avoid phrasing like “the story begins with...” followed by every beat unless the platform specifically benefits from a short synopsis. Prefer a compact hook plus a short context paragraph.

Recommended metadata shape:

- Title: one clear hook, usually under 80 characters for YouTube and shorter for Chinese platforms.
- Short description: 2 to 4 sentences summarizing the premise, emotional tone, and payoff.
- Tags or hashtags: 8 to 15 relevant terms, not every story object.
- Shipinhao caption: natural Chinese or Traditional Chinese, friendly and concise.
- YouTube description: English or bilingual if appropriate, but not a full script.
- Instagram caption: short hook, mood, and hashtags.

Bad metadata pattern:

```text
This video shows A saying line 1, then B says line 2, then C moves left, then D explains...
```

Good metadata pattern:

```text
A playful Dragon Boat Festival animation where Lala Xia, Aya Chan, Sasa Kun, and robot Zhuangzi turn a race into a teamwork rescue mission. Cute festival energy, zongzi chaos, and a warm shared ending.
```

When a generated-video prompt is long, compress it before metadata generation mentally or in a temporary note. Keep the essence, not the full storyboard. The metadata should sell and explain the finished video, not expose the production script.

## Why `--no-correct-subtitles` Is Often Used for New Uploads

For a brand-new video, standalone subtitle correction may require an existing transcript. If there is no transcript yet, direct correction can be premature.

For new uploads, the safer default is:

```bash
--correction-prompt-file PROMPT.md
--metadata-prompt-file temp/metadata_brief.md
--no-correct-subtitles
--steps keyframes,caption,transcribe,polish,translate,burn,metadata_zh,metadata_en,cover
```

This uses the full prompt as context for polish and the short metadata brief for metadata during the pipeline, after transcription exists.

Use `--correct-subtitles` only when the video already has a transcript or when the correction endpoint is known to operate after transcription in the selected flow.

## Direct Upload and Publish All Platforms

Use this for a generated video that is not already in LazyEdit:

```bash
cd /home/lachlan/DiskMech/Projects/lazyedit
source ~/miniconda3/etc/profile.d/conda.sh
conda activate lazyedit

python scripts/lazyedit_publish.py \
  --video /home/lachlan/ProjectsLFS/LALACHAN/Videos/VIDEO.mp4 \
  --title VIDEO_TITLE_COMPLETED \
  --expect-sha256 SHA256 \
  --expect-duration DURATION_SECONDS \
  --duration-tolerance 0.2 \
  --expect-min-size-mb MIN_MB \
  --expect-max-size-mb MAX_MB \
  --use-current-settings \
  --correction-prompt-file /home/lachlan/ProjectsLFS/LALACHAN/references/prompts/PROMPT.md \
  --metadata-prompt-file temp/metadata_brief.md \
  --no-correct-subtitles \
  --steps keyframes,caption,transcribe,polish,translate,burn,metadata_zh,metadata_en,cover \
  --platforms shipinhao,youtube,instagram \
  --guided-monitor \
  --remote-log-command "ssh lachlan@lazyingart 'tmux capture-pane -pt autopub:0 -S -140 | tail -n 140'" \
  --wait \
  --poll-seconds 10 \
  --process-timeout 3600 \
  --publish-timeout 7200
```

Use a stable title ending in `_COMPLETED` when creating a new LazyEdit video.

## Direct Upload Without Shipinhao

Use this when the user says no Shipinhao:

```bash
python scripts/lazyedit_publish.py \
  --video /home/lachlan/ProjectsLFS/LALACHAN/Videos/VIDEO.mp4 \
  --title VIDEO_TITLE_COMPLETED \
  --expect-sha256 SHA256 \
  --expect-duration DURATION_SECONDS \
  --duration-tolerance 0.2 \
  --use-current-settings \
  --correction-prompt-file /home/lachlan/ProjectsLFS/LALACHAN/references/prompts/PROMPT.md \
  --metadata-prompt-file temp/metadata_brief.md \
  --no-correct-subtitles \
  --steps keyframes,caption,transcribe,polish,translate,burn,metadata_zh,metadata_en,cover \
  --platforms youtube,instagram \
  --guided-monitor \
  --remote-log-command "ssh lachlan@lazyingart 'tmux capture-pane -pt autopub:0 -S -140 | tail -n 140'" \
  --wait \
  --poll-seconds 10 \
  --process-timeout 3600 \
  --publish-timeout 7200
```

## Publish Shipinhao Later from Existing Processed Output

If YouTube and Instagram were already published and the user later asks to publish to Shipinhao, reuse the existing processed video:

```bash
python scripts/lazyedit_publish.py \
  --video-id VIDEO_ID \
  --use-current-settings \
  --platforms shipinhao \
  --no-process \
  --guided-monitor \
  --remote-log-command "ssh lachlan@lazyingart 'tmux capture-pane -pt autopub:0 -S -140 | tail -n 140'" \
  --wait \
  --poll-seconds 10 \
  --publish-timeout 7200
```

This avoids duplicate processing and preserves the exact subtitles, logo, cover, and metadata already produced.

## Publish Existing LazyEdit Video with Context

If the video already appears in the LazyEdit publish tab, find its video id:

```bash
curl -fsS http://127.0.0.1:18787/api/videos | jq '.videos[:20] | map({id,title,created_at,file_path})'
```

Then process and publish:

```bash
python scripts/lazyedit_publish.py \
  --video-id VIDEO_ID \
  --use-current-settings \
  --correction-prompt-file /absolute/path/to/full-script-or-context.md \
  --metadata-prompt-file temp/metadata_brief.md \
  --no-correct-subtitles \
  --steps keyframes,caption,transcribe,polish,translate,burn,metadata_zh,metadata_en,cover \
  --platforms shipinhao,youtube,instagram \
  --guided-monitor \
  --remote-log-command "ssh lachlan@lazyingart 'tmux capture-pane -pt autopub:0 -S -140 | tail -n 140'" \
  --wait \
  --poll-seconds 10
```

## Nutstore Import Path

If the user asks to copy to Nutstore AutoPublish folder, copy with a stable `_COMPLETED` filename:

```bash
cp -f /home/lachlan/ProjectsLFS/LALACHAN/Videos/VIDEO.mp4 \
  "/home/lachlan/Nutstore Files/AutoPublish/AutoPublish/VIDEO_COMPLETED.mp4"
```

Then monitor AutoPubMonitor panes:

```bash
tmux capture-pane -pt autopub-monitor:0.1 -S -100 | tail -n 100
tmux capture-pane -pt autopub-monitor:0.2 -S -100 | tail -n 100
```

Avoid recopying the same video repeatedly. Recopying can create duplicate LazyEdit entries or duplicate platform posts.

## Monitoring Local LazyEdit Processing

The CLI prints process status. Normal progression is:

```text
keyframes:done
caption:done
transcribe:done
polish:done
translate:done
burn:done
metadata_zh:done
metadata_en:done
cover:done
```

If it stalls, inspect the LazyEdit tmux session:

```bash
tmux capture-pane -pt lazyedit:0 -S -180 | tail -n 180
```

Look for:

- Whisper or torchaudio errors.
- GPU out-of-memory errors.
- Segmentation faults.
- HandBrake conversion errors.
- Missing metadata JSON.
- Failed cover extraction.

Do not start duplicate processing unless the current process is confirmed dead or irrelevant.

## Monitoring Remote AutoPublish

With `--guided-monitor`, the CLI prints the local and remote job ids.

Example final state:

```text
Publish job 178: done remote=done remote_id=job-1781245713366-37
Remote AutoPublish: done id=job-1781245713366-37
```

Watch remote logs:

```bash
ssh lachlan@lazyingart 'tmux capture-pane -pt autopub:0 -S -140 | tail -n 140'
```

Successful platform signals:

```text
Successfully published on ShiPinHao.
Instagram publish confirmed.
Successfully published on Instagram.
Video published successfully.
Successfully published on YouTube.
```

## Shipinhao Specific Notes

Shipinhao may require login through a QR code email. The automation intentionally waits a long time for login. Do not shorten this wait.

Expected sequence:

```text
Login iframe detected
Email sent successfully
Login required, will check again
Logged in successfully
Shipinhao editor is ready
Video uploading
Upload preview is ready
Shipinhao post-upload editor is stable
Skipping cover upload
Description set
Collection selected
Cover state before publish: coverReady true
Save draft result
Publish button ready
Successfully published on ShiPinHao
```

Important behavior:

- Wait for upload completion before publishing.
- Wait for cover generation before publishing.
- Save draft before final publish when supported.
- Skip cover upload because the current UI no longer requires it.
- Select the existing collection when possible.
- Short title may not exist in the new UI; skip it if absent.

## YouTube Specific Notes

Expected sequence:

```text
Attached video ..._highlighted.mp4
Upload complete
Title set
Description set
Thumbnail attached
Playlist selected: SimpleLife
Not Made for Kids selected
Tags entered
Checks complete. No issues found.
Publish button clicked
Video published successfully
```

Use generated English metadata for YouTube when available.

If Chinese metadata accidentally appears in English or English metadata is malformed, inspect the metadata prompt and generated JSON before publishing.

## Instagram Specific Notes

Expected sequence:

```text
Instagram already logged in
Set crop to Original
Clicking Next
Adding caption
Clicking Share
Instagram publish confirmed
Successfully published on Instagram
```

A crop-menu timeout after the first successful crop selection is usually not fatal if the post continues to Next and Share.

## Metadata Requirements

Metadata should be generated from both visual captions and the provided context prompt.

For LALACHAN generated videos:

- Use the script as story background.
- Metadata should describe the actual generated video and intended story without dumping the whole script.
- Keep metadata concise and viewer-facing; avoid overwhelming descriptions that reveal every scene beat.
- Do not let Chinese metadata become English unless the target metadata is English.
- YouTube can use English title/description/tags.
- Shipinhao can use Chinese or Traditional Chinese title/description.
- Instagram can use a caption with hashtags and multilingual context when useful.

If the user provides a company name or exact background, include it in metadata prompt context and subtitle correction notes.

## Common Failure Modes and Fixes

Wrong video selected:

- Cause: multiple `final_video (N).mp4` files or stale LALACHAN video copies.
- Fix: verify SHA256, duration, dimensions, and file size before upload.
- Use `--expect-sha256`, `--expect-duration`, and size bounds.

Protected Xiaoyunque download URL fails:

- Cause: final video URL cannot be downloaded outside the browser.
- Fix: use the browser watcher fallback to click the visible `下载` button and copy the newest valid MP4 from `~/Downloads`.
- Quote paths because files may be named `final_video (5).mp4`.

Missing subtitles after publish:

- Cause: subtitle burning was off, `--no-burn-subtitles` was used, or a non-processed output was published.
- Fix: use current settings, verify `burnSubtitles=true`, and process with the `burn` step.

Non-polished subtitles used:

- Cause: published original transcript or reused an old output.
- Fix: use `--use-current-settings`, ensure `subtitleSourceVersion=polished`, and include `polish` before `burn`.

Metadata JSON missing:

- Cause: a publication session path did not contain expected metadata, or metadata generation did not finish.
- Fix: rerun metadata steps or publish from the current completed output.

Shipinhao publish button disabled:

- Cause: cover still generating, upload not complete, or editor not stable.
- Fix: wait for upload preview and cover readiness; do not click publish early.

Remote queue says done but one platform did not publish:

- Cause: platform automation swallowed a transient browser issue or logs were not inspected.
- Fix: check remote `autopub` tmux logs and queue API if available, then rerun only the missing platform with `--no-process`.

Transcription segfault or Whisper failure:

- Cause: model, CUDA, torchaudio, torchcodec, triton, or memory issue.
- Fix: inspect `lazyedit` tmux logs. Avoid rerunning blindly. Use smaller model or CPU fallback only if the code path supports it.

AutoPubMonitor dropped a queued item:

- Old cause: wrapper returned success even when LazyEdit upload failed.
- Expected fix: wrapper should propagate Python exit code so queue entries are not silently dropped.

## Recovery for Valid Completed Subtitles but Failed Status

Sometimes a duplicate late Whisper run can mark `transcribe:error` after valid polished subtitles already exist.

Symptoms:

```text
process-status shows transcribe:error
*_mixed_polished.json exists
*_mixed_polished.srt exists
*_mixed_polished.md exists
Downstream burn or metadata may already be done
```

First stop only a clearly redundant duplicate worker:

```bash
ps -eo pid,ppid,cmd | rg 'vad_lang_subtitle|HandBrakeCLI|scripts/lazyedit_publish.py'
kill PID
```

Then repair the transcription status only if the files are verified. Insert a completed mixed row pointing to the verified polished files:

```bash
source .env 2>/dev/null || true
psql "${LAZYEDIT_DATABASE_URL:-${DATABASE_URL:-dbname=lazyedit_db}}" -v ON_ERROR_STOP=1 -c "
INSERT INTO transcriptions (
  video_id, language_code, status,
  output_json_path, output_srt_path, output_md_path,
  error, publication_session_id
) VALUES (
  VIDEO_ID, 'mixed', 'completed',
  '/abs/path/to/VIDEO_compatible_mixed_polished.json',
  '/abs/path/to/VIDEO_compatible_mixed_polished.srt',
  '/abs/path/to/VIDEO_compatible_mixed_polished.md',
  NULL, NULL
);"
```

This is a status repair, not a content rewrite.

## Recommended Final Report Format

After a successful publish, report:

```text
Published successfully.

Video: VIDEO.mp4
LazyEdit video id: N
LazyEdit publish job: N
Remote AutoPublish job: job-...
Platforms: Shipinhao, YouTube, Instagram
Final status: done
Context used: /path/to/prompt.md
```

Also mention whether:

- polished subtitles were used;
- subtitles were burned;
- LazyEdit logo was enabled;
- no code changes were made;
- any platform was intentionally skipped.

## Do Not Do These

Do not publish the same video multiple times unless the user explicitly asks.

Do not publish to Shipinhao when the user says no Shipinhao.

Do not rerun processing when the user says same version, last run, current run, or no rerun.

Do not use non-polished subtitles for real publishes unless explicitly requested.

Do not change persisted webapp settings unless the user asks.

Do not invent a new logo or replace the existing webapp logo.

Do not recopy to Nutstore repeatedly to trigger processing.

Do not manually delete or reset user data without explicit permission.

Do not shorten the Shipinhao login wait; the user may need time to scan the QR code.

## Practical Examples

Publish a new LALACHAN video to all platforms with context:

```bash
python scripts/lazyedit_publish.py \
  --video /home/lachlan/ProjectsLFS/LALACHAN/Videos/dragon_boat_robot_race_30s_2026-06-12.mp4 \
  --title dragon_boat_robot_race_30s_2026_06_12_COMPLETED \
  --expect-sha256 88e0e4c5252ae7b5a8498ff96f1b769f026eda7c05accc6f44f2dd235319d64e \
  --expect-duration 33.467 \
  --duration-tolerance 0.2 \
  --expect-min-size-mb 44 \
  --expect-max-size-mb 46 \
  --use-current-settings \
  --prompt-file /home/lachlan/ProjectsLFS/LALACHAN/references/prompts/2026-06-12-dragon-boat-robot-race-30s.md \
  --no-correct-subtitles \
  --steps keyframes,caption,transcribe,polish,translate,burn,metadata_zh,metadata_en,cover \
  --platforms shipinhao,youtube,instagram \
  --guided-monitor \
  --remote-log-command "ssh lachlan@lazyingart 'tmux capture-pane -pt autopub:0 -S -140 | tail -n 140'" \
  --wait \
  --poll-seconds 10 \
  --process-timeout 3600 \
  --publish-timeout 7200
```

Publish the same already processed video to Shipinhao only:

```bash
python scripts/lazyedit_publish.py \
  --video-id 372 \
  --use-current-settings \
  --platforms shipinhao \
  --no-process \
  --guided-monitor \
  --remote-log-command "ssh lachlan@lazyingart 'tmux capture-pane -pt autopub:0 -S -140 | tail -n 140'" \
  --wait \
  --poll-seconds 10 \
  --publish-timeout 7200
```

Publish to YouTube and Instagram only:

```bash
python scripts/lazyedit_publish.py \
  --video-id VIDEO_ID \
  --use-current-settings \
  --platforms youtube,instagram \
  --no-process \
  --wait \
  --poll-seconds 10
```

## Operator Checklist Before Pressing Publish

- Source video path is correct.
- Prompt/story context matches the video.
- SHA256 or duration check prevents wrong-file publish.
- Logo settings are enabled and top-left.
- Subtitle source is polished or corrected.
- Burn subtitles is enabled unless explicitly disabled.
- Platform list exactly matches user request.
- Shipinhao is excluded if user says no sph.
- Use `--no-process` only when existing output is known good.
- Use `--wait` and monitor until final status is done or failed.
- If failed, inspect local and remote logs before retrying.
