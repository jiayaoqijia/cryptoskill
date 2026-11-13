---
name: framework-and-scope
domain: security-hardening/framework-and-scope
trigger: "Choosing a framework and drawing the audited boundary."
anti_trigger: "Not for security technique, and not for standards editions."
scope: "Choosing the framework and drawing the audited boundary honestly."
status: seedling
---

# Framework and scope

## Standard

SOC 2 reports against trust-criteria categories the organisation selects; ISO 27001 certifies an information-security management system within a declared boundary. Both audit a scope, and the scope decision precedes all others: what systems, data, and processes are inside the boundary, and what is explicitly out. A scope drawn generously ("everything we do") fails on depth; a scope drawn to hide the risky half fails on honesty, and both failure modes surface at the audit.

The honest scope covers what customers actually receive. If a subprocessor handles customer data, it belongs inside the boundary or inside a disclosed carve-out with its own evidence. If a system is excluded, the exclusion is stated in the report rather than silently omitted. Auditors test the boundary against reality — the report that describes a smaller or larger company than the one present is the first finding.

Primary sources: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2> and <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>.

## Decision rules

- Choose the framework from the customers' requirements, not from engineering preference.
- Draw the boundary from what touches customer data, then from what auditors can traverse.
- Every subprocessor handling in-scope data is either inside the boundary or a disclosed carve-out.
- State exclusions in the report; silent exclusions become findings.
- Fix the criterion categories (e.g. security plus availability) before evidence collection starts.
- Record the framework edition and scope statement with dates in the compliance record.

## Procedure

1. List customer contracts' compliance requirements; identify the framework they name.
2. Draft the boundary from data-flow diagrams of what customer data touches.
3. Mark each subprocessor in or out, with the disclosure language for the out cases.
4. Select the criteria categories beyond the mandatory security one.
5. Write the scope statement and date it against the framework's current edition.
6. Review the scope against reality quarterly; amend before the audit, not after.

## Anti-patterns

- A scope copied from a template that does not match the actual architecture.
- The risky system quietly left outside the boundary.
- Selecting criteria categories post-audit to dodge a weak area.
- Scope prose so broad the audit cannot depth-test anything.
- Scope written by the audit prep team without an engineer reviewing the data flows.

## Done checklist

- [ ] Framework chosen from customer requirements.
- [ ] Boundary drawn from data-flow diagrams.
- [ ] Subprocessors classified with disclosed carve-outs.
- [ ] Criteria categories fixed before evidence work.
- [ ] Scope statement dated against the edition.
- [ ] Quarterly reality review scheduled.

## Sources

- SOC 2 reporting framework: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>
- Control catalogue context: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- Security-standards catalogue context: <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1>
