#!/usr/bin/env python3
"""Poll a submitted Xiaoyunque browser thread and download the first video.

This uses the logged-in Chrome DevTools browser only. It does not call the
Xiaoyunque API and does not submit a new generation task.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import websocket


DEFAULT_CDP_URL = "http://127.0.0.1:9222"
VIDEO_RE = re.compile(r"\.mp4|m3u8|everphoto-media|media|video|tos|blob:", re.I)
NOISE_RE = re.compile(r"/api/|/commerce/|sdk|\.js($|\?)|\.css($|\?)|xgplayer|captcha|webmssdk", re.I)


class CdpPage:
    def __init__(self, page_id: str, cdp_url: str) -> None:
        pages = json.load(urllib.request.urlopen(f"{cdp_url}/json/list", timeout=10))
        target = next((page for page in pages if page.get("id") == page_id), None)
        if not target:
            raise RuntimeError(f"page id not found: {page_id}")
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


def list_page_ids(cdp_url: str) -> set[str]:
    pages = json.load(urllib.request.urlopen(f"{cdp_url}/json/list", timeout=10))
    return {page.get("id", "") for page in pages if page.get("type") == "page"}


def open_thread_page(cdp_url: str, thread_url: str) -> str:
    encoded = urllib.parse.quote(thread_url, safe="")
    req = urllib.request.Request(f"{cdp_url}/json/new?{encoded}", method="PUT")
    page = json.load(urllib.request.urlopen(req, timeout=10))
    return page["id"]


def resolve_page_id(args: argparse.Namespace) -> str:
    if args.page_id and args.page_id in list_page_ids(args.cdp_url):
        return args.page_id
    if not args.thread_url:
        raise SystemExit("Provide --page-id for a live tab or --thread-url to reopen the submitted task.")
    page_id = open_thread_page(args.cdp_url, args.thread_url)
    if args.page_id_file:
        args.page_id_file.write_text(page_id + "\n", encoding="utf-8")
    time.sleep(args.initial_wait)
    return page_id


PROBE_JS = r"""
(() => {
  const text = document.body.innerText || '';
  const status = (text.match(/(生成中|大约还需\s*\d+\s*分钟|完成|下载|失败|内部错误|积分不足|余额不足|审核|合规)/g) || []).slice(-30);
  const videos = [...document.querySelectorAll('video')].map((v, i) => ({
    i,
    src: v.currentSrc || v.src || '',
    poster: v.poster || '',
    ready: v.readyState,
    duration: Number.isFinite(v.duration) ? v.duration : null,
    w: v.videoWidth,
    h: v.videoHeight,
    rect: (() => {
      const r = v.getBoundingClientRect();
      return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
    })()
  }));
  const anchors = [...document.querySelectorAll('a[href]')]
    .map(a => a.href)
    .filter(h => /mp4|download|media|video|everphoto|tos/i.test(h))
    .slice(-100);
  const resources = performance.getEntriesByType('resource')
    .map(e => e.name)
    .filter(h => /mp4|m3u8|media|video|everphoto|tos/i.test(h))
    .slice(-240);
  const buttons = [...document.querySelectorAll('button,[role=button]')]
    .map(b => (b.innerText || b.getAttribute('aria-label') || b.title || '').trim())
    .filter(Boolean)
    .filter(t => /下载|完成|失败|重试|发布|生成/.test(t))
    .slice(-30);
  return {
    time: new Date().toISOString(),
    href: location.href,
    points: (document.querySelector('[class*=pointsBadgeButton]')?.innerText || '').trim(),
    status,
    videos,
    anchors,
    resources,
    buttons,
    tail: text.slice(-1500)
  };
})()
"""


def load_ignore_urls(path: Path | None) -> set[str]:
    if not path or not path.exists():
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def candidate_urls(data: dict[str, Any], ignore: set[str]) -> list[str]:
    urls: list[str] = []
    for video in data.get("videos") or []:
        for key in ("src", "poster"):
            url = video.get(key) or ""
            if url and "pippit-loading" not in url:
                urls.append(url)
    urls.extend(
        url
        for url in (data.get("anchors") or []) + (data.get("resources") or [])
        if url and "pippit-loading" not in url
    )

    seen: list[str] = []
    for url in urls:
        if url in seen or url in ignore:
            continue
        if VIDEO_RE.search(url) and not NOISE_RE.search(url):
            seen.append(url)
    return seen


def head_type(url: str) -> tuple[str, str]:
    if url.startswith("blob:"):
        return "blob", ""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as response:
            return response.headers.get("content-type", ""), response.headers.get("content-length", "")
    except Exception as exc:  # noqa: BLE001 - record and continue polling.
        return f"ERR:{type(exc).__name__}", ""


def download(url: str, output_path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=240) as response, output_path.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)


def verify_video(path: Path) -> None:
    if not shutil.which("ffprobe"):
        return
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,codec_name,avg_frame_rate",
            "-show_entries",
            "format=duration,size",
            "-of",
            "json",
            str(path),
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
    )
    if result.stdout:
        print(result.stdout.strip())


def poll(args: argparse.Namespace) -> int:
    ignore = load_ignore_urls(args.ignore_file)
    page_id = resolve_page_id(args)
    page_id_path = args.page_id_file or args.output_dir / "page_id.txt"
    page_id_path.write_text(page_id + "\n", encoding="utf-8")

    output_path = args.output_dir / args.filename
    final_url_path = args.output_dir / "final_url.txt"
    head_log_path = args.output_dir / "candidate_head_checks.txt"

    for index in range(1, args.max_polls + 1):
        if page_id not in list_page_ids(args.cdp_url):
            if not args.thread_url:
                raise RuntimeError("tab disappeared and --thread-url was not provided")
            page_id = open_thread_page(args.cdp_url, args.thread_url)
            page_id_path.write_text(page_id + "\n", encoding="utf-8")
            time.sleep(args.initial_wait)

        cdp = CdpPage(page_id, args.cdp_url)
        data = cdp.eval(PROBE_JS)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / f"poll_{index:03d}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        status = ",".join(data.get("status") or []) or "no explicit status"
        urls = candidate_urls(data, ignore)
        print(
            f"poll {index:02d}: points={data.get('points')} status={status} "
            f"videos={len(data.get('videos') or [])} candidates={len(urls)}",
            flush=True,
        )

        if any(token in status for token in ("失败", "内部错误", "积分不足", "余额不足", "审核", "合规")):
            return 43

        for url in urls:
            content_type, content_length = head_type(url)
            with head_log_path.open("a", encoding="utf-8") as handle:
                handle.write(f"{time.strftime('%F %T')}\t{content_type}\t{content_length}\t{url}\n")
            if "video" in content_type.lower() or re.search(r"\.mp4(\?|$)", url, re.I):
                final_url_path.write_text(url + "\n", encoding="utf-8")
                print(f"downloading: {url}", flush=True)
                download(url, output_path)
                if args.copy_to_videos:
                    args.copy_to_videos.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(output_path, args.copy_to_videos / output_path.name)
                    print(f"copied: {args.copy_to_videos / output_path.name}", flush=True)
                verify_video(output_path)
                return 0

        time.sleep(args.interval)
    return 124


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL)
    parser.add_argument("--page-id", help="Existing CDP page id for the Xiaoyunque task tab")
    parser.add_argument("--page-id-file", type=Path, help="Read/write page id here")
    parser.add_argument("--thread-url", help="Submitted Xiaoyunque thread URL, used to reopen the task if needed")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--filename", default="xyq_result.mp4")
    parser.add_argument("--copy-to-videos", type=Path, help="Optional folder to copy the downloaded MP4 into")
    parser.add_argument("--ignore-file", type=Path, help="URL list to ignore, useful for uploaded reference assets")
    parser.add_argument("--max-polls", type=int, default=120)
    parser.add_argument("--interval", type=float, default=30)
    parser.add_argument("--initial-wait", type=float, default=5)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.page_id_file and not args.page_id and args.page_id_file.exists():
        args.page_id = args.page_id_file.read_text(encoding="utf-8").strip()
    return poll(args)


if __name__ == "__main__":
    raise SystemExit(main())
