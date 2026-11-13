---
name: value-record
domain: prompt-engineering/value-record
trigger: "Keeping the per-request ledger that turns limit economy into a discipline."
anti_trigger: "Not for infrastructure metering, and not for prompt libraries."
scope: "The per-request ledger: what each request was for, what it returned, what remains."
status: seedling
---

# Value record

## Standard

The ledger is the skill's memory and its enforcement. One line per request: what it was for, what it packed, what came back, and what allowance remains. Under a request-binding regime the ledger carries the economy's three live numbers — requests spent, requests remaining, requests-per-answer ratio — and every habit this skill teaches is measured by what the ledger shows next session.

Its second function is reuse: stored with its question and pack list, a response becomes an asset the preparation leaf draws on, converting one spent request into many future served needs. A ledger that stores only answers without questions and purposes renames files; one that stores the full tuple lets the operator reconstruct why a request was worth its cost, and whether a similar need should be served from disk rather than re-spent.

Primary sources: <https://12factor.net/> and <https://osf.io/prereg/>.

## Decision rules

- One line per request: purpose, pack list, response summary, remaining allowance.
- Update the remainder after every spend; the number on paper must match the number in the world.
- Store question and pack with each response for reuse.
- Compute and track the requests-per-answer ratio every session.
- Reconcile the ledger count against the provider's usage page when one exists.
- Review weekly: highest-burn patterns, ledger-served needs, ratio trend.

## Procedure

1. Open the session with the allowance figure from the provider's page, dated.
2. Log each request at send time, not from memory at day's end.
3. Fill in the response summary and linkage on receipt.
4. Update the remainder immediately.
5. At session end, compute the ratio and the ledger-served count.
6. At week's end, reconcile with the provider meter and review the pattern list.

## Anti-patterns

- Logging from memory, which drops requests and corrupts the remainder.
- Storing responses without questions and pack lists.
- A remainder that drifts from the provider's count.
- No session-end ratio computation, so the habit never gets measured.
- Treating the ledger as an archive rather than an economy's accounts.

## Done checklist

- [ ] Opened with a dated allowance figure.
- [ ] Per-request lines written at send time.
- [ ] Responses stored question-first.
- [ ] Remainder updated every spend.
- [ ] Session ratio and served count computed.
- [ ] Weekly reconciliation and review done.

## Sources

- The twelve-factor app: <https://12factor.net/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
