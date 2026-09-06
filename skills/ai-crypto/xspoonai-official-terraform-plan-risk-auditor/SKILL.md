---
name: terraform-plan-risk-auditor
track: ai-productivity
version: 0.1.0
summary: Analyze Terraform plan JSON for risky changes (destroy/replace/iam/network/public exposure) and output a structured risk report.
description: Analyze Terraform plan JSON for risky changes and blast radius.
author: guangyusong
tags:
  - terraform
  - iac
  - security
  - risk
---

## Description

Analyze Terraform plan JSON (from `terraform show -json plan.out`) for risky changes like destroys, replaces, IAM changes, and potential public exposure.

## Inputs

```json
{
  "plan_json": {"resource_changes": []},
  "plan_json_text": "{...}",
  "plan_path": "path/to/plan.json",
  "max_findings": 50,
  "focus": "security|cost|all"
}
```

Notes:
- Provide exactly one of `plan_json`, `plan_json_text`, or `plan_path`.
- `focus` filters findings (`security`, `cost`, or `all`).

## Outputs

Success:
```json
{
  "ok": true,
  "data": {
    "demo": false,
    "summary": {"create": 0, "update": 0, "delete": 0, "replace": 0, "total_changes": 0},
    "risk_score": 0,
    "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "findings": [],
    "top_resources": []
  }
}
```

Error:
```json
{
  "ok": false,
  "error": "...",
  "details": {"message": "..."}
}
```

## Usage

Demo mode:
```bash
python3 scripts/main.py --demo
```

With parameters:
```bash
python3 scripts/main.py --params '{"plan_path": "./plan.json"}'
```

Via stdin:
```bash
echo '{"plan_path": "./plan.json"}' | python3 scripts/main.py
```

## Examples

```bash
python3 scripts/main.py --params '{"plan_json": {"resource_changes": []}}'
```

## Error Handling

All errors return JSON with `ok:false` and exit with a non-zero code.
