---
name: threat-model
domain: security-hardening/threat-model
trigger: Starting a feature or system design, or reviewing an existing one, and needing to name what can go wrong before choosing controls.
anti_trigger: Fixing an already-identified defect (subskills/injection.md and its siblings); running a pre-merge diff check (subskills/security-review.md).
scope: STRIDE/data-flow model, abuse cases, risk rating
status: seedling
---

# Threat Modeling

## Standard

- Shostack's Four Question Framework: What are we working on? What can go wrong? What are we going to do about it? Did we do a good job? (https://shostack.org/files/papers/The_Four_Question_Framework.pdf).
- STRIDE — Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege — as implemented in OWASP Threat Dragon (https://owasp.org/projects/threat-dragon; https://devguide.owasp.org/en/04-design/01-threat-modeling/).
- OWASP SAMM: five business functions (Governance, Design, Implementation, Verification, Operations), 15 practices, 3 maturity levels (https://owaspsamm.org/model/).
- NIST SSDF SP 800-218 v1.1 (final 2022-02-03) as the outer vocabulary; v1.2 is still a draft.

## Decision rules

1. Threat-model every story — analyse the slice you are building now, not the whole system.
2. The four questions plus one STRIDE pass over a data-flow diagram is the complete method.
3. Rank by likelihood × impact against effort. Effort is the scarce axis: a control costing two days to maintain rarely pays for itself.
4. List crown jewels only — source code, production credentials, DNS, customer personal data, payment access, founder identity. Everything else is secondary.
5. State the evidence honestly: no controlled study shows threat modelling prevents breaches. A 2026 IEEE TSE review of 109 sources found zero controlled experiments (https://doi.org/10.1109/tse.2026.3662996). Do the one-hour version because it is cheap, not because ROI is proven.
6. Write the deliberate-ignore list: bespoke APT targeting, unfunded compliance theatre, threats to data you do not hold.

## Procedure

1. 10 min — draw the system: one box per component, arrows for data flow, a dashed line at every trust boundary (browser→API, API→DB, your code→third-party API, LLM→tools).
2. 15 min — ask the four questions at each boundary. Park speculative findings.
3. 15 min — run STRIDE once over the diagram; skip letters that clearly do not apply.
4. 10 min — score each finding 1–5 on likelihood and impact, divide by effort, take the top three.
5. 10 min — write mitigations as backlog items and one security ADR (SSDF PO.1.2). Fixing is a later task.

## Anti-patterns

- Conflating "found it" with "fixed it" — that is what makes threat modelling feel heavyweight.
- Agonising over STRIDE variants; a 2024 replication found them "not different enough to make a practical impact" (https://doi.org/10.1142/s0218194023500651).
- Running FAIR's Monte Carlo machinery. Use its vocabulary (frequency × magnitude) only; a peer-reviewed critique found inaccurate results in identified cases (https://doi.org/10.1016/j.cose.2019.101659).
- Skipping the model because the project is small. Exposure is punished in minutes: Palo Alto Unit 42's incident-response telemetry puts 80% of compromises inside 24 hours (⚠️ vendor telemetry, not independently replicated).

## Done checklist

- [ ] Diagram drawn with every trust boundary marked.
- [ ] Four questions answered per boundary.
- [ ] One STRIDE pass recorded.
- [ ] Findings ranked; top three chosen; the rest parked with a reason.
- [ ] Mitigations exist as backlog items; one security ADR written.
- [ ] The deliberate-ignore list is written down.

## Sources

- Primary: Shostack, Four Questions framework; OWASP Threat Dragon (https://owasp.org/www-project-threat-dragon/); OWASP Developer Guide (https://owasp.org/www-project-developer-guide/); OWASP SAMM (https://owasp.org/www-project-samm/); NIST SP 800-218 (https://csrc.nist.gov/pubs/sp/800/218/final).
- STRIDE replication: Mbaka & Tuma, 2024, https://doi.org/10.1142/s0218194023500651.
- Exposure telemetry: Palo Alto Unit 42 incident-response reporting (⚠️ vendor source).
