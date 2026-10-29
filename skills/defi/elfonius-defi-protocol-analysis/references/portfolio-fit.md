# Portfolio Fit

## Cluster exposure

Count risk by cluster, not by product name. One cluster can include:

- the same contract stack or proxy admin;
- the same oracle class/provider;
- the same stablecoin or wrapper issuer;
- the same bridge or chain;
- the same curator/manager;
- the same collateral and liquidation venue.

Two “different” vaults can share 95% of exposure. Count the underlying once.

## Risk budget

| Risk | Measure | Why |
|---|---|---|
| Smart contract | Position size, audit coverage, TVL at risk | Total-loss tail |
| Stablecoin | Issuer, reserve, peg history, redemption | Depeg and gate |
| Bridge/chain | Validator model, latency, incidents | Frozen or lost assets |
| Oracle | Class, fallback, deviation, TVS | Liquidation/manipulation |
| Liquidity | Exit days at size, queue, depth | Forced sale |
| Governance | Upgrade/timelock, concentration | Control can change |
| Counterparty | Curator, RWA issuer, custodian | Off-chain failure |
| Regulatory | Jurisdiction, eligibility, sanctions | Access and exit |
| Tax/accounting | Income, cost basis, reporting | Net return |
| Insurance | Scope, limit, exclusions, claims | Residual risk |
| Yield | Organic vs incentives, duration | Sustainability |

## Correlation and drawdown

- Correlate the position with the user's existing book, not just BTC.
- Stress: BTC −30%, ETH −40%, stablecoin depeg 5%, bridge pause, oracle stale, top curator withdraws.
- Report the portfolio drawdown contribution, not only the standalone yield.
- Stablecoin yield is not “cash” if the issuer, bridge or curator can gate redemption.

## Suitability

Use only the constraints the user supplied:

- horizon;
- tolerable drawdown;
- liquidity needs and liability currency;
- jurisdiction/eligibility;
- existing concentration and leverage;
- tax status.

If absent: `suitability not assessable — requires <inputs>`. Never prescribe a position size without constraints. If sizing is requested, present a range with the loss-to-zero branch and the exit-capacity limit, not a single “safe” number.

## Behavioral biases

- Yield chasing and anchoring to the entry APY.
- Sunk cost after a loss; confirmation of a prior thesis.
- Recency after a good quarter; home/chain bias.
- Overconfidence in a familiar protocol; ignoring a changed admin or oracle.
- Treating insurance/backstop as a guarantee.

Separate the asset case from the ownership case. A good protocol can be a bad position at the wrong size, horizon or entry.

## Decision record

- Gate status and the component that decided it.
- Top three risks with probability/impact and the failure shape.
- Expected return range, including the total-loss branch.
- Two or three falsifiers.
- Monitoring dashboard: metric, current, threshold, source, frequency.
- What would make the position size smaller, not just the thesis wrong.
