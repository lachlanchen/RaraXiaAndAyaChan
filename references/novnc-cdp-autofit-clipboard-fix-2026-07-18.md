# noVNC/CDP Autofit and Clipboard Fix

## Problem

The virtual desktop was reachable, but the right side of Chrome was clipped in
the browser viewer. The older URL used the lightweight noVNC client and did not
provide the full clipboard panel. Resizing only the viewer was insufficient
when Chrome had restored an oversized or displaced top-level window.

The working fix has two layers:

1. Render the complete remote desktop with the full noVNC client and scale it
   inside the local browser viewport.
2. Move and resize the remote Chrome window to the exact X display geometry.

## Correct Viewer URL

Use the full client:

```text
http://127.0.0.1:${NOVNC_PORT}/vnc.html?host=127.0.0.1&port=${NOVNC_PORT}&autoconnect=1&resize=scale
```

Do not use the obsolete form:

```text
vnc_lite.html?...&scale=1
```

`vnc.html` supplies the control bar and clipboard panel. `resize=scale` keeps
the remote desktop aspect ratio while fitting the whole canvas into the viewer.
It does not change the server display resolution.

## Reference Stack

The shared logged-in browser currently uses:

| Component | Value |
| --- | --- |
| X display | `:98` |
| X geometry | `1920x1080x24` |
| VNC | `127.0.0.1:5908` |
| noVNC | `127.0.0.1:6099` |
| Chrome CDP | `http://127.0.0.1:9344` |
| Chrome profile | `${XDG_CACHE_HOME:-$HOME/.cache}/xyq-chrome` |

The Lala Studio browser is intentionally separate on display `:96`, noVNC
port `6116`, CDP port `9466`, and its own profile. Do not mix the two profiles.

## Launch Pattern

The reusable implementation is in
`studio/scripts/launch_xyq_novnc.sh`. Its essential process topology is:

```bash
Xvfb :98 -screen 0 1920x1080x24 -ac -nolisten tcp
x11vnc -display :98 -localhost -nopw -forever -shared -noxdamage \
  -rfbport 5908
websockify --web=/usr/share/novnc \
  127.0.0.1:6099 127.0.0.1:5908

DISPLAY=:98 google-chrome \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9344 \
  --remote-allow-origins=http://127.0.0.1:9344 \
  --user-data-dir="${XDG_CACHE_HOME:-$HOME/.cache}/xyq-chrome" \
  --no-first-run --no-default-browser-check \
  --hide-crash-restore-bubble \
  --window-position=0,0 --window-size=1920,1080
```

The production launcher is idempotent: it first probes CDP. If the browser is
already running, it discovers the X display that owns its window and attaches
x11vnc to that display. It must not launch a second Chrome with the same profile.

## Fit the Browser Window

After Chrome is ready, locate its top-level window and fit it to the root X
display. This handles restored window coordinates and browser chrome that would
otherwise extend beyond the visible canvas.

```bash
fit_browser_window() {
  local display="$1" pid="$2" window width height
  window="$(DISPLAY="$display" xdotool search --onlyvisible --pid "$pid" \
    2>/dev/null | tail -n 1 || true)"
  [[ -n "$window" ]] || \
    window="$(DISPLAY="$display" xdotool search --pid "$pid" \
      2>/dev/null | tail -n 1 || true)"
  [[ -n "$window" ]] || return 1

  read -r width height < <(DISPLAY="$display" xdotool getdisplaygeometry)
  DISPLAY="$display" xdotool \
    windowmap "$window" \
    windowmove --sync "$window" 0 0 \
    windowsize --sync "$window" "$width" "$height" \
    windowraise "$window"
}
```

Run it again after a desktop restart or if Chrome restores an old window size.

## Clipboard

Open the noVNC control bar and select the clipboard icon. For host-to-remote
text, paste into the noVNC clipboard panel, focus Chrome, then paste normally.
For remote-to-host text, copy inside Chrome and retrieve it from the same panel.
This is intended for text; file and rich-image clipboard transfer is not part
of the contract.

## Verification

```bash
curl -fsS http://127.0.0.1:9344/json/version
curl -fsS 'http://127.0.0.1:6099/vnc.html?host=127.0.0.1&port=6099&autoconnect=1&resize=scale' >/dev/null
DISPLAY=:98 xdpyinfo | rg 'dimensions|depth of root window'
DISPLAY=:98 xdotool getdisplaygeometry
DISPLAY=:98 xwininfo -root -tree | head -n 80
ss -ltnp | rg ':5908|:6099|:9344'
```

Success means the entire `1920x1080` desktop is visible at once, Chrome fills
that desktop without clipping, the noVNC clipboard panel works for text, and
CDP lists the same tabs visible in noVNC.

## Security and Recovery

- Bind VNC, noVNC, and CDP to `127.0.0.1`; never expose an authenticated Chrome
  profile directly to a LAN or the Internet.
- Use an SSH tunnel for remote viewing. CDP grants control over logged-in tabs,
  so tunnel it only to a trusted operator when automation is required.
- Never copy, delete, overwrite, or commit the Chrome profile directory.
- If CDP is healthy but its window cannot be found on an accessible X display,
  fail closed. Do not start another browser against the same profile.
- If only the viewer is clipped, correct the URL and window geometry. Do not
  restart Chrome or destroy its session unnecessarily.

Implemented in Lala Studio commit `f8ce4f5`.
