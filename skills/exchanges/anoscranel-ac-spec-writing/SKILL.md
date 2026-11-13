---
name: ac-spec-writing
description: "Requirements and specification writing: user stories, acceptance criteria, NFRs, design docs and RFCs. Use when asking \"write a spec\", \"acceptance criteria for this\", \"is this requirement testable\", \"draft the design doc\", \"RFC for this change\", \"set the done criteria\", \"turn this request into requirements\", \"write the NFRs\". Not for slicing an approved spec into a task list, estimating the work, or recording one decision already made; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Spec Writing

## Overview

Two leaves cover the text an engineer writes before code: single requirements with acceptance criteria, and the design document that binds them. Requirements get the ISO/IEC/IEEE 29148 quality test; specs get goals, non-goals, alternatives and open questions.

## When to use

- Writing or reviewing user stories, acceptance criteria, NFR statements.
- Drafting, structuring or reviewing a design doc, spec or RFC before implementation.
- Checking whether one requirement or one spec is testable, complete and unambiguous.

## When not to use

- Slicing an approved spec into ordered tasks, estimating it, or picking a cadence — that work sits outside this skill.
- Recording a single architecture decision already taken — outside this skill.
- Writing code, tests, or prose for end users.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/requirements.md` | Stories, acceptance criteria, NFRs | "write acceptance criteria" |
| `subskills/spec-writing.md` | Design doc before code | "write a spec" |

## See also

- `subskills/requirements.md` — the single-requirement quality test.
- `subskills/spec-writing.md` — the whole-document shape.
