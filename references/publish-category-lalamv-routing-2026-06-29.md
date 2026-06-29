# Publish Category Routing: LalaMV

Date: 2026-06-29

Use `publish_category: lalamv` for LALACHAN character music videos and song-led
MVs. This routes platform metadata as:

| Category | YouTube | Shipinhao | Instagram |
| --- | --- | --- | --- |
| `simplelife` | `SimpleLife` playlist | `简单生活` collection | normal caption/tags |
| `lazyingart` | `LazyingArt` playlist | `懒人艺术` collection | normal caption/tags |
| `musia` | `Musia` playlist | `Musia` collection/music package | normal caption/tags |
| `lalachan` | `LALACHAN` playlist | `啦啦侠` collection | normal caption/tags |
| `lalamv` | `LalaMV` playlist | `LalaMV` collection | normal caption/tags |

`music` remains only a backwards-compatible alias for `musia`.

## Publish Command

For an MV, pass category overrides explicitly:

```bash
cd /home/lachlan/DiskMech/Projects/lazyedit
python scripts/lazyedit_publish.py \
  --video-id VIDEO_ID \
  --use-current-settings \
  --publish-category lalamv \
  --youtube-playlist LalaMV \
  --shipinhao-collection LalaMV \
  --platforms shipinhao,youtube,instagram \
  --wait
```

For YouTube/Instagram only:

```bash
python scripts/lazyedit_publish.py \
  --video-id VIDEO_ID \
  --use-current-settings \
  --publish-category lalamv \
  --youtube-playlist LalaMV \
  --platforms youtube,instagram \
  --wait
```

## Category Creation and Backfill

Shipinhao collection creation is available through the management helper:

```bash
ssh lachlan@lazyingart 'cd ~/Projects/autopub && /home/lachlan/venvs/autopub/bin/python scripts/manage_shipinhao_videos.py ensure-collection --collection LalaMV --apply'
```

Dry-run LalaMV backfill:

```bash
ssh lachlan@lazyingart 'cd ~/Projects/autopub && /home/lachlan/venvs/autopub/bin/python scripts/manage_y2b_videos.py move-category --category lalamv --lalamv-playlist LalaMV --scrolls 20 --output /tmp/youtube_lalamv_plan.json'
ssh lachlan@lazyingart 'cd ~/Projects/autopub && /home/lachlan/venvs/autopub/bin/python scripts/manage_shipinhao_videos.py move-category --category lalamv --lalamv-collection LalaMV --scrolls 20 --output /tmp/shipinhao_lalamv_plan.json'
```

Inspect JSON plans before adding `--apply`.

## Validation Performed

- LazyEdit metadata JSON templates now allow exactly `simplelife`,
  `lazyingart`, `musia`, `lalachan`, and `lalamv`.
- AutoPublish route test returned `lalamv -> YouTube LalaMV` and
  `lalamv -> Shipinhao LalaMV`.
- Remote helper tests confirmed `move-category --category lalamv` exists for
  both YouTube and Shipinhao.
- AutoPublish was restarted after the changes and returned an empty healthy
  queue.

## Caveats

YouTube can create the `LalaMV` playlist during upload, but sometimes the new
playlist is not immediately visible in the same upload dialog. In that case,
continue the publish and repair the playlist later with `move-category`.

Shipinhao collection selection depends on the collection being visible in the
current account UI. If upload-time selection fails, publish should continue and
the collection can be created or repaired afterward.

Instagram has no per-post category or playlist in the desktop web upload flow.
The category is only logged for traceability.
