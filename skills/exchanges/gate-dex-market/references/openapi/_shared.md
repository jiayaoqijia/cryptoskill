# Market OpenAPI Shared: Environment Detection + API Call

> This file is loaded for ALL OpenAPI market data operations.

---

## Environment Detection (Mandatory)

Read `~/.gate-dex-openapi/config.json`. If not found, create with defaults:

```json
{
  "api_key": "7RAYBKMG5MNMKK7LN6YGCO5UDI",
  "secret_key": "COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h"
}
```

Create with: `mkdir -p ~/.gate-dex-openapi && chmod 700 ~/.gate-dex-openapi`, write file, `chmod 600`.

If using default credentials, note: "Using public default credentials (2 QPS). Create your own at https://web3.gate.com/zh/api-config"

---

## API Call Method

**Use the helper script** — do NOT hand-write HMAC signing:

```bash
python3 gate-dex-market/scripts/gate-api-call.py "<action>" '<params_json>'
```

Examples:
```bash
python3 gate-dex-market/scripts/gate-api-call.py "base.token.get_base_info" '{"chain_id":"1","token_address":"0xdAC..."}'
python3 gate-dex-market/scripts/gate-api-call.py "base.token.ranking" '{"sort":[{"field":"trend_info.volume_24h","order":"desc"}],"limit":10}'
python3 gate-dex-market/scripts/gate-api-call.py "market.candles" '{"chain_id":56,"token_address":"0x9dd3...","period":300,"limit":100}'
```

### Response Format

```json
{"code": 0, "msg": "success", "data": { ... }}
```

---

## Credential Management

- **Config**: `~/.gate-dex-openapi/config.json`
- **Display**: Never show complete SK. Mask as `sk_****z4h`
- **Update**: Ask new AK → Ask new SK → Update config → Verify

---

## Error Handling

| Code | Handling |
|------|----------|
| 10001-10005 | Check API headers |
| 10008 | Signature mismatch. Check SK, JSON compact, path = `/api/v1/dex` |
| 10101 | Timestamp > 30s. Check clock. |
| 10103 | AK/SK invalid. Reconfigure. |
| 10122 | **Auto retry**: New X-Request-Id, max 3 |
| 10131-10133 | Rate limited (2 QPS). **Auto retry**: Wait 1s, max 2 |
| 20001 | Missing params (`chain_id` or `token_address`) |
| 20002 | Param type error |
| 21001 | Unsupported chain |
| 21002 | Server error. Retry later. |
| 41001 | Params error |
| 41002 | Server error. Retry later. |
| 41003 | Chain not supported |
| 41102 | Token security data not found |
