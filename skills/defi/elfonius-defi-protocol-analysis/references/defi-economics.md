# DeFi Economics

## Definitions first

Use one definition per metric and state it in the report. Aggregators disagree; a definition is not a fact until reconciled.

| Metric | Definition | What it is not |
|---|---|---|
| TVL | Reported value of user assets deposited in protocol contracts; clean for borrowed coins, own tokens, double counting and unproductive deposits, and state the adjustments | Revenue, executable liquidity or safety |
| Fees | Total value users pay for the service; the gross economic throughput | Protocol revenue |
| Supply-side revenue | Portion of fees paid to LPs, lenders, stakers, validators, integrators or referrers | Protocol profit |
| Revenue | Fees minus supply-side revenue; the protocol's retained share | Tokenholder distribution |
| Tokenholder revenue | Value reaching governance-token holders via buybacks, burns or distributions; label whether funded by receipts, treasury or external bribes/airdrops | Treasury-funded buybacks treated as organic or mint-and-burn accounting |
| Earnings | Revenue minus token incentives emitted in the same period | Free cash flow to holders |
| Market cap | Circulating supply × price | FDV |
| FDV | Maximum/expected supply × price | Current float value |
| P/F | Market cap or FDV ÷ annualized fees | P/E |
| P/S | Market cap or FDV ÷ annualized revenue | P/F |
| P/E | Market cap or FDV ÷ annualized earnings | A clean equity multiple |

A token with no fee switch, buyback, burn or distribution has **zero tokenholder revenue**. Its value then rests on governance, collateral utility, speculation or an expectation of future value capture, all of which must be labelled as such.

## Status and destination of value capture

- **Approved ≠ active.** For a buyback/burn, record the last execution date, pause status, funding source, budget, destination (burn / reserve / distribution) and whether acquired tokens can be resold.
- A paused buyback, or one that buys into a reserve, is **not current tokenholder yield**. Report current yield as zero and the program as a conditional catalyst.
- An announced tokenomics upgrade is not an approval. Require a formal proposal, vote, funding and execution before treating it as value capture.
- Separate protocol revenue, DAO revenue, net income and tokenholder revenue; they are different accounting layers and should not be subtracted from one another across sources.

## The fee-to-holder bridge

```
Activity (volume, borrows, swaps, stakes)
  → Gross fees (what users pay)
  → Supply-side revenue (LPs, lenders, validators, integrators)
  → Protocol revenue (treasury/team)
  → Tokenholder revenue (buyback, burn, distribution)
  → Earnings (protocol revenue − token incentives)
```

Compute each line for the same period and currency. A 90% fee-capture protocol is a different asset from a 1% capture protocol, even at the same TVL.

| Ratio | Formula | Use |
|---|---|---|
| Fee take rate | Fees ÷ volume or borrow volume | Pricing power / throughput |
| Revenue capture | Revenue ÷ fees | Value capture efficiency |
| Holder capture | Tokenholder revenue ÷ fees | What the token actually gets |
| Incentive intensity | Incentives ÷ revenue | How much activity is bought |
| Earnings margin | Earnings ÷ revenue | Sustainability after emissions |
| Fee/TVL | Annualized fees ÷ average TVL | Capital efficiency |
| Volume/TVL | Volume ÷ average TVL | Turnover, not demand quality |
| P/F | Valuation ÷ annualized fees | Gross-throughput multiple |
| P/S | Valuation ÷ annualized revenue | Retained-revenue multiple |
| P/E | Valuation ÷ annualized earnings | Post-incentive multiple |

Use trailing 12 months or a stated annualization; do not annualize a single day. Show market cap and FDV versions separately.

## Demand quality

- Cohort the usage: retail, institutional, integrators, bots and related parties. A large integrator can look like organic demand until it leaves.
- Paid versus incentivized: fees/interest paid by external users versus emissions, points or a related-party subsidy.
- Retention and repeat usage; a wallet count is not a user count.
- Concentration: top borrowers, depositors, traders, LPs and integrators.
- Geography/eligibility: demand that cannot legally use the product is not addressable demand.

## TVL quality

- Decompose by asset, chain, market and depositor cohort.
- Exclude or flag: own-token deposits, borrowed coins, recursive/looped deposits, double counting, unproductive one-sided pools and points-only deposits.
- Check whether TVL can actually be withdrawn: utilization, caps, queues, lockups and bridge latency.
- Compare TVL growth with fees, active users and retained users. TVL that grows while fees fall is usually incentives or a price effect.
- Protocol-owned liquidity vs rented liquidity: POL can support exit, but it is insider-controlled and may not be available to all users.
- Stablecoin TVL is not adoption; it can be idle, mercenary or double-counted.

## Yield decomposition

Four axes:

1. **Who pays?** Borrower interest, trader fees, staking rewards, MEV, RWA cash flow, protocol emissions, points, a related party or the treasury.
2. **Organic vs incentives:** Is the yield funded by external demand, or by token issuance/subsidy?
3. **Endogenous vs exogenous:** Does the yield depend on the protocol's own token/asset price or on an outside cash flow?
4. **Cash vs accrual:** Is it paid now, accrued, locked, queued or only mark-to-market?

Four realization filters:

- **Gross vs net:** subtract performance/management fees, gas, slippage and exit costs.
- **Denomination:** 8% in a volatile token is not 8% in USD.
- **Window:** 7-day, 30-day and since-inception differ; show the window.
- **Size:** the quoted APY may not survive the user's position size or exit.

Write the decomposition as a table: source, share of APY, organic/incentive, cash/accrual, risk it pays for.

## Unit economics

- Revenue per unit: per user, per market, per vault, per GPU/validator, per $1 of TVL.
- Lending denominators: fees/deposits, revenue/deposits, fees/loans, revenue/loans; state whether deposits are gross or net of borrows.
- Cost per unit: incentives, gas rebates, keeper payments, oracle costs, grants, security.
- Gross margin and contribution margin after incentives.
- CAC/payback only if acquisition spend is disclosed; otherwise mark not assessable.
- Treasury runway: liquid treasury ÷ monthly net burn; separate token holdings from stablecoins.
- Who funds the buyback/burn: revenue, treasury, new issuance or a related party.

## Valuation

Use the method that fits the cash-flow claim:

- **Fee/revenue multiples** for protocols with real, recurring fees; compare peers on the same definition and growth.
- **P/E or tokenholder-yield** only where tokenholder revenue is real and sustainable.
- **Reverse valuation:** what fee/revenue growth and margin does the current price imply? If the implied share or growth is implausible, say so.
- **Asset/treasury value** for protocols with a large liquid treasury; separate corporate treasury from user funds.
- **Option/value-of-network** for pre-fee-switch governance tokens; label it as a qualitative option, not a DCF.
- **Scenario range** with bear/base/bull and probability labels; include the total-loss branch.

Do not apply a DCF to a token with no enforceable cash-flow claim. Do not compare a P/S for a 90%-capture protocol with a P/S for a 1%-capture protocol without adjusting for the fee split.

## Common traps

- “TVL is $X, therefore the protocol is safe.”
- “APY is 20%, therefore the token is cheap.”
- “Fees are $X, therefore holders earn $X.”
- “Buyback” funded by the treasury or new issuance.
- “Buyback approved” without checking whether it is active, paused, or buys into a reserve rather than burning.
- Treating protocol revenue, DAO revenue and net income as the same number.
- Market cap compared across different float definitions.
- Annualizing one good week.
- Ignoring emissions and unlocks in “earnings.”
- Comparing a lending protocol's revenue with a DEX's fees.
- Counting the same TVL at every layer of a vault/loop.
- Treating points as cash yield before a confirmed conversion.
