#!/usr/bin/env python3
"""Validate the lightweight LALACHAN story database."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "references" / "story-database"
STORIES = DB / "stories.csv"
SOURCES = DB / "source-references.csv"


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"}


def local_path_exists(value: str) -> bool:
    if not value:
        return True
    if is_url(value):
        return True
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path.exists()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not STORIES.exists():
        errors.append(f"missing {STORIES.relative_to(ROOT)}")
    if not SOURCES.exists():
        errors.append(f"missing {SOURCES.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    sources = read_csv(SOURCES)
    stories = read_csv(STORIES)
    source_ids = {row["reference_id"] for row in sources}

    for row in sources:
        ref_id = row.get("reference_id", "")
        target = row.get("path_or_url", "")
        if not ref_id:
            errors.append("source row with empty reference_id")
        if not target:
            errors.append(f"source {ref_id} has empty path_or_url")
        elif not local_path_exists(target):
            errors.append(f"source {ref_id} missing target: {target}")

    story_ids: set[str] = set()
    for row in stories:
        story_id = row.get("story_id", "")
        if not story_id:
            errors.append("story row with empty story_id")
            continue
        if story_id in story_ids:
            errors.append(f"duplicate story_id: {story_id}")
        story_ids.add(story_id)

        for field in ("story_path", "prompt_path"):
            value = row.get(field, "")
            if value and not local_path_exists(value):
                errors.append(f"story {story_id} missing {field}: {value}")

        video_path = row.get("video_path", "")
        if video_path and not local_path_exists(video_path):
            warnings.append(f"story {story_id} missing optional video_path: {video_path}")

        for ref_id in filter(None, row.get("reference_ids", "").split(";")):
            if ref_id not in source_ids:
                errors.append(f"story {story_id} references unknown source: {ref_id}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARN: {warning}")
        print(f"Checked {len(stories)} stories and {len(sources)} references.")
        return 1

    for warning in warnings:
        print(f"WARN: {warning}")
    print(f"OK: checked {len(stories)} stories and {len(sources)} references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
