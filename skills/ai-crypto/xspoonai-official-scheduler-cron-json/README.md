# scheduler-cron-json (Track: ai-productivity)

Generate scheduling configurations in JSON format for deployed job schedulers and cron services

## Overview

This skill converts cron expressions and scheduling requirements into structured JSON configurations for hosted schedulers like AWS EventBridge, Google Cloud Scheduler, and others. It validates cron syntax, calculates next execution times, and generates scheduler-specific configuration payloads.

## Features

- **Cron Expression Parsing**: Validate and parse standard cron syntax
- **Multiple Formats**: Support various cron formats (standard, AWS, extended)
- **Next Execution Calculation**: Compute next run times from cron expressions
- **Timezone Support**: Handle timezone-aware scheduling
- **Scheduler Adapters**: Output configs for multiple scheduler platforms
- **Validation**: Detect invalid cron expressions with helpful errors
- **Documentation Generation**: Create human-readable schedule descriptions
- **Batch Processing**: Handle multiple schedules efficiently

## Use Cases

- Generate scheduler configs for CI/CD pipelines and deployments
- Create backup job schedules that run at optimal times
- Configure periodic data synchronization tasks
- Set up maintenance window schedules
- Generate alert and health check schedules
- Create batch data processing job schedules

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
| cron_expression | string | Yes | Cron expression (e.g., "0 2 * * *") |
| scheduler_type | string | Yes | Target scheduler (eventbridge, cloud-scheduler, gitlab, github) |
| timezone | string | No | Timezone for schedule (default: UTC) |
| description | string | No | Human-readable description of schedule |
| next_runs | integer | No | Number of next runs to calculate (default: 5) |
| validate_only | boolean | No | Validate cron without generating config - default: false |
| payload | object | No | Payload to include in scheduler config |
| retry_config | object | No | Retry configuration for failed executions |

## Example Output

```json
{
  "ok": true,
  "data": {
    "cron_expression": "0 2 * * *",
    "description": "Daily backup at 2 AM UTC",
    "scheduler_config": {
      "name": "daily-database-backup",
      "expression": "cron(0 2 * * ? *)",
      "timezone": "UTC",
      "enabled": true,
      "retry_policy": {
        "max_attempts": 3,
        "backoff_rate": 2
      }
    },
    "next_runs": [
      "2026-02-08T02:00:00Z",
      "2026-02-09T02:00:00Z",
      "2026-02-10T02:00:00Z"
    ],
    "execution_count_monthly": 30
  }
}
