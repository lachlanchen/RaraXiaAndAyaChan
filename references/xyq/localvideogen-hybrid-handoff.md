# Xiaoyunque And LocalVideoGen Hybrid Workflow

Reviewed the adjacent LocalVideoGen repository on 2026-09-25. This is a
capability-based plan, not a claim that a hybrid render has passed visual QA.

## Division Of Work

Keep accepted Xiaoyunque footage. Local H3 can generate a new reference-guided
shot, an establishing view, or a short continuation without spending XYQ
credits. Matching four character identities and multilingual speaking voices
across two models is not guaranteed. Prefer a silent/ambient insert for the
first hybrid attempt, keeping existing dialogue and music intact.

For the mooncake episode, the approved route is a complete 29-second Mini trial
video within 116 credits. Local generation remains a fallback, not a parallel
duplicate of the same episode.

## Existing Local Interfaces

Read these files in the configured LocalVideoGen checkout:

- `README.md`: supported image/video reference modes and runtime policy.
- `docs/local-series-api.md`: local-only Series API v2 and stdlib client.
- `scripts/localvideogen_series.py`: upload, create, start, status and artifact
  download through the same admission gates used by H3 Studio.
- `docs/model-updates-2026-09.md`: optional Turbo presets and their limitations.
- `docs/reference-subtitle-guard.md`: visual-reference subtitle preflight.

H3 Studio normally listens on loopback port 8190; ComfyUI uses 8188. Check
`/api/config` and deep health before uploads. A failed connection means the
service is unavailable, not permission to start an additional runtime. On this
review, Studio was not listening; no local generation service was started.

## Handoff And Validation

1. Pick one accepted XYQ shot and preserve its original MP4 and soundtrack.
2. Prepare the same individual character references and scene image. An exact
   final frame and a short clean continuity tail may guide a successor shot.
3. Choose an explicit audio intent: `ambient`, `source`, or `conversation`.
   Conversation requires the actual ordered speaker/text lines. Do not rely on
   a prose prompt alone to establish the audio contract.
4. Use existing normalization and memory admission. Visual video references
   require bounded dimensions; long-reference runs use the documented safe
   quality/offload route. Do not bypass it to match XYQ dimensions exactly.
5. Check RAM, swap, GPU ownership and active jobs. GPU 0 is the project's default
   work device; preserve GPU 1 for LocalLLM unless its owner explicitly releases
   it. Start one job only, through the existing lifecycle and render interfaces.
6. Inspect the new shot's faces, anatomy, movement, boundary continuity, audio
   and complete decode. Preserve the output and report failures; no automatic
   rerender loops.
7. Match aspect ratio, cadence, color and loudness only as needed for the edit.
   Use a motivated cut rather than dissolving unlike faces over each other.
   Keep originals, and write a manifest of selected shot ranges and audio.

The local API does not start or stop the engine. Service startup is a separate
resource-checked operation. Hybrid capability does not authorize publication;
use the normal LazyEdit pipeline only when publishing is requested.
