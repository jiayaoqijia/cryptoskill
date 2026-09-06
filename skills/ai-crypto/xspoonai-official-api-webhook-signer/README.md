# api-webhook-signer (Track: ai-productivity)

Generate and verify HMAC-SHA256 signed webhooks with retry queue and exponential backoff.

## Features

- **Sign webhooks**: Generate HMAC-SHA256 signatures for webhook payloads
- **Verify webhooks**: Validate incoming webhook signatures
- **Retry queue**: Generate retry schedules with exponential backoff
- **Secure**: Uses constant-time comparison for signature verification

## Quickstart

```bash
# Run demo
python3 scripts/main.py --demo

# Sign a webhook
python3 scripts/main.py --params '{"action":"sign","payload":{"event":"user.created","user_id":123},"secret":"my_secret"}'

# Verify a webhook
python3 scripts/main.py --params '{"action":"verify","payload":{"event":"user.created","user_id":123},"secret":"my_secret","signature":"b07805bb..."}'
```

## Example Output

```json
{
  "ok": true,
  "data": {
    "demo": true,
    "signed_webhook": {
      "payload": {"event": "user.created", "user_id": 12345},
      "signature": "b07805bb6e9f580fa994f5e253d915eb31a05cfaa8ff9c047abbcb34e492abf1",
      "secret": "demo_secret_key_12345"
    },
    "verification": {"valid": true},
    "retry_queue": [
      {"attempt": 1, "delay_seconds": 1, "next_retry": "2026-02-06T10:00:01Z"},
      {"attempt": 2, "delay_seconds": 2, "next_retry": "2026-02-06T10:00:02Z"},
      {"attempt": 3, "delay_seconds": 4, "next_retry": "2026-02-06T10:00:04Z"}
    ]
  }
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action | string | Yes | "sign" or "verify" |
| payload | object | Yes | Webhook payload to sign/verify |
| secret | string | Yes | Secret key for HMAC |
| signature | string | For verify | Signature to verify |
| retry_config | object | No | Retry configuration |
| retry_config.max_attempts | int | No | Max retry attempts (default: 3) |
| retry_config.base_delay | int | No | Base delay in seconds (default: 1) |
| retry_config.backoff_multiplier | float | No | Backoff multiplier (default: 2) |
