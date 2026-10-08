---
name: context-budgeting
description: Use when a task will read many files, long logs, or large payloads. Filters before loading and offloads to disk so the working window keeps room for reasoning.
---

# Context Budgeting

Context is the agent's scarcest resource; every dumped log evicts reasoning. Treat the window as a budget: filter before reading, offload bulk to disk, and summarize progressively.

## Procedure

1. Set a budget at the start: aim to keep free window above roughly half the total. If a task needs more, the output goes to a file, not into the conversation.
2. Never read a directory wholesale. List and filter first: search for the pattern, get file paths, then read only matching files.
3. Read windows, not whole files, for anything large: use a line range (`offset`/`limit`) and expand only around the relevant region. A 5,000-line file rarely needs more than the 60 lines around the target.
4. For logs and command output, pipe through a filter before it lands: `grep -n "ERROR" app.log | head -50`, `awk '$9==500' access.log | wc -l`.
5. Batch many-item extraction into a script that appends to a workspace file (`data/rows.jsonl`), then read back and aggregate with code — never accumulate 200 results in the window.
6. When the window is filling, write a running summary to `notes/context-summary.md` capturing: goal, decisions, open questions, and the next command. Then continue from the file, not from memory.
7. Re-read a file after it may have changed; do not rely on an earlier read whose content is already summarized away.
8. Keep raw tool output out of the window when it is a step, not a result — only the reduction needs to be seen.
9. Set the budget in real units: "at most 25 files read and 4 large outputs", written before starting.
10. When a tool can return a summary or a count instead of the rows, take the summary and fetch rows only for the ones you will act on.
11. Delete or truncate stale workspace dumps you have already reduced, so later reads do not re-load dead weight.

## Pitfalls

- Pasting a 5MB JSON body into the conversation to grep it by eye.
- Reading all 40 files in `src/` because "I might need them", when 3 import the changed symbol.
- Letting a long-running loop print every item so the window drowns before the run finishes.
- Summarizing to a file and then never reading it back, so the summary is dead weight.
- Re-reading an unchanged file each turn out of habit, burning the budget on constants.
- Loading a whole 2,000-line file to read 30 lines in the middle, when offset/limit would do.
- Letting a helper print every row so the window fills before the reduction is written to disk.

## Verification

    wc -l notes/context-summary.md data/rows.jsonl 2>/dev/null
    # passes when bulk data lives in files and only reductions/conclusions appear inline

Report to the user: files loaded vs skipped, the workspace files holding bulk data, and roughly how much of the window remained free at the end.
