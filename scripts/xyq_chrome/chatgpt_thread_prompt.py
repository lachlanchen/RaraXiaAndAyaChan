#!/usr/bin/env python3
"""Send a prompt to an already-open ChatGPT thread and save the new answer.

This uses the same debug-enabled Chrome profile as the Xiaoyunque helpers.
It is intended for the LALACHAN "小云雀剧本" ChatGPT thread and does not use
the OpenAI API.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

import websocket


DEFAULT_DEBUG_URL = "http://127.0.0.1:9222"
DEFAULT_THREAD_URL = "https://chatgpt.com/c/69fc0bcd-4f2c-83ea-9117-46fc128a2496"


class CDPError(RuntimeError):
    pass


class CDPPage:
    def __init__(self, websocket_url: str, origin: str) -> None:
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
            {"expression": expression, "returnByValue": True, "awaitPromise": await_promise},
        )
        result = response.get("result", {})
        if "exceptionDetails" in result:
            raise CDPError(json.dumps(result["exceptionDetails"], ensure_ascii=False, indent=2))
        return result.get("result", {}).get("value")


def browser_json(debug_url: str, path: str = "/json") -> Any:
    with urllib.request.urlopen(debug_url.rstrip("/") + path, timeout=10) as response:
        return json.load(response)


def attach_chatgpt_page(debug_url: str, thread_url: str) -> CDPPage:
    pages = browser_json(debug_url)
    matches = [
        page
        for page in pages
        if page.get("type") == "page" and page.get("url", "").startswith(thread_url)
    ]
    if not matches:
        matches = [
            page
            for page in pages
            if page.get("type") == "page" and "chatgpt.com" in page.get("url", "")
        ]
    if not matches:
        raise CDPError("No ChatGPT page found in the debug-enabled Chrome profile.")
    return CDPPage(matches[0]["webSocketDebuggerUrl"], origin=debug_url)


def thread_state(page: CDPPage) -> dict[str, Any]:
    return page.js(
        r"""
(() => {
  const text = el => (el && (el.innerText || el.textContent || '')).trim();
  const messages = [...document.querySelectorAll('[data-message-author-role]')].map((el, i) => ({
    i,
    role: el.getAttribute('data-message-author-role'),
    text: text(el),
  }));
  const buttons = [...document.querySelectorAll('button,[role=button]')].map(el => ({
    text: text(el),
    aria: el.getAttribute('aria-label'),
    disabled: !!el.disabled || el.getAttribute('aria-disabled') === 'true',
  }));
  return {
    href: location.href,
    title: document.title,
    assistantCount: messages.filter(m => m.role === 'assistant').length,
    userCount: messages.filter(m => m.role === 'user').length,
    lastAssistant: [...messages].reverse().find(m => m.role === 'assistant') || null,
    lastUser: [...messages].reverse().find(m => m.role === 'user') || null,
    generating: buttons.some(b => /stop/i.test(b.aria || '') || /停止|Stop/i.test(b.text || '')),
    hasSendButton: buttons.some(b => /send/i.test(b.aria || '') || /发送/.test(b.text || '')),
  };
})()
""",
    )


def send_prompt(page: CDPPage, prompt: str) -> dict[str, Any]:
    result = page.js(
        f"""
(async () => {{
  const prompt = {json.dumps(prompt, ensure_ascii=False)};
  const visible = el => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden';
  }};
  const composer = [...document.querySelectorAll('div[role="textbox"][contenteditable="true"], [contenteditable="true"][aria-label*="Chat"], textarea')]
    .filter(visible)
    .sort((a,b) => b.getBoundingClientRect().bottom - a.getBoundingClientRect().bottom)[0];
  if (!composer) return {{ok:false, reason:'composer not found'}};
  composer.focus();
  if (composer.tagName === 'TEXTAREA') {{
    composer.value = prompt;
  }} else {{
    composer.textContent = '';
    const p = document.createElement('p');
    p.textContent = prompt;
    composer.appendChild(p);
  }}
  composer.dispatchEvent(new InputEvent('input', {{bubbles:true, inputType:'insertText', data:prompt.slice(0,32)}}));
  composer.dispatchEvent(new Event('change', {{bubbles:true}}));
  await new Promise(resolve => setTimeout(resolve, 500));
  const buttons = [...document.querySelectorAll('button')].filter(visible);
  const sendButton = buttons.find(el => /send/i.test(el.getAttribute('aria-label') || '') || el.dataset?.testid === 'send-button');
  if (sendButton && !sendButton.disabled && sendButton.getAttribute('aria-disabled') !== 'true') {{
    sendButton.click();
    return {{ok:true, method:'button'}};
  }}
  composer.dispatchEvent(new KeyboardEvent('keydown', {{key:'Enter', code:'Enter', bubbles:true, cancelable:true}}));
  composer.dispatchEvent(new KeyboardEvent('keyup', {{key:'Enter', code:'Enter', bubbles:true, cancelable:true}}));
  return {{ok:true, method:'keyboard'}};
}})()
""",
    )
    if not result.get("ok"):
        raise CDPError(json.dumps(result, ensure_ascii=False))
    return result


def wait_for_answer(page: CDPPage, before_assistant_count: int, timeout_seconds: int) -> dict[str, Any]:
    deadline = time.time() + timeout_seconds
    last_text = ""
    stable_count = 0
    latest: dict[str, Any] = {}
    while time.time() < deadline:
        latest = thread_state(page)
        last = latest.get("lastAssistant") or {}
        text = last.get("text") or ""
        has_new = latest.get("assistantCount", 0) > before_assistant_count
        if has_new and text and not latest.get("generating"):
            if text == last_text:
                stable_count += 1
            else:
                stable_count = 0
                last_text = text
            if stable_count >= 2:
                return latest
        time.sleep(3)
    raise CDPError(f"Timed out waiting for ChatGPT answer. Last state: {json.dumps(latest, ensure_ascii=False)[:1000]}")


def markdown_output(thread_url: str, prompt: str, answer: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""# ChatGPT Today Script

Saved: `{timestamp}`

Source thread:

```text
{thread_url}
```

## Prompt Sent

```text
{prompt}
```

## ChatGPT Answer

{answer.strip()}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a prompt to a ChatGPT browser thread and save the new answer.")
    parser.add_argument("--debug-url", default=DEFAULT_DEBUG_URL)
    parser.add_argument("--thread-url", default=DEFAULT_THREAD_URL)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=240)
    args = parser.parse_args()

    prompt = args.prompt_file.read_text(encoding="utf-8")
    page = attach_chatgpt_page(args.debug_url, args.thread_url)
    try:
        before = thread_state(page)
        send_result = send_prompt(page, prompt)
        after = wait_for_answer(page, before.get("assistantCount", 0), args.timeout_seconds)
        answer = (after.get("lastAssistant") or {}).get("text") or ""
    finally:
        page.close()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown_output(args.thread_url, prompt, answer), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "sent": send_result, "answer_chars": len(answer)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
