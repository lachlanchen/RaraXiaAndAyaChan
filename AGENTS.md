# Repository Guidelines

## Project Structure & Module Organization

This repository stores reusable media workflows, prompts, and generated assets for the LALACHAN project.

- `scripts/` contains reusable command-line utilities. Example: `scripts/video_blurfill.sh`.
- `references/` contains documentation and prompt text. Use `references/prompts/` for generation prompts.
- `Promotion/`, `outputs/`, and character folders contain media assets and generated videos/images. Treat these as working assets, not source code.
- `.env` is local configuration and must not be committed.

## Build, Test, and Development Commands

There is no application build step. The main dependency for video utilities is `ffmpeg`.

```bash
scripts/video_blurfill.sh --help
```

Shows usage and available options for creating portrait blur-fill videos.

```bash
scripts/video_blurfill.sh input.mp4 output.mp4
```

Creates a `1080x1920` vertical video with a blurred duplicate background and a smooth bottom-right watermark patch.

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -show_entries format=duration output.mp4
```

Verifies output dimensions and duration.

## Coding Style & Naming Conventions

Shell scripts should use Bash with `set -euo pipefail`, quote file paths, and expose options through clear long flags such as `--delogo` and `--crop`.

Use lowercase, hyphenated names for reusable docs and scripts, for example `video-blurfill-watermark-workflow.md`. Prompt files should use descriptive slugs, for example `forest-dinosaur-portrait-15s.md`.

Markdown should be concise, task-oriented, and include runnable examples when useful.

## Testing Guidelines

There is no automated test framework yet. For scripts, test by running the command on a small known input and verifying outputs with `ffprobe`.

Check at least:

- Output dimensions match the intended format, usually `1080x1920`.
- Duration is close to the source duration.
- Sample frames visually confirm watermark handling and composition.

## Commit & Pull Request Guidelines

This repository has no established commit history yet. Use short imperative commit messages, such as `Add blur-fill video script` or `Document watermark workflow`.

Pull requests should include:

- A short summary of changed scripts or docs.
- The exact command used to generate or verify outputs.
- Before/after screenshots or sample frame paths for visual video changes.
- Confirmation that `.env`, raw generated videos, and unrelated media assets were not committed unless intentionally requested.

## Security & Configuration Tips

Keep API keys in `.env` only. Do not print secrets in logs or markdown. When adding scripts, prefer explicit input/output arguments over hard-coded personal paths unless the file is documenting a completed local workflow.
