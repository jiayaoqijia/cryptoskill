---
name: ac-code-construction
description: "Writing new code and delivering it in small steps: naming, error handling, lint and type gates, walking skeletons, always-green commits, time-boxed spikes, and docs-as-code inside the repo. Use when asking \"implement this\"\"split this feature into small shippable steps keeping main green\",, \"write the function\", \"how should I name this\", \"how should this handle errors\", \"build it step by step\", \"walking skeleton\", \"keep main green\", \"quick prototype to test this\", \"spike this for two days\", \"add docstrings\", \"generate the API reference\". Not for planning the task list or estimates, cleaning up existing working code as a goal in itself, choosing the test portfolio, or branch policy; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Code Construction

## Overview

Four leaves cover the craft of producing new code: how a unit is written (naming, errors, gates), the order and size of the steps it lands in, the throwaway probes that answer a question before real work, and the in-repo documentation that ships with the change.

## When to use

- Writing new functions, modules, error paths; setting up formatter, linter, type gates.
- Landing work in small green steps; building a walking skeleton; running a Parallel Change.
- Running a time-boxed spike or prototype to answer one question.
- Writing docstrings, comments, or a generated API reference in the repo.

## When not to use

- Slicing the spec into tasks or estimating it — outside this skill.
- Refactoring or simplifying existing working code as the main goal — outside this skill.
- Choosing what to test across the whole suite, or branch/merge policy — outside this skill.
- User-facing prose such as READMEs, tutorials and release notes.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/construction.md` | Write new code | "implement this" |
| `subskills/incremental-delivery.md` | Small verified steps | "build it step by step" |
| `subskills/spikes-prototypes.md` | Time-boxed throwaway experiment | "spike this for two days" |
| `subskills/code-docs.md` | Comments, docstrings, generated reference | "document this function" |

## See also

- `subskills/construction.md` — the unit of code.
- `subskills/incremental-delivery.md` — the order the units land in.
- `subskills/spikes-prototypes.md` — the throwaway probe before real work.
- `subskills/code-docs.md` — the prose that ships beside the code.
