---
name: dmarc-policy
domain: software-engineering/dmarc-policy
trigger: "Setting or raising a DMARC policy from monitoring to enforcement."
anti_trigger: "Not for the underlying SPF or DKIM records, and not for vendor choice."
scope: "The policy layer, alignment, and the reports that tell the truth."
status: seedling
---

# DMARC policy

## Standard

DMARC is the policy that tells a receiver what to do when SPF and DKIM both authenticate but neither aligns with the visible From domain. Alignment is the referee: the envelope or signing domain must match the From domain in a stated way — exact or relaxed — for the authentication to count toward the policy. Without DMARC, a receiver that fails SPF sees an unrelated envelope and makes up its own mind; with it, the domain owner states the consequence: none, quarantine, or reject.

The rollout discipline comes from the reports. A DMARC record names an address that receives aggregate and failure reports from participating receivers; the aggregate report shows which sources authenticate and align, and which do not, at scale. The policy is raised from none to quarantine to reject only when the reports show that legitimate sources are aligned and the remainder looks like forgery, because reject first means discovering a legitimate billing system by its disappearance.

Primary sources: <https://datatracker.ietf.org/doc/html/rfc7489> and <https://dmarc.org/overview/>.

## Decision rules

- Publish the record with at least the aggregate-report address before any enforcement, and read the reports.
- State the alignment mode deliberately: relaxed tolerates subdomains, exact does not.
- Begin at none; raise to quarantine; reject only when reports show alignment coverage of all legitimate sources.
- Inventory every legitimate sending source from the reports before raising the policy — the report is the discovery tool.
- Treat unaligned-but-legitimate sources in reports as setup work owed before enforcement, not as acceptable losses.
- Re-check reports after every provider or architecture change; enforcement is not a steady state.

## Procedure

1. Publish the record with aggregate-reporting addresses and policy none.
2. Collect reports for a stated window; tabulate sources by authentication and alignment.
3. Fix each unaligned legitimate source: SPF include, DKIM selector, or the From domain it uses.
4. Raise to quarantine when the legitimate set is fully aligned; continue collecting.
5. Raise to reject when reports are stable and remaining failures are not the sender's own systems.
6. Keep the report address live permanently; enforcement is maintained by the reports.

## Anti-patterns

- Publishing reject without a reporting window, then finding the invoicing system in the logs.
- Ignoring the aggregate reports after enforcement, so a new unaligned SaaS tool fails silently.
- Confusing authentication success with alignment success; the report distinguishes them.
- Treating the report address as optional once the policy is reject.
- One-time alignment fixes with no re-verification trigger in the record.

## Done checklist

- [ ] Record published with report addresses.
- [ ] Reports collected and sources tabulated.
- [ ] All legitimate sources aligned before each policy raise.
- [ ] Policy raised along none → quarantine → reject with windows.
- [ ] Report address monitored after enforcement.
- [ ] Re-verification trigger set for provider changes.

## Sources

- RFC 7489, the DMARC specification: <https://datatracker.ietf.org/doc/html/rfc7489>
- The overview document: <https://dmarc.org/overview/>
- Sender guidelines from a major receiver: <https://support.google.com/a/answer/81126>
