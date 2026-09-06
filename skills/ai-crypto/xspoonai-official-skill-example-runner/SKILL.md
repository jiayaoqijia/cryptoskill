---
name: skill-example-runner
track: platform-challenge
version: 0.1.0
summary: Run sample input for each skill and save output
---

## Description

Run sample input for each skill and collect outputs. Tests all skills with demo data and saves results for documentation.

## Inputs

```json
{
  "skills_path": "Path to skills directory",
  "save_results": true
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "executed": 50,
    "successful": 48,
    "failed": 2
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Run Examples
```bash
echo '{"skills_path":"./","save_results":true}' | python3 scripts/main.py
```

## Examples

### Example 1: Test All Skills
```bash
$ echo '{"skills_path":".","save_results":true}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "executed": 50,
    "successful": 48,
    "failed": 2,
    "results_file": "skill_outputs.json"
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
