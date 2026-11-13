---
name: ac-evidence-and-citation
description: "Evidence and citation craft for a document being written: finding and judging sources, logging them, checking a document's claims against them, verifying quotes, catching plagiarism risk, and binding claims to checkable citations in a chosen style. Use when asking \"cite this\", \"add references\", \"which citation style\", \"is this plagiarism\", \"check my sources\", \"find evidence for this\", \"verify these quotes\", \"where did this number come from\", \"check my citations resolve\". Not for open-ended research that answers a question rather than defining the record for a document, and not for the AI-disclosure decision; that work sits outside this skill."
license: MIT
metadata:
  domain: writing
---

# Evidence and Citation

## Overview

Two leaves cover the evidence layer of a document. research-sources.md finds sources, judges them and keeps the source log. citation-grounding.md binds claims to checkable sources, verifies quotes, applies the citation style and catches plagiarism risk before anything ships.

## When to use

- Finding and judging sources for a document in progress.
- Checking claims against sources; verifying quotes.
- Adding references in a chosen style; resolving citations.
- Reviewing a document for plagiarism risk.

## When not to use

- A general research question with no document attached — outside this skill.
- Assembling a systematic-review study set — outside this skill.
- The venue's AI-use disclosure decision — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/research-sources.md` | Find, judge and log sources | "check my sources" |
| `subskills/citation-grounding.md` | Bind claims to checkable sources | "cite this" |

## See also

- `subskills/research-sources.md` — find and judge first.
- `subskills/citation-grounding.md` — then bind and check.
