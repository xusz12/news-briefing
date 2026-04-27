#!/usr/bin/env python3
import argparse
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_OUTPUT_FILE = Path(
    "/Users/x/Library/Mobile Documents/iCloud~md~obsidian/Documents/Mind/NewsOfCodex/news_briefing/NewsBriefing.md"
)
LOCAL_TIMEZONE = "Asia/Shanghai"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-file",
        help="Optional override path for testing. Defaults to the fixed NewsBriefing.md output path.",
    )
    args = parser.parse_args()

    content = sys.stdin.read()
    output_file = Path(args.output_file).expanduser() if args.output_file else DEFAULT_OUTPUT_FILE
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output_file.parent, delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    tmp_path.replace(output_file)

    payload = {
        "output_path": str(output_file),
        "bytes_written": len(content.encode("utf-8")),
        "updated_at": datetime.now(ZoneInfo(LOCAL_TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
