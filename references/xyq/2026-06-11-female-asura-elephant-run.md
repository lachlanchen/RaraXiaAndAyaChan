# 2026-06-11 Female Asura Elephant Hunt Video Run

## Outcome

- Output: `Videos/female_asura_elephant_hunt_15s_2026-06-11.mp4`
- Working copy: `outputs/xyq-run/2026-06-11-female-asura-elephant/female_asura_elephant_hunt_15s_2026-06-11.mp4`
- SHA256: `b6de5333b60bc0c98ccbf3a9489e0082f790850bb45b07231fd5fe9b94e63c2e`
- Probe: H.264 + AAC, `1112x836`, `15.125s`, `8519736` bytes

## Browser Settings

- Xiaoyunque browser UI only, no API.
- Mode: `沉浸式短片`
- Model: `Seedance 2.0 Fast`, non-VIP
- Duration: `15秒`
- Ratio: `4:3`
- Cost observed: `75` credits (`5/S` for 15s), leaving `48` points.

## Uploaded References

1. `/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png`
2. `/home/lachlan/ProjectsLFS/LALACHAN/patchwork-leather-notebook-luxury-clean-v2.png`
3. `/home/lachlan/ProjectsLFS/LALACHAN/R1.jpg.jpeg`
4. `/home/lachlan/ProjectsLFS/LALACHAN/R3.jpg.jpeg`
5. `/home/lachlan/ProjectsLFS/LALACHAN/Trio.png`

## Prompt

Prompt source: `references/prompts/2026-06-11-female-asura-elephant-hunt-15s.md`

The prompt explicitly asked for Chinese dialogue, no subtitles, no messy generated text, and preserved `AgInTi` capitalization.

## Notes

- The first page estimate was very long (`168分钟`) but the job continued correctly.
- The page later showed `切换通道积分不足，去充值`; this was an upsell for faster channel switching, not a failed render.
- `scripts/xyq_chrome/watch_thread_dom_download.py` was updated so that `切换通道积分不足` does not stop monitoring when the active job still shows queue/generation status.
- The final download came from a fresh browser-authenticated video URL and was copied to `Videos/`; hashes of the working copy and `Videos/` copy match.
