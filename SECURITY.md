# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |
| Older   | No        |

## Reporting a Vulnerability

**Please do not file a public issue for security vulnerabilities.**

To report a vulnerability, email **security@cryptoskill.app** with:

- Description of the vulnerability
- Steps to reproduce
- Affected skill(s) or component(s)
- Potential impact assessment

### Response Timeline

| Stage | Timeline |
|-------|----------|
| Acknowledgment | Within 48 hours |
| Initial assessment | Within 1 week |
| Fix development | Depends on severity |
| Public disclosure | After fix is released |

## Scope

### In Scope

- **Skill content security** — malicious code in skill scripts, hardcoded credentials, unsafe external calls
- **Website vulnerabilities** — XSS, injection, or other web security issues on cryptoskill.app
- **Repository integrity** — unauthorized modifications, supply chain concerns
- **Data exposure** — leaking of API keys, secrets, or private data in skill files

### Out of Scope

- **Individual skill functionality bugs** — if a skill produces incorrect data or fails to connect to an API, that is a bug, not a security issue. Please open a regular bug report instead.
- **Issues in upstream dependencies** — report these to their upstream projects.
- **Third-party API security** — vulnerabilities in the APIs that skills connect to should be reported to those projects directly.
- **Social engineering attacks**
- **Denial of service through expected resource usage**

## Responsible Disclosure

We ask that you:

1. Give us reasonable time to fix the issue before public disclosure
2. Make a good faith effort to avoid data destruction and service disruption
3. Do not access or modify data belonging to others
4. Act in good faith to avoid degrading our services

We commit to:

1. Acknowledging your report promptly
2. Keeping you informed of our progress
3. Crediting you (if desired) when we publish the fix
4. Not pursuing legal action against good-faith security researchers
