---
name: phase-gate
description: Evaluate whether a research project may leave phase P0..P8 by checking the STATE.md gate checklist, CLAIMS.md verdicts, EVIDENCE.md coverage of paper numbers, and bib-verify status. Use at every phase transition and before any external submission.
---

# phase-gate

The orchestrator owns gates; this skill is the checklist and the mechanical checker.

## Mechanical check

```bash
python3 skills/phase-gate/scripts/gate_check.py --project . --phase P6
python3 skills/phase-gate/scripts/gate_check.py --project . --phase P7 --paper paper/
python3 skills/phase-gate/scripts/gate_check.py --selftest
```

It fails on: unticked gate items (waivers need `WAIVED: <reason> (DECISIONS D-<n>)`), `open` claims from P6 on,
`survived`/`weakened` claims without EVIDENCE refs or falsifier evidence, paper numbers (×, %, ms, bits, 2^k …)
without a matching EVIDENCE row from P7 on (escape hatch: `% no-evidence: <reason>` on the line, e.g. a number quoted
from a cited paper), and a missing/stale/unclean bib-verify report at P8.

## Gate checklists (copy into STATE.md under `## Gate P<k>`)

**P0 Scoping** — [ ] one-paragraph problem statement with a measurable target · [ ] target venue(s) + deadline ·
[ ] scope: in/out list · [ ] resources (machines, libraries, time budget) · [ ] kill criteria written.

**P1 Literature** — [ ] related-work matrix with ≥ the 2–4 true competitors in bold · [ ] novelty check logged
(≤30 days, verdict not `taken`) · [ ] refs.bib passes bib-verify · [ ] reading notes for every competitor ·
[ ] baseline candidates listed with code availability.

**P2 Ideation** — [ ] ≥1 idea with pre-gate sentence (security-bearing vs substrate) · [ ] Gate A (freed parameter)
and Gate B (anomaly) recorded, or honest negative · [ ] every idea's core claims entered in CLAIMS.md as
falsifiable rows (status `open`) · [ ] novelty re-check for the chosen idea.

**P3 Theory** — [ ] each theorem stated with all hypotheses · [ ] numerically checked (Sage/Python) on small cases ·
[ ] load-bearing lemmas formalised or independently re-derived · [ ] parameter/security estimate reproduced with an
estimator, cost model stated · [ ] lower bound or explicit "no bound known".

**P4 Baselines** — [ ] each competitor pinned (url, commit/tag, build recipe) in `baselines/MANIFEST.md` ·
[ ] baseline reproduces its paper's headline number within tolerance, or the discrepancy is documented ·
[ ] build flags identical between baseline and ours.

**P5 Experiments** — [ ] bench protocol (machine, threads, pinning, warm-up, interleaving, repeats) fixed before
running · [ ] every result in EVIDENCE.md with command/log/commit/machine/date/runs · [ ] control candidate measured ·
[ ] component and end-to-end, absolute and relative.

**P6 Falsification** — [ ] falsifier ruled on every claim (no `open`) · [ ] refuted claims removed or reworded;
weakened claims restated with their new scope · [ ] cost/price of each gain stated · [ ] PI decision in DECISIONS.md.

**P7 Writing + figures** — [ ] every paper number has an EVIDENCE row · [ ] every claim in the paper maps to a
`survived`/`weakened` CLAIMS row · [ ] figures regenerated from logged data by script · [ ] related work written from
the matrix · [ ] notation consistent.

**P8 Review → submit → rebuttal → camera-ready** — [ ] ≥1 venue-calibrated mock review, all major points answered ·
[ ] bib-verify clean on the final bib · [ ] anonymisation and page limits checked · [ ] artifact builds from a clean
checkout · [ ] final novelty re-check (≤7 days before submission).

## Loops

P6 may send work back to P2 (idea refuted), P3 (proof gap), or P5 (measurement gap). P8 may send back to P7 or P5.
Every backward transition is a DECISIONS.md entry with the triggering claim/review id.
