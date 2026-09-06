---
name: incident-template
track: enterprise-skills
version: 0.1.0
summary: Generate incident response templates with timeline sections
---

## Description

Emit incident response templates with structured timeline sections. Provides templates for incident documentation, root cause analysis, and action items.

## Inputs

```json
{
  "incident_type": "outage|security|data-loss",
  "severity": "critical|high|medium"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "template": "Incident response markdown template"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Generate Incident Template
```bash
echo '{"incident_type": "outage", "severity": "critical"}' | python3 scripts/main.py
```

## Examples

### Example 1: Critical Outage Template
```bash
$ echo '{"incident_type": "outage", "severity": "critical"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "template": "# Incident Report\n\n## Summary\n\n## Timeline\n\n## Impact\n\n## Root Cause\n\n## Action Items"
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
    "incident_type": "Invalid incident type"
  }
}
```
