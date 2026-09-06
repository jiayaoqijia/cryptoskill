---
name: k8s-manifest-security-auditor
track: enterprise-skills
version: 0.1.0
summary: Lint Kubernetes YAML manifests for security and reliability risks (privileged, hostNetwork, hostPath, runAsRoot, missing limits).
description: Static analysis for common Kubernetes manifest security and reliability risks.
author: guangyusong
tags:
  - kubernetes
  - k8s
  - security
  - yaml
---

## Description

Audit Kubernetes YAML manifests (multi-doc supported) for common security and reliability issues without requiring cluster access.

## Inputs

```json
{
  "manifests_yaml": "...multi-doc yaml...",
  "manifest_path": "k8s.yaml",
  "ruleset": "baseline|restricted",
  "max_findings": 200
}
```

Notes:
- Provide exactly one of `manifests_yaml` or `manifest_path`.
- `ruleset` influences some severities (e.g., missing limits).

## Outputs

Success:
```json
{
  "ok": true,
  "data": {
    "demo": false,
    "summary": {
      "documents": 0,
      "resources_scanned": 0,
      "findings_total": 0,
      "by_severity": {"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0}
    },
    "risk_score": 0,
    "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "findings": []
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
python3 scripts/main.py --params '{"manifest_path":"./k8s.yaml","ruleset":"restricted"}'
```

Via stdin:
```bash
echo '{"manifests_yaml":"apiVersion: v1\nkind: Pod\n..."}' | python3 scripts/main.py
```

## Examples

```bash
python3 scripts/main.py --params '{"manifests_yaml":"apiVersion: v1\nkind: Pod\nmetadata:\n  name: p\nspec:\n  containers: [{name: c, image: alpine}]"}'
```

## Error Handling

All errors return JSON with `ok:false` and exit with a non-zero code.
