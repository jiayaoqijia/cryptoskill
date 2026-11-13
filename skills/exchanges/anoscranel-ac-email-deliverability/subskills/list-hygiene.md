---
name: list-hygiene
domain: software-engineering/list-hygiene
trigger: "Keeping the address list from poisoning the sending domain."
anti_trigger: "Not for growing the list or marketing copy, and not for legal advice."
scope: "Permission, engagement decay, and the addresses that poison a domain."
status: seedling
---

# List hygiene

## Standard

The list is the deliverability asset and its main liability. Addresses enter, and then two clocks start: permission and engagement. Permission decays when the basis for sending changes — an address collected for order updates will not tolerate a marketing playbook, even if it once ticked a broad box. Engagement decays quietly; an address that has not opened anything in a year is statistically indistinguishable, to a filter, from an address that never existed, and sending to enough of them produces the pattern filters associate with spam.

The craft is a set of mechanical hygiene rules: never email an address that did not grant permission recorded somewhere; never re-add a suppressed address because a colleague found an old export; sunset non-engagers on a stated horizon; and treat every imported list as hostile until verified, because the fastest way to destroy a domain is to load an address list that someone else already burned.

Primary sources: <https://support.google.com/a/answer/81126> and <https://datatracker.ietf.org/doc/html/rfc8058>.


## Decision rules

- Record the permission basis with the address: where, when, and for what class of mail.
- Suppress on unsubscribe, complaint, or hard bounce; suppression is permanent until the owner re-subscribes.
- Define the engagement horizon and sunset addresses that cross it, re-permissioning only with a fresh opt-in.
- Quarantine imported lists; verify before merging; never mix an unverified import into a warm sending identity.
- Send class-aligned mail only: what the recipient permitted is the class, not what the sender hopes.
- Audit the list for recycled and role addresses — postmaster, abuse, sales — and remove them from anything transactional-unrelated.

## Procedure

1. Inventory address sources and confirm a recorded permission basis for each segment.
2. Define the sunset horizon and the re-permission path for non-engagers.
3. Establish the import quarantine: verify a sample, check recycled-address patterns, then merge or reject.
4. Wire suppression into every send path; any address suppressed anywhere is suppressed everywhere.
5. Schedule a recurring hygiene pass: sunsets, role addresses, engagement recalculation.
6. Record list segments and hygiene actions with dates in the deliverability record.

## Anti-patterns

- The old spreadsheet someone "cleaned" by deleting the bounces once.
- Re-adding suppressed addresses after finding a bigger, newer export of the same list.
- A sunset horizon of never, with the list ageing into a hard-bounce farm.
- Marketing blasts to addresses granted only transactional permission.
- Judging list health by size instead of by the engagement distribution of its tails.

## Done checklist

- [ ] Permission basis recorded per segment.
- [ ] Suppression wired across all send paths.
- [ ] Sunset horizon defined and enforced.
- [ ] Import quarantine with verification before merge.
- [ ] Mail class aligned to permission class.
- [ ] Hygiene pass scheduled and recorded.

## Sources

- Sender guidelines from a major receiver: <https://support.google.com/a/answer/81126>
- RFC 8058, one-click unsubscribe: <https://datatracker.ietf.org/doc/html/rfc8058>
- Complaint context: <https://datatracker.ietf.org/doc/html/rfc5965>
