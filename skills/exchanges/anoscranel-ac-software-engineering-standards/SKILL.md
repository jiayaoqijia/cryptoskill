---
name: ac-software-engineering-standards
description: "Software-engineering standards reference: which standard exists and which edition is current — SWEBOK v4, ISO/IEC 25010, ISO/IEC/IEEE 29148, SemVer, Conventional Commits, WCAG 2.2, NIST SSDF SP 800-218, IEC 62304, DO-178C — plus definitions of done per lifecycle activity and the map that places security activities in lifecycle phases. Use when asking \"what is the standard for\", \"which SWEBOK/SSDF practice applies\", \"where does security fit in our process\", \"definition of done for X\", \"map our process to SSDF\", \"shift-left or shield-right\". Not for doing the governed work itself — writing the spec, hardening the endpoint, designing the schema; those sit outside this skill; security-standard editions and dates (use ac-security-standards)."
license: MIT
metadata:
  domain: software-engineering
---

# Software Engineering Standards

## Overview

The reference layer, not the workshop. One leaf maps the domain's standards: names, current editions, dates, and what each governs. One leaf defines done for each lifecycle activity. One leaf places security activities across the lifecycle phases — the SSDF map — without selecting any control. It states where authority lives; it never says how to do the work.

## When to use

- "What is the standard for X" and "which edition is current" questions.
- Picking which standard or practice group governs an activity.
- Setting done criteria for a task or a Definition of Done for the team.
- Placing security work into lifecycle phases: specify, design, implement, verify, release, respond.

## When not to use

- Performing the task the standard governs — specifying, designing, building, testing, shipping, hardening. Those are craft tasks outside this skill.
- Selecting or implementing any security control; only the phase map lives here.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/standards-map.md` | Which standard applies, with edition and date | "what is the standard for" |
| `subskills/definition-of-done.md` | Done criteria per activity | "definition of done for X" |
| `subskills/secure-sdlc.md` | Security activities by lifecycle phase | "where does security fit in our process" |

## See also

- `subskills/standards-map.md` — the authorities.
- `subskills/definition-of-done.md` — the finish lines.
- `subskills/secure-sdlc.md` — security's seat in the lifecycle.
