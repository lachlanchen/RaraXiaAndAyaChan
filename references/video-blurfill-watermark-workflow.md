# Video Blur-Fill and Watermark Workflow

This documents the video edits used for the panda promotion clip and keeps the commands reusable.

## Source

```bash
/home/lachlan/ProjectsLFS/LALACHAN/Promotion/Panda_Advertises_AI_Glasses_and_Notebook.mp4
```

Source metadata:

- Original size: `1280x720`
- Duration: about `8.043s`
- Watermark: bottom-right corner, around `x=1190 y=666 w=84 h=44`

## Output Styles

### 1. Crop-Based Watermark Removal

This removes the watermark by cropping off the bottom-right area.

Tradeoff: the mark is fully removed, but the original frame is no longer complete.

Command shape:

```bash
ffmpeg -i input.mp4 \
  -vf "crop=1168:664:0:0" \
  -c:v libx264 -preset medium -crf 18 -c:a copy -movflags +faststart \
  output_landscape_nowatermark.mp4
```

Portrait with flat padding:

```bash
ffmpeg -i input.mp4 \
  -vf "crop=1168:664:0:0,scale=1080:-2,pad=1080:1920:0:(oh-ih)/2:color=0xD9D4D0" \
  -c:v libx264 -preset medium -crf 18 -c:a copy -movflags +faststart \
  output_portrait_9x16.mp4
```

Portrait with blurred fill:

```bash
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]crop=1168:664:0:0,split=2[fgsrc][bgsrc];[bgsrc]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=34,eq=brightness=-0.04:saturation=1.12[bg];[fgsrc]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
  -c:v libx264 -preset medium -crf 18 -c:a copy -movflags +faststart \
  output_portrait_9x16_blurfill.mp4
```

### 2. Full-Frame Delogo With Symmetric Blur Fill

This keeps the full original foreground frame and patches the watermark area with ffmpeg `delogo`.

Tradeoff: the foreground frame is preserved, but the bottom-right mark is smoothed over rather than truly reconstructed.

Command shape:

```bash
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]delogo=x=1190:y=666:w=84:h=44:show=0,split=2[fgsrc][bgsrc];[bgsrc]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=36,eq=brightness=-0.05:saturation=1.10[bg];[fgsrc]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
  -c:v libx264 -preset medium -crf 18 -c:a copy -movflags +faststart \
  output_fullframe_delogo_portrait_9x16_blurfill.mp4
```

This is the preferred reusable version when the goal is a TikTok/Reels/Shorts-style portrait video without losing the original left/right framing.

## Reusable Script

The reusable script is:

```bash
/home/lachlan/ProjectsLFS/LALACHAN/scripts/video_blurfill.sh
```

Default: full frame, delogo watermark patch, symmetric blurred background.

```bash
scripts/video_blurfill.sh \
  "/home/lachlan/ProjectsLFS/LALACHAN/Promotion/Panda_Advertises_AI_Glasses_and_Notebook.mp4" \
  "/home/lachlan/ProjectsLFS/LALACHAN/Promotion/edited/Panda_Advertises_AI_Glasses_and_Notebook_delogo_fullframe_portrait_9x16_blurfill.mp4"
```

Crop-based version:

```bash
scripts/video_blurfill.sh \
  "/home/lachlan/ProjectsLFS/LALACHAN/Promotion/Panda_Advertises_AI_Glasses_and_Notebook.mp4" \
  "/home/lachlan/ProjectsLFS/LALACHAN/Promotion/edited/Panda_Advertises_AI_Glasses_and_Notebook_crop_portrait_9x16_blurfill.mp4" \
  --crop 0:0:1168:664 \
  --no-delogo
```

Custom watermark rectangle:

```bash
scripts/video_blurfill.sh input.mp4 output.mp4 --delogo X:Y:W:H
```

## Filter Notes

- `delogo=x:y:w:h` smooths over a rectangular watermark area using surrounding pixels.
- `split=2` duplicates the cleaned/cropped frame into foreground and background streams.
- `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920` makes the background fill the vertical frame symmetrically from the center.
- `gblur=sigma=36` creates the soft background blur.
- `eq=brightness=-0.05:saturation=1.10` slightly darkens and saturates the background so the foreground stays readable.
- `scale=1080:-2` scales the full landscape foreground to portrait width while preserving aspect ratio.
- `overlay=(W-w)/2:(H-h)/2` centers the foreground on the blurred background.

## Existing Outputs

```bash
/home/lachlan/ProjectsLFS/LALACHAN/Promotion/edited/Panda_Advertises_AI_Glasses_and_Notebook_nowatermark_landscape.mp4
/home/lachlan/ProjectsLFS/LALACHAN/Promotion/edited/Panda_Advertises_AI_Glasses_and_Notebook_nowatermark_portrait_9x16.mp4
/home/lachlan/ProjectsLFS/LALACHAN/Promotion/edited/Panda_Advertises_AI_Glasses_and_Notebook_nowatermark_portrait_9x16_blurfill.mp4
/home/lachlan/ProjectsLFS/LALACHAN/Promotion/edited/Panda_Advertises_AI_Glasses_and_Notebook_delogo_fullframe_portrait_9x16_blurfill.mp4
```
