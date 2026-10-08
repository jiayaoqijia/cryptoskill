---
name: resumable-handoff-capsule
description: Use when a task must pause, be handed to another agent, or span a context window boundary. Writes a machine-readable capsule so the next actor resumes without re-deriving anything.
---

# Resumable Handoff Capsule

A crisp status paragraph is not a handoff. A capsule lets a different agent, or you after a compaction, pick up the exact next action with zero re-discovery.

## Procedure

1. Choose the path deterministically: `.hermes/handoff/<task-slug>.md`. One file per task, overwritten rather than appended, so it never goes stale in pieces.
2. Fill the capsule with these fixed keys, one per line, no prose paragraphs:
   - `task:` the original ask in the user's own words.
   - `status:` one of `blocked`, `in-progress`, `ready-to-verify`, `done`.
   - `done:` bullet list of completed units, each with the command that proved it.
   - `next:` the single next action as a runnable command, not a description.
   - `blocker:` what stops progress, or `none`.
   - `files:` paths touched, with `git status --porcelain` output pasted verbatim.
   - `resume:` the exact first command the next actor runs.
   - `verified:` what is confirmed vs assumed.
3. Make `resume:` self-contained: it must work from a cold shell in the repo root, e.g. `git checkout feat/api && pytest tests/test_api.py -q`.
4. Record unresolved questions explicitly so the next actor does not silently guess: `open-question: <...>`.
5. Store any large intermediate output in `notes/<task-slug>/` and reference paths, never inline blobs.
6. Before writing, re-run `git status --porcelain` and paste the true output; do not describe it.
7. Commit nothing on the user's behalf; a capsule is a working note, not a deliverable, unless the task says otherwise.
8. On resume, read the capsule, run its `resume:` command, then reconcile as in `reconcile-state-before-acting` before editing.

## Pitfalls

- Writing "continue the refactor" as `next:` — a description is not resumable.
- Letting `files:` claim a change that `git status` does not show, so the next actor edits a clean tree.
- Overwriting the capsule mid-task and losing the record of what was already verified.
- Recording a `resume:` command with placeholder paths like `/path/to/repo`.
- Omitting the blocker, so the next actor re-hits the same wall.

## Verification

    sed -n '1,40p' .hermes/handoff/<task-slug>.md
    # passes when every key is present and `resume:` runs clean from repo root

Report to the user: the capsule path and its `status` and `next` values verbatim.
