# MV Subtitle And Ruby Notes

## Current-Line Website Rendering

For LalaMedias and future MV pages, render timed text as one active line below the video instead of a full subtitle dump. Prefer the order:

1. Japanese with ruby/furigana when available.
2. English translation.
3. Chinese translation.

Use color-coded word spans for readability, but keep the text as real timed subtitle content. Do not show local paths, script notes, or full prompt text on viewer-facing pages.

## Furigana Rule

Japanese learner-facing text needs real furigana metadata from the subtitle/translation pipeline. If a LazyEdit `*_ja_furigana.json` file contains kanji but has empty `furigana_pairs` and no `<rt>` markup, treat it as an upstream bug. Do not invent readings in LalaMedias unless a dedicated Japanese reading tool is explicitly run and validated.

## Hikari Ame Issue

The Hikari Ame MV publish generated timed Japanese, English, and Chinese JSON, but the Japanese furigana fields were empty. A LazyEdit bug report was written here:

```text
/home/lachlan/DiskMech/Projects/lazyedit/bug-reports/2026-06-29-hikari-ame-furigana-missing.md
```

Future MV workflows should validate that Japanese kanji lines include `furigana_pairs` or `<ruby><rt>...</rt></ruby>` before final website handoff.

