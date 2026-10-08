---
name: separate-correctness-from-style-in-review
description: Use when a review is mixing bug-hunting with taste and the author cannot tell what actually blocks the merge. Runs correctness first, then style, and only the first pass gates.
---

# Separate correctness from style in a review

A reviewer who interleaves "this variable name is confusing" with "this dereferences a null" teaches the author that both are equal. They are not: one ships a bug, the other ships a nit.

## Procedure

1. Fetch the real merge delta, not the branch tip: `git diff --merge-base origin/main HEAD` or `gh pr diff 482`. Review the lines that will land, not local scratch work.
2. Run pass one — correctness only. For every changed line ask: what input makes this wrong, and does the code handle it? Nothing else belongs in this pass.
3. Label each finding with its class, in the comment text:
   - `bug:` — fails for some input; blocking.
   - `risk:` — correct today, fragile tomorrow; discuss, do not block.
   - `nit:` / `style:` / `optional:` — taste; never blocks.
4. Give every `bug:` a reproduction: the input, expected output, actual output. A finding you cannot reproduce is a style opinion wearing a bug's clothes.
5. Run pass two — style, naming, structure, tests. Batch it into one review comment marked `non-blocking`, so the thread stays about behaviour.
6. Approve only when zero `bug:` items remain and each `risk:` has an owner or a linked follow-up issue.
7. Note which pass each comment came from. A reviewer who cannot say which pass a remark belongs to is guessing.

## Pitfalls

- Phrasing a taste comment as "this is wrong"; the author treats it as a stop-the-line defect and burns a day.
- Debating a helper's name while a panic path sits four lines below, unflagged.
- A whole-file reformat folded into a logic change, so the real delta is invisible in the diff.
- Approving with a `bug:` still open because the author is under deadline pressure.

## Verification

    gh pr diff 482 | grep -nE '^\+.*(panic\(|unwrap\(\)|TODO|FIXME)'
    # Each surviving hit must be addressed or explicitly deferred in a bug:-labelled comment.

Every blocking comment must carry an input that reproduces it. Report: "pass one found 3 correctness findings (1 blocking), pass two batched 11 style items as non-blocking."

## Worked example

A PR adds `GET /reports/{id}`. Pass one: the handler reads `id`, runs `Report.objects.get(pk=id)` with no owner filter, and returns 200 for any valid id — filed as `bug:` with the repro "user B fetches user A's report id, gets 200". Pass two: the local is named `rep` and the JSON keys are camelCase in a snake_case API — batched as one `nit:` comment. The author fixes the authz and merges; the naming lands whenever.
