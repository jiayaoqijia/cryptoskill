# Mock Network Requests

Use `mm mock-network` to stub or record network requests during an active session. Prefer this over raw CDP when you need deterministic API responses or want to read what the Extension sent. To only watch traffic, use `mm network` ([logs-and-network.md](logs-and-network.md)).

## Contents

- [Rules](#rules)
- [Where rules apply](#where-rules-apply)
- [Rule Shape](#rule-shape)
- [Record request bodies](#record-request-bodies)
- [Examples](#examples)
- [Verification Pattern](#verification-pattern)
- [In mm run-steps](#in-mm-run-steps)

## Rules

- Run `mm launch` first. Requests during `mm launch` itself cannot be mocked.
- Add rules **before** the UI action that triggers the request. Data the Extension already fetched stays cached; after you add a rule for loaded data, run `mm reload`.
- `mm cleanup` removes all rules; `mm mock-network clear` removes rules and request history without ending the session.
- Unmatched requests on a mocked origin continue unchanged and are recorded as misses.
- A rule only works if the Extension makes the request. Find the exact URL first with `mm network --url <text>`. In the e2e fixture Basic functionality is off, so many MetaMask API calls never happen; the service worker still calls `token.api.cx.metamask.io`, `geolocation.dev-api.cx.metamask.io`, and during a send `security-alerts.api.cx.metamask.io/validate/0x539`.
- `mm mock-network requests` shows URLs as sent, API keys included (for example Infura project IDs). `mm network` redacts them. Redact keys before you paste `requests` output anywhere.

## Where rules apply

Rules match requests from pages (`page`), the background service worker (`sw`), the MV3 offscreen document (`offscreen`) and the snaps iframes it runs (`iframe`). `add` and `list` report where they intercept now:

```json
{"contexts":["page","sw","offscreen"],"pending":["iframe"]}
```

- `pending: ["iframe"]` is normal while no snap runs. In the e2e fixture snaps run only after you turn on Basic functionality (Settings > Privacy, `mm click --testid basic-functionality-toggle`); `list` then shows `"contexts":["page","sw","offscreen","iframe"],"pending":[]`. A rule added before a snap starts still covers it.
- `offscreen` in `pending` means the offscreen document is not attached; its requests and its snaps' requests are then not mocked.
- Each record in `requests` has `context` (`page`, `sw`, `offscreen` or `iframe`) and `"serviceWorker": true` for the background worker.
- A snap's JSON `POST` is preceded by a CORS preflight (`OPTIONS`). For a rule with a `response` it is answered for you and never recorded.

## Rule Shape

```json
{
  "id": "token-prices",
  "method": "GET",
  "url": "https://price.api.metamask.io/v1/**",
  "response": {
    "status": 200,
    "json": { "ethereum": { "usd": 1234.56 } }
  }
}
```

A rule needs `id`, `method`, `url`, and `response`, `record` or both.

| Field              | Description                                                                       |
| ------------------ | --------------------------------------------------------------------------------- |
| `id`               | Stable identifier. Same `id` replaces the previous rule.                          |
| `method`           | HTTP method; normalized to uppercase.                                             |
| `url`              | Absolute URL or glob. `*` matches within a segment; `**` matches any path suffix. |
| `response`         | Mocked response. Leave it out (with `record`) to forward the real request unchanged and only record it. |
| `response.status`  | Optional HTTP status; defaults to `200`.                                          |
| `response.json`    | JSON response payload.                                                            |
| `response.body`    | Text response payload. Use either `json` or `body`.                               |
| `response.headers` | Optional. JSON/text defaults include `access-control-allow-origin: *`.            |
| `record`           | Optional. `{"body":true}` and/or `{"headers":true}`; see below.                   |

## Record request bodies

Add `record` to a rule to keep the body and/or headers of each request it matches, and read them with `--bodies`:

```bash
mm mock-network add '{"id":"blockaid","method":"POST","url":"https://security-alerts.api.cx.metamask.io/validate/**","response":{"status":201,"json":{"block":1,"result_type":"Malicious","reason":"transfer_farming","description":"","features":["Interaction with a known malicious address"]}},"record":{"body":true}}'
# ...open a send up to the review page...
mm mock-network requests --url validate --bodies
```

```json
{"method":"POST","url":"https://security-alerts.api.cx.metamask.io/validate/0x539","matched":true,"ruleId":"blockaid","status":201,"context":"sw","serviceWorker":true,"body":{"type":"json","size":285,"value":{"jsonrpc":"2.0","method":"eth_sendTransaction","origin":"metamask","params":[{"from":"0x5cfe…","to":"0x2f31…","value":"0x2386f26fc10000",…}]}}}
```

- `record.body`: JSON is parsed, other text kept as text, binary bodies only as a size. `record.maxBodyBytes` (default 65536) cuts longer bodies (`"truncated": true`).
- `record.headers`: `authorization`, `cookie` and headers whose name contains `token`, `secret`, `key` or `auth` are `[REDACTED]`. Secrets in bodies (`password`, `apiKey`, `writeKey`, …) are redacted too.
- Only matched requests are recorded with bodies. Without `--bodies`, `requests` has no bodies or headers.
- A rule with `record` and no `response` forwards the real request. A forwarded request from the offscreen document or a snap gets no `status` in the record; read it with `mm network`.

## Examples

```bash
# Single rule
mm mock-network add '{"id":"token-prices","method":"GET","url":"https://price.api.metamask.io/v1/**","response":{"status":200,"json":{"ethereum":{"usd":1234.56}}}}'

# Multiple rules
mm mock-network add '{"routes":[
  {"id":"feature-flags","method":"GET","url":"https://client-config.api.cx.metamask.io/**","response":{"json":{"flags":{}}}},
  {"id":"empty-nfts","method":"POST","url":"https://nft.api.metamask.io/**","response":{"status":200,"json":{"nfts":[]}}}
]}'

# A snap request (needs Basic functionality on): fail the Bitcoin snap's block poll
mm mock-network add '{"id":"btc-blocks","method":"GET","url":"https://bitcoin-mainnet.infura.io/**/esplora/blocks","response":{"status":503,"body":"mocked"}}'

# Inspect and manage
mm mock-network list
mm mock-network requests --limit 20 --url validate --bodies
mm mock-network clear
```

## Verification Pattern

1. Find the request: `mm network --url <text> --cursor <mark>` shows its exact URL, method and `target.kind`.
2. Add the rule with `mm mock-network add ...` and check `contexts` / `pending`.
3. Trigger the UI flow that makes the request (`mm reload` first if the data is already loaded).
4. Run `mm mock-network requests --url <text>`: the request has `matched: true`, the expected `ruleId` and `context`.
5. Check the effect on the screen (`mm get-text`, `mm screenshot`) or in `mm network --url <text>` (the record shows the mocked `status`).

## In mm run-steps

Use tool name `mock_network` with the same input shape:

```bash
mm run-steps '{"steps":[
  {"tool":"mock_network","args":{"action":"add","rule":{"id":"prices","method":"GET","url":"https://price.api.metamask.io/v1/**","response":{"json":{"ok":true}}}}},
  {"tool":"navigate","args":{"screen":"url","url":"https://test-dapp.io"}}
]}'
```
