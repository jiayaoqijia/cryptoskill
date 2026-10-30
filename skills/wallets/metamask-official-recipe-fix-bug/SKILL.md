---
name: recipe-fix-bug
description: Execute an explicitly requested fix-bug task using the shared Recipe Cook checklist.
disable-model-invocation: true
maturity: experimental
---

# Fix-bug with runtime proof

Use only when explicitly named by the user or selected workflow. Read the installed `mms-recipe-cook/SKILL.md` as this entry point's declared dependency.

Pass flow `fix-bug`, the unchanged request, any explicit domain/template and the existing task directory when supplied. For a new task, pass authored criteria from the request or available ticket to Cook as separate `--acceptance` values; a hosted task reuses its recorded criteria. Follow Cook's selection rules for a new task; reuse the frozen checklist for an existing task. Do not create a second checklist or infer another skill from metadata.

Cook owns checklist execution and task completion. When it completes, report the outcome and ask what to do next; the usual path is commit plus a Pretty PR from the evidence with `/mms-recipe-pretty-pr <task-dir>`. Cleanup is a separate explicit action.
