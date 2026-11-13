---
name: ac-architecture
description: "Software architecture and design records: system structure and styles, C4 views, quality-attribute trade-offs, internal module boundaries, coupling and cohesion, Architecture Decision Records. Use when asking \"how should we structure this system\", \"monolith or microservices\", \"which architecture style\", \"will this scale\", \"C4 view\", \"where should this code live\", \"this module does too much\", \"reduce coupling\", \"record this decision\", \"write an ADR\". Not for the external API contract itself, line-level code cleanup, or drawing slide-deck diagrams; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Architecture

## Overview

Three leaves cover one seam: whole-system structure (styles, C4, quality attributes), internal boundaries inside a codebase (deep modules, coupling), and the record of a significant decision once taken. Structure first, boundaries second, the record last.

## When to use

- Choosing or reviewing a system structure: monolith vs services, layering, data ownership.
- Designing module boundaries inside one codebase; reducing coupling, god modules, cycles.
- Writing, numbering or superseding an ADR for a decision already made.

## When not to use

- Designing the public HTTP/RPC contract — outside this skill.
- Free-form code cleanup, naming, or dependency upgrades — outside this skill.
- Diagrams as presentation art with no design decision attached.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/architecture.md` | System structure and trade-offs | "how should we structure this" |
| `subskills/module-design.md` | Internal module boundaries | "where should this code live" |
| `subskills/adr.md` | Record a decision | "write an ADR" |

## See also

- `subskills/architecture.md` — the whole-system view.
- `subskills/module-design.md` — inside one codebase.
- `subskills/adr.md` — the decision record.
