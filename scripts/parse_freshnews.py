#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


SECTION_RE = re.compile(r"^##\s+(.+?)（(\d+)(条|个)）$")
ITEM_RE = re.compile(r"^###\s+\[(.+)\]\((.+)\)$")
TIME_RE = re.compile(r"^- 发布时间：(.+)$")


def parse_file(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()

    sections = []
    empty_sections = []
    current = None
    current_item = None
    in_empty_block = False
    in_errors = False

    def finish_item() -> None:
        nonlocal current_item, current
        if current is not None and current_item is not None:
            current["items"].append(current_item)
        current_item = None

    def finish_section() -> None:
        nonlocal current
        if current is not None:
            sections.append(current)
        current = None

    for raw_line in lines:
        line = raw_line.rstrip()

        if line == "## errors":
            finish_item()
            finish_section()
            in_errors = True
            in_empty_block = False
            continue

        if in_errors:
            continue

        if line.startswith("## 本次无更新的分组"):
            finish_item()
            finish_section()
            in_empty_block = True
            continue

        if in_empty_block:
            if line.startswith("- "):
                empty_sections.append(line[2:].strip())
            continue

        section_match = SECTION_RE.match(line)
        if section_match:
            finish_item()
            finish_section()
            current = {
                "name": section_match.group(1),
                "count": int(section_match.group(2)),
                "kind": section_match.group(3),
                "summary_line": "",
                "items": [],
            }
            continue

        if current is None:
            continue

        if line.startswith("> ") and current_item is None and not current["summary_line"]:
            current["summary_line"] = line[2:].strip()
            continue

        item_match = ITEM_RE.match(line)
        if item_match:
            finish_item()
            current_item = {
                "title": item_match.group(1).strip(),
                "url": item_match.group(2).strip(),
                "time": "",
                "quoted_text": "",
            }
            continue

        if current_item is None:
            continue

        if line.startswith("> "):
            quote_line = line[2:].strip()
            current_item["quoted_text"] = (
                quote_line
                if not current_item["quoted_text"]
                else f"{current_item['quoted_text']}\n{quote_line}"
            )
            continue

        time_match = TIME_RE.match(line)
        if time_match:
            current_item["time"] = time_match.group(1).strip()
            continue

    finish_item()
    finish_section()

    item_count = sum(len(section["items"]) for section in sections)
    return {
        "source_file": str(path),
        "sections": sections,
        "empty_sections": empty_sections,
        "stats": {
            "section_count": len(sections),
            "non_empty_section_count": sum(1 for section in sections if section["items"]),
            "empty_section_count": len(empty_sections),
            "item_count": item_count,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to a freshNews markdown file")
    args = parser.parse_args()

    path = Path(args.file).expanduser()
    payload = parse_file(path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
