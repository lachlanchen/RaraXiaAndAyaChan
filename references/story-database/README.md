# Story Database

This folder keeps a lightweight database for LALACHAN stories, prompts, series,
and source references.

## Files

- `stories.csv`: one row per story, prompt, series episode, or reusable concept.
- `source-references.csv`: source IDs for books, local folders, visual assets,
  workflow docs, and generated references.

Use the CSV files as the source of truth when planning a new story. Markdown
series bibles can be richer, but the CSV table should record where each story
belongs and what references informed it.

## Story Row Fields

```text
story_id,date,title,series,status,story_path,prompt_path,video_path,reference_ids,concepts,notes
```

Field notes:

- `story_id`: stable slug. Use lowercase hyphenated names.
- `date`: creation or target date, `YYYY-MM-DD`.
- `title`: readable title.
- `series`: one of the series names in `references/series/README.md`.
- `status`: `draft`, `prompted`, `generated`, `archived`, or `reference`.
- `story_path`: Markdown story file if available.
- `prompt_path`: Xiaoyunque prompt file if available.
- `video_path`: final local video path if tracked or important.
- `reference_ids`: semicolon-separated IDs from `source-references.csv`.
- `concepts`: semicolon-separated themes, concepts, or teaching topics.
- `notes`: short free-form note.

## Source Reference Row Fields

```text
reference_id,type,title,path_or_url,usage_rule,notes
```

Types:

- `book-local`
- `project-local`
- `visual-asset`
- `workflow`
- `web-primary`
- `generated-asset`

## Copyright-Safe Source Rule

For copyrighted books, the database should record source IDs and page/range notes
only. Do not paste book text into story drafts. Future story work should extract
motifs, pressures, objects, and questions, then write an original scene.

Recommended extraction record:

```text
source_id:page-note -> motif only, no quote
```

Example:

```text
city-mars:p42 -> habitat logistics and legal uncertainty
japanese-history:p88 -> gate ritual and social hierarchy
sanxingdui:p31 -> bronze object as silent question
```

## Add A New Story

1. Add the story Markdown under `references/stories/`.
2. Add the Xiaoyunque prompt under `references/prompts/` if generated.
3. Add or update one row in `stories.csv`.
4. If new source material is used, add a row in `source-references.csv`.
5. If the story belongs to a canon series, update that series bible too.

## Validate The Database

Run:

```bash
python3 scripts/story_db_check.py
```

The validator checks:

- duplicate `story_id` values;
- unknown `reference_ids`;
- missing local story, prompt, and source paths;
- optional missing `video_path` values as warnings, because generated videos are
  usually ignored by git;
- source rows with empty IDs or targets.
