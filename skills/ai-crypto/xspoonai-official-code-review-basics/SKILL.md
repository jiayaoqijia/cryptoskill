---
name: code-review-basics
track: enterprise-skills
version: 0.1.0
summary: Run static checks and emit code review checklist
---

## Description

Run static analysis checks and emit a comprehensive code review checklist. Language-agnostic approach for reviewing code quality, style, and best practices.

## Inputs

```json
{
  "files": ["list of files to review"],
  "language": "python|javascript|go"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "issues": [],
    "checklist": []
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Review Code
```bash
echo '{"files": ["src/main.py"], "language": "python"}' | python3 scripts/main.py
```

## Examples

### Example 1: Python Code Review
```bash
$ echo '{"files": ["main.py"], "language": "python"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "issues": ["Missing docstrings", "Line too long"],
    "checklist": ["Code style check pass", "Import organization verified"]
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
