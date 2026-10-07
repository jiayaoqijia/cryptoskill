# Limits, headers and errors

## The keyless budget

- One budget per client address, shared by every route: **5 units per second, burst 20** (300 per
  minute). An IPv6 address counts by its `/64`.
- A call spends its route's CU ÷ 10 units, at least 1. `GET /chains` spends 1, a pair 2, the screener
  3, wallet rankings 5, candles 6, a token batch 10. `GET /status` and `GET /key` spend nothing.
- The largest keyless page is 50 rows.
- A key only raises limits; nothing requires one. A key goes in `X-API-Key` (or
  `Authorization: Bearer`), never in the query string (`400 key_in_query`). A key that is sent but
  unknown is `401 invalid_api_key`, never a silent downgrade.

## Headers on every limited answer

| Header | Meaning |
|---|---|
| `RateLimit-Policy`, `RateLimit` | IETF draft form: quota, window, and what remains |
| `X-RateLimit-Limit` | calls per second of this route at your pace |
| `X-RateLimit-Remaining` | how many more calls of this route the budget holds now |
| `X-RateLimit-Reset` | seconds until the budget refills |
| `Retry-After` | on `429`: seconds to wait |
| `ETag` | on cacheable answers: send back as `If-None-Match` for a `304` |
| `X-Request-Id` | quote it when reporting a problem; you may send your own (letters, digits, `-`, `_`, up to 64) |

## Backoff recipe

```text
on 429:          sleep(Retry-After); retry
on repeat 429:   sleep(min(60, base * 2^attempt) + random jitter); retry, at most ~5 times
on 503 / 504:    same backoff; the request did nothing
on 400 / 404:    do not retry; fix the input
```

Pace wallet routes at about one call per second and run them one at a time. Prefer a batch route
over many single calls when one exists (`POST /tokens/batch`, `POST /wallets/labels/batch`).

## Error shape

Every non-2xx is RFC 9457 `application/problem+json`:

```json
{"type": "…/errors/chain_not_found", "title": "unknown chain", "status": 404,
 "code": "chain_not_found", "detail": "…", "param": "chain", "request_id": "4f2f…"}
```

| Code | Status | What to do |
|---|---|---|
| `invalid_param` | 400 | fix the parameter named in `param` |
| `key_in_query` | 400 | move the key to the `X-API-Key` header |
| `invalid_api_key` | 401 | fix the key, or send none |
| `plan_required` | 403 | the route needs a higher plan |
| `chain_not_found` | 404 | read `GET /chains` for the current roster |
| `not_found` | 404 | check the chain and the address; also returned for a route this host does not serve yet |
| `rate_limited` | 429 | wait `Retry-After` |
| `internal` | 500 | retry once later; report with `request_id` |
| `upstream_unavailable` | 503 | retry with backoff |
| `upstream_timeout` | 504 | retry with backoff |

The code set is closed within v1. Tolerate unknown response fields and unknown enum values: the
contract grows additively.
