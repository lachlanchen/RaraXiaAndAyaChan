#!/usr/bin/env python3
"""Watch a submitted Xiaoyunque browser thread and copy the finished MP4.

This is browser/CDP-only. It does not submit a new job and does not call the
Xiaoyunque open API. It reads the logged-in page DOM/resources, waits for a
finished video URL, downloads it, verifies it with ffprobe when available, and
copies it to requested folders.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import websocket


STATUS_RE = (
    r"(排队等待中|优先处理中|生成中|大约还需\s*\d+\s*分钟|还需\s*\d+\s*分钟|"
    r"下载|完成|生成失败|任务失败|内部错误|"
    r"积分不足|余额不足|审核|合规|开会员加速|重新生成)"
)

PROBE_JS = rf"""
(() => {{
  const text = document.body ? (document.body.innerText || '') : '';
  const tail = text.slice(-2500);
  const status = (tail.match(/{STATUS_RE}/g) || []).slice(-100);
  const visible = element => {{
    const rect = element.getBoundingClientRect();
    const style = getComputedStyle(element);
    return rect.width > 2 && rect.height > 2 && style.display !== 'none' && style.visibility !== 'hidden';
  }};
  const hasVisibleDownload = [...document.querySelectorAll('button')].some(button =>
    visible(button) && !button.disabled && (button.innerText || button.textContent || '').trim() === '下载'
  );
  const activeExecutions = [...document.querySelectorAll('button[aria-label]')]
    .map(button => (button.getAttribute('aria-label') || '').trim())
    .filter(label => /执行中|生成中|进行中/.test(label));
  const resultVideos = [...document.querySelectorAll('video')].filter(video =>
    video.closest('.ag-ui-x-biz-video-part') || (visible(video) && hasVisibleDownload)
  );
  const videos = resultVideos.map((v, i) => ({{
    i,
    src: v.currentSrc || v.src || '',
    poster: v.poster || '',
    ready: v.readyState,
    duration: Number.isFinite(v.duration) ? v.duration : null,
    w: v.videoWidth,
    h: v.videoHeight,
    rect: (() => {{
      const r = v.getBoundingClientRect();
      return {{x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}};
    }})()
  }}));
  const resultRoots = [...document.querySelectorAll('.ag-ui-x-biz-video-part')];
  const anchors = resultRoots.flatMap(root => [...root.querySelectorAll('a[href]')])
    .map(a => a.href)
    .filter(h => /mp4|download|media|video|everphoto|tos/i.test(h))
    .slice(-100);
  const resources = performance.getEntriesByType('resource')
    .map(e => e.name)
    .filter(h => /mp4|m3u8|media|video|everphoto|tos/i.test(h))
    .filter(h => !/\.webp|\.png|\.jpg|\.jpeg|sdk|\.js|\.css|sync_asset|common\/upload|pippit_cms/i.test(h))
    .slice(-200);
  return {{
    time: new Date().toISOString(),
    href: location.href,
    points: (document.querySelector('[class*=pointsBadgeButton]')?.innerText || '').trim(),
    status,
    activeExecutions,
    videos,
    anchors,
    resources,
    tail
  }};
}})()
"""


class CdpPage:
    def __init__(self, page_id: str, cdp_url: str) -> None:
        pages = json.load(urllib.request.urlopen(f"{cdp_url}/json/list", timeout=10))
        target = next((page for page in pages if page.get("id") == page_id), None)
        if not target:
            raise RuntimeError(f"CDP page not found: {page_id}")
        self.ws = websocket.create_connection(target["webSocketDebuggerUrl"], timeout=20)
        self.next_id = 0

    def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.next_id += 1
        msg_id = self.next_id
        self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == msg_id:
                if "error" in message:
                    raise RuntimeError(json.dumps(message["error"], ensure_ascii=False))
                return message.get("result", {})

    def eval(self, expression: str) -> Any:
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": True},
        )
        remote = result.get("result", {})
        if remote.get("subtype") == "error":
            raise RuntimeError(remote.get("description", "Runtime.evaluate failed"))
        return remote.get("value")

    def navigate(self, url: str) -> None:
        self.call("Page.enable")
        self.call("Page.navigate", {"url": url})


def page_exists(page_id: str, cdp_url: str) -> bool:
    pages = json.load(urllib.request.urlopen(f"{cdp_url}/json/list", timeout=10))
    return any(page.get("id") == page_id for page in pages)


def open_thread_page(thread_url: str, cdp_url: str) -> str:
    encoded = urllib.parse.quote(thread_url, safe="")
    request = urllib.request.Request(f"{cdp_url}/json/new?{encoded}", method="PUT")
    page = json.load(urllib.request.urlopen(request, timeout=10))
    return str(page["id"])


def head_type(url: str) -> tuple[str, str]:
    if url.startswith("blob:"):
        return "blob", ""
    try:
        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://xyq.jianying.com/"},
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.headers.get("content-type", ""), response.headers.get("content-length", "")
    except Exception as exc:  # noqa: BLE001 - record and keep trying other candidates.
        return f"ERR:{type(exc).__name__}", ""


def _response_total_bytes(response: Any, start: int) -> int | None:
    content_range = response.headers.get("content-range", "")
    if "/" in content_range:
        total = content_range.rsplit("/", 1)[-1]
        if total.isdigit():
            return int(total)
    content_length = response.headers.get("content-length", "")
    if content_length.isdigit():
        return start + int(content_length)
    return None


def download(url: str, output: Path, expected_bytes: int | None = None, retries: int = 8) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    partial = output.with_name(f"{output.name}.part")
    # Only a .part file is resumable. An existing final-name file may belong to
    # an older candidate URL, so never append a new response to it.
    if output.exists() and not partial.exists():
        output.unlink()

    for attempt in range(1, retries + 1):
        start = partial.stat().st_size if partial.exists() else 0
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://xyq.jianying.com/"}
        if start:
            headers["Range"] = f"bytes={start}-"
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                status = getattr(response, "status", response.getcode())
                if start and status != 206:
                    start = 0
                    partial.unlink(missing_ok=True)
                response_total = _response_total_bytes(response, start)
                target_bytes = expected_bytes or response_total
                mode = "ab" if start and status == 206 else "wb"
                with partial.open(mode) as handle:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        handle.write(chunk)
        except Exception as exc:  # noqa: BLE001 - resume an interrupted signed transfer.
            print(
                f"download attempt {attempt}/{retries} interrupted at "
                f"{partial.stat().st_size if partial.exists() else 0} bytes: "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )
            if attempt == retries:
                raise
            time.sleep(min(attempt * 2, 10))
            continue

        size = partial.stat().st_size
        if target_bytes is not None and size < target_bytes:
            print(
                f"download attempt {attempt}/{retries} ended early: "
                f"{size}/{target_bytes} bytes; resuming",
                flush=True,
            )
            if attempt == retries:
                raise RuntimeError(f"incomplete download: {size}/{target_bytes} bytes")
            time.sleep(min(attempt * 2, 10))
            continue
        if target_bytes is not None and size > target_bytes:
            raise RuntimeError(f"download exceeded expected size: {size}/{target_bytes} bytes")

        os.replace(partial, output)
        return

    raise RuntimeError("download retries exhausted")


def browser_fetch_info(page: CdpPage, url: str) -> dict[str, Any]:
    expression = f"""
(async () => {{
  try {{
    const response = await fetch({json.dumps(url)}, {{credentials: 'include'}});
    return {{
      ok: response.ok,
      status: response.status,
      type: response.headers.get('content-type') || '',
      length: response.headers.get('content-length') || ''
    }};
  }} catch (error) {{
    return {{ok: false, error: String(error)}};
  }}
}})()
"""
    return page.eval(expression)


def trigger_browser_blob_download(page: CdpPage, url: str, filename: str) -> dict[str, Any]:
    expression = f"""
(async () => {{
  try {{
    const response = await fetch({json.dumps(url)}, {{credentials: 'include'}});
    if (!response.ok) return {{ok: false, status: response.status}};
    const blob = await response.blob();
    const objectUrl = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = objectUrl;
    anchor.download = {json.dumps(filename)};
    document.body.appendChild(anchor);
    anchor.click();
    setTimeout(() => {{
      URL.revokeObjectURL(objectUrl);
      anchor.remove();
    }}, 5000);
    return {{ok: true, size: blob.size, type: blob.type}};
  }} catch (error) {{
    return {{ok: false, error: String(error)}};
  }}
}})()
"""
    return page.eval(expression)


def wait_for_browser_download(filename: str, min_bytes: int, timeout: float = 120) -> Path | None:
    downloads = Path.home() / "Downloads"
    deadline = time.time() + timeout
    path = downloads / filename
    partial = downloads / f"{filename}.crdownload"
    while time.time() < deadline:
        if path.exists() and path.stat().st_size >= min_bytes and not partial.exists():
            return path
        time.sleep(1)
    return None


def newest_downloaded_mp4_since(since: float, min_bytes: int) -> Path | None:
    downloads = Path.home() / "Downloads"
    if any(downloads.glob("*.crdownload")):
        return None
    candidates = [
        path
        for path in downloads.glob("*.mp4")
        if path.stat().st_mtime >= since - 3 and path.stat().st_size >= min_bytes
    ]
    if not candidates:
        return None
    latest = max(candidates, key=lambda path: path.stat().st_mtime)
    size = latest.stat().st_size
    time.sleep(1)
    if latest.exists() and latest.stat().st_size == size:
        return latest
    return None


def click_page_download_button(page: CdpPage) -> dict[str, Any]:
    expression = """
(() => {
  const buttons = [...document.querySelectorAll('button')];
  const visible = buttons.filter(button => {
    const r = button.getBoundingClientRect();
    const text = (button.innerText || button.textContent || button.title || button.getAttribute('aria-label') || '').trim();
    return text === '下载' && r.width > 0 && r.height > 0 && !button.disabled;
  });
  const button =
    visible.find(b => String(b.className || '').includes('artifactPreviewDownloadButton')) ||
    visible[visible.length - 1];
  if (!button) {
    const cards = [...document.querySelectorAll('.ag-ui-x-biz-video-part')].filter(card => {
      const r = card.getBoundingClientRect();
      return r.width > 2 && r.height > 2;
    });
    const card = cards[cards.length - 1];
    if (!card) return {ok: false, reason: 'download button and result card not found'};
    card.click();
    return {ok: false, reason: 'opened result preview'};
  }
  const r = button.getBoundingClientRect();
  const x = r.x + r.width / 2;
  const y = r.y + r.height / 2;
  button.dispatchEvent(new MouseEvent('mouseover', {bubbles: true, clientX: x, clientY: y}));
  button.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, clientX: x, clientY: y}));
  button.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, clientX: x, clientY: y}));
  button.click();
  return {ok: true, text: button.innerText, x: Math.round(r.x), y: Math.round(r.y)};
})()
"""
    return page.eval(expression)


def ffprobe(path: Path) -> str:
    if not shutil.which("ffprobe"):
        return ""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size",
            "-show_entries",
            "stream=width,height,codec_name",
            "-of",
            "json",
            str(path),
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def media_duration(path: Path) -> float | None:
    if not shutil.which("ffprobe"):
        return None
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def media_dimensions(path: Path) -> tuple[int, int] | None:
    if not shutil.which("ffprobe"):
        return None
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=p=0:s=x",
            str(path),
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    value = result.stdout.strip()
    if "x" not in value:
        return None
    try:
        width, height = value.split("x", 1)
        return int(width), int(height)
    except ValueError:
        return None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_aspect_ratio(value: str | None) -> float | None:
    if not value:
        return None
    separator = ":" if ":" in value else "/" if "/" in value else None
    if not separator:
        ratio = float(value)
    else:
        width, height = value.split(separator, 1)
        ratio = float(width) / float(height)
    if ratio <= 0:
        raise ValueError("aspect ratio must be positive")
    return ratio


def fully_decodes(path: Path) -> bool:
    if not shutil.which("ffmpeg"):
        return True
    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-nostdin",
                "-v",
                "error",
                "-xerror",
                "-i",
                str(path),
                "-map",
                "0:v:0",
                "-map",
                "0:a:0?",
                "-f",
                "null",
                "-",
            ],
            check=False,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=600,
        )
    except subprocess.TimeoutExpired:
        print(f"candidate rejected: full-stream decode timed out for {path}", flush=True)
        return False
    errors = result.stderr.strip()
    if result.returncode == 0 and not errors:
        return True
    detail = errors.splitlines()[-1] if errors else f"ffmpeg exit {result.returncode}"
    print(f"candidate rejected: incomplete or corrupt media stream for {path}: {detail}", flush=True)
    return False


def media_matches(
    path: Path,
    expected_duration: float | None,
    duration_tolerance: float,
    expected_aspect_ratio: float | None,
    aspect_ratio_tolerance: float,
    excluded_sha256: set[str],
) -> bool:
    digest = file_sha256(path) if excluded_sha256 else ""
    if digest and digest in excluded_sha256:
        print(f"candidate rejected: SHA-256 matches an excluded input asset: {path}", flush=True)
        return False
    if not fully_decodes(path):
        return False

    if expected_duration is not None:
        actual_duration = media_duration(path)
        if actual_duration is None:
            print(f"candidate rejected: cannot verify duration for {path}", flush=True)
            return False
        if abs(actual_duration - expected_duration) > duration_tolerance:
            print(
                f"candidate rejected: duration {actual_duration:.3f}s is outside "
                f"{expected_duration:.3f}s +/- {duration_tolerance:.3f}s for {path}",
                flush=True,
            )
            return False

    if expected_aspect_ratio is not None:
        dimensions = media_dimensions(path)
        if not dimensions or dimensions[1] == 0:
            print(f"candidate rejected: cannot verify dimensions for {path}", flush=True)
            return False
        actual_ratio = dimensions[0] / dimensions[1]
        if abs(actual_ratio - expected_aspect_ratio) > aspect_ratio_tolerance:
            print(
                f"candidate rejected: dimensions {dimensions[0]}x{dimensions[1]} give aspect "
                f"{actual_ratio:.4f}, expected {expected_aspect_ratio:.4f} "
                f"+/- {aspect_ratio_tolerance:.4f} for {path}",
                flush=True,
            )
            return False

    return True


def finish_from_file(source: Path, output: Path, copy_to: list[Path]) -> None:
    if source.resolve() != output.resolve():
        shutil.copy2(source, output)
    probe = ffprobe(output)
    if probe:
        print(probe, flush=True)
    for destination in copy_to:
        if destination.suffix.lower() in {".mp4", ".mov", ".mkv", ".webm"}:
            target = destination
            target.parent.mkdir(parents=True, exist_ok=True)
        else:
            destination.mkdir(parents=True, exist_ok=True)
            target = destination / output.name
        shutil.copy2(output, target)
        print(f"copied: {target}", flush=True)
    print(f"DONE output={output}", flush=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cdp-url", default="http://127.0.0.1:9222")
    parser.add_argument("--page-id", required=True)
    parser.add_argument("--thread-url", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--copy-to", type=Path, action="append", default=[])
    parser.add_argument("--interval", type=float, default=30)
    parser.add_argument("--max-polls", type=int, default=240)
    parser.add_argument("--min-bytes", type=int, default=200_000)
    parser.add_argument("--expected-duration", type=float)
    parser.add_argument("--duration-tolerance", type=float, default=5.0)
    parser.add_argument(
        "--expected-aspect-ratio",
        help="Expected output ratio such as 4:3, 16:9, or 1.3333.",
    )
    parser.add_argument("--aspect-ratio-tolerance", type=float, default=0.03)
    parser.add_argument(
        "--exclude-sha256",
        action="append",
        default=[],
        help="Reject a downloaded candidate whose SHA-256 matches this value.",
    )
    parser.add_argument("--reload-every", type=float, default=600)
    return parser


def has_blocking_status(status: str, tail: str, active_executions: list[str] | None = None) -> bool:
    # Threads keep earlier failure messages in the DOM after the agent has
    # already retried and advanced. A currently executing step is stronger
    # evidence than stale transcript text, so keep monitoring in that case.
    if active_executions:
        return False

    blocking_tokens = ("失败", "内部错误", "审核", "合规")
    if any(token in status for token in blocking_tokens):
        return True

    has_insufficient = "积分不足" in status or "余额不足" in status
    if not has_insufficient:
        return False

    has_queue = (
        "排队等待中" in status
        or "还需" in status
        or "优先处理中" in status
        or "进行中" in status
        or "生成中" in status
    )
    is_channel_upsell = "切换通道积分不足" in tail
    if has_queue and is_channel_upsell:
        return False

    # The thread keeps old messages in the tail. After a user recharges, an
    # earlier insufficient-points message may still match the status regex while
    # the latest state has moved on. Do not stop on stale payment blockers.
    latest_insufficient = max(tail.rfind("积分不足"), tail.rfind("余额不足"))
    latest_payment = max(tail.rfind("支付成功"), tail.rfind("充值成功"))
    if latest_payment > latest_insufficient and has_queue:
        return False

    return True


def main() -> int:
    args = build_parser().parse_args()
    try:
        expected_aspect_ratio = parse_aspect_ratio(args.expected_aspect_ratio)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise SystemExit(f"invalid --expected-aspect-ratio: {exc}") from exc
    excluded_sha256 = {value.lower().strip() for value in args.exclude_sha256 if value.strip()}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / args.filename
    page_id = args.page_id
    seen: set[str] = set()
    start = time.time()
    last_reload = start
    page_download_attempts = 0

    for poll in range(1, args.max_polls + 1):
        if not page_exists(page_id, args.cdp_url):
            print(f"poll {poll:03d}: page id missing; reopening thread", flush=True)
            try:
                page_id = open_thread_page(args.thread_url, args.cdp_url)
                (args.output_dir / "watch_page_id.txt").write_text(page_id + "\n", encoding="utf-8")
                time.sleep(8)
            except Exception as exc:  # noqa: BLE001 - keep the watcher alive.
                print(f"poll {poll:03d}: reopen failed {type(exc).__name__}: {exc}", flush=True)
                time.sleep(args.interval)
                continue

        try:
            page = CdpPage(page_id, args.cdp_url)
        except Exception as exc:  # noqa: BLE001 - keep the watcher alive.
            print(f"poll {poll:03d}: attach failed {type(exc).__name__}: {exc}", flush=True)
            time.sleep(args.interval)
            continue

        try:
            if poll == 1:
                page.eval("performance.clearResourceTimings(); true")
            if time.time() - last_reload > args.reload_every:
                page.navigate(args.thread_url)
                last_reload = time.time()
                time.sleep(8)
            data = page.eval(PROBE_JS)
        except Exception as exc:  # noqa: BLE001 - keep the watcher alive.
            print(f"poll {poll:03d}: cdp error {type(exc).__name__}: {exc}", flush=True)
            time.sleep(args.interval)
            continue

        (args.output_dir / f"watch_{poll:03d}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        status = ",".join(data.get("status") or []) or "no explicit status"
        videos = data.get("videos") or []
        print(
            f"poll {poll:03d}: points={data.get('points')} status={status} "
            f"videos={len(videos)} elapsed={int(time.time() - start)}s",
            flush=True,
        )

        if has_blocking_status(
            status,
            str(data.get("tail") or ""),
            list(data.get("activeExecutions") or []),
        ):
            print("blocking status seen; not retrying automatically", flush=True)
            return 43

        downloaded = newest_downloaded_mp4_since(start, args.min_bytes)
        if downloaded and ("完成" in status or "下载" in status or videos):
            print(f"found browser download: {downloaded}", flush=True)
            if media_matches(
                downloaded,
                args.expected_duration,
                args.duration_tolerance,
                expected_aspect_ratio,
                args.aspect_ratio_tolerance,
                excluded_sha256,
            ):
                finish_from_file(downloaded, output, args.copy_to)
                return 0

        urls = [
            video.get("src") or ""
            for video in videos
            if video.get("src") and not str(video.get("src")).startswith("blob:")
        ]
        video_srcs = set(urls)
        if urls or "下载" in status:
            urls.extend(data.get("anchors") or [])
            urls.extend(data.get("resources") or [])

        for url in urls:
            if not url or url in seen:
                continue
            seen.add(url)
            if url.startswith("blob:"):
                download_name = f"{output.stem}.browser.{int(time.time())}{output.suffix}"
                try:
                    triggered = trigger_browser_blob_download(page, url, download_name)
                except Exception as exc:  # noqa: BLE001 - keep trying other candidates.
                    print(f"browser blob download failed: {type(exc).__name__}: {exc}", flush=True)
                    continue
                print(f"browser blob download: {json.dumps(triggered, ensure_ascii=False)}", flush=True)
                if not triggered.get("ok"):
                    continue
                downloaded = wait_for_browser_download(download_name, args.min_bytes)
                if not downloaded or not media_matches(
                    downloaded,
                    args.expected_duration,
                    args.duration_tolerance,
                    expected_aspect_ratio,
                    args.aspect_ratio_tolerance,
                    excluded_sha256,
                ):
                    continue
                finish_from_file(downloaded, output, args.copy_to)
                return 0
            content_type, content_length = head_type(url)
            print(f"candidate: {content_type} {content_length} {url[:180]}", flush=True)
            if content_type.startswith("ERR:") or content_type.startswith("text/html"):
                if url in video_srcs:
                    try:
                        info = browser_fetch_info(page, url)
                    except Exception as exc:  # noqa: BLE001 - keep trying other candidates.
                        print(f"browser fetch probe failed: {type(exc).__name__}: {exc}", flush=True)
                        continue
                    print(f"browser fetch: {json.dumps(info, ensure_ascii=False)}", flush=True)
                    if info.get("ok") and "video" in str(info.get("type", "")).lower():
                        download_name = f"{output.stem}.browser.{int(time.time())}{output.suffix}"
                        try:
                            triggered = trigger_browser_blob_download(page, url, download_name)
                        except Exception as exc:  # noqa: BLE001 - keep trying other candidates.
                            print(f"browser download trigger failed: {type(exc).__name__}: {exc}", flush=True)
                            continue
                        print(f"browser download trigger: {json.dumps(triggered, ensure_ascii=False)}", flush=True)
                        if not triggered.get("ok"):
                            continue
                        downloaded = wait_for_browser_download(download_name, args.min_bytes)
                        if not downloaded:
                            print(f"browser download not found: {download_name}", flush=True)
                            continue
                        if media_matches(
                            downloaded,
                            args.expected_duration,
                            args.duration_tolerance,
                            expected_aspect_ratio,
                            args.aspect_ratio_tolerance,
                            excluded_sha256,
                        ):
                            finish_from_file(downloaded, output, args.copy_to)
                            return 0
                continue
            if "video" not in content_type.lower() and ".mp4" not in url.lower():
                continue

            try:
                expected_bytes = int(content_length) if content_length.isdigit() else None
                download(url, output, expected_bytes=expected_bytes)
            except Exception as exc:  # noqa: BLE001 - protected URLs can expire or require page-only access.
                print(f"download failed: {type(exc).__name__}: {exc}", flush=True)
                continue
            if output.stat().st_size < args.min_bytes:
                print(f"download too small: {output.stat().st_size}", flush=True)
                continue

            if media_matches(
                output,
                args.expected_duration,
                args.duration_tolerance,
                expected_aspect_ratio,
                args.aspect_ratio_tolerance,
                excluded_sha256,
            ):
                finish_from_file(output, output, args.copy_to)
                return 0

        if videos and ("完成" in status or "下载" in status) and page_download_attempts < 3:
            page_download_attempts += 1
            click_time = time.time()
            try:
                clicked = click_page_download_button(page)
            except Exception as exc:  # noqa: BLE001 - keep polling if the UI shifts.
                print(f"page download click failed: {type(exc).__name__}: {exc}", flush=True)
                clicked = {"ok": False}
            print(f"page download click: {json.dumps(clicked, ensure_ascii=False)}", flush=True)
            if clicked.get("ok"):
                deadline = time.time() + 120
                while time.time() < deadline:
                    downloaded = newest_downloaded_mp4_since(click_time, args.min_bytes)
                    if downloaded:
                        print(f"found browser download: {downloaded}", flush=True)
                        if media_matches(
                            downloaded,
                            args.expected_duration,
                            args.duration_tolerance,
                            expected_aspect_ratio,
                            args.aspect_ratio_tolerance,
                            excluded_sha256,
                        ):
                            finish_from_file(downloaded, output, args.copy_to)
                            return 0
                    time.sleep(1)

        time.sleep(args.interval)

    print("timed out waiting for Xiaoyunque result", flush=True)
    return 124


if __name__ == "__main__":
    raise SystemExit(main())
