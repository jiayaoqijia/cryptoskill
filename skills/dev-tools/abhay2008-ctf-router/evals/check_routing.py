#!/usr/bin/env python3
"""Coverage check: real-world CTF corpus vs. router + skill text.

For each case in corpus.json:
  - router_groups: every group must match somewhere in ctf-router/SKILL.md
  - skill_groups:  every group must match somewhere in the expected skill's *.md
Groups are lists of regex alternatives (OR within a group, AND across groups).

Exit status 1 if any case fails. Prints a per-case report.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # .agents/skills
ROUTER = ROOT / "ctf-router" / "SKILL.md"
CORPUS = Path(__file__).resolve().parent / "corpus.json"


def read_skill_text(skill: str) -> str:
    d = ROOT / skill
    if not d.is_dir():
        return ""
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(d.glob("*.md")))


def group_pass(groups, text):
    """Return list of (group_index, matched_regex_or_None)."""
    results = []
    for gi, alts in enumerate(groups):
        hit = None
        for pat in alts:
            if re.search(pat, text, re.IGNORECASE | re.MULTILINE):
                hit = pat
                break
        results.append((gi, hit))
    return results


def main():
    data = json.loads(CORPUS.read_text(encoding="utf-8"))
    router_text = ROUTER.read_text(encoding="utf-8")
    cases = data["cases"]
    total = len(cases)
    router_ok = skill_ok = 0
    failures = []
    print(f"{'ID':34} {'EXP':14} {'ROUTER':7} {'SKILL':6}")
    print("-" * 70)
    for c in cases:
        cid = c["id"]
        expected = c["expected"]
        skill_text = read_skill_text(expected)
        r_res = group_pass(c["router_groups"], router_text)
        s_res = group_pass(c["skill_groups"], skill_text)
        r_pass = all(h is not None for _, h in r_res)
        s_pass = all(h is not None for _, h in s_res)
        if r_pass:
            router_ok += 1
        if s_pass:
            skill_ok += 1
        status_r = "OK" if r_pass else "FAIL"
        status_s = "OK" if s_pass else "FAIL"
        print(f"{cid:34} {expected:14} {status_r:7} {status_s:6}")
        if not (r_pass and s_pass):
            failures.append((c, r_res, s_res))
    print("-" * 70)
    print(f"router: {router_ok}/{total}   skill: {skill_ok}/{total}   cases: {total}")
    if failures:
        print("\nFAILURES:")
        for c, r_res, s_res in failures:
            print(f"\n  {c['id']} ({c['expected']})")
            print(f"    url: {c['url']}")
            for gi, hit in r_res:
                if hit is None:
                    print(f"    ROUTER group {gi} unmatched: {c['router_groups'][gi]}")
            for gi, hit in s_res:
                if hit is None:
                    print(f"    SKILL  group {gi} unmatched: {c['skill_groups'][gi]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
PY