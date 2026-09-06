---
name: skill-metrics-collector
track: platform-challenge
version: 0.1.0
summary: Collect usage metrics JSON for skills
---

## Description

Collect usage metrics for skills in JSON format. Tracks execution statistics and performance metrics locally.

## Inputs

```json
{
  "metrics_path": "Path to save metrics",
  "collect_from": "local|remote"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "metrics": {},
    "timestamp": "ISO timestamp"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Collect Metrics
```bash
echo '{"metrics_path":"./metrics","collect_from":"local"}' | python3 scripts/main.py
```

## Examples

### Example 1: Collect Metrics
```bash
$ echo '{"metrics_path":"./metrics","collect_from":"local"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "metrics": {"total_executions": 250, "avg_latency": 245},
    "timestamp": "2026-02-06T07:31:06.856041+00:00"
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
    "metrics_path": "Invalid path"
  }
}
```
