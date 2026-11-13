---
name: ac-debugging
description: "Scientific debugging and defect analysis: reproduce and minimise a failure, hypothesis-driven experiments, sanitizers and race detection, git bisect and delta debugging, fixing the defect class instead of the instance, and triaging a red build or broken pipeline back to green. Use when asking \"why does this fail\", \"fix this bug\", \"it crashes when\", \"race condition\", \"find the root cause\", \"git bisect this\", \"why do we keep getting this bug\", \"CI is red\", \"the build is broken\". Not for designing the test suite that catches the next defect, nor the pipeline's wiring once it is green; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Debugging

## Overview

Three leaves form one loop: reproduce and fix the single bug with the scientific method, find and kill the defect class behind it, and restore a red pipeline to green by failure class. Fix the instance, fix the class, fix the line.

## When to use

- A crash, wrong value, race or deadlock; reproduction, minimisation, hypothesis tests.
- Sanitizers and race detectors; the fails-before-passes-after fix test.
- Bisecting history, shrinking a failing input, causal chains, fix-the-class controls.
- Main is red or the build broke: classify, isolate, restore green, add a guard.

## When not to use

- Designing the test suite or judging its strength — outside this skill.
- Pipeline wiring, caching and required checks once it is green — outside this skill.
- Declaring and running a user-facing outage — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/debugging.md` | Reproduce and fix one bug | "why does this fail" |
| `subskills/root-cause.md` | The class behind a defect | "find the root cause" |
| `subskills/build-failures.md` | Restore a red build or pipeline | "CI is red" |

## See also

- `subskills/debugging.md` — the loop.
- `subskills/root-cause.md` — the class.
- `subskills/build-failures.md` — the red line.
