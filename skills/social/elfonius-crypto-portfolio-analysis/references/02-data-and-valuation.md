# 02 — Data Integrity and Valuation

## Purpose

Make every number reproducible and dated. A portfolio review is only as good as its weakest price, balance, or timestamp.

## Inputs

- Wallet addresses or exported positions; chain and contract identifiers.
- Price source(s), quote currency, and timestamp.
- Balance source(s): RPC, indexer, exchange export, protocol dashboard.
- Position type: spot, staked, locked, vesting, LP, lending collateral/debt, accrued rewards.
- FX rate and base currency.

## Method

1. Collect the primary balance and price source for each position.
2. Assign a fair-value tier and timestamp.
3. Reconcile against a second source.
4. Convert to the base currency.
5. Record unresolved differences and lower the data coverage.
6. Do not value an unpriced position at zero; mark it unassessable.

## Source hierarchy

1. **Primary chain/RPC or official protocol contract** — balances, debt, collateral, LP components.
2. **Official protocol API or dashboard** — pool state, rewards, governance.
3. **Independent market aggregator** — price and volume cross-check.
4. **Team/report/claim** — label `REPORTED`; never treat as verified.
5. **Model/scenario** — label `MODELED`; show assumptions.

Use the narrowest source that answers the question. Do not dump a full API response into the report.

## Fair-value hierarchy

Borrow the GIPS-style discipline:

- **Level 1:** quoted price for an identical asset in an active market.
- **Level 2:** quoted price for a similar asset, or observable inputs.
- **Level 3:** unobservable inputs, appraisal, or model value.

For Level 2/3 positions, state the method and a range. Do not present a model value with the same confidence as a live exchange price.

## Valuation rules

- Convert everything to one base currency; show the FX rate and date.
- Cross-check prices with a second source; if the difference is **>2%**, report both and do not average silently.
- Stablecoins: use market price, not the $1 label; check depeg history and redemption gates.
- LP tokens: value the redeemable claim, not the sum of the underlying tokens, unless redemption is actually available.
- Staked/locked assets: value the claim and note the unstake/vesting delay; do not add illiquid and liquid balances without a discount note.
- Accrued rewards: include only if claimable and valued; label unclaimed and illiquid rewards separately.
- Debt: subtract from the position value; show gross and net exposure.
- NFTs and illiquid assets: use a range and a liquidity discount; never a single floor price as fact.

## Reconciliation

1. Compare balance sources; record the difference.
2. Compare total value with the wallet/provider total.
3. Explain >2% differences (fees, pending tx, stale cache, missing position).
4. If unresolved, report `UNRECONCILED` and reduce data coverage.

## Data biases to check

- **Survivorship:** dead tokens/protocols omitted from the current list.
- **Look-ahead:** using a token that was listed later in a historical backtest.
- **Stale price:** low-liquidity token marked at the last trade.
- **Wash trading:** volume inflated by self-trades; check venue and maker/taker concentration.
- **Exchange vs on-chain:** custodial balances may not be verifiable on-chain.
- **Double counting:** the same exposure through a wrapper, LP, or staking receipt.
- **Timestamp mismatch:** prices from different times presented as one snapshot.

## Output

| Position | Quantity | Price | Source/time | Value | Fair-value tier | Reconciliation |
|---|---:|---:|---|---:|---|---|
| Example | 1.0 | $X | Source, UTC | $X | Level 1 | 0.3% |

Also state: data coverage %, stale positions, unresolved differences, and base currency/FX date.

## Failure modes

- Treating a dashboard total as audited.
- Using a stablecoin at $1 during a depeg.
- Counting the same LP exposure twice.
- Mixing price timestamps.
- Hiding an unreconciled balance inside “other.”

## Sources

- CFA Institute, *Overview of the Global Investment Performance Standards* (2026): fair value hierarchy, fees, TWR, no annualizing <1 year.
- DefiLlama, CoinGecko, Binance, Taostats probes (2026-10-30); see `12-methodology-and-sources.md`.
