---
name: perf-budget-checker
track: enterprise-skills
version: 0.1.0
summary: Check performance budgets against metrics
---

## Description

Check simple performance budgets against metrics JSON. Validates that application metrics stay within defined budgets for performance thresholds.

## Inputs

```json
{
  "metrics": {
    "bundle_size": "100kb",
    "load_time": "3s"
  },
  "budgets": {
    "bundle_size": "150kb",
    "load_time": "5s"
  }
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "passed": true,
    "violations": []
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Check Performance Budget
```bash
echo '{"metrics": {}, "budgets": {}}' | python3 scripts/main.py
```

## Examples

### Example 1: Budget Check
```bash
$ echo '{"metrics": {"bundle_size": "100kb"}, "budgets": {"bundle_size": "150kb"}}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "passed": true,
    "violations": []
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
    "metrics": "Invalid metrics format"
  }
}
```
