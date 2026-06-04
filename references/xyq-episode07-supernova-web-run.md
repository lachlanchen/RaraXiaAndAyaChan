# Xiaoyunque Episode 07 Web Run

Date: `2026-05-18`

This records the successful browser-based generation for Episode 07, using the logged-in Chrome/CDP page. No API submission was used.

## Result

- Output: `Videos/episode07_supernova_sneeze_15s.mp4`
- Working copy: `outputs/xyq-episode07-supernova-web-normal-fast/episode07_supernova_sneeze_15s.mp4`
- Contact sheet: `outputs/xyq-episode07-supernova-web-normal-fast/contact_sheet.jpg`
- Prompt: `references/prompts/2026-05-18-episode07-supernova-duanpian-15s.md`
- Browser thread: `thread_id=e65f0b85-55f7-4f34-bfa5-3f3266a55c0f`

Verified with:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,codec_name,avg_frame_rate \
  -show_entries format=duration,size \
  -of json Videos/episode07_supernova_sneeze_15s.mp4
```

Observed output: H.264, `1280x720`, `30 fps`, `15.1s`, about `18 MB`.

## Browser Setup Used

The active Chrome DevTools endpoint was:

```text
http://127.0.0.1:9222
```

The run used the existing logged-in Xiaoyunque page, then recovered the same submitted task by reopening the thread URL when the original CDP target disappeared.

Useful checks:

```bash
scripts/xyq_cdp_browser.py list-pages
scripts/xyq_cdp_browser.py visible PAGE_ID
scripts/xyq_cdp_browser.py screenshot PAGE_ID outputs/xyq-episode07-supernova-web-normal-fast/current_thread.png
```

## Settings

- Mode: `沉浸式短片`
- Model: `Seedance 2.0 Fast`
- VIP: not used
- Duration: `15秒`
- Starting credits: `88`
- Credits after task started: `13`

Before submission, the page state showed:

```text
mode: 短片
model: 2.0 Fast
duration: 15秒
uploaded image count: 5 successful uploads
```

## Reference Images

The five standard images were uploaded through the page file input:

```text
/home/lachlan/ProjectsLFS/LALACHAN/display.png
/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png
/home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg
/home/lachlan/ProjectsLFS/LALACHAN/Trio.png
```

Upload command pattern:

```bash
scripts/xyq_cdp_browser.py set-file-input "$PAGE" \
  display.png \
  patchwork-leather-notebook-luxury-clean-v2.png \
  R1.jpg.jpeg \
  R3.jpg.jpeg \
  Trio.png \
  --index 0
```

## Prompt Fill And Submit

Prompt copy used for this run:

```text
outputs/xyq-episode07-supernova-web-normal-fast/prompt.txt
```

Fill command:

```bash
scripts/xyq_cdp_browser.py set-prompt "$PAGE" \
  outputs/xyq-episode07-supernova-web-normal-fast/prompt.txt
```

The first DOM click did not submit because the create button had moved after the prompt area grew. The working submit method was a coordinate click on the current button center:

```bash
scripts/xyq_cdp_browser.py click "$PAGE" 1186 753
```

After click, the URL changed to:

```text
https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=e65f0b85-55f7-4f34-bfa5-3f3266a55c0f&source=home_prompt&entrance_from=home
```

## Poll And Download

The successful download URL appeared only after refreshing/reopening the submitted thread. The final URL was saved to:

```text
outputs/xyq-episode07-supernova-web-normal-fast/final_url.txt
```

For future runs, use the reusable polling tool:

```bash
scripts/xyq_chrome/poll_result_download.py \
  --page-id-file outputs/xyq-episode07-supernova-web-normal-fast/page_id.txt \
  --thread-url "https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id=e65f0b85-55f7-4f34-bfa5-3f3266a55c0f&source=home_prompt&entrance_from=home" \
  --output-dir outputs/xyq-episode07-supernova-web-normal-fast \
  --filename episode07_supernova_sneeze_15s.mp4 \
  --copy-to-videos Videos \
  --ignore-file outputs/xyq-episode07-supernova-web-normal-fast/poll_fixed_001_candidate_urls.txt
```

The `--ignore-file` is optional. It helps avoid mistaking uploaded reference image/media URLs for the generated result.

## Notes For Next Time

- Use the page workflow by default; avoid API generation unless explicitly requested.
- Confirm `Seedance 2.0 Fast` without VIP before submitting.
- Confirm `15秒` for `沉浸式短片`.
- Use the bottom `+` upload flow or the file input directly for the five image references.
- If the task stays at `大约还需1分钟`, reopen the same `thread_id` URL and continue polling instead of resubmitting.
- Keep the generated MP4 even if the model ignores `不要字幕`; only run subtitle cleanup when the visible text is actually a problem.
