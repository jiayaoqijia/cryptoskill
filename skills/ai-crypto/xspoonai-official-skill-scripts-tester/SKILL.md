---
name: skill-scripts-tester
track: platform-challenge
version: 0.1.0
summary: Run scripts/main.py --demo for all skills
---

## Description

Run demo mode for all skills and generate comprehensive test report. Validates all skill implementations work correctly.

## Inputs

```json
{
  "skills_path": "Path to skills directory",
  "generate_report": true
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "total": 50,
    "passed": 49,
    "failed": 1,
    "report": "Test report path"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Test All Skills
```bash
echo '{"skills_path":"./","generate_report":true}' | python3 scripts/main.py
```

## Examples

### Example 1: Run Test Suite
```bash
$ echo '{"skills_path":".","generate_report":true}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "total": 50,
    "passed": 49,
    "failed": 1,
    "report": "test_report_2026_02_06.md"
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
    "skills_path": "Directory not found"
  }
}
```
