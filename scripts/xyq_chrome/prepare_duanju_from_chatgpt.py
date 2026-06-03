#!/usr/bin/env python3
"""Prepare Xiaoyunque 短剧 Agent from the saved ChatGPT draft.

The script opens the dedicated short-drama Agent workspace, uploads the Trio
character image through the Xiaoyunque skill API, and optionally pastes the
local draft text into the page. It does not submit generation.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from xyq_cdp import DEFAULT_DEBUG_URL, DEFAULT_XYQ_DUANJU_URL, attach_xyq_page


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHATGPT_URL = "https://chatgpt.com/c/69fc0bcd-4f2c-83ea-9117-46fc128a2496"
DEFAULT_DRAFT = REPO_ROOT / "Lala-Aya-Sasa-draft/duanju-agent-chatgpt-sushi.md"
DEFAULT_SCRIPT_UPLOAD_FILE = REPO_ROOT / "Lala-Aya-Sasa-draft/duanju-agent-chatgpt-sushi.txt"
DEFAULT_TRIO_IMAGE = REPO_ROOT / "Trio.png"
DEFAULT_DOTENV = REPO_ROOT / ".env"
DEFAULT_SKILL_SCRIPTS = Path("/home/lachlan/.agents/skills/xyq-nest-skill/scripts")
DEFAULT_LOG = REPO_ROOT / "outputs/xyq-duanju-agent-chatgpt-prepare.json"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def import_upload_file(skill_scripts: Path):
    sys.path.insert(0, str(skill_scripts))
    from upload_file import upload_file  # type: ignore

    return upload_file


def upload_trio_image(path: Path, *, skill_scripts: Path) -> dict[str, str]:
    upload_file = import_upload_file(skill_scripts)
    data = upload_file(str(path))
    asset_id = data.get("pippit_asset_id") or data.get("asset_id")
    if not asset_id:
        raise RuntimeError(f"upload_file returned no asset id for {path}: {data}")
    return {"path": str(path), "asset_id": asset_id}


def upload_script_file_to_duanju_page(
    script_file: Path,
    *,
    debug_url: str,
    duanju_url: str,
) -> dict[str, Any]:
    page = attach_xyq_page(debug_url, duanju_url)
    try:
        page.navigate(duanju_url, wait_seconds=1.5)
        click_result = page.js(
            r"""
(() => {
  const text = el => (el && (el.innerText || el.textContent || '')).trim();
  const visible = el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden';
  };
  const uploadButton = [...document.querySelectorAll('button,[role=button]')]
    .filter(visible)
    .find(el => text(el).replace(/\s+/g, ' ') === '上传我的剧本');
  if (uploadButton) uploadButton.click();
  const input = document.querySelector('input[type="file"][accept*=".txt"], input[type="file"]');
  return {
    ok: !!input,
    clickedUpload: !!uploadButton,
    inputAccept: input ? input.getAttribute('accept') : null,
    href: location.href,
  };
})()
""",
        )
        if not click_result.get("ok"):
            return {**click_result, "reason": "file input not found"}

        document = page.call("DOM.getDocument")
        root_id = document["result"]["root"]["nodeId"]
        node = page.call(
            "DOM.querySelector",
            {"nodeId": root_id, "selector": 'input[type="file"][accept*=".txt"], input[type="file"]'},
        )
        node_id = node.get("result", {}).get("nodeId")
        if not node_id:
            return {**click_result, "ok": False, "reason": "file input node id not found"}

        response = page.call(
            "DOM.setFileInputFiles",
            {"nodeId": node_id, "files": [str(script_file.resolve())]},
        )
        if "error" in response:
            return {**click_result, "ok": False, "reason": response["error"]}
        summary: dict[str, Any] = {}
        for _ in range(10):
            time.sleep(0.5)
            summary = page.js(
                rf"""
(() => {{
  const body = document.body.innerText || '';
  const buttons = [...document.querySelectorAll('button,[role=button]')]
    .map(el => (el.innerText || el.textContent || '').trim())
    .filter(Boolean)
    .slice(0, 25);
  return {{
    ok:true,
    href:location.href,
    fileName:{json.dumps(script_file.name)},
    bodyMentionsFile:body.includes({json.dumps(script_file.name)}),
    hasParseButton:buttons.some(text => text.includes('剧本解析')),
    buttons
  }};
}})()
""",
            )
            if summary.get("hasParseButton"):
                break
        return {**click_result, **summary, "uploadedFile": str(script_file)}
    finally:
        page.close()


def paste_draft_into_duanju_page(
    draft_text: str,
    *,
    debug_url: str,
    duanju_url: str,
) -> dict[str, Any]:
    page = attach_xyq_page(debug_url, duanju_url)
    try:
        page.navigate(duanju_url, wait_seconds=1.5)
        result = page.js(
            rf"""
(async () => {{
  const draft = {json.dumps(draft_text, ensure_ascii=False)};
  const text = el => (el && (el.innerText || el.textContent || '')).trim();
  const visible = el => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden';
  }};
  const setNativeValue = (el, value) => {{
    el.focus();
    if (el.isContentEditable) {{
      el.textContent = value;
    }} else {{
      const proto = Object.getPrototypeOf(el);
      const desc = Object.getOwnPropertyDescriptor(proto, 'value');
      if (desc && desc.set) desc.set.call(el, value); else el.value = value;
    }}
    el.dispatchEvent(new InputEvent('input', {{bubbles:true, inputType:'insertText', data:value.slice(0, 32)}}));
    el.dispatchEvent(new Event('change', {{bubbles:true}}));
  }};
  const clickByText = label => {{
    const candidates = [...document.querySelectorAll('button,[role=button]')]
      .filter(visible)
      .filter(el => text(el).replace(/\s+/g, ' ').includes(label))
      .sort((a,b) => {{
        const at = text(a).replace(/\s+/g, ' ');
        const bt = text(b).replace(/\s+/g, ' ');
        const ar = a.getBoundingClientRect(), br = b.getBoundingClientRect();
        const exactA = at === label ? 0 : 1;
        const exactB = bt === label ? 0 : 1;
        return exactA - exactB || (ar.width * ar.height) - (br.width * br.height);
      }});
    const el = candidates[0];
    if (!el) return null;
    el.click();
    return {{text:text(el).slice(0, 80), tag:el.tagName}};
  }};
  const clickedPaste = clickByText('粘贴文本') || clickByText('上传我的剧本');
  await new Promise(resolve => setTimeout(resolve, 700));
  const editables = [...document.querySelectorAll('textarea,input,[contenteditable=true],[contenteditable=plaintext-only]')]
    .filter(visible)
    .sort((a,b) => {{
      const ar = a.getBoundingClientRect(), br = b.getBoundingClientRect();
      return (br.width * br.height) - (ar.width * ar.height);
    }});
  if (!editables.length) {{
    return {{
      ok:false,
      reason:'no visible editor after opening paste/upload controls',
      clickedPaste,
      href:location.href,
      buttons:[...document.querySelectorAll('button,[role=button]')].filter(visible).map(el => text(el).slice(0,80)).slice(0,30)
    }};
  }}
  const editor = editables[0];
  setNativeValue(editor, draft);
  await new Promise(resolve => setTimeout(resolve, 250));
  const r = editor.getBoundingClientRect();
  return {{
    ok:true,
    clickedPaste,
    href:location.href,
    editor:{{tag:editor.tagName, x:r.x, y:r.y, w:r.width, h:r.height}},
    pastedChars:draft.length
  }};
}})()
""",
        )
        return result
    finally:
        page.close()


def write_log(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def browser_action_ok(result: dict[str, Any] | None) -> bool:
    if result is None:
        return True
    if "ok" in result:
        return bool(result["ok"])
    return all(bool(value.get("ok")) for value in result.values() if isinstance(value, dict))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare Xiaoyunque short-drama Agent with the saved ChatGPT draft and Trio reference image.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--chatgpt-url", default=DEFAULT_CHATGPT_URL)
    parser.add_argument("--duanju-url", default=DEFAULT_XYQ_DUANJU_URL)
    parser.add_argument("--draft", type=Path, default=DEFAULT_DRAFT)
    parser.add_argument("--script-upload-file", type=Path, default=DEFAULT_SCRIPT_UPLOAD_FILE)
    parser.add_argument("--trio-image", type=Path, default=DEFAULT_TRIO_IMAGE)
    parser.add_argument("--dotenv", type=Path, default=DEFAULT_DOTENV)
    parser.add_argument("--skill-scripts", type=Path, default=DEFAULT_SKILL_SCRIPTS)
    parser.add_argument("--debug-url", default=DEFAULT_DEBUG_URL)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--trio-asset-id", default="", help="Reuse an existing uploaded Trio asset id")
    parser.add_argument("--force-upload-trio", action="store_true", help="Upload Trio even if an asset id is available")
    parser.add_argument("--no-upload-trio", action="store_true", help="Skip Xiaoyunque Trio asset upload")
    parser.add_argument(
        "--browser-action",
        choices=("upload", "paste", "both", "none"),
        default="upload",
        help="How to prepare the short-drama page; never submits generation",
    )
    args = parser.parse_args()

    if not args.draft.exists():
        parser.error(f"draft file does not exist: {args.draft}")
    if args.browser_action in {"upload", "both"} and not args.script_upload_file.exists():
        parser.error(f"script upload file does not exist: {args.script_upload_file}")
    if not args.trio_image.exists():
        parser.error(f"Trio image does not exist: {args.trio_image}")

    load_dotenv(args.dotenv)
    draft_text = args.draft.read_text(encoding="utf-8")

    upload_result: dict[str, str] | None = None
    existing_asset_id = args.trio_asset_id or os.environ.get("XYQ_TRIO_ASSET_ID", "")
    if args.no_upload_trio:
        upload_result = None
    elif existing_asset_id and not args.force_upload_trio:
        upload_result = {"path": str(args.trio_image), "asset_id": existing_asset_id, "source": "existing"}
    else:
        upload_result = upload_trio_image(args.trio_image, skill_scripts=args.skill_scripts)

    browser_result: dict[str, Any] | None = None
    if args.browser_action == "upload":
        browser_result = upload_script_file_to_duanju_page(
            args.script_upload_file,
            debug_url=args.debug_url,
            duanju_url=args.duanju_url,
        )
    elif args.browser_action == "paste":
        browser_result = paste_draft_into_duanju_page(
            draft_text,
            debug_url=args.debug_url,
            duanju_url=args.duanju_url,
        )
    elif args.browser_action == "both":
        browser_result = {
            "upload": upload_script_file_to_duanju_page(
                args.script_upload_file,
                debug_url=args.debug_url,
                duanju_url=args.duanju_url,
            ),
            "paste": paste_draft_into_duanju_page(
                draft_text,
                debug_url=args.debug_url,
                duanju_url=args.duanju_url,
            ),
        }

    payload = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "chatgpt_url": args.chatgpt_url,
        "duanju_url": args.duanju_url,
        "draft": str(args.draft),
        "script_upload_file": str(args.script_upload_file),
        "default_character_image": str(args.trio_image),
        "trio_upload": upload_result,
        "browser_fill": browser_result,
        "submitted_generation": False,
    }
    write_log(args.log, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if browser_action_ok(browser_result) else 2


if __name__ == "__main__":
    raise SystemExit(main())
