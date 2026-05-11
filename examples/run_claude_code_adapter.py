"""Run the Claude Code adapter against a project and print event counts.

Usage:
    python -m examples.run_claude_code_adapter /storage/kiran-stuff/triplet-proof

This is the script to use after copying the JSONL from Boron to the
local machine. Or, if running directly on Boron, point it at the live
project path. Either way, ~/.claude/projects/ must be present locally.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from aivs.adapters.claude_code import ClaudeCodeAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path", type=Path)
    parser.add_argument(
        "--verbosity",
        choices=["summary", "default", "verbose"],
        default="default",
    )
    parser.add_argument("--limit", type=int, default=0,
                        help="0 = no limit; otherwise stop after N events.")
    args = parser.parse_args()

    adapter = ClaudeCodeAdapter(verbosity=args.verbosity)
    if not adapter.detect(args.project_path):
        print(f"No Claude Code sessions found for {args.project_path}")
        print(f"  expected at: {adapter._project_dir(args.project_path)}")
        return

    counts = Counter()
    first_ts = None
    last_ts = None
    n = 0
    for ev in adapter.extract(args.project_path):
        counts[ev.action] += 1
        if first_ts is None or ev.timestamp < first_ts:
            first_ts = ev.timestamp
        if last_ts is None or ev.timestamp > last_ts:
            last_ts = ev.timestamp
        n += 1
        if args.limit and n >= args.limit:
            break

    print(f"=== Claude Code adapter ({args.verbosity}) ===")
    print(f"  project       : {args.project_path}")
    print(f"  total events  : {n}")
    print(f"  time range    : {first_ts} → {last_ts}")
    print("  by action     :")
    for action, count in counts.most_common():
        print(f"    {action:20s} {count:6d}")


if __name__ == "__main__":
    main()
