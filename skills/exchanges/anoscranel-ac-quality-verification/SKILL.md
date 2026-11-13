---
name: ac-quality-verification
description: "Quality models and verification-and-validation work: ISO/IEC 25010 quality attributes with numbers, V&V plans, bidirectional traceability matrices, the formal-methods ladder from assertions to provers, and lifecycle evidence for regulated software — IEC 62304, DO-178C, agile inside a QMS. Use when asking \"write a V&V plan\", \"build a traceability matrix\", \"regulator wants proof every requirement is verified\", \"IEC 62304 evidence\", \"DO-178C objectives\", \"ISO 25010 quality model\". Not for the general test portfolio, running an outage, or release governance; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Quality Verification

## Overview

Two leaves cover verification-and-validation as a discipline. One sets measurable quality attributes, writes the V&V plan, and picks the cheapest formal-methods rung that can find the feared defect. The other shapes the evidence a regulated lifecycle demands: classification, independence, SOUP registers and audit rehearsals.

## When to use

- Turning NFRs into measurable quality attributes; writing the V&V plan.
- Building a bidirectional requirement-to-test traceability matrix.
- Choosing between property tests, model checking and proof assistants.
- Preparing IEC 62304, DO-178C or FDA-agile lifecycle evidence.

## When not to use

- The general test portfolio and its CI gates — outside this skill.
- Running an outage or postmortem — outside this skill.
- Ordinary release governance — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/quality-vv.md` | Quality model, V&V plan, traceability | "write a V&V plan" |
| `subskills/regulated-software.md` | IEC 62304, DO-178C evidence | "medical device software" |

## See also

- `subskills/quality-vv.md` — prove quality.
- `subskills/regulated-software.md` — prove it to a regulator.
