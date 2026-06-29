# Hikari Ame Full MV Browser Generation

Date: 2026-06-29

This records the reusable workflow for generating a full-song Musia MV in Xiaoyunque through the logged-in browser/noVNC path, then preserving the Musia master audio.

## Inputs

- Xiaoyunque mode: `创作 Agent` for full-song long MV.
- Ratio: `16:9（横屏）`.
- Audio: `aya-chan-hikari-ame-selected.mp3`, duration `68.04s`.
- Prompt: `references/prompts/2026-06-29-hikari-ame-full-mv-68s.md`.
- Correction/approval prompt: `references/prompts/2026-06-29-hikari-ame-full-mv-confirmation.md`.
- Uploaded assets: words card, Zhuangzi robot, LightMind glasses, notebook, RaraXia, Aya Chan, Sasa Kun, Trio, and the Musia MP3.

## Prompt Lesson

For MV jobs, explicitly say the characters can perform the song:

```text
阿芽酱是主唱感，啦啦侠、飒飒君和庄子机器人可以在副歌处轻轻跟唱、合唱或回应，也可以喊“冲啊冲啊”。音乐仍然是主线，台词只保留少量自然短句，不要连续讲话。
```

Keep dialogue sparse. The prompt should not look like a dialogue short film; it should say the song is the timing and emotion authority.

## Browser Steps

1. Open the logged-in Xiaoyunque page in the existing Chrome/CDP/noVNC session.
2. Upload actual files, not local path text.
3. Paste the full MV prompt.
4. Select `16:9（横屏）`.
5. Submit once.
6. If Agent generates a storyboard that does not match the song duration, correct it before paid render. In this run it first made `78s`; the confirmation prompt asked it to revise to `66-70s`.
7. Confirm the paid render only after duration/ratio/subtitle state is correct.

Confirmed render in this run:

```text
扣除 748 积分
68s
字幕：关闭
```

## Download Fallback

The generic DOM watcher did not find a normal `<video>` URL, but the completed thread exposed a resource card:

```text
视频 -> 生成结果 -> final_video.mp4
```

Click `final_video.mp4`, then click the preview-panel `下载` button. The button text may change to `下载中 NN%`; wait for a completed file in `~/Downloads`.

Reusable wait command:

```bash
start="$(date +%s)"
# click the Xiaoyunque preview download button here
scripts/wait_downloaded_mp4.sh --since-epoch "$start" --min-bytes 1000000 --timeout 300
```

For this run Chrome saved:

```text
~/Downloads/final_video (13).mp4
```

## Local Outputs

Raw Xiaoyunque output:

```text
Videos/aya_chan_hikari_ame_full_mv_xyq_2026-06-29.mp4
outputs/xyq-2026-06-29-hikari-ame-full-mv/aya_chan_hikari_ame_full_mv_xyq_2026-06-29.mp4
```

Song-locked final using the exact Musia audio:

```text
Videos/aya_chan_hikari_ame_full_mv_song_locked_2026-06-29.mp4
outputs/xyq-2026-06-29-hikari-ame-full-mv/aya_chan_hikari_ame_full_mv_song_locked_2026-06-29.mp4
```

Verified:

```text
Raw: 1280x720, 68.900s, AAC stereo
Song-locked: 1280x720, 68.022s, AAC stereo from Musia master
```

## Final Audio Rule

If Xiaoyunque changes or weakens the music, keep the generated visuals and mux the Musia master track:

```bash
scripts/musia_mv_finalize.sh \
  --video Videos/aya_chan_hikari_ame_full_mv_xyq_2026-06-29.mp4 \
  --audio "$MUSIA_ROOT/data/creative_projects/aya-chan-hikari-ame-20260628/final/aya-chan-hikari-ame-selected.mp3" \
  --output Videos/aya_chan_hikari_ame_full_mv_song_locked_2026-06-29.mp4
```

Use `$MUSIA_ROOT` and `$LALACHAN_ROOT` in public reusable docs or skills.
