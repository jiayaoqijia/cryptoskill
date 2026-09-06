# incident-template (Track: enterprise-skills)

Generate structured incident reports and response documentation with timeline, analysis, and action tracking

## Overview

This skill creates professional incident reports with comprehensive sections including timeline, impact assessment, team assignments, root cause analysis, and action items. Supports multiple output formats (Markdown for human reading, JSON for programmatic use).

## Features

- **Structured Reporting**: Generate well-organized incident reports with all critical sections
- **Multiple Formats**: Output as Markdown, JSON structured data, or both simultaneously
- **Severity Levels**: Support for critical, high, medium, and low severity incidents with SLA tracking
- **Timeline Management**: Document event sequence with timestamps and descriptions
- **Team Assignment**: Track incident commander and team members involved
- **Root Cause Documentation**: Structured root cause analysis and resolution steps
- **Action Tracking**: Track action items with ownership and completion status
- **Incident Metadata**: Generate unique incident IDs and tracking information

## Use Cases

- Generate incident reports during active incident response
- Create post-incident documents for postmortems
- Track incident metadata and metrics for analysis
- Generate human-readable markdown for stakeholder communication
- Provide structured JSON data for ticketing system integration
- Document incident history and lessons learned

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
| title | string | Yes | Incident title |
| severity | string | Yes | Severity level (critical, high, medium, low) |
| type | string | No | Incident type (service_outage, degradation, security, data_loss, other) |
| impact | string | No | Description of impact on users/systems |
| affected_systems | array | No | List of affected system names |
| assigned_team | array | No | Array of {name, role} objects for team members |
| timeline | array | No | Array of {time, event} with timestamps and descriptions |
| root_cause | string | No | Root cause analysis details |
| resolution_steps | array | No | List of resolution steps taken |
| action_items | array | No | Array of {task, owner, status} for follow-up items |
| format | string | No | Output format (markdown, json, both) - default: markdown |

## Example Output

```json
{
  "ok": true,
  "data": {
    "demo": true,
    "incident_id": "INC-20260207085254",
    "markdown": "# Incident Report\n\n## Database Connection Pool Exhaustion...",
    "structured": {
      "id": "INC-20260207085254",
      "title": "Database Connection Pool Exhaustion",
      "severity": "high",
      "type": "degradation",
      "status": "resolved",
      "timeline_count": 6,
      "action_items_total": 4,
      "action_items_completed": 1
    }
  }
}
```
