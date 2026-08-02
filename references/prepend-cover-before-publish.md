# Prepend a Cover Before Publishing

Use `scripts/prepend-image-cover.sh` when a LALACHAN video should open with a generated reference or cover image. Add the cover before sending the source to LazyEdit so subtitle timing, portrait blur-fill, logo placement, metadata, and platform packages all use the same final timeline.

```bash
scripts/prepend-image-cover.sh \
  references/cover.png \
  Videos/source.mp4 \
  Videos/source-cover-intro.mp4 \
  2
```

The script matches the source resolution and frame rate, creates silent stereo audio for the still image, adds a restrained zoom, and concatenates it with the original audio/video. Verify the result before publication:

```bash
ffprobe -v error \
  -show_entries stream=codec_name,width,height \
  -show_entries format=duration,size \
  -of json Videos/source-cover-intro.mp4
```

For normal LALACHAN publication, pass the cover-intro video to LazyEdit with the reviewed story as `--prompt-file`. Use the standard `lalachan` settings: portrait blur-fill, multilingual subtitles, contextual correction, and the configured logo at the top-right.

If ASR returns unrelated promotional phrases, inspect the audio and generated frames before publishing. Run normal contextual correction first. If it still preserves obvious hallucinations, save a reviewed polished subtitle timeline, regenerate translation and burn artifacts in a new publication session, inspect sample frames, and publish that exact session once.
