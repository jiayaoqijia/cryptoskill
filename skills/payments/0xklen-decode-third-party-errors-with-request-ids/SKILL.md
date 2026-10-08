---
name: decode-third-party-errors-with-request-ids
description: Use when an API call fails and support must act. Capture the provider's request id, the exact request, and the raw error body so the ticket is actionable.
---

# Decode third-party errors with request ids

"No way to reproduce" is what a support ticket says when it lacks the provider's request id.
Capture the id, the request, and the raw body the moment a call fails.

## Procedure

1. Read the request id from the response header on every call: `x-request-id`, `x-amzn-RequestId`, `cf-ray`.
2. Log it with the failure:
   ```python
   rid = r.headers.get("x-request-id")
   log.error("call failed rid=%s status=%s url=%s", rid, r.status_code, r.url)
   ```
3. Capture the raw body before parsing; error formats vary (`{"error": {...}}`, `{"message": "..."}`, plain text):
   ```python
   raw = r.text[:2000]
   ```
4. Redact secrets before logging: strip `Authorization`, `api_key`, and cookies.
5. Put status, request-id, method, and a body snippet into the raised exception — no query secrets.
6. Only open a support ticket with the request id and a UTC timestamp; "it failed" is not a report.
7. Keep a small ring buffer of the last N requests for postmortem context.

## Pitfalls

- Logging the full URL leaks API keys that are query params; redact the query string.
- Each retry has a different request id; log the id of the attempt that finally failed.
- Truncating the body too early hides the field that explains the error.
- Local clock skew makes the timestamp useless to support; use UTC with an offset.
- Providers may return the id only on 5xx, not 4xx — scrape both headers and body.

## Verification

    grep 'rid=' run.log | tail -1
    # rid=01HZ... status=503 url=/v1/items

Report: "Support ticket carries request-id 01HZ..., status 503, timestamp 2026-10-08T...Z, body 'upstream timeout'."
