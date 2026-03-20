# OKX API v5 — Authentication Reference

## Signature Algorithm

All private REST endpoints require HMAC SHA256 authentication.

### Step-by-step

1. **Generate timestamp** — ISO 8601 UTC with milliseconds:
   ```
   2024-01-15T10:30:00.123Z
   ```
   Python: `datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"`

2. **Build pre-sign string**:
   ```
   pre_sign = timestamp + METHOD + path_with_query + body
   ```
   - `METHOD`: uppercase `GET` or `POST`
   - `path_with_query`: full path including `?key=value` query string
   - `body`: JSON string for POST, **empty string** for GET (not null, not `{}`)

3. **Sign**:
   ```python
   mac = hmac.new(secret_key.encode('utf-8'), pre_sign.encode('utf-8'), hashlib.sha256)
   signature = base64.b64encode(mac.digest()).decode()
   ```

4. **Set headers**:
   ```
   OK-ACCESS-KEY:        your_api_key
   OK-ACCESS-SIGN:       computed_signature
   OK-ACCESS-TIMESTAMP:  timestamp_used_for_signing
   OK-ACCESS-PASSPHRASE: your_passphrase
   Content-Type:         application/json  (POST only)
   ```

---

## Edge Cases

### GET requests with query parameters

The query string is **part of the signed path**:
```
pre_sign = "2024-01-15T10:30:00.123Z" + "GET" + "/api/v5/market/ticker?instId=BTC-USDT" + ""
```

Order of params in the query string must match exactly what is sent in the request.

### POST requests

Body must be a **compact JSON string** (no extra whitespace) and must match exactly what is sent:
```python
body_str = json.dumps(body, separators=(',', ':'))
# OR just json.dumps(body) — the default compact format works too
```

Empty POST body: use `""` (empty string), not `"{}"`.

### Timestamp tolerance

OKX rejects requests with timestamps more than **±30 seconds** from server time. If you get error `50114`, sync your system clock.

Check server time:
```
GET /api/v5/public/time
```
Response: `{"ts": "1705312200123"}`

---

## Demo/Sandbox Trading

Same base URL (`https://www.okx.com`) with an additional header:
```
x-simulated-trading: 1
```

All account data and orders in sandbox are isolated from live trading. The API key for sandbox must be created specifically in the OKX demo environment.

---

## WebSocket Authentication

Private WebSocket channels use a `login` op with a different timestamp format (Unix seconds as string):

```json
{
  "op": "login",
  "args": [{
    "apiKey": "your_key",
    "passphrase": "your_passphrase",
    "timestamp": "1705312200",
    "sign": "computed_signature"
  }]
}
```

Signature for WebSocket login:
```
pre_sign = "1705312200" + "GET" + "/users/self/verify" + ""
```

The path `/users/self/verify` is a fixed string used only for WebSocket auth — it's not a real REST endpoint.

---

## Common Auth Error Codes

| Code | Message | Cause |
|------|---------|-------|
| `50111` | Invalid OK-ACCESS-KEY | API key doesn't exist or was deleted |
| `50112` | Invalid OK-ACCESS-PASSPHRASE | Wrong passphrase |
| `50113` | Invalid signature | Signature mismatch — check pre-sign string construction |
| `50114` | Invalid timestamp | System clock out of sync (±30s tolerance) |
| `50116` | Invalid request | IP not in whitelist (if whitelist is enabled) |

### Debugging `50113` Invalid Signature

1. Print the pre-sign string before signing and verify it matches: `timestamp + METHOD + path + body`
2. Check that the secret key is the exact string from OKX (no trailing whitespace/newline)
3. For GET: confirm the query string is appended to the path in the pre-sign string
4. For POST: confirm `body_str` is the exact JSON string sent in the request body
5. Confirm timestamp string format: `2024-01-15T10:30:00.123Z` (not Unix timestamp, not without milliseconds)
