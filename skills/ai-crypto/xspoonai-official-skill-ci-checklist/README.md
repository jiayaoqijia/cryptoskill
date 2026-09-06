# skill-ci-checklist (Track: platform-challenge)

Validate skill quality and CI/CD readiness against quality gates

## Overview

This skill performs comprehensive validation of skill implementations checking documentation, code structure, Python syntax, and required functionality. It ensures all skills meet quality standards before deployment.

## Features

- **Structure Validation**: Check required files (SKILL.md, README.md, main.py, pull.md)
- **Documentation Analysis**: Validate sections, length, and completeness
- **YAML Validation**: Verify SKILL.md frontmatter contains required metadata
- **Code Quality**: Check Python syntax, imports, and functionality
- **Quality Scoring**: Calculate overall quality score (0-100)
- **Severity Classification**: Grade issues as critical, high, medium, or low
- **Actionable Recommendations**: Provide specific improvements needed

## Usage

Validate a skill directory to ensure it meets all CI/CD quality gates and requirements:

```bash
# Validate skill with explicit path
python3 scripts/main.py skill-ci-checklist

# Run in demo mode (validates itself)
python3 scripts/main.py --demo

# Check skill with custom parameters
python3 scripts/main.py --params '{"skill_path": "path/to/skill"}'
```

The skill checks:
- All required files exist (SKILL.md, README.md, scripts/main.py, pull.md)
- README contains required sections (Overview, Features, Use Cases, Parameters, Example Output)
- SKILL.md contains required YAML fields (name, track, version, summary)
- Python code has valid syntax and required handlers (argparse, demo, params, error handling)
- Documentation shows minimum quality (246+ words)

## Use Cases

- Pre-merge quality gates for skill submissions
- Validate skill consistency across repository
- Identify documentation gaps
- Ensure code structure compliance
- Generate quality reports for skill authors

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
| skill_path | string | Yes | Path to skill directory to validate |
| skill_name | string | No | Name of the skill being validated |

## Example Output

```json
{
  "ok": true,
  "data": {
    "skill": "skill-ci-checklist",
    "timestamp": "2026-02-07T09:12:00",
    "metrics": {
      "total_checks": 24,
      "passed": 22,
      "failed": 0,
      "warnings": 2,
      "quality_score": 91.7,
      "status": "excellent"
    },
    "checks_by_severity": {
      "critical": 4,
      "high": 8,
      "medium": 6,
      "low": 6
    },
    "critical_issues": [],
    "recommendations": [
      "All quality gates passed",
      "Consider expanding usage examples"
    ]
  }
}
```

