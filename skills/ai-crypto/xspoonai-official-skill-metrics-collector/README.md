# skill-metrics-collector (Track: platform-challenge)

Collect and aggregate skill execution metrics with comprehensive reporting

## Overview

This skill collects, aggregates, and analyzes execution metrics from skill invocations. It tracks invocation counts, success rates, performance percentiles, and error patterns across multiple skills with configurable time windows.

## Features

- **Metrics Collection**: Track invocations, success rates, and execution times per skill
- **Performance Tracking**: Calculate min, max, average, and percentile response times (p75, p95, p99)
- **Aggregation**: Aggregate metrics across all skills or analyze specific skills
- **Time Windows**: Support flexible time ranges (hours, days) for metric analysis
- **Error Analysis**: Categorize errors (timeout, validation, other) and track frequency
- **Recommendations**: Generate actionable insights based on performance data
- **Success Rates**: Calculate and track success/failure counts and percentages

## Usage

Collect execution metrics from skill invocations:

```bash
# Collect metrics for all skills over 24 hours
python3 scripts/main.py --demo

# Collect metrics for specific skill
python3 scripts/main.py --skill api-webhook-signer

# Specify time window
python3 scripts/main.py --skill security-deps-audit --hours 72

# Custom parameters
python3 scripts/main.py --params '{"skill": "test-suggestions", "hours": 48}'
```

## Use Cases

- Monitor skill performance and reliability
- Identify performance bottlenecks and optimization opportunities
- Track skill adoption and usage patterns
- Generate performance reports for teams
- Detect error trends and problematic skills

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skill | string | No | Specific skill to analyze metrics for |
| hours | number | No | Time window in hours (default: 24) |

## Example Output

Metrics for 5 skills over 24 hours showing 105 total invocations with 96.2% overall success rate. Each skill includes performance percentiles, error breakdown, and recommendations. Skills tracked: api-webhook-signer, security-deps-audit, test-suggestions, skill-ci-checklist, whale-tracker.
