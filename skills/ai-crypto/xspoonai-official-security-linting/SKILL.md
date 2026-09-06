---
name: security-linting
description: Automated security scanning for Python code using Bandit.
version: 1.0.0
author: SpoonOS Contributor
tags: [security, code-quality, python, bandit]
---

# Security Linting

Automated security scanning for Python code to detect common vulnerabilities like hardcoded secrets, injection flaws, and unsafe function usage.

## Quick Start

```python
# Run security scan on current directory
scan_result = await agent.run_tool("security_scan", path=".")
print(scan_result)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [security_scan.py](scripts/security_scan.py) | Scans Python files/directories for security issues |

## Environment Variables

None required. Uses local `bandit` installation (will be installed if missing).

## Best Practices

1. Run scans before committing code.
2. Review high-severity issues immediately.
3. Use `# nosec` to suppress false positives (use sparingly).
