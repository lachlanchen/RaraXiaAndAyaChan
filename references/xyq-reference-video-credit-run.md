# Xiaoyunque Reference Video Credit Run

This records the full method used to attach the logged-in Xiaoyunque driver, submit a local reference video, continue after storyboard confirmation, and stop at the insufficient-credit step.

## Driver Chrome

The reusable Chrome driver is the controlled Chrome profile started by:

```bash
PORT=9222 PROFILE_DIR="$HOME/.cache/xyq-chrome" \
  scripts/xyq_chrome/launch_chrome.sh \
  "https://xyq.jianying.com/home?tab_name=integrated-agent"
```

Current verified driver state on `2026-05-08`:

```text
Chrome: 147.0.7727.137
CDP endpoint: http://127.0.0.1:9222/json/version
Profile: /home/lachlan/.cache/xyq-chrome
Main PID at time of recording: 2307554
Thread: c883f4a0-8ffb-43ff-bf1a-2a8c1fffee82
URL: https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=c883f4a0-8ffb-43ff-bf1a-2a8c1fffee82&agent_name=pippit_nest_agent
```

Check the driver later:

```bash
curl -fsS http://127.0.0.1:9222/json/version
scripts/xyq_chrome/xyq_cdp.py --state
ps -eo pid,ppid,stat,etime,cmd | rg 'remote-debugging-port=9222|xyq-chrome'
```

## Reference Video Submission

Reference file:

```bash
Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_mask_inpaint_v3.mp4
```

Prompt:

```text
请参考这个视频，生成一个同风格的新视频。
```

Confirmation prompt:

```text
确认，请继续生成视频。
```

Uploaded asset id:

```text
1059072118284
```

First run:

```text
skill_b9a1f623-c3c3-4a76-8633-cff65f32cc2e
```

The first run uploaded the reference video, analyzed it, generated a storyboard and reference materials, then asked for confirmation before generating video.

Second run after confirmation:

```text
skill_51689363-8a58-4db0-8b46-80407ffac31c
```

It reached:

```text
tool: generate_shot_video
error code: 11001
message: 积分不足
browser text: 本次任务需要消耗220积分
```

This is the intended stopping point for checking that the workflow reaches generation and then blocks on credits.

## Tool Stack Used

Local scripts:

```text
scripts/xyq_chrome/launch_chrome.sh
scripts/xyq_chrome/xyq_cdp.py
scripts/xyq_chrome/reference_video_until_credit.py
/home/lachlan/.agents/skills/xyq-nest-skill/scripts/upload_file.py
/home/lachlan/.agents/skills/xyq-nest-skill/scripts/submit_run.py
/home/lachlan/.agents/skills/xyq-nest-skill/scripts/get_thread.py
```

Runtime methods:

- Chrome DevTools Protocol for attaching to the controlled logged-in browser.
- Xiaoyunque OpenAPI skill scripts for uploading the local video and submitting asset-backed runs.
- Browser composer fill through CDP for traceability; the actual file attachment and submit are done through the API.
- Polling `get_thread` until storyboard confirmation, then submitting one continuation message.
- Credit-block detection from `biz/error` payloads containing `code=11001`, `message=积分不足`, or `insufficient_credit_key`.

## Manual Commands Used

Load local configuration without printing secrets:

```bash
set -a
. ./.env
set +a
```

Upload the reference video through the installed Xiaoyunque skill:

```bash
python3 /home/lachlan/.agents/skills/xyq-nest-skill/scripts/upload_file.py \
  Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_mask_inpaint_v3.mp4
```

Fill the browser composer for visibility:

```bash
scripts/xyq_chrome/xyq_cdp.py \
  --fill-prompt "请参考这个视频，生成一个同风格的新视频。"
```

Submit the run with the uploaded asset:

```bash
python3 /home/lachlan/.agents/skills/xyq-nest-skill/scripts/submit_run.py \
  --thread-id c883f4a0-8ffb-43ff-bf1a-2a8c1fffee82 \
  --message "请参考这个视频，生成一个同风格的新视频。" \
  --asset-ids 1059072118284
```

Poll:

```bash
python3 /home/lachlan/.agents/skills/xyq-nest-skill/scripts/get_thread.py \
  --thread-id c883f4a0-8ffb-43ff-bf1a-2a8c1fffee82 \
  --run-id skill_b9a1f623-c3c3-4a76-8633-cff65f32cc2e \
  --after-seq 0
```

Continue after confirmation:

```bash
python3 /home/lachlan/.agents/skills/xyq-nest-skill/scripts/submit_run.py \
  --thread-id c883f4a0-8ffb-43ff-bf1a-2a8c1fffee82 \
  --message "确认，请继续生成视频。"
```

## Reusable One-Command Tool

The wrapper script reproduces the workflow:

```bash
scripts/xyq_chrome/reference_video_until_credit.py \
  --video Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_mask_inpaint_v3.mp4 \
  --thread-id c883f4a0-8ffb-43ff-bf1a-2a8c1fffee82 \
  --json-log outputs/xyq-reference-video-run.json
```

It reads `.env`, uploads the video plus the three default Lala/Aya/Sasa reference images, fills the browser composer through CDP when available, submits the prompt with all asset ids, auto-confirms once if Xiaoyunque asks to continue, polls the run, and stops when it sees an insufficient-credit block or another terminal state.

The three default images are included unless disabled:

```bash
--no-include-default-images
```
