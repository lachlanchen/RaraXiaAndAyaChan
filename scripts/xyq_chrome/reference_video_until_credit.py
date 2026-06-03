#!/usr/bin/env python3
"""Submit a Xiaoyunque reference-video job and poll until it blocks or finishes.

This wraps the installed xyq-nest-skill scripts while optionally filling the
logged-in Chrome composer through scripts/xyq_chrome/xyq_cdp.py so the browser
stays aligned with the API run.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SKILL_SCRIPTS = Path("/home/lachlan/.agents/skills/xyq-nest-skill/scripts")
DEFAULT_PROMPT = "请参考这个视频，生成一个同风格的新视频。"
DEFAULT_CONFIRM = "确认，请继续生成视频。"
DEFAULT_REFERENCE_IMAGES = [
    REPO_ROOT / "display.png",
    REPO_ROOT / "patchwork-leather-notebook-luxury-clean-v2.png",
    REPO_ROOT / "Trio.png",
]
CREDIT_MARKERS = ("insufficient_credit", "credit", "credits", "积分不足", "积分不够", "额度不足", "余额不足")


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def import_xyq_modules(skill_scripts: Path):
    sys.path.insert(0, str(skill_scripts))
    from upload_file import upload_file  # type: ignore
    from _common import GET_THREAD_PATH, api_post, parse_response, submit_run  # type: ignore

    return upload_file, submit_run, api_post, parse_response, GET_THREAD_PATH


def cdp_fill(text: str, *, enabled: bool, cdp_script: Path) -> None:
    if not enabled:
        return
    try:
        subprocess.run(
            [str(cdp_script), "--fill-prompt", text],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
    except Exception as exc:
        print(f"warning: browser fill failed: {exc}", file=sys.stderr)


def get_run(api_post, parse_response, get_thread_path: str, thread_id: str, run_id: str) -> dict[str, Any]:
    body: dict[str, Any] = {"thread_id": thread_id, "after_seq": 0}
    if run_id:
        body["run_id"] = run_id
    response = parse_response(api_post(get_thread_path, body))
    runs = response.get("thread", {}).get("run_list") or []
    if not runs:
        raise RuntimeError("Xiaoyunque returned no run_list")
    for run in runs:
        if run.get("run_id") == run_id:
            return run
    return runs[0]


def json_data(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except Exception:
        return value


def summarize_run(run: dict[str, Any]) -> dict[str, Any]:
    texts: list[str] = []
    tools: list[str] = []
    errors: list[dict[str, Any]] = []
    urls: list[str] = []
    raw_credit_hits: list[str] = []

    for entry in run.get("entry_list") or []:
        item = entry.get("message") or entry.get("artifact") or {}
        for content in item.get("content") or []:
            raw = json.dumps(content, ensure_ascii=False)
            lower_raw = raw.lower()
            if any(marker in lower_raw for marker in CREDIT_MARKERS) or any(marker in raw for marker in CREDIT_MARKERS):
                raw_credit_hits.append(raw[:1200])

            data = json_data(content.get("data"))
            content_type = content.get("type")
            sub_type = content.get("sub_type")

            if content_type == "text" and isinstance(data, str):
                texts.append(data.strip())
            elif sub_type == "biz/x_data_intermediate_message" and isinstance(data, dict):
                message = data.get("message") or data.get("loading_text")
                if message:
                    texts.append(str(message).strip())
            elif sub_type == "tool_call_req" and isinstance(data, dict):
                tool = data.get("tool_name")
                if tool:
                    tools.append(str(tool))
            elif sub_type == "biz/error":
                errors.append(data if isinstance(data, dict) else {"raw": data})

            if isinstance(data, str) and "http" in data:
                urls.append(data)
            elif isinstance(data, dict):
                encoded = json.dumps(data, ensure_ascii=False)
                if "http" in encoded:
                    urls.append(encoded)

    return {
        "state": run.get("state"),
        "fail_reason": run.get("fail_reason"),
        "texts": texts,
        "tools": tools,
        "errors": errors,
        "credit_hits": raw_credit_hits,
        "urls": urls,
    }


def needs_confirmation(summary: dict[str, Any]) -> bool:
    text = "\n".join(summary["texts"])
    return "请确认" in text and ("继续" in text or "生成视频" in text)


def has_credit_block(summary: dict[str, Any]) -> bool:
    combined = json.dumps(summary, ensure_ascii=False).lower()
    return any(marker in combined for marker in CREDIT_MARKERS)


def print_summary(label: str, summary: dict[str, Any]) -> None:
    print(f"\n[{label}] state={summary['state']} fail_reason={summary.get('fail_reason')}")
    for text in summary["texts"][-8:]:
        print(f"- {text[:300]}")
    for tool in summary["tools"][-5:]:
        print(f"- tool: {tool}")
    for error in summary["errors"][-3:]:
        print(f"- error: {json.dumps(error, ensure_ascii=False)[:500]}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload a reference video, submit it to Xiaoyunque, auto-confirm once, and stop on credit block.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--video", type=Path, required=True, help="Reference video path")
    parser.add_argument("--reference-file", type=Path, action="append", default=[], help="Extra image/video reference file; can be repeated")
    parser.add_argument(
        "--include-default-images",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Also upload LightMind glasses image, patchwork leather notebook image, and Trio.png",
    )
    parser.add_argument("--thread-id", default="", help="Existing Xiaoyunque thread id")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--confirm-prompt", default=DEFAULT_CONFIRM)
    parser.add_argument("--poll-seconds", type=float, default=10.0)
    parser.add_argument("--max-polls", type=int, default=120)
    parser.add_argument("--auto-confirm", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--browser-fill", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dotenv", type=Path, default=REPO_ROOT / ".env")
    parser.add_argument("--skill-scripts", type=Path, default=DEFAULT_SKILL_SCRIPTS)
    parser.add_argument("--cdp-script", type=Path, default=REPO_ROOT / "scripts/xyq_chrome/xyq_cdp.py")
    parser.add_argument("--json-log", type=Path, help="Optional run log path without secrets")
    args = parser.parse_args()

    reference_files = [args.video]
    if args.include_default_images:
        reference_files.extend(DEFAULT_REFERENCE_IMAGES)
    reference_files.extend(args.reference_file)

    missing = [str(path) for path in reference_files if not path.exists()]
    if missing:
        parser.error(f"reference file(s) do not exist: {missing}")

    load_dotenv(args.dotenv)
    upload_file, submit_run, api_post, parse_response, get_thread_path = import_xyq_modules(args.skill_scripts)

    events: list[dict[str, Any]] = []

    asset_ids: list[str] = []
    for path in reference_files:
        print(f"Uploading reference file: {path}")
        asset_data = upload_file(str(path))
        asset_id = asset_data.get("pippit_asset_id")
        if not asset_id:
            raise RuntimeError(f"upload did not return pippit_asset_id for {path}: {asset_data}")
        asset_ids.append(asset_id)
        print(f"asset_id={asset_id}")

    cdp_fill(args.prompt, enabled=args.browser_fill, cdp_script=args.cdp_script)
    run_data = submit_run(thread_id=args.thread_id, message=args.prompt, asset_ids=asset_ids)
    run = run_data.get("run", {})
    thread_id = run.get("thread_id")
    run_id = run.get("run_id")
    web_thread_link = run_data.get("web_thread_link")
    print(json.dumps({"thread_id": thread_id, "run_id": run_id, "web_thread_link": web_thread_link}, ensure_ascii=False, indent=2))
    events.append({
        "event": "submitted",
        "asset_ids": asset_ids,
        "reference_files": [str(path) for path in reference_files],
        "thread_id": thread_id,
        "run_id": run_id,
        "web_thread_link": web_thread_link,
    })

    confirmed = False
    active_run_id = run_id

    for poll in range(1, args.max_polls + 1):
        time.sleep(args.poll_seconds)
        active_run = get_run(api_post, parse_response, get_thread_path, thread_id, active_run_id)
        summary = summarize_run(active_run)
        events.append({"event": "poll", "poll": poll, "run_id": active_run_id, "summary": summary})
        print_summary(f"poll {poll}", summary)

        if has_credit_block(summary):
            print("\nStopped: Xiaoyunque reported an insufficient-credit block.")
            break

        if summary["state"] == 3 and args.auto_confirm and not confirmed and needs_confirmation(summary):
            print("\nConfirmation requested; submitting continuation prompt.")
            cdp_fill(args.confirm_prompt, enabled=args.browser_fill, cdp_script=args.cdp_script)
            next_run_data = submit_run(thread_id=thread_id, message=args.confirm_prompt, asset_ids=None)
            next_run = next_run_data.get("run", {})
            active_run_id = next_run.get("run_id")
            confirmed = True
            events.append({"event": "confirmed", "run_id": active_run_id, "message": args.confirm_prompt})
            continue

        if summary["state"] in (3, 4, 5):
            print("\nStopped: run reached terminal state.")
            break
    else:
        print("\nStopped: max polls reached.")

    if args.json_log:
        args.json_log.parent.mkdir(parents=True, exist_ok=True)
        args.json_log.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote log: {args.json_log}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
