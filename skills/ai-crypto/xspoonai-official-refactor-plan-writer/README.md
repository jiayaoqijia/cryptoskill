# refactor-plan-writer (Track: enterprise-skills)

Generate prioritized refactoring plans based on code analysis

## Overview

This skill analyzes code complexity and creates structured refactoring plans. It prioritizes work based on impact, identifies code duplication, and estimates effort required for each task.

## Features

- **Priority-Based Planning**: Organize tasks by impact and priority
- **Complexity Analysis**: Identify functions and modules needing refactoring
- **Effort Estimation**: Estimate low/medium/high effort for each task
- **Duplication Detection**: Flag repeated code patterns
- **Markdown Export**: Generate refactoring roadmap documents

## Use Cases

- Plan technical debt reduction
- Prioritize refactoring work
- Generate team documentation for code improvements
- Break down complex refactoring into manageable tasks
- Track refactoring progress

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
| dependencies | array | No | List of dependency updates |

## Example Output

```json
{
  "ok": true,
  "data": {
    "demo": true,
    "timestamp": "2026-02-07T09:10:41",
    "project": "legacy-app",
    "analysis": {
      "code_smells": [
        {
          "type": "large_parameters",
          "name": "process_user_data",
          "param_count": 9,
          "severity": "medium",
          "threshold": 4,
          "description": "Function 'process_user_data' has 9 parameters"
        },
        {
          "type": "missing_docstrings",
          "name": "process_user_data",
          "severity": "low"
        }
      ],
      "technical_debt": {
        "total_issues": 8,
        "estimated_hours": 11.5,
        "debt_percentage": 7.2,
        "risk_level": "medium"
      },
      "summary": {
        "total_issues": 8,
        "estimated_effort_days": 1.4,
        "recommended_priority": "immediate"
      }
    }
  }
}
```
