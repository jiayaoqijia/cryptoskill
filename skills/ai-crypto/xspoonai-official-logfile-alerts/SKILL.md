---
name: logfile-alerts
track: ai-productivity
version: 0.1.0
summary: Scan logs and emit structured alerts
---

## Description

Scan log files for patterns and emit structured alerts. Identifies errors, warnings, and anomalies with configurable alert thresholds.

## Inputs

```json
{
  "log_file": "Path to log file",
  "patterns": ["ERROR", "WARNING"],
  "threshold": "Number of occurrences"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "alerts": [],
    "total_matches": 0
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Scan Logs
```bash
echo '{"log_file":"/var/log/app.log","patterns":["ERROR"]}' | python3 scripts/main.py
```

## Examples

### Example 1: Log Analysis
```bash
$ echo '{"log_file":"app.log","patterns":["ERROR"],"threshold":5}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "alerts": ["5 ERROR entries found"],
    "total_matches": 5
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
    "log_file": "File not found"
  }
}
```
