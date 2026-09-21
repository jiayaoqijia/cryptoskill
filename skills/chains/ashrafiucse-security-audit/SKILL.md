---
name: security-audit
description: Comprehensive security audit of any codebase. Maps the project's stack, scans for hardcoded secrets, vulnerable dependencies, injection flaws, auth/authz bugs, weak crypto, misconfigurations, container/IaC risks, and data exposure, then writes a prioritized SECURITY-AUDIT.md report with file:line evidence, CWE mapping, and fix recommendations. Use when the user asks for a security audit, security review, vulnerability scan, pentest prep, or project hardening.
license: MIT
---

# Security Audit

Full-project, read-only security review that ends in a written report. Works for any language/stack.

## Ground rules

- **Read-only.** Never modify, delete, move, or "fix" files. Never run destructive or mutating commands. Never actually exploit a finding — reasoning about exploitability on paper is enough.
- **Evidence or it didn't happen.** Every finding must cite `path/file.ext:line` and a short code excerpt you actually read.
- **Verify before reporting.** Read surrounding context to kill false positives (test files, examples, fixtures, obviously-fake values).
- **No network required**, but if network is available, the `dependency-vulns` and `cve-research` skills use live databases.

## Phase 0 — Recon: build the security map

Do NOT read every file. Probe cheaply first:

```bash
rg --files -g '!node_modules' -g '!vendor' -g '!dist' -g '!build' -g '!target' -g '!coverage' | head -100
rg --files -g 'package.json' -g 'package-lock.json' -g 'yarn.lock' -g 'pnpm-lock.yaml' \
   -g 'requirements*.txt' -g 'Pipfile*' -g 'pyproject.toml' -g 'poetry.lock' \
   -g 'Gemfile*' -g 'Cargo.toml' -g 'Cargo.lock' -g 'composer.json' -g 'composer.lock' \
   -g 'go.mod' -g 'go.sum' -g 'pom.xml' -g '*.csproj' -g 'pubspec.yaml' -g 'mix.exs'
rg --files -g 'Dockerfile*' -g 'docker-compose*' -g '*.tf' -g '*.yaml' -g '*.yml' -g '.env*' -g '*.conf' -g 'nginx*' -g '*.toml'
git log --oneline -5 2>/dev/null; git remote -v 2>/dev/null
```

Record in the report's "Stack" section:
- Languages + frameworks + versions (from manifests and config)
- Entry points (HTTP handlers, CLI mains, background jobs, webhooks)
- Infra: Docker/K8s/Terraform/CI configs, cloud providers
- Auth mechanism, database(s), external services
- Repo size class (if huge, sample smartly — prioritize first-party code over vendored/generated code)

## Phase 1 — Deep scans

For each applicable domain, **read the sibling skill and follow it** (paths are relative to this skill's directory):

| If the project has... | Read and follow |
|---|---|
| Any source code at all | `../secrets-detection/SKILL.md` |
| Any dependency manifest | `../dependency-vulns/SKILL.md` |
| Input handling / queries / templates / subprocesses | `../injection-flaws/SKILL.md` |
| GraphQL server / `.graphql` schema files | `../graphql-security/SKILL.md` |
| Android/iOS files (`AndroidManifest.xml`, `Info.plist`, mobile code) | `../mobile-security/SKILL.md` |
| Laravel/PHP project (`composer.json` with laravel/framework, `artisan`, Blade views) | `../laravel-security/SKILL.md` |
| Django/Python project (`manage.py`, `settings.py`, Django in requirements) | `../django-security/SKILL.md` |
| Rails project (`Gemfile` with rails, `app/controllers`) | `../rails-security/SKILL.md` |
| Spring/Java project (`pom.xml`/`build.gradle` with spring dependencies) | `../spring-security/SKILL.md` |
| Login, sessions, tokens, permissions | `../auth-review/SKILL.md` |
| Crypto, hashing, tokens, certs | `../crypto-review/SKILL.md` |
| HTTP servers, CORS, headers, cookies, CI configs | `../config-hardening/SKILL.md` |
| Dockerfile / compose / K8s / Terraform | `../container-iac-security/SKILL.md` |
| PII, secrets handling, logging, file output | `../data-exposure/SKILL.md` |

Then, if network is available: `../cve-research/SKILL.md` for live CVE checks against the exact stack versions found in Phase 0.

Scan hygiene:
- Always exclude `node_modules/ vendor/ dist/ build/ target/ .git/ __pycache__/ .venv/ venv/ coverage/` and minified `*.min.js`
- Prioritize: auth code > input handlers > data access > config > everything else
- For repos > ~2k files, scan by category (auth files first, then routes/controllers, then DB layers) rather than exhaustively

## Phase 2 — Triage

Rate each finding:

| Severity | Meaning |
|---|---|
| **Critical** | Directly exploitable now: RCE, SQLi on reachable input, auth bypass, leaked prod secrets, known-CVE-with-public-exploit in the actual dependency version |
| **High** | Exploitable with preconditions: stored XSS, IDOR on sensitive objects, weak password hashing, exposed admin endpoints |
| **Medium** | Defense-in-depth failures: missing headers, verbose errors, wildcard CORS with credentials, weak randomness in non-security context |
| **Low** | Hygiene: outdated-but-patched deps, missing lockfile, debug flags in non-prod config |

Also tag **Likelihood** (reachable from unauthenticated input? internal only?) and **Effort to fix** (S/M/L).

**Completeness gate:** walk `references/owasp-top10.md` top to bottom. For any category with project surface but no recorded findings, either scan it now or mark it "not assessed" in the report — never skip silently.

## Phase 3 — Report

Write `SECURITY-AUDIT.md` in the project root (this is the only file you create). Compute the knowledge-base header line with `ls ../cve-research/vuln-db/entries/ | wc -l` and the newest filename's date prefix — it shows the user how fresh their checkout is:

```markdown
# Security Audit — <project>
Date: YYYY-MM-DD | Scope: <commit hash / "working tree"> | Auditor: security-skills v<version>
Knowledge base: <N> vuln-db entries (newest YYYY-MM-DD) | Live checks: OSV.dev + CISA KEV

## Stack
<2–5 lines from Phase 0>

## Summary
| Severity | Count |
|---|---|
| Critical | n | ...

## Findings
### SEC-001: <short title> — CRITICAL
- **Where:** `path/file.ext:42`
- **CWE:** CWE-89 (SQL Injection)
- **Evidence:**
  ```<lang>
  <the actual offending lines>
  ```
- **Impact:** what an attacker gains, concretely
- **Fix:** specific, actionable change (show corrected code when short)
- **References:** CWE / CVE / OWASP link if applicable

### SEC-002: ...

## What looks good
<controls that are done right — honest positives>

## Recommended fix order
1. SEC-001 (critical, small effort) → ...
```

End the session with a 3–5 line verbal summary: total counts, the single worst issue, and the first action to take.

## Notes

- If the user asks to **fix** findings afterward, that's fine — but do it as a separate, explicitly-approved step after the report is delivered.
- If a finding is uncertain, report it as "Possible — needs verification" with what to check, rather than silently dropping it.
