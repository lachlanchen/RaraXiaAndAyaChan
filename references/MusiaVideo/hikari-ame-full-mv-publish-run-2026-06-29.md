# Hikari Ame Full MV Publish Run

Date: 2026-06-29

This records the completed publish workflow for the portrait blur-fill version of the full **Hikari Ame** MV.

## Final Source

```text
Videos/aya_chan_hikari_ame_full_mv_song_locked_portrait_blurfill_fg30_2026-06-29.mp4
```

Verified source:

```text
1080x1920, H.264 yuv420p, AAC, 68.022s, 102.4 MB
sha256: 6a461d80b3a057146b3cd5f228e56a7d283d2a8be0baac2458ebe29678920c66
```

This version places the sharp foreground around `fg-y 576`, leaving roughly top 30%, foreground 30%, bottom 40%. This looked better than the first portrait layout where the foreground sat too high and the lower blurred area dominated the frame.

## LazyEdit Processing

LazyEdit video id:

```text
425
```

Processed publication session:

```text
15
```

The processed output used normal LazyEdit subtitle/logo logic:

- corrected subtitles from the Hikari Ame lyrics and MV prompt context;
- normal LazyEdit subtitle burn;
- logo position set to `top-right`;
- publish category set to `lalamv`.

Future rule: when LazyEdit has portrait blur-fill available as a built-in feature, prefer the LazyEdit feature and reburn subtitles/logo there. Avoid manual subtitle/logo burning unless it is a recovery path.

## Publish Routing

Canonical category:

```text
lalamv
```

Requested platform routing:

```text
YouTube playlist: LalaMV
Shipinhao collection: LalaMV
Instagram: no category UI; metadata only
```

The five canonical LazyEdit/AutoPublish categories are:

```text
simplelife
lazyingart
musia
lalachan
lalamv
```

`music` is kept only as a backwards-compatible alias for `musia`.

## Publish Results

All-platform job:

```text
LazyEdit publish job: 240
Remote AutoPublish job: job-1782710628734-1
Platforms: shipinhao, youtube, instagram
```

Result:

- Shipinhao: succeeded.
- Instagram: succeeded.
- YouTube: failed at first due playlist UI issues.

YouTube-only recovery job:

```text
LazyEdit publish job: 243
Remote AutoPublish job: job-1782711770236-1
Platform: youtube
Result: done
```

## Problems Found

### Shipinhao Collection

The publish form only exposed these collections:

```text
简单生活共499个内容
懒人艺术共0个内容
```

`LalaMV` was not selectable. AutoPublish continued and published without a collection. The collection creation helper could not find a visible create control on the current Shipinhao management page, so Shipinhao collection creation still needs either manual creation or a deeper UI-specific automation update.

### YouTube Playlist

AutoPublish attempted to select/create the YouTube playlist `LalaMV`.

Problems found:

- missing playlist originally caused a fatal failure;
- after creating the playlist, YouTube left a transparent overlay/backdrop that intercepted the next click;
- the newly created playlist did not immediately appear as selectable;
- the playlist state then interfered with the `Not Made for Kids` radio click.

Fixes applied to `AutoPublish/pub_y2b.py` and synced to the remote AutoPublish host:

- playlist creation/selection is now best effort, not a fatal blocker;
- stale transparent YouTube overlay backdrops are cleared after playlist dialog handling;
- `Not Made for Kids` uses scroll-into-view and JS click fallback.

Final YouTube publish succeeded after those fixes. The job carried `publishCategory: lalamv` and `youtubePlaylist: LalaMV`; the playlist selection itself was skipped after the UI failed to expose the newly created playlist.

## Reusable Command Shape

Full process and publish:

```bash
python scripts/lazyedit_publish.py \
  --video /path/to/final_portrait.mp4 \
  --expect-sha256 SHA256 \
  --expect-duration 68.022 \
  --duration-tolerance 0.5 \
  --expect-min-size-mb 90 \
  --expect-max-size-mb 130 \
  --use-current-settings \
  --platforms shipinhao,youtube,instagram \
  --publish-category lalamv \
  --youtube-playlist LalaMV \
  --shipinhao-collection LalaMV \
  --correct-subtitles \
  --correction-source polished \
  --correction-prompt-file references/MusiaVideo/hikari-ame-full-mv-subtitle-correction-context-2026-06-29.md \
  --metadata-prompt-file references/MusiaVideo/hikari-ame-full-mv-publish-metadata-2026-06-29.md \
  --burn-subtitles \
  --logo-position top-right \
  --new-run \
  --guided-monitor \
  --wait
```

YouTube-only recovery from an already processed session:

```bash
python scripts/lazyedit_publish.py \
  --video-id 425 \
  --publication-session-id 15 \
  --use-current-settings \
  --platforms youtube \
  --publish-category lalamv \
  --youtube-playlist LalaMV \
  --no-process \
  --new-run \
  --guided-monitor \
  --wait
```

Use `--new-run` for recovery retries; otherwise LazyEdit may reattach to a stale failed publish job.

