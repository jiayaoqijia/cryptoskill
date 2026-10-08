---
name: write-a-memory-entry-that-ages-well
description: Use when storing a fact that must stay useful months later. Writes it with a date, scope, source, and expiry so a future reader can trust or discard it.
---

# Write a Memory Entry That Ages Well

A bare fact rots: with no date or scope, a later reader cannot tell if it is current. An entry that ages well carries its own provenance so it can be believed or dropped without re-deriving.

## Procedure

1. State the fact as a key and a value, one line: `prod-db-host = prod-2.cluster.internal`.
2. Date it: `2026-10-08`.
3. Cite the source: `(aws rds describe-db-instances --db-instance-identifier prod)`.
4. Scope it: which environment, account, or project the fact applies to — an unscoped fact gets misapplied.
5. Add an expiry when the fact decays on its own: `expires: 2026-12-01`, or `expires: never` for stables.
6. Record the check command, so a future reader can re-confirm in one line instead of guessing.
7. Keep one fact per entry; bundling three facts makes each un-prunable on its own.
8. Avoid relative wording ("currently", "recently") — it means nothing to a reader six months later.
9. Write the *observed* value, not an inferred one; inference goes in a separate decision note.
10. Re-read the entry as a stranger would, and fix anything you would have to ask about.

## Pitfalls

- Storing a value with no date, so a reader cannot tell a live fact from a stale one.
- Using "currently" or "now", which reads as true forever and is false within a day.
- Omitting the source, so re-confirming means re-discovering the whole chain.
- Bundling several facts in one line, so pruning one forces keeping all.
- Writing an environment-scoped value as global, so it gets applied in the wrong account.

- Writing a fact that is already inferable, adding a line to maintain for no gain.
- Copying a value into memory without its check command, so it cannot be re-confirmed cheaply.
- Storing the source as a bare tool name, which does not say which arguments produced the value.

## Verification

    grep -E "^[a-z-]+ = .*[0-9]{4}-[0-9]{2}-[0-9]{2}.*\(" ~/.hermes/memories/*.md | wc -l
    # passes when every marked entry carries all three of value, date, and source

Report to the user: the entry written, its key, date, source, scope, and expiry.
