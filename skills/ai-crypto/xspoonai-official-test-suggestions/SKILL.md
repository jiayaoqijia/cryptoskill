---
name: test-suggestions
track: enterprise-skills
version: 0.1.0
summary: Suggest unit tests from file list and functions
---

## Description

Suggest unit tests from file list and function definitions. Analyzes code to recommend test cases and provides test templates for better coverage.

## Inputs

```json
{
  "files": ["list of source files"],
  "functions": ["function names to test"]
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "suggestions": [],
    "coverage_estimate": "75%"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Get Test Suggestions
```bash
echo '{"files": ["main.py"], "functions": ["process_data"]}' | python3 scripts/main.py
```

## Examples

### Example 1: Test Suggestions
```bash
$ echo '{"files": ["utils.py"], "functions": ["calculate_total"]}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "suggestions": ["Test with positive numbers", "Test with negative numbers", "Test edge cases"],
    "coverage_estimate": "85%"
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
    "files": "File not found"
  }
}
```
