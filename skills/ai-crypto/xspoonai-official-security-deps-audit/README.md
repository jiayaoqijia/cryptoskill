# security-deps-audit (Track: enterprise-skills)

Scan dependencies for known security vulnerabilities and CVEs

## Overview

This skill checks project dependencies against a vulnerability database to identify known security issues. It reports CVE IDs, severity levels, and recommended fixes for vulnerable packages.

## Features

- **CVE Detection**: Identify known vulnerabilities in dependencies
- **Severity Levels**: Categorize vulnerabilities by impact (critical, high, medium, low)
- **Fix Recommendations**: Suggest updated versions that patch vulnerabilities
- **Compliance Reporting**: Generate audit reports for security review
- **Database Updates**: Integrate with latest vulnerability databases

## Use Cases

- Prevent vulnerable dependencies in production
- Scan before each deployment
- Generate security audit reports
- Track vulnerability remediation
- Ensure compliance with security standards

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
| dependencies | array | Yes | Array of {name, version} objects |
| vulnerability_db | object | No | Custom vulnerability database |

## Example Output

```json
{
  "ok": true,
  "data": {
    "demo": true,
    "timestamp": "2026-02-07T09:09:37",
    "project": "web-application",
    "audit": {
      "summary": {
        "total_packages": 8,
        "safe_packages": 1,
        "vulnerable_packages": 7,
        "critical_vulnerabilities": 2,
        "high_vulnerabilities": 5,
        "security_score": 10,
        "audit_status": "critical"
      },
      "critical": [
        {
          "package": "django",
          "version": "3.2.9",
          "cve": "CVE-2021-35042",
          "title": "SQL injection in QuerySet.annotate()",
          "cvss_score": 9.8,
          "severity": "critical",
          "exploit_available": true
        },
        {
          "package": "pyyaml",
          "version": "5.4",
          "cve": "CVE-2020-14343",
          "title": "Arbitrary code execution via YAML parser",
          "cvss_score": 9.8,
          "severity": "critical"
        }
      ],
      "high": [
        {
          "package": "requests",
          "version": "2.20.0",
          "cve": "CVE-2023-32681",
          "cvss_score": 7.5,
          "severity": "high"
        }
      ],
      "safe": [
        {
          "package": "flask",
          "version": "2.0.0",
          "status": "safe"
        }
      ]
    }
  }
}
```
