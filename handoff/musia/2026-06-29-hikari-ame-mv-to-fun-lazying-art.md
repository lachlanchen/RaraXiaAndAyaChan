# Handoff: Publish Hikari Ame MV To Fun Lazying Art

Status: handoff only. Do not publish from this note without an explicit follow-up request.

## Goal

Publish the generated full MV for **Aya Chan Hikari Ame** to the Musia website at `fun.lazying.art`, using the LalaMedias archive as the source of the clean video and timed subtitle data.

Recommended website item:

```text
media id: aya-chan-hikari-ame-full-mv
canonical URL: https://fun.lazying.art/#aya-chan-hikari-ame-full-mv
kind: video / mv
artist: Musia
category/tag: LalaMV
```

Existing related song item:

```text
media id: aya-chan-hikari-ame
canonical URL: https://fun.lazying.art/#aya-chan-hikari-ame
manifest: /home/lachlan/ProjectsLFS/Musia/website/data/songs/aya-chan-hikari-ame/manifest.json
```

Keep the existing song page available. The MV can either be a new item linked from the song page, or a video tab/asset added to the existing song page if the website UI supports it.

## Source Repositories

```text
LALACHAN:   /home/lachlan/ProjectsLFS/LALACHAN
LalaMedias: /home/lachlan/ProjectsLFS/LalaMedias
Musia:      /home/lachlan/ProjectsLFS/Musia
```

## LalaMedias MV Record

```text
slug: aya-chan-hikari-ame-full-mv-c371e7d0
title: Aya Chan Hikari Ame Full MV
category: lalamv
duration: 68.022s
size: 78,128,088 bytes
dimensions: 1280x720
sha256: c371e7d0c3b01a2677a7a8310ac0e9fc452db98e190cb9a3dbfa89306f861edc
```

Local archive paths:

```text
/home/lachlan/ProjectsLFS/LalaMedias/media/videos/aya-chan-hikari-ame-full-mv-c371e7d0.mp4
/home/lachlan/ProjectsLFS/LalaMedias/media/thumbs/aya-chan-hikari-ame-full-mv-c371e7d0.jpg
/home/lachlan/ProjectsLFS/LalaMedias/data/transcripts/aya-chan-hikari-ame-full-mv-c371e7d0.json
/home/lachlan/ProjectsLFS/LalaMedias/videos/aya-chan-hikari-ame-full-mv-c371e7d0.html
```

GitHub Release video URL:

```text
https://github.com/lachlanchen/LalaMedias/releases/download/media-v1/aya-chan-hikari-ame-full-mv-c371e7d0.mp4
```

Expected LalaMedias website URL if GitHub Pages is enabled:

```text
https://lachlanchen.github.io/LalaMedias/videos/aya-chan-hikari-ame-full-mv-c371e7d0.html
```

## Original Clean Video

The LalaMedias canonical source came from:

```text
/home/lachlan/ProjectsLFS/LALACHAN/Videos/aya_chan_hikari_ame_full_mv_song_locked_2026-06-29.mp4
```

Alternative generated visual-only source:

```text
/home/lachlan/ProjectsLFS/LALACHAN/Videos/aya_chan_hikari_ame_full_mv_xyq_2026-06-29.mp4
```

Use the song-locked version unless there is a clear reason to remix the audio.

## Musia Song Package

Main audio:

```text
/home/lachlan/ProjectsLFS/Musia/data/creative_projects/aya-chan-hikari-ame-20260628/final/aya-chan-hikari-ame-selected.mp3
/home/lachlan/ProjectsLFS/Musia/data/creative_projects/aya-chan-hikari-ame-20260628/final/aya-chan-hikari-ame-selected.wav
```

Existing website cover:

```text
/home/lachlan/ProjectsLFS/Musia/website/assets/covers/aya-chan-hikari-ame-16x9.png
```

Existing song manifest:

```text
/home/lachlan/ProjectsLFS/Musia/website/data/songs/aya-chan-hikari-ame/manifest.json
```

MV prompt/story handoff package:

```text
/home/lachlan/ProjectsLFS/Musia/data/creative_projects/aya-chan-hikari-ame-20260628/mv/hikari-ame-full-hope-battle-20260629
```

## Timed Text And Ruby

LalaMedias transcript JSON:

```text
/home/lachlan/ProjectsLFS/LalaMedias/data/transcripts/aya-chan-hikari-ame-full-mv-c371e7d0.json
```

It currently contains timed entries with tracks:

```text
ja
en
zh
```

Important caveat: the Japanese track is timed and colorized, but the upstream LazyEdit Hikari Ame export had empty `furigana_pairs`, so real furigana is not available yet. Do not fake readings in the website item. Fix or regenerate furigana in LazyEdit/Musia before marking the MV as Japanese-learning complete.

Related LazyEdit bug report:

```text
/home/lachlan/DiskMech/Projects/lazyedit/bug-reports/2026-06-29-hikari-ame-furigana-missing.md
```

## Suggested Musia Website Work

1. Create a new website media item:

```text
/home/lachlan/ProjectsLFS/Musia/website/data/songs/aya-chan-hikari-ame-full-mv/manifest.json
```

2. Add the MV video asset to the manifest. Prefer using the LalaMedias release URL first:

```text
https://github.com/lachlanchen/LalaMedias/releases/download/media-v1/aya-chan-hikari-ame-full-mv-c371e7d0.mp4
```

3. Use the existing cover or generate an MV-specific poster:

```text
/home/lachlan/ProjectsLFS/Musia/website/assets/covers/aya-chan-hikari-ame-16x9.png
```

4. Convert the LalaMedias timed transcript JSON into Musia website lyric/timed-text JSON shape. Preserve current-line timing and `ja/en/zh` tracks.

5. Add the new item to:

```text
/home/lachlan/ProjectsLFS/Musia/website/data/catalog.json
```

6. Link the existing song page and MV page in both directions if the manifest schema supports related media:

```text
song -> full MV
full MV -> original song
```

## Metadata Draft

Use concise viewer-facing metadata, not the full storyboard.

```text
Title: Aya Chan Hikari Ame Full MV
Subtitle: A rain-of-light LALACHAN music video
Description: Aya Chan, RaraXia, Sasa Kun, and Zhuangzi run through a glowing rainstorm in a hopeful Musia MV about small courage becoming light.
Tags: Musia, LALACHAN, LalaMV, Aya Chan, Hikari Ame, music video, Japanese song, rain, hope
Languages: ja, en, zh
```

## Validation Before Publishing

Run from `/home/lachlan/ProjectsLFS/Musia` after implementation:

```bash
npm run website:validate
musia fun-audit --media-id aya-chan-hikari-ame-full-mv
node --check website/app.js
git diff --check
```

If a local preview is needed:

```bash
python3 -m http.server 9174 --directory website
```

Then check:

```text
http://127.0.0.1:9174/#aya-chan-hikari-ame-full-mv
```

Do not publish until the video plays, the current timed line changes correctly, and the Japanese furigana issue is either fixed or explicitly marked as a known caveat.

