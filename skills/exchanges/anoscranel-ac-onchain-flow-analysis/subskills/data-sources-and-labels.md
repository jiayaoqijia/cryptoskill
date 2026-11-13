---
name: data-sources-and-labels
domain: crypto-trading/data-sources-and-labels
trigger: "Choosing where on-chain data comes from and how much to trust its labels."
anti_trigger: "Not for predicting prices, and not for address attribution forensics."
scope: "Explorers, indexers, and label providers, and the difference between a verified and an asserted identity."
status: seedling
---

# Data sources and labels

## Standard

On-chain analysis begins with a source decision that most commentary skips. Explorers show canonical ledger state; indexers add interpretation and convenience; label providers attach identity claims. Each layer adds convenience and removes certainty, and the record must say which layer a figure came from.

The distinction that matters most is between verified and asserted identity. A contract's own registry entry, an issuer's published address, or a signed message can verify an identity. A third-party label is an assertion by someone who may be right. Both are usable; only one is evidence.

Primary sources: <https://ethereum.org/en/developers/docs/> and <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Every figure cites its layer: explorer, indexer, or label provider, with the date.
- Identity claims are classed verified (registry, issuer disclosure, signed message) or asserted (third-party label).
- Where two label providers disagree, record both and treat the identity as unknown.
- Address clusters are treated as hypotheses; one actor can operate many addresses.
- Contract addresses are verified against the issuer's own disclosure where one exists.
- If the only source is a social-media screenshot, the figure is recorded as unverified.

## Procedure

1. Identify the question and the addresses it concerns.
2. Pull canonical ledger state from an explorer for each address.
3. Cross-check with at least one indexer and note discrepancies.
4. Classify each identity claim as verified or asserted, with its source.
5. Record cluster hypotheses separately from identity claims.
6. Build the source table with layer, date, and confidence.

## Anti-patterns

- Treating a label provider's tag as fact.
- Using an indexer's derived metric without its definition.
- Quoting a chart from a screenshot without the underlying addresses.
- Assuming one wallet equals one actor.
- Mixing data from different dates in one claim.

## Done checklist

- [ ] Question and addresses identified.
- [ ] Canonical state pulled per address.
- [ ] Second source cross-checked; discrepancies noted.
- [ ] Identities classified verified or asserted with sources.
- [ ] Cluster hypotheses recorded separately.
- [ ] Source table built with layer, date, confidence.

## Sources

- Ethereum developer documentation on data and analytics: <https://ethereum.org/en/developers/docs/>
- Empirical measurement of venue-level flows during stress: <https://arxiv.org/abs/2608.03616>
- Entity and disclosure context: <https://www.sec.gov/investor>

The source table is the part of the record that ages best: vendors change, labels rot, and a reader two years later needs to know which layer produced a number before deciding whether to trust it again. Write the layer, the date, and the exact query or address list, not just the finding.
