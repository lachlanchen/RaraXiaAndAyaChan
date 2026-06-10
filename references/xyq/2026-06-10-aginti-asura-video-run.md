# 2026-06-10 AgInTi Asura Video Run

## Goal

Generate a 30-second Xiaoyunque video from the saved story prompt:

- Story: `references/stories/2026-06-10-aginti-asura-eternal-medicine-30s.md`
- Prompt: `references/prompts/2026-06-10-aginti-asura-eternal-medicine-30s.md`

## Browser Thread

- CDP endpoint: `http://127.0.0.1:9222`
- Page ID: `40EDD2844107F75CD30F241489B82615`
- Submitted thread: `https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=6ebfd06e-1603-414f-acc3-a628f2ddde2b&agent_name=pippit_nest_agent`
- Workflow: `创作 Agent` / `integrated-agent`
- Reason: `沉浸式短片` was locked to `15秒` and showed `Seedance 2.0 Fast VIP`; for 30-second work, use Agent mode instead.
- Credit balance changed from `437` to `63` during this run.

## Uploaded References

Only these five images were uploaded:

1. `/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png`
2. `/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png`
3. `/home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg`
4. `/home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg`
5. `/home/lachlan/ProjectsLFS/LALACHAN/Trio.png`

Upload verification screenshot:

- `outputs/xyq-run/2026-06-10-asura/after-upload.png`

Pre-submit screenshot:

- `outputs/xyq-run/2026-06-10-asura/pre-submit.png`

## Commands

```bash
python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 list-pages
python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 bring-to-front 40EDD2844107F75CD30F241489B82615

python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 upload-images-verify 40EDD2844107F75CD30F241489B82615 \
  /home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png \
  /home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png \
  /home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg \
  /home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg \
  /home/lachlan/ProjectsLFS/LALACHAN/Trio.png \
  --timeout 240 \
  --screenshot outputs/xyq-run/2026-06-10-asura/after-upload.png

python3 scripts/xyq_cdp_browser.py --cdp-url http://127.0.0.1:9222 type-prompt 40EDD2844107F75CD30F241489B82615 \
  references/prompts/2026-06-10-aginti-asura-eternal-medicine-30s.md --wait 1

python3 scripts/xyq_chrome/watch_thread_dom_download.py \
  --cdp-url http://127.0.0.1:9222 \
  --page-id 40EDD2844107F75CD30F241489B82615 \
  --thread-url "https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=6ebfd06e-1603-414f-acc3-a628f2ddde2b&agent_name=pippit_nest_agent" \
  --output-dir outputs/xyq-run/2026-06-10-asura \
  --filename aginti_asura_eternal_medicine_30s.mp4 \
  --copy-to Videos \
  --interval 30 \
  --max-polls 240
```

## Notes For Future Runs

- Keep prompt text compact. Do not repeat long negative constraints.
- Do not paste local paths into Xiaoyunque. Upload files, then refer to them as `图1`, `图2`, etc.
- If the Agent asks for continuation after storyboard/material creation, reply in the same thread with `继续生成视频。`
- If the page appears stuck loading, focus the browser address bar and press Enter, then re-run `list-pages` and `visible`.

## Outcome

- Xiaoyunque generated a `34秒` storyboard, then rendered a `34.320s` final MP4.
- Final video copied to: `Videos/aginti_asura_eternal_medicine_30s_2026-06-10.mp4`
- Correct download source: `/home/lachlan/Downloads/final_video (4).mp4`
- Correct `ffprobe` result: `1112x836`, duration `34.320000`.
- Correct SHA256: `d9f920b80ec55265047ca7021cf19a679fc0487db652d5dc07f87f235cf1c5fd`.

The watcher did not detect a direct video URL from the artifact grid. The reliable fallback was:

1. Open the `final_video.mp4` artifact card.
2. Click the page `下载` button.
3. Copy the freshly downloaded `final_video (*.mp4)` from `~/Downloads`.
4. Verify the downloaded file by modified time, size, `ffprobe`, and hash before copying.

Correction note: the first local copy accidentally used stale `/home/lachlan/Downloads/final_video (3).mp4`, which was the previous AgInTi lab video. The correct file was `/home/lachlan/Downloads/final_video (4).mp4`. The LALACHAN `Videos/` copy and LazyEdit DATA source were replaced with `final_video (4).mp4`. Wrong LazyEdit derivative files were moved to:

- `/home/lachlan/DiskMech/Projects/lazyedit/DATA/aginti_asura_eternal_medicine_30s_2026-06-10/_wrong_source_20260610_1112/`

During continuation, Xiaoyunque reported a reference-image limit:

- Generated assets initially used `10` reference images.
- It automatically cleared image paths for minor props `P3` and `P4`.
- It rendered successfully with `8` references.
