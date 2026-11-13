---
name: connection-and-cursor-leaks
domain: software-engineering/connection-and-cursor-leaks
trigger: "Diagnosing a pool that never returns its checked-out items."
anti_trigger: "Not for setting pool sizes from load (that is limits-from-evidence)."
scope: "Pools that never return: leaked connections, cursors, sessions, and handles."
status: seedling
---

# Connection and cursor leaks

## Standard

A pool hands out a resource on request and takes it back when the borrower releases it. A leak is a borrower that never releases — usually an error path: the function that closes the connection on success but returns early on the exception before the close runs. The pool drains as these accumulate, and the error the client sees, "pool exhausted", points at the victim while the cause sits in a call stack that has already returned.

The categorical tell is the curve. A leak under steady load is a staircase: pool usage rises, never returns to baseline, and each step is a leaked instance. Saturation by contrast is a plateau that tracks load — high but flat, returning at night. The staircase demands leak-hunting in code; the plateau demands a size decision; confusing one for the other wastes a day.

## Decision rules

- Sample the pool's checked-out count over time before reading any code.
- Classify the curve: staircase (leak), plateau (saturation), or sawtooth (churn).
- For a leak, capture a stack trace of borrowers at the moment of exhaustion; the holder list names the code paths.
- Audit error paths in the borrowing code — the leak is almost always on the early-return side of an error.
- Check that idle evictors are configured and actually run; a pool without eviction keeps dead connections.
- Record any borrow timeout clients experience as a symptom, not as the pool's setting to tune.

## Procedure

1. Plot checked-out count against time at the pool's own resolution.
2. Classify the curve.
3. On a staircase, capture holder stacks at exhaustion.
4. Read each holding path for the missing release on the error branch.
5. Verify eviction and validation settings are as believed.
6. Record the verdict and the specific code path or size decision.

## Anti-patterns

- Rebuilding the pool as the first response — it resets the staircase and the evidence.
- Blaming the pool's size when the curve is a staircase.
- Reading only the success path of the borrowing code.
- Disabling borrow timeouts to "stop the errors" — it moves the failure to a hang.
- Treating validation queries as a fix for a leak; they keep corpses fresh, not fewer.

## Done checklist

- [ ] Pool curve sampled and classified.
- [ ] Holder stacks captured on exhaustion.
- [ ] Error paths audited in borrowing code.
- [ ] Eviction configuration verified.
- [ ] Verdict recorded: leak path or size decision.
- [ ] Timeout symptom separated from the fixing action.

## Sources

- Connection pool concepts and failure modes: <https://learn.microsoft.com/en-us/azure/data-explorer/>
- JDBC pooling behaviour: <https://docs.oracle.com/en/java/javase/jdbc/>
- Database cursor management: <https://www.postgresql.org/docs/current/sql-close.html>
