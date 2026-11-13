---
name: exchange-flows
domain: crypto-trading/exchange-flows
trigger: "Interpreting inflows to and outflows from exchange addresses."
anti_trigger: "Not for predicting price direction, and not for identifying individual depositors."
scope: "Inflows and outflows, what they can and cannot imply, and the custodian-versus-exchange ambiguity."
status: seedling
---

# Exchange flows

## Standard

Exchange netflow is the most quoted and least understood on-chain metric. The intuition — coins moving to exchanges precede selling, coins leaving precede holding — is plausible and frequently wrong, because exchange addresses are omnibus wallets serving many purposes: customer custody, market making, cold-storage rotation, and settlement for over-the-counter trades.

A custody reshuffle between an exchange's hot and cold wallets produces the same ledger trace as a large deposit. The metric can still be informative when the address classification is careful and the window is long, but it must be read as a proxy for activity and intention, never as a direct measure of either.

Primary sources: <https://ethereum.org/en/developers/docs/> and <https://arxiv.org/abs/2608.03616>.

## Decision rules

- Distinguish hot, cold, and settlement addresses of the same exchange; a transfer between them is not a flow.
- Netflow is meaningful over multi-day windows, not single transactions.
- A large single transfer is an event to investigate, not a signal; identify the counterparty class first.
- Custodian and market-maker wallets are excluded or flagged; they are not customer flows.
- Flows are compared against the venue's disclosed reserves where available.
- Any inference about intention carries a confidence level and a falsifier.

## Procedure

1. Build the address set for the venues in question, classified hot, cold, settlement, custodian.
2. Exclude intra-exchange transfers from the flow calculation.
3. Compute netflow over a stated window, with the exclusion rule stated.
4. Identify the largest contributors and their class.
5. Compare against venue reserve disclosures where they exist.
6. Write the inference with confidence and falsifier.

## Anti-patterns

- Treating hot-to-cold movement as an outflow.
- Reading a single transaction as a trend.
- Ignoring market-maker wallets in the address set.
- Quoting netflow without the window.
- Inferring selling intention from a deposit without a counterparty class.

## Done checklist

- [ ] Address set built and classified.
- [ ] Intra-exchange transfers excluded.
- [ ] Netflow computed over a stated window.
- [ ] Largest contributors identified by class.
- [ ] Reserve disclosures compared where available.
- [ ] Inference recorded with confidence and falsifier.

## Sources

- Ethereum developer documentation on ledger data: <https://ethereum.org/en/developers/docs/>
- Empirical venue-flow measurement during stress: <https://arxiv.org/abs/2608.03616>
- Disclosure context for reserve attestations: <https://www.sec.gov/investor>

The strongest use of exchange flows is comparative: the same venue, the same window length, the same exclusions, across several periods. A single reading tells you almost nothing; a series built on a consistent rule tells you when the venue's behaviour changed, which is the question a trading decision actually needs answered.
