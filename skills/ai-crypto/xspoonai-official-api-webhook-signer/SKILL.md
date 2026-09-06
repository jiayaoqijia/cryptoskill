---
name: api-webhook-signer
track: ai-productivity
version: 0.1.0
summary: Generate and verify HMAC-SHA256 signed webhooks
---

## Description

Generate and verify HMAC-SHA256 signed webhooks with retry queue and exponential backoff. Provides secure webhook signing and validation for API integrations.

## Inputs

```json
{
  "action": "sign|verify",
  "payload": "Webhook payload",
  "secret": "HMAC secret key",
  "signature": "Signature to verify (for verify action)"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "signature": "Generated signature",
    "valid": true
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Sign Webhook
```bash
echo '{"action":"sign","payload":{"event":"user.created"},"secret":"my_secret"}' | python3 scripts/main.py
```

## Examples

### Example 1: Sign Webhook
```bash
$ echo '{"action":"sign","payload":{"event":"user.created","user_id":123},"secret":"my_secret"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "signature": "sha256=abc123def456..."
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": {
    "secret": "Secret key is required"
  }
}
```
