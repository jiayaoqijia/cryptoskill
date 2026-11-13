---
name: ac-code-review
description: "Preparing and judging pull requests: author side — small self-contained changes, PR descriptions, self-review, stacked PRs, review packets for agent-written code. Reviewer side — review order, labelled comments, response times, approve-or-request-changes rules. Use when asking \"open a PR\", \"write the PR description\", \"this PR is too big\", \"self-review my diff\", \"stack these PRs\", \"review this PR\", \"is this change OK to merge\", \"approve or request changes\". Not for commit messages and history repair, branching models and protection, or governing machine-written code as a whole; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Code Review

## Overview

Two leaves cover both sides of a change. The author leaf prepares it: one self-contained unit, a description that lets a stranger judge it, self-review, and a review packet when an agent wrote the code. The reviewer leaf judges it: what to check and in what order, labelled comments, response time, and the approve rule.

## When to use

- Opening, sizing or splitting a PR; stacked PRs; drafting the description.
- Self-review before requesting review; CI green first.
- Attaching the review packet for agent-written changes.
- Reviewing a diff: blocking versus non-blocking comments, verdicts, merge calls.

## When not to use

- Commit wording, rebasing and history repair — outside this skill.
- Branch protection, merge queues and CODEOWNERS setup — outside this skill.
- Whole-program governance of machine-written code — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/pr-authoring.md` | Prepare the change | "open a PR" |
| `subskills/code-review.md` | Judge the change | "review this PR" |

## See also

- `subskills/pr-authoring.md` — the author's half.
- `subskills/code-review.md` — the reviewer's half.
