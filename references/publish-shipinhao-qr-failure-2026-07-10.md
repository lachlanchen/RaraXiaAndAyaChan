# Shipinhao QR Failure Note - 2026-07-10

## Context

Video:

```text
Videos/cloud_swordsmen_cotton_parliament_15s_2026-07-10.mp4
```

LazyEdit video id: `467`

Publication session: `46`

Verified ZIP for retry:

```text
/home/lachlan/DiskMech/Projects/lazyedit/DATA/cloud_swordsmen_cotton_parliament_15s_2026-07-10/publications/session_46/publish/cloud_swordsmen_cotton_parliament_15s_2026-07-10_session_46.zip
```

## What Happened

The normal target set was requested:

```text
shipinhao,youtube,instagram,douyin
```

Two combined AutoPublish jobs failed before reaching the non-Shipinhao platforms:

- `job-1783688612790-8`
- `job-1783688798308-9`

Both failed with:

```text
Shipinhao login iframe was not available and the publish editor is not ready.
```

The expected Shipinhao login behavior is to detect the QR code and send the login email. In this run, the automation failed before that QR-email path ran.

To avoid blocking the already-correct package, the same ZIP was then submitted to the remaining platforms only:

- `job-1783688984360-10`
- Platforms: `douyin`, `youtube`, `instagram`
- Final status: `done`
- YouTube URL observed in remote logs: `https://youtube.com/shorts/PqwL__rka8o`

Shipinhao remains pending for this video.

## Future Rule

For normal LALACHAN public videos, always include Shipinhao unless the user explicitly says not to. If Shipinhao blocks on login:

1. Keep the verified ZIP.
2. Publish YouTube, Instagram, and Douyin separately only as a partial fallback.
3. Report Shipinhao as pending, not done.
4. Retry Shipinhao only from the same ZIP after login or QR-email handling is fixed.

## Shipinhao-Only Retry

After the Shipinhao login state is repaired, retry this exact ZIP:

```bash
zip="/home/lachlan/DiskMech/Projects/lazyedit/DATA/cloud_swordsmen_cotton_parliament_15s_2026-07-10/publications/session_46/publish/cloud_swordsmen_cotton_parliament_15s_2026-07-10_session_46.zip"

curl -fsS -X POST \
  "http://lazyingart:8081/publish?filename=cloud_swordsmen_cotton_parliament_15s_2026-07-10_session_46.zip&publish_shipinhao=true&restart_platforms=shipinhao" \
  --data-binary @"$zip"
```

If the same iframe/editor error appears again, inspect and fix the remote AutoPublish Shipinhao login flow before retrying. The bug is that the QR-code email path is not reached for this login-page state.

