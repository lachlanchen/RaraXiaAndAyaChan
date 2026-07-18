# Shared noVNC/CDP Browser Handoff

Use this note when another repository, agent, or automation tool must operate
the same logged-in Chrome that is visible in noVNC.

## Connection Contract

```text
Purpose: shared logged-in browser for Xiaoyunque and related web workflows
X display: :98
VNC: 127.0.0.1:5908
noVNC: http://127.0.0.1:6099/vnc.html?host=127.0.0.1&port=6099&autoconnect=1&resize=scale
CDP: http://127.0.0.1:9344
Profile: ${XDG_CACHE_HOME:-$HOME/.cache}/xyq-chrome
Launcher: studio/scripts/launch_xyq_novnc.sh
```

The noVNC viewer and CDP endpoint are two interfaces to the same Chrome:
noVNC provides observable human input; CDP provides precise DOM automation.

## Instructions for the Receiving Tool

1. Run the launcher with `start`. It reuses the current browser when CDP is
   already healthy and exposes its owning X display through noVNC.
2. Verify `/json/version` and open the noVNC URL before doing browser work.
3. Attach to CDP `9344`; do not launch Chrome, select another profile, or use a
   temporary browser context.
4. Enumerate existing pages and reuse the matching tab. Bring it to the front
   before every visible action. Create a tab only when no suitable tab exists.
5. Confirm that the CDP page URL/title is also visible in noVNC. If the two do
   not match, stop instead of operating an unobserved browser.
6. Use normal visible clicks, typing, and file uploads. Use direct HTTP only for
   health probes, not as a substitute for requested UI interaction.
7. Do not close the shared browser when the task ends. In particular, avoid a
   Playwright `browser.close()` call against this CDP connection.

## Start and Check

```bash
cd "$LALACHAN_ROOT/studio"
scripts/launch_xyq_novnc.sh start
scripts/launch_xyq_novnc.sh status

curl -fsS http://127.0.0.1:9344/json/version
curl -fsS http://127.0.0.1:9344/json/list | jq \
  '.[] | {id, title, url, type}'
```

If the receiving project is on another machine, tunnel loopback services rather
than exposing them:

```bash
ssh -N \
  -L 6099:127.0.0.1:6099 \
  -L 9344:127.0.0.1:9344 \
  user@workstation
```

Then use the same `127.0.0.1` URLs locally. Omit the CDP tunnel when only human
viewing is needed.

## Playwright Attachment Pattern

```javascript
import { chromium } from "playwright";

const cdpUrl = process.env.SHARED_CDP_URL ?? "http://127.0.0.1:9344";
const browser = await chromium.connectOverCDP(cdpUrl);
const context = browser.contexts()[0];
const pages = context.pages();
let page = pages.find((candidate) => candidate.url().includes("xyq.jianying.com"));

if (!page) page = await context.newPage();
await page.bringToFront();

// Perform visible, evidence-backed actions here.
// Do not call browser.close(); this is a shared persistent browser.
```

Prefer stable roles, labels, and `data-testid` selectors. Save before/after
screenshots and report the page ID, URL, and observable result.

## Autofit and Clipboard Requirements

- Use full `vnc.html`, not `vnc_lite.html`.
- Include `autoconnect=1&resize=scale` in the noVNC URL.
- Size Chrome to the X display with `xdotool`; viewer scaling alone cannot fix
  a displaced or oversized remote window.
- Use the full-client clipboard panel for bidirectional plain text.

Technical details and the reusable window-fit function are documented in
`references/novnc-cdp-autofit-clipboard-fix-2026-07-18.md`.

## Fail-Closed Checklist

Do not proceed unless all are true:

- CDP `/json/version` responds.
- The noVNC URL loads and shows the complete browser window.
- CDP and noVNC expose the same active tab.
- The expected logged-in profile is present.
- The target page is brought to the front.
- No other process is trying to own the same profile.

Do not restart, log out, clear browser state, open repeated tabs, or destroy the
profile as a recovery shortcut. Preserve the existing session and fix only the
failed display, proxy, or controller layer.
