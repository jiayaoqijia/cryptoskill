---
name: subject-requests
domain: software-engineering/subject-requests
trigger: "Handling an access, erasure, or portability request as a workflow."
anti_trigger: "Not for legal determination, and not for identity policy."
scope: "Access, erasure, and portability requests as an engineering workflow."
status: seedling
---

# Subject requests

## Standard

A subject request is a deadline with an evidence requirement. The requester has a legal right to a response within a stated period, and the organisation must be able to show what was found and what was done. That makes the request an engineering workflow rather than a support task: it needs a verified identity, an exhaustive search across the inventory, a machine-readable output where portability applies, and an audit record of the whole exchange.

The failure mode is incompleteness that looks complete. A search that queries the primary database returns a tidy answer and misses the support system, the analytics table, and the email archive, and the requester — or a regulator — discovers the omission.

Primary sources: <https://ico.org.uk/> and <https://www.w3.org/Privacy/>.

## Decision rules

- Record the verification method for identity and its strength relative to the data's sensitivity.
- Record the search scope: every store in the inventory, not the obvious one.
- Record the output format for access and for portability, which differ.
- Record the deadline and the internal milestone that leaves review time.
- Record the erasure path and its interaction with retention exceptions.
- Record the audit artefact that evidences the search and the response.

## Procedure

1. Verify identity and record the method used.
2. Search every store in the inventory and record each result, including empty ones.
3. Assemble the response in the required format.
4. For erasure, apply the deletion path and record exceptions that block it.
5. Record the audit artefact with timestamps.
6. Review the elapsed time against the deadline.

## Anti-patterns

- Searching only the primary database.
- Treating an empty search result as proof of absence.
- Using the same output for access and portability.
- Silently declining the parts blocked by a retention exception.
- No audit artefact, so the response cannot be evidenced later.

## Done checklist

- [ ] Identity verification recorded.
- [ ] Search scope recorded per store.
- [ ] Output format recorded.
- [ ] Deadline and milestones recorded.
- [ ] Erasure path and exceptions recorded.
- [ ] Audit artefact recorded.

The internal milestone matters more than the legal deadline, because the deadline includes review time that is lost if the search finishes on the last day: recording an internal date at seventy percent of the period gives the review somewhere to happen, and makes the difference between a compliant response and a rushed one.


## Sources

- Subject rights guidance: <https://ico.org.uk/>
- Web privacy standards: <https://www.w3.org/Privacy/>
- NIST privacy framework: <https://www.nist.gov/privacy-framework>
