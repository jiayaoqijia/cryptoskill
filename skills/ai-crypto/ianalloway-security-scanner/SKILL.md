---
name: security-scanner
description: "Scan code and dependencies for security vulnerabilities. Check npm audit, pip safety, and common security issues."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🔒",
        "requires": { "bins": ["npm", "pip", "grep"] },
        "credentials": [],
      },
  }
---

# Security Scanner

Scan your projects for security vulnerabilities in dependencies and common code issues.

## Dependency Scanning

### NPM Projects

Check for known vulnerabilities in npm packages:

```bash
npm audit
```

Get JSON output for parsing:

```bash
npm audit --json | jq '{vulnerabilities: .metadata.vulnerabilities, total: .metadata.vulnerabilities.total}'
```

Fix automatically where possible:

```bash
npm audit fix
```

### Python Projects

Check Python dependencies with pip-audit:

```bash
pip install pip-audit && pip-audit
```

Or use safety (requires free API key from https://safetycli.com/):

```bash
pip install safety && safety check
```

Check requirements.txt directly:

```bash
pip-audit -r requirements.txt
```

## Code Security Checks

### Find Hardcoded Secrets

Search for potential API keys and secrets:

```bash
grep -rn "api_key\|apikey\|secret\|password\|token" --include="*.js" --include="*.ts" --include="*.py" --include="*.env" .
```

### Find Dangerous Functions

Check for potentially dangerous code patterns:

```bash
# JavaScript/TypeScript - eval usage
grep -rn "eval(" --include="*.js" --include="*.ts" .

# Python - exec/eval usage
grep -rn "exec(\|eval(" --include="*.py" .

# SQL injection risks
grep -rn "execute.*%s\|execute.*f\"" --include="*.py" .
```

### Check for Debug Code

Find debug statements that shouldn't be in production:

```bash
grep -rn "console.log\|debugger\|print(" --include="*.js" --include="*.ts" --include="*.py" .
```

## Environment Security

### Check for Exposed .env Files

```bash
find . -name ".env*" -not -path "*/node_modules/*" -not -path "*/.git/*"
```

### Verify .gitignore

Ensure sensitive files are ignored:

```bash
cat .gitignore | grep -E "\.env|secret|credential|\.pem|\.key"
```

## Docker Security

### Scan Docker Images

Using Trivy (install: https://trivy.dev/):

```bash
trivy image your-image:tag
```

### Check Dockerfile Best Practices

```bash
# Check for root user
grep -n "USER root" Dockerfile

# Check for latest tag
grep -n "FROM.*:latest" Dockerfile
```

## Quick Security Audit

Run a quick audit on a project:

```bash
# For npm projects
echo "=== NPM Audit ===" && npm audit 2>/dev/null || echo "Not an npm project"

# Check for secrets
echo "=== Potential Secrets ===" && grep -rn "password\|secret\|api_key" --include="*.js" --include="*.py" --include="*.ts" . 2>/dev/null | head -20

# Check for .env files
echo "=== Environment Files ===" && find . -name ".env*" -not -path "*/node_modules/*" 2>/dev/null
```

## GitHub Security Features

### Enable Dependabot

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Security Policy Template

Create `SECURITY.md` in your repo to establish responsible disclosure guidelines.

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [npm audit docs](https://docs.npmjs.com/cli/v8/commands/npm-audit)
- [pip-audit](https://pypi.org/project/pip-audit/)
- [Trivy Scanner](https://trivy.dev/)
- [GitHub Security Features](https://docs.github.com/en/code-security)

## Tips

- Run security scans in CI/CD pipelines
- Set up Dependabot for automatic dependency updates
- Use pre-commit hooks to catch secrets before commit
- Review third-party dependencies before adding them
- Keep dependencies updated regularly
