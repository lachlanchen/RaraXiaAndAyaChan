# Musia To LALACHAN MV Style Research: Full Song vs Chorus Cut

Date: 2026-06-29  
Scope: document how to create LALACHAN music videos from Musia songs in two reusable styles: full-song MV and chorus/highlight MV.

## Conclusion

Use two separate MV products from the same song:

1. **Full-song MV**: use the whole song and build a complete story arc.
2. **Chorus / climax MV**: use only the strongest hook, 副歌, or 高潮部分 and make a compact social cut.

For **Aya Chan Hikari Ame**, create the full-song MV first. The selected song is about `68.04s`, and the hope/rain/battle idea needs a beginning, danger, charge, and warm ending. A chorus cut can be made later from the same story as a trailer or short social version.

## Style A: Full-Song MV

Use this when the song has a complete emotional journey or when the user wants a “real MV.”

Best for:

- 60s+ songs
- story-led videos
- character development
- hopeful or dramatic arcs
- a final public music video

Structure:

| Song Part | MV Role |
| --- | --- |
| Intro | quiet visual hook; establish place and mood |
| Verse | introduce characters and ordinary world |
| Pre-chorus | introduce threat, problem, or emotional tension |
| Chorus | biggest movement, fight, dance, or charge |
| Bridge | dreamlike expansion, memory, reversal, or close-up emotion |
| Final chorus/outro | resolution and warm image |

Rules:

- Let the song drive the timeline. Do not force too much dialogue over vocals.
- Add short character speech only in gaps or transitions.
- Use story sound lightly: rain, footsteps, shield shimmer, monster rumble, crowd/war ambience.
- If the video tool changes the music, replace final audio with the reviewed Musia MP3/WAV.
- Segment the prompt with timestamps and a JSON timeline before generation.

For Hikari Ame, the full-song story should be:

```text
阿芽酱在雨夜听见小铃发光。啦啦侠、飒飒君和庄子机器人赶来，跟她一起保护雨中快要熄灭的小光点。暴风化成影子恐龙/幻想怪物，城市变成梦境战场。大家害怕但没有退开，在副歌处一起喊“冲啊冲啊”，把黑雨冲成星光雨。清晨，雨还在下，但已经变亮。
```

## Style B: Chorus / Climax MV

Use this when the goal is speed, low cost, social media testing, or a strong hook.

Best for:

- 10s, 15s, or 30s videos
- TikTok/Reels/Shorts style cuts
- testing a song before spending more credits
- promoting a longer MV
- one clear visual gag or action scene

Structure:

| Time | MV Role |
| --- | --- |
| 0-2s | instant hook; show the strongest image first |
| 2-6s | characters enter action |
| 6-12s | chorus action, dance, fight, or emotional peak |
| final seconds | one payoff image, joke, pose, or loopable ending |

Rules:

- Use one idea only. Do not include a complete plot with many turns.
- Avoid long explanations or lore.
- Use the most memorable lyric/hook section.
- If the song has a vocal climax, the visuals should move on beat rather than add many spoken lines.
- This version can be generated first when credits are limited.

For Hikari Ame, a chorus cut could be:

```text
副歌一开始，雨街突然变成星光战场。影子恐龙冲过来，庄子展开透明伞盾，飒飒君带风绕开黑云，啦啦侠扶起灯笼，阿芽酱举起发光小铃。四个伙伴一起喊“冲啊冲啊”，黑雨变成金色光雨，最后大家站在清晨雨光里笑。
```

## Audio Policy

The Musia song is the master.

Preferred workflow:

1. Upload the Musia audio to Xiaoyunque if the UI accepts it.
2. Ask Xiaoyunque to follow the song’s rhythm, mood, and section changes.
3. Download the generated video.
4. If Xiaoyunque altered the song, mux the reviewed Musia audio back in.

Reusable command:

```bash
scripts/musia_mv_finalize.sh \
  --video GENERATED_VISUAL.mp4 \
  --audio ../Musia/data/creative_projects/SONG/final/selected.mp3 \
  --output Videos/SONG-mv-final.mp4
```

Keep two outputs when useful:

- `visual`: Xiaoyunque output as downloaded.
- `song-locked`: final image track with the exact Musia master audio.

## Prompting Rules

Prompt should include:

- uploaded asset labels only, such as `图1`, `图2`, `音频1`
- scene order and rough timestamps
- emotional direction
- limited dialogue and SFX notes
- “不要字幕，不要歌词字幕，不要路径、文件名或说明文字”

Prompt should not include:

- local file paths
- long hidden production notes
- all lyrics as visible text
- dense dialogue over the vocal
- custom LazyEdit publish instructions

## Hikari Ame Decision

For this song, use **full-song MV** as the main target.

Reason:

- The selected track is `68.04s`, long enough for a complete arc.
- The title idea, 光 / 雨, works best as a visual transformation across time.
- The requested battle and “冲啊冲啊” moment needs setup, attack, team charge, and resolution.
- A chorus-only cut should be derived later as a promotional highlight, not replace the main MV.

Existing handoff package:

```text
../Musia/data/creative_projects/aya-chan-hikari-ame-20260628/mv/hikari-ame-full-hope-battle-20260629
```

LALACHAN pointer:

```text
references/MusiaVideo/aya-chan-hikari-ame-full-hope-battle-20260629/README.md
```

## Quality Checklist

Before submit:

- Story has one clear emotional arc.
- Full-song MV has timed sections; chorus MV has one strong action idea.
- Dialogue is short and natural.
- Song audio is uploaded or planned for local muxing.
- Assets are uploaded as files, not pasted paths.
- No subtitles or lyric text are requested unless explicitly needed.
- Ratio and duration match the target.

After download:

- Verify duration with `ffprobe`.
- Check the audio track exists.
- Confirm whether the song was preserved.
- If needed, mux the Musia master audio.
- For public publishing, use normal LazyEdit publish logic and concise metadata.

