---
name: ac-architecture-survey
description: "Read-only, evidence-backed survey of a whole repository for architecture and module-deepening opportunities, producing a prioritized report of bounded improvement candidates. Use when asking 'survey this repository', 'architecture review of our codebase', 'what should we improve first', 'find structural problems in this code', 'audit our architecture', 'prioritize refactoring opportunities'. Not for making structure or design decisions (that is ac-architecture), not for executing refactors or debt cleanup (ac-codebase-maintenance), not for reviewing a diff or PR (ac-code-review)."
license: MIT
metadata:
  domain: software-engineering
---

# Architecture Survey

## Overview

A read-only, evidence-backed survey of a whole repository for architecture and module-deepening opportunities, producing a prioritized report of bounded improvement candidates. The survey never implements a candidate and never designs the replacement — it stops at the report, and the user chooses. The only permitted write is the report itself.

## When to use

- Reviewing an existing codebase to locate scattered policy, repeated coordination, and structural smells before planning changes.
- Building an evidence-graded survey report that prioritizes module-deepening opportunities across a repository.
- Establishing baseline structural coverage and sampling evidence before committing refactoring effort.

## When not to use

- Making new system architecture or design decisions (use ac-architecture).
- Executing code refactors, structural migrations, or debt removal (use ac-codebase-maintenance).
- Reviewing an isolated pull request, commit, or patch (use ac-code-review).

## Subskill index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/survey-scope.md` | `software-engineering/survey-scope` | Scoping the read-only survey: stack, entry points, ownership boundaries, dependency direction, runtime paths, tests, and existing architecture records; sampling callers to distinguish recurring problems from isolated files; coverage discipline. |
| `subskills/evidence-versus-judgment.md` | `software-engineering/evidence-versus-judgment` | The evidence bar: every finding cites concrete observed evidence separated from design judgment; the recurring-versus-isolated test; why unsupported aesthetic claims fail the bar. |
| `subskills/structural-smells.md` | `software-engineering/structural-smells` | The catalog of architectural smells: scattered policy, repeated coordination, unclear lifecycle ownership, pass-through layers, duplicated boundaries, hidden side effects, and verify-hostile seams. |
| `subskills/candidate-formation.md` | `software-engineering/candidate-formation` | Turning a finding into a bounded candidate: concrete pain and cited evidence, proposed responsibility boundary, affected callers, expected benefit, risk, and proportionate validation. |
| `subskills/ranking-criteria.md` | `software-engineering/ranking-criteria` | Ranking candidates across impact, locality, confidence, and effort axes; prioritizing recurring high-impact problems over broad aesthetic rewrites; shortlist structure. |
| `subskills/report-discipline.md` | `software-engineering/report-discipline` | The report as the sole permitted write: scale to the repository, omit empty sections, state coverage and unknowns, write only to the specified path, and stop after delivery. |
| `subskills/follow-up-boundary.md` | `software-engineering/follow-up-boundary` | After candidate selection: recording the chosen candidate and its evidence trail for subsequent design, migration, or implementation phases without starting them uninvited. |

## Status and honest limits

- Status: seedling.
- Honest limits: The survey relies on static sampling, text grepping, and structural tree inspection. It cannot prove runtime performance characteristics or catch dynamic reflection paths that evade static symbol references. ⚠️
