# email-ses-sender (Track: ai-productivity)

Send templated emails via AWS SES with support for HTML rendering, attachments, and bulk delivery

## Overview

This skill enables sending formatted emails through AWS Simple Email Service (SES). It supports HTML templates with variable substitution, CC/BCC recipients, attachments, and delivery tracking. Perfect for transactional emails, notifications, and automated communications.

## Features

- **AWS SES Integration**: Direct integration with AWS SES for reliable delivery
- **Template Support**: Render HTML templates with variable substitution
- **Rich Formatting**: Support for HTML emails with inline CSS
- **Attachments**: Include file attachments in emails
- **Bulk Send**: Send to multiple recipients efficiently
- **Delivery Tracking**: Get delivery status and bounce information
- **Custom Headers**: Add custom email headers
- **Sandbox Mode**: Test emails in AWS SES sandbox

## Use Cases

- Send password reset emails with verification links
- Deliver transaction receipts and order confirmations
- Send daily/weekly digest emails to users
- Notify team members of important events
- Generate automated reports and send via email
- User signup confirmation and onboarding emails

## Quickstart
```bash
python3 scripts/main.py --help
```

## Example
```bash
python3 scripts/main.py --demo
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| from_address | string | Yes | Sender email address (must be verified in SES) |
| to_addresses | array | Yes | Array of recipient email addresses |
| subject | string | Yes | Email subject line |
| body_html | string | Yes | HTML body content |
| body_text | string | No | Plain text fallback body |
| template_name | string | No | SES template name to use |
| template_data | object | No | Variables for template rendering |
| cc_addresses | array | No | CC recipient addresses |
| bcc_addresses | array | No | BCC recipient addresses |
| attachments | array | No | Array of attachment objects |
| configuration_set | string | No | SES configuration set for tracking |

## Example Output

```json
{
  "ok": true,
  "data": {
    "message_id": "0000014d-95ad-4c41-b6b8-3e0836dc9d6d-000000",
    "from": "noreply@example.com",
    "to": ["user@example.com"],
    "subject": "Welcome to Our Service",
    "status": "sent",
    "timestamp": "2026-02-07T10:15:30Z",
    "body_preview": "Hello user@example.com, Welcome to our platform...",
    "headers_sent": 12
  }
}
