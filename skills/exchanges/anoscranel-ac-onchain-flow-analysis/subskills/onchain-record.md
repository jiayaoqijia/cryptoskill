---
name: onchain-record
domain: crypto-trading/onchain-record
trigger: "Writing the record of an on-chain analysis so it can be checked and falsified."
anti_trigger: "Not for making the trade decision, and not for the trade journal."
scope: "The written on-chain record: claim, ledger evidence, label status, confidence, and falsifier."
status: seedling
---

# On-chain record

## Standard

An on-chain analysis that exists only as a chart cannot be checked. The record states the claim, the addresses and the window it rests on, the label status of every identity involved, the exclusions applied, the confidence, and the evidence that would show the claim wrong. It is written so a reader can re-run the query.

The record's most important field is the falsifier. "Exchange inflows rose" is a description; "exchange inflows rose, which would be falsified if the increase is entirely cold-wallet rotation, checkable by the venue's disclosed cold addresses" is an analysis.

Primary sources: <https://ethereum.org/en/developers/docs/> and <https://osf.io/prereg/>.

## Decision rules

- Every claim names its addresses, its window, and its exclusions.
- Every identity carries a label status: verified, asserted, or unknown.
- Confidence is stated per claim and capped by the weakest label involved.
- A falsifier is written for each claim before it is used in a memo.
- Excluded address classes are listed, so the reader knows what was left out.
- The record is append-only; corrections are dated amendments.

## Procedure

1. State the question and the claim in one sentence each.
2. List addresses and the window, with exclusions.
3. Record label status per identity.
4. State the confidence and the weakest link behind it.
5. Write the falsifier and how it would be checked.
6. File the record and reference it from any memo that uses the claim.

## Anti-patterns

- Recording a claim without the address list.
- Omitting the exclusions.
- Stating confidence without naming the weakest label.
- Using the claim in a memo before writing the falsifier.
- Editing the record silently after a correction.

## Done checklist

- [ ] Question and claim stated separately.
- [ ] Addresses, window, and exclusions listed.
- [ ] Label status recorded per identity.
- [ ] Confidence stated with the weakest link named.
- [ ] Falsifier written with its check method.
- [ ] Record filed and referenced.

## Sources

- Ethereum developer documentation on address and transfer data: <https://ethereum.org/en/developers/docs/>
- Pre-registration practice for falsifiers before use: <https://osf.io/prereg/>
- Empirical flow measurement under stress: <https://arxiv.org/abs/2608.03616>

Keep the record with the addresses and the query, not just the conclusion, so that a later reader can re-derive the figure when a label provider changes its mind. The record's value compounds: each one makes the next analysis cheaper, and a set of them makes a monitoring series possible.
