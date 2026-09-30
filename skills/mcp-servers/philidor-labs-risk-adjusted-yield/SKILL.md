---
name: risk-adjusted-yield
description: >
  Use this when the user wants a risk-adjusted yield comparison across DeFi
  vaults: APR next to Philidor score, tier, TVL, and whether deposits are
  open. Cite only identifiers and figures the Philidor tools return.
---

# Risk-adjusted yield comparison

Compare yield only beside the risk evidence Philidor returns. Do not invent a risk-adjusted APY, a Sharpe-style ratio, or any score the tools did not return. If you rank vaults, say whether the list is a sample (a capped `search_vaults` page) or the top-10 audited screen from `find_safest_vaults`.

The hosted server is `https://mcp.philidor.io/api/mcp`.

## Steps

1. Call `search_vaults` with the filters the user named: `asset`, `chain`, `protocol`, `protocolVersion`, `riskTier` (`Prime`, `Core`, or `Edge`). Set `depositable` to `true` when they want vaults that can still be entered. Sort with `sortBy` `apr_net` or `tvl_usd` and `sortOrder` `asc` or `desc`. `limit` defaults to 10 and maxes at 50.
2. Aave V4 is `protocol=aave` and `protocolVersion=v4`. `aave-v4` is an accepted alias, not its own protocol id.
3. Keep base yield and reward APR as separate fields when the payload splits them. Do not add them into a number Philidor did not label.
4. Drop or flag rows the user cannot enter: deposit status `closed`. Keep `unknown` visible and label it unknown. Do not call an unknown row open.
5. For two or three finalists, call `compare_vaults`. `vaults` is an array of 2–3 objects, each with `network` and `address` copied from `search_vaults` or `get_vault`. Never type an address that no tool returned.
6. Call `get_vault_risk_breakdown` on a finalist when the user wants vector detail. Call `explain_risk_score` with a score that was returned. Read `philidor://methodology` before explaining the four vectors.
7. Call `find_safest_vaults` only for “safest” or “highest score” questions. It returns the top 10 audited vaults for the optional `asset`, `chain`, and `minTvl`. It does not rank by APR. A high score is lower assessed risk, not a guarantee.
8. If the client exposes MCP prompts, `defi_yield_comparison` takes optional `asset`, `chain`, and `riskTier`.

## Done when

- Every row shows the returned vault id, network, address, tier, score, TVL, and the APR labels the tool used.
- The answer states the filter and the cap (`limit` or top 10), so “highest APR” is not presented as the whole market.
- No risk figure appears that was not in a tool result from this turn.
