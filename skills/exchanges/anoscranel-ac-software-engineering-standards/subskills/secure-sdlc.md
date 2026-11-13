---
name: secure-sdlc
domain: software-engineering/secure-sdlc
trigger: "\"where does security fit in our process\", \"set up the secure SDLC\", \"map our process to SSDF\", \"shift-left or shield-right\"."
anti_trigger: "Selecting or implementing a control such as auth, input validation, crypto or secrets; threat modelling a design; CVE triage; SBOM and signing policy. Any of those is security-controls work outside this tree, not this leaf."
scope: "Which security activity sits in which lifecycle phase (SSDF map); not the controls"
status: "seedling"
---

# Secure SDLC

## Standard

- **NIST SSDF SP 800-218 v1.1** (Final, 3 Feb 2022): four practice groups — Prepare the Organization, Protect the Software, Produce Well-Secured Software, Respond to Vulnerabilities (https://csrc.nist.gov/pubs/sp/800/218/final). v1.2 is a draft with comments closed 30 Jan 2026.
- **Microsoft SDL** is the phase-gate ancestor — training, requirements, design with threat modelling, static analysis, verification, release, response — and **OWASP Top 10** is awareness, not a test plan; ASVS Level 1/2/3 is the verifiable set.
- **Shift-left versus shield-right**: pre-merge tooling catches known-bad patterns cheaply and misses authorisation and chained flaws, which surface at runtime or in a pentest.
- **US driver**: EO 14028 (May 2021) drove vendor self-attestation; OMB M-26-05 (Jan 2026) replaced it with a risk-based approach.

## Decision rules

1. One row per phase. An activity without a phase is a policy nobody runs.
2. Requirement phase: abuse cases and security NFRs ship with the feature.
3. Design phase: a threat model exists for each new trust boundary or external dependency.
4. Implementation phase: static analysis and dependency scanning run left of merge.
5. Release phase: the artifact is signed and an SBOM is produced.
6. Response phase: triage is keyed to exploitability — exploited-in-the-wild outranks a theoretical score.
7. This leaf maps the phases only. It does not choose the control.

## Procedure

1. Write the phases this project has: specify, design, implement, verify, release, respond.
2. Fill the table with the activities that already exist, cheapest first: ```markdown
 | Phase | Activity | Gate | Evidence |
 |---|---|---|---|
 | implement | dependency scan | blocking | CI scan report |
 | design | threat model for new boundary | blocking | review record |
 | release | artifact signing | blocking | attestation log |
 ```
3. Mark each row blocking or advisory. A gate that never blocks is a dashboard.
4. Add the missing rows: dependency scanning, secret scanning, threat modelling. Give each row an owner and a cadence.
5. Route the responder path: who triages an advisory, on what clock, with what rule.
6. Re-check the map quarterly, and report blanks as gaps, not empty cells.

## Anti-patterns

- A checklist with no phase, no gate and no owner.
- An awareness poster standing in for verification.
- Static analysis set to advisory, so every finding is waived.
- Shift-left tooling treated as sufficient for authorisation flaws.
- Control selection restated inside the phase map.

## Done checklist

- [ ] Each phase has its activities written down.
- [ ] Every row marked blocking or advisory, with evidence.
- [ ] Response path defined with a triage rule and an owner.
- [ ] Signing and SBOM steps exist before the first release.
- [ ] Map reviewed; gaps reported.

## Sources

- <https://csrc.nist.gov/pubs/sp/800/218/final>
- <https://www.wiley.law/alert-OMB-Rescinds-Secure-Software-Development-Mandate-in-Favor-of-a-Risk-Based-Approach>
- https://csrc.nist.gov/pubs/sp/800/218/final
