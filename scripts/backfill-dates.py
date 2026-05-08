#!/usr/bin/env python3
"""
Backfill added_at + last_updated for every skill directory by walking git
history. Result is cached in scripts/.skill-dates.json so the bot doesn't
re-walk 1300+ trees on every catalog run.

added_at  = first commit that added any file under the skill dir
last_updated = most recent commit touching the skill dir

Run:
  python3 scripts/backfill-dates.py            # only fills missing entries
  python3 scripts/backfill-dates.py --rebuild  # discards cache, re-walks all
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CACHE = ROOT / "scripts" / ".skill-dates.json"


def git_date(args):
    """Return the ISO date of the first/last matching commit, or None.

    Note on `[-1]`: `git log` defaults to reverse-chronological order
    (newest first), so the LAST line of the output is the OLDEST commit.
    For `added_at` we pass `--diff-filter=A` and want the oldest add
    commit — `[-1]` is therefore correct.
    For `last_updated` we pass `-1` so only one line is returned and
    `[-1]` and `[0]` both yield the same most-recent commit.
    Verified empirically against a multi-add skill dir
    (skills/exchanges/binance-official-spot returns
    [2026-04-26, 2026-03-20], and `[-1]` correctly extracts 2026-03-20)."""
    try:
        r = subprocess.run(
            ["git", "-C", str(ROOT), *args],
            capture_output=True, text=True, timeout=20, check=False,
        )
        out = (r.stdout or "").strip()
        return out.split("\n")[-1].strip()[:10] or None  # YYYY-MM-DD
    except (subprocess.TimeoutExpired, OSError):
        return None


def added_and_updated(rel_path):
    """First-add commit + most-recent commit covering this directory."""
    # First commit that ADDED files in this dir (--diff-filter=A).
    first = git_date(["log", "--diff-filter=A", "--format=%cI",
                      "--", rel_path])
    last = git_date(["log", "-1", "--format=%cI", "--", rel_path])
    return first, last


def load_cache():
    if not CACHE.exists():
        return {}
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_cache(data):
    CACHE.write_text(json.dumps(data, indent=2, sort_keys=True),
                     encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rebuild", action="store_true",
                   help="Discard cache and re-walk every skill")
    args = p.parse_args()

    cache = {} if args.rebuild else load_cache()
    discovered = 0
    filled = 0
    skipped = 0

    for cat in sorted(SKILLS_DIR.iterdir()):
        if not cat.is_dir():
            continue
        for skill in sorted(cat.iterdir()):
            if not skill.is_dir():
                continue
            rel = str(skill.relative_to(ROOT))
            discovered += 1
            if rel in cache and cache[rel].get("added_at"):
                skipped += 1
                continue
            added, updated = added_and_updated(rel)
            cache[rel] = {"added_at": added, "last_updated": updated}
            filled += 1
            if filled % 50 == 0:
                save_cache(cache)
                print(f"  ... {filled} filled", file=sys.stderr)

    save_cache(cache)
    print(f"discovered: {discovered}")
    print(f"filled:     {filled}")
    print(f"cached hit: {skipped}")
    print(f"cache file: {CACHE}")


if __name__ == "__main__":
    main()
