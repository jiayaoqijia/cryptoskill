---
name: drift
description: "Inspect the legacy Drift Protocol integration and its availability limits. The original program is paused and hosted data endpoints are unavailable. Tools remain read-only and must not silently use Velocity data. Triggers: drift, drift protocol, SOL-PERP, drift funding, app.drift.trade."
---

# ChainGPT Drift Skill

The original Drift program is paused. The hosted `dlob.drift.trade` and
`data.api.drift.trade` services do not resolve from the validation environment.
Treat their market, orderbook, funding and account reads as unavailable until a
compatible legacy data source is independently verified. Do not recommend the
old trading or funding-arbitrage workflows as currently executable.

The [official migration guide](https://docs.velocity.exchange/developers/migrate-from-drift)
describes Velocity as a separate deployment with a new program ID and no
carried-over account state. Its quote asset and SDK also differ. Never return
Velocity markets, accounts or prices under the existing Drift tool names.
Adding Velocity requires a separately identified integration and validation.
Changing `SOLANA_RPC_URL` does not repair these HTTP data endpoints.

## Tools

All five tool names are retained for compatibility. They read legacy Drift data
and never sign or broadcast transactions.

| Tool | Legacy data |
|---|---|
| `chaingpt_drift_markets` | Perp market list |
| `chaingpt_drift_market` | One-market detail |
| `chaingpt_drift_orderbook` | L2 bids and asks |
| `chaingpt_drift_funding` | Funding history |
| `chaingpt_drift_user` | Account collateral, positions and orders |

`DRIFT_DLOB_URL` can select a trusted service implementing the legacy routes.
Verify its ownership, program identity, response schema, units and freshness
before using its output. The override does not resume the onchain program.
Do not connect a wallet, fund an account or initiate migration as part of
availability checks. Surface errors and missing coverage explicitly.

## Reference

- [Provider investigation and remaining gaps](../../docs/provider-warning-followup.md)
- [Legacy app pause notice](https://app.drift.trade/)
- Original Drift program: `dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH`
- Legacy public endpoints: `https://dlob.drift.trade`, `https://data.api.drift.trade`

These tools cost 0 ChainGPT credits. Successful fixture tests establish handler
behavior, not live availability or current market liquidity.
