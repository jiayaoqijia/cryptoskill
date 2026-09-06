---
name: messaging-slack-notify
track: ai-productivity
version: 0.1.0
summary: Send formatted Slack notifications from scripts
---

## Description

Send formatted Slack notifications from scripts. Supports rich message formatting, attachments, and webhook integration.

## Inputs

```json
{
  "channel": "#notifications|@user",
  "message": "Notification message",
  "format": "text|rich"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "message_id": "Message timestamp",
    "status": "sent"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Send Notification
```bash
echo '{"channel":"#alerts","message":"Server down!"}' | python3 scripts/main.py
```

## Examples

### Example 1: Send Alert
```bash
$ echo '{"message":"Critical: Database connection failed"}' | python3 scripts/main.py --params '{"webhook_url":"https://hooks.slack.com/services/...","message":"Critical: Database connection failed"}'
{
  "ok": true,
  "message_sent": {
    "channel": "#general",
    "text": "Critical: Database connection failed",
    "timestamp": "1738940130.000001",
    "status": "sent",
    "delivery_time_ms": 142
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
    "channel": "Channel not found"
  }
}
```
