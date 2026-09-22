---
name: check-nesting
description: Audit a React Native component for unnecessary wrapper nesting and suggest flattening opportunities. Also flags non-interactive containers missing accessible={false}. Use when reviewing or generating components to reduce native view depth and accessibility node count.
---

## When To Use

- Reviewing or authoring a React Native component and suspecting unnecessary layout wrappers
- Reducing native view depth to improve rendering performance
- Flagging non-interactive containers that are missing `accessible={false}` to lower accessibility node count
- Running a broad audit across a folder or the entire project

## Workflow

See the repo overlay for the full step-by-step playbook (locate files → identify patterns A–F → format findings → ask before fixing → verify tests → open PR → risk report). At a high level:

1. Locate the target file(s) based on user input (path, component name, folder, `--all`, or git diff)
2. Identify removable wrappers (Patterns A–E) and accessibility gaps (Pattern F)
3. Report findings grouped by file with a summary table
4. Ask the user whether to fix all, fix one by one, or just report
5. If fixing: apply edits, run tests per file, then open a PR if requested
