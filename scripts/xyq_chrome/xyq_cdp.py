#!/usr/bin/env python3
"""Chrome DevTools Protocol helper for Xiaoyunque (小云雀).

Launch Chrome with scripts/xyq_chrome/launch_chrome.sh first. Normal Chrome
windows cannot be attached after the fact unless they were started with a
remote-debugging port.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import websocket


DEFAULT_DEBUG_URL = "http://127.0.0.1:9222"
DEFAULT_XYQ_URL = "https://xyq.jianying.com/home?tab_name=integrated-agent"
DEFAULT_XYQ_HOME_URL = "https://xyq.jianying.com/home?tab_name=home"
DEFAULT_XYQ_DUANJU_URL = "https://xyq.jianying.com/novel/list?enter_from=small_tool"
MODE_ALIASES = {
    "agent": "Agent 模式",
    "agent模式": "Agent 模式",
    "agent moshi": "Agent 模式",
    "短剧": "短剧 Agent",
    "短剧agent": "短剧 Agent",
    "duanju": "短剧 Agent",
    "duanju agent": "短剧 Agent",
    "duanpian": "沉浸式短片",
    "chenjinshi duanpian": "沉浸式短片",
    "短片": "沉浸式短片",
    "沉浸式短片": "沉浸式短片",
    "long2": "智能长视频 2.0",
    "长视频2.0": "智能长视频 2.0",
    "zhineng changshipin 2.0": "智能长视频 2.0",
    "长视频": "智能长视频",
    "image": "生成图片",
    "图片": "生成图片",
}
MODE_URL_ALIASES = {
    "agent": DEFAULT_XYQ_URL,
    "agent模式": DEFAULT_XYQ_URL,
    "agent moshi": DEFAULT_XYQ_URL,
    "短剧": DEFAULT_XYQ_DUANJU_URL,
    "短剧agent": DEFAULT_XYQ_DUANJU_URL,
    "duanju": DEFAULT_XYQ_DUANJU_URL,
    "duanju agent": DEFAULT_XYQ_DUANJU_URL,
    "duanpian": DEFAULT_XYQ_HOME_URL,
    "chenjinshi duanpian": DEFAULT_XYQ_HOME_URL,
    "短片": DEFAULT_XYQ_HOME_URL,
    "沉浸式短片": DEFAULT_XYQ_HOME_URL,
    "long2": DEFAULT_XYQ_HOME_URL,
    "长视频2.0": DEFAULT_XYQ_HOME_URL,
    "zhineng changshipin 2.0": DEFAULT_XYQ_HOME_URL,
    "长视频": DEFAULT_XYQ_HOME_URL,
}


class CDPError(RuntimeError):
    pass


class CDPPage:
    def __init__(self, websocket_url: str, origin: str = DEFAULT_DEBUG_URL) -> None:
        self.ws = websocket.create_connection(websocket_url, timeout=20, origin=origin)
        self._id = 0
        self.call("Runtime.enable")

    def close(self) -> None:
        self.ws.close()

    def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == self._id:
                return message

    def js(self, expression: str, *, await_promise: bool = True) -> Any:
        response = self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": await_promise,
            },
        )
        result = response.get("result", {})
        if "exceptionDetails" in result:
            raise CDPError(json.dumps(result["exceptionDetails"], ensure_ascii=False, indent=2))
        return result.get("result", {}).get("value")

    def navigate(self, url: str, wait_seconds: float = 2.0) -> None:
        self.call("Page.enable")
        response = self.call("Page.navigate", {"url": url})
        if "error" in response:
            raise CDPError(json.dumps(response["error"], ensure_ascii=False, indent=2))
        time.sleep(wait_seconds)
        self.install_helpers()

    def install_helpers(self) -> None:
        self.js(
            r"""
window.__xyqCtl = (() => {
  const text = el => (el && (el.innerText || el.textContent || '')).trim();
  const visible = el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden';
  };
  const setNativeValue = (el, value) => {
    el.focus();
    if (el.isContentEditable) {
      el.textContent = value;
    } else {
      const proto = Object.getPrototypeOf(el);
      const desc = Object.getOwnPropertyDescriptor(proto, 'value');
      if (desc && desc.set) desc.set.call(el, value); else el.value = value;
    }
    el.dispatchEvent(new InputEvent('input', {bubbles:true, inputType:'insertText', data:value}));
    el.dispatchEvent(new Event('change', {bubbles:true}));
  };
  const editables = () => [...document.querySelectorAll('textarea,input,[contenteditable=true],[contenteditable=plaintext-only]')]
    .filter(visible)
    .map((el, i) => {
      const r = el.getBoundingClientRect();
      return {i, tag: el.tagName, role: el.getAttribute('role'), placeholder: el.getAttribute('placeholder'),
        aria: el.getAttribute('aria-label'), text: text(el).slice(0,120), value: (el.value || '').slice(0,120),
        x:r.x, y:r.y, w:r.width, h:r.height};
    });
  const editableElements = () => [...document.querySelectorAll('textarea,input,[contenteditable=true],[contenteditable=plaintext-only]')]
    .filter(visible);
  const composer = () => {
    const els = editableElements();
    if (!els.length) return null;
    return els.sort((a,b) => b.getBoundingClientRect().bottom - a.getBoundingClientRect().bottom)[0];
  };
  const fillPrompt = value => {
    const el = composer();
    if (!el) return {ok:false, reason:'no visible editable composer'};
    setNativeValue(el, value);
    const r = el.getBoundingClientRect();
    return {ok:true, tag:el.tagName, x:r.x, y:r.y, w:r.width, h:r.height};
  };
  const buttons = () => [...document.querySelectorAll('button,[role=button]')]
    .filter(visible)
    .map((el, i) => {
      const r = el.getBoundingClientRect();
      return {i, text:text(el).slice(0,80), disabled:!!el.disabled || el.getAttribute('aria-disabled') === 'true',
        x:r.x, y:r.y, w:r.width, h:r.height};
    });
  const externalLinks = () => [...document.querySelectorAll('svg.lucide-external-link')]
    .filter(visible)
    .map((el, i) => {
      const r = el.getBoundingClientRect();
      const parentText = text(el.closest('[role=button],button,div') || el).slice(0,160);
      return {i, parentText, x:r.x, y:r.y, w:r.width, h:r.height};
    });
  const clickExternalLink = index => {
    const links = [...document.querySelectorAll('svg.lucide-external-link')].filter(visible);
    const el = links[index || 0];
    if (!el) return {ok:false, reason:'external-link icon not found'};
    (el.closest('button,[role=button],div') || el).click();
    return {ok:true, index:index || 0};
  };
  const knownModes = ['Agent 模式', '短剧 Agent', '沉浸式短片', '智能长视频 2.0', '生成图片', '智能长视频'];
  const triggerModes = [...knownModes, '短片', '视频 2.0', '长视频 2.0', '长视频', '图片'];
  const dropdownItems = () => [...document.querySelectorAll('[class*="dropdownItem"]')]
    .filter(visible);
  const creationModes = () => dropdownItems().map((el, i) => {
    const r = el.getBoundingClientRect();
    const titleEl = el.querySelector('[class*="dropdownText"]') || el;
    const descEl = el.querySelector('[class*="dropdownDesc"]');
    return {i, title:text(titleEl), desc:text(descEl), selected:/Selected/.test(el.className),
      x:r.x, y:r.y, w:r.width, h:r.height};
  }).filter(item => knownModes.some(mode => item.title.includes(mode) || item.desc.includes(mode)));
  const openCreationModeDropdown = () => {
    const existing = creationModes();
    if (existing.length) return {ok:true, alreadyOpen:true, modes:existing};
    const toolbarCandidates = [...document.querySelectorAll('[class*="selectedTag"],[class*="toolbarLeft"],[class*="configButtons"]')]
      .filter(visible)
      .filter(el => {
        const t = text(el);
        const toolbar = el.closest('[class*="toolbar"],[class*="inputSection"],[class*="promptContainer"]');
        return toolbar && t.length < 160 && triggerModes.some(mode => t.includes(mode));
      })
      .sort((a,b) => {
        const ar = a.getBoundingClientRect(), br = b.getBoundingClientRect();
        return (ar.width * ar.height) - (br.width * br.height);
      });
    const candidates = toolbarCandidates.length ? toolbarCandidates : [...document.querySelectorAll('button,[role=button],div,span')]
      .filter(visible)
      .filter(el => {
        const t = text(el);
        const r = el.getBoundingClientRect();
        return r.x > 200 && r.y > 50 && t.length < 260
          && triggerModes.some(mode => t.includes(mode));
      })
      .sort((a,b) => {
        const ar = a.getBoundingClientRect(), br = b.getBoundingClientRect();
        return (ar.width * ar.height) - (br.width * br.height);
      });
    const el = candidates[0];
    if (!el) return {ok:false, reason:'mode dropdown trigger not found'};
    el.click();
    const r = el.getBoundingClientRect();
    return {ok:true, clicked:text(el).slice(0,120), x:r.x, y:r.y, w:r.width, h:r.height};
  };
  const selectCreationMode = async label => {
    const openResult = openCreationModeDropdown();
    await new Promise(resolve => setTimeout(resolve, 350));
    const items = dropdownItems();
    const item = items.find(el => text(el).includes(label));
    if (!item) return {ok:false, reason:'mode option not found', label, openResult, modes:creationModes()};
    item.click();
    await new Promise(resolve => setTimeout(resolve, 350));
    return {ok:true, label, openResult, modes:creationModes()};
  };
  const state = () => ({
    href: location.href,
    title: document.title,
    editables: editables(),
    buttons: buttons().slice(0,80),
    externalLinks: externalLinks(),
    creationModes: creationModes(),
    videoCount: document.querySelectorAll('video').length,
    imageCount: document.querySelectorAll('img').length,
  });
  return {state, fillPrompt, clickExternalLink, creationModes, openCreationModeDropdown, selectCreationMode};
})();
true
""",
        )

    def state(self) -> dict[str, Any]:
        self.install_helpers()
        return self.js("window.__xyqCtl.state()")

    def fill_prompt(self, prompt: str) -> dict[str, Any]:
        self.install_helpers()
        return self.js(f"window.__xyqCtl.fillPrompt({json.dumps(prompt, ensure_ascii=False)})")

    def click_external_link(self, index: int = 0) -> dict[str, Any]:
        self.install_helpers()
        return self.js(f"window.__xyqCtl.clickExternalLink({int(index)})")

    def list_creation_modes(self) -> list[dict[str, Any]]:
        self.install_helpers()
        return self.js("window.__xyqCtl.creationModes()")

    def open_creation_mode_dropdown(self) -> dict[str, Any]:
        self.install_helpers()
        return self.js("window.__xyqCtl.openCreationModeDropdown()")

    def select_creation_mode(self, label: str) -> dict[str, Any]:
        self.install_helpers()
        return self.js(f"window.__xyqCtl.selectCreationMode({json.dumps(label, ensure_ascii=False)})")


def browser_json(debug_url: str, path: str = "/json") -> Any:
    with urllib.request.urlopen(debug_url.rstrip("/") + path, timeout=10) as response:
        return json.load(response)


def new_tab(url: str, debug_url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe=":/?&=%")
    request = urllib.request.Request(debug_url.rstrip("/") + f"/json/new?{encoded}", method="PUT")
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def page_matches_url(page_url: str, desired_url: str) -> bool:
    current = urllib.parse.urlparse(page_url)
    desired = urllib.parse.urlparse(desired_url)
    if current.netloc != desired.netloc or current.path != desired.path:
        return False

    desired_query = urllib.parse.parse_qs(desired.query)
    if not desired_query:
        return True
    current_query = urllib.parse.parse_qs(current.query)
    return all(current_query.get(key) == value for key, value in desired_query.items())


def xyq_page_priority(page_url: str) -> int:
    parsed = urllib.parse.urlparse(page_url)
    query = urllib.parse.parse_qs(parsed.query)
    if parsed.path == "/home" and query.get("tab_name") == ["integrated-agent"]:
        return 0
    if parsed.path == "/home" and query.get("tab_name") == ["home"]:
        return 1
    if parsed.path == "/home":
        return 2
    if parsed.path == "/novel/list":
        return 3
    return 10


def attach_xyq_page(debug_url: str, url: str | None = None) -> CDPPage:
    pages = browser_json(debug_url, "/json")
    matches = [
        p
        for p in pages
        if p.get("type") == "page" and "xyq.jianying.com" in p.get("url", "")
    ]
    if url:
        exact_matches = [p for p in matches if page_matches_url(p.get("url", ""), url)]
        if exact_matches:
            matches = exact_matches
        else:
            new_tab(url, debug_url)
            time.sleep(2)
            pages = browser_json(debug_url, "/json")
            matches = [
                p
                for p in pages
                if p.get("type") == "page" and page_matches_url(p.get("url", ""), url)
            ]
    if not matches and url:
        new_tab(url, debug_url)
        time.sleep(2)
        pages = browser_json(debug_url, "/json")
        matches = [
            p
            for p in pages
            if p.get("type") == "page" and "xyq.jianying.com" in p.get("url", "")
        ]
    if not matches:
        raise CDPError("No Xiaoyunque page found. Launch Chrome with scripts/xyq_chrome/launch_chrome.sh first.")
    matches.sort(key=lambda p: xyq_page_priority(p.get("url", "")))
    page = CDPPage(matches[0]["webSocketDebuggerUrl"], origin=debug_url)
    page.install_helpers()
    return page


def main() -> int:
    parser = argparse.ArgumentParser(description="Attach to a debug-enabled 小云雀 Chrome page.")
    parser.add_argument("--debug-url", default=DEFAULT_DEBUG_URL)
    parser.add_argument("--url", default=DEFAULT_XYQ_URL, help="URL to open if no 小云雀 page exists")
    parser.add_argument("--state", action="store_true", help="Print page state")
    parser.add_argument("--fill-prompt", help="Fill the visible composer; does not submit")
    parser.add_argument("--fill-prompt-file", type=Path, help="Read prompt text from file and fill composer; does not submit")
    parser.add_argument("--click-external-link", type=int, help="Click an indexed lucide external-link icon")
    parser.add_argument("--list-modes", action="store_true", help="Open/read the creation-mode dropdown and list mode options")
    parser.add_argument("--select-mode", help="Select creation mode by label or alias, e.g. agent or duanpian")
    parser.add_argument("--eval", help="Evaluate custom JavaScript expression")
    args = parser.parse_args()

    page = attach_xyq_page(args.debug_url, args.url)
    try:
        if args.state:
            print(json.dumps(page.state(), ensure_ascii=False, indent=2))
        if args.fill_prompt_file:
            print(json.dumps(page.fill_prompt(args.fill_prompt_file.read_text(encoding="utf-8")), ensure_ascii=False, indent=2))
        if args.fill_prompt:
            print(json.dumps(page.fill_prompt(args.fill_prompt), ensure_ascii=False, indent=2))
        if args.click_external_link is not None:
            print(json.dumps(page.click_external_link(args.click_external_link), ensure_ascii=False, indent=2))
        if args.list_modes:
            page.open_creation_mode_dropdown()
            print(json.dumps(page.list_creation_modes(), ensure_ascii=False, indent=2))
        if args.select_mode:
            label = MODE_ALIASES.get(args.select_mode.strip().lower(), args.select_mode)
            print(json.dumps(page.select_creation_mode(label), ensure_ascii=False, indent=2))
        if args.eval:
            print(json.dumps(page.js(args.eval), ensure_ascii=False, indent=2))
        if not any([
            args.state,
            args.fill_prompt,
            args.fill_prompt_file,
            args.click_external_link is not None,
            args.list_modes,
            args.select_mode,
            args.eval,
        ]):
            print(json.dumps(page.state(), ensure_ascii=False, indent=2))
    finally:
        page.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
