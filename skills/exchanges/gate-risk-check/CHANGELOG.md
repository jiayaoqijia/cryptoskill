# Changelog — gate-info-riskcheck

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Token and address risk assessment. Trigger: is this token safe, check contract risk, is this address safe. Mode A: info_compliance_check_token_security + info_coin_get_coin_info. Mode B: Address Risk (degraded — check_address_risk not yet available).
- SKILL.md: Token Security workflow, Address Risk degradation, Report Template (7 sections), Decision Logic, Risk Level Mapping, Error Handling, Available Tools & Degradation Notes, Safety. Synced from docs/pd-vs-skills/skills/gate-info-riskcheck; tool names in underscore form.
- README.md, references/scenarios.md.

### Audit

- Read-only. Mandatory honeypot warning when detected; no investment advice; no absolute safety guarantees.
