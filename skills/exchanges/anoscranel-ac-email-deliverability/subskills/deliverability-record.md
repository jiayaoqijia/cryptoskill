---
name: deliverability-record
domain: software-engineering/deliverability-record
trigger: "Writing the record of a domain's deliverability state and actions."
anti_trigger: "Not for the send itself, and not for the marketing content calendar."
scope: "The written record: DNS state, loops, thresholds, and actions taken."
status: seedling
---

# Deliverability record

## Standard

The deliverability record holds the state a future responder needs when placement breaks at the worst hour: the DNS authentication inventory and who owns each record, the sending identities and what rides them, the feedback loops and their thresholds, the suppression and sunset policies in force, and the dated actions already taken — every policy raise, every provider migration, every incident and its resolution.

Its value is the incident that has not happened yet. Placement failures arrive with urgent pressure to change something, and the record converts that into a bounded question: what changed since the last verified state. Without it, the team re-litigates SPF mechanisms from memory while the invoices land in spam; with it, the diff against the last good state is a few minutes of reading.

Primary sources: <https://support.google.com/a/answer/81126> and <https://dmarc.org/overview/>.

## Decision rules

- Record the full DNS inventory — SPF mechanisms and lookup count, DKIM selectors and rotation dates, DMARC policy and report addresses — with the owner of each record.
- Record each sending identity: subdomain, mail classes, warm-up dates, and current signals.
- Record loop status: bounce webhook endpoints, complaint loops registered, and the thresholds in force.
- Record policy and hygiene rules in force: suppression, sunset horizon, import quarantine.
- Every action is a dated entry: policy raises, provider changes, incident findings, and their resolution.
- The record is the audit trail for changes; DNS and list state that are not written down are presumed unknown.

## Procedure

1. Assemble the DNS inventory with owners, dates, and the SPF lookup count.
2. List sending identities with their warm-up history and signal sources.
3. Tabulate loop registrations, endpoints, and thresholds in force.
4. Write the hygiene policies as rules, not intentions.
5. Add dated entries for every change and every incident.
6. Re-read the record before any placement change: the diff against the last good state is the first diagnostic.

## Anti-patterns

- SPF and DKIM knowledge that lives in the person who set them up and nowhere else.
- An incident resolved but never described in the record, so the next responder repeats the diagnosis.
- Records that name no owner, so expiry and rotation silently stop happening.
- Thresholds enforced in code but unwritten, so nobody notices when they drift.
- A record updated only during incidents, so the good states are exactly the ones missing.

## Done checklist

- [ ] DNS inventory with owners and dates.
- [ ] Identities with warm-up and signal history.
- [ ] Loops and thresholds tabulated.
- [ ] Hygiene rules written as rules.
- [ ] Dated entries for actions and incidents.
- [ ] Diff-against-last-good-state is the standing diagnostic.

## Sources

- Sender guidelines from a major receiver: <https://support.google.com/a/answer/81126>
- DMARC overview for policy-state context: <https://dmarc.org/overview/>
- RFC 7489 for report and alignment semantics: <https://datatracker.ietf.org/doc/html/rfc7489>
