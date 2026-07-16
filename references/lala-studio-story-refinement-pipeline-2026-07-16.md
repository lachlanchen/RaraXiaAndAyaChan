# Lala Studio Story Refinement Pipeline

Date: `2026-07-16`

Lala Studio now provides one visible, bounded workflow for turning an idea or
rough draft into a reviewed story:

```text
draft (high) -> independent critic (x-high) -> final writer (ultra)
-> deterministic gate -> optional one-time repair (ultra)
```

The critic and writer run in separate model invocations. The critic reports
exact weak lines, and the final writer receives that evidence. The candidate
does not replace the editor until the user clicks **Use in editor**.

## Visible Workflow

Start the dedicated Studio desktop:

```bash
cd studio
scripts/launch_studio_novnc.sh start --project-root /path/to/LALACHAN
```

Open:

```text
http://127.0.0.1:6116/vnc_lite.html?host=127.0.0.1&port=6116&autoconnect=1&scale=1
```

Create, refine, apply, and save through visible browser controls:

```bash
node tools/lala-studio-browser.mjs story-pipeline \
  --title "Story title" \
  --duration 15 \
  --message "Concrete story idea"
```

The equivalent Studio CLI action is:

```bash
node bin/lala-studio.js ai refine "Concrete story idea" \
  --story-id STORY_ID \
  --duration 15
```

## Acceptance Rules

- A 15-second story may use at most four short dialogue beats.
- Required Markdown and multilingual word-card metadata must be complete.
- All deterministic checks must pass with a score of at least 90.
- The critic must compare the draft with the requested protagonist, activity,
  setting, relationship, and tone.
- A failed gate may trigger one repair, never an unbounded retry loop.
- A rejected candidate has no apply control.

## Real-Run Finding

The sushi test caught three issues that a simple one-pass writer missed:

1. The first final used six dialogue beats despite a 15-second target.
2. The critic initially mistook the required word card for prompt leakage.
3. A later rewrite made 啦啦侠 the apparent cook even though 阿芽酱 was the
   requested protagonist.

The workflow now checks dialogue density, treats the word card as out-of-story
metadata, and requires a semantic `Requirement coverage` review.

## Accepted Story

[戴歪帽子的寿司](stories/2026-07-16-aya-sushi-team-15s.md)

The final scene has one causal comedy chain: 阿芽酱 makes the sushi, 啦啦侠
fans the rice and sends a salmon slice flying, 飒飒君 catches it onto a rice
ball while nudging the plate, 庄子 stops the plate, and the crooked salmon
slides onto 啦啦侠's forehead when 阿芽酱 feeds him the accidental creation.

Implementation details live in
[`studio/docs/story-refinement-pipeline.md`](../studio/docs/story-refinement-pipeline.md).
