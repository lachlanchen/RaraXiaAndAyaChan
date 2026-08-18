# Subtitle alignment incident: Japan sky route

The published Japan sky-route episode exposed a subtitle-correction failure.
The source ASR had 20 cues, while the polished output had 21 cues. Later story
dialogue was inserted into earlier timestamps and some lines were duplicated at
their original later position. The resulting multilingual subtitles did not
follow the audible dialogue.

Future LALACHAN publication must treat story text as correction context only.
Ordinary correction may change cue text but must preserve cue count, order, and
start/end timestamps. Missing dialogue needs a separate audio-alignment pass.
Before translation or burn, run the LazySkills timeline validator and sample
audible dialogue near the start, middle, and end. Any timeline failure blocks
publication.

Affected artifacts:

- LazyEdit video `526`
- Publish job `362`
- AutoPublish job `job-1787033609705-5`
- Source: `*_mixed.srt`
- Invalid corrected output: `*_mixed_polished.srt`

This record does not request republishing the affected video. It records the
failure so the same correction method is not reused.
