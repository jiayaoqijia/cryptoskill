---
name: review-sql-construction-in-the-diff
description: Use when a PR builds SQL by string interpolation or adds a query that could be injected. Sweeps the diff for concatenated SQL and requires parameter binding before approving.
---

# Review SQL construction in the diff

Any query built by concatenating user-controlled values is an injection waiting for the right input. In review, the question is not "is this string safe?" but "is this string built from parameters at all?"

## Procedure

1. Sweep the added lines for query construction: `gh pr diff 482 | grep -nE '^\+.*(SELECT|INSERT|UPDATE|DELETE|WHERE).*(\+|\$\{|%s|f\"|\.format)'`.
2. For every hit, check the parameters are bound, not interpolated. Safe:
       cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
       db.query("SELECT * FROM orders WHERE id = :id", { "id": order_id })
   Unsafe — string interpolation of `email` on the right side of a f-string.
3. Reject identifiers (table names, column names, `ORDER BY` fields) placed by interpolation too — they cannot be parameterized and must be validated against an allowlist of known column names.
4. Check the ORM escape hatch: raw fragments in Django (`RawSQL`, `.extra`), SQLAlchemy `text()` with an f-string, Prisma `$queryRawUnsafe`. Each needs a parameter argument.
5. Look for secondary injection surfaces: `LIKE` patterns where `%` and `_` in user input should be escaped, and `IN (...)` built by joining a list.
6. For stored or admin-only paths, do not downgrade the finding — a compromised admin token still exfiltrates.
7. Run the project's scanner on the diff and reconcile: `semgrep --config p/sql-injection <changed-files>`.

## Pitfalls

- Parameterizing the value but concatenating the column name from a request parameter.
- An ORM's "raw" method that takes a string and a params dict; passing the whole query as one string defeats the binding.
- Trusting a value because it "comes from our own database" — second-order injection stores the payload in one row and executes it in another query.
- A `%` in a `LIKE` pattern treated as literal, so a user can match unintended rows.

## Verification

    gh pr diff 482 | grep -nE '^\+.*(execute|query|text|raw)[^\n]*(f"|\+|%s)'
    semgrep --config p/sql-injection --error path/to/changed_file.py

A pass has zero interpolated query-construction hits and a clean semgrep run. Report every hit, the binding used to fix it, and any identifier placed by allowlist.

## Worked example

Added line:
    db.execute(f"SELECT * FROM accounts WHERE name = '{name}'")
grep flags the f-string. The fix binds the value:
    db.execute("SELECT * FROM accounts WHERE name = :name", {"name": name})
The sort column still arrives from the request, so it is validated against `{'name', 'created_at'}` before it is placed in the query text.
