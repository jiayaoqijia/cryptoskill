# code-review-basics (Track: enterprise-skills)

Automate code analysis and generate code review checklists for quality assurance

## Overview

This skill performs static analysis on source code and generates structured code review checklists. It detects common issues like overly long functions, complexity problems, and provides actionable review items.

## Features

- **Static Analysis**: Parse and analyze code structure using AST
- **Issue Detection**: Identify long functions, complex code, unused variables
- **Review Checklist**: Generate structured review points for human reviewers
- **Multi-Language Ready**: Built for Python, extensible to others
- **Severity Levels**: Categorize issues by importance

## Use Cases

- Automate initial code review steps
- Enforce coding standards consistently
- Train junior developers on code quality
- Generate peer review guidance
- Detect potential bugs early

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
| code | string | Yes | Source code to analyze |
| language | string | No | Programming language (python, javascript) - default: python |
| threshold | integer | No | Max lines for function (default: 50) |

## Example Output

```json
{
  "ok": true,
  "data": {
    "issues": [
      {
        "type": "long_function",
        "line": 42,
        "message": "Function 'process_data' is 75 lines long (>50)"
      }
    ],
    "checklist": [
      {"item": "Check for long functions", "status": "fail"},
      {"item": "Check for unused variables", "status": "pass"},
      {"item": "Check for complexity", "status": "pass"}
    ]
  }
}
```
