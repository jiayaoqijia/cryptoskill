---
name: verification-level
domain: security-hardening/verification-level
trigger: Deciding how thoroughly an application must be verified, and which OWASP ASVS level and Top 10 mapping to use as the target.
anti_trigger: Reviewing one diff against the chosen target (subskills/security-review.md); running automated scans (subskills/security-testing.md).
scope: Choose ASVS 5.0 level; map Top 10:2025 to controls
status: seedling
---

# Verification Level

## Standard

- OWASP ASVS **5.0.0**, released 2025-05-30 (release tag `v5.0.0_release`, https://github.com/OWASP/ASVS/releases). The restructure is total: 14→17 chapters, ~286→345 requirements, **every requirement renumbered**. Any ASVS v4 ID is stale.
- ASVS chapters V1–V17: V1 Encoding & Sanitization, V2 Validation & Business Logic, V3 Web Frontend Security, V4 API & Web Service, V5 File Handling, V6 Authentication, V7 Session Management, V8 Authorization, V9 Self-contained Tokens, V10 OAuth & OIDC, V11 Cryptography, V12 Secure Communication, V13 Configuration, V14 Data Protection, V15 Secure Coding & Architecture, V16 Security Logging & Error Handling, V17 WebRTC (https://asvs.dev).
- Levels are cumulative: L1 baseline (low assurance, largely black-box), L2 recommended for applications handling personal data, financial transactions or business-critical functions, L3 high assurance (medical, critical infrastructure).
- OWASP Top 10 **2025** (announced 2025-11-06, final January 2026) and API Security Top 10 **2023** — the only official API edition (https://owasp.org/API-Security/editions/2023/en/0x04-release-notes).

## Decision rules

1. An app handling personal or payment data targets **L2**, not L1. ⚠️ The L1/L2/L3 percentage splits are vendor-reported; the direction (L2 for PII/payments) is consistent across four-plus secondary sources.
2. "Roughly 350" is OWASP's own count; the exact 345 is community-derived from the release CSV. ⚠️
3. Map every Top 10 category to ASVS chapters: A01 Broken Access Control→V8; A05 Injection→V1.2; A10 Exceptional Conditions→V16; A03 Supply Chain→V13 policy plus SCA tooling (ASVS does not verify third-party code).
4. API work maps to V4 plus the 2023 API Top 10; authentication and sessions sit in the new standalone V6, V7, V9, V10.
5. Re-baseline the level on each material change (new data class, new payment flow, new integration).
6. Record the level decision and its reason in an ADR; the level is a business decision about harm, not a technical maximum.

## Procedure

1. Classify the app: data classes held, money moved, users affected.
2. Choose the level: L1 for internal/low-value, L2 for personal/payment data, L3 only when a regulator or contract demands it.
3. Build the verification checklist from the ASVS chapters that apply (V1, V2, V3, V4, V5, V6, V7, V8, V11, V13, V16 are the usual set).
4. Walk the Top 10:2025 list as a cross-check; every category must trace to at least one checklist item.
5. Verify as black-box at L1; add code review for the L2 items that tests cannot reach.
6. Re-run the checklist whenever the classification changes.

## Anti-patterns

- Citing an ASVS v4 requirement ID — it does not exist in 5.0.
- Targeting L3 "for safety" — it burns time on medical-grade controls a small app never needs.
- Treating ASVS as sufficient for supply chain: it verifies your code, not your dependencies (subskills/supply-chain.md).
- Quoting an "API Security Top 10 2025" — no such official edition exists.

## Done checklist

- [ ] App classified by data and money.
- [ ] Level chosen and recorded with its reason.
- [ ] Checklist built from named ASVS 5.0 chapters.
- [ ] Every Top 10:2025 category maps to a checklist item.
- [ ] No v4 requirement IDs cited anywhere.
- [ ] Re-baseline trigger defined.

## Sources

- Primary: https://asvs.dev and the OWASP Top 10 2025 <https://owasp.org>; CISA guidance <https://www.cisa.gov>.
