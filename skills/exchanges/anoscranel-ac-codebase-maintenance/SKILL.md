---
name: ac-codebase-maintenance
description: "Maintaining an existing codebase: simplification, dead-code removal, named refactorings and strangler-fig migrations, tech-debt registers and hotspots, dependency upgrades and licence intake, retiring features and systems. Use when asking \"simplify this\"\"make this clearer without changing what it does\", \"dead code\", \"remove the dead branches\", \"rename and shrink this\",, \"clean up this function\", \"refactor this\", \"strangler fig\", \"remove dead code\", \"where is our tech debt\", \"what should we fix first\", \"upgrade dependencies\", \"this package is abandoned\", \"remove this feature\", \"retire this system\". Not for writing new behaviour, schema-migration mechanics, or CI gate wiring; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Codebase Maintenance

## Overview

Five leaves cover keeping, improving and retiring existing code: free-form simplification, the named refactoring recipes, the debt register that picks which fix pays, the dependency life cycle, and the end-of-life process for a feature or system.

## When to use

- Cutting complexity or dead code without changing behaviour.
- Applying a named refactoring, or moving a system with a strangler fig.
- Measuring debt, building a register, entering a legacy codebase safely.
- Adding, pinning, upgrading or removing a dependency; licence intake.
- Announcing, deprecating and sunsetting a feature, API or system.

## When not to use

- New behaviour or a first-time build — outside this skill.
- Live-schema change mechanics (expand-migrate-contract) — outside this skill.
- Pipeline wiring and CI gate order — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/simplification.md` | Cut complexity, same behaviour | "simplify this" |
| `subskills/refactoring.md` | Named refactorings in safe steps | "refactor this" |
| `subskills/tech-debt.md` | Debt register, legacy entry | "where is our debt" |
| `subskills/dependency-management.md` | Add, pin, upgrade dependencies | "upgrade dependencies" |
| `subskills/deprecation.md` | Retire a feature or system | "remove this feature" |

## See also

- `subskills/simplification.md` — free-form cleanup.
- `subskills/refactoring.md` — the catalogue moves.
- `subskills/tech-debt.md` — what to fix first.
- `subskills/dependency-management.md` — the libraries you ride.
- `subskills/deprecation.md` — the exit.
