---
name: document-an-api-endpoint-with-a-runnable-example
description: Use when writing reference docs for an HTTP API endpoint. Specifies method, path, parameters, a copy-pasteable request, a real response, and each error with its fix.
---

# Document an API Endpoint with a Runnable Example

API docs are read by someone writing a client under deadline. Give them a request they can paste into curl and the exact response, then the errors.

## Procedure

1. Open with the method and path in a code span: `POST /v1/invoices`. State the purpose in one sentence.
2. Give an auth line: required scopes and header, e.g. `Authorization: Bearer $ACME_TOKEN`, scope `invoices:write`.
3. List path, query, and body parameters in a table with name, type, required, and default. Mark enum values exhaustively: status in {draft, open, paid, void}.
4. Provide a runnable curl example with real-looking values and the token in a variable so the reader substitutes one thing:
   `curl -sS -X POST https://api.acme.dev/v1/invoices -H "Authorization: Bearer $ACME_TOKEN" -d '{"amount_cents":500,"currency":"usd"}'`
5. Show the actual JSON response with a 200, including field types. Do not hand-wave with an empty object.
6. Document every error the endpoint can return: code, HTTP status, meaning, and the fix. For 409 conflict_idempotency, tell the caller to reuse the same Idempotency-Key or fetch the existing resource.
7. Note rate limits and the `Retry-After` header value the endpoint sends.
8. State idempotency behaviour explicitly: which key header, and the retention window (e.g. 24h).
9. Add one worked error example showing the fix applied.
10. Document pagination if the endpoint lists: the cursor field, the page size limit, and the parameter to advance.
11. Keep the request and response in a consistent order so a reader scans top-to-bottom.
12. Give a timestamp and timezone convention for any date field (`ISO 8601, UTC`).

## Pitfalls

- A request example that omits the auth header, so the first copy-paste returns 401.
- Showing only the happy path response; callers then mishandle the 4xx cases.
- Parameter tables that mark everything optional when the server rejects missing fields.
- Field descriptions that restate the name, such as "amount: the amount".
- Documenting the success status only, hiding that the same verb returns 202 when queued.
- A pagination note that omits the maximum page size, so callers guess and get truncated results.
- Amounts shown as floats where the field is integer minor units, causing rounding bugs downstream.

## Verification

    curl -sS -o /dev/null -w '%{http_code}\n' -X POST "$BASE/v1/invoices" -H "Authorization: Bearer $ACME_TOKEN" -d '{}'
    # run against staging; the code must match the documented error for that input

Run every documented example against staging and confirm status codes and response shapes match the docs exactly.
