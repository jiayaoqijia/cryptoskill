# DeFi Yield, Vaults and Structured Products

## Yield sources

| Source | Paid by | Risk it pays for |
|---|---|---|
| Trading fees | Traders | Market making, IL/LVR, inventory risk |
| Borrow interest | Borrowers | Credit, collateral, liquidation, liquidity |
| Staking rewards | Protocol inflation / fees | Validator/slashing, lockup, MEV |
| MEV | Searchers/traders | Order flow, latency, censorship |
| RWA cash flow | Off-chain borrower/issuer | Credit, duration, custody, legal |
| Funding/basis | Perp traders | Basis, venue, liquidation |
| Token emissions | Protocol | Dilution, mercenary liquidity |
| Points | Protocol/airline-style program | Unconfirmed conversion, dilution |
| Related-party subsidy | Team/treasury | Withdrawal risk, sustainability |

An APY is a claim about a source. If the source cannot be named, the yield is not understood.

## APY decomposition

Four axes:

1. **Who pays:** external borrower/trader vs protocol emissions vs treasury/related party.
2. **Organic vs incentives:** fees/interest vs token printing.
3. **Endogenous vs exogenous:** depends on the protocol's own token/asset vs an outside cash flow.
4. **Cash vs accrual:** paid, accrued, locked, queued or mark-to-market.

Four filters:

- Gross vs net of performance/management fees, gas, slippage and exit costs.
- Denomination: USD vs ETH vs the protocol token.
- Window: 7-day, 30-day, since inception; show the window.
- Size: does the quoted rate survive the user's position and exit?

## Vaults and curators

- Five layers: venue protocol, vault infrastructure, curator, underlying assets/counterparties, distribution.
- Curator mandate, discretion, track record, fees, skin in the game and risk limits.
- Allocation by market/asset/chain; look through nested vaults to the leaves.
- Caps, liquidity buffer, queue/epoch, redemption terms and who can change them.
- First-loss/backstop: who absorbs a loss before depositors?
- Curator conflicts: affiliated market, oracle, backstop or service provider.
- A curator's past APY is not a promise; request stress behavior and time-to-exit.

## Looping and composed positions

```
Net carry = Σ(leg yield) − Σ(borrow cost) × leverage − entry/exit/gas
```

- Evaluate the construction as one position, not separate legs.
- Risks compound; the position fails if any leg fails.
- Oracle class per leg; liquidation fires on the collateral leg's mark.
- Liquidation distance at the position's LTV; stress the collateral move.
- Unwind path in reverse order; queues add up; one gate traps the whole position.
- Double-count check: the same TVL can appear at every layer; count cluster exposure once.

## Restaking and LST/LRT

- Validator/operator set, slashing conditions and reward source.
- Restaking layer/AVS exposure; penalties pass through to the LST/LRT holder?
- Withdrawal queue and secondary-market peg; depeg history.
- Governance/upgrade control at each layer; a safe LST on an unsafe restaking layer is not safe.
- Yield is compensation for slashing and liquidity risk, not free yield.

## RWA and tokenized funds

- Legal claim, issuer, custodian, fund administrator, auditor and NAV reporter.
- Mint/redemption windows, transfer restrictions, eligibility and secondary market.
- NAV oracle/attestation cadence and stale-price controls.
- Credit, duration, liquidity and counterparty risk of the underlying.
- Fee stack: issuer, curator, custodian, administrator; what does the holder keep?
- A tokenized fund is a legal wrapper, not a trustless protocol.

## Points and airdrops

- Points are not cash; conversion, supply, vesting and eligibility are unknown until announced.
- Value the points case separately and label it speculative.
- Check whether the protocol can change the program retroactively.
- Do not include points at face value in a base-case yield.

## Structured products and options

- Payoff, Greeks, collateral, counterparty and path dependency.
- Oracle/settlement source and early-exercise/knock-in terms.
- Who is short the tail; is the yield a premium for selling insurance?
- Liquidity of the hedge and the unwind path.
- Fee stack; compare with a simple alternative.

## Red flags

- APY far above its decomposable sources.
- Yield paid in the product's own token or points.
- 100% utilization on an exit-relevant market.
- NAV oracle controlled by the party being priced, with no bounds.
- Backstop provided by an affiliate of the manager.
- “Diversified” name over concentrated composition.
- Recently changed redemption terms or a queue that appeared in stress.
- Anonymous manager with no inspectable incident history.
- Incentives masking the organic rate.
- Refusal or inability to reproduce the numbers from public data.
