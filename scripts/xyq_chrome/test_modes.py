#!/usr/bin/env python3
"""Non-destructive Xiaoyunque mode smoke test.

This script attaches to the debug-enabled Chrome profile, selects Xiaoyunque
creation modes, records visible composer evidence, and never submits prompts.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from xyq_cdp import (
    DEFAULT_DEBUG_URL,
    DEFAULT_XYQ_DUANJU_URL,
    DEFAULT_XYQ_HOME_URL,
    attach_xyq_page,
)


def composer_summary(page: Any) -> dict[str, Any]:
    return page.js(
        r"""
(() => {
  const text = el => (el && (el.innerText || el.textContent || '')).trim();
  const visible = el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden';
  };
  const composerTexts = [...document.querySelectorAll(
    '[class*="promptContainer"],[class*="toolbar"],[class*="configButtons"],[class*="creditTip"]'
  )].filter(visible).map(text).filter(Boolean).slice(0, 8);
  const buttons = [...document.querySelectorAll('button,[role=button]')]
    .filter(visible)
    .map(el => text(el).replace(/\s+/g, ' ').slice(0, 80))
    .filter(Boolean)
    .slice(0, 20);
  return {
    href: location.href,
    title: document.title,
    composerTexts,
    buttons,
    hasEditable: [...document.querySelectorAll('textarea,input,[contenteditable=true],[contenteditable=plaintext-only]')]
      .filter(visible).length > 0,
  };
})()
""",
    )


def set_short_duration(page: Any, label: str = "15s") -> dict[str, Any]:
    return page.js(
        rf"""
(async () => {{
  const text = el => (el && (el.innerText || el.textContent || '')).trim();
  const visible = el => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && s.display !== 'none' && s.visibility !== 'hidden';
  }};
  const durationButton = [...document.querySelectorAll('button')]
    .filter(visible)
    .find(el => /^\d+s$/.test(text(el)));
  if (!durationButton) return {{ok:false, reason:'duration button not found'}};
  durationButton.click();
  await new Promise(resolve => setTimeout(resolve, 250));
  const option = [...document.querySelectorAll('.lv-dropdown-menu-item,[class*="videoPartDurationItem"],div')]
    .filter(visible)
    .find(el => text(el) === {json.dumps(label)});
  if (!option) return {{ok:false, reason:'duration option not found', label:{json.dumps(label)}}};
  option.click();
  await new Promise(resolve => setTimeout(resolve, 250));
  return {{ok:true, label:{json.dumps(label)}}};
}})()
""",
    )


def record_mode(page: Any, label: str) -> dict[str, Any]:
    result = page.select_creation_mode(label)
    time.sleep(0.4)
    summary = composer_summary(page)
    ok = bool(result.get("ok")) or any(label in item for item in summary.get("composerTexts", []))
    return {"mode": label, "ok": ok, "selectResult": result, "summary": summary}


def test_modes(debug_url: str) -> list[dict[str, Any]]:
    home_page = attach_xyq_page(debug_url, DEFAULT_XYQ_HOME_URL)
    try:
        results = [
            record_mode(home_page, "Agent 模式"),
            record_mode(home_page, "沉浸式短片"),
        ]
        duration_result = set_short_duration(home_page, "15s")
        results[-1]["durationResult"] = duration_result
        results[-1]["summaryAfterDuration"] = composer_summary(home_page)
        results.append(record_mode(home_page, "智能长视频 2.0"))
    finally:
        home_page.close()

    duanju_page = attach_xyq_page(debug_url, DEFAULT_XYQ_DUANJU_URL)
    try:
        summary = composer_summary(duanju_page)
        evidence = "\n".join(summary.get("buttons", []))
        results.append(
            {
                "mode": "短剧 Agent",
                "ok": "上传我的剧本" in evidence and "AI 生成剧本" in evidence,
                "selectResult": {"ok": True, "url": DEFAULT_XYQ_DUANJU_URL, "directTab": True},
                "summary": summary,
            }
        )
    finally:
        duanju_page.close()

    return results


def markdown_report(results: list[dict[str, Any]]) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Xiaoyunque Mode Smoke Test",
        "",
        f"Generated: `{generated}`",
        "",
        "Scope: non-destructive browser test through the controlled Chrome driver. No prompt was submitted and no video generation was started.",
        "",
        "| Mode | Result | Evidence |",
        "| --- | --- | --- |",
    ]
    for item in results:
        summary = item.get("summaryAfterDuration") or item.get("summary") or {}
        evidence = " / ".join(summary.get("composerTexts") or summary.get("buttons") or [])
        evidence = evidence.replace("\n", " ").replace("|", "\\|")[:220]
        lines.append(f"| {item['mode']} | {'PASS' if item.get('ok') else 'CHECK'} | {evidence} |")

    lines.extend(
        [
            "",
            "## Mode Defaults",
            "",
            "- `Agent 模式`: default mode when the user does not ask for a specific mode; use for longer Agent-driven videos.",
            "- `沉浸式短片`: default short-video mode; set duration to `15s` before submission.",
            "- `智能长视频 2.0`: selectable from the home composer dropdown; use only when explicitly requested or when long-video multi-shot planning is needed.",
            "- `短剧 Agent`: use the dedicated tab directly: `https://xyq.jianying.com/novel/list?enter_from=small_tool`.",
            "",
            "## Re-run",
            "",
            "```bash",
            "scripts/xyq_chrome/test_modes.py --output references/xyq-mode-test-results.md",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test Xiaoyunque mode selection without submitting.")
    parser.add_argument("--debug-url", default=DEFAULT_DEBUG_URL)
    parser.add_argument("--output", type=Path, help="Optional Markdown report path")
    parser.add_argument("--json-output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()

    results = test_modes(args.debug_url)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    report = markdown_report(results)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0 if all(item.get("ok") for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
