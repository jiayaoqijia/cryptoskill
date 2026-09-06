# perf-budget-checker (Track: enterprise-skills)

Validate application performance metrics against defined budgets with detailed analysis and recommendations

## Overview

This skill implements comprehensive performance budget checking for web and mobile applications. It tracks multiple performance metrics, detects violations, calculates overages, and provides actionable recommendations for improvement.

## Features

- **Multi-Metric Support**: Load time, bundle size, requests, FCP, memory, error rate, and more
- **Severity Levels**: Pass, warning, caution, and critical based on overage percentage
- **Trend Analysis**: Compare current metrics against baseline for degradation detection
- **Detailed Reports**: Overage percentages, margin remaining, and metric-specific recommendations
- **Flexible Configuration**: Support for any custom metrics and thresholds
- **Actionable Recommendations**: Specific optimization suggestions for each metric type
- **Timestamp Tracking**: Record when checks were performed

## Use Cases

- Enforce performance budgets in CI/CD pipelines
- Prevent performance regressions in deployments
- Monitor historical performance trends
- Generate performance reports for stakeholders
- Alert teams when metrics exceed budgets
- Track optimization efforts over time

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
| application | string | No | Application name |
| environment | string | No | Environment (production, staging, development) |
| metrics | object | Yes | Current metrics {metric_name: value} |
| budget | object | Yes | Budget limits {metric_name: limit} |
| baseline | object | No | Previous metrics for trend analysis |

### Supported Metrics

- `load_time_ms`: Page load time (milliseconds)
- `bundle_size_kb`: JavaScript bundle size (kilobytes)
- `requests`: Number of HTTP requests (count)
- `first_contentful_paint_ms`: Time to FCP (milliseconds)
- `memory_mb`: Memory usage (megabytes)
- `error_rate`: Error rate (percentage)

## Example Output

```json
{
  "ok": true,
  "data": {
    "demo": true,
    "application": "web-frontend",
    "environment": "production",
    "check": {
      "timestamp": "2026-02-07T09:01:24",
      "summary": {
        "total_metrics": 6,
        "passed": 5,
        "warnings": 1,
        "cautions": 0,
        "critical": 0
      },
      "overall_status": "warning",
      "checks": [
        {
          "metric": "bundle_size_kb",
          "value": 520,
          "budget": 500,
          "status": "warning",
          "overage_pct": 4.0,
          "margin_pct": 0,
          "trend": "degraded",
          "trend_change": "+8.3%",
          "recommendation": "Nearly at budget. Monitor closely."
        }
      ]
    }
  }
}
```
