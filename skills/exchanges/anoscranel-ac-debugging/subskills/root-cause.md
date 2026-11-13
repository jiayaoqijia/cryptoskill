---
name: root-cause
domain: software-engineering/root-cause
trigger: "\"Find the root cause\", \"which commit broke this\", \"git bisect this\", \"shrink this failing input\", \"why do we keep getting this bug\", \"fix the class, not the instance\"."
anti_trigger: "Reproducing and fixing a single bug (subskills/debugging.md); a red pipeline (subskills/build-failures.md); writing an incident postmortem."
scope: "Finding the cause behind a defect: bisect, delta debugging, 5-whys limits, fix-the-class"
status: "seedling"
---

# Root Cause

## Standard

- **Bisection**: `git bisect` binary-searches history for the first bad commit. `git bisect run` takes a script: exit 0 = good, 1–127 = bad, 125 = skip (https://git-scm.com/docs/git-bisect).
- **Delta debugging**: Zeller's ddmin reduces a failing input to a 1-minimal cause set (https://arxiv.org/abs/cs/0012009).
- **Evidence for the cheap tool**: a 2026 ICSE study found bisect to the bug-inducing commit beat spectrum-based fault localisation on Top-1 and Top-5 across 120 GCC and LLVM bugs (https://dl.acm.org/doi/10.1145/3744916.3773254). ⚠️ Single study.
- **RCA methods**: five whys, Ishikawa (fishbone), fault tree. Five whys follows one chain and tends to land on a person; use it to start, not to conclude.
- **Classification**: IEEE 1044 failure / fault / defect classes drive causal analysis and process improvement (https://standards.ieee.org/ieee/1044/1526).
- **Test gap**: for each escape, name the test level that should have caught it.

## Decision rules

1. "It used to work" → bisect first. It is cheap and objective.
2. Large failing input → ddmin it before reading code.
3. Root cause = the earliest point where a change would have prevented the defect class, not only this instance.
4. Ask "why" until you reach a process, design or tooling cause you can change. Stop at a person and you have stopped too early.
5. Grep for the same pattern elsewhere. One instance usually means more.
6. Fix the class with the strongest cheap control: make it impossible (types, API shape) → fail fast (lint rule, assertion, CI check) → visible (test, alert) → documented.
7. Every root cause yields a regression test at the level that should have caught it.
8. Unconfirmed causes stay labelled "hypothesis".

## Procedure

1. Bisect:
   ```bash
   git bisect start
   git bisect bad HEAD
   git bisect good v1.4.0
   git bisect run ./repro.sh      # exit 0 good, 1 bad, 125 skip
   git bisect reset
   ```
2. Read the first bad commit. State what it changed and why that breaks the case.
3. Minimise input: keep halving and keep the part that still fails (ddmin), or use a reducer such as `creduce`.
4. Draw the chain: trigger → fault → failure. Mark where a check could have stopped it.
5. Classify: requirements, design, code, configuration, test or environment.
6. Search the repo for siblings.
7. Choose the class fix by rule 6. Add the test at the missing level.
8. Write the record:
   ```markdown
   Defect: <id>  Class: <type>
   Introduced by: <commit>  Escaped: <test level>
   Chain: trigger → fault → failure
   Class fix: <control added>  Siblings fixed: <n>
   ```

## Anti-patterns

- "Root cause: human error."
- Stopping at the bad commit without asking why the gate missed it.
- Fixing one instance while siblings remain.
- Calling an agent's guess a root cause.

## Done checklist

- [ ] Introducing commit or minimal input found.
- [ ] Causal chain written with evidence.
- [ ] Defect classified; escaped test level named.
- [ ] Siblings searched and fixed.
- [ ] Class-level control and regression test added.

## Sources

- <https://courses.cs.duke.edu/compsci308/spring26/readings/Zeller_Scientific_Debugging.pdf>
- <https://noriskillsets.dev/skills/systematic-debugging>
- https://git-scm.com/docs/git-bisect · https://arxiv.org/abs/cs/0012009
