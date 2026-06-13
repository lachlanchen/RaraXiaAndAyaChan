# AgInTi Writing Supervision Note

Date: `2026-06-13`

Scope: supervision of AgInTiFlow while rewriting the LALACHAN story
`实验台上的小舞步`.

## What Happened

The user asked for a smoother story because previous LALACHAN drafts often
used strange, stiff, or AI-like language. The requested task was:

- read the existing story and prompt;
- use AgInTiFlow's `writing_specialist`;
- rewrite the biological-lab dance story with more natural Chinese dialogue;
- save exact v2 story and prompt filenames.

AgInTiFlow correctly started in the LALACHAN repo and SCS recognized that
`writing_specialist` was a hard requirement. The first pass did call
`writing_specialist` and produced a better timed storyboard.

However, the result still had awkward language and instruction-following gaps.

## Problems Observed In AgInTiFlow

### 1. It Missed Exact Filenames

Requested output:

```text
references/stories/2026-06-13-biological-lab-dance-aginti-writer-v2.md
references/prompts/2026-06-13-biological-lab-dance-aginti-writer-v2-30s.md
```

AgInTi wrote:

```text
references/stories/2026-06-13-biological-lab-dance-revised.md
references/prompts/2026-06-13-biological-lab-dance-30s-revised.md
```

It then reported completion without verifying the exact requested paths.

### 2. It Used `writing_specialist` Once, Then Drifted

The first pass used `writing_specialist`. The follow-up explicitly asked for
another `writing_specialist` pass, but AgInTi used the main/in-session model and
patched local sentences instead.

This is a tool-contract problem: if the user requires a named tool, the current
turn should verify the named tool was used in that turn.

### 3. SCS Helped But Did Not Fully Enforce The Contract

SCS correctly noticed the requirement to use `writing_specialist`, which is good.
But the final gate did not reject the wrong filenames. The validator should
check exact deliverables, not only that some related files exist.

### 4. Language State Mismatch

The command used:

```bash
aginti --language zh-Hans --scs --routing smart
```

Startup still displayed:

```text
language=en (English)
```

That makes language-aware writing and routing harder to trust.

## Writing Problems Found

The first AgInTi rewrite was better than the previous draft, but still had lines
that sounded like a model explaining a concept rather than characters speaking:

```text
我的手很稳，但跳舞的版本可能不太稳……
结论：实验需要冷静，也需要一点点节奏。
```

These failed the spoken-language test. A person or character would not naturally
say `版本` here, and `结论` makes the ending feel like a lab report.

Better final direction:

```text
我的手很稳，但跳舞嘛……不太行。
看来，做实验要静得下来，也要踩得准拍子。
```

Even these should be treated as "acceptable for now", not perfect. The stronger
principle is: dialogue should sound like friends in a situation, not like a
summary of the theme.

## Supervision Lessons

- Ask AgInTi for a writing-specialist pass, but still critique the output.
- Do not accept `writer used` as sufficient. Check whether the writing is
  actually smoother.
- Check exact output filenames externally.
- Look for phrases that only exist because the writer wants to explain the
  lesson.
- Keep raw AgInTi output for traceability, then save a stable v2 file when the
  output is usable.
- If AgInTi misses a mechanical contract, report the defect in AgInTiFlow rather
  than only fixing the local file.

## Files Produced In LALACHAN

Raw AgInTi output:

```text
references/stories/2026-06-13-biological-lab-dance-revised.md
references/prompts/2026-06-13-biological-lab-dance-30s-revised.md
```

Stable v2 output:

```text
references/stories/2026-06-13-biological-lab-dance-aginti-writer-v2.md
references/prompts/2026-06-13-biological-lab-dance-aginti-writer-v2-30s.md
```

AgInTiFlow bug report:

```text
/home/lachlan/ProjectsLFS/Agent/AgInTiFlow/bug-reports/2026-06-13-writing-specialist-contract-and-routing.md
```

## Future Rule

For every LALACHAN story before video generation:

1. Write the story normally first.
2. Run a critic pass.
3. Fix unnatural dialogue and weak causality.
4. Only then create the Xiaoyunque prompt.

