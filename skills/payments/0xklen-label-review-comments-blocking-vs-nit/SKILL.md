---
name: label-review-comments-blocking-vs-nit
description: Use when authors cannot tell which review comments must be resolved before merge. Prefix every comment with a severity token and document the legend in the repo.
---

# Label review comments blocking vs nit

An unlabelled comment forces the author to guess intent. Guessing wrong either blocks a merge on a preference or ships a real defect because it looked like a preference.

## Procedure

1. Adopt a fixed token set and put it in `CONTRIBUTING.md`:
   - `blocking:` — must be fixed or answered before merge.
   - `question:` — I may be missing context; answer, do not necessarily change code.
   - `suggestion:` — worth considering, author may decline with a reason.
   - `nit:` — trivial taste, ignore freely.
2. Start every comment with exactly one token, lowercase, followed by a colon and a space. This makes severity greppable and unambiguous.
3. Reserve `blocking:` for defects, security, data loss, or broken contracts. Never mark a naming or formatting preference blocking.
4. Make the merge rule explicit in the repo's PR template: no `blocking:` thread stays unresolved at merge time.
5. After changes land, verify the counts: `gh pr view 482 --json comments | jq -r '.comments[].body' | grep -cE '^(blocking|nit|question|suggestion):'`.
6. When a `suggestion:` is declined, the author replies with the reason, and the thread is resolved rather than left dangling.
7. Re-read your own review before submitting: any comment lacking a token gets one, or gets deleted.

## Pitfalls

- Using "minor" for something that is actually blocking; the author merges and the bug ships.
- Different reviewers using different words (FYI, minor, must-fix) so the legend drifts into meaninglessness.
- Marking a genuine security concern as a `nit:` to avoid seeming harsh.
- A `blocking:` comment with no explanation of what correct looks like, leaving the author stuck.

## Verification

    gh pr view 482 --json comments \
      | jq -r '.comments[].body' \
      | grep -oE '^(blocking|question|suggestion|nit):' | sort | uniq -c

Every comment line must match one of the four tokens. Report the counts by class and confirm zero unresolved `blocking:` threads remain.

## Worked example

Review of a caching PR:
    blocking: stale entries are never evicted, so memory grows unbounded — add a TTL.
    suggestion: consider `functools.lru_cache` here, but the manual dict is fine.
    nit: `cache2` is an unusual name.
The author lowers the TTL to fix the first, replies "keeping the dict for per-key metrics" on the second, and renames on the third. One round-trip, and no ambiguity about what gated the merge.
