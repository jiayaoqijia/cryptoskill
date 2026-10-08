---
name: build-a-service-error-taxonomy
description: Use when every failure looks identical in the logs — builds a closed error taxonomy with stable codes, a retryable flag, transport mapping and an owner per class.
---

# Build a service error taxonomy

Untyped errors force every handler to guess whether to retry. A closed taxonomy with a stable code, a retryable flag and an owner per class turns error handling into a lookup instead of a judgement call.

## Procedure

1. Enumerate failure modes from the caller's point of view, not from the stack. Start with six classes: `INVALID` (bad input, never retry), `NOTFOUND`, `CONFLICT` (optimistic-lock failure, retry after refetch), `DEPENDENCY` (transient upstream, retry with backoff), `OVERLOAD` (retry later, honour Retry-After), `INTERNAL` (bug, do not retry).

2. Give each a stable string code that never changes once shipped: `CHECKOUT_CARD_DECLINED`, not `Err42`. Codes are part of the public API contract.

3. Define each error as a fixed record rather than a class hierarchy:
       type Error struct { Code string; Class Class; Retryable bool; HTTP int; Owner string }
       var CardDeclined = Error{"CHECKOUT_CARD_DECLINED", Invalid, false, 402, "payments"}

4. Map class to transport in exactly one place: INVALID→400/422, NOTFOUND→404, CONFLICT→409, DEPENDENCY→502, OVERLOAD→503 with `Retry-After`, INTERNAL→500. Never hand-write a status code at a call site.

5. Derive the client contract from `Retryable`. Only `Retryable=true` errors may be retried, and only with jittered backoff. A 500 caused by a bug must not be retried — retrying a nil-dereference triples load during an incident.

6. Assign an owner team per code and export `errors_total{code,class,owner}` so burn is attributed to a team, not to "the service".

7. Wrap at every component boundary, preserving the cause internally while keeping internals off the wire: Go `fmt.Errorf("...: %w", err)` with `errors.As`, Python `raise ApiError(...) from e`.

8. Freeze the list: a lint test asserts every raised code exists in `errors.yaml` and every entry in `errors.yaml` is raised somewhere.

## Pitfalls

- Retrying an `INTERNAL` error. Deterministic failures are amplified by retry, not cured.
- Leaking internals in the wire message (`pq: deadlock detected on relation orders`) — useful in the log, a security and coupling problem in the API.
- Adding a code with no owner, so its alerts page nobody and its dashboard has no reader.
- One giant `INTERNAL` bucket that swallows a real DEPENDENCY spike and hides an outage behind a 500 count.

## Verification

    python tools/lint_errors.py     # taxonomy: 24 codes, 0 unowned, 0 orphans
    grep -rn 'return.*NewError' src | grep -v 'errors\.' && echo UNCLASSIFIED

Report: N codes mapped to class/retryable/HTTP/owner, a clean lint run, and the `errors_total` dashboard attributing last week's burn to a named team.
