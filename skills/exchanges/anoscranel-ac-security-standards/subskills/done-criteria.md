---
name: done-criteria
domain: security-hardening/done-criteria
trigger: "Asking what done means for a security or hardening task — the artifacts and evidence that must exist before the work counts as finished."
anti_trigger: "Performing the hardening work itself, or choosing which specific control fixes a defect; that craft sits outside this leaf (use ac-security-engineer)."
scope: "Definition of done per hardening-task class; the evidence record owed at hand-off"
status: "seedling"
---

# Done Criteria

## Standard

A hardening pass is done when its evidence exists, not when effort stops. The universal record:

- **The verification target**: the ASVS 5.0 level chosen (L1, L2, L3) and the reason, recorded durably. Personal or payment data is not done below L2.
- **The change list**: each modification mapped to the requirement or finding it closes. An unmapped fix is an unverified fix.
- **The evidence bundle**: test results, scan outputs, review note, kept with the change.
- **The residual-risk statement**: findings accepted rather than fixed, each with severity, owner, and expiry or review date. ⚠️ "Accepted-risk expiry" is practice convention; no single standard mandates one.

## Decision rules

Pick the task class below; "done" means its items plus the universal record. When two classes apply, both lists apply.

## Procedure

**Threat model of a feature or system.** Done when the document holds: the trust boundaries drawn, the threats enumerated per boundary, and for each threat a decision (mitigate, accept, transfer) with an owner. A diagram alone is not a threat model.

**Hardening one endpoint, flow, or component.** Done when: input validation and output encoding are in place; the applicable ASVS chapter requirements for the chosen level are each accounted for (met, or logged as accepted risk); negative tests exist for the abuse cases the change claims to stop (injection probes, cross-tenant reads, replay).

**Authentication, session, or authorization work.** Done when: the flows are tested end-to-end including recovery and logout; object-level checks are proven with cross-user negative tests; token lifetimes and storage are stated in writing against the current guidance edition.

**Dependency and CVE triage.** Done when every in-scope CVE has a disposition: fixed, unreachable-with-reason, or accepted-risk with owner and review date. Any KEV-listed (known-exploited) item still open blocks "done" outright. ⚠️ SLA numbers per severity are organisational policy, not standard text.

**Security testing gate in CI.** Done when the gate fails the build on the agreed finding classes, the agreed classes are written down, and a tuning path exists for false positives. A scanner that only warns is a report, not a gate.

**LLM or agent feature.** Done when: the feature is checked against the current OWASP LLM/Agentic Top 10 (editions per the standards map); indirect-prompt-injection and tool-abuse cases have explicit negative tests; the model's permitted tool surface is enumerated in writing.

**Logging readiness.** Done when the security events the team will alert on are listed, each maps to a log statement, and a redaction check confirms no secrets or personal data at rest in those logs.

**Incident and disclosure readiness.** Done when the first-hour steps and the contact path exist in writing (a `security.txt` per RFC 9116 where the org runs one), and — for EU in-scope products — the CRA reporting clocks (24 h / 72 h from 2026-09-11) are assigned to a named owner.

**Review of one diff.** Done when the review note records: the target level, the checks run, the findings (or the explicit "none found"), and the merge verdict.

## Anti-patterns

- Evidence kept in chat or memory instead of with the change.
- Accepted risks without owner or review date.

## Done checklist

- [ ] Could a reviewer who was not present reconstruct what was verified, against which edition, and what was knowingly left open? If the answers live only in someone's memory, it is not done.

## Sources

- ASVS 5.0 levels: https://asvs.dev · RFC 9116: https://www.rfc-editor.org/rfc/rfc9116 · EU CRA reporting clocks: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R2847 · CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
