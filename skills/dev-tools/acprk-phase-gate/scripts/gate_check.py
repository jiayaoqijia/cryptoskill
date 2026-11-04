#!/usr/bin/env python3
"""gate_check.py -- mechanical part of a phase gate on the research blackboard.

    python3 gate_check.py --project . --phase P6
    python3 gate_check.py --project . --phase P7 --paper paper/
    python3 gate_check.py --selftest

Checks (each prints PASS/FAIL/WARN; exit 1 if any FAIL):

  all phases  STATE.md has a gate section for the phase ("## Gate P<k>" or any heading containing
              "Gate" and "P<k>") and every checkbox in it is ticked ("- [x]").
              Unticked boxes may be waived with "- [~] ... WAIVED: <reason> (DECISIONS D-<n>)".
  >= P6       CLAIMS.md: no claim in status `open`; every `survived`/`weakened` claim has at
              least one EVIDENCE ref and a non-empty falsifier-evidence cell.
              Also: EVIDENCE logs exist and are unchanged since recorded (.cra/evidence-hashes.json).
  >= P7       with --paper DIR: every number-with-unit in the .tex sources (e.g. "3.2x", "41%",
              "2^{128}", "12.5 ms") must appear verbatim in the EVIDENCE.md column
              "number/fact as printed in paper", unless the line carries "% no-evidence: <reason>";
              every \\claimref{C<n>} names a survived/weakened claim; every \\evid{E<n>} a ledger row.
  >= P8       refs.bib exists and bib-verify-report.md is fresh for it and lists only VERIFIED entries.
              Freshness: the report's "bib-sha256: <hex>" line must equal sha256(refs.bib)
              (written by verify_bib.py). Legacy reports without that line fall back to git
              commit times (both files tracked and unmodified), then to file mtimes (WARN).

The checks themselves live in lib/core (package `cra_core`, also used by the `cra` CLI and the
cra-mcp server); this script is a thin wrapper.  Install once: pip install -e lib/core

Blackboard formats follow SPEC section 3 (tables with a header row; column order as in SPEC).
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import tempfile

try:
    from cra_core.gates import PHASES, check_gate as check
except ImportError:  # running from a checkout without `pip install -e lib/core`
    _here = os.path.dirname(os.path.abspath(__file__))
    for _up in ("../../../lib/core", "../../../../lib/core"):
        _cand = os.path.normpath(os.path.join(_here, _up))
        if os.path.isdir(os.path.join(_cand, "cra_core")):
            sys.path.insert(0, _cand)
            break
    try:
        from cra_core.gates import PHASES, check_gate as check
    except ImportError:
        sys.exit("gate_check.py needs the cra_core package: pip install -e <crypto-research-agents>/lib/core")


def selftest() -> int:
    with tempfile.TemporaryDirectory() as d:
        w = lambda n, t: open(os.path.join(d, n), "w").write(t)
        w("STATE.md", "# STATE\nphase: P7\n## Gate P7 (writing)\n- [x] outline approved\n"
                      "- [~] figure 3 WAIVED: no data yet (DECISIONS D-4)\n## Active tasks\n- [ ] x\n")
        w("CLAIMS.md", "| ID | claim (falsifiable) | proposer | status | falsifier evidence | EVIDENCE refs |\n"
                       "|---|---|---|---|---|---|\n| C1 | toy is 2x faster | idea-miner | survived | reran, holds | E1 |\n"
                       "| C2 | toy is optimal | theorist | refuted | counterexample n=6 | |\n")
        w("EVIDENCE.md", "| ID | number/fact as printed in paper | command | log path | commit | machine | date | runs/median |\n"
                         "|---|---|---|---|---|---|---|---|\n| E1 | 2.0x | make bench | logs/a | abc | m1 | 2099-01-01 | 5 |\n")
        os.makedirs(os.path.join(d, "paper"))
        os.makedirs(os.path.join(d, "logs"))
        w("logs/a", "2.0x\n")
        w("paper/main.tex", "We are 2.0x faster.\nAlso 17\\% smaller. % no-evidence: quoted from [X]\n")
        r = check(d, "P7", "paper")
        assert all(s != "FAIL" for s, _ in r), r
        w("paper/main.tex", "We are 2.0x faster and 3.5x smaller, 12\\% less memory. % 99x in a comment is ignored\n")
        r = check(d, "P7", "paper")
        assert any("3.5x" in m for s, m in r if s == "FAIL"), r
        assert any("12" in m for s, m in r if s == "FAIL") and not any("99x" in m for _, m in r), r
        w("CLAIMS.md", "| ID | claim | proposer | status | falsifier evidence | EVIDENCE refs |\n|---|---|---|---|---|---|\n"
                       "| C1 | x | y | open | | |\n")
        assert any("still open" in m for s, m in check(d, "P6", None))
        # P8 bib freshness: content hash, not mtime
        w("STATE.md", "# STATE\n## Gate P8\n- [x] done\n")
        w("CLAIMS.md", "| ID | claim | proposer | status | falsifier evidence | EVIDENCE refs |\n"
                       "|---|---|---|---|---|---|\n| C1 | x | y | survived | ok | E1 |\n")
        w("refs.bib", "@misc{a, title={A}}\n")
        sha = hashlib.sha256(b"@misc{a, title={A}}\n").hexdigest()
        w("bib-verify-report.md", f"# bib-verify report\n\nbib-sha256: {sha}\n\n| status | key |\n|---|---|\n| VERIFIED | `a` |\n")
        os.utime(os.path.join(d, "bib-verify-report.md"), (0, 0))   # mtime older than refs.bib: must not matter
        assert any(s == "PASS" and "bib-verify" in m for s, m in check(d, "P8", None)), check(d, "P8", None)
        w("refs.bib", "@misc{a, title={A}}\n@misc{b, title={B}}\n")   # bib changed after verification
        assert any(s == "FAIL" and "stale" in m for s, m in check(d, "P8", None))
    print("selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default=".")
    ap.add_argument("--phase", choices=PHASES)
    ap.add_argument("--paper", help="paper directory relative to project (enables number check at P7+)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.phase:
        ap.error("--phase is required")
    res = check(a.project, a.phase, a.paper)
    for s, m in res:
        print(f"{s:4s}  {m}")
    fails = sum(s == "FAIL" for s, _ in res)
    print(f"\nGate {a.phase}: {'PASS' if not fails else f'FAIL ({fails} blocking items)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
