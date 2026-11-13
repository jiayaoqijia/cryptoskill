---
name: policies-that-match
domain: security-hardening/policies-that-match
trigger: "Writing policies that state what the system enforces and no more."
anti_trigger: "Not for legal review, and not for the technical control design."
scope: "Policies stating what the system enforces, nothing more."
status: seedling
---

# Policies that match

## Standard

An audited policy is a claim the system must survive: "access is reviewed quarterly", "offboarding revokes access within one business day", "changes require approval before merging". Each such sentence creates a test — the auditor samples the quarter, the day, or the merge — and every sentence that does not match the system's actual behaviour creates a finding. The discipline is to write the minimum set of sentences the framework requires, each phrased at the precision the system can honestly deliver.

The failure pattern is aspirational drafting: a policy promising encryption everywhere where the system encrypts most things, or a quarterly review where the system has only run once. The repair is either to fix the system or to write "annual", never to pick the more impressive word. Policy and system are optimised together — any drift between them is a control finding that would have been cheaper to fix as a draft edit.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final> and <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1>.

## Decision rules

- Every policy sentence names a frequency and an actor the system can evidence.
- Prefer the frequency the system actually achieves over the one the draft aspires to.
- Version-controlled, changelogged, with dated approval from the named authority.
- Each control in the mapping has exactly one policy source, not duplicates across documents.
- Exceptions to policy are rare, recorded, and time-bounded — a permanent exception is a policy change in disguise.
- Policy review dates reflect actual practice, and dates measured against actual review dates *once*.

## Procedure

1. From the control mapping, list which ones require a policy statement; get the framework's exact requirement first.
2. Draft each sentence against observed practice, with real frequencies and actors.
3. Validate the sentences against what the pipeline produces: query the evidence again.
4. Version-control the change, obtain dated approval, publish with the next review date.
5. Reconcile at every pipeline change: if the system changes behaviour, the same commit carries the policy change.
6. At audit time, sample each claim against random dates yourself again.

## Anti-patterns

- "Best-efforts" in any audited sentence.
- Security policies pasted from a template that no one has reconciled against the actual system.
- Duplicate overlapping policies across documents that drift apart silently.
- The policy promising quarterly with the system producing once.
- Annual-review dates marked "reviewed" with no change record because no one knew what reviewing means.

## Done checklist

- [ ] Policy sentences matched, word by word, to evidence.
- [ ] Frequencies phrased from observed practice, not aspiration.
- [ ] Version history and dated approvals in the repo.
- [ ] One policy source per control.
- [ ] Exceptions time-bounded and recorded.
- [ ] Review dates verified against actual occurrences.

## Sources

- Control phrase requirements: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- Documentation and drift practice: <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1>
- SOC 2 framework: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>
