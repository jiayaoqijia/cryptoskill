# Portable execution templates

An execution template is a phased Markdown checklist. TASK.md carries the request and required inputs; CHECKLIST.md is the sole step list. Use the same template content and provenance whether invoked by an engineer or another tool.

Complete the work, write the declared outputs, invoke the task marker, and return the outcome. A completion signal does not publish or clean up resources. Publication is a separately invoked workflow. A caller may impose additional requirements through the task contract, but the skill does not detect or branch on the caller's identity.

`recipe-qa` accepts PR, range and daily scopes. PR runtime validation selects `qa/default`; `qa/pr.mobile` and `qa/pr.extension` are explicit `--template` choices. Static Perps review uses the installed `mms-perps-review-pr/SKILL.md` checklist directly and never launches an app. For a frozen source bundle, the parent task registers the shared skill and repository overlay as consecutive child checklists. No duplicate template catalog is required.

Workflow skills require explicit invocation. Descriptions, labels and changed paths only filter compatible content after invocation. `mm-harness` provides portable task-directory and recipe commands; no control-plane installation or configuration is required.
