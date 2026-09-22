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

## Mode: fix verification (re-audit)

Use when the user asks to "verify the fixes", "re-audit", "check what's fixed", or an existing `SECURITY-AUDIT.md` is present from a prior run. Never silently re-scan from zero when prior findings exist — verification comes first.

1. **Load the prior report** (`SECURITY-AUDIT.md` in project root). If missing, run the normal flow.
2. **Verify each prior finding** by reading the cited `file:line` (and its function/route context):
   - **FIXED** — the offending code is gone or the defense is present (parameterized, allowlisted, guarded, rotated secret + scrubbed history)
   - **STILL PRESENT** — evidence unchanged
   - **MOVED / REGRESSED** — code moved: re-cite the new `file:line`; if the "fix" introduced a new flaw, that's a new finding
   - Secrets: FIXED only after rotation evidence — removing the string from HEAD is not a fix (history + old deployments keep it)
3. **Then scan for NEW findings** in changed code since the prior report (`git diff <prior-commit>..HEAD` if the report records a commit) — full re-scan only if the user asks.
4. **Rewrite `SECURITY-AUDIT.md`**: per-finding status line (`FIXED` / `STILL PRESENT`, with the re-checked citation), a summary table (fixed n / open n / new n), and new findings appended with fresh SEC-NNN ids. Keep ids stable across runs — SEC-004 stays SEC-004 whether open or fixed.
5. Verbal summary: fixed count, still-open worst issue, anything the fix broke.

## Mode: incremental (PR / diff) audit — catch gaps when they land

Use when the user says "audit this PR / branch / these commits" or hands you a diff — no prior `SECURITY-AUDIT.md` needed. Early-stage math: a gap caught in the PR costs an hour; caught at ship time it costs a chain.

1. Scope the delta (read-only):
   ```bash
   bash ../security-audit/scripts/pr_diff_scope.sh <base-ref>   # default origin/main
   ```
   It prints BASE, changed files, and which sibling skills apply — verify the BASE line resolved to the ref you expected.
2. Run ONLY the dispatched skills, plus ALWAYS: `../secrets-detection/SKILL.md` over the ADDED lines, and `../dependency-vulns/SKILL.md` when any manifest/lockfile changed.
3. Audit the chain, not the line: a changed route pulls in its controller → model → view; a changed model pulls in every writer. Read the neighborhood of each change.
4. Delta matrix: disposition every actor×surface cell the delta touches (Completeness gate v2 rules unchanged — a one-file PR still gets its surfaces dispositioned).
5. Report to `SECURITY-AUDIT-PR.md` in the project root: findings cited in delta code, the delta matrix, census receipts, and a CI verdict line — `VERDICT: BLOCK` if any High+ finding is reachable from unauthenticated input, else `VERDICT: PASS`.

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

Then census the coverage targets — they seed the Phase 2 matrix:

```bash
rg -n "role|is_admin|isAdmin|middleware\(|policy|Gate::|->can\(" app/ src/ routes/ config/ 2>/dev/null | head -25
rg -n -i "webhook|queue|job|listener|command|upload|admin" app/ src/ routes/ 2>/dev/null | head -15
```

- **ACTORS** — every identity the code distinguishes: anonymous/public, authenticated user, staff/instructor/moderator, admin/tenant-admin, service/webhook caller, third-party integration. Record all, even "boring" ones.
- **SURFACES** — every place code meets an actor: public pages/catalog, auth endpoints, authenticated app, admin panel, moderation queues, uploads/downloads, webhooks, background jobs, emails, external APIs.
- If the project root has a `THREAT-MODEL.md` (from `../design-threat-review/SKILL.md`), load it: its actor×surface matrix is your seed and its threat rows are checks to disposition — design and audit share one artifact.

## Phase 1 — Deep scans

For each applicable domain, **read the sibling skill and follow it** (paths are relative to this skill's directory):

| If the project has... | Read and follow |
|---|---|
| Any source code at all | `../secrets-detection/SKILL.md` |
| Any dependency manifest | `../dependency-vulns/SKILL.md` |
| Input handling / queries / templates / subprocesses | `../injection-flaws/SKILL.md` |
| GraphQL server / `.graphql` schema files | `../graphql-security/SKILL.md` |
| LLM/AI stack (langchain/llamaindex/autogen, openai/anthropic SDKs, model files `.pkl/.pt/.gguf/.safetensors`) | `../llm-security/SKILL.md` |
| Android/iOS files (`AndroidManifest.xml`, `Info.plist`, mobile code) | `../mobile-security/SKILL.md` |
| Laravel/PHP project (`composer.json` with laravel/framework, `artisan`, Blade views) | `../laravel-security/SKILL.md` |
| Django/Python project (`manage.py`, `settings.py`, Django in requirements) | `../django-security/SKILL.md` |
| Rails project (`Gemfile` with rails, `app/controllers`) | `../rails-security/SKILL.md` |
| Spring/Java project (`pom.xml`/`build.gradle` with spring dependencies) | `../spring-security/SKILL.md` |
| Login, sessions, tokens, permissions | `../auth-review/SKILL.md` |
| Stateful business flows (order/payment/invoice, checkout, submit/approve/publish, signup/verify, refunds, provisioning) | `../flow-security/SKILL.md` — load it BEFORE route-level grepping for transactional apps |
| Course/e-learning platform (courses, lessons, enrollments, cohorts, previews, subscriptions) | `../course-platform-security/SKILL.md` — persona-driven (public/student/admin) |
| Spec/PRD/design doc shared BEFORE implementation (no or early code) | `../design-threat-review/SKILL.md` — produces THREAT-MODEL.md; at audit time, load it as the Phase 0 matrix seed |
| Crypto, hashing, tokens, certs | `../crypto-review/SKILL.md` |
| HTTP servers, CORS, headers, cookies, CI configs | `../config-hardening/SKILL.md` |
| Dockerfile / compose / K8s / Terraform | `../container-iac-security/SKILL.md` |
| PII, secrets handling, logging, file output | `../data-exposure/SKILL.md` |

Then, if network is available: `../cve-research/SKILL.md` for live CVE checks against the exact stack versions found in Phase 0.

Scan hygiene:
- Always exclude `node_modules/ vendor/ dist/ build/ target/ .git/ __pycache__/ .venv/ venv/ coverage/` and minified `*.min.js`
- Prioritize: auth code > input handlers > data access > config > everything else
- For repos > ~2k files, scan by category (auth files first, then routes/controllers, then DB layers) rather than exhaustively
- **Enumeration discipline:** sampling is for prioritizing WHICH skill runs next — inside a skill's check, its grep output is a census. Count the hits (`wc -l`), disposition every line (finding / verified-safe / not-assessed), never `head`-truncate an inventory. A pattern that mixes frameworks' noise (React `!!` vs Blade `{!!`) must be globbed to the framework's file type first. An unexamined tail is an unaudited tail.
- **Census receipts:** for every census scan, record `hits=N, dispositioned=N` (a hit is dispositioned when you have read it and assigned finding / verified-safe / not-assessed). Receipts ship in the report's Census receipts table; any census with dispositioned < hits means the audit is INCOMPLETE and the report must say so in its first line.

## Phase 1.5 — Optional tool bridges (skip silently if absent)

```bash
bash ../security-audit/scripts/probe_tools.sh .
```

If a scanner is installed, run its probe line (all read-only) and ingest the results alongside manual scans:

| Tool | Catches that greps miss | Ingestion rule |
|---|---|---|
| gitleaks / trufflehog | secrets in **full git history** (deleted-then-rotated keys are invisible to worktree regex) | report as `../secrets-detection/SKILL.md` findings; verify before CRITICAL |
| semgrep | cross-file taint flows, language-semantic sinks | treat hits as leads — re-verify `file:line` and source→sink yourself; drop tool-only findings that fail context triage |
| osv-scanner / npm audit / pip-audit | offline dep CVEs | merge + dedupe with the OSV API results from `../dependency-vulns/SKILL.md` |
| checkov / kube-linter / tfsec | IaC misconfigs beyond the grep set | map to `../container-iac-security/SKILL.md` categories |

Rules: tools are leads, not verdicts — every reported finding still needs evidence you read yourself. Never install tools on the user's machine; never run a tool in a mode that writes/modifies. No tools found → proceed with the manual phases exactly as below.

## Phase 2 — Triage

Rate each finding:

| Severity | Meaning |
|---|---|
| **Critical** | Directly exploitable now: RCE, SQLi on reachable input, auth bypass, leaked prod secrets, known-CVE-with-public-exploit in the actual dependency version |
| **High** | Exploitable with preconditions: stored XSS, IDOR on sensitive objects, weak password hashing, exposed admin endpoints |
| **Medium** | Defense-in-depth failures: missing headers, verbose errors, wildcard CORS with credentials, weak randomness in non-security context |
| **Low** | Hygiene: outdated-but-patched deps, missing lockfile, debug flags in non-prod config |

Also tag **Likelihood** (reachable from unauthenticated input? internal only?) and **Effort to fix** (S/M/L).

**Completeness gate v2 — disposition everything, skip nothing.** Build the coverage matrix from the Phase 0 census: every ACTOR × every SURFACE cell gets exactly one disposition:

- ✅ **FINDING** — a finding covers this cell (cite SEC-NNN)
- 🟢 **VERIFIED-SAFE** — you checked it and a control holds (name the control)
- ⬜ **NOT-ASSESSED** — you didn't get to it; the report lists these cells by name

Gate rules:
1. Walk `references/owasp-top10.md` top to bottom — each category maps to matrix cells or carries its own disposition. Never skip silently.
2. **Moderation/queue rule**: any artifact an unprivileged actor creates that a privileged actor opens (reviews, tickets, messages, submissions, uploaded filenames) gets its own cell — that is where student→admin XSS lives (see `../course-platform-security/SKILL.md` §6.5 and laravel-security Step 4's privilege-direction table).
3. A cell with no disposition means the audit is INCOMPLETE — not small. Ship the full matrix in the report; untested surface is unreported risk.

## Phase 2.5 — Chain analysis (compound impact)

Individual severities understate real risk — pentest-grade reports show how findings COMBINE. Before writing the report, walk the finding list and try to complete known chains:

| Chain | Components | Compound impact |
|---|---|---|
| SSRF → metadata → creds | SSRF + IMDSv1/no hop limit + instance role | Cloud account takeover |
| XSS → session theft | any XSS + token in localStorage/sessionStorage | Account takeover |
| Moderation-queue XSS | unprivileged-submitted content + raw render in a staff detail view | Staff/admin account takeover (the approval workflow itself is the delivery mechanism) |
| Redirect → code theft | open redirect + OAuth/SSO callback carrying code/token in URL | Account takeover |
| Upload → RCE | upload-to-webroot + parse gadget (image/php) | Server RCE |
| Pollution → RCE | prototype pollution + gadget (child_process/template env) | Server RCE |
| Enumeration → stuffing | user enumeration + no rate limit + weak policy | Mass compromise |
| CI → supply chain | PR-title injection / pull_request_target + secrets | Repo/package takeover |
| IDOR → privesc | IDOR + mass assignment (role/isAdmin) | Admin access |
| Flow-state confusion | unguarded transition (F1/F5) + terminal artifact (invoice/refund/credit) | Money theft, cross-user invoicing |
| Webhook spoof → paid | unverified callback (F8) + status write | Free goods/services |
| TLS-off + spoof | verify=False + trusted-header authz on internal hop | Auth bypass |
| Log forging → cover | CWE-117 + audit-gap findings | Undetectable attacks |

Rules: a Medium that COMPLETES a Critical chain gets tagged `chain-critical` (its standalone severity stays, the report shows both). List completed chains in the Summary section as one-liners — "SSRF + IMDSv1 → role creds → account takeover". Chains you can ALMOST complete (one component missing) go under "What would make this worse" — that's prioritized hardening advice, not a finding.

## Phase 3 — Report

Write `SECURITY-AUDIT.md` in the project root (this is the only file you create). Compute the knowledge-base header line with `ls ../cve-research/vuln-db/entries/ | wc -l` and the newest filename's date prefix — it shows the user how fresh their checkout is:

```markdown
# Security Audit — <project>
Date: YYYY-MM-DD | Scope: <commit hash / "working tree"> | Auditor: security-skills v$(git describe --tags --always 2>/dev/null || echo dev)
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

## Coverage matrix (actor × surface — from the Phase 0 census)
| Surface ↓ · Actor → | anonymous | user | staff/mod | admin |
|---|---|---|---|---|
| Public catalog | 🟢 status+visibility filter | n/a | n/a | n/a |
| Review moderation queue | n/a | ✅ SEC-011 | 🟢 list view escaped | 🟢 role middleware |

<every cell: ✅ SEC-NNN / 🟢 verified-safe + the control / ⬜ not-assessed / n-a>

## Not assessed
- <actor × surface cell> — why, and the scan that would close it

## Census receipts
| Census | hits | dispositioned |
|---|---|---|
| Blade raw echoes (glob *.blade.php) | 206 | 206 |

## Recommended fix order
1. SEC-001 (critical, small effort) → ...
```

End the session with a 3–5 line verbal summary: total counts, the single worst issue, and the first action to take.

## Notes

- If the user asks to **fix** findings afterward, that's fine — but do it as a separate, explicitly-approved step after the report is delivered.
- If a finding is uncertain, report it as "Possible — needs verification" with what to check, rather than silently dropping it.
