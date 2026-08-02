#!/usr/bin/env python3
"""Guarded Chrome/CDP controller for Doubao music and video workflows."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websocket


DEFAULT_CDP = "http://127.0.0.1:9344"
DOUBAO_URL = "https://www.doubao.com/chat/"


def targets(cdp_url: str) -> list[dict]:
    with urllib.request.urlopen(f"{cdp_url}/json/list", timeout=10) as response:
        return json.load(response)


def new_page(cdp_url: str, url: str) -> dict:
    encoded = urllib.parse.quote(url, safe="")
    request = urllib.request.Request(f"{cdp_url}/json/new?{encoded}", method="PUT")
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def find_page(cdp_url: str, page_id: str | None = None, create: bool = False) -> dict:
    pages = [page for page in targets(cdp_url) if page.get("type") == "page"]
    if page_id:
        found = next((page for page in pages if page.get("id") == page_id), None)
        if not found:
            raise SystemExit(f"Doubao page not found: {page_id}")
        return found
    found = next((page for page in pages if "doubao.com" in page.get("url", "")), None)
    if found:
        return found
    if create:
        return new_page(cdp_url, DOUBAO_URL)
    raise SystemExit("No Doubao tab found. Run: doubao_cdp_browser.py open")


class Cdp:
    def __init__(self, page: dict) -> None:
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=20)
        self.seq = 0

    def call(self, method: str, params: dict | None = None) -> dict:
        self.seq += 1
        request_id = self.seq
        self.ws.send(json.dumps({"id": request_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == request_id:
                if message.get("error"):
                    raise RuntimeError(json.dumps(message["error"], ensure_ascii=False))
                return message.get("result", {})

    def eval(self, javascript: str) -> object:
        result = self.call(
            "Runtime.evaluate",
            {"expression": javascript, "returnByValue": True, "awaitPromise": True},
        ).get("result", {})
        return result.get("value", result)

    def screenshot(self, output: Path) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = self.call("Page.captureScreenshot", {"format": "png", "fromSurface": True})
        output.write_bytes(base64.b64decode(payload["data"]))

    def upload(self, files: list[Path], selector: str = "input[type=file]") -> dict:
        root = self.call("DOM.getDocument", {"depth": -1, "pierce": True})["root"]["nodeId"]
        node_ids = self.call("DOM.querySelectorAll", {"nodeId": root, "selector": selector})["nodeIds"]
        if not node_ids:
            return {"ok": False, "error": "No file input is currently present"}
        kinds = {mimetypes.guess_type(str(path))[0] or "" for path in files}
        desired = "audio" if all(kind.startswith("audio/") for kind in kinds) else "image"
        candidates = []
        for position, node_id in enumerate(node_ids):
            node = self.call("DOM.describeNode", {"nodeId": node_id}).get("node", {})
            raw = node.get("attributes") or []
            attrs = {raw[index]: raw[index + 1] for index in range(0, len(raw), 2)}
            accept = attrs.get("accept", "").lower()
            score = (200 if desired in accept else 0) + (20 if "multiple" in attrs else 0) - position
            candidates.append((score, position, node_id, accept))
        _, position, node_id, accept = max(candidates)
        if desired == "audio" and "audio" not in accept:
            return {
                "ok": False,
                "unsupported": True,
                "kind": "audio",
                "error": "The active Doubao mode has no audio-capable file input",
                "availableAccept": [candidate[3] for candidate in candidates],
            }
        if desired == "image" and not any(token in accept for token in ("image", ".png", ".jpg", ".jpeg", ".webp")):
            return {
                "ok": False,
                "unsupported": True,
                "kind": "image",
                "error": "The active Doubao mode has no image-capable file input",
                "availableAccept": [candidate[3] for candidate in candidates],
            }
        paths = [str(path.resolve()) for path in files]
        self.call("DOM.setFileInputFiles", {"nodeId": node_id, "files": paths})
        return {"ok": True, "position": position, "accept": accept, "files": paths}


STATE_JS = r"""
(() => {
  const visible = e => { const r=e.getBoundingClientRect(), s=getComputedStyle(e); return r.width>2&&r.height>2&&s.display!=='none'&&s.visibility!=='hidden'; };
  const text = e => (e.innerText || e.textContent || '').trim().replace(/\s+/g, ' ');
  const editables = [...document.querySelectorAll('textarea,[contenteditable=true],[contenteditable="plaintext-only"]')].filter(visible);
  const buttons = [...document.querySelectorAll('button,[role=button]')].filter(visible).map(e => text(e)).filter(Boolean);
  const files = [...document.querySelectorAll('input[type=file]')].map((e,i)=>({i,accept:e.accept,multiple:e.multiple}));
  const body = text(document.body);
  return {
    title: document.title, url: location.href,
    loggedIn: !buttons.some(t => t === '登录') && !body.includes('登录后使用'),
    modes: buttons.filter(t => ['视频生成','音乐生成','图像生成'].some(x => t.includes(x))),
    editableCount: editables.length,
    fileInputs: files,
    visibleText: body.slice(0, 1800)
  };
})()
"""


def click_text(cdp: Cdp, label: str) -> object:
    return cdp.eval(
        """(() => {
          const visible=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>2&&r.height>2&&s.display!=='none'&&s.visibility!=='hidden'};
          const nodes=[...document.querySelectorAll('button,[role=button],div,span')].filter(visible);
          const exact=nodes.find(e=>(e.innerText||e.textContent||'').trim()===LABEL);
          const partial=nodes.find(e=>(e.innerText||e.textContent||'').trim().includes(LABEL));
          const target=exact||partial; if(!target)return {ok:false,label:LABEL}; target.click();
          return {ok:true,label:LABEL,tag:target.tagName,text:(target.innerText||target.textContent||'').trim().slice(0,100)};
        })()""".replace("LABEL", json.dumps(label, ensure_ascii=False))
    )


def set_prompt(cdp: Cdp, prompt: str) -> object:
    return cdp.eval(
        """(() => {
          const visible=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>2&&r.height>2&&s.display!=='none'&&s.visibility!=='hidden'};
          const nodes=[...document.querySelectorAll('textarea,[contenteditable=true],[contenteditable="plaintext-only"]')].filter(visible);
          const target=nodes.sort((a,b)=>b.getBoundingClientRect().bottom-a.getBoundingClientRect().bottom)[0];
          if(!target)return {ok:false,error:'No visible composer'};
          target.focus();
          if(target.tagName==='TEXTAREA'){target.value=TEXT;target.dispatchEvent(new Event('input',{bubbles:true}));}
          else{target.replaceChildren(document.createTextNode(TEXT));target.dispatchEvent(new InputEvent('input',{bubbles:true,inputType:'insertText',data:TEXT}));}
          return {ok:true,length:TEXT.length,tag:target.tagName};
        })()""".replace("TEXT", json.dumps(prompt, ensure_ascii=False))
    )


def click_composer_send(cdp: Cdp) -> object:
    return cdp.eval(
        r"""(() => {
          const visible=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>2&&r.height>2&&s.display!=='none'&&s.visibility!=='hidden'};
          const editables=[...document.querySelectorAll('textarea,[contenteditable=true],[contenteditable="plaintext-only"]')].filter(visible);
          const editor=editables.sort((a,b)=>b.getBoundingClientRect().bottom-a.getBoundingClientRect().bottom)[0];
          if(!editor)return {ok:false,error:'No visible composer'};
          const er=editor.getBoundingClientRect();
          const buttons=[...document.querySelectorAll('button,[role=button]')].filter(visible).filter(e=>{
            const r=e.getBoundingClientRect();
            const disabled=e.disabled||e.getAttribute('aria-disabled')==='true';
            return !disabled && r.bottom>=er.bottom-60 && r.top<=er.bottom+80 && r.left>er.left+er.width*0.65;
          }).sort((a,b)=>b.getBoundingClientRect().right-a.getBoundingClientRect().right);
          const target=buttons[0]; if(!target)return {ok:false,error:'No enabled composer send button'};
          const r=target.getBoundingClientRect(); target.click();
          return {ok:true,x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),text:(target.innerText||target.textContent||'').trim()};
        })()"""
    )


def result_state(cdp: Cdp, activate: bool = False) -> dict:
    if activate:
        cdp.eval("(() => { const cards=[...document.querySelectorAll('[class*=block-video]')]; const card=cards[cards.length-1]; if(card) card.click(); return Boolean(card); })()")
        time.sleep(2)
    return cdp.eval(
        r"""(() => {
          const body=document.body.innerText||'';
          const videos=[...document.querySelectorAll('video')].map((v,i)=>({i,src:v.currentSrc||v.src||'',readyState:v.readyState,duration:Number.isFinite(v.duration)?v.duration:null}));
          const complete=body.includes('你的视频生成好了');
          const submitted=body.includes('视频生成已提交');
          const latest=body.slice(-1200);
          return {complete,submitted,videos,latest};
        })()"""
    )


def download_url(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.doubao.com/"})
    with urllib.request.urlopen(request, timeout=120) as response, output.open("wb") as handle:
        while chunk := response.read(1024 * 1024):
            handle.write(chunk)


def validate(cdp: Cdp, prompt: str | None, files: list[Path]) -> dict:
    state = cdp.eval(STATE_JS)
    body = str(state.get("visibleText", ""))
    result = {
        "loggedIn": bool(state.get("loggedIn")),
        "composer": int(state.get("editableCount", 0)) > 0,
        "promptEvidence": bool(prompt and prompt[:24] in body) if prompt else None,
        "requestedFilesExist": all(path.is_file() and path.stat().st_size > 0 for path in files),
        "state": state,
    }
    result["ready"] = result["loggedIn"] and result["composer"] and result["requestedFilesExist"]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cdp-url", default=DEFAULT_CDP)
    parser.add_argument("--page-id")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("open")
    sub.add_parser("list")
    sub.add_parser("status")
    sub.add_parser("front")
    shot = sub.add_parser("screenshot"); shot.add_argument("output", type=Path)
    mode = sub.add_parser("mode"); mode.add_argument("name", choices=["video", "music"])
    upload = sub.add_parser("upload"); upload.add_argument("files", nargs="+", type=Path)
    prompt = sub.add_parser("prompt"); prompt.add_argument("--text"); prompt.add_argument("--file", type=Path)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--prompt-file", required=True, type=Path)
    prepare.add_argument("--audio", type=Path)
    prepare.add_argument("--image", action="append", default=[], type=Path)
    prepare.add_argument("--screenshot", type=Path)
    submit = sub.add_parser("submit")
    submit.add_argument("--confirm-paid", action="store_true")
    result = sub.add_parser("result"); result.add_argument("--activate", action="store_true")
    download = sub.add_parser("download"); download.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if args.command == "list":
        print(json.dumps([{k:p.get(k) for k in ("id","title","url")} for p in targets(args.cdp_url)], ensure_ascii=False, indent=2)); return
    page = find_page(args.cdp_url, args.page_id, create=args.command == "open")
    cdp = Cdp(page)
    cdp.call("Page.bringToFront")
    if args.command == "open": print(json.dumps({"ok":True,"pageId":page["id"],"url":page["url"]}, ensure_ascii=False, indent=2))
    elif args.command == "status": print(json.dumps(cdp.eval(STATE_JS), ensure_ascii=False, indent=2))
    elif args.command == "front": print(json.dumps({"ok":True,"pageId":page["id"]}, indent=2))
    elif args.command == "screenshot": cdp.screenshot(args.output); print(args.output)
    elif args.command == "mode": print(json.dumps(click_text(cdp, "视频生成" if args.name == "video" else "音乐生成"), ensure_ascii=False, indent=2))
    elif args.command == "upload": print(json.dumps(cdp.upload(args.files), ensure_ascii=False, indent=2))
    elif args.command == "prompt":
        value = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
        print(json.dumps(set_prompt(cdp, value), ensure_ascii=False, indent=2))
    elif args.command == "prepare":
        prompt_text = args.prompt_file.read_text(encoding="utf-8")
        requested = ([args.audio] if args.audio else []) + args.image
        missing = [str(path) for path in requested if not path.is_file()]
        if missing: raise SystemExit("Missing files: " + ", ".join(missing))
        mode_result = click_text(cdp, "视频生成")
        time.sleep(1)
        upload_results = []
        if args.audio: upload_results.append(cdp.upload([args.audio]))
        if args.image: upload_results.append(cdp.upload(args.image))
        prompt_result = set_prompt(cdp, prompt_text)
        time.sleep(1)
        evidence = validate(cdp, prompt_text, requested)
        if args.screenshot: cdp.screenshot(args.screenshot)
        print(json.dumps({
            "mode": mode_result,
            "uploads": upload_results,
            "prompt": prompt_result,
            "validation": evidence,
            "externalAudioFallbackRequired": any(
                item.get("unsupported") and item.get("kind") == "audio"
                for item in upload_results
            ),
            "submitted": False,
        }, ensure_ascii=False, indent=2))
    elif args.command == "submit":
        if not args.confirm_paid: raise SystemExit("Refusing paid submit without --confirm-paid")
        state = cdp.eval(STATE_JS)
        if not state.get("loggedIn"): raise SystemExit("Refusing submit: Doubao is not logged in")
        result = click_composer_send(cdp)
        print(json.dumps({"submitted":bool(result.get("ok")),"result":result}, ensure_ascii=False, indent=2))
    elif args.command == "result":
        print(json.dumps(result_state(cdp, activate=args.activate), ensure_ascii=False, indent=2))
    elif args.command == "download":
        state = result_state(cdp, activate=True)
        urls = [item.get("src") for item in state.get("videos", []) if item.get("src")]
        if not urls:
            raise SystemExit("No completed Doubao video source is available")
        download_url(urls[-1], args.output)
        print(json.dumps({"ok": True, "output": str(args.output.resolve()), "source": urls[-1]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
