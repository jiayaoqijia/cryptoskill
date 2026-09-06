# messaging-slack-notify (Track: ai-productivity)

Send formatted Slack messages with rich formatting, attachments, and interactive elements

## Overview

This skill provides integration with Slack for sending notifications and messages. It supports message blocks, rich formatting, mentions, file uploads, and interactive buttons. Perfect for CI/CD notifications, alert systems, and automated team communications.

## Features

- **Message Blocks**: Create complex formatted messages with block Kit
- **Mentions**: Tag users and channels in messages
- **Emoji Support**: Use emoji in messages and reactions
- **File Uploads**: Attach files to Slack messages
- **Message Threads**: Reply to specific messages
- **Interactive Buttons**: Add action buttons to messages
- **Rich Formatting**: Bold, italic, code formatting support
- **Channel Routing**: Send to channels, DMs, or user groups

## Use Cases

- Alert on critical system events and errors
- Notify team on deployment status and releases
- Send daily standup summaries to channels
- Create incident alerts for on-call engineers
- Report on automation task completion
- Notify on code review requests and approvals

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
| webhook_url | string | Yes | Slack webhook URL for incoming webhooks |
| channel | string | No | Channel ID or name (overrides webhook default) |
| username | string | No | Display name for the bot message |
| text | string | No | Plain text message (for simple messages) |
| blocks | array | No | Array of Block Kit blocks for rich formatting |
| attachments | array | No | Array of attachment objects |
| icon_emoji | string | No | Emoji for bot icon |
| thread_ts | string | No | Message timestamp to reply in thread |
| reply_broadcast | boolean | No | Share thread reply in channel - default: false |

## Example Output

```json
{
  "ok": true,
  "message_sent": {
    "channel": "#deployments",
    "text": ":rocket: Deployment completed successfully",
    "timestamp": "1738940130.000001",
    "status": "sent",
    "delivery_time_ms": 142
  },
  "webhook_response": {
    "status_code": 200,
    "status": "success"
  }
}
