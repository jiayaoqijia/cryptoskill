# logfile-alerts (Track: ai-productivity)

Scan logs and emit structured alerts with pattern matching and severity classification

## Overview

This skill enables automated log file analysis and alert generation. It reads log files, identifies patterns matching configurable rules, classifies severity levels, and emits structured alerts for downstream processing. Perfect for monitoring application logs, system logs, and custom log formats.

## Features

- **Pattern Matching**: Configure regex patterns to detect specific log events
- **Severity Classification**: Automatically categorize alerts as critical, warning, info, or debug
- **Structured Output**: Generate JSON-formatted alerts with metadata
- **Tail Support**: Monitor growing log files for real-time alerts
- **Filter Options**: Include/exclude log lines based on criteria
- **Customizable Rules**: Define alert rules with pattern and action pairs

## Use Cases

- Monitor application error logs for exceptions and stack traces
- Track performance warnings and performance degradation alerts
- Detect security-related events in authentication logs
- Generate alerts for failed deployments or build errors
- Process syslog entries for infrastructure monitoring

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
| log_file | string | Yes | Path to log file to scan |
| patterns | array | Yes | Array of pattern objects to match |
| patterns[].regex | string | Yes | Regular expression to match log lines |
| patterns[].severity | string | Yes | Severity level (critical, warning, info, debug) |
| patterns[].action | string | No | Action on match (alert, log, count) |
| output_format | string | No | Output format (json, text, csv) - default: json |
| tail_mode | boolean | No | Monitor file for new lines - default: false |
| max_alerts | integer | No | Maximum alerts to generate - default: 100 |
| time_window | integer | No | Time window in seconds for deduplication |

## Example Output

```json
{
  "ok": true,
  "alerts": [
    {
      "timestamp": "2026-02-07T10:15:30Z",
      "severity": "critical",
      "pattern": "ERROR.*Exception",
      "matched_line": "2026-02-07 10:15:30 ERROR NullPointerException in UserService",
      "line_number": 1245,
      "context": {
        "file": "app.log",
        "service": "api-server"
      }
    },
    {
      "timestamp": "2026-02-07T10:16:45Z",
      "severity": "warning",
      "pattern": "Response time.*>.*1000ms",
      "matched_line": "2026-02-07 10:16:45 WARN Response time for GET /users: 1245ms",
      "line_number": 1256
    }
  ],
  "summary": {
    "total_lines_scanned": 5234,
    "total_alerts": 2,
    "by_severity": {"critical": 1, "warning": 1, "info": 0}
  }
}
