# license-audit (Track: enterprise-skills)

Comprehensive license audit for project dependencies with compliance checking and risk assessment

## Overview

This skill performs deep analysis of software dependencies to identify licensing compliance issues. It uses a comprehensive license database to classify licenses by risk level, check against corporate policies, and provide actionable recommendations for remediation.

## Features

- **Comprehensive License Database**: SPDX-based license classification with metadata
- **License Categories**: Permissive, weak-copyleft, and strong copyleft (GPL, AGPL) licenses
- **Policy Enforcement**: Configure forbidden licenses and categories
- **Risk Assessment**: Critical, high, medium, and low risk levels
- **Compliance Scoring**: Calculate overall project compliance percentage
- **Detailed Reports**: Issues, warnings, and info messages with recommendations
- **Multiple Licenses**: Handle dual-licensed packages (e.g., "Apache-2.0 OR MIT")
- **Commercial Compatibility**: Track which licenses allow commercial use

## Use Cases

- Audit dependencies before publishing/shipping
- Enforce company licensing policies
- Identify problematic dependencies (GPL, AGPL)
- Generate compliance reports for legal review
- Prevent accidental license violations
- Track license categories across projects

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
| project_name | string | No | Name of project being audited |
| dependencies | array | Yes | Array of {name, version, license} objects |
| policy | object | No | Custom compliance policy rules |

### Policy Object
```json
{
  "forbidden_licenses": ["GPL-2.0", "AGPL-3.0"],
  "forbidden_categories": ["copyleft"],
  "warn_categories": ["weak-copyleft"],
  "allow_unknown": true
}
```

## Example Output

```json
{
  "ok": true,
  "data": {
    "project_name": "sample-python-project",
    "audit": {
      "total_dependencies": 11,
      "compliance_score": 81.8,
      "status": "non-compliant",
      "summary": {
        "compliant": 9,
        "warnings": 0,
        "critical": 2,
        "unknown": 0
      },
      "critical_issues": [
        {
          "package": "ffmpeg-python@0.2.3",
          "license": "GPL-3.0",
          "severity": "critical",
          "recommendation": "Replace with compatible alternative"
        }
      ]
    }
  }
}
```
