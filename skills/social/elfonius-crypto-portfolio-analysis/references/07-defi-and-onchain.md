# 07 — DeFi Positions and On-chain Flows

## Purpose

Evaluate DeFi positions as conditional claims with liquidation, oracle, contract, and contagion risk — and read on-chain flows as evidence, not decoration.

## Inputs

- Position, chain, contract, market, and LP identifiers.
- Collateral, debt, LTV, liquidation threshold, and oracle.
- Reward rate, reward token, and emission source.
- On-chain flow and holder data.

## Method

1. Resolve the exact chain, contract, market, and position.
2. Compute LTV, health factor, and liquidation distance.
3. Identify the oracle, close factor, and liquidation penalty.
4. Decompose LP yield into fees, incentives, and IL.
5. Map shared stablecoin, bridge, oracle, curator, and validator dependencies.
6. Read on-chain flows with venue and label confidence.
7. Flag any position that cannot be resolved exactly.

## Lending positions

Inputs: collateral asset and amount, debt asset and amount, LTV, liquidation threshold (LLTV), oracle, market isolation, close factor, penalties.

- `LTV = debt / collateral_value`.
- `Health factor = liquidation_value / debt`; below 1.0 means liquidatable.
- `Liquidation price = debt × LLTV / collateral_quantity` (adjust for decimals and oracle quote).
- Distance to liquidation = `(current_price − liquidation_price) / current_price`.

Check:

- Is the market isolated or shared?
- Which oracle and fallback? Is it stale/manipulable?
- Is the debt stablecoin or volatile?
- What is the close factor and liquidation penalty?
- Can the position be repaid/withdrawn under stress?
- Is the yield from borrowers or from token incentives?

## LP positions

- Value the redeemable claim, not the underlying sum.
- Impermanent loss: compare LP value with holding the two assets.
- APR decomposition: trading fees + protocol rewards + token emissions − IL − fees.
- Check pool depth, concentration, and withdrawal fees.
- Identify the pool’s dependency on one stablecoin, bridge, or oracle.

## Staking

- Validator identity and concentration.
- Unstake queue and unbonding period.
- Slashing conditions and historical incidents.
- Liquid staking receipt: issuer, redemption, peg, and smart-contract risk.
- Reward source: inflation, fees, or both.

## Derivatives

Perpetuals:

- Funding rate and basis; is the position paying or receiving?
- Open interest and liquidation cluster; where is the squeeze?
- Margin mode, maintenance margin, and liquidation price.
- Venue/counterparty: centralized exchange, on-chain perp, or synthetic.
- Oracle/index composition and mark-price manipulation risk.

Options:

- Delta, gamma, vega, theta; expiry and strike.
- Implied volatility vs realized; event risk.
- Counterparty and settlement; physical vs cash.
- Collateral and early-assignment risk.

Structured products:

- Principal protection: who guarantees it?
- Yield source: options premium, lending, or token emissions.
- Lock-up, redemption gate, and issuer credit risk.

Report derivatives separately from spot and DeFi; do not net them into “cash” without showing collateral and liquidation.

## Contagion map

| Shared dependency | Positions exposed | Failure mode |
|---|---|---|
| Stablecoin issuer | A, B | Depeg/redemption gate |
| Bridge | C, D | Pause/loss of wrapped asset |
| Oracle | E, F | Stale/manipulated price |
| Curator/vault | G, H | Withdrawal freeze/loss |
| Validator | I, J | Slashing/downtime |

One dependency can turn “different” positions into one trade.

## On-chain flows

Use:

- Exchange inflows/outflows, with venue labels and confidence.
- Holder cohorts and concentration.
- Whale/labeled entity flows; label as probabilistic.
- Net protocol flows, fees, and active users.
- Stablecoin mint/burn and chain distribution.

Limits:

- Exchange internal transfers can look like flows.
- Wash trading inflates volume.
- Entity labels are probabilistic.
- CEX balances are not fully verifiable on-chain.
- A flow is not a thesis; pair it with a mechanism.

## Output

| Position | Type | Collateral/debt or LP | Health/LTV | Oracle | Incident history | Exit path |
|---|---|---|---:|---|---|---|
| Example | Lending | $X / $Y | 1.4 | Chainlink | None found | Repay/withdraw |

Derivatives: add funding/basis, OI, liquidation, delta/vega, and counterparty in a separate table.

## Failure modes

- Approximating an LP token with its underlying assets.
- Ignoring the oracle and liquidation threshold.
- Treating emissions APR as organic yield.
- Counting the same stablecoin/bridge exposure twice.
- Reading exchange inflows as “selling” without venue context.

## Sources

- FSB, *The Financial Stability Risks of Decentralised Finance* (2023).
- arXiv 2507.08915, *Quantifying Crypto Portfolio Risk* (2025).
- Chainalysis, *2025 Crypto Theft Reaches $3.4 Billion* (2025-12-18).
