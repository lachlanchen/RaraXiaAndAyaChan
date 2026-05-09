#!/usr/bin/env python3
"""Small Chrome DevTools helper for Xiaoyunque browser automation."""

from __future__ import annotations

import argparse
import base64
import json
import sys
import time
import urllib.request
from pathlib import Path

import websocket


DEFAULT_CDP = "http://127.0.0.1:9222"


class Cdp:
    def __init__(self, page_id: str, cdp_url: str = DEFAULT_CDP) -> None:
        page = json.load(urllib.request.urlopen(f"{cdp_url}/json/list"))
        target = next((p for p in page if p.get("id") == page_id), None)
        if not target:
            raise SystemExit(f"Page id not found: {page_id}")
        self.ws = websocket.create_connection(target["webSocketDebuggerUrl"], timeout=10)
        self.next_id = 0

    def call(self, method: str, params: dict | None = None) -> dict:
        self.next_id += 1
        msg_id = self.next_id
        self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        while True:
            raw = self.ws.recv()
            msg = json.loads(raw)
            if msg.get("id") == msg_id:
                if "error" in msg:
                    raise RuntimeError(json.dumps(msg["error"], ensure_ascii=False))
                return msg.get("result", {})

    def eval(self, expression: str, *, await_promise: bool = False) -> object:
        result = self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": await_promise,
            },
        )
        remote = result.get("result", {})
        if "value" in remote:
            return remote["value"]
        return remote

    def click(self, x: float, y: float) -> None:
        for event_type in ("mouseMoved", "mousePressed", "mouseReleased"):
            params = {
                "type": event_type,
                "x": x,
                "y": y,
                "button": "left",
                "clickCount": 1,
            }
            if event_type == "mousePressed":
                params["buttons"] = 1
            self.call("Input.dispatchMouseEvent", params)

    def screenshot(self, output: Path) -> None:
        data = self.call("Page.captureScreenshot", {"format": "png", "fromSurface": True})["data"]
        output.write_bytes(base64.b64decode(data))

    def navigate(self, url: str) -> None:
        self.call("Page.enable")
        self.call("Page.navigate", {"url": url})

    def set_file_input_files(self, files: list[Path], selector: str = "input[type=file]", index: int = -1) -> dict:
        root = self.call("DOM.getDocument", {"depth": -1, "pierce": True})["root"]["nodeId"]
        nodes = self.call("DOM.querySelectorAll", {"nodeId": root, "selector": selector})["nodeIds"]
        if not nodes:
            return {"ok": False, "error": f"no nodes for selector: {selector}"}
        node_id = nodes[index]
        abs_files = [str(path.resolve()) for path in files]
        self.call("DOM.setFileInputFiles", {"nodeId": node_id, "files": abs_files})
        return {"ok": True, "selector": selector, "index": index, "nodeCount": len(nodes), "files": abs_files}


def list_pages(args: argparse.Namespace) -> None:
    pages = json.load(urllib.request.urlopen(f"{args.cdp_url}/json/list"))
    for page in pages:
        if page.get("type") == "page":
            print(f"{page.get('id')}\t{page.get('title')}\t{page.get('url')}")


def cmd_eval(args: argparse.Namespace) -> None:
    cdp = Cdp(args.page_id, args.cdp_url)
    result = cdp.eval(args.javascript, await_promise=args.await_promise)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_visible(args: argparse.Namespace) -> None:
    js = r"""
(() => {
  const items = [];
  const nodes = [...document.querySelectorAll('button,[role=button],input,textarea,[contenteditable=true],.uploadMenuItem-GDs2iL,.historyItem-EesJ6i')];
  for (const el of nodes) {
    const r = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    if (r.width < 2 || r.height < 2 || style.visibility === 'hidden' || style.display === 'none') continue;
    items.push({
      tag: el.tagName,
      cls: el.className && String(el.className).slice(0, 120),
      text: (el.innerText || el.getAttribute('title') || el.getAttribute('aria-label') || '').trim().slice(0, 160),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
    });
  }
  return items;
})()
"""
    cdp = Cdp(args.page_id, args.cdp_url)
    print(json.dumps(cdp.eval(js), ensure_ascii=False, indent=2))


def cmd_click(args: argparse.Namespace) -> None:
    cdp = Cdp(args.page_id, args.cdp_url)
    cdp.click(args.x, args.y)


def cmd_click_text(args: argparse.Namespace) -> None:
    contains = json.dumps(args.text, ensure_ascii=False)
    js = f"""
(() => {{
  const needle = {contains};
  const nodes = [...document.querySelectorAll('button,[role=button],.uploadMenuItem-GDs2iL,.historyItem-EesJ6i,div,span')];
  const visible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden';
  }};
  const el = nodes.find(n => visible(n) && ((n.innerText || '').trim().includes(needle) || (n.getAttribute('title') || '').includes(needle)));
  if (!el) return {{ok:false, error:'not found'}};
  const r = el.getBoundingClientRect();
  el.click();
  return {{ok:true, text:(el.innerText || el.getAttribute('title') || '').trim(), x:r.x+r.width/2, y:r.y+r.height/2, cls:String(el.className).slice(0,120)}};
}})()
"""
    cdp = Cdp(args.page_id, args.cdp_url)
    print(json.dumps(cdp.eval(js), ensure_ascii=False, indent=2))


def cmd_navigate(args: argparse.Namespace) -> None:
    cdp = Cdp(args.page_id, args.cdp_url)
    cdp.navigate(args.url)


def cmd_screenshot(args: argparse.Namespace) -> None:
    cdp = Cdp(args.page_id, args.cdp_url)
    cdp.screenshot(Path(args.output))
    print(args.output)


def cmd_set_file_input(args: argparse.Namespace) -> None:
    files = [Path(path) for path in args.files]
    missing = [str(path) for path in files if not path.exists()]
    if missing:
        raise SystemExit(f"Missing files: {', '.join(missing)}")
    cdp = Cdp(args.page_id, args.cdp_url)
    print(json.dumps(cdp.set_file_input_files(files, args.selector, args.index), ensure_ascii=False, indent=2))


def cmd_set_prompt(args: argparse.Namespace) -> None:
    content = Path(args.markdown_file).read_text(encoding="utf-8")
    # Tiptap accepts HTML. Preserve line breaks as paragraphs.
    html_parts = []
    for block in content.split("\n\n"):
        escaped = (
            block.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )
        if escaped.strip():
            html_parts.append(f"<p>{escaped}</p>")
    html = "".join(html_parts)
    js = f"""
(() => {{
  const html = {json.dumps(html, ensure_ascii=False)};
  const el = document.querySelector('.editor-HT1dqv') || document.querySelector('.ProseMirror') || document.querySelector('[contenteditable=true]');
  if (!el) return {{ok:false, error:'editor not found'}};
  if (el.editor && el.editor.commands) {{
    el.editor.commands.setContent(html, true);
    el.editor.commands.focus('end');
    return {{ok:true, method:'tiptap', length:(el.innerText || '').length}};
  }}
  el.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('insertText', false, {json.dumps(content, ensure_ascii=False)});
  return {{ok:true, method:'execCommand', length:(el.innerText || '').length}};
}})()
"""
    cdp = Cdp(args.page_id, args.cdp_url)
    print(json.dumps(cdp.eval(js), ensure_ascii=False, indent=2))


def cmd_wait(args: argparse.Namespace) -> None:
    time.sleep(args.seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cdp-url", default=DEFAULT_CDP)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-pages").set_defaults(func=list_pages)

    p = sub.add_parser("eval")
    p.add_argument("page_id")
    p.add_argument("javascript")
    p.add_argument("--await-promise", action="store_true")
    p.set_defaults(func=cmd_eval)

    p = sub.add_parser("visible")
    p.add_argument("page_id")
    p.set_defaults(func=cmd_visible)

    p = sub.add_parser("click")
    p.add_argument("page_id")
    p.add_argument("x", type=float)
    p.add_argument("y", type=float)
    p.set_defaults(func=cmd_click)

    p = sub.add_parser("click-text")
    p.add_argument("page_id")
    p.add_argument("text")
    p.set_defaults(func=cmd_click_text)

    p = sub.add_parser("navigate")
    p.add_argument("page_id")
    p.add_argument("url")
    p.set_defaults(func=cmd_navigate)

    p = sub.add_parser("screenshot")
    p.add_argument("page_id")
    p.add_argument("output")
    p.set_defaults(func=cmd_screenshot)

    p = sub.add_parser("set-file-input")
    p.add_argument("page_id")
    p.add_argument("files", nargs="+")
    p.add_argument("--selector", default="input[type=file]")
    p.add_argument("--index", type=int, default=-1)
    p.set_defaults(func=cmd_set_file_input)

    p = sub.add_parser("set-prompt")
    p.add_argument("page_id")
    p.add_argument("markdown_file")
    p.set_defaults(func=cmd_set_prompt)

    p = sub.add_parser("wait")
    p.add_argument("seconds", type=float)
    p.set_defaults(func=cmd_wait)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
