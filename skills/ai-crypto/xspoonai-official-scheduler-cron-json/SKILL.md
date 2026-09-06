---
name: scheduler-cron-json
track: ai-productivity
version: 0.1.0
summary: Emit cronjob JSON configurations for hosted schedulers
---

## Description

Emit cronjob JSON configurations for hosted schedulers. Generates cron configurations for task automation platforms.

## Inputs

```json
{
  "schedule": "0 0 * * *|cron expression",
  "task": "Task name",
  "webhook": "Webhook URL"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "config": "Cron configuration",
    "next_run": "ISO timestamp"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Generate Cron Config
```bash
echo '{"schedule":"0 0 * * *","task":"daily_backup"}' | python3 scripts/main.py
```

## Examples

### Example 1: Create Daily Schedule
```bash
$ echo '{"schedule":"0 0 * * *","task":"daily_backup","webhook":"https://corns-testingbysambit.vercel.app/test"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "config": "0 0 * * * curl https://corns-testingbysambit.vercel.app/test",
    "next_run": "2026-02-07T00:00:00Z"
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
    "schedule": "Invalid cron expression"
  }
}
```
