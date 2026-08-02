# 乱徵《洛神》Doubao MV Handoff

## Intent

Create a cinematic video in Doubao using music generated elsewhere. The source
work is 乱徵《洛神》, whose lyrics reorganize lines from 曹植《洛神赋》.

## External Audio

Preferred reviewed recording:

```text
/home/lachlan/ProjectsLFS/Musia/data/creative_projects/luoshenfu-original-excerpt-preview-20260729/selected/luoshenfu-original-excerpt-pronunciation-v2-seed729403.mp3
```

Duration: approximately `136.032s`.

## Visual Reference

```text
references/MusiaVideo/luan-zheng-luoshen-doubao-mv-2026-08-02/luoshen-goddess-palace-reference.png
```

The reference establishes one realistic adult Luo goddess, a very long
floor-sweeping silk gown, moonlit water, and a monumental classical palace.

## Operation

Use `DOUBAO_PROMPT.md` with `scripts/doubao_cdp_browser.py prepare`. Do not paste
local paths into Doubao. Validate login, audio attachment, image attachment,
prompt, visible cost, duration, and model before one guarded submission.

If Doubao cannot preserve the uploaded song, generate the visual sequence and
replace its soundtrack with the reviewed MP3 after download.

## Completed Proof Run

- Doubao conversation: `https://www.doubao.com/chat/38436450640289026`
- Model/duration: Seedance 2.0 Mini, automatic 10 seconds, daily free quota.
- Direct audio upload: unavailable; image input accepted only image formats.
- Reference-image attempt: rejected because realistic face references are not
  supported by the active Seedance portrait-protection policy.
- Accepted route: text-to-video using `DOUBAO_TEXT_TO_VIDEO_PROMPT_10S.md`.
- Downloaded raw video: `Videos/luan_zheng_luoshen_doubao_visual_10s_2026-08-02.mp4`.
- Song-locked video: `Videos/luan_zheng_luoshen_doubao_music_locked_10s_2026-08-02.mp4`.
