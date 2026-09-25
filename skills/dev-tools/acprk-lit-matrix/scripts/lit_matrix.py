#!/usr/bin/env python3
"""lit_matrix.py -- lint the related-work matrix and novelty-check log in LITERATURE.md.

    python3 lit_matrix.py LITERATURE.md [--bib refs.bib] [--max-novelty-age 30]
    python3 lit_matrix.py --template          # print an empty matrix + log skeleton
    python3 lit_matrix.py --selftest

Matrix columns (order fixed, header row must match case-insensitively):
  work | venue/year | setting | technique | asymptotics | concrete numbers + source | code? | our delta

Row rules
  * work: contains a bib key  `[@key]`  or  `\\cite{key}`  or an ePrint id  YYYY/NNNN
  * concrete numbers + source: empty, "n/a", or numbers WITH a source pointer
    (Tab./Table/Fig./Sec./§/p./Thm./"measured" + EVIDENCE id E<n>/"reported in")
  * code?: yes <url> | no | unknown
  * our delta: non-empty (what we do that this row does not; "none" is an honest answer and a red flag)
With --bib: every key used in the matrix must exist in refs.bib.

Novelty log: a section "## Novelty checks" with lines
  - YYYY-MM-DD | query: "..." | sources: eprint,crossref | window: 12m | hits reviewed: N | verdict: clear|overlap:<key>|taken:<key>
The newest entry must be at most --max-novelty-age days old (default 30) and must not say "taken".
Exit 1 on any error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys

COLUMNS = ["work", "venue/year", "setting", "technique", "asymptotics",
           "concrete numbers + source", "code?", "our delta"]
SOURCE_PTR = re.compile(r"(tab\.?|table|fig\.?|figure|sec\.?|§|p\.\s?\d|thm\.?|measured|reported in|\bE\d+\b)", re.I)
KEY_PAT = re.compile(r"\[@([\w:\-./]+)\]|\\cite[pt]?\{([^}]+)\}")
EPRINT_PAT = re.compile(r"\b(19|20)\d{2}/\d{2,5}\b")

TEMPLATE = """## Related-work matrix

| work | venue/year | setting | technique | asymptotics | concrete numbers + source | code? | our delta |
|---|---|---|---|---|---|---|---|
| [@Key20] Short name | CONF 2020 | params / model / threat model | main idea in <= 12 words | e.g. O(n log n) ops, O(1) rounds | 3.1 ms @ 128-bit (Tab. 4) | yes https://... | what we add; "none" = red flag |

## Novelty checks

- 2099-01-01 | query: "..." | sources: eprint,crossref | window: 12m | hits reviewed: 0 | verdict: clear
"""


def parse_matrix(text: str):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.strip().startswith("|"):
            hdr = [h.strip().lower() for h in l.strip().strip("|").split("|")]
            if hdr[:1] == ["work"]:
                rows = []
                for r in lines[i + 2:]:
                    if not r.strip().startswith("|"):
                        break
                    cells = [c.strip() for c in r.strip().strip("|").split("|")]
                    rows.append(cells + [""] * (len(hdr) - len(cells)))
                return hdr, rows
    return None, []


def bib_keys(path: str) -> set[str]:
    with open(path, encoding="utf-8") as fh:
        return set(re.findall(r"@\w+\s*[{(]\s*([^,\s]+)\s*,", fh.read()))


def lint(text: str, bib: set[str] | None, max_age: int, today: dt.date) -> list[str]:
    errs = []
    hdr, rows = parse_matrix(text)
    if hdr is None:
        return ["no related-work matrix found (header must start with '| work |')"]
    if hdr != COLUMNS:
        errs.append(f"matrix header {hdr} != expected {COLUMNS}")
    if not rows:
        errs.append("matrix has no rows")
    for n, c in enumerate(rows, 1):
        c = dict(zip(COLUMNS, c))
        tag = f"row {n} ({c['work'][:30]})"
        keys = [k for m in KEY_PAT.finditer(c["work"]) for k in (m.group(1) or m.group(2)).split(",")]
        if not keys and not EPRINT_PAT.search(c["work"]):
            errs.append(f"{tag}: no bib key or ePrint id")
        if bib is not None:
            for k in keys:
                if k.strip() not in bib:
                    errs.append(f"{tag}: key '{k.strip()}' not in refs.bib")
        num = c["concrete numbers + source"]
        if num and num.lower() not in ("n/a", "-", "none") and re.search(r"\d", num) and not SOURCE_PTR.search(num):
            errs.append(f"{tag}: numbers without a source pointer: '{num}'")
        if not re.match(r"^(yes\b.*https?://\S+|no\b|unknown\b)", c["code?"], re.I):
            errs.append(f"{tag}: code? must be 'yes <url>', 'no' or 'unknown'")
        if not c["our delta"]:
            errs.append(f"{tag}: empty 'our delta'")
        elif c["our delta"].lower().startswith("none"):
            errs.append(f"{tag}: WARNING our delta = none (overlap; tell the PI)")
    m = re.search(r"^##\s*Novelty checks\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if not m:
        errs.append("no '## Novelty checks' section")
    else:
        entries = re.findall(r"^-\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)$", m.group(1), re.M)
        if not entries:
            errs.append("novelty log is empty")
        else:
            newest = max(entries, key=lambda e: e[0])
            age = (today - dt.date.fromisoformat(newest[0])).days
            if age > max_age:
                errs.append(f"newest novelty check is {age} days old (> {max_age}); re-run eprint_search.py")
            if re.search(r"verdict:\s*taken", newest[1], re.I):
                errs.append(f"newest novelty check says TAKEN: {newest[1].strip()}")
    return errs


def selftest() -> int:
    good = TEMPLATE.replace("2099-01-01", "2000-01-10")
    e = lint(good, {"Key20"}, 30, dt.date(2000, 1, 20))
    assert e == [], e
    bad = good.replace("(Tab. 4)", "").replace("yes https://...", "maybe")
    e = lint(bad, {"Other"}, 30, dt.date(2000, 3, 1))
    assert any("source pointer" in x for x in e) and any("code?" in x for x in e)
    assert any("not in refs.bib" in x for x in e) and any("days old" in x for x in e), e
    print("selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("literature", nargs="?")
    ap.add_argument("--bib")
    ap.add_argument("--max-novelty-age", type=int, default=30)
    ap.add_argument("--template", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.template:
        print(TEMPLATE)
        return 0
    if not a.literature:
        ap.error("give LITERATURE.md")
    with open(a.literature, encoding="utf-8") as fh:
        text = fh.read()
    errs = lint(text, bib_keys(a.bib) if a.bib else None, a.max_novelty_age, dt.date.today())
    for x in errs:
        print(("WARN  " if x.startswith("row") and "WARNING" in x else "ERROR ") + x)
    hard = [x for x in errs if "WARNING" not in x]
    print("lit-matrix:", "OK" if not hard else f"{len(hard)} error(s)")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
