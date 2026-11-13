---
name: ac-git-workflow
description: "Version-control craft: branching models and trunk-based development, branch protection, merge queues, CODEOWNERS and monorepo layout, plus commit messages, Conventional Commits, rebase versus merge, history repair and changelog generation. Use when asking \"which branching model\", \"trunk-based or GitFlow\", \"set up branch protection\", \"add a merge queue\", \"set up CODEOWNERS\", \"write a commit message\", \"rebase or merge\", \"fix my git history\", \"which commit broke this\". Not for preparing or judging a pull request, finding the defect a commit introduced, or pipeline job design; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Git Workflow

## Overview

Two leaves cover version control. One owns the branching policy: trunk-based versus release branches, protection on main, merge queues and CODEOWNERS. The other owns the history itself: atomic commits, message conventions, rebase versus merge, repair and the changelog. Policy first, then the commits that flow through it.

## When to use

- Picking a branching model; setting protection, a merge queue or CODEOWNERS.
- Commit subjects and bodies, Conventional Commits types, splitting with `git add -p`.
- Rebase versus merge, cleaning local history, reverting on shared branches.
- Bisecting history for a breaking commit; generating the changelog.

## When not to use

- Sizing, describing or reviewing a pull request — outside this skill.
- Finding why the code broke; that hunt is a debugging task — outside this skill.
- Pipeline jobs, caches and required checks — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/git-workflow.md` | Branching model and protections | "which branching model" |
| `subskills/commits-history.md` | Commits, history, changelog | "write a commit message" |

## See also

- `subskills/git-workflow.md` — the policy.
- `subskills/commits-history.md` — the history it produces.
