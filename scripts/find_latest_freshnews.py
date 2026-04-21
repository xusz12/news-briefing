#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


# Pattern definitions
FRESHNESS_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}_freshNews\.md$")
DAILY_NEW_PATTERN = re.compile(r"^dailyFreshNews_(\d{4}-\d{2}-\d{2})\.md$")
DAILY_OLD_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})_dailyFreshNews\.md$")


def parse_daily_date(path: Path, pattern: re.Pattern) -> str | None:
    m = pattern.match(path.name)
    return m.group(1) if m else None


def find_latest(directory: Path, mode: str = "fresh") -> Path:
    if mode == "file":
        raise ValueError("use --file to specify a concrete path")

    candidates = []
    for path in directory.iterdir():
        if not path.is_file():
            continue
        if mode == "fresh":
            if FRESHNESS_PATTERN.match(path.name):
                candidates.append(path)
        elif mode == "daily":
            date = parse_daily_date(path, DAILY_NEW_PATTERN) or parse_daily_date(path, DAILY_OLD_PATTERN)
            if date:
                candidates.append((path, date))

    if not candidates:
        raise FileNotFoundError(f"no {mode} files found in: {directory}")

    if mode == "fresh":
        return sorted(candidates, key=lambda p: p.name)[-1]

    # mode == "daily": sort by date desc, then prefer new naming over old
    # candidates: list of (Path, date_str)
    by_date: dict[str, list[Path]] = {}
    for path, date in candidates:
        by_date.setdefault(date, []).append(path)

    latest_date = sorted(by_date.keys(), reverse=True)[0]
    daily_paths = by_date[latest_date]
    # prefer new naming
    for p in sorted(daily_paths, key=lambda x: x.name):
        if DAILY_NEW_PATTERN.match(p.name):
            return p
    return daily_paths[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="Directory containing freshNews or dailyFreshNews files")
    parser.add_argument(
        "--mode",
        default="fresh",
        choices=["fresh", "daily"],
        help="'fresh' finds latest YYYY-MM-DD-HH-mm_freshNews.md; 'daily' finds latest dailyFreshNews_YYYY-MM-DD.md (supports both old and new naming)",
    )
    parser.add_argument(
        "--file",
        help="If provided, use this specific file directly and skip finder",
    )
    args = parser.parse_args()

    if args.file:
        path = Path(args.file).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"file not found: {path}")
        payload = {
            "directory": str(path.parent),
            "file_name": path.name,
            "path": str(path),
            "mode": "file",
        }
    else:
        directory = Path(args.dir).expanduser()
        latest = find_latest(directory, args.mode)
        payload = {
            "directory": str(directory),
            "file_name": latest.name,
            "path": str(latest),
            "mode": args.mode,
        }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()