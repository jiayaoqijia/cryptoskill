---
name: record-api-calls-for-replay
description: Use when building tests against a live API. Record real request/response pairs once, then replay them offline so tests are deterministic and need no network.
---

# Record API calls for replay

Tests that hit a live API are slow, flaky, and rate-limited. Record the exchanges once, scrub
the secrets, and replay them so the suite is deterministic and offline.

## Procedure

1. Record with a cassette library (`vcrpy` for Python, `nock` for Node, `VCR` for Ruby) or a mitm proxy: `--record-mode=once` first run, `none` afterwards.
2. Filter secrets before writing:
   ```python
   def before_record(r):
       r["headers"].pop("Authorization", None)
       return r
   ```
3. Commit cassettes so CI runs offline and deterministically.
4. Normalise volatile values (timestamps, ids, request-ids) with match rules so replays are not brittle.
5. Match on method plus path plus query — not full headers — so a header tweak does not break replay.
6. Re-record when the API actually changes; a stale cassette hides a live breaking change.
7. Record the error responses too: capture a 429 and a 500 deliberately to exercise the retry path.

## Pitfalls

- Cassettes containing live keys leak credentials into version control.
- Full-header matching breaks on changing date/user-agent; match narrowly.
- A one-time cassette validates code against a shape the live API no longer serves.
- Exact-body matching fails when the request carries a random idempotency key; scrub it in the matcher.
- Recording a whole large run bloats the repo; record only the fixtures the tests use.

## Verification

    pytest -q --record-mode=none       # passes with the network disabled

Report: "34 cassettes replay offline; 2 recorded 429s exercise the retry path."
