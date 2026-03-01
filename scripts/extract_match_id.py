#!/usr/bin/env python3
import re
import sys

def main():
    if len(sys.argv) != 2:
        print("usage: extract_match_id.py <pr_title>", file=sys.stderr)
        return 2

    title = sys.argv[1]
    m = re.search(r"\bMatch:\s*(\d+)\b", title)
    if not m:
        print(f"cannot parse match id from title: {title}", file=sys.stderr)
        return 3

    print(m.group(1))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())