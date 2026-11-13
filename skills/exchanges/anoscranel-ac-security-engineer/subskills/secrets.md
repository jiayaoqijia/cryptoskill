---
name: secrets
domain: security-hardening/secrets
trigger: Storing, injecting, scanning or rotating credentials and keys — or responding to one that leaked.
anti_trigger: Choosing algorithms and managing cryptographic keys for encryption (subskills/crypto-use.md); cloud account and IaC configuration (subskills/cloud-iac.md).
scope: Storing, injecting, scanning, rotating secrets; leak response
status: seedling
---

# Secrets

## Standard

- OWASP Secrets Management Cheat Sheet: centralise, never hardcode, least privilege, audit access (https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html). NIST SP 800-57 Part 1 Rev 5 (2020-05) defines cryptoperiods for cryptographic keys.
- Twelve-Factor III: store config in environment variables; the litmus test is "could the codebase be made open-source right now, without compromising any credentials?" (https://12factor.net/config).
- Evidence: GitGuardian's *State of Secrets Sprawl 2026* (2026-03-17): 28,649,024 new hardcoded secrets in public GitHub commits (+34% year-on-year, eight of the ten fastest-growing leak types are AI services); over 64% of credentials valid in 2022 were still valid in January 2026. The 2025 DBIR measured a 94-day median to remediate a leaked GitHub secret.

## Decision rules

1. Rotate first, rewrite history second: GitHub's guidance is to revoke/rotate the exposed credential first — a history rewrite "may not be warranted".
2. Use the platform's native secret store first; add a free-tier manager only when one secret is shared across services.
3. `.env` is acceptable only gitignored, never committed, never the production source of truth.
4. Prefer short-lived OIDC federation over long-lived CI keys: a token per job, at least one trust condition, no long-lived cloud credential.
5. Scope one key per service and per environment; never reuse a credential across services, so a leak cannot pivot.
6. No industry standard defines a rotation cadence for vendor API keys. ⚠️ Do not dress a made-up "90 days" as a standard.

## Procedure

1. Scan full history, not just HEAD: `gitleaks detect --log-opts="--all"` or `trufflehog git file://.`. Layer the scans: gitleaks pre-commit, trufflehog in CI (`--results=verified`), GitHub push protection last.
2. Store secrets in the platform store or a manager; reference by name in code, never by value.
3. On a leak: **revoke at the issuer first (human-gated — revoking credentials is irreversible)**; issue a scoped replacement; update store and CI; redeploy; confirm the old value is dead.
4. Only then scrub where feasible: `git filter-repo --sensitive-data-removal`, force-push all refs, ask the host to purge cached views. Forks and clones keep the value; collaborators rebase, not merge.
5. Log the incident: what leaked, when, blast radius — future-you's memory.

## Anti-patterns

- Running `git filter-repo` while the key is still live. The key is the vulnerability; the commit is the receipt.
- Echoing secrets in build logs, `set -x`, or CI debug output.
- One long-lived cloud key stored in CI instead of per-job OIDC tokens.
- The leak surface is wider than the repo: JS bundles, CI logs, screenshots, `.env` files (Intruder: 42,000+ exposed tokens across 5 million scanned apps, ⚠️ vendor).

## Done checklist

- [ ] Full-history scan runs pre-commit and in CI; push protection enabled on the code host.
- [ ] Secrets live in the platform store or a manager, referenced by name.
- [ ] CI uses OIDC federation; no long-lived cloud keys.
- [ ] Leak SOP rehearsed: revoke → replace → redeploy → confirm → scrub → log.
- [ ] Each key scoped per service and environment.

## Sources

- Primary: OWASP Secrets Management Cheat Sheet; Twelve-Factor III; NIST SP 800-57 Pt 1 Rev 5; GitHub docs (secret scanning, push protection, removing sensitive data, Actions OIDC); GitGuardian State of Secrets Sprawl 2026; Verizon DBIR 2025; gitleaks and trufflehog repos; Intruder JS-bundle scan (⚠️ vendor).
- <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>
- <https://www.cisa.gov>
