# LazyEdit Video Publish Handoff Note

Use this note when handing a LALACHAN-generated video to LazyEdit for subtitle correction, metadata generation, and publishing.

## Default Publish Path

Use LazyEdit CLI from:

```bash
cd /home/lachlan/DiskMech/Projects/lazyedit
source ~/miniconda3/etc/profile.d/conda.sh
conda activate lazyedit
```

Use `scripts/lazyedit_publish.py` so the webapp queue stays synchronized.

## Normal Defaults

- Use current Studio settings with `--use-current-settings`.
- Use polished/corrected subtitles.
- Burn subtitles unless the user explicitly disables it.
- Burn the existing LazyEdit webapp logo. Current LALACHAN/MV default is top-right.
- Use the corresponding LALACHAN prompt/story markdown as context.
- Publish only to the platforms requested by the user.
- For Xiaoyunque/LALACHAN generation tasks, always auto-download the finished
  MP4, copy it to `Videos/`, and submit it to LazyEdit. Direct CLI upload is
  preferred; Nutstore AutoPublish import is acceptable. If the user did not
  explicitly request platform publishing, use `--no-publish`.
- If user says `no sph`, do not publish Shipinhao.
- If publishing a platform later from the same processed video, use `--no-process`.
- For portrait/mobile versions, prefer LazyEdit's built-in portrait blur-fill and normal subtitle/logo reburn. Manual blur-fill scripts are fallback/recovery only.
- Use canonical publish categories: `simplelife`, `lazyingart`, `musia`, `lalachan`, `lalamv`. Use `lalamv` for LALACHAN music videos and route to YouTube `LalaMV` and Shipinhao `LalaMV` when available.
- YouTube playlist and Shipinhao collection selection should be best effort. Do not fail an otherwise valid publish only because a category UI is temporarily missing or unstable; report the limitation.

## Context Use

For subtitles, the script is a reference for fixing ASR mistakes. Correct clear recognition errors and broken phrases, but do not force the subtitles to match the script if the audio/video differs.

For singing videos, first identify the song before correction. Read the raw transcript for distinctive lyric fragments, search online with `歌词` or `lyrics`, and confirm the song from multiple matching fragments when possible. Use the song title and artist as context for subtitles and metadata. Do not let Whisper hallucinations such as random Japanese, Korean, Spanish, or English fragments become metadata. For copyrighted songs, do not paste full lyrics into responses or handoff notes; use song-fragment annotations such as `[歌曲：《Title》片段]` when the sung section is long or unclear.

Bridge-video lesson: `IMG_4379_2026_06_09_07_35_11_COMPLETED` should have been treated as a song-identification task. The likely songs were fragments of 《夏天的风》 and 《十年》. Future similar videos need lyric search before publish.

For metadata, the script is background context only. Do not turn metadata into a script dump. Avoid listing every scene beat, every line, or every production instruction. Metadata should be concise, viewer-facing, and platform-appropriate.

Operational rule: do not pass the full script through `--prompt-file` when metadata will be regenerated. Split the inputs:

- `--correction-prompt-file`: full story/script/prompt, used for subtitle correction.
- `--metadata-prompt-file`: a short temporary metadata brief, used for title, descriptions, captions, and tags.

The metadata brief should contain only the hook, characters, setting, central joke or emotion, final payoff, and a small keyword/hashtag list.

Good metadata should include:

- a short hook;
- the main character or setting;
- the central joke, conflict, or emotional idea;
- a few searchable keywords;
- compact hashtags where useful.

Bad metadata is a full storyboard summary. If the prompt is long, compress it mentally before metadata generation: keep the premise, tone, characters, and payoff.

## New Video Command Pattern

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
  --platforms shipinhao,youtube,instagram \
  --guided-monitor \
  --remote-log-command "ssh lachlan@lazyingart 'tmux capture-pane -pt autopub:0 -S -140 | tail -n 140'" \
  --wait \
  --poll-seconds 10 \
  --process-timeout 3600 \
  --publish-timeout 7200
```

## Publish Existing Processed Output to Shipinhao Later

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

## Required Final Check

Wait until LazyEdit and remote AutoPublish both report `done`. Final response should include video id, publish job id, remote job id, platforms, and context file used.
