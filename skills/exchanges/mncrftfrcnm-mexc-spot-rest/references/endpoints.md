# MEXC Spot V3 REST Endpoint Reference

Source basis: official MEXC Spot V3 API docs checked 2026-06-01.

Use the compact catalog instead of reading a long prose reference:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/lookup.py" <topic>
```

## Auth Summary

- Base URL: `https://api.mexc.com`
- Public: no API key.
- API-key-only: `X-MEXC-APIKEY`.
- Signed: `X-MEXC-APIKEY`, `timestamp`, optional `recvWindow`, and HMAC-SHA256 `signature` over `totalParams`.

## Topics

`market`, `account`, `orders`, `listen-key`, `wallet`, `sub-account`, `rebate`

## Implementation Notes

- Pass signed business parameters through `--params`; do not embed query strings in signed paths.
- Use `POST /api/v3/order/test` before live `POST /api/v3/order`.
- Use uppercase symbols such as `BTCUSDT` and exact decimal strings.
- MEXC is live-only; back off on `429` and honor `Retry-After` when returned.
