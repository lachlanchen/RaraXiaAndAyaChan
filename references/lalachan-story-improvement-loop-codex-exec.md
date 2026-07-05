# LALACHAN Story Improvement Loop With Codex Exec

This note records the reusable method for improving a LALACHAN story through repeated critique and rewrite rounds.

## Purpose

Use this when a story feels strange, too AI-like, hard to understand, not shareable, or not ready for Xiaoyunque.

The loop is intentionally mechanical:

```text
draft -> critique exact problem -> revise -> re-check -> repeat
```

For important stories, run 10 rounds.

## Command

```bash
scripts/lalachan_story_improve_loop_codex.sh references/stories/example.md --rounds 10
```

Default model settings:

```text
model: gpt-5.5
reasoning: xhigh
```

The script saves each round under:

```text
references/story-improvement-runs/
```

## Review Gates

Each round should check one concrete failure type:

- story promise and payoff
- event count for 15s or 30s
- causality instead of random sudden events
- character voices
- dialogue read-aloud quality
- visual comedy and retellable joke
- safety and credibility
- share hook
- Xiaoyunque prompt cleanliness
- final compression

## Output Standard

The final story should be easy to explain in one sentence, have one visible central joke, and end with either a payoff or a next-episode question.

Do not mix generation instructions into the story. Put visual or safety constraints in `Prompt Notes`.
