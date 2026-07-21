# LALACHAN World Database

`lalachan-world.json` is the canonical, Git-versioned source for characters, places, tools, outfits, continuing arcs, episode links, and media lineage used by Lala Studio.

## Editing Contract

- Edit canon through the Studio **World** workspace when possible.
- Replacing a reference image creates a new media version; do not overwrite an old version silently.
- Generated scene references and word cards are archived under `media/<story-id>/` and registered with SHA-256 hashes.
- Videos remain under `Videos/` and are recorded by path and hash. They are not committed to Git.
- Every connected episode resolves its immediate problem and may leave one small visible hook for an open arc.

## Data Model

- `characters`: identity, personality, natural voice, visual rules, relationships, and default outfit.
- `places`: recurring locations, visual anchors, common uses, and graph connections.
- `tools`: stable capabilities and explicit limitations.
- `outfits`: versioned clothing or robot shells tied to reference assets.
- `arcs`: long-running questions with status and episode links.
- `topics`: recurring emotional or educational themes.
- `episodes`: the selected canon for each story and its current production state.
- `media`: reference and generated asset versions with SHA-256 provenance.

Inspect the current series state with:

```bash
jq '{revision, episodes, openArcs: [.arcs[] | select(.status == "open")]}' references/world/lalachan-world.json
```

## Media Policy

Generated word cards and scene keyframes are committed under `media/<story-id>/` with monotonically increasing `vNNN` names. Videos stay in `Videos/`; the database records their path and SHA-256 with `tracked: false` so the series remains auditable without putting large MP4 files in Git.

## Story Shape

The structure borrows only broad serial-story principles from enduring ensemble adventures: a familiar home, recurring destinations, tools with stable rules, distinct relationships, self-contained episodes, and a slowly unfolding mystery. It does not copy characters, plots, terminology, or settings from another work.
