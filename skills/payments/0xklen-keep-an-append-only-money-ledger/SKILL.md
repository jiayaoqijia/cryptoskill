---
name: keep-an-append-only-money-ledger
description: Use when money movements must be auditable and reversible. Records every movement as an immutable double-entry post, derives balances by summation, and never mutates a past entry.
---

# Keep an append-only money ledger

Auditability requires that history cannot be rewritten: post immutable entries and derive balances from them. A balance is a cache of a sum, never the source of truth. Corrections are new reversing entries, not edits.

## Procedure

1. Model double entry: every post has debits and credits summing to zero within an entry id.
   `SELECT entry_id FROM post GROUP BY entry_id HAVING SUM(signed_minor) <> 0` must return no rows.
2. Columns: `entry_id`, `posted_at` (UTC), `account_id`, `currency`, `amount_minor` (signed integer), `memo`, and a link to the source event. Grant only `INSERT` on this table — no `UPDATE`, no `DELETE`.
3. Derive an account balance by summing its posts: `SELECT SUM(amount_minor) FROM post WHERE account_id = $1`. Cache it if you must, but the cache is always rebuildable from posts.
4. Corrections: post a reversing entry referencing the original (`reverses_entry_id`), then post the correct entry. The pair nets to zero and the history shows both.
5. Enforce one currency per account so any sum over it is dimensionally valid.
6. Add an idempotency key per source event (`UNIQUE(source_type, source_id)`) so a retried webhook cannot double-post.
7. Stamp `posted_at` from the server clock in UTC and never backdate a new entry to move it between periods; use a period-closing entry instead.
8. Run a nightly check: the sum of all posts per currency is zero (or equals the known external float), and every cached balance matches its recomputed sum.
9. Partition the table by `posted_at` month for query speed while keeping the entries immutable.
10. Keep a rebuildable materialized balance view rather than writing balances back into the post table.

## Pitfalls

- An `UPDATE` to fix a typo destroys the audit trail; reverse and re-post instead.
- A mutable balance column drifts from the posts after a partial failure, and reconciliation cannot tell which is right.
- A floating-point `amount` makes the `SUM() <> 0` check fail on rounding noise.
- Deleting a "test" entry with `DELETE` leaves a gap in the `entry_id` sequence that auditors flag.
- Backdating a correction into the prior period falsifies the close; post it in the current period with a reference.
- No idempotency key: a retried payment webhook double-credits.
- A trigger or ORM hook that "fixes" an entry on insert violates append-only; audit the write path, not just the table grants.

## Verification

    psql -c "SELECT COUNT(*) FROM (SELECT entry_id FROM post GROUP BY entry_id HAVING SUM(amount_minor) <> 0) x"   # expect 0
    psql -c "SELECT SUM(amount_minor) FROM post WHERE currency='USD'"   # equals external float

Report the unbalanced-entry count (must be 0) and the derived-vs-cached balance check.
