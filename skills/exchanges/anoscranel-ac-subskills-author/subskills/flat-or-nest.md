---
name: flat-or-nest
domain: skill-authoring/flat-or-nest
trigger: After the domain map sets the leaf count — decide the tree's shape.
anti_trigger: The leaf count is already decided and recorded for this skill.
scope: The flat-vs-nested decision; records the decision and its reason.
status: seedling
---

# Flat or Nest (pipeline step 3)

Decide the tree shape from the leaf count. **Flat-first is the default; nesting is the
overflow valve, never the default**.

## Standard

Why flat wins below the ceiling (operator judgment; ~60 rests on an unsourced ~8
lines/row estimate): one hop, full-read guarantee, zero second-hop selection error, and
Rules 3–4 become trivially checkable because every scope claim lives in one file.
"Reality is nested" is served by the index's *wording*, not by filesystem depth.

## Decision rules

- **≤60 (operator-set limit ⚠️) leaves → FLAT depth-1, preferred (lint WARNs otherwise).**
  One rich multi-column index in SKILL.md (task | trigger | leaf); every leaf linked
  directly. No intermediate files.
- **>60 leaves → nesting becomes legal**, and then ONLY as: `subskills/<group>/INDEX.md`
  (a pure TOC — frontmatter + heading + routing table, **zero imperative sentences**)
  routing to leaves. Max depth 2 (index→index→leaf). Depth ≥3 is forbidden.

## Procedure

1. Read the leaf count from domain-map's output table.
2. If ≤60, choose FLAT. If >60, split into groups and nest one level.
3. If NESTED, name each group and confirm each `INDEX.md` is pure TOC.

## Anti-patterns

- Nesting to look organized — nest only when the index alone would blow the ≤500-line
  SKILL.md body budget.
- A nesting level deeper than index→index→leaf.

## Done checklist

The decision (FLAT or NESTED), the leaf count, and a one-paragraph rationale, recorded
and shown to the operator at hand-off.

The deciding question is not size but whether a reader would ever need one leaf without the others: a set of leaves that are always consulted together is a document, and one whose leaves are consulted alone is a tree. Counting leaves answers a question nobody asked.

The practical test is to ask what the index would have to say if the leaves were flattened: if it would be a list of headings with no argument between them, the nesting was doing nothing and the leaves should merge. If it would be a paragraph of routing decisions, the tree is carrying information the flat file would lose.


A third consideration is the cost of a wrong choice in each direction: a flat file that should have been a tree is annoying but readable, while a tree that should have been flat hides its content behind a navigation step that nobody takes. When the evidence is ambiguous, the flatter form fails more gently.


## Sources

- House standard for skills-with-subskills (unpublished).
- <https://martinfowler.com>
- <https://github.com/>
