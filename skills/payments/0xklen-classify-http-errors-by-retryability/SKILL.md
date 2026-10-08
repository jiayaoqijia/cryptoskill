---
name: classify-http-errors-by-retryability
description: Use when writing the error path of an API client. Map status codes into a small taxonomy — retry, refresh, fail-fast, conflict — so each class gets exactly one correct handler.
---

# Classify HTTP errors by retryability

A single `except Exception: retry` treats a validation error, an expired token, and an upstream
outage identically. Split them once and each class gets the right response.

## Procedure

1. Define the classes in code, not in prose:
   ```python
   RETRY    = {408, 429, 500, 502, 503, 504}
   AUTH     = {401, 403}
   CLIENT   = {400, 404, 405, 410, 422}
   CONFLICT = {409}
   ```
2. `RETRY`: back off with jitter and retry a bounded number of times.
3. `AUTH` 401: refresh the token once and retry; a second 401 is fail-fast. 403 is a scope problem and is never retryable.
4. `CLIENT`: raise immediately; retrying a 400 just repeats a bad request.
5. `CONFLICT` 409: fetch current state and reconcile, do not blindly retry.
6. 3xx: follow only configured redirects; a 301/302 on a POST can silently drop the body and change the method to GET.
7. Log status, request-id, and the parsed error body for every non-2xx at the boundary.

## Pitfalls

- Treating all 4xx as retryable turns a validation bug into infinite load.
- 401 and 403 look alike but a fresh token never fixes 403.
- Some APIs return 200 with an error object in the body; check the body, not only the code.
- 429 without reading `Retry-After` retries too early.
- A 302 on a POST often drops the body; verify the final request the server saw.

## Verification

    python -c "from client import classify; print(classify(503), classify(422), classify(409))"
    # ('retry', 'client', 'conflict')

Report the class counts from a run: "1,240 requests: 12 retries (all 503), 0 unclassified."
