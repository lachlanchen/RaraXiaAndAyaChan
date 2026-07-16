# Lala Studio Story-to-Publish Journey

This document records the verified LALACHAN workflow for writing a story,
generating a Xiaoyunque video through a visible browser, downloading it safely,
and publishing the processed result through LazyEdit and AutoPublish.

The reference run was the 15-second episode **戴歪帽子的寿司**. It completed
with one Xiaoyunque submission and reached terminal success on Shipinhao,
YouTube, Instagram, and Douyin.

## System Map

| Layer | Responsibility |
| --- | --- |
| Lala Studio | Story room, critic pipeline, prompt building, visible production contract, and publish contract |
| Codex image generation | Creates a fresh episode-specific physical words card from the supplied product reference |
| Xiaoyunque browser | Uploads references and generates the video without using the Xiaoyunque API |
| noVNC + CDP | Makes browser work observable while retaining precise DOM control |
| Download watcher | Scopes the result, resumes interrupted transfers, validates full media streams, and copies the accepted MP4 |
| LazyEdit | ASR, context correction, multilingual subtitles, portrait blur-fill, logo, metadata, cover, and package creation |
| AutoPublish | Publishes the same verified ZIP to the requested platforms and reports terminal status |

Portable environment names used below:

```bash
export LALACHAN_ROOT=/path/to/RaraXiaAndAyaChan
export LALA_STUDIO_ROOT="$LALACHAN_ROOT/studio"
export LAZYEDIT_ROOT=/path/to/lazyedit
export XYQ_CDP_URL=http://127.0.0.1:9344
```

Do not put private browser profiles, access keys, cookies, or `.env` contents in
documentation or Git.

## Proven Defaults

- Story length: `15s` unless the user requests another duration.
- Xiaoyunque mode: `沉浸式短片` for ordinary short episodes.
- Model: cheapest suitable visible model, currently `Seedance 2.0 Mini 体验版`.
- Aspect ratio: `4:3` for the generated source.
- Prompt language: mainly Chinese.
- Characters: 啦啦侠, 阿芽酱, 飒飒君, and 庄子机器人.
- Reference images: fresh words card, 庄子, LightMind glasses, notebook, and the three individual character references.
- `Trio.png`: omitted when the user requests the no-Trio workflow.
- Generated video: no generated subtitles.
- Public master: LazyEdit portrait blur-fill, corrected multilingual subtitles,
  configured logo at top-right, and LALACHAN category.
- Default public platforms: Shipinhao, YouTube, Instagram, and Douyin.

## Phase 1: Write and Critique the Story

Use one visible cause-and-effect chain that fits the requested duration:

1. Establish the activity immediately.
2. Introduce one concrete problem.
3. Let each participating character perform a visible action.
4. End with a clear emotional or comic payoff.

Dialogue must sound like friends talking. Remove report-like robot language,
slogans, unnecessary explanations, forced cuteness, and events connected only
by `突然`.

The Studio pipeline performs three independent stages:

1. Draft.
2. Skeptical critic pass with quoted weak lines.
3. Final rewrite and quality gate.

Visible controller example:

```bash
cd "$LALA_STUDIO_ROOT"
node tools/lala-studio-browser.mjs story-pipeline \
  --title "Episode title" \
  --duration 15 \
  --message "Concrete story idea"
```

Save the accepted story under `references/stories/` and its generated-video
prompt under `references/prompts/`.

## Phase 2: Pre-generate the Words Card

The Markdown `## 对应词卡` section keeps field names because Studio parses it as
metadata. The physical card face must not show those field names.

Use the supplied words-card product image as the image-generation reference.
Before generating, verify that every value expresses the same intended word and
is correctly written in its respective language or script. Validation applies
equally to every language.

The card face contains only four lines:

```text
{{ENGLISH_VALUE}}
{{JAPANESE_VALUE}}
{{FURIGANA_VALUE}}
{{OTHER_LANGUAGE_VALUE}}
```

Do not render `English:`, `Japanese:`, `Furigana:`, `中文:`, language names,
colons, bullets, numbering, or explanatory text. Preserve the physical product
design from the reference image.

After image generation:

1. Open the PNG at original resolution.
2. Compare every line character-by-character with the requested block.
3. Confirm semantic equivalence across all four values.
4. Reject labels, spelling errors, wrong scripts, missing text, duplicated text,
   or unreadable glyphs.
5. Regenerate before paid video submission if any check fails.

Save the accepted image inside the current run directory as
`generated-word-card.png`; upload it instead of the base style reference.

## Phase 3: Open Observable Browsers

Start Studio and Xiaoyunque with their persistent profiles:

```bash
cd "$LALA_STUDIO_ROOT"
scripts/launch_studio_novnc.sh start --project-root "$LALACHAN_ROOT"
scripts/launch_xyq_novnc.sh start
```

Auto-fit viewer links:

```text
Studio:      http://127.0.0.1:6116/vnc_lite.html?host=127.0.0.1&port=6116&autoconnect=1&scale=1
Xiaoyunque: http://127.0.0.1:6099/vnc_lite.html?host=127.0.0.1&port=6099&autoconnect=1&scale=1
```

`vnc_lite.html` reads `scale=1`; it ignores `resize=remote`. The wrong parameter
leaves a 1920x1080 canvas clipped on smaller viewers.

## Phase 4: Build the Paid-Submit Contract

The Studio-generated prompt must:

- number only files that were actually uploaded;
- anchor each main character to its individual image;
- preserve the LazyingArt chest logo on 庄子;
- describe the generated words card as an existing physical prop;
- include the four exact card values without labels;
- contain no local paths or filenames;
- say `不要字幕`;
- avoid excessive negative prompting.

Before submission, visibly verify:

1. Correct Xiaoyunque thread and logged-in profile.
2. `沉浸式短片` mode.
3. Cheapest approved model.
4. `15s` duration.
5. `4:3` ratio.
6. Every required attachment reports success.
7. No Trio attachment when the run is no-Trio.
8. Prompt identity anchors and unlabeled card text.
9. Visible credit estimate is acceptable.

Prepare without spending credits:

```bash
node tools/lala-studio-browser.mjs production \
  --message "Prepare this 15-second video" \
  --operation prepare
```

Generate only after explicit user approval:

```bash
node tools/lala-studio-browser.mjs production \
  --operation generate \
  --confirm-paid \
  --wait-seconds 7200
```

Submit exactly once. A point deduction or queued/running state proves the first
click was accepted; monitor rather than clicking again.

## Phase 5: Monitor and Download Safely

Use the browser-scoped watcher, not a page-wide first-video search:

```bash
python "$LALACHAN_ROOT/scripts/xyq_chrome/watch_thread_dom_download.py" \
  --cdp-url "$XYQ_CDP_URL" \
  --page-id PAGE_ID \
  --thread-url THREAD_URL \
  --output-dir "$LALACHAN_ROOT/outputs/current-run" \
  --filename episode.mp4 \
  --expected-duration 15 \
  --copy-to "$LALACHAN_ROOT/Videos"
```

The watcher now writes `.part` files, checks the expected byte count, resumes
with HTTP Range requests, and renames atomically only after completion.

Do not trust an MP4 container header alone. One observed interrupted transfer
reported 15 seconds in `ffprobe` while its media packets stopped at 8 seconds.
Acceptance requires a complete decode:

```bash
ffmpeg -v error -xerror -i episode.mp4 \
  -map 0:v:0 -map 0:a:0? -f null -
```

Also verify:

```bash
ffprobe -v error -count_frames \
  -show_entries format=duration,size \
  -show_entries stream=codec_type,codec_name,width,height,nb_frames,nb_read_frames \
  -of json episode.mp4
sha256sum episode.mp4
```

Extract early and late sample frames. A successful 15-second container with no
decodable frame near 14 seconds is not a successful download.

After a generation job reaches a terminal state, Studio refreshes the story and
video inventory and selects the exact matching `<story-id>.mp4`. The publish
preflight must still compare the visible filename with the intended episode.

## Phase 6: Process and Publish in Studio

Ask Studio to create a delivery contract in the story chat, then inspect the
Publish workspace before confirming.

Required visible state:

- exact MP4 selected;
- exact story context selected;
- `Polished ASR + story` subtitle source;
- `LALACHAN` category;
- requested platforms checked;
- portrait fill, multilingual subtitles, and top-right logo shown.

Studio delegates one normal command to LazyEdit. Equivalent CLI shape:

```bash
cd "$LAZYEDIT_ROOT"
python scripts/lazyedit_publish.py \
  --video "$LALACHAN_ROOT/Videos/episode.mp4" \
  --title "Episode title" \
  --source lalachan \
  --platforms shipinhao,youtube,instagram,douyin \
  --publish-category lalachan \
  --use-current-settings \
  --prompt-file "$LALACHAN_ROOT/references/stories/episode.md" \
  --correct-subtitles \
  --process --publish \
  --burn-subtitles \
  --portrait-blur-fill \
  --portrait-blur-mode lalachan \
  --logo --logo-position top-right \
  --guided-monitor --wait --json
```

Use the story as correction and metadata evidence, not as a verbatim public
description. Let LazyEdit derive viewer-facing metadata through its normal
pipeline.

Inspect the processed master before declaring success:

- `1080x1920` portrait output;
- sharp 4:3 foreground;
- blurred current-frame background;
- lower subtitle reserve;
- multilingual subtitles and readings;
- top-right configured logo;
- full-stream decode succeeds.

Monitor the remote queue:

```bash
curl -fsS "$AUTOPUBLISH_API/publish/queue" | jq .
```

Platform success is terminal only when AutoPublish reports `done`, not merely
when a browser upload reaches 100%.

## Platform Behavior Learned

- **Shipinhao:** a login QR may be emailed. Wait for login rather than
  restarting the whole job. Collection assignment is best-effort; publish can
  still succeed when the requested collection is absent.
- **YouTube:** wait for checks to complete and capture the final public URL.
  Playlist creation/selection is best-effort because a newly created playlist
  may not immediately become selectable.
- **Instagram:** select Original crop for the already prepared portrait master
  and wait for the publish confirmation.
- **Douyin:** verify the accepted post in the management page, not only the
  publish-button click.

If one platform fails after others succeed, reuse the same verified ZIP and
retry only that platform. Do not reprocess or republish successful platforms.

## Code and Tool Map

| File or tool | Purpose |
| --- | --- |
| `studio/server/story-refinement.ts` | Independent story critic and final rewrite pipeline |
| `studio/server/codex.ts` | Story-writing standards and model prompts |
| `studio/server/prompt-builder.ts` | Path-free numbered Xiaoyunque prompt |
| `studio/server/workflows.ts` | Word-card generation contract, production, validation, and publish orchestration |
| `studio/src/App.tsx` | Refreshes matching video state after generation |
| `studio/tools/lala-studio-browser.mjs` | Visible Studio controller |
| `studio/scripts/launch_studio_novnc.sh` | Dedicated Studio desktop/profile |
| `studio/scripts/launch_xyq_novnc.sh` | Canonical Xiaoyunque desktop/profile |
| `scripts/xyq_cdp_browser.py` | Precise CDP browser operations |
| `scripts/xyq_chrome/watch_thread_dom_download.py` | Result scoping, resumable download, decode validation, and copying |
| `LazyEdit/scripts/lazyedit_publish.py` | One-command processing, packaging, queueing, and monitoring |

## Failure Modes and General Fixes

| Failure | Correct response |
| --- | --- |
| Card contains `English:` or other labels | Regenerate an unlabeled four-line card before paid submission |
| Any card language is wrong | Correct the source values, then regenerate and re-inspect every line |
| Base words card uploaded instead of fresh PNG | Stop before submit and replace attachment 1 |
| Typed paths appear in prompt | Remove paths; upload real files and refer to `图N` |
| Attachment remains uploading | Wait or repair upload; do not submit |
| Wrong model or ratio | Reopen selector and verify selected row/checkmark |
| Old episode selected in Publish workspace | Refresh video inventory and select exact filename |
| Download has plausible duration but missing late frames | Reject, resume/re-download, and require clean full decode |
| noVNC desktop is clipped | Use `vnc_lite.html?...&scale=1` |
| One platform fails | Reuse the existing ZIP and retry only the missing platform |

## Final Acceptance Checklist

- Story passed critique and reads naturally.
- Fresh unlabeled words card passed equal language-accuracy checks.
- Required reference images are visibly uploaded.
- Mode, model, duration, ratio, credit estimate, and prompt are proven.
- Exactly one generation submission occurred.
- MP4 byte count, duration, streams, late frames, full decode, and hash pass.
- Exact video and story context are selected for publishing.
- Portrait blur-fill, subtitles, readings, and logo are visually inspected.
- LazyEdit package contains the intended processed MP4, cover, metadata, and
  corrected subtitle files.
- Every requested platform reaches a terminal status.
- Partial platform limitations such as unavailable collections/playlists are
  reported without misrepresenting the publication result.
