#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def index_by_id(matches):
    m = {}
    for i, obj in enumerate(matches):
        if isinstance(obj, dict) and "ID" in obj:
            try:
                mid = int(obj["ID"])
            except Exception:
                continue
            m[mid] = (i, obj)
    return m

def main():
    if len(sys.argv) != 4:
        print("usage: splice_match.py <match_id> <main_json_path> <pr_json_path>", file=sys.stderr)
        return 2

    match_id = int(sys.argv[1])
    main_path = Path(sys.argv[2])
    pr_path = Path(sys.argv[3])

    main = json.loads(main_path.read_text(encoding="utf-8"))
    pr = json.loads(pr_path.read_text(encoding="utf-8"))

    main_matches = main.get("Matches")
    pr_matches = pr.get("Matches")
    if not isinstance(main_matches, list) or not isinstance(pr_matches, list):
        print("invalid json shape: both main/pr must contain top-level Matches array", file=sys.stderr)
        return 3

    main_map = index_by_id(main_matches)
    pr_map = index_by_id(pr_matches)

    if match_id not in pr_map:
        print(f"pr json does not contain match ID={match_id}", file=sys.stderr)
        return 4
    if match_id not in main_map:
        print(f"main json does not contain match ID={match_id}", file=sys.stderr)
        return 5

    main_idx, _ = main_map[match_id]
    _, pr_obj = pr_map[match_id]

    # 仅替换目标 match
    main_matches[main_idx] = pr_obj

    # 写回 main_path（会规范化 JSON 格式：indent=2）
    out = json.dumps(main, ensure_ascii=False, indent=2)
    main_path.write_text(out, encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())