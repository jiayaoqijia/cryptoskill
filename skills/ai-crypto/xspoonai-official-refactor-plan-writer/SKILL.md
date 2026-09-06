---
name: refactor-plan-writer
track: enterprise-skills
version: 0.1.0
summary: Suggest refactor plans for code improvements
---

## Description

Suggest refactor plans given a codebase summary. Analyzes code structure and proposes concrete refactoring strategies for code quality improvements.

## Inputs

```json
{
  "codebase_summary": "Summary of code structure",
  "issues": ["List of code issues"]
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "refactor_plan": "Detailed refactoring recommendations",
    "priority": "high|medium|low"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Generate Refactor Plan
```bash
echo '{"codebase_summary": "...", "issues": []}' | python3 scripts/main.py
```

## Examples

### Example 1: Refactor Recommendation
```bash
$ echo '{"codebase_summary": "Large monolithic service", "issues": ["high complexity"]}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "refactor_plan": "1. Extract business logic into separate modules\n2. Implement dependency injection",
    "priority": "high"
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
    "codebase_summary": "Summary is required"
  }
}
```
