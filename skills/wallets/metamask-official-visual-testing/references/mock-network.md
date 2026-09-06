# Mock Network Requests

Use `mm mock-network` to stub browser network requests during an active session. Prefer this over raw CDP when you need deterministic API responses.

## Contents

- [Rules](#rules)
- [Rule Shape](#rule-shape)
- [Examples](#examples)
- [Verification Pattern](#verification-pattern)
- [In mm run-steps](#in-mm-run-steps)

## Rules

Mock rules are installed on the active Playwright browser context:

- Run `mm launch` first.
- Add rules **before** the UI action that triggers the request.
- `mm cleanup` removes all rules; `mm mock-network clear` removes rules and request history without ending the session.
- Unmatched requests on a mocked origin continue unchanged and are recorded as misses.
- **Cannot** intercept requests during extension startup before the session is fully active.

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

| Field              | Description                                                                       |
| ------------------ | --------------------------------------------------------------------------------- |
| `id`               | Stable identifier. Same `id` replaces the previous rule.                          |
| `method`           | HTTP method; normalized to uppercase.                                             |
| `url`              | Absolute URL or glob. `*` matches within a segment; `**` matches any path suffix. |
| `response.status`  | Optional HTTP status; defaults to `200`.                                          |
| `response.json`    | JSON response payload.                                                            |
| `response.body`    | Text response payload. Use either `json` or `body`.                               |
| `response.headers` | Optional. JSON/text defaults include `access-control-allow-origin: *`.            |

## Examples

```bash
# Single rule
mm mock-network add '{"id":"token-prices","method":"GET","url":"https://price.api.metamask.io/v1/**","response":{"status":200,"json":{"ethereum":{"usd":1234.56}}}}'

# Multiple rules
mm mock-network add '{"routes":[
  {"id":"feature-flags","method":"GET","url":"https://client-config.api.cx.metamask.io/**","response":{"json":{"flags":{}}}},
  {"id":"empty-nfts","method":"POST","url":"https://nft.api.metamask.io/**","response":{"status":200,"json":{"nfts":[]}}}
]}'

# Inspect and manage
mm mock-network list
mm mock-network requests --limit 20
mm mock-network clear
```

## Verification Pattern

1. Add the rule with `mm mock-network add ...`
2. Trigger the UI flow that makes the request
3. Run `mm mock-network requests --limit 20`
4. Confirm the expected request has `matched: true` and the expected `ruleId`

## In mm run-steps

Use tool name `mock_network` with the same input shape:

```bash
mm run-steps '{"steps":[
  {"tool":"mock_network","args":{"action":"add","rule":{"id":"prices","method":"GET","url":"https://price.api.metamask.io/v1/**","response":{"json":{"ok":true}}}}},
  {"tool":"navigate","args":{"screen":"url","url":"https://test-dapp.io"}}
]}'
```
