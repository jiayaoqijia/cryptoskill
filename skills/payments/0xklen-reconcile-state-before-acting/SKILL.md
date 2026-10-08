---
name: reconcile-state-before-acting
description: Use when resuming a task, inheriting another agent's work, or opening a repo after a gap. Establishes observed reality before any mutation, because memory and handoff notes drift from disk.
---

# Reconcile State Before Acting

Every assumption you carry in from memory, a summary, or a handoff is a guess until a command confirms it. Reconcile observed state against expected state, write down the delta, and only then change anything.

## Procedure

1. Capture expected state first, in one line per claim. Example: "branch is clean", "file `src/Api.py` exists and matches HEAD", "no server on port 8080". If you cannot state the expectation, you do not have one and must not assume it.
2. Read actual repository state before touching files:
   `git status --porcelain=v1` and `git log --oneline -5` and `git stash list`.
3. Check for work in flight that a summary would not mention: open editors' lock files, `.git/MERGE_HEAD` (mid-merge), `.git/rebase-merge` (mid-rebase), and `ls .git/*.lock`.
4. Check process and port reality when the task involves a running service: `pgrep -fl node`, `lsof -nP -iTCP:8080 -sTCP:LISTEN`.
5. Inspect the artefact you were told exists: `ls -la <path>` and `wc -l <path>`. Absence is a finding, not an error to route around.
6. Compute the delta between steps 1 and 2-5 and write it to `notes/reconcile-<task>.md` as three lists: confirmed, contradicted, unknown.
7. Resolve every `contradicted` entry before proceeding. If you cannot, stop and report it rather than editing on top of it.
8. Only after the lists are stable, begin the actual task, and re-run step 2 immediately before any commit or destructive step.
9. Record the facts you will re-assert at the end so drift is detectable: the HEAD sha (`git rev-parse --short HEAD`), the line count of the file you will edit, and the listening port.
10. Clear or account for stale locks from an interrupted run (`.terraform.tfstate.lock.info`, `*.pid`, `.git/index.lock`) before starting; a stale lock imitates a live process.
11. Capture environment coordinates (`git rev-parse --abbrev-ref HEAD`, `python --version`, `pwd`) and compare them to what the task assumes.

## Pitfalls

- Trusting a handoff note that says "tests pass" when the working tree has uncommitted edits that were never run.
- Assuming a cached directory listing or a prior `ls` output is still true after another process ran.
- Reading a file's content from memory of an earlier read instead of re-reading it before an edit.
- Editing on top of a dirty tree and then committing unrelated changes you did not author.
- Treating a port or process as free because it was free five minutes ago.
- Reconciling file contents but not the branch, so edits land on `main` instead of the feature branch.
- Trusting a green CI badge from an older commit as evidence about the current tree.

## Verification

    git status --porcelain=v1
    # passes when it prints only files you intended to change, or nothing

Report to the user as an observation: the reconcile note path, plus the counts of confirmed/contradicted/unknown, and any contradicted claim you resolved or escalated.
