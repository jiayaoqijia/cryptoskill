---
name: record-and-replay-a-failing-interaction
description: Use when a bug depends on live network calls, a third-party API, or a user session that is hard to trigger. Captures the real traffic once and replays it deterministically forever after.
---

# Record and Replay a Failing Interaction

Live dependencies are the enemy of reproducibility: the API changes, the session expires, the rate limit trips. Capture one real failing exchange to disk, then debug offline against the frozen bytes.

## Procedure

1. Put a recording proxy in front of the client: `mitmproxy -w repro/session.flow` or `mitmproxy --mode reverse:https://api.example.com`.
2. Point the app at the proxy (`HTTPS_PROXY=http://127.0.0.1:8080`) and generate the failing interaction exactly once.
3. For a specific bug, mark the flow: press `m` in mitmproxy or add a comment, so the interesting exchange is findable by filter.
4. Verify the capture contains the full request *and* response, including headers and body: `mitmdump -nr repro/session.flow | head`.
5. Redact secrets before committing — auth headers, cookies, `Set-Cookie` — with `mitmdump -nr repro/session.flow -w repro/redacted.flow --set 'modify_body=...'` or a small script.
6. Replay offline: `mitmdump -nr repro/redacted.flow --server-replay-header-ignored '*'`, or use a cassette layer (`vcrpy`, `nock`, `POLYFILL` HTTP recorders) so the test needs no network.
7. Confirm the app fails against the frozen interaction the same way it did live. If it passes, the difference is time, auth, or an upstream you did not capture.
8. Commit the cassette with the failing test from `write-a-failing-test-before-the-fix`.
9. Re-run the replayed test in CI with no network namespace; if it needs egress, the cassette is incomplete.
10. Fix the code against the cassette, then re-record once against the live API to confirm the fix holds on real bytes.

## Pitfalls

- Capturing only the request; the interesting bug lives in a response header or a body the client mis-parsed.
- Committing real credentials, session cookies, or PII into the cassette.
- A cassette that expires because it embeds a timestamp or nonce the server later rejects.
- Replay matching on the full URL querystring, so any ordering change makes the cassette miss.
- Recording against the mock and thinking you recorded the real API.
- Forgetting TLS: without trusting the mitmproxy CA, the client fails to connect and you capture nothing.

## Verification

    mitmdump -nr repro/redacted.flow 2>&1 | grep -c 'Response'      # > 0 means a response is present
    grep -riE 'authorization|set-cookie|bearer ' repro/redacted.flow && echo "SECRETS PRESENT" || echo "clean"
    # passes when responses exist and no credential strings remain in the cassette

Report to the user: the cassette path, the count of request/response pairs, and confirmation the app reproduces the failure offline against it.
