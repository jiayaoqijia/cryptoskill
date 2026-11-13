---
name: holder-cohorts
domain: crypto-trading/holder-cohorts
trigger: "Segmenting holders by age and size to read behaviour rather than identity."
anti_trigger: "Not for identifying individuals, and not for predicting price."
scope: "Age and size cohorts, cost-basis proxies, and cohort behaviour over a cycle."
status: seedling
---

# Holder cohorts

## Standard

Cohorts are the honest alternative to whale-watching. Instead of asking who holds, cohort analysis asks how holdings are distributed by age and size, and how those distributions change. A market where large balances are being distributed into many small ones looks different from one where small balances consolidate into large ones, and the change is visible even when every identity is unknown.

Age cohorts use the last movement of a balance as a proxy for when it was acquired. The proxy is imperfect — custody rotation resets it — but the shape of the distribution over time is still informative, and it does not depend on a label provider being right.

Primary sources: <https://ethereum.org/en/developers/docs/> and <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Cohorts are defined by ledger-observable properties: balance size bands and age since last movement.
- Cost basis is a proxy derived from the price at last movement; label it as a proxy, never as fact.
- Exchange and custodian addresses are excluded from cohort statistics or placed in their own cohort.
- Cohort shifts are compared across a stated window, not day to day.
- A shift in distribution is recorded as a finding about concentration, not about intention.
- Where cohort boundaries change, the series is restated and the restatement noted.

## Procedure

1. Define size bands and age bands before pulling data.
2. Exclude or isolate exchange and custodian addresses.
3. Compute the distribution for two dates at least a month apart.
4. Compare the shift by band.
5. Derive the cost-basis proxy for the largest cohorts.
6. Record the finding with the definitions used.

## Anti-patterns

- Choosing band boundaries after seeing the result.
- Treating age since last movement as true holding period for custodial balances.
- Including exchange omnibus wallets in a "whale" cohort.
- Reading a one-day change as a trend.
- Presenting cost-basis proxies as measured cost.

## Done checklist

- [ ] Size and age bands defined in advance.
- [ ] Exchange and custodian addresses excluded or isolated.
- [ ] Distributions computed for two dated snapshots.
- [ ] Shift by band recorded.
- [ ] Cost-basis proxy derived and labelled.
- [ ] Definitions recorded with the finding.

## Sources

- Ethereum developer documentation on ledger data: <https://ethereum.org/en/developers/docs/>
- Empirical measurement of holder behaviour under stress: <https://arxiv.org/abs/2608.03616>
- Investor education on concentration and disclosure: <https://www.investor.gov/introduction-investing>

Cohort work is slow and unglamorous, and that is the point: it produces statements like 'the largest size band shrank by a fifth while the middle band grew' rather than 'whales are accumulating'. The former can be checked by anyone with the same definitions; the latter cannot be checked at all.
