---
name: security-testing
domain: security-hardening/security-testing
trigger: "Setting up or fixing the security gates in CI: scanners, secret detection, dependency checks, AI-code review rules."
anti_trigger: "Which dependencies to fix first once scanners fire (subskills/cve-triage.md); the manual pre-merge review pass (subskills/security-review.md)."
scope: "SAST, DAST, secret scan and AI-code gates in CI"
status: "seedling"
---

# Security Testing

## Standard

- The process frame is NIST **SSDF SP 800-218**: v1.1 final 3 Feb 2022; the v1.2 revision is an **Initial Public Draft (17 Dec 2025)**, comments closed 30 Jan 2026 — not final (https://csrc.nist.gov/pubs/sp/800/218/r1/ipd). Groups: PO, PS, PW, RV. Companion **SP 800-218A** (Jul 2024) is authorship-neutral: all source is evaluated before use.
- Scanner silence is not evidence of safety: single-tool SAST catches only **11–27%** of seeded flaws, under 45% combined and tuned; one pipeline's pattern SAST missed ~97.8% of Z3-proven AI-code findings (⚠️ single preprint); runtime violations ran ~2× for AI code while SAST showed both equally safe (arXiv:2607.00107).
- A WAF is not a gate: **1,207 unique bypasses** across tested framework/WAF combinations, every framework falling to at least one bypass class (WAFFLED, ACSAC 2025).
- AI-code vulnerability density sits in a **27–44%** band across matched-task studies (quote the range with method); AI-assisted commits leak secrets at ~2× baseline (GitGuardian 2026 ⚠️).

## Decision rules

1. Gates block; advisories die — every gate output routes to a tracker with an owner, or the build fails.
2. Layer the scanners: secret scan + dependency registry check + SAST + SCA. No single tool suffices.
3. Order: pre-commit secret scan (sub-second) → commit-time blocking gates → pre-release DAST/IAST → runtime WAF. Cheapest deterministic check earliest.
4. Keep untrusted-PR jobs in a separate workflow with no release secrets (pipeline parasitism: Ultralytics, tj-actions, GhostAction, Nx waves).
5. Tune before blocking: a gate that fires 500 false positives gets disabled within a week — measure the FP rate per rule first.

## Procedure

1. Secret scanning, three layers: gitleaks pre-commit (sub-second, no network); trufflehog in CI with `--results=verified` (verification separates live from dead); GitHub push protection as the last net (free on public repos). Scan full history, not just HEAD.
2. SAST: Semgrep with rules you own, `--error` so the merge blocks on your critical rules.
3. Dependency gate: registry-existence + pin on every new or AI-suggested package, then SCA (OSV-Scanner, Dependabot) — `subskills/supply-chain.md` for the pin rule, `subskills/cve-triage.md` for triage.
4. AI-written-code gate: (a) secrets gate on history; (b) SAST beside, never alone; (c) registry-existence + pin on suggested deps; (d) independent human review by a named owner, on a **different model/provider from the producer**, with out-of-scope edits (lockfiles, CI config) reviewed as the top-cited failure mode.
5. DAST/IAST pre-release against staging with auth (SSDF Produce group); every finding a ticket with an owner.
6. Record the evidence: gate results, justified exceptions, approvals — an append-only trail, also the audit sample.

## Anti-patterns

- One SAST tool as the whole programme; a gate that only comments.
- WAF-in-front as the answer to injection (parameterise — `subskills/injection.md`).
- Treating "the agent ran the tests" as a gate result.

## Done checklist

- [ ] Secret scan in pre-commit, CI, push protection; history scanned; SAST `--error` on owned critical rules.
- [ ] Registry-existence + pin gate on every dependency; AI code has a named human owner and independent review step.
- [ ] Untrusted-PR jobs secret-free and separated; every gate failure lands in a tracker with an owner; no silent suppressions.

## Sources

- Primary: NIST SP 800-218/218A; WAFFLED (ACSAC 2025); arXiv:2607.00107 (⚠️ preprint); GitGuardian 2026 (⚠️ vendor).
- <https://owasp.org/www-project-web-security-testing-document/>
- <https://cheatsheetseries.owasp.org>
