# Mars + Japan + Sanxingdui Story Synthesis

This is a named series method for future LALACHAN stories that combine Mars,
Japanese history, Sanxingdui, and optionally VoidAbyss. It is connected to Red
Sand Paper Kite, but it can also produce standalone daily stories.

## Purpose

Each new story should read a small source slice from each pillar:

1. one page-like unit from a Mars source;
2. one page-like unit from Japanese history;
3. one page-like unit from Sanxingdui;
4. optionally one page-like unit from VoidAbyss notes.

Then transform the extracted motifs into a new imaginative story. Do not copy
source plots or phrasing. The final video story should feel smooth, intriguing,
and original, not like a summary of the books.

## Source Pillars

Mars source rotation:

- `city-mars`: settlement logistics, law, air, risk, ownership.
- `sirens-mars`: projection, false canals, longing, evidence versus desire.
- `red-mars`: competing visions for a new world.
- `the-martian`: practical repair and humor under constraint.
- `martian-chronicles`: poetic memory and haunted frontier mood.

Japanese history source:

- `japanese-history`: gates, bridges, ritual order, islands, waterworks, court
  rules, social boundaries, politeness as both protection and pressure.

Sanxingdui source:

- `sanxingdui`: bronze masks, gold birds, sacred trees, ritual pits, artifact
  fragments, mystery, silent objects that ask questions.

VoidAbyss optional source:

- `voidabyss`: paper kite, rift, ordinary suffering, shared governance, freedom
  with responsibility.

All IDs are defined in `references/story-database/source-references.csv`.

## What Counts As One Page

Because local builds may be TeX, Markdown, or generated book folders, "one page"
means one compact reading unit:

- about 450-700 Chinese characters;
- or one printed/PDF page if working from a visible PDF;
- or one short section fragment if the source is TeX/Markdown;
- or one self-contained paragraph cluster.

Do not paste that page into story notes. Record only:

- source ID;
- approximate page/section note;
- 3-5 extracted motifs;
- one emotional pressure;
- one visual object.

## Extraction Template

Use this private planning template before writing the story:

```text
Mars page:
- source:
- page/section note:
- practical pressure:
- false belief or risk:
- visual object:

Japan page:
- source:
- page/section note:
- social/ritual pressure:
- place form:
- rule or etiquette:

Sanxingdui page:
- source:
- page/section note:
- artifact:
- mystery:
- silent question:

VoidAbyss page, optional:
- source:
- page/section note:
- ethical pressure:
- ordinary-person cost:

Original story seed:
- setting:
- conflict:
- funny misunderstanding:
- Aya's interpretation:
- technical/practical detail:
- ending hook:
```

## Combination Formula

Turn the four sources into four story functions:

- Mars source gives the survival or frontier constraint.
- Japanese history gives the social rule, gate, ritual, road, or bridge.
- Sanxingdui gives the visual mystery object.
- VoidAbyss gives the ethical question.

Example transformation:

```text
Mars pressure: the habitat needs shared air.
Japanese form: a bridge only opens after a polite ritual.
Sanxingdui object: a bronze bird holds the missing air key.
VoidAbyss question: who is allowed to breathe first when the system is failing?
Original 15s story: the trio reaches a red bridge where everyone bows to borrow
air. Lala Xia thinks the bowing machine is a snack dispenser. Aya notices a tiny
old worker at the end of the line. The bronze bird drops the key only when the
trio lets the slowest person cross first.
```

## Story Tone

For LALACHAN:

- beautiful, mysterious, warm, funny;
- one strong visual object;
- one short concept or moral pressure;
- short dialogue, mostly Chinese;
- do not over-explain the book sources;
- no visible subtitles except intentional physical props like the words card.

For VoidAbyss:

- slower, heavier, more political;
- same motifs can become institutions, laws, betrayals, and public ethics;
- ordinary people must remain visible.

## 15-Second Episode Shape

```text
0-3s: Strange place appears.
3-6s: Rule or danger appears.
6-9s: Lala Xia or Sasa misunderstands it.
9-12s: Aya sees the real meaning.
12-15s: Artifact reacts and opens the next clue.
```

## 1-Minute Episode Shape

```text
0-8s: Arrival and visual wonder.
8-18s: Rule, artifact, or survival problem.
18-32s: comic mistake and escalating physical action.
32-45s: source-derived deeper pressure appears.
45-55s: original humane solution.
55-60s: next-series hook.
```

## Example Future Story

Title: `青铜鸟与借来的空气`

The trio arrives at a red-sand station shaped like a small island bridge. Everyone
must bow to borrow air from a polite gate. Lala Xia thinks the bowing counter is
a snack vending machine and keeps bowing for "extra portions." Sasa Kun bows so
hard that his bamboo rolls across the bridge and wakes a bronze bird.

The bronze bird carries a tiny air key but refuses to drop it. Aya Chan opens
her notebook and realizes the bridge rule is upside down: it rewards the fastest
traveler, while the oldest worker at the back of the line is almost out of air.

The trio gives up their place. The bronze bird finally drops the key into the
worker's hands, not theirs. The gate changes its rule from "first arrival" to
"shared crossing." The final shot shows the bridge stretching toward a distant
gold tree, while Lala Xia whispers, "So bowing is not a snack system?"

## Database Rule

When using this method, add the story row to:

```text
references/story-database/stories.csv
```

Use `series`:

```text
Mars Japan Sanxingdui
```

Reference IDs should include the exact source pillars used, for example:

```text
city-mars;japanese-history;sanxingdui;voidabyss;trio-image;lightmind-display;aya-notebook
```

The `notes` field should briefly record the page-selection logic, such as:

```text
Mars logistics page + Japanese bridge/ritual page + bronze bird artifact page.
```

