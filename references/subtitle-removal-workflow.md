# Hardcoded Subtitle Removal Workflow

This workflow documents the subtitle-removal approach used for:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/Videos/v03c76g10004d7ugka2ljht9cibm.728.mp4
```

The source is `836x1112`, `30 fps`, about `15.1s`.

## Result

The first working output used a feathered Gaussian blur over only the subtitle band:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/Videos/edited/v03c76g10004d7ugka2ljht9cibm.728_subtitle_blur_removed.mp4
```

For this clip, the effective subtitle band was:

```text
x=46 y=880 w=744 h=105
```

The reusable dynamic tool was also applied to these additional clips:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/Videos/edited/v03c76g10004d7spspaljht0mpia.885_2026_05_05_15_41_55_COMPLETED_subtitle_removed_dynamic.mp4
/home/lachlan/ProjectsLFS/LALACHAN/Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_dynamic.mp4
```

Both outputs were verified as `836x1112`, `30 fps`, `15.100s`.

The second clip needed a stronger corrected pass because the conservative dynamic blur left the top of some two-line subtitles visible. The corrected output is:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_mask_inpaint_v3.mp4
```

## Why Blur Instead Of Inpaint

The first attempted algorithm was text-mask inpainting:

1. Search the lower frame for low-saturation, high-value subtitle pixels.
2. Filter connected components to keep small glyph-like shapes.
3. Dilate the mask to include outlines and compression artifacts.
4. Run OpenCV `cv2.inpaint(..., INPAINT_TELEA)`.

This was rejected because the subtitle text has outlines and compression noise, and inpainting left visible fragments or smeared reconstruction artifacts on complex backgrounds.

The fallback was better: blur a narrow, feathered rectangle over the subtitle location. It does not reconstruct the image, but it removes readable text while leaving the rest of the frame untouched.

## Reusable Tool

Use:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/scripts/remove_subtitle_band.py
```

Dynamic default:

```bash
scripts/remove_subtitle_band.py input.mp4 output.mp4
```

The default mode scans the lower frame for subtitle-like bright text, smooths the detected vertical position over time, and applies a feathered blur to a narrow band.

Manual exact band:

```bash
scripts/remove_subtitle_band.py input.mp4 output.mp4 --rect 46:880:744:105
```

Fixed ratio band without dynamic detection:

```bash
scripts/remove_subtitle_band.py input.mp4 output.mp4 --no-auto --rect-ratio 0.055:0.791:0.890:0.095
```

Experimental inpaint mode:

```bash
scripts/remove_subtitle_band.py input.mp4 output.mp4 --mode inpaint --rect 46:880:744:105
```

Use inpaint only when the subtitle sits on simple backgrounds. For detailed animated scenes, blur is usually cleaner.

Masked inpaint mode:

```bash
scripts/remove_subtitle_band.py input.mp4 output.mp4 --mode mask-inpaint
```

This mode detects bright glyph-like subtitle components, dilates the text mask to catch outlines, inpaints only those masked components, and applies a small blur inside the mask. It is better when a plain blur leaves readable glyph shapes, but it needs tighter detection thresholds to avoid touching bright non-subtitle objects.

Commands used for the two later clips:

```bash
scripts/remove_subtitle_band.py \
  Videos/v03c76g10004d7spspaljht0mpia.885_2026_05_05_15_41_55_COMPLETED.mp4 \
  Videos/edited/v03c76g10004d7spspaljht0mpia.885_2026_05_05_15_41_55_COMPLETED_subtitle_removed_dynamic.mp4

scripts/remove_subtitle_band.py \
  Videos/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED.mp4 \
  Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_dynamic.mp4
```

Corrected command for the second clip:

```bash
scripts/remove_subtitle_band.py \
  Videos/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED.mp4 \
  Videos/edited/v03c76g10004d7ua3eiljhtaq0re.232_2026_05_07_22_37_08_COMPLETED_subtitle_removed_mask_inpaint_v3.mp4 \
  --mode mask-inpaint \
  --rect-ratio 0:0.74:1:0.18 \
  --search-y0 0.80 \
  --search-y1 0.96 \
  --search-x0 0 \
  --search-x1 1 \
  --min-row-score 170 \
  --comp-max-w 120 \
  --comp-max-h 72 \
  --comp-max-area 2400 \
  --mask-dilate-x 19 \
  --mask-dilate-y 11 \
  --mask-dilate-iterations 2 \
  --sigma-x 9 \
  --sigma-y 6 \
  --mask-feather 3 \
  --crf 18
```

Command used for `v03c76g10004d7v6p8iljhtesi7r.660.mp4`, which had both bottom subtitles and a top-left `AI生成` mark:

```bash
cp --update=none /home/lachlan/Downloads/v03c76g10004d7v6p8iljhtesi7r.660.mp4 \
  Videos/v03c76g10004d7v6p8iljhtesi7r.660.mp4

scripts/remove_subtitle_band.py \
  Videos/v03c76g10004d7v6p8iljhtesi7r.660.mp4 \
  Videos/edited/v03c76g10004d7v6p8iljhtesi7r.660_subtitle_removed_stage1.mp4 \
  --mode mask-inpaint \
  --rect-ratio 0.08:0.76:0.84:0.16 \
  --search-y0 0.68 \
  --search-y1 0.94 \
  --search-x0 0.05 \
  --search-x1 0.95 \
  --value-min 145 \
  --sat-max 130 \
  --mask-dilate-x 19 \
  --mask-dilate-y 9 \
  --mask-dilate-iterations 2 \
  --mask-feather 4 \
  --inpaint-radius 5 \
  --sigma-x 10 \
  --sigma-y 5 \
  --crf 18

scripts/remove_subtitle_band.py \
  Videos/edited/v03c76g10004d7v6p8iljhtesi7r.660_subtitle_removed_stage1.mp4 \
  Videos/edited/v03c76g10004d7v6p8iljhtesi7r.660_clean_no_subtitle_no_ai_text.mp4 \
  --mode inpaint \
  --no-auto \
  --rect 14:18:112:55 \
  --inpaint-radius 7 \
  --crf 18
```

For this clip, broad inpaint on the small top-left rectangle was cleaner than glyph-only masking because the mark included semi-transparent border/text remnants.

## Verification Commands

Check metadata:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate \
  -show_entries format=duration \
  -of default=noprint_wrappers=1 output.mp4
```

Create a sample contact sheet:

```bash
mkdir -p /tmp/subtitle_check
for t in 1 4 8 12 14; do
  ffmpeg -hide_banner -loglevel error -y -ss "$t" -i output.mp4 \
    -frames:v 1 "/tmp/subtitle_check/out_${t}.jpg"
done
ffmpeg -hide_banner -loglevel error -y -pattern_type glob \
  -i "/tmp/subtitle_check/out_*.jpg" \
  -vf "scale=418:-1,tile=1x5" /tmp/subtitle_check/contact.jpg
```

## Codex Prompt For Future Clips

```text
Inspect the video metadata and 5 representative frames. Use scripts/remove_subtitle_band.py with dynamic detection first. If the detected band misses the text, rerun with --rect X:Y:W:H based on the preview frames. Prefer --mode blur for complex backgrounds; use --mode inpaint only when the subtitle is on a flat/simple area. Verify with ffprobe and a contact sheet before finalizing.
```
