---
name: fix-sql-injection-with-parameterised-queries
description: Use when SQL is built by concatenating or formatting user input. Finds the sinks, converts them to bound parameters, and proves the injection is closed with a live payload.
---

# Fix SQL injection with parameterised queries

String-built SQL is the dominant injection sink because it is easy to write and hard to spot in
review. The fix is never escaping — it is separating the query text from the data so the driver
sends them through distinct channels.

## Procedure

1. Find candidate sinks — f-strings, `%`, `+`, `.format`, and template literals next to SQL verbs:

       rg -n -i "(select|insert|update|delete|where).*(f\"|f'|%s|\+|\.format\(|\$\{)" src/ | tee /tmp/sqli.txt

2. Run a rule-based scanner for a first cut:

       semgrep --config p/python --config p/sql-injection src/   # swap p/<lang> per stack

3. Convert each sink to a bound parameter. The placeholder style follows the driver:

       # psycopg / psycopg2 (Python) — note the comma, params as a tuple
       cur.execute("SELECT * FROM users WHERE email = %s AND tenant = %s", (email, tenant))
       # database/sql (Go)
       row := db.QueryRowContext(ctx, "SELECT * FROM users WHERE email = ?", email)
       # node-postgres (JS)
       await pool.query('SELECT * FROM users WHERE email = $1', [email])

4. Identifiers cannot be bound (table/column names, `ORDER BY` direction). Allowlist them against
   a fixed set rather than interpolating:

       ORDER_COLS = {"created_at", "id", "email"}
       if sort not in ORDER_COLS:
           raise ValueError("bad sort column")
       sql = f"SELECT * FROM users ORDER BY {sort}"

5. Fix `LIKE` and `IN` carefully: `IN` needs one placeholder per element; `LIKE` escape `%` and `_`
   in the user value even when bound.

6. Replace raw SQL with an ORM for simple CRUD; keep bound SQL for anything it cannot express.

7. Prove the fix. Replay a payload against the patched endpoint and expect a normal empty result,
   not a 500 with a syntax error:

       curl -s "https://app.example.com/api/users?email=' OR '1'='1" | head -c 200

8. Add a regression test with the payload `' OR '1'='1` and a test that asserts a syntax-error 500
   no longer appears.

## Pitfalls

- Escaping quotes by hand is bypassable; only bound parameters are safe.
- `sqlalchemy.text()` does not bind unless you pass a params dict — interpolated `text()` is still
  injectable.
- `cursor.execute("... %s" % x)` with one arg looks bound but the `%s` was consumed by Python.
- Stored procedures that internally concatenate their own `@sql` parameter reintroduce the bug.
- Second-order injection: a value stored cleanly is concatenated later by a reporting query; grep
  the whole codebase, not just request handlers.
- ORMs expose `.raw()` / `.extra(where=[...])` escape hatches that bypass parameterisation.

## Verification

    semgrep --config p/sql-injection src/ 2>&1 | rg -c "sql-injection" ; \
    curl -s "https://app.example.com/api/users?email=' OR '1'='1" -o /dev/null -w '%{http_code}\n'

Pass: semgrep reports zero sql-injection findings for the changed files and the payload returns
200 with an empty set (not 500). Report the sinks converted, the files touched, and the residual
allowlisted identifiers.
