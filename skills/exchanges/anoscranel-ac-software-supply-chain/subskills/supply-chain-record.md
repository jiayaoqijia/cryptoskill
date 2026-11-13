---
name: supply-chain-record
domain: software-engineering/supply-chain-record
trigger: "Writing down where every external input comes from."
anti_trigger: "Not for the security review itself, and not for the release notes."
scope: "The written record of sources and verifications."
status: seedling
---

# Supply-chain record

## Standard

The supply-chain record states the sources of external code, the trust boundary each crosses, and the verifications applied at each crossing. It is the map a responder reaches for during an incident: which registries feed the builds, which artifacts are signed and by whom, which checks would fire on substitution, and which repositories would need attention if a given package were compromised.

Its second purpose is auditability of the trust decisions themselves. Vendoring here, mirroring there, a scope rule here, an exception granted there — each is a decision with a reason and a date, and without a record the reasons live only in the recollection of whoever made them. The record turns the supply chain from a set of habits into a set of decisions someone can review, challenge, and change.

Primary source: <https://slsa.dev/>.

## Decision rules

- Record each external source: registry, mirror, vendored copy, direct URL.
- Record the trust boundary and the verification at each crossing.
- Record signing identities and provenance expectations per artifact class.
- Record the resolution order and the refusal rules that enforce it.
- Record exceptions — a source trusted without the usual check — with the reason, period, and approver.
- Reconcile the record against actual configuration quarterly, and log the reconciliation.

## Procedure

1. Inventory every external source and its class.
2. Record the crossing's verification per source.
3. Record signing identities and provenance expectations.
4. Record resolution order and refusal rules.
5. Exception-log every deviation with approver and period.
6. Reconcile quarterly and record the result.

## Anti-patterns

- A record of policy that has never been compared to actual inputs.
- Exceptions granted forever with no review.
- Signing identities recorded without the rotation procedure.
- A resolution order documented as intent while the reality diverged.
- No incident use case in mind — a record nobody could respond from.

## Done checklist

- [ ] External sources inventoried by class.
- [ ] Verifications recorded per crossing.
- [ ] Identities and provenance recorded.
- [ ] Resolution order and refusals recorded.
- [ ] Exceptions logged with approver and period.
- [ ] Quarterly reconciliation logged.

The record earns its keep the day a public disclosure lands: the first question is always which builds consumed the affected artifact, and a record organised by source answers it in minutes. A record organised by policy takes an afternoon, and the afternoon is what the incident window does not have.

## Sources

- Supply-chain integrity levels: <https://slsa.dev/>
- In-toto attestations: <https://in-toto.io/>
- Reproducible builds: <https://reproducible-builds.org/>
