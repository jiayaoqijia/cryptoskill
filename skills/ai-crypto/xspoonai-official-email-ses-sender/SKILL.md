---
name: email-ses-sender
track: ai-productivity
version: 0.1.0
summary: Send templated emails via AWS SES
---

## Description

Send templated emails via AWS SES (Simple Email Service). Supports email templates, variables, and sandbox testing mode.

## Inputs

```json
{
  "to": "Recipient email",
  "subject": "Email subject",
  "template": "Template name",
  "variables": {}
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "message_id": "Email message ID",
    "status": "sent"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Send Email
```bash
echo '{"to":"user@example.com","subject":"Hello","template":"welcome"}' | python3 scripts/main.py
```

## Examples

### Example 1: Send Email to test@sambitsargam.in
```bash
$ echo '{"to":"test@sambitsargam.in","subject":"Test Email","template":"notification","variables":{"message":"This is a test email"}}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "message_id": "0000014a-aee4-4a01-a640-a8f7f5bd5e7e-000001",
    "status": "sent",
    "recipient": "test@sambitsargam.in",
    "timestamp": "2026-02-07T10:15:30Z"
  }
```

### Example 2: Send Email to sambitsargam2003@gmail.com
```bash
$ echo '{"to":"sambitsargam2003@gmail.com","subject":"Important Update","template":"alert","variables":{"alert_type":"system","severity":"high"}}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "message_id": "0000014a-aee4-4a01-a640-a8f7f5bd5e7e-000001",
    "status": "sent",
    "recipient": "sambitsargam2003@gmail.com",
    "timestamp": "2026-02-07T10:15:35Z"
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
    "to": "Invalid email address"
  }
}
```
